import enum
from django import forms # Import forms module

class PredictionType(enum.Enum):
    NUMERICAL = "numerical"
    PLAYER = "player"
    BOOLEAN = "boolean"

    @classmethod
    def get_choices(cls): # Renamed to avoid conflict if CHOICES was a property
        return [
            (cls.NUMERICAL.value, "Numerical"),
            (cls.PLAYER.value, "Player"),
            (cls.BOOLEAN.value, "Boolean"),
        ]

    def get_form_field(self):
        if self == PredictionType.NUMERICAL:
            return forms.IntegerField # Using IntegerField for numerical predictions
        elif self == PredictionType.PLAYER:
            # For player, we'll return ChoiceField. Choices will be populated later.
            return forms.ChoiceField
        elif self == PredictionType.BOOLEAN:
            # BooleanField by default uses a CheckboxInput widget
            return forms.BooleanField
        raise ValueError(f"Unsupported prediction type: {self.value}")
