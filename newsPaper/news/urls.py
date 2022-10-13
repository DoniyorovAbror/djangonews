from django.urls import path
from .views import ListNews, DetailNews

urlpatterns = [path('', ListNews.as_view()),
               path('<int:pk>', DetailNews.as_view())]
