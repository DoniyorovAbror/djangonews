from django.urls import path
from .views import *

urlpatterns = [
    # path('', IndexView.as_view()),
    path('', ListNews.as_view(), name= 'post_list'),
    path('<int:pk>', DetailNews.as_view(), name= 'post_detail'),
    path('search/', ListNews.as_view(), name= 'search'),
    path('news/create/', CreateNews.as_view(), name= 'news_create'),
    path('article/create/', CreateArticle.as_view(), name= 'article_create'),
    path('news/<int:pk>/edit', UpdateNews.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', DeleteNews.as_view(), name='news_delete'),
    path('article/<int:pk>/edit', UpdateNews.as_view(), name='article_edit'),
    path('article/<int:pk>/delete', DeleteNews.as_view(), name='article_delete'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
]

