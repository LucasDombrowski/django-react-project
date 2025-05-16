import React from 'react';
import { TeamListItemData } from '@/libs/types/models/teamListItemData';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from '@django-bridge/react';
import { cn } from '@/libs/utils';
import homeStrings from '@/libs/keychains/home.json'; // Assuming some strings might be needed, e.g. for button

interface TeamListItemProps {
  team: TeamListItemData;
}

const TeamListItem: React.FC<TeamListItemProps> = ({ team }) => {
  const getInitials = (name: string) => {
    if (!name) return '';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  return (
    <Link href={`/team/${team.id}/`} className="block hover:no-underline focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 rounded-lg h-full">
      <Card className={cn("overflow-hidden transition-all hover:shadow-md active:scale-[0.99] bg-card flex flex-col h-full")}>
        <CardContent className="p-4 flex flex-col items-center text-center flex-grow">
          <Avatar className="h-20 w-20 mb-3">
            {team.logo_url ? (
              <AvatarImage src={team.logo_url} alt={`${team.name} logo`} className="object-contain"/>
            ) : null}
            <AvatarFallback className="text-2xl">{getInitials(team.name)}</AvatarFallback>
          </Avatar>
          <p className="font-semibold text-md text-foreground truncate w-full">{team.name}</p>
        </CardContent>
        <CardFooter className="p-3 pt-0 mt-auto">
            <Button variant="outline" className="w-full text-xs sm:text-sm">
                {homeStrings.view_team_button}
            </Button>
        </CardFooter>
      </Card>
    </Link>
  );
};

export default TeamListItem; 