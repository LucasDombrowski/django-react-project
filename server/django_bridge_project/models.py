from django.db import models
from django.conf import settings # Import settings to get AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser # Import AbstractUser
from .enums.prediction_types import PredictionType # Import the enum
from .validators.image_validators import CustomImageValidator # Added import

class CustomUser(AbstractUser):
    # Add any additional fields here. For example:
    # bio = models.TextField(blank=True)
    score = models.IntegerField(default=0, help_text="The user's current score in the betting game.")

    def __str__(self):
        return self.username

class Competition(models.Model):
    name = models.CharField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='competition_logos/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.logo and hasattr(self.logo, 'file'): # Check if file exists
            CustomImageValidator.validate(self.logo.file, "Logo")

    class Meta:
        ordering = ['start_date', 'name']
        verbose_name = "Competition"
        verbose_name_plural = "Competitions"


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.logo and hasattr(self.logo, 'file'): # Check if file exists
            CustomImageValidator.validate(self.logo.file, "Logo")

    class Meta:
        ordering = ['name']
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True) # e.g., Forward, Midfielder, Defender, Goalkeeper
    photo = models.ImageField(upload_to='player_photos/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        if self.photo and hasattr(self.photo, 'file'): # Check if file exists
            CustomImageValidator.validate(self.photo.file, "Photo")

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Player"
        verbose_name_plural = "Players"


class Match(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matches')

    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    team_one_score = models.IntegerField(default=0)
    team_two_score = models.IntegerField(default=0)

    #These following scores will be filled only if the match was finished at a draw and it needed a winner
    is_winner_needed = models.BooleanField(default=False, help_text="If True, the match needs a winner and it can be sometimes decided by a draw score.")
    team_one_draw_score = models.IntegerField(blank=True, null=True, help_text="The score of the match if it was a draw and it needed a winner.")
    team_two_draw_score = models.IntegerField(blank=True, null=True, help_text="The score of the match if it was a draw and it needed a winner.")

    score_points = models.IntegerField(default=10, help_text="Points awarded if the user's bet on this match is correct.")
    start_datetime = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    points_calculation_done = models.BooleanField(default=False, help_text="True if points have been calculated and attributed for this finished match.")

    def __str__(self):
        return f"{self.team_one.name} vs {self.team_two.name} ({self.competition.name} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        ordering = ['start_datetime']
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        # A team cannot play against itself. We can add a custom validation for this in the form/admin.


class Prediction(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='predictions')
    label = models.CharField(max_length=255, help_text="The question or description for this prediction. E.g., 'Final score of Team A?', 'First player to score?', 'Will a penalty be awarded?'")
    prediction_type = models.CharField(
        max_length=20,
        choices=PredictionType.get_choices(),
        default=PredictionType.NUMERICAL.value,
        help_text=(
            "Numerical: Expects a number (e.g., score, count).<br>"
            "Player: Expects a selection of a player (stores Player ID).<br>"
            "Boolean: Expects a Yes/No or True/False choice."
        )
    )
    score_points = models.IntegerField(default=10, help_text="Points awarded if the user's bet on this prediction is correct.")
    correct_value = models.CharField(max_length=255, blank=True, null=True, help_text="The actual outcome of this prediction, filled after the match is settled.")

    def __str__(self):
        return f"{self.label} ({self.get_prediction_type_display()}) for Match {self.match.id}"

    class Meta:
        ordering = ['match', 'label']
        verbose_name = "Prediction Criterion"
        verbose_name_plural = "Prediction Criteria"
        # You might want a prediction label to be unique per match:
        # unique_together = (('match', 'label'),)


class Bet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='bets')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bets')
    winner_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner_bets', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bet by {self.user.username} on Match {self.match.id}"

    class Meta:
        ordering = ['match', 'user']
        unique_together = (('match', 'user'),) # Ensures a user can only have one Bet instance per match
        verbose_name = "Bet Slip"
        verbose_name_plural = "Bet Slips"


class Answer(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, related_name='answers')
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name='user_answers')
    
    value = models.CharField(max_length=255) 

    def __str__(self):
        return f"Answer by {self.bet.user.username} for '{self.prediction.label}': {self.value}"

    class Meta:
        unique_together = (('bet', 'prediction'),)
        ordering = ['bet', 'prediction']
        verbose_name = "User's Answer"
        verbose_name_plural = "User's Answers"