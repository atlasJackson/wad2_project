from django.shortcuts import render
from fives.models import Player, Game


def index(request):
    context_dict = {}
    response = render(request, 'fives/index.html', context=context_dict)
    return response

def about_us(request):
    context_dict = {}
    response = render(request, 'fives/about_us.html', context=context_dict)
    return response

def match_list(request):
    context_dict = {}
    response = render(request, 'fives/match_list.html', context=context_dict)
    return response

def create_match(request):
    context_dict = {}
    response = render(request, 'fives/create_match.html', context=context_dict)
    return response
