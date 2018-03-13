from django import template

register = template.Library()

@register.filter(name='divide')
def divide(value, arg):
    try:
        return round(value / (arg * 1.0)) # Returns an integer rounded to the next integer from float divison.
    except (ValueError, ZeroDivisionError):
        return 0 # In case a player has no ratings.
