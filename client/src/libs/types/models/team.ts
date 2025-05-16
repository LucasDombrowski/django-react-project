import { Player } from './player';

export interface Team {
  id: number;
  name: string;
  logo_url: string | null;
  players: Player[];
} 