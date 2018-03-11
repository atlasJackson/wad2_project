from django.contrib import admin
from fives.models import Player, Game, Participation

# Class to customise the Admin Interface
#class PlayerAdmin(admin.ModelAdmin):
#    list_display = ['gender']

# Class to customise the Admin Interface
class GameAdmin(admin.ModelAdmin):
    list_display = ['host', 'date', 'start_time', 'end_time', 'free_slots']
    prepopulated_fields = {'custom_slug':('custom_slug',)}


admin.site.register(Player)#, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Participation)
