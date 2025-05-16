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
        
        # Ensure this logic runs only if 'correct_value' is an active field in this form instance
        # and we are dealing with an existing prediction instance tied to a match.
        if 'correct_value' in self.fields and \
           self.instance and self.instance.pk and \
           self.instance.prediction_type and \
           hasattr(self.instance, 'match') and self.instance.match:
            
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
    # fieldsets are defined below

    add_page_fieldsets = (
        (None, {
            'fields': ('label', 'prediction_type', 'score_points')
        }),
    )

    change_page_fieldsets = (
        (None, {
            'fields': ('label', 'prediction_type', 'score_points')
        }),
        ('Outcome (Set after match is finished)', {
            'classes': ('collapse',), 
            'fields': ('correct_value',)
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj: 
            return self.add_page_fieldsets
        return self.change_page_fieldsets

    def get_readonly_fields(self, request, obj=None):
        parent_match = None
        if obj and hasattr(obj, 'match') and obj.match:
            parent_match = obj.match
        elif hasattr(request, 'resolver_match') and request.resolver_match and 'object_id' in request.resolver_match.kwargs:
            try:
                match_id = request.resolver_match.kwargs['object_id']
                parent_match = Match.objects.get(pk=match_id)
            except (Match.DoesNotExist, ValueError):
                pass 

        # If points are calculated for the parent match, make ALL fields in the inline read-only.
        if parent_match and parent_match.points_calculation_done:
            all_inline_fields = set()
            for _fieldset_name, fieldset_options in self.get_fieldsets(request, obj):
                if 'fields' in fieldset_options:
                    for field in fieldset_options['fields']:
                        if isinstance(field, (list, tuple)):
                            all_inline_fields.update(f for f in field if isinstance(f, str))
                        elif isinstance(field, str):
                            all_inline_fields.add(field)
            return list(all_inline_fields)
        
        # Otherwise (points not calculated or no parent match context), 
        # rely on superclass or default behavior. 
        # 'correct_value' should be editable in this case.
        return list(super().get_readonly_fields(request, obj) or [])

    def correct_value(self, obj):
        """Custom display for the read-only correct_value field."""
        if obj is None or obj.correct_value is None or obj.correct_value == '':
            return "-" 

        if obj.prediction_type == PredictionType.PLAYER.value:
            try:
                player_id = int(obj.correct_value)
                player = Player.objects.get(pk=player_id)
                return str(player)
            except (ValueError, Player.DoesNotExist):
                return f"Invalid Player ID: {obj.correct_value}"
        elif obj.prediction_type == PredictionType.BOOLEAN.value:
            if str(obj.correct_value).lower() == 'true':
                return "Yes"
            elif str(obj.correct_value).lower() == 'false':
                return "No"
            return obj.correct_value 
        return obj.correct_value 
    correct_value.short_description = 'Correct Outcome' 

# Custom Admin for Match model
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'competition', 'start_datetime', 'is_finished', 'points_calculation_done')
    list_filter = ('competition', 'is_finished', 'start_datetime', 'points_calculation_done')
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

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.points_calculation_done:
            # Make all fields read-only. This should also make inlines non-editable.
            return [field.name for field in obj._meta.fields]
        # If you have other fields that are always read-only, you can add them here:
        # base_readonly_fields = super().get_readonly_fields(request, obj) or [] 
        # return list(base_readonly_fields)
        return [] # Default: no fields are read-only unless specified in readonly_fields attribute

# Register other models
admin.site.register(Competition)
admin.site.register(Team, TeamAdmin) # Use custom TeamAdmin
admin.site.register(Match, MatchAdmin) # Use custom MatchAdmin