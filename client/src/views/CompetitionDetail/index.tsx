import React from 'react';
import { CompetitionData } from '@/libs/types/models/competitionData';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import MatchListDisplay from '@/components/competition/MatchListDisplay';
import { cn } from '@/libs/utils';
import competitionDetailStrings from '@/libs/keychains/competitionDetail.json';
import { Separator } from "@/components/ui/separator";

export interface CompetitionDetailViewProps {
  competition: CompetitionData;
}

const CompetitionDetailView: React.FC<CompetitionDetailViewProps> = ({ competition }) => {
  const { name, logo_url, start_date, end_date, matches } = competition;

  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const getInitials = (nameStr: string) => {
    if (!nameStr) return '';
    return nameStr.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8 min-h-screen bg-background">
      {/* Competition Header */}
      <Card className={cn("mb-0 shadow-xl overflow-hidden border-border")}>
        <CardHeader className="p-6 text-center bg-muted/20">
          {logo_url ? (
            <Avatar className={cn("w-24 h-24 sm:w-28 sm:h-28 mx-auto mb-4 border-2 border-border bg-background shadow-sm")}>
              <AvatarImage src={logo_url} alt={`${name}${competitionDetailStrings.competition_logo_alt}`} className="object-contain" />
              <AvatarFallback className="text-3xl sm:text-4xl">{getInitials(name)}</AvatarFallback>
            </Avatar>
          ) : (
            <div className={cn("w-24 h-24 sm:w-28 sm:h-28 mx-auto mb-4 flex items-center justify-center bg-muted rounded-full border-2 border-border shadow-sm")}>
              <span className="text-3xl sm:text-4xl text-muted-foreground">{getInitials(name)}</span>
            </div>
          )}
          <CardTitle className="text-2xl sm:text-3xl lg:text-4xl font-bold text-foreground tracking-tight">{name}</CardTitle>
          <CardDescription className="text-sm sm:text-base text-muted-foreground mt-1">
            {competitionDetailStrings.dates_label} {formatDate(start_date)} {competitionDetailStrings.to_separator} {formatDate(end_date)}
          </CardDescription>
        </CardHeader>
      </Card>

      <Separator className="my-6 sm:my-8" />

      {/* Matches List Section - Now uses MatchListDisplay */}
      <MatchListDisplay matches={matches} />
    </div>
  );
};

export default CompetitionDetailView; 