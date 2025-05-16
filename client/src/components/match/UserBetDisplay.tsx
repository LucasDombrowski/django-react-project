import React from 'react';
import {
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"; // Import Table components
import { cn } from '@/libs/utils';
import matchDetailStrings from '@/libs/keychains/matchDetail.json'; // Import keychain
// Import the consolidated types
import { UserBetDetailsType } from '@/libs/types/bets';

interface UserBetDisplayProps {
  details: UserBetDetailsType;
  matchScorePoints?: number; // Pass match.score_points specifically for winner
}

const UserBetDisplay: React.FC<UserBetDisplayProps> = ({ details, matchScorePoints }) => {
  if (!details) return null;

  const winnerPoints = details.chosen_winner?.score_points ?? matchScorePoints;

  return (
    <Card className={cn("shadow-xl", "w-full")}>
      <CardHeader>
        <CardTitle className="text-2xl font-semibold text-foreground">{matchDetailStrings.user_bet_display_title}</CardTitle>
        <CardDescription className="text-muted-foreground">
          {matchDetailStrings.user_bet_display_description}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Display Predicted Winner Separately */}
        {details.chosen_winner && (
          <Card className="bg-muted/50">
            <CardHeader>
              <CardTitle className="text-xl">{matchDetailStrings.user_bet_display_predicted_winner_title}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between items-center">
                <p className="text-lg text-primary">
                  {details.chosen_winner.name}
                </p>
                {winnerPoints !== undefined && (
                    <Badge variant="outline" className="text-base">
                        {winnerPoints} pts
                    </Badge>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Display Prediction Answers in a Table */}
        <div>
          <h3 className="text-xl font-semibold text-foreground mb-4">{matchDetailStrings.user_bet_display_detailed_predictions_title}</h3>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[60%]">{matchDetailStrings.user_bet_display_table_header_prediction}</TableHead>
                <TableHead>{matchDetailStrings.user_bet_display_table_header_your_answer}</TableHead>
                <TableHead className="text-right">{matchDetailStrings.user_bet_display_table_header_points}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {details.answers.map((answer) => (
                <TableRow key={answer.prediction_id}>
                  <TableCell className="font-medium text-foreground">{answer.prediction_label}</TableCell>
                  <TableCell className="text-primary">{`${answer.user_answer_display}`}</TableCell>
                  <TableCell className="text-right">
                    <Badge variant="secondary">{answer.prediction_score_points} pts</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
};

export default UserBetDisplay;

// Note: The points for "Predicted Winner" might need a dedicated way to be passed
// if `match.score_points` is not directly tied to a prediction named "MATCH_WINNER".
// The current BetFormGenerator puts points on its label. For display here, we either need
// to ensure it's one of the `answers` with that type or pass `match.score_points` separately to this component. 