from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import User


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = User.objects.get(email=email_address.email)
    user.is_active = True
    user.save()
    
    html_content = render_to_string(
        template_name= 'welcome.html',
        context={'user' : user.username, 'site_url' : f'{settings.SITE_URL}'}
    )
    send_mail(
        subject= 'Добро пожаловать наш сайт',
        message= '',
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = (user.email,),
        html_message = html_content,
    )