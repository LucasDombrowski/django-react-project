from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse
from django.views import View # Import Django's base View class

from django_bridge.response import Response

from ..forms import LoginForm, RegistrationForm # Use relative import for forms

class AuthController(View):
    def _get_common_props(self, request):
        current_user_data = None
        if request.user.is_authenticated:
            current_user_data = {
                "id": request.user.id,
                "username": request.user.username,
                "score": getattr(request.user, 'score', 0) # Safely access score
            }
        return {
            "isAuthenticated": request.user.is_authenticated,
            "currentUser": current_user_data,
        }

    def display_login_form(self, request, *args, **kwargs):
        form = LoginForm(request)
        props = {
            'form': form,
            'action_url': reverse('login'),
            **self._get_common_props(request)
        }
        return Response(request, "LoginView", props)

    def handle_login_submission(self, request, *args, **kwargs):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('home')) 
        
        props = {
            'form': form,
            'action_url': reverse('login'),
            **self._get_common_props(request)
        }
        return Response(request, "LoginView", props) 

    # Registration methods will be added in the next step 

    # --- Registration Methods --- 
    def display_registration_form(self, request, *args, **kwargs):
        form = RegistrationForm()
        props = { 
            'form': form,
            'action_url': reverse('register'),
            **self._get_common_props(request)
        }
        return Response(request, "RegisterView", props)

    def handle_registration_submission(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            return redirect(reverse('home')) 
        
        props = {
            'form': form,
            'action_url': reverse('register'),
            **self._get_common_props(request)
        }
        return Response(request, "RegisterView", props) 