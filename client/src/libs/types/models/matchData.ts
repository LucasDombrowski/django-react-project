import { Competition } from './competition';
import { Team } from './team';
import { Prediction } from './prediction';

// New type for a leaderboard entry
export interface LeaderboardEntryType {
  user: {
    id: number;
    username: string;
  };
  total_gained_points: number;
}

export interface MatchData {
  id: number;
  name: string; // Example: "Team A vs Team B (Competition Name - Date)"
  competition: Competition;
  team_one: Team;
  team_two: Team;
  team_one_score: number;
  team_two_score: number;
  start_datetime: string; // ISO format
  is_finished: boolean;
  points_calculation_done: boolean; // Added this flag
  is_winner_needed: boolean;
  team_one_draw_score: number | null;
  team_two_draw_score: number | null;
  score_points: number;
  predictions: Prediction[];
  leaderboard?: LeaderboardEntryType[] | null; // Leaderboard data
} 