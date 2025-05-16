import { MatchListItemData } from './matchListItemData';
import { PlayerData } from './playerData';

export interface TeamData {
  id: number;
  name: string;
  logo_url: string | null;
  players: PlayerData[];
  matches: MatchListItemData[];
} 