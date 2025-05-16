from django.db.models import Q
from django_bridge_project.models import Team, Player, Match

class TeamDataHelper:
    def __init__(self, request, team_instance: Team):
        self.request = request
        self.team_instance = team_instance

    def _serialize_player(self, player_instance: Player):
        photo_url = None
        if player_instance.photo and hasattr(player_instance.photo, 'url'):
            photo_url = self.request.build_absolute_uri(player_instance.photo.url)
        return {
            "id": player_instance.id,
            "first_name": player_instance.first_name,
            "last_name": player_instance.last_name,
            "nickname": player_instance.nickname,
            "role": player_instance.role,
            "photo_url": photo_url,
        }

    # Reusing the serialization logic from CompetitionDataHelper for matches
    # To avoid duplication, this could be moved to a more generic utility if used in many places
    # For now, let's define it here or ensure CompetitionDataHelper's version is accessible/imported
    def _serialize_team_info_for_match(self, team_instance: Team): # Renamed to avoid conflict if inheriting
        if not team_instance:
            return None
        logo_url = None
        if team_instance.logo and hasattr(team_instance.logo, 'url'):
            logo_url = self.request.build_absolute_uri(team_instance.logo.url)
        return {
            "name": team_instance.name,
            "logo_url": logo_url,
        }

    def _serialize_match_list_item(self, match_instance: Match):
        return {
            "id": match_instance.id,
            "team_one": self._serialize_team_info_for_match(match_instance.team_one),
            "team_two": self._serialize_team_info_for_match(match_instance.team_two),
            "start_datetime": match_instance.start_datetime.isoformat(),
            "is_finished": match_instance.is_finished,
        }

    def get_team_data(self):
        team_logo_url = None
        if self.team_instance.logo and hasattr(self.team_instance.logo, 'url'):
            team_logo_url = self.request.build_absolute_uri(self.team_instance.logo.url)

        players_qs = self.team_instance.players.all().order_by('last_name', 'first_name')
        serialized_players = [self._serialize_player(player) for player in players_qs]

        # Fetch matches where the team is either team_one or team_two
        matches_qs = Match.objects.filter(
            Q(team_one=self.team_instance) | Q(team_two=self.team_instance)
        ).select_related('team_one', 'team_two', 'competition').order_by('-start_datetime') # Show recent matches first
        
        serialized_matches = [self._serialize_match_list_item(match) for match in matches_qs]

        return {
            "id": self.team_instance.id,
            "name": self.team_instance.name,
            "logo_url": team_logo_url,
            "players": serialized_players,
            "matches": serialized_matches,
        } 