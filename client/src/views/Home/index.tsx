import React from 'react';
import { HomePageData } from '@/libs/types/pages/homePageData';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from '@/libs/utils';
import homeStrings from '@/libs/keychains/home.json';
import Layout from '@/components/layout/Layout';
import { CurrentUser } from '@/libs/types/currentUser';

import GenericLeaderboard from '@/components/match/MatchLeaderboard';
import MatchListItem from '@/components/match/MatchListItem';
import TeamListItem from '@/components/team/TeamListItem';
import CompetitionListItem from '@/components/competition/CompetitionListItem';

export interface HomeViewProps extends HomePageData {
  isAuthenticated: boolean;
  currentUser: CurrentUser | null;
  csrfToken: string;
}

const HomeView: React.FC<HomeViewProps> = ({
  leaderboard,
  upcoming_matches,
  featured_teams,
  featured_competitions,
  current_user_id,
  isAuthenticated,
  currentUser,
  csrfToken,
}) => {

  const leaderboardStrings = {
    title: homeStrings.leaderboard_title,
    rank_header: homeStrings.leaderboard_rank_header,
    player_header: homeStrings.leaderboard_player_header,
    points_header: homeStrings.leaderboard_points_header,
    no_data: homeStrings.no_leaderboard_data,
  };

  return (
    <Layout isAuthenticated={isAuthenticated} currentUser={currentUser} csrfToken={csrfToken}>
      <div className="container mx-auto p-4 sm:p-6 lg:p-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
          {/* Main Content Area */}
          <div className="lg:col-span-2 space-y-6 lg:space-y-8">
            <GenericLeaderboard 
              leaderboardData={leaderboard} 
              currentUserId={current_user_id} 
              strings={leaderboardStrings} 
              pointsSuffix="pts"
            />
            <Card className={cn("shadow-xl border-border")}>
              <CardHeader>
                <CardTitle className="text-xl sm:text-2xl font-semibold text-foreground">{homeStrings.upcoming_matches_title}</CardTitle>
              </CardHeader>
              <CardContent className="pt-0 sm:pt-2 pb-4 sm:pb-6">
                {upcoming_matches && upcoming_matches.length > 0 ? (
                  <div className="space-y-3 sm:space-y-4">
                    {upcoming_matches.map((match) => (
                      <MatchListItem key={match.id} match={match} />
                    ))}
                  </div>
                ) : (
                  <p className="text-muted-foreground text-sm sm:text-base p-4 text-center">{homeStrings.no_upcoming_matches}</p>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar Area */}
          <div className="lg:col-span-1 space-y-6 lg:space-y-8">
            <Card className={cn("shadow-xl border-border")}>
              <CardHeader>
                <CardTitle className="text-xl sm:text-2xl font-semibold text-foreground">{homeStrings.featured_teams_title}</CardTitle>
              </CardHeader>
              <CardContent className="pt-0 sm:pt-2 pb-4 sm:pb-6">
                {featured_teams && featured_teams.length > 0 ? (
                  <div className="space-y-3 sm:space-y-4">
                    {featured_teams.map((team) => (
                      <TeamListItem key={team.id} team={team} />
                    ))}
                  </div>
                ) : (
                  <p className="text-muted-foreground text-sm sm:text-base p-4 text-center">{homeStrings.no_featured_teams}</p>
                )}
              </CardContent>
            </Card>
            <Card className={cn("shadow-xl border-border")}>
              <CardHeader>
                <CardTitle className="text-xl sm:text-2xl font-semibold text-foreground">{homeStrings.featured_competitions_title}</CardTitle>
              </CardHeader>
              <CardContent className="pt-0 sm:pt-2 pb-4 sm:pb-6">
                {featured_competitions && featured_competitions.length > 0 ? (
                  <div className="space-y-3 sm:space-y-4">
                    {featured_competitions.map((competition) => (
                      <CompetitionListItem key={competition.id} competition={competition} />
                    ))}
                  </div>
                ) : (
                  <p className="text-muted-foreground text-sm sm:text-base p-4 text-center">{homeStrings.no_featured_competitions}</p>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default HomeView;
