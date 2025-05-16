interface TeamInfo {
  name: string;
  logo_url: string | null;
}

export interface MatchListItemData {
  id: number;
  team_one: TeamInfo;
  team_two: TeamInfo;
  start_datetime: string; // ISO format string
  is_finished: boolean; // Added is_finished status
} 