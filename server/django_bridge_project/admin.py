from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.db.models import Q
from .models import CustomUser, Competition, Team, Player, Match, Prediction, Bet, Answer
from .enums.prediction_types import PredictionType

# To customize the CustomUser admin:
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('score',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('score',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('score',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Inline for Players within Team Admin
class PlayerInline(admin.StackedInline):
    model = Player
    extra = 1 # Number of empty forms to display
    # No 'fields' attribute here means it will show all fields by default
    # fields = ['first_name', 'last_name', 'role'] # Removed this line
    # readonly_fields = ['photo', 'birth_date'] 

# Custom Admin for Team model
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [PlayerInline]

# Custom ModelForm for Prediction inline
class PredictionAdminForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure this logic runs only for existing instances with a prediction_type and match
        if self.instance and self.instance.pk and self.instance.prediction_type and hasattr(self.instance, 'match') and self.instance.match:
            prediction_type = self.instance.prediction_type
            match_instance = self.instance.match

            # Make correct_value not required by default as model field allows blank/null
            self.fields['correct_value'].required = False

            if prediction_type == PredictionType.NUMERICAL.value:
                self.fields['correct_value'].widget = forms.NumberInput()
                self.fields['correct_value'].help_text = "Enter the correct numerical value."
            elif prediction_type == PredictionType.BOOLEAN.value:
                self.fields['correct_value'].widget = forms.Select(choices=[
                    ('', '---------'), 
                    ('True', 'Yes'), 
                    ('False', 'No')
                ])
                self.fields['correct_value'].help_text = "Select Yes (True) or No (False)."
            elif prediction_type == PredictionType.PLAYER.value:
                players = Player.objects.filter(
                    Q(team=match_instance.team_one) | Q(team=match_instance.team_two)
                ).distinct().order_by('last_name', 'first_name')
                
                player_choices = [('', '---------')]
                player_choices.extend([(str(p.id), str(p)) for p in players])
                
                self.fields['correct_value'].widget = forms.Select(choices=player_choices)
                self.fields['correct_value'].help_text = "Select the correct player by ID."
            else:
                # Default for other types or if something is unexpected
                self.fields['correct_value'].help_text = "Enter the correct value based on the prediction type."

# Inline for Predictions within Match Admin
class PredictionInline(admin.StackedInline):
    model = Prediction
    form = PredictionAdminForm # Assign the custom form
    extra = 1
    # Simplified fieldset, description is now in model field's help_text
    # fields = ('label', 'prediction_type', 'score_points', 'correct_value') # We'll use fieldsets instead

    # Define the fieldsets for the 'add' page of the parent (Match)
    add_page_fieldsets = (
        (None, {
            'fields': ('label', 'prediction_type', 'score_points')
        }),
    )

    # Define the fieldsets for the 'change' page of the parent (Match)
    change_page_fieldsets = (
        (None, {
            'fields': ('label', 'prediction_type', 'score_points')
        }),
        ('Outcome (Set after match is finished)', {
            'classes': ('collapse',), # Keep it collapsed by default on change page
            'fields': ('correct_value',)
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:  # This is an add form for the Match (parent obj is None)
            return self.add_page_fieldsets
        return self.change_page_fieldsets # This is a change form for the Match

# Custom Admin for Match model
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'competition', 'start_datetime', 'is_finished')
    list_filter = ('competition', 'is_finished', 'start_datetime')
    search_fields = ('team_one__name', 'team_two__name', 'competition__name')
    inlines = [PredictionInline] # Added PredictionInline here

    # Define the fieldsets for the 'add' page
    add_page_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('competition', 'team_one', 'team_two', 'is_winner_needed', 'start_datetime', 'score_points'),
        }),
    )

    # Define the fieldsets for the 'change' page (includes the results)
    change_page_fieldsets = (
        (None, {
            'fields': ('competition', 'team_one', 'team_two', 'is_winner_needed', 'start_datetime', 'score_points'),
        }),
        ('Match Result', {
            'classes': ('collapse',),
            'fields': ('team_one_score', 'team_two_score', 'team_one_draw_score', 'team_two_draw_score', 'is_finished'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:  # This is an add form (obj is None)
            return self.add_page_fieldsets
        return self.change_page_fieldsets # This is a change form

# Register other models
admin.site.register(Competition)
admin.site.register(Team, TeamAdmin) # Use custom TeamAdmin
admin.site.register(Match, MatchAdmin) # Use custom MatchAdmin