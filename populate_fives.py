import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
    'wad2_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from fives.models import Player, Game, Participation
from geopy.geocoders import Nominatim
from datetime import datetime
import uuid

def populate():

    # List of users - also contains details for corresponding player entry.
    users = {"realMarioMario":
                {"password": "password",
                "first_name": "Mario",
                "last_name": "Mario",
                "gender": 1,
                "host_rating": 8,
                "num_host_ratings": 2,
                "punctuality": 16,
                "likeability": 20,
                "skill": 10,
                "num_player_ratings": 4},

            "luigi-best-mario":
                {"password": "password",
                "first_name": "Luigi",
                "last_name": "Mario",
                "gender": 1,
                "host_rating": 0,
                "num_host_ratings": 1,
                "punctuality": 18,
                "likeability": 19,
                "skill": 10,
                "num_player_ratings": 5},

            "kakarot":
                {"password": "password",
                "first_name": "Goku",
                "last_name": "Son",
                "gender": 1,
                "host_rating": 5,
                "num_host_ratings": 1,
                "punctuality": 15,
                "likeability": 15,
                "skill": 15,
                "num_player_ratings": 3},

            "ryanIndustries1946":
                {"password": "password",
                "first_name": "Andrew",
                "last_name": "Ryan",
                "gender": 1,
                "host_rating": 0,
                "num_host_ratings": 0,
                "punctuality": 4,
                "likeability": 1,
                "skill": 4,
                "num_player_ratings": 1},

            "kevin-garvey":
                {"password": "password",
                "first_name": "Kevin",
                "last_name": "Garvey",
                "gender": 1,
                "host_rating": 0,
                "num_host_ratings": 0,
                "punctuality": 6,
                "likeability": 8,
                "skill": 12,
                "num_player_ratings": 3},

            "testuser":
                {"password": "password",
                "first_name": "Test",
                "last_name": "User",
                "gender": 0,
                "host_rating": 0,
                "num_host_ratings": 0,
                "punctuality": 0,
                "likeability": 0,
                "skill": 0,
                "num_player_ratings": 0},

            "wonderWoman":
                {"password": "password",
                "first_name": "Diana",
                "last_name": "Prince",
                "gender": 0,
                "host_rating": 5,
                "num_host_ratings": 1,
                "punctuality": 10,
                "likeability": 9,
                "skill": 9,
                "num_player_ratings": 2},

            "Greatest-Earthbender-in-the-World":
                {"password": "password",
                "first_name": "Toph",
                "last_name": "Beifong",
                "gender": 0,
                "host_rating": 0,
                "num_host_ratings": 0,
                "punctuality": 14,
                "likeability": 5,
                "skill": 12,
                "num_player_ratings": 3},

            "BtVS":
                {"password": "password",
                "first_name": "Buffy",
                "last_name": "Summers",
                "gender": 0,
                "host_rating": 5,
                "num_host_ratings": 2,
                "punctuality": 10,
                "likeability": 10,
                "skill": 13,
                "num_player_ratings": 3},

            "DragonQueen":
                {"password": "password",
                "first_name": "Daenerys",
                "last_name": "Targaryen",
                "gender": 0,
                "host_rating": 8,
                "num_host_ratings": 2,
                "punctuality": 8,
                "likeability": 7,
                "skill": 8,
                "num_player_ratings": 2},
            }

    games = {"realMarioMario-20180326-1800":
                {"game_type": 0,
                "free_slots": 7,
                "start": "2018-03-26 18:00",
                "end": "2018-03-26 19:00",
                "duration": 1,
                "street": "1 Kennedy Street",
                "city": "Glasgow",
                "postcode": "G4 0EB",
                "price": 4,
                "booked": 1,
                "host": "realMarioMario"},

            "realMarioMario-20180324-1700":
                {"game_type": 5,
                "free_slots": 0,
                "start": "2018-03-24 17:00",
                "end": "2018-03-24 19:00",
                "duration": 2,
                "street": "137 Shawbridge Street",
                "city": "Glasgow",
                "postcode": "G43 1QQ",
                "price": 5,
                "booked": 1,
                "host": "realMarioMario"},

            "ryanIndustries1946-20180325-1200":
                {"game_type": 1,
                "free_slots": 9,
                "start": "2018-03-25 12:00",
                "end": "2018-03-25 14:00",
                "duration": 2,
                "street": "Victoria Park",
                "city": "Glasgow",
                "postcode": "G14 9NN",
                "price": 0,
                "booked": 0,
                "host": "ryanIndustries1946"},
            }

    particpants = {"realMarioMario-20180326-1800":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0)],

                    "realMarioMario-20180324-1700":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],

                    "ryanIndustries1946-20180325-1200":
                        [("ryanIndustries1946",0)],
            }


    for user, user_data in users.items():
        u = add_user(user,user_data["password"], user_data["first_name"], user_data["last_name"])
        p = add_player(user, user_data["gender"], user_data["host_rating"], user_data["num_host_ratings"],
            user_data["punctuality"], user_data["likeability"], user_data["skill"], user_data["num_player_ratings"])

    for game, game_data in games.items():
        g = add_game(game,game_data["game_type"], game_data["free_slots"], game_data["start"],
            game_data["end"], game_data["duration"], game_data["street"], game_data["city"], game_data["postcode"],
            game_data["price"], game_data["booked"], game_data["host"])

    for p_game, p_players in particpants.items():
        for player in p_players:
            p = add_participant(p_game,player[0],player[1])



    # Print out the players we have added.
    for u in User.objects.all():
        print (str(u))

    for p in Player.objects.all():
        print (str(p))

    # Print out the games we have added.
    for g in Game.objects.all():
        print (str(g))

    # Print out the participants we have added.
    for p in Participation.objects.all():
        print (str(p))


def add_user(username, password, first_name, last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.first_name = first_name
    u.last_name = last_name
    u.save()
    return u

def add_player(user, gender, host_rating, num_host_ratings, punctuality, likeability, skill, num_player_ratings):

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

def add_game(custom_slug, game_type, free_slots, start, end, duration,
            street, city, postcode, price, booked, host):

    h = User.objects.get(username=host)

    #year, month, day = date.split("-")
    #date = datetime.date(int(year), int(month), int(day))
    
    #start_hour, start_min = start_time.split(":")
    #end_hour, end_min = end_time.split(":")
    #start_time = datetime.time(int(start_hour), int(start_min))
    #end = datetime.time(int(end_hour), int(end_min))

    start = datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = datetime.strptime(end, '%Y-%m-%d %H:%M')
    print "START IS:", start

    g = Game.objects.get_or_create(custom_slug=custom_slug, host=h,
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

def add_participant(game, player, rated):
    u = User.objects.get(username=player)
    pl = Player.objects.get(user=u)
    g = Game.objects.get(custom_slug=game)
    p = Participation(game=g, player=pl, rated=rated)
    p.save()
    return p

# Start execution here.
if __name__ == '__main__':
    print("Starting Fives population script...")
    populate()
