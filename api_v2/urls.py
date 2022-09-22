from django.urls import path

from api_v2.views import ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

app_name = 'api_v2'

urlpatterns = [
    path('article/', ArticleListView.as_view(), name='article'),
    path('article/create', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/update', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDeleteView.as_view(), name='article_delete')
]
