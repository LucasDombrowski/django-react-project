import React from 'react';
import { TeamData } from '@/libs/types/models/teamData';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import PlayerListItem from '@/components/team/PlayerListItem';
import MatchListDisplay from '@/components/competition/MatchListDisplay'; // Reusing this component
import { cn } from '@/libs/utils';
import teamDetailStrings from '@/libs/keychains/teamDetail.json';

export interface TeamDetailViewProps {
  team: TeamData;
  // Add other props like isAuthenticated if needed later
}

const TeamDetailView: React.FC<TeamDetailViewProps> = ({ team }) => {
  const { name, logo_url, players, matches } = team;

  const getInitials = (nameStr: string) => {
    if (!nameStr) return '';
    return nameStr.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8 min-h-screen bg-background">
      {/* Team Header */}
      <Card className={cn("mb-0 shadow-xl overflow-hidden border-border")}>
        <CardHeader className="p-6 text-center bg-muted/20">
          {logo_url ? (
            <Avatar className={cn("w-24 h-24 sm:w-28 sm:h-28 mx-auto mb-4 border-2 border-border bg-background shadow-sm")}>
              <AvatarImage src={logo_url} alt={`${name}${teamDetailStrings.team_logo_alt}`} className="object-contain" />
              <AvatarFallback className="text-3xl sm:text-4xl">{getInitials(name)}</AvatarFallback>
            </Avatar>
          ) : (
            <div className={cn("w-24 h-24 sm:w-28 sm:h-28 mx-auto mb-4 flex items-center justify-center bg-muted rounded-full border-2 border-border shadow-sm")}>
              <span className="text-3xl sm:text-4xl text-muted-foreground">{getInitials(name)}</span>
            </div>
          )}
          <CardTitle className="text-2xl sm:text-3xl lg:text-4xl font-bold text-foreground tracking-tight">{name}</CardTitle>
          {/* Optional: Add a CardDescription for team slogan or short info if available in TeamData */}
        </CardHeader>
      </Card>

      <Separator className="my-6 sm:my-8" />

      {/* Players List Section */}
      <Card className={cn("shadow-xl border-border")}>
        <CardHeader>
          <CardTitle className="text-xl sm:text-2xl font-semibold text-foreground">{teamDetailStrings.players_header}</CardTitle>
        </CardHeader>
        <CardContent className="pt-0 sm:pt-2 pb-4 sm:pb-6">
          {players && players.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
              {players.map((player) => (
                <PlayerListItem key={player.id} player={player} />
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground text-sm sm:text-base p-4 text-center">{teamDetailStrings.no_players_message}</p>
          )}
        </CardContent>
      </Card>

      <Separator className="my-6 sm:my-8" />

      {/* Matches List Section - Reusing MatchListDisplay */}
      {/* Note: MatchListDisplay expects competitionDetailStrings for its internal headers if no matches */} 
      {/* We might need to pass specific titles or adjust MatchListDisplay if this becomes an issue */} 
      <MatchListDisplay matches={matches} /> 

    </div>
  );
};

export default TeamDetailView; 