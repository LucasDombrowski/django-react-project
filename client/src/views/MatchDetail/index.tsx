import React from 'react';
import { MatchData } from '../../libs/types/models/matchData';
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
    <div className="container mx-auto p-4 bg-gray-900 text-white min-h-screen">
      {/* Competition Section */}
      <div className="mb-8 p-6 bg-gray-800 rounded-lg shadow-xl text-center">
        {competition.logo_url && (
          <img
            src={competition.logo_url}
            alt={`${competition.name} logo`}
            className="w-24 h-24 mx-auto mb-4 rounded-full object-contain"
          />
        )}
        <h1 className="text-4xl font-bold text-teal-400">{competition.name}</h1>
        <p className="text-xl text-gray-400">{match.name.split('(')[0].trim()}</p> {/* Extracts "Team A vs Team B" */}
      </div>

      {/* Teams and Score Section */}
      <div className="mb-8 p-6 bg-gray-800 rounded-lg shadow-xl">
        <div className="flex items-center justify-around text-center">
          {/* Team One */}
          <div className="flex flex-col items-center w-1/3">
            {team_one.logo_url && (
              <img
                src={team_one.logo_url}
                alt={`${team_one.name} logo`}
                className="w-32 h-32 mb-3 rounded-lg object-contain shadow-md"
              />
            )}
            <h2 className="text-3xl font-semibold text-blue-400">{team_one.name}</h2>
          </div>

          {/* Score / VS */}
          <div className="flex flex-col items-center">
            <p className="text-6xl font-bold text-yellow-400">
              {team_one_score} - {team_two_score}
            </p>
            <span className="text-2xl text-gray-500 mt-2">VS</span>
          </div>

          {/* Team Two */}
          <div className="flex flex-col items-center w-1/3">
            {team_two.logo_url && (
              <img
                src={team_two.logo_url}
                alt={`${team_two.name} logo`}
                className="w-32 h-32 mb-3 rounded-lg object-contain shadow-md"
              />
            )}
            <h2 className="text-3xl font-semibold text-red-400">{team_two.name}</h2>
          </div>
        </div>
      </div>

      {/* Match Status and Date Section */}
      <div className="mb-8 p-6 bg-gray-800 rounded-lg shadow-xl text-center">
        <p className="text-2xl font-semibold mb-2">
          Status: <span className={is_finished ? "text-green-400" : "text-orange-400"}>
            {is_finished ? "Finished" : "Upcoming / In Progress"}
          </span>
        </p>
        <p className="text-lg text-gray-400">Date: {matchDate}</p>
      </div>
      
    </div>
  );
};

export default MatchDetailView; 