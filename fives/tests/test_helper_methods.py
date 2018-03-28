from django.contrib.auth.models import User
from fives.models import Player, Game, Participation
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import pytz
import uuid

##############################################################################################################
### USER/PLAYER HELPER METHODS
##############################################################################################################

# Helper method to create a user object.
def create_user(username, password, email, first_name, last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.email = email
    u.first_name = first_name
    u.last_name = last_name
    u.save()
    return u

# Helper method to create a player object corresponding to the user passed in as a parameter.
def create_player(user, gender=0, host_rating=0, num_host_ratings=0, punctuality=0, likeability=0, skill=0, num_player_ratings=0):
    u = User.objects.get_or_create(username=user)[0]
    p = Player.objects.get_or_create(user=u)[0]
    p.gender = gender
    p.host_rating = host_rating
    p.num_host_ratings = num_host_ratings
    p.punctuality = punctuality
    p.likeability = likeability
    p.skill = skill
    p.num_player_ratings = num_player_ratings
    p.save()
    return p

# Helper method to return user and player objects.
def generate_test_user(username, password, email, first_name, last_name):
    u = create_user(username, password, email, first_name, last_name)
    p = create_player(u)
    return u, p


##############################################################################################################
### GAME HELPER METHODS
##############################################################################################################

# Helper method to create a game object.
def create_game(game_type, free_slots, start, end, duration,
            street, city, postcode, price, booked, host):

    # The following page helped solve the issue of a runtime warning appearing for using a naive datetime.
    # https://stackoverflow.com/questions/7065164/how-to-make-an-unaware-datetime-timezone-aware-in-python
    start = datetime.strptime(start, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.UTC)
    end = datetime.strptime(end, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.UTC)

    g = Game.objects.get_or_create(host=host,
        start=start, end=end, price=price)[0]

    g.game_type = game_type
    g.free_slots = free_slots
    g.duration = duration
    g.street = street
    g.city = city
    g.postcode = postcode
    geolocator = Nominatim(scheme='http')
    location = geolocator.geocode(g.street + " " + g.city)
    g.latitude = location.latitude
    g.longitude = location.longitude
    g.booked = booked
    g.save()
    return g

# Helper method to populate the database with some test games that have already taken place.
def generate_past_test_games(host):
    start_datetime, end_datetime = start_and_end_datetime_generator(-240,1)
    create_game(0, 9, start_datetime, end_datetime, 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, host)

    start_datetime, end_datetime = start_and_end_datetime_generator(-120,2)
    create_game(1, 9, start_datetime, end_datetime, 2, "10 Keith St", "Glasgow", "G11 5DD", 0, 0, host)

    start_datetime, end_datetime = start_and_end_datetime_generator(-48,1)
    create_game(2, 9, start_datetime, end_datetime, 1, "Greendyke St", "Glasgow", "G1 5DB", 2, 1, host)

    start_datetime, end_datetime = start_and_end_datetime_generator(-24,1)
    create_game(3, 9, start_datetime, end_datetime, 1, "33 Scotland St", "Glasgow", "G5 8NB", 10, 1, host)

# Helper method to populate the database with some test games that have yet to be played.
def generate_future_test_games(host):
    start_datetime, end_datetime = start_and_end_datetime_generator(240,1)
    create_game(0, 9, start_datetime, end_datetime, 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, host)

    start_datetime, end_datetime = start_and_end_datetime_generator(120,2)
    create_game(1, 9, start_datetime, end_datetime, 2, "10 Keith St", "Glasgow", "G11 5DD", 0, 0, host)

    start_datetime, end_datetime = start_and_end_datetime_generator(48,1)
    create_game(2, 9, start_datetime, end_datetime, 1, "Greendyke St", "Glasgow", "G1 5DB", 2, 1, host)

    start_datetime, end_datetime = start_and_end_datetime_generator(24,1)
    create_game(3, 9, start_datetime, end_datetime, 1, "33 Scotland St", "Glasgow", "G5 8NB", 10, 1, host)

def generate_past_and_future_test_games(host):
    generate_past_test_games(host=host)
    generate_future_test_games(host=host)

# Helper method to create a participation object.
def create_participation(game, player, rated):
    p = Participation(game=game, player=player, rated=rated)
    p.save()
    return p

##############################################################################################################
### DATETIME HELPER METHODS
##############################################################################################################

# Helper method that returns a start date and a start time string from the current time's hour plus the parameter hours from that time.
def start_date_and_time_generator(hours):
    now = datetime.now(pytz.UTC)
    start_datetime = now + timedelta(hours=hours)

    start_date = start_datetime.strftime('%Y-%m-%d')
    start_time = start_datetime.strftime('%H:%M')

    return start_date, start_time

# Helper method that returns a start datetime string from the current time's hour plus the parameter hours from that time.
# Endtime is calculated from duration.
def start_and_end_datetime_generator(hours, duration):
    now = datetime.now(pytz.UTC)
    start_datetime = now + timedelta(hours=hours)
    end_datetime = start_datetime + timedelta(hours=+duration)

    start_datetime = start_datetime.strftime('%Y-%m-%d %H:%M')
    end_datetime = end_datetime.strftime('%Y-%m-%d %H:%M')

    return start_datetime, end_datetime
