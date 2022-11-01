from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group


class CustomSignUpForm(SignupForm):
    email = forms.EmailField(required= True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name = 'common_users')
        user.groups.add(common_users)
        return user
    
        