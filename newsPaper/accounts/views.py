from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import CustomSignUpForm


class SignUp(CreateView):
    model = User
    form_class = CustomSignUpForm
    success_url = '/accounts/login'
    template_name = 'allauth/account/signup.html'
    

class Login(CreateView):
    model = User
    form_class = CustomSignUpForm
    success_url = 'news/'
    template_name = 'login.html'
    