import { UserLeaderboardEntryData } from '../models/userLeaderboardEntryData';
import { MatchListItemData } from '../models/matchListItemData'; // Reused
import { TeamListItemData } from '../models/teamListItemData';
import { CompetitionListItemData } from '../models/competitionListItemData';

export interface HomePageData {
  leaderboard: UserLeaderboardEntryData[];
  upcoming_matches: MatchListItemData[];
  featured_teams: TeamListItemData[];
  featured_competitions: CompetitionListItemData[];
  current_user_id?: number | null; // For highlighting in leaderboard
} 