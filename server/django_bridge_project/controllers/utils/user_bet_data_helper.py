from django_bridge_project.models import Bet, Answer, Prediction, Team, Player
from django_bridge_project.enums.prediction_types import PredictionType

class UserBetDataHelper:
    def __init__(self, user, match_instance):
        self.user = user
        self.match_instance = match_instance

    def _get_player_name(self, player_id):
        try:
            player = Player.objects.get(pk=player_id)
            return f"{player.first_name} {player.last_name} ({player.nickname})" if player.nickname else f"{player.first_name} {player.last_name}"
        except Player.DoesNotExist:
            return "Unknown Player"

    def get_user_bet_details(self):
        try:
            user_bet = Bet.objects.get(user=self.user, match=self.match_instance)
        except Bet.DoesNotExist:
            return None

        # Serialize chosen winner
        chosen_winner_details = None
        if user_bet.winner_team:
            chosen_winner_details = {
                "id": user_bet.winner_team.id,
                "name": user_bet.winner_team.name,
                "score_points": self.match_instance.score_points # Add match score points for winner
            }
        else: # It was a draw
            chosen_winner_details = {
                "id": 0, # Consistent with form value for draw
                "name": "Draw",
                "score_points": self.match_instance.score_points # Add match score points for draw case too (points if correctly predicted as draw)
            }
        
        serialized_answers = []
        # Fetch all predictions for the match to ensure all are listed
        all_match_predictions = Prediction.objects.filter(match=self.match_instance).order_by('id')
        user_answers_for_bet = {ans.prediction_id: ans for ans in user_bet.answers.all()}

        for pred in all_match_predictions:
            user_answer_instance = user_answers_for_bet.get(pred.id)
            user_answer_value = None
            display_value = None

            if user_answer_instance:
                user_answer_value = user_answer_instance.value
                display_value = user_answer_value # Default display value
                
                if pred.prediction_type == PredictionType.PLAYER.value and user_answer_value:
                    try:
                        player_id = int(user_answer_value)
                        display_value = self._get_player_name(player_id)
                    except ValueError:
                        display_value = "Invalid Player ID" # Should not happen with form validation
                elif pred.prediction_type == PredictionType.BOOLEAN.value:
                    display_value = "Yes" if user_answer_value == 'True' else ("No" if user_answer_value == 'False' else "Not answered")


            serialized_answers.append({
                "prediction_id": pred.id,
                "prediction_label": pred.label,
                "prediction_type": pred.prediction_type,
                "prediction_score_points": pred.score_points,
                "user_answer_value": user_answer_value, # The raw value stored
                "user_answer_display": display_value if display_value is not None else "Not answered"
            })

        return {
            "chosen_winner": chosen_winner_details,
            "answers": serialized_answers,
            "bet_id": user_bet.id # Might be useful for display or future actions
        } 