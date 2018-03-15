from django import template

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
