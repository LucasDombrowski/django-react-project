import React from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { LeaderboardEntryType } from '@/libs/types/models/matchData'; // Ensure this path is correct
import matchDetailStrings from '@/libs/keychains/matchDetail.json';
import { cn } from '@/libs/utils';

interface MatchLeaderboardProps {
  leaderboardData: LeaderboardEntryType[];
  currentUserId?: number | null; // Add currentUserId prop (optional)
}

const MatchLeaderboard: React.FC<MatchLeaderboardProps> = ({ leaderboardData, currentUserId }) => {
  if (!leaderboardData || leaderboardData.length === 0) {
    return (
      <Card className={cn("shadow-lg", "mt-8")}>
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-foreground">
            {matchDetailStrings.leaderboard_title}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">{matchDetailStrings.leaderboard_no_data}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={cn("shadow-lg", "mt-8")}>
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center text-foreground">
          {matchDetailStrings.leaderboard_title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[10%]">{matchDetailStrings.leaderboard_rank_header}</TableHead>
              <TableHead>{matchDetailStrings.leaderboard_player_header}</TableHead>
              <TableHead className="text-right">{matchDetailStrings.leaderboard_points_header}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {leaderboardData.map((entry, index) => {
              const isCurrentUser = entry.user.id === currentUserId;
              return (
                <TableRow 
                  key={entry.user.id}
                  className={cn(isCurrentUser ? 'bg-primary/10' : '')} // Apply conditional styling
                >
                  <TableCell className={cn("font-semibold", isCurrentUser ? 'text-primary' : '')}>{index + 1}</TableCell>
                  <TableCell className={cn(isCurrentUser ? 'font-bold text-primary' : '')}>{entry.user.username}</TableCell>
                  <TableCell className="text-right">
                    <Badge 
                      variant={isCurrentUser ? "outline" : (entry.total_gained_points > 0 ? "default" : "secondary")}
                      className={cn("text-md", isCurrentUser ? 'border-primary text-primary' : '')}
                    >
                      {entry.total_gained_points} pts
                    </Badge>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default MatchLeaderboard; 