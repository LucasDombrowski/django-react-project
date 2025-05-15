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
