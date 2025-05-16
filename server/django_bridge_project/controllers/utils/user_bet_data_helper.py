from django_bridge_project.models import Bet, Answer, Prediction, Team, Player, Match
from django_bridge_project.enums.prediction_types import PredictionType

class UserBetDataHelper:
    def __init__(self, user, match_instance: Match):
        self.user = user
        self.match_instance = match_instance

    def _get_player_name(self, player_id_str):
        try:
            player_id = int(player_id_str)
            player = Player.objects.get(pk=player_id)
            return f"{player.first_name} {player.last_name} ({player.nickname})" if player.nickname else f"{player.first_name} {player.last_name}"
        except (Player.DoesNotExist, ValueError):
            return "Unknown Player"
    
    def _get_displayable_correct_value(self, prediction: Prediction):
        if prediction.correct_value is None or prediction.correct_value == '':
            return "N/A" # Not available or not set
        
        if prediction.prediction_type == PredictionType.PLAYER.value:
            return self._get_player_name(prediction.correct_value)
        elif prediction.prediction_type == PredictionType.BOOLEAN.value:
            return "Yes" if str(prediction.correct_value).lower() == 'true' else ("No" if str(prediction.correct_value).lower() == 'false' else prediction.correct_value)
        return str(prediction.correct_value)

    def _determine_actual_winner_team_details(self):
        m = self.match_instance
        actual_winner_id = None
        actual_winner_name = "Error determining winner"
        is_draw = False

        if m.team_one_score > m.team_two_score:
            actual_winner_id = m.team_one_id
            actual_winner_name = m.team_one.name
        elif m.team_two_score > m.team_one_score:
            actual_winner_id = m.team_two_id
            actual_winner_name = m.team_two.name
        else: # Main scores are draw
            is_draw = True
            if m.is_winner_needed and m.team_one_draw_score is not None and m.team_two_draw_score is not None:
                if m.team_one_draw_score > m.team_two_draw_score:
                    actual_winner_id = m.team_one_id
                    actual_winner_name = m.team_one.name
                    is_draw = False
                elif m.team_two_draw_score > m.team_one_draw_score:
                    actual_winner_id = m.team_two_id
                    actual_winner_name = m.team_two.name
                    is_draw = False
                else: # Draw scores equal, still a draw for betting if not resolved
                    actual_winner_name = "Draw"
            else: # Winner not needed or draw scores not set, it's a draw
                actual_winner_name = "Draw"
        
        return {"id": actual_winner_id, "name": actual_winner_name, "is_draw": is_draw}

    def get_user_bet_details(self):
        try:
            user_bet = Bet.objects.select_related('winner_team').get(user=self.user, match=self.match_instance)
        except Bet.DoesNotExist:
            return None

        chosen_winner_details = {}
        if user_bet.winner_team:
            chosen_winner_details = {
                "id": user_bet.winner_team.id,
                "name": user_bet.winner_team.name,
                "score_points": self.match_instance.score_points
            }
        else:
            chosen_winner_details = {"id": 0, "name": "Draw", "score_points": self.match_instance.score_points}
        
        serialized_answers = []
        all_match_predictions = Prediction.objects.filter(match=self.match_instance).order_by('id')
        user_answers_for_bet = {ans.prediction_id: ans for ans in user_bet.answers.all()}

        points_have_been_calculated = self.match_instance.points_calculation_done
        total_gained_points_for_match = 0
        actual_match_winner_info = None
        if points_have_been_calculated:
            actual_match_winner_info = self._determine_actual_winner_team_details()
            chosen_winner_details['actual_winner_details'] = actual_match_winner_info
            gained_points_for_winner = 0
            predicted_winner_id = user_bet.winner_team_id if user_bet.winner_team else 0
            
            actual_winner_id_for_comparison = actual_match_winner_info['id']
            if actual_match_winner_info['is_draw'] and actual_match_winner_info['id'] is None : # Actual draw is id 0 for comparison
                 actual_winner_id_for_comparison = 0

            if predicted_winner_id == actual_winner_id_for_comparison:
                gained_points_for_winner = self.match_instance.score_points
            
            chosen_winner_details['gained_points_for_winner'] = gained_points_for_winner
            total_gained_points_for_match += gained_points_for_winner

        for pred in all_match_predictions:
            user_answer_instance = user_answers_for_bet.get(pred.id)
            user_answer_value = None
            display_value = "Not answered"

            if user_answer_instance:
                user_answer_value = user_answer_instance.value
                display_value = user_answer_value 
                if pred.prediction_type == PredictionType.PLAYER.value and user_answer_value:
                    display_value = self._get_player_name(user_answer_value)
                elif pred.prediction_type == PredictionType.BOOLEAN.value:
                    display_value = "Yes" if user_answer_value == 'True' else ("No" if user_answer_value == 'False' else "Not answered")
            
            answer_data = {
                "prediction_id": pred.id,
                "prediction_label": pred.label,
                "prediction_type": pred.prediction_type,
                "prediction_score_points": pred.score_points,
                "user_answer_value": user_answer_value,
                "user_answer_display": display_value
            }

            if points_have_been_calculated:
                answer_data['correct_value_display'] = self._get_displayable_correct_value(pred)
                gained_points_for_answer = 0
                if user_answer_instance and user_answer_instance.value is not None and user_answer_instance.value != '' and \
                   pred.correct_value is not None and pred.correct_value != '':
                    
                    is_correct = False
                    correct_value_str = str(pred.correct_value)
                    user_answer_value_str = str(user_answer_instance.value)

                    if pred.prediction_type == PredictionType.BOOLEAN.value:
                        is_correct = user_answer_value_str.lower() == correct_value_str.lower()
                    elif pred.prediction_type == PredictionType.PLAYER.value:
                        is_correct = user_answer_value_str == correct_value_str
                    elif pred.prediction_type == PredictionType.NUMERICAL.value:
                        try:
                            is_correct = float(user_answer_value_str) == float(correct_value_str)
                        except ValueError:
                            is_correct = False
                    else:
                        is_correct = user_answer_value_str == correct_value_str
                    
                    if is_correct:
                        gained_points_for_answer = pred.score_points
                
                answer_data['gained_points'] = gained_points_for_answer
                total_gained_points_for_match += gained_points_for_answer
            
            serialized_answers.append(answer_data)

        return_data = {
            "chosen_winner": chosen_winner_details,
            "answers": serialized_answers,
            "bet_id": user_bet.id,
            "points_have_been_calculated": points_have_been_calculated
        }
        if points_have_been_calculated:
            return_data["total_gained_points"] = total_gained_points_for_match
        
        return return_data 