from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.forms import formset_factory

from geopy.geocoders import Nominatim
import datetime
import pytz
import sys

from fives.models import User, Player, Game, Participation
from fives.forms import UserForm, PlayerForm, GameForm, RatingForm, RateHostForm, FilterForm

def index(request):
    games = Game.objects.filter(start__gte=datetime.date.today()).order_by('start')[:5]
    context_dict = {'games': games}
    return render(request, 'fives/index.html', context=context_dict)


def about_us(request):
    context_dict = {}
    response = render(request, 'fives/about_us.html', context=context_dict)
    return response

def game_list(request):
    games = Game.objects.filter(start__gte=datetime.date.today()).order_by('start')[:30]
    context_dict = {'games': games}
    return render(request, 'fives/game_list.html', context=context_dict)

def filter_game(request):
    games = Game.objects.filter(start__gte=datetime.date.today()).order_by('start')
    game_type = int(request.POST.get('game_type'))
    if (game_type != 9):
        games = games.filter(game_type=int(game_type))

    games[:30]
    print (games)

    games_filtered = True

    data = {'games_filtered': games_filtered}

    return JsonResponse(data)
    

@login_required
def create_game(request):
    game_form = GameForm()

    # An HTTP POST?
    if request.method == 'POST':
        game_form = GameForm(request.POST)

        # Have we been provided with a valid form?
        if game_form.is_valid():
            # Save, but don't commit
            game = game_form.save(commit=False)

            # Combine date and time for DateTimeField
            date = game_form.cleaned_data["date"]
            time = game_form.cleaned_data["time"]

            #d = datetime.datetime(date.year, date.month, date.day, time.hour, time.minute)
            game.start = datetime.datetime.combine(date, time)
            #game.start = d

            # Get latitiude and longitude from address
            # Source: https://geopy.readthedocs.io/en/1.10.0/
            geolocator = Nominatim()
            location = geolocator.geocode(game.street + " " + game.city)
            game.latitude = location.latitude
            game.longitude = location.longitude

            # Calculate end from start and duration
            game.end = datetime.datetime(date.year, date.month, date.day, time.hour + game.duration, time.minute)

            # Get host entry from current user
            game.host = request.user

            # Save the new Game to the database
            game.save()

            # Add the user to the list of the game's participants.
            user_player = Player.objects.get(user=request.user)
            p = Participation(player=user_player, game=game)
            p.save()

            # Direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors - print them to the terminal.
            print(game_form.errors)

    return render(request, 'fives/create_game.html', {'game_form': game_form})


def show_game(request, game_custom_slug):
    context_dict = {}

    try:
        # Try to find a game with the given slug.
        game = Game.objects.get(custom_slug=game_custom_slug)
        # Retreive a list of all players, and corresponding user entries, participating in the game.
        participants = [p.player for p in Participation.objects.select_related('player').filter(game=game)]
        users = [p.player.user for p in Participation.objects.select_related('player').filter(game=game)]

        # Check if game is in the past.
        now = datetime.datetime.now(pytz.utc)
        gameTookPlace = True if game.end < now else False

        # Add entities to the context dictionary
        context_dict['game'] = game
        context_dict['participants'] = participants
        context_dict['users'] = users
        context_dict['gameTookPlace'] = gameTookPlace

    except Game.DoesNotExist:
        # We get here if we couldn't find the specified game
        context_dict['game'] = None
        context_dict['participants'] = None
        context_dict['users'] = None
        context_dict['gameTookPlace'] = None

    return render(request, 'fives/show_game.html', context=context_dict)

