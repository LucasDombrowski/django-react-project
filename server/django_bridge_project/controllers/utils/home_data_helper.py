from django.utils import timezone
from datetime import timedelta
from django_bridge_project.models import CustomUser, Match, Team, Competition

class HomeDataHelper:
    def __init__(self, request):
        self.request = request

    def _get_general_leaderboard_data(self, limit=10):
        users = CustomUser.objects.order_by('-score', 'username')[:limit]
        leaderboard_data = []
        for user in users:
            leaderboard_data.append({
                "user": {"id": user.id, "username": user.username},
                "score": user.score
            })
        return leaderboard_data

    # Common serialization logic for team/competition list items
    def _serialize_generic_list_item(self, instance, type_name="item"):
        logo_url = None
        if instance.logo and hasattr(instance.logo, 'url'):
            logo_url = self.request.build_absolute_uri(instance.logo.url)
        return {
            "id": instance.id,
            "name": instance.name,
            "logo_url": logo_url,
        }

    def _serialize_team_list_item(self, team_instance: Team):
        return self._serialize_generic_list_item(team_instance, "team")

    def _serialize_competition_list_item(self, competition_instance: Competition):
        return self._serialize_generic_list_item(competition_instance, "competition")
    
    # Match list item serialization (similar to what's in other helpers)
    # Consider centralizing this if it becomes too repetitive
    def _serialize_match_list_item(self, match_instance: Match):
        team_one_info = self._serialize_team_list_item(match_instance.team_one) if match_instance.team_one else None
        team_two_info = self._serialize_team_list_item(match_instance.team_two) if match_instance.team_two else None
        return {
            "id": match_instance.id,
            "team_one": team_one_info,
            "team_two": team_two_info,
            "start_datetime": match_instance.start_datetime.isoformat(),
            "is_finished": match_instance.is_finished, 
        }

    def _get_upcoming_matches_data(self, limit=5):
        now = timezone.now()
        # Example: matches starting in the next 7 days, not yet finished
        upcoming_matches_qs = Match.objects.filter(
            start_datetime__gte=now,
            # start_datetime__lte=now + timedelta(days=7), # Optional: to limit how far in future
            is_finished=False
        ).select_related('team_one', 'team_two').order_by('start_datetime')[:limit]
        return [self._serialize_match_list_item(match) for match in upcoming_matches_qs]

    def _get_featured_teams_data(self, limit=6):
        # Simple approach: get some teams, maybe ordered by name or randomly later
        teams_qs = Team.objects.all().order_by('?')[:limit] # Random order for variety
        return [self._serialize_team_list_item(team) for team in teams_qs]

    def _get_featured_competitions_data(self, limit=4):
        now = timezone.now()
        # Example: competitions that are currently active or starting soon
        competitions_qs = Competition.objects.filter(
            end_date__gte=now
        ).order_by('start_date')[:limit]
        return [self._serialize_competition_list_item(comp) for comp in competitions_qs]

    def get_home_page_data(self):
        current_user_id = self.request.user.id if self.request.user.is_authenticated else None
        current_user_data = None
        if self.request.user.is_authenticated:
            current_user_data = {
                "id": self.request.user.id,
                "username": self.request.user.username,
                "score": self.request.user.score # Assuming CustomUser has a score field
            }

        return {
            "leaderboard": self._get_general_leaderboard_data(),
            "upcoming_matches": self._get_upcoming_matches_data(),
            "featured_teams": self._get_featured_teams_data(),
            "featured_competitions": self._get_featured_competitions_data(),
            "current_user_id": current_user_id, # Kept for existing GenericLeaderboard logic if needed, but ideally use currentUser directly
            "isAuthenticated": self.request.user.is_authenticated,
            "currentUser": current_user_data,
        } 