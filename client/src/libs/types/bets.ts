// Types related to user bets and their display

export interface SerializedPredictionAnswer {
  prediction_id: number;
  prediction_label: string;
  prediction_type: string; 
  prediction_score_points: number;
  user_answer_value: string | null; 
  user_answer_display: string; // Display-friendly version
}

export interface ChosenWinnerDetails {
  id: number | null;
  name: string;
  score_points?: number; // Optional: if we pass match.score_points here
}

export interface UserBetDetailsType {
  chosen_winner: ChosenWinnerDetails | null;
  answers: SerializedPredictionAnswer[];
  bet_id: number;
} 