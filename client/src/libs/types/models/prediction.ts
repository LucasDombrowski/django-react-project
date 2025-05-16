export interface Prediction {
  id: number;
  label: string;
  prediction_type: string;
  // prediction_type_display was removed by user preference
  score_points: number;
  correct_value: string | null;
} 