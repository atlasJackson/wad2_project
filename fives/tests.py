from django.contrib.auth.models import User
from fives.models import Player, Game, Participation
from django.test import TestCase

from geopy.geocoders import Nominatim
from datetime import datetime
import uuid

# Create your tests here.
class PlayerMethodTests(TestCase):
    # Test the string representation of the player returns their username. 
    def test_player_string_representation(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.assertEqual(str(test_player), test_user.username)

def generate_test_user(username, password, email, first_name, last_name):
    u = create_user(username, password, email, first_name, last_name)
    p = create_player(u)
    return u, p

def create_user(username, password, email, first_name, last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.email = email
    u.first_name = first_name
    u.last_name = last_name
    u.save()
    return u

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

class GameMethodTests(TestCase):
    def test_game_string_representation(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        test_game = create_game(0, 9, "2018-02-28 14:00", "2018-02-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        self.assertEqual(str(test_game), str(test_game.host) + " " + str(test_game.start) + " " + str(test_game.game_id)[:6])

def create_game(game_type, free_slots, start, end, duration,
            street, city, postcode, price, booked, host):

    start = datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = datetime.strptime(end, '%Y-%m-%d %H:%M')

    g = Game.objects.get_or_create(host=host,
        start=start, end=end, price=price)[0]

    g.game_type = game_type
    g.free_slots = free_slots
    g.duration = duration
    g.street = street
    g.city = city
    g.postcode = postcode
    geolocator = Nominatim()
    location = geolocator.geocode(g.street + " " + g.city)
    g.latitude = location.latitude
    g.longitude = location.longitude
    g.booked = booked
    g.save()
    return g