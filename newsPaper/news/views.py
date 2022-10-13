from django.views.generic import ListView, DetailView

from .models import Post

# Create your views here.
class ListNews(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = "newslist.html"
    context_object_name = 'news'
  
class DetailNews(DetailView):
    model = Post
    template_name = 'newsdetail.html'
    context_object_name = "anews"
    