from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django_bridge_project.models import Match # Assuming models.py is in the same app
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt # If you need to exempt CSRF for API-like views
from django_bridge.response import Response # ADDED
from django_bridge_project.forms.utils.bet_form_utils import BetFormGenerator # Import BetFormGenerator
from django.middleware.csrf import get_token # Import get_token
from django.urls import reverse # To generate action_url

# It's good practice to define a base controller if you have common functionalities
# For now, we'll create a simple controller

class MatchController(View):
    """
    Controller to handle requests related to a single match.
    """

    def render_match_detail_page(self, request, match_id):
        """
        Fetches match data, creates a betting form, and renders the MatchDetail React component page.
        """
        try:
            match_instance = get_object_or_404(Match, pk=match_id) # Renamed for clarity

            # Helper to serialize a competition
            def serialize_competition(competition):
                if not competition:
                    return None
                logo_url = None
                if competition.logo and hasattr(competition.logo, 'url'):
                    logo_url = request.build_absolute_uri(competition.logo.url)
                return {
                    "id": competition.id,
                    "name": competition.name,
                    "logo_url": logo_url
                }

            # Helper to serialize a team
            def serialize_team(team):
                if not team:
                    return None
                logo_url = None
                if team.logo and hasattr(team.logo, 'url'):
                    logo_url = request.build_absolute_uri(team.logo.url)
                
                players_data = []
                for player in team.players.all(): # Access players via related_name
                    photo_url = None
                    if player.photo and hasattr(player.photo, 'url'):
                        photo_url = request.build_absolute_uri(player.photo.url)
                    players_data.append({
                        "id": player.id,
                        "first_name": player.first_name,
                        "last_name": player.last_name,
                        "nickname": player.nickname,
                        "role": player.role,
                        "photo_url": photo_url
                    })

                return {
                    "id": team.id,
                    "name": team.name,
                    "logo_url": logo_url,
                    "players": players_data,
                    # Add other team fields if needed
                }

            # Prepare predictions data
            predictions_data = []
            for pred in match_instance.predictions.all():
                predictions_data.append({
                    "id": pred.id,
                    "label": pred.label,
                    "prediction_type": pred.prediction_type,
                    "score_points": pred.score_points,
                    "correct_value": pred.correct_value, # Will be None if not set
                })

            # For now, let's prepare some basic data
            # We can expand this later to include more details like predictions, teams, etc.
            match_data = {
                "id": match_instance.id,
                "name": str(match_instance), # Using the __str__ method for a general name
                "competition": serialize_competition(match_instance.competition),
                "team_one": serialize_team(match_instance.team_one),
                "team_two": serialize_team(match_instance.team_two),
                "team_one_score": match_instance.team_one_score,
                "team_two_score": match_instance.team_two_score,
                "start_datetime": match_instance.start_datetime.isoformat(),
                "is_finished": match_instance.is_finished,
                "is_winner_needed": match_instance.is_winner_needed,
                "team_one_draw_score": match_instance.team_one_draw_score,
                "team_two_draw_score": match_instance.team_two_draw_score,
                "score_points": match_instance.score_points,
                "predictions": predictions_data,
            }

            # Create the betting form instance
            bet_form = BetFormGenerator.create_bet_form_for_match(match_instance, request=request)
            
            props = {
                "match": match_data,
                "bet_form": bet_form,
                "isAuthenticated": request.user.is_authenticated,
                "csrfToken": get_token(request),
                "action_url": reverse('match_detail', kwargs={'match_id': match_id})
            }
            
            return Response(request, "MatchDetailView", props)
        except Http404:
            raise # Re-raise the Http404 exception to be handled by Django
