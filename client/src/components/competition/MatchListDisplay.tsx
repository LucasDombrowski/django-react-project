import React from 'react';
import { MatchListItemData } from '@/libs/types/models/matchListItemData';
import MatchListItem from '@/components/match/MatchListItem';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/libs/utils';
import competitionDetailStrings from '@/libs/keychains/competitionDetail.json';

interface MatchListDisplayProps {
  matches: MatchListItemData[];
}

const MatchListDisplay: React.FC<MatchListDisplayProps> = ({ matches }) => {
  const upcomingMatches = matches.filter(match => !match.is_finished);
  const finishedMatches = matches.filter(match => match.is_finished);

  if (!matches || matches.length === 0) {
    return (
      <Card className={cn("shadow-xl border-border")}>
        <CardHeader>
          <CardTitle className="text-xl sm:text-2xl font-semibold text-foreground">
            {competitionDetailStrings.matches_header}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-sm sm:text-base p-4 text-center">
            {competitionDetailStrings.no_matches_message}
          </p>
        </CardContent>
      </Card>
    );
  }

  // Only render sections if there are matches of that type, or show a message if no matches of that type but other matches exist.
  const shouldShowUpcomingSection = upcomingMatches.length > 0 || (upcomingMatches.length === 0 && finishedMatches.length > 0 && matches.length > 0);
  const shouldShowFinishedSection = finishedMatches.length > 0 || (finishedMatches.length === 0 && upcomingMatches.length > 0 && matches.length > 0);

  return (
    <div className="space-y-8">
      {shouldShowUpcomingSection && (
        <Card className={cn("shadow-xl border-border")}>
          <CardHeader>
            <CardTitle className="text-xl sm:text-2xl font-semibold text-foreground">
              {competitionDetailStrings.upcoming_matches_header}
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0 sm:pt-2 pb-4 sm:pb-6">
            {upcomingMatches.length > 0 ? (
              <div className="space-y-3 sm:space-y-4">
                {upcomingMatches.map((match, index) => (
                  <React.Fragment key={match.id}>
                    <MatchListItem match={match} />
                    {index < upcomingMatches.length - 1 && <Separator className="my-3 sm:my-4" />} 
                  </React.Fragment>
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground text-sm sm:text-base p-4 text-center">
                {competitionDetailStrings.no_upcoming_matches_message}
              </p>
            )}
          </CardContent>
        </Card>
      )}

      {shouldShowFinishedSection && (
        <Card className={cn("shadow-xl border-border")}>
          <CardHeader>
            <CardTitle className="text-xl sm:text-2xl font-semibold text-foreground">
              {competitionDetailStrings.finished_matches_header}
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0 sm:pt-2 pb-4 sm:pb-6">
            {finishedMatches.length > 0 ? (
              <div className="space-y-3 sm:space-y-4">
                {finishedMatches.map((match, index) => (
                  <React.Fragment key={match.id}>
                    <MatchListItem match={match} />
                    {index < finishedMatches.length - 1 && <Separator className="my-3 sm:my-4" />} 
                  </React.Fragment>
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground text-sm sm:text-base p-4 text-center">
                {competitionDetailStrings.no_finished_matches_message}
              </p>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default MatchListDisplay; 