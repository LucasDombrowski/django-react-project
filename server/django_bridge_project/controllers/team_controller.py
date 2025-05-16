from django.shortcuts import get_object_or_404
from django_bridge_project.models import Team
from django_bridge.response import Response
from .utils.team_data_helper import TeamDataHelper

class TeamController:
    """
    Controller to handle requests related to a single team.
    """
    def render_team_detail_page(self, request, team_id: int):
        """
        Fetches team data, its players, and its matches using TeamDataHelper,
        then renders the TeamDetail React component page.
        """
        team_instance = get_object_or_404(Team, pk=team_id)
        
        helper = TeamDataHelper(request, team_instance)
        serialized_team_data = helper.get_team_data()

        current_user_data = None
        if request.user.is_authenticated:
            current_user_data = {
                "id": request.user.id,
                "username": request.user.username,
                "score": getattr(request.user, 'score', 0) # Safely access score
            }

        props = {
            "team": serialized_team_data,
            "isAuthenticated": request.user.is_authenticated,
            "currentUser": current_user_data,
        }
        
        return Response(request, "TeamDetailView", props) 