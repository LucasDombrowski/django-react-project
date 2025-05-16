from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django_bridge_project.models import Match, Bet, Answer, Team, Prediction # Added Bet, Answer, Team, Prediction
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt # If you need to exempt CSRF for API-like views
from django_bridge.response import Response # ADDED
from django_bridge_project.forms.utils.bet_form_utils import BetFormGenerator # Import BetFormGenerator
from django.middleware.csrf import get_token # Import get_token
from django.urls import reverse # To generate action_url
from django.contrib import messages as django_messages # Use an alias
from django.db import transaction # Added transaction for atomic operations
from .utils.match_data_helper import MatchDataHelper # Import the new helper
from .utils.user_bet_data_helper import UserBetDataHelper # Import the new helper

# It's good practice to define a base controller if you have common functionalities
# For now, we'll create a simple controller

class MatchController(View):
    """
    Controller to handle requests related to a single match.
    """

    def render_match_detail_page(self, request, match_id, bet_form_instance=None):
        """
        Fetches match data, creates/uses a betting form, and renders the MatchDetail React component page.
        """
        try:
            match_instance = get_object_or_404(Match, pk=match_id)

            # Use the helper to get match_data
            helper = MatchDataHelper(request, match_instance)
            match_data = helper.get_match_data()

            user_bet_details = None
            if request.user.is_authenticated:
                bet_helper = UserBetDataHelper(request.user, match_instance)
                user_bet_details = bet_helper.get_user_bet_details()

            # Use the passed form instance if available (e.g., from a failed POST)
            # Or if a bet already exists, we don't need to generate/pass the form for new betting
            final_bet_form = None
            if not user_bet_details: # Only prepare a new form if no existing bet
                final_bet_form = bet_form_instance if bet_form_instance is not None else BetFormGenerator.create_bet_form_for_match(match_instance, request=request)
            
            # Extract messages for React
            contrib_messages = django_messages.get_messages(request)
            messages_for_react = []
            for message in contrib_messages:
                messages_for_react.append({
                    'text': str(message),
                    'level': message.level_tag, # e.g., 'debug', 'info', 'success', 'warning', 'error'
                })

            props = {
                "match": match_data,
                "bet_form": final_bet_form, 
                "isAuthenticated": request.user.is_authenticated,
                "csrfToken": get_token(request),
                "action_url": reverse('match_detail', kwargs={'match_id': match_id}),
                "messages": messages_for_react,
                "user_bet_details": user_bet_details # Add user_bet_details to props
            }
            
            return Response(request, "MatchDetailView", props)
        except Http404:
            raise

    @transaction.atomic # Ensure all database operations are atomic
    def handle_bet_submission(self, request, match_id):
        if not request.user.is_authenticated:
            django_messages.error(request, "You must be logged in to place a bet.")
            # Redirect to login or simply re-render; re-rendering keeps them on the page
            # but they won't be able to submit. The form is already disabled on frontend.
            # For a server-side redirect to login:
            # return redirect(f"{reverse('login')}?next={reverse('match_detail', kwargs={'match_id': match_id})}")
            # For now, re-rendering the page which will show the form disabled and login prompt.
            return self.render_match_detail_page(request, match_id)

        try:
            match_instance = get_object_or_404(Match, pk=match_id)
        except Http404:
            raise

        # Check if the match is already finished
        if match_instance.is_finished:
            django_messages.error(request, "This match has already finished. Betting is closed.")
            return self.render_match_detail_page(request, match_id)

        if Bet.objects.filter(user=request.user, match=match_instance).exists():
            django_messages.warning(request, "You have already placed a bet on this match.") # Ensure message is set before re-render
            return self.render_match_detail_page(request, match_id) # Re-render with the message

        bet_form = BetFormGenerator.create_bet_form_for_match(match_instance, request=request) # Binds POST data

        if bet_form.is_valid():
            try:
                # Instantiate the helper (it needs request for building URIs, though not strictly for saving bet here)
                # but it was already instantiated in render_match_detail_page. We might need it if we re-render.
                # For saving, we primarily need match_instance which helper would have if pre-instantiated.
                # Let's assume we pass request and match_instance to it as before, or ensure it has them.
                # Actually, helper is not instantiated in this path yet. Let's instantiate it.
                helper = MatchDataHelper(request, match_instance) # Instantiate helper

                helper.save_bet_from_form_data(
                    user=request.user,
                    cleaned_data=bet_form.cleaned_data
                )

                django_messages.success(request, "Your bet has been placed successfully!")
                return redirect(reverse('match_detail', kwargs={'match_id': match_id}))
            except Http404: # Raised if get_object_or_404 fails for team or prediction inside helper
                django_messages.error(request, "Error finding team or prediction details. Bet not placed.")
                # Transaction will rollback
                return self.render_match_detail_page(request, match_id, bet_form_instance=bet_form)
            except ValueError: # Raised if int conversion for prediction_id fails in helper
                django_messages.error(request, "Error processing prediction data. Bet not placed.")
                return self.render_match_detail_page(request, match_id, bet_form_instance=bet_form)
            except Exception as e:
                # Catch any other unexpected errors during bet processing
                django_messages.error(request, f"An unexpected error occurred: {str(e)}. Bet not placed.")
                # Transaction will rollback
                return self.render_match_detail_page(request, match_id, bet_form_instance=bet_form)
        else:
            # Form is not valid, re-render the page with the form containing errors
            django_messages.error(request, "Please correct the errors in the form below.")
            # We need to pass the invalid form instance to render_match_detail_page
            # so it can be used in the props.
            # Modifying render_match_detail_page to accept an optional form instance.
            return self.render_match_detail_page(request, match_id, bet_form_instance=bet_form)
