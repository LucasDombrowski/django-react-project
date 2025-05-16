import React from 'react';
import { MatchListItemData } from '@/libs/types/models/matchListItemData';
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from '@/libs/utils';
import { Link } from '@django-bridge/react';

interface MatchListItemProps {
  match: MatchListItemData;
}

const MatchListItem: React.FC<MatchListItemProps> = ({ match }) => {
  const matchDate = new Date(match.start_datetime).toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  return (
    <Link href={`/match/${match.id}/`} className="block hover:no-underline focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 rounded-lg">
      <Card className={cn("overflow-hidden transition-all hover:shadow-md active:scale-[0.99] bg-card")}>
        <CardContent className="p-4 flex items-center justify-between space-x-2 sm:space-x-4">
          {/* Team One */}
          <div className="flex items-center space-x-2 sm:space-x-3 w-2/5 min-w-0">
            <Avatar className="h-8 w-8 sm:h-10 sm:w-10">
              {match.team_one.logo_url ? (
                <AvatarImage src={match.team_one.logo_url} alt={`${match.team_one.name} logo`} />
              ) : null}
              <AvatarFallback>{getInitials(match.team_one.name)}</AvatarFallback>
            </Avatar>
            <span className="font-medium text-xs sm:text-sm truncate text-foreground">{match.team_one.name}</span>
          </div>

          {/* VS and Datetime */}
          <div className="flex flex-col items-center text-center flex-shrink-0 mx-1">
            <span className="text-sm sm:text-base font-semibold text-muted-foreground">VS</span>
            <span className="text-[10px] sm:text-xs text-muted-foreground mt-1 whitespace-nowrap">{matchDate}</span>
          </div>

          {/* Team Two */}
          <div className="flex items-center space-x-2 sm:space-x-3 justify-end w-2/5 min-w-0">
            <span className="font-medium text-xs sm:text-sm truncate text-right text-foreground">{match.team_two.name}</span>
            <Avatar className="h-8 w-8 sm:h-10 sm:w-10">
              {match.team_two.logo_url ? (
                <AvatarImage src={match.team_two.logo_url} alt={`${match.team_two.name} logo`} />
              ) : null}
              <AvatarFallback>{getInitials(match.team_two.name)}</AvatarFallback>
            </Avatar>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
};

export default MatchListItem; 