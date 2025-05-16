from django.db import transaction
from django_bridge_project.models import Match, Bet, Answer, Prediction, Team, CustomUser
from django_bridge_project.enums.prediction_types import PredictionType

class PointsAttributionHelper:
    def __init__(self, match_instance: Match):
        if not match_instance.is_finished:
            # Or raise an error, log a warning. Processing points for an unfinished match is usually not desired.
            print(f"Warning: PointsAttributionHelper initialized with an unfinished match (ID: {match_instance.id})")
        self.match_instance = match_instance

    @staticmethod
    def calculate_points_for_prediction_answer(user_answer_value_str: str | None, prediction_instance: Prediction) -> int:
        """
        Calculates points for a single prediction answer.
        Returns the prediction's score_points if correct, 0 otherwise.
        """
        if user_answer_value_str is None or user_answer_value_str == '' or \
           prediction_instance.correct_value is None or prediction_instance.correct_value == '':
            return 0

        is_correct = False
        correct_value_str = str(prediction_instance.correct_value)
        # user_answer_value_str is already passed as a string

        if prediction_instance.prediction_type == PredictionType.BOOLEAN.value:
            is_correct = user_answer_value_str.lower() == correct_value_str.lower()
        elif prediction_instance.prediction_type == PredictionType.PLAYER.value:
            is_correct = user_answer_value_str == correct_value_str
        elif prediction_instance.prediction_type == PredictionType.NUMERICAL.value:
            try:
                is_correct = float(user_answer_value_str) == float(correct_value_str)
            except ValueError:
                is_correct = False
        else:
            is_correct = user_answer_value_str == correct_value_str
        
        return prediction_instance.score_points if is_correct else 0

    @staticmethod
    def calculate_points_for_match_winner(predicted_winner_id: int, actual_winner_id: int, match_score_points: int) -> int:
        """
        Calculates points for correctly predicting the match winner.
        predicted_winner_id = 0 for a predicted draw.
        actual_winner_id = 0 for an actual draw.
        """
        if predicted_winner_id == actual_winner_id:
            return match_score_points
        return 0

    def _determine_actual_winner_team_id(self):
        """Determines the ID of the winning team or 0 for a draw."""
        m = self.match_instance
        if m.team_one_score > m.team_two_score:
            return m.team_one_id
        elif m.team_two_score > m.team_one_score:
            return m.team_two_id
        else: # Main scores are draw
            if m.is_winner_needed and m.team_one_draw_score is not None and m.team_two_draw_score is not None:
                if m.team_one_draw_score > m.team_two_draw_score:
                    return m.team_one_id
                elif m.team_two_draw_score > m.team_one_draw_score:
                    return m.team_two_id
                else:
                    # This case (draw scores are equal in a match that needed a winner) might need specific business logic.
                    # For now, considering it a draw for betting purposes if main score draw was not resolved by draw scores.
                    return 0 # Draw
            return 0 # Draw if winner not needed or draw scores not set

    @transaction.atomic
    def process_match_bets_and_attribute_points(self):
        """Processes all bets for the match and attributes points to users."""
        if not self.match_instance.is_finished:
            print(f"Match {self.match_instance.id} is not finished. Points will not be attributed.")
            return {"status": "error", "message": "Match not finished."}

        bets = Bet.objects.filter(match=self.match_instance).select_related('user', 'winner_team').prefetch_related('answers__prediction')
        
        if not bets.exists():
            print(f"No bets found for match {self.match_instance.id}.")
            return {"status": "info", "message": "No bets to process."}

        actual_winner_id = self._determine_actual_winner_team_id()
        match_predictions = list(self.match_instance.predictions.all())
        
        processed_users = {} # To batch user score updates if needed, or just update one by one
        total_points_awarded_for_match = 0

        for bet in bets:
            user_total_points_for_this_bet = 0 # Renamed for clarity within this loop
            user = bet.user

            # 1. Check predicted winner
            predicted_winner_id = bet.winner_team_id if bet.winner_team else 0 # 0 for predicted draw
            
            # Use the new static method for match winner points
            user_total_points_for_this_bet += PointsAttributionHelper.calculate_points_for_match_winner(
                predicted_winner_id,
                actual_winner_id,
                self.match_instance.score_points
            )

            # 2. Check answers for each prediction
            answers_map = {answer.prediction_id: answer for answer in bet.answers.all()}
            for prediction in match_predictions:
                user_answer = answers_map.get(prediction.id)
                if user_answer:
                    # Use the new static method
                    points_for_this_answer = PointsAttributionHelper.calculate_points_for_prediction_answer(
                        str(user_answer.value), # Ensure it's a string
                        prediction
                    )
                    user_total_points_for_this_bet += points_for_this_answer
            
            if user_total_points_for_this_bet > 0:
                user.score = (user.score or 0) + user_total_points_for_this_bet # Ensure user.score is not None
                user.save(update_fields=['score'])
                total_points_awarded_for_match += user_total_points_for_this_bet
                if user.id not in processed_users:
                    processed_users[user.id] = 0
                processed_users[user.id] += user_total_points_for_this_bet

        print(f"Points attribution completed for match {self.match_instance.id}. Total points awarded: {total_points_awarded_for_match}")
        return {
            "status": "success", 
            "message": f"Points processed. {total_points_awarded_for_match} total points awarded.", 
            "users_updated_count": len(processed_users),
            "processed_users_points": processed_users
        } 