from django.test import TestCase
from fives.models import Game
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
import fives.tests.test_helper_methods as th

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
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        th.generate_past_test_games(test_user)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no scheduled matches.")

        # The games are in the past, so should not be passed through to the index when the games are filtered in the view.
        num_games = len(response.context['games'])
        self.assertEqual(num_games , 0)

    # Test the view when future games are passed to the index template.
    def test_index_view_with_games_in_future(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        th.generate_future_test_games(test_user)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 2)

        # Now the number of games in the context dictionary should be 4.
        num_games = len(response.context['games'])
        self.assertEqual(num_games , 4)

    # Test the view when past and future games are passed to the index template.
    def test_index_view_with_games_in_past_and_future(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        th.generate_past_and_future_test_games(test_user)

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
class GameListViewTests(TestCase):

    # Test the view when there are no games in game_list template.
    def test_game_list_view_with_no_games(self):
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no scheduled games.")
        self.assertQuerysetEqual(response.context['games'], [])

    # Test the view when games are passed to the game_list template.
    def test_index_view_with_games_in_future(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        th.generate_future_test_games(test_user)

        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 2)

        # Now the number of games in the context dictionary should be 4.
        num_games = len(response.context['games'])
        self.assertEqual(num_games , 4)

### Create Game View Tests
class CreateGameViewTests(TestCase):

    def test_create_game_without_login(self):
        response = self.client.get('/fives/create_game/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please sign in")

    def test_create_game_view_with_login(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.client.login(username='test-user-1', password='fivesPass123')
        response = self.client.get('/fives/create_game/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "create your own game")

    def test_create_game_view_with_no_conflict(self):
        # Add user and login, redirect to create game.
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.client.login(username='test-user-1', password='fivesPass123')
        self.client.get(reverse('create_game'), follow =True)
        
        # https://stackoverflow.com/questions/46001747/django-test-client-post-data
        start_date, start_time = th.start_date_and_time_generator(10)
        response = self.client.post(reverse('create_game'), {'game_type': 0, 'date': start_date, 'time': start_time, 'duration': 1, 
                                                  'street': "66 Bankhead Dr", 'city': "Edinburgh", 'postcode': "EH11 4EQ", 'price': 5, 'booked': 1} )

        self.assertEqual(response.status_code, 302)

        game_custom_slug = Game.objects.all()[0].custom_slug
        self.assertRedirects(response, ('/fives/game_list/%s/' % game_custom_slug))

    # Creating new game should be prevented if the user has another game during that time
    def test_create_game_view_with_conflict(self):
        # Add user and login, add game and particpation to database, and redirect to create game.
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.client.login(username='test-user-1', password='fivesPass123')

        start_datetime, end_datetime = th.start_and_end_datetime_generator(10,2)
        th.create_game(0, 9, start_datetime, end_datetime, 2, "10 Keith St", "Glasgow", "G11 6QQ", 0, 0, test_user)
        game = Game.objects.filter(game_type=0)[0]
        th.create_participation(game, test_player, 0)
        
        self.client.get(reverse('create_game'))

        # Try creating a game with a time conflict.
        start_date, start_time = th.start_date_and_time_generator(10)
        response = self.client.post(reverse('create_game'), {'game_type': 0, 'date': start_date, 'time': start_time, 'duration': 1, 
                                                  'street': "66 Bankhead Dr", 'city': "Edinburgh", 'postcode': "EH11 4EQ", 'price': 5, 'booked': 1} )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You already have a game scheduled during this time")

        # Game should not have been added to the database.
        response = self.client.get(reverse('index'))
        num_games = len(response.context['games'])
        self.assertEqual(num_games , 1)


    # Creating new game should be prevented if the start time is within two hours.
    def test_create_game_within_two_hour(self):
        # Add user and login, and redirect to create game.
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.client.login(username='test-user-1', password='fivesPass123')        
        self.client.get(reverse('create_game'))

        # Try creating a game within two hours.
        start_date, start_time = th.start_date_and_time_generator(1)
        response = self.client.post(reverse('create_game'), {'game_type': 0, 'date': start_date, 'time': start_time, 'duration': 1, 
                                                  'street': "66 Bankhead Dr", 'city': "Edinburgh", 'postcode': "EH11 4EQ", 'price': 5, 'booked': 1} )

        # Post unsuccessful, check conflilct message matches content.
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['conflictMessage'], "You can't create a game in the past or within two hours from now.")

        ## Game should not have been added to the database.
        response = self.client.get(reverse('index'))
        num_games = len(response.context['games'])
        self.assertEqual(num_games , 0)


