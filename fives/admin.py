from django.contrib import admin
from fives.models import Player, Game, Participation

# Class to customise the Admin Interface
#class PlayerAdmin(admin.ModelAdmin):
#    list_display = ['gender']
class PlayerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Class to customise the Admin Interface
class GameAdmin(admin.ModelAdmin):
    list_display = ['host', 'date', 'start_time', 'end_time', 'free_slots']
    readonly_fields = ('game_id','custom_slug',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Participation)
