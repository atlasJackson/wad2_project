from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
import datetime

from fives.models import Player, Game
from fives.forms import UserForm, PlayerForm, GameForm


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

@login_required
def create_match(request):
    game_form = GameForm()

    # An HTTP POST?
    if request.method == 'POST':
        game_form = GameForm(request.POST)

        # Have we been provided with a valid form?
        if game_form.is_valid():
            # Save, but don't commit
            game = game_form.save(commit=False)

            # Calculate end time from start time and duration
            end_time_hour = (game.start_time.hour + game.duration) % 24
            game.end_time = datetime.time(end_time_hour, game.start_time.minute)
            
            # Get host entry from current user
            game.host = request.user
            # Save the new Match to the database
            game.save()

            # Direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors - print them to the terminal.
            print(game_form.errors)

    return render(request, 'fives/create_match.html', {'game_form': game_form})

def sign_up(request):
    # A boolean value for telling the template
    # whether the registration was succesful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's an HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        player_form = PlayerForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and player_form.is_valid():
            # Save the user's data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the Player instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            player = player_form.save(commit=False)
            player.user = user

            # Now we save the Player model instance.
            player.save()

            # Update our variables to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Print problems to the terminal.
            print(user_form.errors, player_form.errors)
    else:
        # Not an HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        player_form = PlayerForm()

    # Render the template depending on the context.
    return render(request,
                  'fives/sign_up.html',
                  {'user_form': user_form,
                  'player_form': player_form,
                  'registered': registered}
                  )

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'] because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'fives/login.html', {})

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))

def my_account(request):
    context_dict = {}
    response = render(request, 'fives/my_account.html', context=context_dict)
    return response
