from django.shortcuts import redirect
from django.contrib.auth import login # Removed unused 'authenticate'
from django.urls import reverse
from django.http import Http404 # Added for match_detail_view

from django_bridge.response import Response

# Removed direct import of LoginForm as it's handled by the controller
from .controllers.auth_controller import AuthController # Import the controller
from .controllers.match_controller import MatchController # Import the MatchController
from .controllers.competition_controller import CompetitionController # Import the CompetitionController

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

def match_detail_view(request, match_id):
    controller = MatchController()
    if request.method == 'POST':
        return controller.handle_bet_submission(request, match_id)
    else: # GET or other methods
        return controller.render_match_detail_page(request, match_id)

def competition_detail_view(request, competition_id):
    controller = CompetitionController()
    # This page is likely to be GET only for now, unless we add forms later
    return controller.render_competition_detail_page(request, competition_id)
