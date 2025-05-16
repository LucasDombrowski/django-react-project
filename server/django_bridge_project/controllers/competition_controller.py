from django.shortcuts import get_object_or_404
from django_bridge_project.models import Competition # Removed Match, Team as they are handled by helper
from django_bridge.response import Response
# from django.urls import reverse # Not strictly needed here anymore
from .utils.competition_data_helper import CompetitionDataHelper # Import the new helper

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

        props = {
            "competition": serialized_competition_data,
            # We can add other necessary props like csrfToken if forms are involved later
            # "isAuthenticated": request.user.is_authenticated,
            # "csrfToken": get_token(request), # Needs from django.middleware.csrf import get_token
        }
        
        return Response(request, "CompetitionDetailView", props) 