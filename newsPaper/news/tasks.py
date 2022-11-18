from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from .models import Post, Category
from celery import shared_task


@shared_task
def notify_subscribers(postid):
    # if kwargs['action'] == 'post_add':
    post = Post.objects.get(pk=postid)
    categories = post.postCategory.all()
    subscribers = []
    for cats in categories:
        subscribers += cats.subscribers.all()
        
    username = [usr.username for usr in subscribers]
    subscribers = [usr.email for usr in subscribers]
        
    html_content = render_to_string(
        template_name='subscribers_email_notify.html',
        context={
            'text': post.preview(),
            'post_link': f'{settings.SITE_URL}/{post.id}',
            'username': username,
        }
    )
    msg = EmailMultiAlternatives(
        subject=post.title,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def notify_subscribers_weekly():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week).order_by('-dateCreation')
    categories = set(posts.values_list('postCategory__name', flat=True))
    username = set(
        Category.objects.filter(name__in=categories).values_list('subscribers__username', flat=True))
    subscribers = set(
        Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    
    html_content = render_to_string(
        template_name='subscribers_email_notify_weekly.html',
        context={
            'posts': posts,
            'posts_link': settings.SITE_URL,
            'username': username,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Посты за неделю',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    