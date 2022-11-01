import django_filters
from django import forms
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post, Author, Category


class PostFilter(FilterSet):
    # author = django_filters.ModelChoiceFilter(
    #     lookup_expr='exact',
    #     field_name='author',
    #     queryset=Author.objects.all(),
    #     label='Автор',
    #     empty_label='Все',
    # )

    title = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='title',
        label='Название',
        widget=forms.TextInput(attrs={'class': 'me-2'})
    )
    text = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='text',
        label='Содержание',
        widget=forms.TextInput(attrs={'class': 'me-2'})
    )
    postCategory = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        field_name='postCategory',
        queryset= Category.objects.all(),
        label='Тип',
        empty_label='Все',
        widget=forms.Select(attrs={'class':'me-2'})
    )
    categoryType = django_filters.ChoiceFilter(
        lookup_expr='exact',
        field_name='categoryType',
        choices = Post.CATEGORY_CHOICES,
        label = 'Категория',
        empty_label = 'Все',
        widget = forms.Select(attrs={'class': 'me-2'})
    )
    dateCreation_gt = django_filters.DateFilter(
        lookup_expr='gt',
        field_name='dateCreation',
        label='С',
        widget=DateInput(attrs={'type': 'date', 'class': 'me-2'})
    )
    dateCreation_lt = django_filters.DateFilter(
        lookup_expr='lt',
        field_name='dateCreation',
        label='По',
        widget=DateInput(attrs={'type': 'date', 'class': 'me-2'})
    )
    
    class Meta:
        model = Post
        fields = []
        