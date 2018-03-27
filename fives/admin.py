from django.contrib import admin
from fives.models import Player, Game, Participation

# Class to customise the Admin Interface for Player
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender']
    readonly_fields = ('id',)

# Class to customise the Admin Interface for Game
class GameAdmin(admin.ModelAdmin):
    list_display = ['host', 'start', 'end', 'free_slots']
    readonly_fields = ('game_id','custom_slug',)

# Class to customise the Admin Interface for Participation
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['player', 'game', 'rated']
    readonly_fields = ('player','game',)

admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Participation, ParticipationAdmin)
