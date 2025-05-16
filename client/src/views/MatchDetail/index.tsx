import React from 'react';
import { MatchData } from '@/libs/types/models/matchData';
// import MatchSection from '@/components/match/MatchSection'; // No longer needed
import TeamDisplay from '@/components/match/TeamDisplay'; // Updated path alias
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'; // Import ShadCN Card components
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"; // Import Avatar for competition logo
import { Badge } from "@/components/ui/badge"; // Import Badge for status
import { cn } from '@/libs/utils'; // Import cn utility
import matchDetailStrings from '@/libs/keychains/matchDetail.json'; // Import keychain
import StyledBetFormRenderer from '@/components/forms/StyledBetFormRenderer'; // Import the new form renderer
import { Button } from '@/components/ui/button'; // Import Button for login/submit
import { DjangoProvidedForm } from '@/libs/types/forms'; // Updated import path
// Note: Competition, Team, Player, Prediction are implicitly used through MatchData

// Removed import { MatchDetailViewProps } from '../../libs/types/matchDetailViewProps';

export interface MatchDetailViewProps {
  match: MatchData;
  bet_form: DjangoProvidedForm; // Add bet_form
  isAuthenticated: boolean; // Add isAuthenticated
  csrfToken: string; // Add csrfToken
  action_url: string; // Add action_url
}

const MatchDetailView: React.FC<MatchDetailViewProps> = ({ 
  match,
  bet_form,
  isAuthenticated,
  csrfToken,
  action_url
}) => {
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
          {competition.logo_url ? (
            <Avatar className={cn("w-24 h-24 mx-auto mb-4")}>
              <AvatarImage src={competition.logo_url} alt={`${competition.name}${matchDetailStrings.alt_logo_suffix}`} />
              <AvatarFallback>{competition.name.substring(0, 1)}</AvatarFallback>
            </Avatar>
          ) : (
            <div className="w-24 h-24 mx-auto mb-4 flex items-center justify-center bg-muted rounded-full">
              <span className="text-3xl text-muted-foreground">{competition.name.substring(0,1)}</span>
            </div>
          )}
          <CardTitle className="text-4xl font-bold text-foreground">{competition.name}</CardTitle>
          <CardDescription className="text-xl text-muted-foreground">{match.name.split('(')[0].trim()}</CardDescription>
        </CardHeader>
      </Card>

      {/* Teams and Score Section */}
      <Card className={cn("mb-8", "shadow-xl")}>
        <CardContent className="pt-6"> {/* Added pt-6 for padding similar to previous p-6 on section */}
          <div className="flex items-center justify-around text-center">
            <TeamDisplay team={team_one} />

            {/* Score / VS / Date / Status */}
            <div className="flex flex-col items-center">
              <p className="text-6xl font-bold text-foreground">
                {team_one_score} - {team_two_score}
              </p>
              <span className="text-2xl text-muted-foreground mt-2">{matchDetailStrings.vs_text}</span>
              <p className="text-sm text-muted-foreground mt-3 italic">{matchDate}</p>
              <div className="mt-3">
                <Badge variant={is_finished ? "default" : "secondary"} className="text-lg px-3 py-1">
                  {matchDetailStrings.status_prefix}
                  {is_finished ? matchDetailStrings.status_finished : matchDetailStrings.status_upcoming}
                </Badge>
              </div>
            </div>

            <TeamDisplay team={team_two} />
          </div>
        </CardContent>
      </Card>

      {/* Bet Form Section */}
      <Card className={cn("shadow-xl")}>
        <CardHeader>
          <CardTitle className="text-2xl font-semibold text-foreground">{matchDetailStrings.bet_form_title}</CardTitle>
          <CardDescription className="text-muted-foreground">{matchDetailStrings.bet_form_description}</CardDescription>
        </CardHeader>
        <CardContent>
          {!isAuthenticated && (
            <div className="text-center mb-4 p-4 border border-border rounded-md bg-card">
              <p className="text-muted-foreground mb-3">{matchDetailStrings.login_to_bet_prompt}</p>
              <Button asChild>
                <a href="/login/">{matchDetailStrings.login_button_text}</a>
              </Button>
            </div>
          )}
          <form method="POST" action={action_url}>
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            <StyledBetFormRenderer form={bet_form} isDisabled={!isAuthenticated} />
            {isAuthenticated && (
              <Button type="submit" className="w-full mt-6" disabled={!isAuthenticated}>
                {matchDetailStrings.submit_bet_button_text}
              </Button>
            )}
          </form>
        </CardContent>
      </Card>      
    </div>
  );
};

export default MatchDetailView; 