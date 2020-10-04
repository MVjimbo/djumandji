from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView


class MySignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/register.html'
    success_url = '/'


class MyLogInView(LoginView):
    template_name = "user/login1.html"
    redirect_authenticated_user = True
