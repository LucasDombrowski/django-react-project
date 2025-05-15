from django.shortcuts import redirect
from django.contrib.auth import login # Removed unused 'authenticate'
from django.urls import reverse

from django_bridge.response import Response

# Removed direct import of LoginForm as it's handled by the controller
from .controllers.auth_controller import AuthController # Import the controller

def home(request):
    return Response(request, "Home", {})

def login_view(request):
    auth_controller = AuthController()
    if request.method == 'POST':
        return auth_controller.handle_login_submission(request)
    else: # GET or other methods
        return auth_controller.display_login_form(request)

def registration_view(request):
    auth_controller = AuthController() # Re-instantiate or use a single instance if appropriate
    if request.method == 'POST':
        return auth_controller.handle_registration_submission(request)
    else: # GET or other methods
        return auth_controller.display_registration_form(request)
