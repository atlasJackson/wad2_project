from django.shortcuts import render
from fives.models import Player, Game
from fives.forms import GameForm


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
    form = GameForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = GameForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new Match to the database
            match = form.save(commit=True)
            print(match)
            # Now that the Match is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    response = render(request, 'fives/create_match.html', {'form': form})
    return response

def login(request):
    context_dict = {}
    response = render(request, 'fives/login.html', context=context_dict)
    return response

def sign_up(request):
    context_dict = {}
    response = render(request, 'fives/sign_up.html', context=context_dict)
    return response
