from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Article, Comment


class UserArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title"]


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "tags"]
        widgets = {
            "tags": widgets.CheckboxSelectMultiple,
            "content": widgets.Textarea(attrs={"placeholder": "введите контент"})
        }

    def clean(self):
        if self.cleaned_data.get("title") == self.cleaned_data.get("content"):
            raise ValidationError("Название и описание не могут совпадать")
        return super().clean()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class ArticleDeleteForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title"]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if self.instance.title != title:
            raise ValidationError("Названия не совпадают")
        return title
