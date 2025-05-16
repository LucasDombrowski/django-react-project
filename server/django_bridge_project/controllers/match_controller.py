from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django_bridge_project.models import Match # Assuming models.py is in the same app
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt # If you need to exempt CSRF for API-like views
from django_bridge.response import Response # ADDED

# It's good practice to define a base controller if you have common functionalities
# For now, we'll create a simple controller

class MatchController(View):
    """
    Controller to handle requests related to a single match.
    """

    def render_match_detail_page(self, request, match_id):
        """
        Fetches match data and renders the MatchDetail React component page.
        """
        try:
            match = get_object_or_404(Match, pk=match_id)

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
            for pred in match.predictions.all():
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
                "id": match.id,
                "name": str(match), # Using the __str__ method for a general name
                "competition": serialize_competition(match.competition),
                "team_one": serialize_team(match.team_one),
                "team_two": serialize_team(match.team_two),
                "team_one_score": match.team_one_score,
                "team_two_score": match.team_two_score,
                "start_datetime": match.start_datetime.isoformat(),
                "is_finished": match.is_finished,
                "is_winner_needed": match.is_winner_needed,
                "team_one_draw_score": match.team_one_draw_score,
                "team_two_draw_score": match.team_two_draw_score,
                "score_points": match.score_points,
                "predictions": predictions_data,
            }
            # return bridge.render( # Old way
            #     request,
            #     component="views/MatchDetail",
            #     props={"match": match_data}
            # )
            return Response(request, "MatchDetailView", {"match": match_data}) # New way
        except Http404:
            raise # Re-raise the Http404 exception to be handled by Django
