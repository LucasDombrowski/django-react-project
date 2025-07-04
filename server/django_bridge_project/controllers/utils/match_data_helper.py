from django_bridge_project.models import Match, Bet, Answer, Team, Prediction # Added Bet, Answer, Team, Prediction
from django.shortcuts import get_object_or_404 # Added for the new method
from django_bridge_project.services.points_attribution_helper import PointsAttributionHelper # Added import

class MatchDataHelper:
    def __init__(self, request, match_instance: Match):
        self.request = request
        self.match_instance = match_instance
        # Instantiate PointsAttributionHelper if match is finished for _get_actual_winner_id
        if self.match_instance.is_finished:
            self.points_helper = PointsAttributionHelper(self.match_instance)
        else:
            self.points_helper = None

    def _get_actual_winner_id(self) -> int | None:
        """Gets the actual winner ID using PointsAttributionHelper."""
        if self.points_helper:
            return self.points_helper._determine_actual_winner_team_id()
        return None # Should not be called if match not finished / points_helper not init

    def _serialize_competition(self, competition):
        if not competition:
            return None
        logo_url = None
        if competition.logo and hasattr(competition.logo, 'url'):
            logo_url = self.request.build_absolute_uri(competition.logo.url)
        return {
            "id": competition.id,
            "name": competition.name,
            "logo_url": logo_url
        }

    def _serialize_team(self, team):
        if not team:
            return None
        logo_url = None
        if team.logo and hasattr(team.logo, 'url'):
            logo_url = self.request.build_absolute_uri(team.logo.url)
        
        players_data = []
        # Ensure players related name is correct, e.g., team.players.all()
        for player in team.players.all(): 
            photo_url = None
            if player.photo and hasattr(player.photo, 'url'):
                photo_url = self.request.build_absolute_uri(player.photo.url)
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
            "players": players_data
        }

    def _serialize_predictions(self):
        predictions_data = []
        for pred in self.match_instance.predictions.all():
            predictions_data.append({
                "id": pred.id,
                "label": pred.label,
                "prediction_type": pred.prediction_type,
                "score_points": pred.score_points,
                "correct_value": pred.correct_value,
            })
        return predictions_data

    def _get_match_leaderboard_data(self):
        if not self.match_instance.points_calculation_done or not self.points_helper:
            return None

        leaderboard = []
        actual_winner_id = self._get_actual_winner_id()
        if actual_winner_id is None: # Should not happen if points_calculation_done is True
            return None 

        bets = Bet.objects.filter(match=self.match_instance)\
                          .select_related('user', 'winner_team')\
                          .prefetch_related('answers__prediction')

        for bet in bets:
            user_total_points_for_this_bet = 0
            predicted_winner_id = bet.winner_team_id if bet.winner_team else 0
            
            user_total_points_for_this_bet += PointsAttributionHelper.calculate_points_for_match_winner(
                predicted_winner_id,
                actual_winner_id,
                self.match_instance.score_points
            )

            for answer in bet.answers.all():
                user_total_points_for_this_bet += PointsAttributionHelper.calculate_points_for_prediction_answer(
                    str(answer.value) if answer.value is not None else None,
                    answer.prediction # This is the Prediction instance
                )
            
            leaderboard.append({
                "user": {"id": bet.user.id, "username": bet.user.username},
                "total_gained_points": user_total_points_for_this_bet
            })
        
        return sorted(leaderboard, key=lambda x: x['total_gained_points'], reverse=True)

    def get_match_data(self):
        match_data = {
            "id": self.match_instance.id,
            "name": str(self.match_instance),
            "competition": self._serialize_competition(self.match_instance.competition),
            "team_one": self._serialize_team(self.match_instance.team_one),
            "team_two": self._serialize_team(self.match_instance.team_two),
            "team_one_score": self.match_instance.team_one_score,
            "team_two_score": self.match_instance.team_two_score,
            "start_datetime": self.match_instance.start_datetime.isoformat(),
            "is_finished": self.match_instance.is_finished,
            "points_calculation_done": self.match_instance.points_calculation_done, # Added this flag
            "is_winner_needed": self.match_instance.is_winner_needed,
            "team_one_draw_score": self.match_instance.team_one_draw_score,
            "team_two_draw_score": self.match_instance.team_two_draw_score,
            "score_points": self.match_instance.score_points,
            "predictions": self._serialize_predictions(),
            "leaderboard": self._get_match_leaderboard_data() # Added leaderboard data
        }
        return match_data

    def save_bet_from_form_data(self, user, cleaned_data):
        """
        Creates Bet and Answer objects from validated form data.
        Assumes to be called within a transaction.
        Raises Http404 if related objects (Team, Prediction) are not found.
        """
        winner_team_id_str = cleaned_data.get('match_winner')
        winner_team = None
        if winner_team_id_str:
            if winner_team_id_str == '0':  # '0' represents Draw
                winner_team = None
            else:
                winner_team = get_object_or_404(Team, pk=int(winner_team_id_str))
        
        new_bet = Bet.objects.create(
            match=self.match_instance,
            user=user,
            winner_team=winner_team
        )

        for field_name, value in cleaned_data.items():
            if field_name.startswith('prediction_') and value is not None and value != '':
                prediction_id_str = field_name.split('_')[1]
                # ValueError or Http404 will propagate up to the controller
                prediction_id = int(prediction_id_str)
                prediction_instance = get_object_or_404(Prediction, pk=prediction_id, match=self.match_instance)
                
                Answer.objects.create(
                    bet=new_bet,
                    prediction=prediction_instance,
                    value=str(value)
                )
        return new_bet # Return the created bet object 