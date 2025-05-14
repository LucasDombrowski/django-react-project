from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views import View # Import Django's base View class

from django_bridge.response import Response

from ..forms import LoginForm # Use relative import for forms

class AuthController(View):
    def display_login_form(self, request, *args, **kwargs):
        form = LoginForm(request)
        return Response(request, "Login", {
            'form': form,
            'action_url': reverse('login') 
        })

    def handle_login_submission(self, request, *args, **kwargs):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('home')) 
        
        # If form is invalid, re-render the LoginView with the form containing errors
        return Response(request, "Login", {
            'form': form,
            'action_url': reverse('login')
        }) 