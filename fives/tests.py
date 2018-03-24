from django.contrib.auth.models import User
from fives.models import Player, Game, Participation
from django.test import TestCase
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import uuid

##############################################################################################################
### UNIT TESTS FOR MODELS
##############################################################################################################

### Player Model Tests
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

### Game Model Tests
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

### Participation Model Tests
class ParticipationMethodTests(TestCase):
    # Test that the string representation of the participation object returns the concatenation of the player, game and rating.
    def test_participation_string_representation(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        test_game = create_game(0, 9, "2018-04-28 14:00", "2018-04-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        test_participation = create_participation(test_game, test_player, 0)
        self.assertEqual(str(test_participation), str(test_participation.player) + " " + str(test_participation.game) + " " + str(test_participation.rated))

# Helper method to create a participation object.
def create_participation(game, player, rated):
    p = Participation(game=game, player=player, rated=rated)
    p.save()
    return p

##############################################################################################################
### UNIT TESTS FOR VIEWS
##############################################################################################################

### Index View Tests
class IndexViewTests(TestCase):
    ## The first two tests are based on the tests in the book Tango With Django; Chapter 18: Automated Testing.

    # If there are no games, the index displays an appropriate message.
    def test_index_view_with_no_games(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no scheduled matches.")
        self.assertQuerysetEqual(response.context['games'], [])

    # If the only games in the database are in the past, then no games should be passed to the index.
    def test_index_view_with_games_in_past(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        create_game(0, 9, "2018-02-28 14:00", "2018-02-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        create_game(1, 9, "2018-02-22 11:00", "2018-02-22 13:00", 2, "10 Keith St", "Glasgow", "G11 5DD", 0, 0, test_user)
        create_game(2, 9, "2018-02-10 18:00", "2018-02-10 19:00", 1, "Greendyke St", "Glasgow", "G1 5DB", 2, 1, test_user)
        create_game(3, 9, "2018-02-15 10:00", "2018-02-15 11:00", 1, "33 Scotland St", "Glasgow", "G5 8NB", 10, 1, test_user)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no scheduled matches.")

        # The games are in the past, so should not be passed through to the index when the games are filtered in the view.
        num_games = len(response.context['games'])
        self.assertEqual(num_games , 0)

    # Test the view when future games are passed to the index template.
    def test_index_view_with_games_in_future(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        create_game(0, 9, "2018-04-28 14:00", "2018-04-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        create_game(1, 9, "2018-04-22 11:00", "2018-04-22 13:00", 2, "10 Keith St", "Glasgow", "G11 5DD", 0, 0, test_user)
        create_game(2, 9, "2018-04-10 18:00", "2018-04-10 19:00", 1, "Greendyke St", "Glasgow", "G1 5DB", 2, 1, test_user)
        create_game(3, 9, "2018-04-15 10:00", "2018-04-15 11:00", 1, "33 Scotland St", "Glasgow", "G5 8NB", 10, 1, test_user)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 2)

        # Now the number of games in the context dictionary should be 4.
        num_games = len(response.context['games'])
        self.assertEqual(num_games , 4)

### About Us View Tests
class AboutUsViewTests(TestCase):

    # The about us view should not have any errors. The main check is that the coorindates passed in the context dictionary
    # will generate the correct location on the map display.
    def test_about_us_view(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "We can also be contacted through the School of Computing Science.")

        # Test the correct coordinates are passed to the view (uses geolocator to get coordinates based on the address).
        geolocator = Nominatim()
        location = geolocator.geocode("Sir Alwyn Williams Building, Glasgow")
        self.assertEqual(response.context['latitude'], location.latitude)
        self.assertEqual(response.context['longitude'], location.longitude)

### Game List View Tests
class GameListTests(TestCase):

    # Test the view when there are no games in game_list template.
    def test_game_list_view_with_no_games(self):
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no scheduled games.")
        self.assertQuerysetEqual(response.context['games'], [])

    # Test the view when games are passed to the game_list template.
    def test_index_view_with_games_in_future(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        create_game(0, 9, "2018-04-28 14:00", "2018-04-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        create_game(1, 9, "2018-04-22 11:00", "2018-04-22 13:00", 2, "10 Keith St", "Glasgow", "G11 5DD", 0, 0, test_user)
        create_game(2, 9, "2018-04-10 18:00", "2018-04-10 19:00", 1, "Greendyke St", "Glasgow", "G1 5DB", 2, 1, test_user)
        create_game(3, 9, "2018-04-15 10:00", "2018-04-15 11:00", 1, "33 Scotland St", "Glasgow", "G5 8NB", 10, 1, test_user)

        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 2)

        # Now the number of games in the context dictionary should be 4.
        num_games = len(response.context['games'])
        self.assertEqual(num_games , 4)

### Create Game View Tests
class CreateGameTests(TestCase):

    def test_create_game_without_login(self):
        response = self.client.get('/fives/create_game/', follow=True)
        self.assertContains(response, "Please sign in", status_code=200)

    def test_create_game_view_with_login(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.client.login(username='test-user-1', password='fivesPass123')
        response = self.client.get('/fives/create_game/', follow=True)
        self.assertContains(response, "create your own game", status_code=200)

##### Need to be fixed
    def test_create_game_view_with_no_conflict(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.client.login(username='test-user-1', password='fivesPass123')
        response = self.client.get(reverse('create_game'), follow =True)
        create_game(0, 9, "2018-04-23 14:00", "2018-04-23 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/fives/game_list/')

    # Creating new game should be prevented if the user has another game during that time
    def test_create_game_view_with_conflict(self):
        test_user, test_player = generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        create_game(0, 9, "2018-04-28 16:00", "2018-04-28 18:00", 2, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        create_game(0, 9, "2018-04-28 17:00", "2018-04-28 18:00", 1, "10 Keith St", "Glasgow", "G11 6QQ", 0, 0, test_user)

        response = self.client.get(reverse('create_game'))
        self.assertContains(response, "You already have a game scheduled during this time", status_code=302)

        num_games = len(response.context['games'])
        self.assertEqual(num_games , 1)

    def test_create_game_within_two_hour(self):
