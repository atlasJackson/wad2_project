from django.test import TestCase
from fives.models import *
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
import fives.tests.test_helper_methods as th
from django.utils import timezone
import pytz

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

### Show Game View Tests
class ShowGameViewTests(TestCase):

    def test_show_game_with_existing_games(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        test_game = th.create_game(0, 9, "2018-04-28 14:00", "2018-04-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        test_participation = th.create_participation(test_game, test_player, 0)

        game_custom_slug = Game.objects.all()[0].custom_slug

        response = self.client.get('/fives/game_list/%s/' % game_custom_slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")

    def test_show_game_with_non_existing_games(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        test_game = th.create_game(0, 9, "2018-04-28 14:00", "2018-04-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        test_participation = th.create_participation(test_game, test_player, 0)

        game_custom_slug = 'hello-20180326-2211'
        response = self.client.get('/fives/game_list/%s/' % game_custom_slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The specified game does not exist!")

### Show Past Game View Tests
class ShowPastGameViewTests(TestCase):

    def test_show_past_game_from_participants(self):
        # Create 10 more users and players and login as test-user-1
        test_user1, test_player1 = th.generate_test_user("test-user-1", "fivesPass1", "testemail1@testmail.com", "Test1", "User1")
        test_user2, test_player2 = th.generate_test_user("test-user-2", "fivesPass2", "testemail2@testmail.com", "Test2", "User2")
        test_user3, test_player3 = th.generate_test_user("test-user-3", "fivesPass3", "testemail3@testmail.com", "Test3", "User3")
        test_user4, test_player4 = th.generate_test_user("test-user-4", "fivesPass4", "testemail4@testmail.com", "Test4", "User4")
        test_user5, test_player5 = th.generate_test_user("test-user-5", "fivesPass5", "testemail5@testmail.com", "Test5", "User5")
        test_user6, test_player6 = th.generate_test_user("test-user-6", "fivesPass6", "testemail6@testmail.com", "Test6", "User6")
        test_user7, test_player7 = th.generate_test_user("test-user-7", "fivesPass7", "testemail7@testmail.com", "Test7", "User7")
        test_user8, test_player8 = th.generate_test_user("test-user-8", "fivesPass8", "testemail8@testmail.com", "Test8", "User8")
        test_user9, test_player9 = th.generate_test_user("test-user-9", "fivesPass9", "testemail9@testmail.com", "Test9", "User9")
        test_user10, test_player10 = th.generate_test_user("test-user-10", "fivesPass10", "testemail10@testmail.com", "Test10", "User10")
        self.client.login(username='test-user-1', password='fivesPass1')

        # Let user1 create the past game and let user 2...10 join the game
        test_game = th.create_game(0, 9, "2018-02-28 14:00", "2018-02-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user1)
        th.create_participation(test_game, test_player1, 0)
        th.create_participation(test_game, test_player2, 0)
        th.create_participation(test_game, test_player3, 0)
        th.create_participation(test_game, test_player4, 0)
        th.create_participation(test_game, test_player5, 0)
        th.create_participation(test_game, test_player6, 0)
        th.create_participation(test_game, test_player7, 0)
        th.create_participation(test_game, test_player8, 0)
        th.create_participation(test_game, test_player9, 0)
        th.create_participation(test_game, test_player10, 0)

        game_custom_slug = Game.objects.all()[0].custom_slug
        player = Player.objects.all()[0].user.username
        response = self.client.get('/fives/user/%s/%s/' % (player,game_custom_slug))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "rating")


### Edit booking View Tests
class EditBookingViewTests(TestCase):

    def test_edit_booking(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass1", "testemail1@testmail.com", "Test", "User")
        self.client.login(username='test-user-1', password='fivesPass1')

        # Create a game with booking status 'booked'
        th.create_game(0, 9, "2018-04-28 14:00", "2018-04-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        game = Game.objects.filter(game_type=0)[0]
        th.create_participation(game, test_player, 0)

        game_custom_slug = Game.objects.all()[0].custom_slug
        self.client.get('/fives/game_list/%s/' % game_custom_slug)

        # Change booking status to 'Not Booked'
        game.booked = not game.booked
        game.save()
        response = self.client.post('/fives/game_list/%s/' % game_custom_slug, {'bookingChanged': True} )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not Booked")

### Join Game View Tests
class JoinGameViewTests(TestCase):

    def test_join_game(self):
        # Create a user1, user2 and player1, player2 and login with user2 account
        test_user1, test_player1 = th.generate_test_user("test-user-1", "fivesPass1", "testemail1@testmail.com", "Test1", "User1")
        test_user2, test_player2 = th.generate_test_user("test-user-2", "fivesPass2", "testemail2@testmail.com", "Test2", "User2")
        self.client.login(username='test-user-2', password='fivesPass2')

        # Create a game and make user1 as a host for the test game and user2 as a participant
        th.create_game(0, 9, "2018-04-22 14:00", "2018-04-22 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user1)
        game = Game.objects.filter(game_type=0)[0]
        th.create_participation(game, test_player1, 0)

        game_custom_slug = Game.objects.all()[0].custom_slug
        self.client.get('/fives/game_list/%s/' % game_custom_slug)

        # Joining the game and decrease the free_slots by one
        th.create_participation(game, test_player2, 0)
        game.free_slots -= 1
        game.save()

        game_conflict = True
        player_added = False

        response = self.client.post('/fives/game_list/%s/' % game_custom_slug, {'player_added': True, 'game_conflict': False} )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leave Game")

### Leave Game View Tests
class LeaveGameViewTests(TestCase):

    def test_leave_game(self):
        # Create a user1, user2 and player1, player2 and login with user2 account
        test_user1, test_player1 = th.generate_test_user("test-user-1", "fivesPass1", "testemail1@testmail.com", "Test1", "User1")
        test_user2, test_player2 = th.generate_test_user("test-user-2", "fivesPass2", "testemail2@testmail.com", "Test2", "User2")
        self.client.login(username='test-user-2', password='fivesPass2')

        # Create a game and make user1 as a host for the test game and user2 as a participant
        th.create_game(0, 9, "2018-04-22 14:00", "2018-04-22 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user1)
        game = Game.objects.filter(game_type=0)[0]
        th.create_participation(game, test_player1, 0)

        user = User.objects.get(username=test_user2)
        player=Player.objects.get(user=user)

        game_custom_slug = Game.objects.all()[0].custom_slug
        self.client.get('/fives/game_list/%s/' % game_custom_slug)

        # Joining the game and decrease the free_slots by one
        th.create_participation(game, test_player2, 0)
        game.free_slots -= 1
        game.save()

        # Leaving the game by Deleting the participation from the Data, increase the free_slots by one
        p = Participation.objects.get(player=player, game=game)
        p.delete()
        game.free_slots += 1
        game.save()

        response = self.client.post('/fives/game_list/%s/' % game_custom_slug, {'player_removed': True} )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Join Game")

### Leave Game View Tests
class DeleteGameViewTests(TestCase):

    def test_delete_game(self):
        # Create a user1, user2 and player1, player2 and login with user1 account
        test_user1, test_player1 = th.generate_test_user("test-user-1", "fivesPass1", "testemail1@testmail.com", "Test1", "User1")
        test_user2, test_player2 = th.generate_test_user("test-user-2", "fivesPass2", "testemail2@testmail.com", "Test2", "User2")
        self.client.login(username='test-user-2', password='fivesPass2')

        # Create a game and make user1 as a host for the test game and user2 as a participant
        th.create_game(0, 9, "2018-04-22 14:00", "2018-04-22 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user1)
        game = Game.objects.filter(game_type=0)[0]
        th.create_participation(game, test_player1, 0)

        user = User.objects.get(username=test_user2)
        player=Player.objects.get(user=user)

        game_custom_slug = Game.objects.all()[0].custom_slug
        self.client.get('/fives/game_list/%s/' % game_custom_slug)

        game.delete()

        response = self.client.post('/fives/game_list/%s/' % game_custom_slug, {'game_deleted': True} )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no scheduled games.")
        self.assertQuerysetEqual(response.context['games'], [])

###############################################
# User-centric Views Tests
###############################################
