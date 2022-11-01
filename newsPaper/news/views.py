from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import ArticleForm, NewsForm
from .models import Post


class ListNews(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = "newslist.html"
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetailNews(DetailView):
    model = Post
    template_name = 'newsdetail.html'
    context_object_name = "anews"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['same_post_author'] = self.get_object().author.authorUser.id
        return context
    
    
class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    model = Post
    template_name = 'editnews.html'
    form_class = NewsForm
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = Post.NEWS
        return super().form_valid(form)


class CreateArticle(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'editnews.html'
    form_class = ArticleForm
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = Post.ARTICLE
        return super().form_valid(form)
    
    
class UpdateNews(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    template_name = 'editnews.html'
    form_class = NewsForm
    success_url = reverse_lazy('post_list')


class DeleteNews(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'newsdelete.html'
    success_url = reverse_lazy('post_list')
    