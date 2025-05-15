import enum

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

    # If you want to easily get the display name in other parts of your code:
    # @property
    # def display_name(self):
    #     # You would need to adjust this if CHOICES is no longer a static list on the class
    #     # A possible implementation:
    #     choices_dict = {choice[0]: choice[1] for choice in self.get_choices()}
    #     return choices_dict.get(self.value, str(self.name).title()) 