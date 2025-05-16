import React from 'react';
import { MatchData } from '@/libs/types/models/matchData';
// import MatchSection from '@/components/match/MatchSection'; // No longer needed
import TeamDisplay from '@/components/match/TeamDisplay'; // Updated path alias
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'; // Import ShadCN Card components
import { cn } from '@/libs/utils'; // Import cn utility
// Note: Competition, Team, Player, Prediction are implicitly used through MatchData

// Removed import { MatchDetailViewProps } from '../../libs/types/matchDetailViewProps';

export interface MatchDetailViewProps {
  match: MatchData;
}

const MatchDetailView: React.FC<MatchDetailViewProps> = ({ match }) => {
  const {
    competition,
    team_one,
    team_two,
    team_one_score,
    team_two_score,
    is_finished,
    start_datetime,
  } = match;

  // Format date for display (optional, can be more sophisticated)
  const matchDate = new Date(start_datetime).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className="container mx-auto p-4 min-h-screen">
      {/* Competition Section */}
      <Card className={cn("mb-8 text-center", "shadow-xl")}>
        <CardHeader>
          {competition.logo_url && (
            <img
              src={competition.logo_url}
              alt={`${competition.name} logo`}
              className="w-24 h-24 mx-auto mb-4 rounded-full object-contain"
            />
          )}
          <CardTitle className="text-4xl font-bold text-teal-600">{competition.name}</CardTitle>
          <CardDescription className="text-xl text-gray-600">{match.name.split('(')[0].trim()}</CardDescription>
        </CardHeader>
      </Card>

      {/* Teams and Score Section */}
      <Card className={cn("mb-8", "shadow-xl")}>
        <CardContent className="pt-6"> {/* Added pt-6 for padding similar to previous p-6 on section */}
          <div className="flex items-center justify-around text-center">
            <TeamDisplay team={team_one} nameColorClass="text-blue-600" />

            {/* Score / VS / Date / Status */}
            <div className="flex flex-col items-center">
              <p className="text-6xl font-bold text-yellow-500">
                {team_one_score} - {team_two_score}
              </p>
              <span className="text-2xl text-gray-700 mt-2">VS</span>
              <p className="text-sm text-gray-500 mt-3 italic">{matchDate}</p>
              <p className="text-lg font-semibold mt-3">
                Status: <span className={is_finished ? "text-green-600" : "text-orange-500"}>
                  {is_finished ? "Finished" : "Upcoming / In Progress"}
                </span>
              </p>
            </div>

            <TeamDisplay team={team_two} nameColorClass="text-red-600" />
          </div>
        </CardContent>
      </Card>

      {/* Match Status and Date Section - REMOVED */}
      {/* 
      <MatchSection className="text-center">
        <p className="text-2xl font-semibold mb-2">
          Status: <span className={is_finished ? "text-green-600" : "text-orange-500"}>
            {is_finished ? "Finished" : "Upcoming / In Progress"}
          </span>
        </p>
        <p className="text-lg text-gray-600">Date: {matchDate}</p>
      </MatchSection>
      */}
      
    </div>
  );
};

export default MatchDetailView; 