from . import settings

# Code based on comment on Stack Overflow:
# https://stackoverflow.com/questions/17901341/django-how-to-make-a-variable-available-to-all-templates

# Pass api_key to template context.
def api_key_processor(request):
    api_key = settings.GOOGLE_API_KEY
    return {'api_key': api_key}