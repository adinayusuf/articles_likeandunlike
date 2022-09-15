from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Case, When, BooleanField
from django.http import HttpResponse, JsonResponse

from django.urls import reverse_lazy

# Create your views here.
from django.utils.http import urlencode
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import SearchForm, ArticleForm, ArticleDeleteForm
from webapp.models import LikeArticle, Article


class IndexView(ListView):
    model = Article
    template_name = "articles/index.html"
    context_object_name = "articles"
    ordering = "-updated_at"
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-updated_at")
        if self.search_value:
            queryset = Article.objects.filter(
                Q(author__icontains=self.search_value) |
                Q(title__icontains=self.search_value)).order_by("-updated_at")
        queryset = queryset.annotate(
            is_liked=Case(
                When(likes__user_id=self.request.user.id,
                     then=True),
                default=False,
                output_field=BooleanField()))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
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
            return HttpResponse(status=403, content={})
        LikeArticle.objects.create(user=user, article_id=pk)
        count = LikeArticle.objects.filter(article_id=pk).count()
        return JsonResponse({'count': count, 'action': 'like', 'pk': pk})


class ArticleLikeDelete(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        if not LikeArticle.objects.filter(user=user, article_id=pk).exists():
            return HttpResponse(status=403, content={})
        LikeArticle.objects.get(user=user, article_id=pk).delete()
        count = LikeArticle.objects.filter(article_id=pk).count()
        return JsonResponse({'count': count, 'action': 'unlike', 'pk': pk})
