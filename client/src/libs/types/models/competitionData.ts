import { MatchListItemData } from './matchListItemData';

export interface CompetitionData {
  id: number;
  name: string;
  logo_url: string | null;
  start_date: string; // Formatted as YYYY-MM-DD
  end_date: string;   // Formatted as YYYY-MM-DD
  matches: MatchListItemData[];
} 