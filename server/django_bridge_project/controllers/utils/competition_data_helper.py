from django_bridge_project.models import Competition, Match, Team

class CompetitionDataHelper:
    def __init__(self, request, competition_instance: Competition):
        self.request = request
        self.competition_instance = competition_instance

    def _serialize_team_info(self, team_instance: Team):
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
            "team_one": self._serialize_team_info(match_instance.team_one),
            "team_two": self._serialize_team_info(match_instance.team_two),
            "start_datetime": match_instance.start_datetime.isoformat(),
            "is_finished": match_instance.is_finished,
        }

    def get_competition_data(self):
        """
        Fetches and serializes competition data and its matches.
        """
        competition_logo_url = None
        if self.competition_instance.logo and hasattr(self.competition_instance.logo, 'url'):
            competition_logo_url = self.request.build_absolute_uri(self.competition_instance.logo.url)

        matches_qs = Match.objects.filter(competition=self.competition_instance)\
                                .select_related('team_one', 'team_two')\
                                .order_by('start_datetime')
        
        serialized_matches = [self._serialize_match_list_item(match) for match in matches_qs]

        return {
            "id": self.competition_instance.id,
            "name": self.competition_instance.name,
            "logo_url": competition_logo_url,
            "start_date": self.competition_instance.start_date.isoformat(),
            "end_date": self.competition_instance.end_date.isoformat(),
            "matches": serialized_matches,
        } 