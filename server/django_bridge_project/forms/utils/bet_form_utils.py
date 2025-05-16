from django import forms
from django_bridge_project.models import Match, Player # Assuming models.py is accessible
from django_bridge_project.enums.prediction_types import PredictionType

class BetFormGenerator:

    @staticmethod
    def create_bet_form_for_match(match: Match, request=None, *args, **kwargs):
        """
        Dynamically creates a Django Form class for betting on a given match.
        The form will include a field for the match winner and fields for each prediction.
        """
        form_fields = {}

        # 1. Add field for match winner
        #    Choices will be Team One, Team Two. Consider adding Draw if applicable.
        winner_choices = [
            (match.team_one.id, match.team_one.name),
            (match.team_two.id, match.team_two.name),
            # You might want to add a 'draw' option, e.g., (0, "Draw")
            # Or handle this based on match.is_winner_needed or a similar field
        ]
        form_fields['match_winner'] = forms.ChoiceField(
            choices=winner_choices,
            label="Predict the Winner",
            required=True,
            widget=forms.RadioSelect # Using RadioSelect for better UX
        )

        # 2. Add fields for each prediction associated with the match
        #    Ensure players for ChoiceFields are loaded efficiently.
        #    It's often better to fetch all players for the two teams once.
        team_one_players = list(match.team_one.players.all().values_list('id', 'first_name', 'last_name'))
        team_two_players = list(match.team_two.players.all().values_list('id', 'first_name', 'last_name'))
        all_match_players_choices = [
            (pid, f"{fname} {lname}") for pid, fname, lname in team_one_players + team_two_players
        ]

        for prediction in match.predictions.all():
            field_name = f'prediction_{prediction.id}'
            field_label = f"{prediction.label} ({prediction.score_points} pts)"
            field_type_enum = PredictionType(prediction.prediction_type) # Convert string to enum member
            field_class = field_type_enum.get_form_field()
            
            field_kwargs = {
                'label': field_label,
                'required': False, # Bets on individual predictions are often optional
            }

            if field_type_enum == PredictionType.PLAYER:
                field_kwargs['choices'] = [(None, '----------')] + all_match_players_choices
            
            if field_type_enum == PredictionType.BOOLEAN:
                 # BooleanField doesn't need a widget specified for default checkbox
                 # It also doesn't typically use help_text in the same way, label is key.
                 pass # Default BooleanField is fine

            if field_type_enum == PredictionType.NUMERICAL:
                field_kwargs['widget'] = forms.NumberInput(attrs={'placeholder': 'Enter a number'})

            form_fields[field_name] = field_class(**field_kwargs)

        # Dynamically create the Form class
        # The `request` and `*args, **kwargs` are for initializing the form instance later
        BetForm = type('BetForm', (forms.Form,), form_fields)
        
        # If request is provided (meaning we are instantiating for a POST or initial GET)
        if request:
            if request.method == 'POST':
                return BetForm(request.POST, *args, **kwargs)
            return BetForm(*args, **kwargs) # For GET
        
        return BetForm # Return the class itself if no request (e.g. for type hinting)
