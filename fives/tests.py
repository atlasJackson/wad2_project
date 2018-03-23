from django.contrib.auth.models import User
from fives.models import Player, Game, Participation
from django.test import TestCase
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import uuid

### Model Tests
class PlayerMethodTests(TestCase):
    # Test that the string representation of the player returns their username.
    def test_player_string_representation(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.assertEqual(str(test_player), test_user.username)

# Helper method to return user and player objects.
def generate_test_user(username, password, email, first_name, last_name):
    u = create_user(username, password, email, first_name, last_name)
    p = create_player(u)
    return u, p

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

class GameMethodTests(TestCase):
    # Test that the string representation of the game returns the concatenation of the host, start date and game id (auto-generated).
    def test_game_string_representation(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        test_game = create_game(0, 9, "2018-02-28 14:00", "2018-02-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        self.assertEqual(str(test_game), str(test_game.host) + " " + str(test_game.start) + " " + str(test_game.game_id)[:6])

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
    geolocator = Nominatim()
    location = geolocator.geocode(g.street + " " + g.city)
    g.latitude = location.latitude
    g.longitude = location.longitude
    g.booked = booked
    g.save()
    return g

class ParticipationMethodTests(TestCase):
    # Test that the string representation of the participation object returns the concatenation of the player, game and rating.
    def test_participation_string_representation(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        test_game = create_game(0, 9, "2018-02-28 14:00", "2018-02-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        test_participation = create_participation(test_game, test_player, 0)
        self.assertEqual(str(test_participation), str(test_participation.player) + " " + str(test_participation.game) + " " + str(test_participation.rated))

# Helper method to create a participation object.
def create_participation(game, player, rated):
    p = Participation(game=game, player=player, rated=rated)
    p.save()
    return p

### View Tests
class IndexViewTests(TestCase):

    def test_index_view_with_no_games(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no scheduled matches.")
        self.assertQuerysetEqual(response.context['games'], [])

    def test_index_view_with_games(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        create_game(0, 9, "2018-02-28 14:00", "2018-02-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        create_game(1, 9, "2018-02-22 11:00", "2018-02-22 13:00", 2, "10 Keith St", "Glasgow", "G11 5DD", 0, 0, test_user)
        create_game(2, 9, "2018-02-10 18:00", "2018-02-10 19:00", 1, "Greendyke St", "Glasgow", "G1 5DB", 2, 1, test_user)
        create_game(3, 9, "2018-02-15 10:00", "2018-02-15 11:00", 1, "33 Scotland St", "Glasgow", "G5 8NB", 10, 1, test_user)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 2)

        num_games =len(response.context['games'])
        self.assertEqual(num_games , 4)
