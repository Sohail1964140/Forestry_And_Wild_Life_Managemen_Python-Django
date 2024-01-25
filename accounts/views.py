from typing import List
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from . forms import  UserForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.

class RegistrationView(CreateView):
    
    model = get_user_model()
    template_name = 'accounts/register.html'
    form_class = UserForm
    success_url = reverse_lazy('account:signUp')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User created successfully!')
        return response


class SignInView(LoginView):
    
    template_name = 'accounts/login.html'
    

    
class userLogoutView(LogoutView):
    
    def get_template_names(self) -> List[str]:
        return ['index.html']
    

class userPasswordChangeView(PasswordChangeView):
    template_name='accounts/passwordChange.html'
    success_url='accounts/passwordChangeDone/'



