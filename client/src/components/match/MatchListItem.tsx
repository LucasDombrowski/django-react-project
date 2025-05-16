import React from 'react';
import { MatchListItemData } from '@/libs/types/models/matchListItemData';
import { Card, CardContent } from "@/components/ui/card";
import { cn } from '@/libs/utils';
import { Link } from '@django-bridge/react';
import MatchTeamDisplay from './MatchTeamDisplay';

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

  return (
    <Link href={`/match/${match.id}/`} className="block hover:no-underline focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 rounded-lg">
      <Card className={cn("overflow-hidden transition-all hover:shadow-md active:scale-[0.99] bg-card")}>
        <CardContent className="p-4 flex items-center justify-between space-x-2 sm:space-x-4 relative">
          {/* Team One */}
          <MatchTeamDisplay team={match.team_one} alignment="left" />

          {/* VS and Datetime */}
          <div className="flex flex-col items-center text-center flex-shrink-0 mx-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <span className="text-sm sm:text-base font-semibold text-muted-foreground">VS</span>
            <span className="text-[10px] sm:text-xs text-muted-foreground mt-1 whitespace-nowrap">{matchDate}</span>
          </div>

          {/* Team Two */}
          <MatchTeamDisplay team={match.team_two} alignment="right" />
        </CardContent>
      </Card>
    </Link>
  );
};

export default MatchListItem; 