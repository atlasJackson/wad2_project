from django import template
from fives.models import Participation, Player, Game
register = template.Library()

# Add a css class to a field.
@register.filter(name='addCss')
def addCss(field, css):
   return field.as_widget(attrs={"class":css})

# Return name for player in the list. Used in template to rate players.
@register.filter(name='getName')
def getName(list, i):
    return list[i].user.first_name

# Return surname for player in the list. Used in template to rate players.
@register.filter(name='getSurname')
def getSurname(list, i):
    return list[i].user.last_name

# Return gender for player in the list. Used in template to rate players.
@register.filter(name='getGender')
def getGender(list, i):
    return list[i].gender

# Return boolean, depending if a user has already rated a game or not.
@register.filter(name='isRated')
def isRated(game, user):
    p = Participation.objects.get(game=game, player=user.player)
    if game.free_slots == 9 and game.host == user: # This is the case if the host was the only player in that game, so he doesn't see an empty rating page with no players to rate.
        return True # Return True for "already rated".
    return p.rated

# Return the game type as string representation.
@register.filter(name='getType')
def getType(value):
    for elm in Game.GAME_CHOICES:
        if value in elm:
            return elm[1]
    return "No Type"

# Return duration of a game. Used for filtering the game list.
@register.filter(name='duration')
def duration(start, end):
    dt = end - start
    return dt.days * 24 + dt.seconds // 3600

# Returns a string of length equal to the player's rating defined by the parameter
# Used in for-loops to display icons for ratings.
@register.filter(name='ratingAsRange')
def ratingAsRange(player, label):
    switcher = {
        "skill": player.skill,
        "likeability": player.likeability,
        "punctuality": player.punctuality,
        "host": player.host_rating
    }
    rating = switcher.get(label, 0)

    try:
        if label == "host":
            rating = round(rating / (player.num_host_ratings * 1.0))
        else:
            rating = round(rating / (player.num_player_ratings * 1.0))
    except (ValueError, ZeroDivisionError):
        rating = 0 # In case a player has no ratings.

    string = ""
    for i in range(0, int(rating)):
        string += " "
    return string
