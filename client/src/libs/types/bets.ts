// Types related to user bets and their display

export interface SerializedPredictionAnswer {
  prediction_id: number;
  prediction_label: string;
  prediction_type: string; 
  prediction_score_points: number;
  user_answer_value: string | null; 
  user_answer_display: string; // Display-friendly version
  // New fields for when points are calculated
  correct_value_display?: string | null; // Display-friendly correct value
  gained_points?: number | null;
}

export interface ActualWinnerDetails {
    id: number | null; // null if draw and not resolved by draw_scores, or if error
    name: string; // Team name or "Draw"
    is_draw: boolean;
}

export interface ChosenWinnerDetails {
  id: number | null; // User's chosen winner team ID, or 0 for draw
  name: string; // User's chosen winner team name, or "Draw"
  score_points?: number; // Points for correctly predicting match winner
  // New fields for when points are calculated
  actual_winner_details?: ActualWinnerDetails | null;
  gained_points_for_winner?: number | null;
}

export interface UserBetDetailsType {
  chosen_winner: ChosenWinnerDetails | null;
  answers: SerializedPredictionAnswer[];
  bet_id: number;
  points_have_been_calculated?: boolean; // Flag indicating if results are in
  total_gained_points?: number; // Total points gained for this bet if calculated
} 