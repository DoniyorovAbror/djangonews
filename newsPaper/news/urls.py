from django.urls import path
from .views import *

urlpatterns = [
    path('', ListNews.as_view(), name= 'post_list'),
    path('<int:pk>', DetailNews.as_view()),
    path('search/', ListNews.as_view()),
    path('news/create/', CreateNews.as_view()),
    path('article/create/', CreateArticle.as_view()),
    path('news/<int:pk>/edit', UpdateNews.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', DeleteNews.as_view(), name='news_delete'),
    path('article/<int:pk>/edit', UpdateNews.as_view(), name='article_edit'),
    path('article/<int:pk>/delete', DeleteNews.as_view(), name='article_delete'),
]
