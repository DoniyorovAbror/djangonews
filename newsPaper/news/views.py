from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import ArticleForm, NewsForm
from .models import Post, Category, User
from .tasks import notify_subscribers


# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10], eta=datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')
    
    
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
        if self.request.user in User.objects.all():
            today = datetime.now()
            today = today.replace(hour=0, minute=0, second=0)
            context['author_post'] = Post.objects.filter(author__authorUser=self.request.user).filter(dateCreation__gte=today).count
        return context
    

class DetailNews(DetailView):
    model = Post
    template_name = 'newsdetail.html'
    context_object_name = "anews"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['same_post_author'] = self.get_object().author.authorUser.id
        context['is_subscribed'] = Category.objects.filter(subscribers=self.request.user.id)
        return context

    
@login_required
def subscribe(request, *args, **kwargs):
    Category.objects.get(pk=int(kwargs['pk'])).subscribers.add(request.user.id)
    
    return redirect('/')


@login_required
def unsubscribe(request, *args, **kwargs):
    Category.objects.get(pk=int(kwargs['pk'])).subscribers.remove(request.user.id)
    
    return redirect('/')

    
class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    model = Post
    template_name = 'editnews.html'
    form_class = NewsForm
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = Post.CATEGORY_CHOICES
        context['categories'] = Category.objects.all
        return context
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = Post.NEWS
        post.save()
        notify_subscribers.apply_async([post.pk], countdown = 60)
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
        post.save()
        notify_subscribers.apply_async([post.pk], countdown=60)
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
    