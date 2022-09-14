from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

# Create your views here.
from django.utils.http import urlencode
from django.views import View

from webapp.forms import ArticleForm, SearchForm, ArticleDeleteForm, UserArticleForm
from webapp.models import Article
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from article_project.source.webapp.models import LikeArticle


class IndexView(ListView):
    model = Article
    template_name = "articles/index.html"
    context_object_name = "articles"
    ordering = "-updated_at"
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        # print(request.user.user_permissions.all())
        # request.user.user_permissions.add(Permission.objects.get(codename="delete_article"))
        # print(request.user.user_permissions.all())
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Article.objects.filter(
                Q(author__icontains=self.search_value) |
                Q(title__icontains=self.search_value)).order_by("-updated_at")
        return Article.objects.all().order_by("-updated_at")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})  # search=dcsdvsdvsd
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ArticleView(DetailView):
    template_name = "articles/article_view.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by("-created_at")
        return context


class CreateArticle(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = "articles/create.html"

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and self.request.user.has_perm("webapp.add_article"):
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect("accounts:login")

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)


class UpdateArticle(PermissionRequiredMixin, UpdateView):
    form_class = ArticleForm
    template_name = "articles/update.html"
    model = Article

    def has_permission(self):
        return self.request.user.has_perm("webapp.change_article") or \
               self.request.user == self.get_object().author


class DeleteArticle(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "articles/delete.html"
    success_url = reverse_lazy('webapp:index')
    form_class = ArticleDeleteForm
    permission_required = "webapp.delete_article"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

        # return self.request.user.is_superuser or \
        #        self.request.user.groups.filter(name__in=("Модераторы",)).exists()

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            return self.delete(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)


class ArticleLikeCreate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        if LikeArticle.objects.filter(user=user, article_id=pk).exists():
            return HttpResponse(status=403, content='Лайк уже есть')
        LikeArticle.objects.create(user=user, article_id=pk)
        count = LikeArticle.objects.filter(article_id=pk).count()
        return JsonResponse({'count': count, 'action': 'like', 'pk': pk})


class ArticleLikeDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        if LikeArticle.objects.filter(user=user, article_id=pk).exists():
            return HttpResponse(status=403, content='Лайка не было')
        LikeArticle.objects.create(user=user, article_id=pk).delete()
        count = LikeArticle.objects.filter(article_id=pk).count()
        return JsonResponse({'count': count, 'action': 'like', 'pk': pk})
