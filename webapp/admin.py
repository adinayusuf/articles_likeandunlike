from django.contrib import admin

# Register your models here.
from webapp.models import Article, Tag, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_display_links = ['title']
    list_filter = ['author']
    search_fields = ['title', 'content']
    fields = ['title', 'author', 'content', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Article, ArticleAdmin)
