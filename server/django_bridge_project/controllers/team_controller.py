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

        props = {
            "team": serialized_team_data,
            # "isAuthenticated": request.user.is_authenticated, # If needed later
            # "csrfToken": get_token(request), # If needed later, requires import
        }
        
        return Response(request, "TeamDetailView", props) 