@login_required
def show_past_game(request, player, game_custom_slug):
    try:
        # Try to find a game with the given slug.
        game = Game.objects.get(custom_slug=game_custom_slug)
        # Retreive a list of all players(except current user), and corresponding user entries, participating in the game.
        participants = [p.player for p in Participation.objects.select_related('player').filter(game=game)]
        users = [p.player.user for p in Participation.objects.select_related('player').filter(game=game)]
        # Retreive a list of all players to be rated, all minus the current user.
        playersToBeRated = [p.player for p in Participation.objects.select_related('player').filter(game=game).exclude(player=request.user.player)]
        # Retreive participation relationship.
        participation = Participation.objects.get(game=game, player=request.user.player)
        # Check if game is in the past.
        now = datetime.datetime.now(pytz.utc)
        gameTookPlace = True if game.end < now else False

        context_dict = {'player': player, 'game': game, 'participants': participants, 'users': users, 'gameTookPlace':gameTookPlace, 'participation': participation, 'playersToBeRated': playersToBeRated}

    except Game.DoesNotExist:
        # We get here if we couldn't find the specified game
        context_dict = {'player': None, 'game': None, 'participants': None, 'users': None, 'gameTookPlace':None, 'participation': None, 'playersToBeRated': playersToBeRated}

    # Cerate as many formsets as there are players to be rated(not including the player who is giving ratings).
    RatingFormSet = formset_factory(RatingForm, extra=len(playersToBeRated))

    # An HTTP POST?
    if request.method == 'POST':
        rating_formset = RatingFormSet(request.POST)
        host_form = RateHostForm(request.POST)

        # Have we been provided with a valid form?
        if rating_formset.is_valid():
            index = 0
            for rating_form in rating_formset:
                p = Player.objects.get(user=participants[index].user)
                p.skill += int(rating_form.cleaned_data.get('skill'))
                p.likeability += int(rating_form.cleaned_data.get('likeability'))
                p.punctuality += int(rating_form.cleaned_data.get('punctuality'))
                p.num_player_ratings += 1

                p.save()
                index += 1

            participation.rated = True
            participation.save()

            if request.user != game.host:
                if host_form.is_valid():
                    host = Player.objects.get(user=game.host)
                    host.host_rating += int(host_form.cleaned_data["host_rating"])
                    host.num_host_ratings += 1
                    host.save()

            return HttpResponseRedirect(reverse('show_past_game', kwargs={'player':player, 'game_custom_slug':game_custom_slug}))
        else:
            # Print problems to the terminal.
            print(rating_form.errors)
            print(host_form.errors)
    else:
        # Not an HTTP POST, so we render our forms.
        # These forms will be blank, ready for user input.
        rating_formset = RatingFormSet()
        host_form = RateHostForm()

    context_dict['rating_formset'] = rating_formset
    context_dict['host_form'] = host_form

    return render(request, 'fives/show_past_game.html', context=context_dict)


@login_required
def join_game(request, game_custom_slug):
    gameid = request.POST.get('gameid')
    game = Game.objects.get(game_id=gameid)

    username = request.POST.get('user')
    user = User.objects.get(username=username)
    player=Player.objects.get(user=user) # player = Player.objects.get(user=request.user)

    if game:
        if game.free_slots == 0:
            player_added = False
        else:
            game.free_slots -= 1
            game.save()
            p = Participation(player=player, game=game)
            p.save()
            player_added = True
    else:
        player_added = False

    data = {'player_added': player_added}

    return JsonResponse(data)

@login_required
def leave_game(request, game_custom_slug):
    gameid = request.POST.get('gameid')
    game = Game.objects.get(game_id=gameid)

    username = request.POST.get('user')
    user = User.objects.get(username=username)
    player=Player.objects.get(user=user)

    if game:
        p = Participation.objects.get(player=player, game=game)
        p.delete()
        game.free_slots += 1
        game.save()
        player_removed = True
    else:
        player_removed = False

    data = {'player_removed': player_removed}

    return JsonResponse(data)

@login_required
def delete_game(request, game_custom_slug):
    gameid = request.POST.get('gameid')
    game = Game.objects.get(game_id=gameid)

    username = request.POST.get('user')
    user = User.objects.get(username=username)
    player=Player.objects.get(user=user)

    game.delete()

    try:
        game = Game.objects.get(game_id=gameid)
        game_deleted = False
    except Game.DoesNotExist:
        game_deleted = True

    data = {'game_deleted': game_deleted}

    return JsonResponse(data)

def update_pitch(request, game_custom_slug):
    gameid = request.POST.get('gameid')
    game = Game.objects.get(game_id=gameid)

    pitch_updated = False
    if game:
        game.booked = not game.booked
        game.save()
        pitch_updated = True

    data = {'pitch_updated': pitch_updated}

    return JsonResponse(data)

###############################################
# User-centric Views
###############################################

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

def user_account(request, player):
    context_dict = {}
    user = User.objects.get(username=player)
    player = Player.objects.get(user=user)

    gameSlugs = [g.game.custom_slug for g in Participation.objects.select_related('game').filter(player=player)]

    joinedGames = Game.objects.filter(custom_slug__in=gameSlugs).exclude(host=user).filter(
        start__gte=datetime.date.today()).order_by('start')[:20]

    hostingGames = Game.objects.filter(host=user).filter(start__gte=datetime.date.today()).order_by('start')[:20]

    pastGames = Game.objects.filter(custom_slug__in=gameSlugs).filter(
        start__lt=datetime.date.today()).order_by('-start')[:5]

    context_dict = {'player': player, 'joinedGames': joinedGames, 'hostingGames': hostingGames, 'pastGames': pastGames}

    return render(request, 'fives/user_account.html', context=context_dict)

def history(request, player):
    context_dict = {}
    user = User.objects.get(username=player)
    player = Player.objects.get(user=user)

    gameSlugs = [g.game.custom_slug for g in Participation.objects.select_related('game').filter(player=player)]
    fullHistory = Game.objects.filter(custom_slug__in=gameSlugs).filter(
        start__lt=datetime.date.today()).order_by('-start')

    context_dict = {'player': player, 'fullHistory': fullHistory}

    return render(request, 'fives/history.html', context=context_dict)
