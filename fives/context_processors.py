# Code based on comment on Stack Overflow:
# https://stackoverflow.com/questions/17901341/django-how-to-make-a-variable-available-to-all-templates

# Pass api_key to template context.
def api_key_processor(request):
    api_key = "AIzaSyDUX2r2xDl7hy2QUQOyzS7ACOPLUqWWEDw" # YOUR API_KEY HERE
    return {'api_key': api_key}