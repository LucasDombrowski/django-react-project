from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Competition, Team, Player, Match, Prediction, Bet, Answer

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

# Custom Admin for Match model
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'competition', 'start_datetime', 'is_finished')
    list_filter = ('competition', 'is_finished', 'start_datetime')
    search_fields = ('team_one__name', 'team_two__name', 'competition__name')

    # Define the fieldsets for the 'add' page
    add_page_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('competition', 'team_one', 'team_two', 'start_datetime', 'score_points'),
        }),
    )

    # Define the fieldsets for the 'change' page (includes the results)
    change_page_fieldsets = (
        (None, {
            'fields': ('competition', 'team_one', 'team_two', 'start_datetime', 'score_points'),
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