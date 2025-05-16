from django.shortcuts import get_object_or_404
from django_bridge_project.models import Competition # Removed Match, Team as they are handled by helper
from django_bridge.response import Response
# from django.urls import reverse # Not strictly needed here anymore
from .utils.competition_data_helper import CompetitionDataHelper # Import the new helper
from django.middleware.csrf import get_token # Added import

class CompetitionController:
    """
    Controller to handle requests related to a single competition.
    """

    # _serialize_team_info and _serialize_match_list_item methods are now removed from here

    def render_competition_detail_page(self, request, competition_id: int):
        """
        Fetches competition data and its matches using CompetitionDataHelper, 
        then renders the CompetitionDetail React component page.
        """
        competition_instance = get_object_or_404(Competition, pk=competition_id)
        
        helper = CompetitionDataHelper(request, competition_instance)
        serialized_competition_data = helper.get_competition_data()

        current_user_data = None
        if request.user.is_authenticated:
            current_user_data = {
                "id": request.user.id,
                "username": request.user.username,
                "score": getattr(request.user, 'score', 0) # Safely access score
            }

        props = {
            "competition": serialized_competition_data,
            "isAuthenticated": request.user.is_authenticated,
            "currentUser": current_user_data,
            "csrfToken": get_token(request), # Added csrfToken
        }
        
        return Response(request, "CompetitionDetailView", props) 