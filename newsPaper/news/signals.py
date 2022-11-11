from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from newsPaper.settings import DEFAULT_FROM_EMAIL, SITE_URL
from .models import PostCategory, Post

from django.shortcuts import get_object_or_404


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    # print(kwargs['action'])
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers = []
        for cats in categories:
            subscribers += cats.subscribers.all()
        
        username = [usr.username for usr in subscribers]
        subscribers = [usr.email for usr in subscribers]
        
        html_content = render_to_string(
            template_name='subscribers_email_notify.html',
            context={
                'text': instance.preview(),
                'post_link': f'{SITE_URL}/{instance.id}',
                'username': username,
            }
        )
        msg = EmailMultiAlternatives(
            subject=instance.title,
            from_email=DEFAULT_FROM_EMAIL,
            to=subscribers,
        )
        
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

