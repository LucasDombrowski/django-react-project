from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse
from django.views import View # Import Django's base View class

from django_bridge.response import Response

from ..forms import LoginForm, RegistrationForm # Use relative import for forms

class AuthController(View):
    def display_login_form(self, request, *args, **kwargs):
        form = LoginForm(request)
        return Response(request, "LoginView", {
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
        return Response(request, "LoginView", {
            'form': form,
            'action_url': reverse('login')
        }) 

    # Registration methods will be added in the next step 

    # --- Registration Methods --- 
    def display_registration_form(self, request, *args, **kwargs):
        form = RegistrationForm()
        return Response(request, "RegisterView", { # Assuming React component will be RegisterView
            'form': form,
            'action_url': reverse('register') # Assuming URL name will be 'register'
        })

    def handle_registration_submission(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST) # Pass request.POST data
        if form.is_valid():
            user = form.save() # UserCreationForm's save method creates the user
            login(request, user) # Log the user in directly after registration
            return redirect(reverse('home')) # Redirect to home or a welcome page
        
        # If form is invalid, re-render the RegisterView with the form containing errors
        return Response(request, "RegisterView", {
            'form': form,
            'action_url': reverse('register')
        }) 