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
  // matchScorePoints is now part of details.chosen_winner.score_points
}

const UserBetDisplay: React.FC<UserBetDisplayProps> = ({ details }) => {
  if (!details) return null;

  const { chosen_winner, answers, points_have_been_calculated, total_gained_points } = details;

  return (
    <Card className={cn("shadow-xl", "w-full")}>
      <CardHeader>
        <CardTitle className="text-2xl font-semibold text-foreground">{matchDetailStrings.user_bet_display_title}</CardTitle>
        <CardDescription className="text-muted-foreground">
          {points_have_been_calculated ? 
            matchDetailStrings.user_bet_display_description_results_in :
            matchDetailStrings.user_bet_display_description
          }
        </CardDescription>
        {points_have_been_calculated && total_gained_points !== undefined && (
            <div className="mt-2 text-lg font-semibold">
                <span className="text-primary">{matchDetailStrings.total_gained_points_on_match_label} </span> 
                <Badge variant={total_gained_points > 0 ? "default" : "secondary"} className="text-lg">{total_gained_points} pts</Badge>
            </div>
        )}
      </CardHeader>
      <CardContent className="space-y-6">
        {chosen_winner && (
          <Card className="bg-muted/50">
            <CardHeader>
              <CardTitle className="text-xl">{matchDetailStrings.user_bet_display_predicted_winner_title}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex justify-between items-center">
                <p className="text-lg text-primary">
                  {matchDetailStrings.your_prediction_label} {chosen_winner.name}
                </p>
                {chosen_winner.score_points !== undefined && (
                    <Badge variant="outline" className="text-sm">
                        {matchDetailStrings.potential_points_label} {chosen_winner.score_points} pts
                    </Badge>
                )}
              </div>
              {points_have_been_calculated && chosen_winner.actual_winner_details && (
                <div className="mt-2 pt-2 border-t">
                  <div className="flex justify-between items-center">
                    <p className="text-md font-semibold">
                        {matchDetailStrings.actual_winner_label} {chosen_winner.actual_winner_details.name}
                    </p>
                    <Badge 
                        variant={(chosen_winner.gained_points_for_winner ?? 0) > 0 ? "default" : "secondary"}
                        className="text-sm"
                    >
                       {matchDetailStrings.gained_points_label} {chosen_winner.gained_points_for_winner ?? 0} pts
                    </Badge>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        <div>
          <h3 className="text-xl font-semibold text-foreground mb-4">{matchDetailStrings.user_bet_display_detailed_predictions_title}</h3>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[40%]">{matchDetailStrings.user_bet_display_table_header_prediction}</TableHead>
                <TableHead>{matchDetailStrings.user_bet_display_table_header_your_answer}</TableHead>
                {points_have_been_calculated && (
                  <>
                    <TableHead>{matchDetailStrings.user_bet_display_table_header_correct_answer}</TableHead>
                    <TableHead className="text-right">{matchDetailStrings.user_bet_display_table_header_gained_points}</TableHead>
                  </>
                )}
                <TableHead className="text-right">{matchDetailStrings.user_bet_display_table_header_potential_points}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {answers.map((answer) => (
                <TableRow key={answer.prediction_id}>
                  <TableCell className="font-medium text-foreground">{answer.prediction_label}</TableCell>
                  <TableCell className="text-primary">{`${answer.user_answer_display}`}</TableCell>
                  {points_have_been_calculated && (
                    <>
                      <TableCell className="text-muted-foreground">{answer.correct_value_display ?? 'N/A'}</TableCell>
                      <TableCell className="text-right">
                        <Badge 
                            variant={(answer.gained_points ?? 0) > 0 ? "default" : "secondary"}
                        >
                            {answer.gained_points ?? 0} pts
                        </Badge>
                      </TableCell>
                    </>
                  )}
                  <TableCell className="text-right">
                    <Badge variant="outline">{answer.prediction_score_points} pts</Badge>
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