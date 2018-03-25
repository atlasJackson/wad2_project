from django.test import TestCase
import fives.tests.test_helper_methods as th

### Player Model Tests
class PlayerMethodTests(TestCase):
    # Test that the string representation of the player returns their username.
    def test_player_string_representation(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        self.assertEqual(str(test_player), test_user.username)

### Game Model Tests
class GameMethodTests(TestCase):
    # Test that the string representation of the game returns the concatenation of the host, start date and game id (auto-generated).
    def test_game_string_representation(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        test_game = th.create_game(0, 9, "2018-02-28 14:00", "2018-02-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        self.assertEqual(str(test_game), str(test_game.host) + " " + str(test_game.start) + " " + str(test_game.game_id)[:6])

### Participation Model Tests
class ParticipationMethodTests(TestCase):
    # Test that the string representation of the participation object returns the concatenation of the player, game and rating.
    def test_participation_string_representation(self):
        test_user, test_player = th.generate_test_user("test-user-1", "fivesPass123", "testemail@testmail.com", "Test", "User")
        test_game = th.create_game(0, 9, "2018-04-28 14:00", "2018-04-28 15:00", 1, "66 Bankhead Dr", "Edinburgh", "EH11 4EQ", 5, 1, test_user)
        test_participation = th.create_participation(test_game, test_player, 0)
        self.assertEqual(str(test_participation), str(test_participation.player) + " " + str(test_participation.game) + " " + str(test_participation.rated))
