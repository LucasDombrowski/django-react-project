import React from 'react';
import { PlayerData } from '@/libs/types/models/playerData';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card"; // Using Card for structure
import { cn } from '@/libs/utils';
import teamDetailStrings from '@/libs/keychains/teamDetail.json';

interface PlayerListItemProps {
  player: PlayerData;
}

const PlayerListItem: React.FC<PlayerListItemProps> = ({ player }) => {
  const playerName = player.nickname || `${player.first_name} ${player.last_name}`;
  const playerInitials = (player.first_name?.[0] || '') + (player.last_name?.[0] || '');

  return (
    <Card className={cn("overflow-hidden", "hover:shadow-md transition-shadow")}>
      <CardContent className="p-3 sm:p-4 flex items-center space-x-3 sm:space-x-4">
        <Avatar className="h-12 w-12 sm:h-16 sm:w-16">
          {player.photo_url ? (
            <AvatarImage src={player.photo_url} alt={`${teamDetailStrings.player_photo_alt_prefix}${playerName}`} className="object-cover" />
          ) : null}
          <AvatarFallback className="text-lg sm:text-xl">{playerInitials.toUpperCase()}</AvatarFallback>
        </Avatar>
        <div className="min-w-0">
          <p className="text-sm sm:text-base font-semibold truncate text-foreground">{playerName}</p>
          {player.role && (
            <p className="text-xs sm:text-sm text-muted-foreground truncate">
              {teamDetailStrings.role_prefix}{player.role}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default PlayerListItem; 