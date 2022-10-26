from django import forms

from news.models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',  'text', 'postCategory', 'author']
        labels = {
            'title': 'Название',
            'text' : 'Контент',
            'postCategory' : 'Категория',
            'author' : 'Автор'
        }
        
        
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'postCategory',  'author']
        labels = {
            'title': 'Название',
            'text': 'Контент',
            'postCategory': 'Категория',
            'author': 'Автор'
        }

