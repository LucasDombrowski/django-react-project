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
import { cn } from '@/libs/utils';

// Renamed and made more generic
export interface GenericLeaderboardEntry {
  user: {
    id: number;
    username: string;
  };
  score: number; // Generic score field
  // total_gained_points is now just 'score'
}

interface LeaderboardStrings {
    title: string;
    rank_header: string;
    player_header: string;
    points_header: string;
    no_data: string;
}

interface GenericLeaderboardProps {
  leaderboardData: GenericLeaderboardEntry[];
  currentUserId?: number | null;
  strings: LeaderboardStrings;
  pointsSuffix?: string; // e.g., "pts" or "points"
}

const GenericLeaderboard: React.FC<GenericLeaderboardProps> = ({ 
    leaderboardData, 
    currentUserId, 
    strings, 
    pointsSuffix = "pts" 
}) => {
  if (!leaderboardData || leaderboardData.length === 0) {
    return (
      <Card className={cn("shadow-lg", "mt-8")}>
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-foreground">
            {strings.title}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">{strings.no_data}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={cn("shadow-lg", "mt-8")}>
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center text-foreground">
          {strings.title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[10%]">{strings.rank_header}</TableHead>
              <TableHead>{strings.player_header}</TableHead>
              <TableHead className="text-right">{strings.points_header}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {leaderboardData.map((entry, index) => {
              const isCurrentUser = entry.user.id === currentUserId;
              return (
                <TableRow 
                  key={entry.user.id}
                  className={cn(isCurrentUser ? 'bg-primary/10' : '')}
                >
                  <TableCell className={cn("font-semibold", isCurrentUser ? 'text-primary' : '')}>{index + 1}</TableCell>
                  <TableCell className={cn(isCurrentUser ? 'font-bold text-primary' : '')}>{entry.user.username}</TableCell>
                  <TableCell className="text-right">
                    <Badge 
                      variant={isCurrentUser ? "outline" : (entry.score > 0 ? "default" : "secondary")}
                      className={cn("text-md", isCurrentUser ? 'border-primary text-primary' : '')}
                    >
                      {entry.score} {pointsSuffix}
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

export default GenericLeaderboard; 