from django.shortcuts import render
from fives.models import Player, Game


def index(request):
    context_dict = {}
    response = render(request, 'fives/index.html', context=context_dict)
    return response
