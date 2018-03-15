from django import template
from fives.models import Participation, Player, Game

register = template.Library()

@register.filter(name='divide')
def divide(value, arg):
    try:
        return round(value / (arg * 1.0)) # Returns an integer rounded to the next integer from float divison.
    except (ValueError, ZeroDivisionError):
        return 0 # In case a player has no ratings.


@register.filter(name='getName')
def getName(list, i):
    return list[i].user.first_name

@register.filter(name='getSurname')
def getSurname(list, i):
    return list[i].user.last_name

@register.filter(name='getGender')
def getGender(list, i):
    return list[i].gender

@register.filter(name='isRated')
def isRated(game, user):
    p = Participation.objects.get(game=game, player=user.player)
    return p.rated

@register.filter(name='getType')
def getType(value):
    for elm in Game.GAME_CHOICES:
        if value in elm:
            return elm[1]
    return "No Type"

@register.filter(name='getRating')
def getRating(player, rating):
    try:
        if rating == "skill":
            value = player.skill
        elif rating == "likeability":
            value = player.likeability
        elif rating == "punctuality":
            value = player.punctuality
        return round(value / (player.num_player_ratings * 1.0))
    except (ValueError, ZeroDivisionError):
        return 0 # In case a player has no ratings.
