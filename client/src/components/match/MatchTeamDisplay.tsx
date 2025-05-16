import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from '@/libs/utils';

interface TeamInfo {
  name: string;
  logo_url?: string | null;
}

interface MatchTeamDisplayProps {
  team: TeamInfo;
  alignment?: 'left' | 'right';
}

const MatchTeamDisplay: React.FC<MatchTeamDisplayProps> = ({ team, alignment = 'left' }) => {
  const getInitials = (name: string) => {
    if (!name) return '';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  const avatar = (
    <Avatar className="h-8 w-8 sm:h-10 sm:w-10 flex-shrink-0">
      {team.logo_url ? (
        <AvatarImage src={team.logo_url} alt={`${team.name} logo`} className="object-cover" />
      ) : null}
      <AvatarFallback>{getInitials(team.name)}</AvatarFallback>
    </Avatar>
  );

  const teamName = (
    <span 
      className={cn(
        "font-medium text-xs sm:text-sm truncate text-foreground",
        alignment === 'right' && "text-right ml-2 sm:ml-3"
      )}
    >
      {team.name}
    </span>
  );

  return (
    <div 
      className={cn(
        "flex items-center",
        alignment === 'left' ? "space-x-2 sm:space-x-3" : "justify-end flex-row-reverse"
      )}
    >
      {alignment === 'left' ? (
        <>
          {avatar}
          {teamName}
        </>
      ) : (
        <>
          {teamName}
          {avatar}
        </>
      )}
    </div>
  );
};

export default MatchTeamDisplay; 