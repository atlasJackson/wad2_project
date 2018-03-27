import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
    'wad2_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from fives.models import Player, Game, Participation
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import uuid

def populate():

    # List of users - also contains details for corresponding player entry.
    users = {"realMarioMario":
                {"password": "password",
                "email": "mario@mariobros.mk",
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
                "email": "luigi@mariobros.mk",
                "first_name": "Luigi",
                "last_name": "Mario",
                "gender": 1,
                "host_rating": 1,
                "num_host_ratings": 1,
                "punctuality": 18,
                "likeability": 19,
                "skill": 10,
                "num_player_ratings": 5},

            "kakarot":
                {"password": "password",
                "email": "",
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
                "email": "andrew.ryan@ryanindusties.rap",
                "first_name": "Andrew",
                "last_name": "Ryan",
                "gender": 1,
                "host_rating": 1,
                "num_host_ratings": 3,
                "punctuality": 4,
                "likeability": 1,
                "skill": 4,
                "num_player_ratings": 1},

            "kevin-garvey":
                {"password": "password",
                "email": "kgarvey71@jpd.com",
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
                "email": "user1@testemail.com",
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
                "email": "",
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
                "email": "",
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
                "email": "buffy4angel@gmail.com",
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
                "email": "",
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

    games = {"realMarioMario-20180310-1700":
                {"game_type": 1,
                "free_slots": 0,
                "start": "2018-03-10 17:00",
                "end": "2018-03-10 19:00",
                "duration": 2,
                "street": "137 Shawbridge Street",
                "city": "Glasgow",
                "postcode": "G43 1QQ",
                "price": 5,
                "booked": 1,
                "host": "realMarioMario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],},

            "realMarioMario-20180317-1700":
                {"game_type": 5,
                "free_slots": 0,
                "start": "2018-03-17 17:00",
                "end": "2018-03-17 19:00",
                "duration": 2,
                "street": "137 Shawbridge Street",
                "city": "Glasgow",
                "postcode": "G43 1QQ",
                "price": 5,
                "booked": 1,
                "host": "realMarioMario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",0),
                        ("testuser",0),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],},

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
                "host": "realMarioMario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",0),
                        ("testuser",0),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],},

            "realMarioMario-20180326-1800":
                {"game_type": 4,
                "free_slots": 7,
                "start": "2018-03-26 18:00",
                "end": "2018-03-26 19:00",
                "duration": 1,
                "street": "1 Kennedy Street",
                "city": "Glasgow",
                "postcode": "G4 0EB",
                "price": 4,
                "booked": 1,
                "host": "realMarioMario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0)],},

            "realMarioMario-20180331-1700":
                {"game_type": 5,
                "free_slots": 5,
                "start": "2018-03-31 17:00",
                "end": "2018-03-31 19:00",
                "duration": 2,
                "street": "137 Shawbridge Street",
                "city": "Glasgow",
                "postcode": "G43 1QQ",
                "price": 3,
                "booked": 1,
                "host": "realMarioMario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kakarot",0),
                        ("wonderWoman",0),
                        ("DragonQueen",0)],},

            "ryanIndustries1946-20180312-1700":
                {"game_type": 4,
                "free_slots": 0,
                "start": "2018-03-12 17:00",
                "end": "2018-03-12 19:00",
                "duration": 2,
                "street": "137 Shawbridge Street",
                "city": "Glasgow",
                "postcode": "G43 1QQ",
                "price": 6,
                "booked": 1,
                "host": "ryanIndustries1946",
                "participants":
                        [("realMarioMario",1),
                        ("luigi-best-mario",1),
                        ("kevin-garvey",1),
                        ("ryanIndustries1946",1),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",1),
                        ("DragonQueen",0)],},

            "ryanIndustries1946-20180325-1200":
                {"game_type": 1,
                "free_slots": 8,
                "start": "2018-03-25 12:00",
                "end": "2018-03-25 14:00",
                "duration": 2,
                "street": "Victoria Park",
                "city": "Glasgow",
                "postcode": "G14 9NN",
                "price": 0,
                "booked": 0,
                "host": "ryanIndustries1946",
                "participants":
                        [("ryanIndustries1946",0),
                        ("realMarioMario",0)],},

            "luigi-best-mario-20180311-1100":
                {"game_type": 5,
                "free_slots": 0,
                "start": "2018-03-11 11:00",
                "end": "2018-03-11 13:00",
                "duration": 2,
                "street": "137 Shawbridge Street",
                "city": "Glasgow",
                "postcode": "G43 1QQ",
                "price": 5,
                "booked": 0,
                "host": "luigi-best-mario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],},

            "luigi-best-mario-20180314-1700":
                {"game_type": 5,
                "free_slots": 0,
                "start": "2018-03-14 17:00",
                "end": "2018-03-14 18:00",
                "duration": 1,
                "street": "137 Shawbridge Street",
                "city": "Glasgow",
                "postcode": "G43 1QQ",
                "price": 5,
                "booked": 1,
                "host": "luigi-best-mario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],},

            "luigi-best-mario-20180302-1500":
                {"game_type": 4,
                "free_slots": 0,
                "start": "2018-03-02 15:00",
                "end": "2018-03-02 17:00",
                "duration": 2,
                "street": "1 Kennedy Street",
                "city": "Glasgow",
                "postcode": "G4 0EB",
                "price": 5,
                "booked": 1,
                "host": "luigi-best-mario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",1),
                        ("ryanIndustries1946",0),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],},

            "luigi-best-mario-20180210-1700":
                {"game_type": 4,
                "free_slots": 0,
                "start": "2018-02-10 17:00",
                "end": "2018-02-10 19:00",
                "duration": 2,
                "street": "1 Kennedy Street",
                "city": "Glasgow",
                "postcode": "G4 0EB",
                "price": 5,
                "booked": 1,
                "host": "luigi-best-mario",
                "participants":
                        [("realMarioMario",1),
                        ("luigi-best-mario",1),
                        ("kevin-garvey",1),
                        ("ryanIndustries1946",1),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",1),
                        ("Greatest-Earthbender-in-the-World",1),
                        ("BtVS",1),
                        ("DragonQueen",1)],},

            "luigi-best-mario-20180410-1700":
                {"game_type": 1,
                "free_slots": 5,
                "start": "2018-04-10 17:00",
                "end": "2018-04-10 19:00",
                "duration": 2,
                "street": "1 Kennedy Street",
                "city": "Glasgow",
                "postcode": "G4 0EB",
                "price": 5,
                "booked": 1,
                "host": "luigi-best-mario",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",0),],},

            "wonderWoman-20180401-1700":
                {"game_type": 2,
                "free_slots": 5,
                "start": "2018-04-01 17:00",
                "end": "2018-04-01 19:00",
                "duration": 2,
                "street": "Motherwell Street",
                "city": "Airdrie",
                "postcode": "ML6 7HU",
                "price": 3,
                "booked": 1,
                "host": "wonderWoman",
                "participants":
                        [("testuser",0),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],},

            "wonderWoman-20180402-1700":
                {"game_type": 2,
                "free_slots": 7,
                "start": "2018-04-02 17:00",
                "end": "2018-04-02 19:00",
                "duration": 2,
                "street": "Motherwell Street",
                "city": "Airdrie",
                "postcode": "ML6 7HU",
                "price": 3,
                "booked": 1,
                "host": "wonderWoman",
                "participants":
                        [("testuser",0),
                        ("wonderWoman",0),
                        ("DragonQueen",0)],},

            "wonderWoman-20180403-1700":
                {"game_type": 2,
                "free_slots": 5,
                "start": "2018-04-03 17:00",
                "end": "2018-04-03 19:00",
                "duration": 2,
                "street": "Motherwell Street",
                "city": "Airdrie",
                "postcode": "ML6 7HU",
                "price": 3,
                "booked": 1,
                "host": "wonderWoman",
                "participants":
                        [("testuser",0),
                        ("wonderWoman",0),
                        ("Greatest-Earthbender-in-the-World",0),
                        ("BtVS",0),
                        ("DragonQueen",0)],},

            "kevin-garvey-20180403-2000":
                {"game_type": 0,
                "free_slots": 5,
                "start": "2018-04-03 20:00",
                "end": "2018-04-03 21:00",
                "duration": 1,
                "street": "66 Bankhead Dr",
                "city": "Edinburgh ",
                "postcode": "EH11 4EQ",
                "price": 5,
                "booked": 1,
                "host": "kevin-garvey",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",0),],},

            "kevin-garvey-20180404-2000":
                {"game_type": 0,
                "free_slots": 5,
                "start": "2018-04-04 20:00",
                "end": "2018-04-04 21:00",
                "duration": 1,
                "street": "66 Bankhead Dr",
                "city": "Edinburgh ",
                "postcode": "EH11 4EQ",
                "price": 5,
                "booked": 1,
                "host": "kevin-garvey",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("ryanIndustries1946",0),
                        ("kakarot",0),],},

            "kevin-garvey-20180405-2000":
                {"game_type": 0,
                "free_slots": 4,
                "start": "2018-04-05 20:00",
                "end": "2018-04-05 21:00",
                "duration": 1,
                "street": "66 Bankhead Dr",
                "city": "Edinburgh ",
                "postcode": "EH11 4EQ",
                "price": 5,
                "booked": 1,
                "host": "kevin-garvey",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",0),
                        ("kevin-garvey",0),
                        ("kakarot",0),],},


            "kakarot-20180201-1700":
                {"game_type": 4,
                "free_slots": 0,
                "start": "2018-02-01 17:00",
                "end": "2018-02-01 19:00",
                "duration": 2,
                "street": "1 Kennedy Street",
                "city": "Glasgow",
                "postcode": "G4 0EB",
                "price": 5,
                "booked": 1,
                "host": "kakarot",
                "participants":
                        [("realMarioMario",1),
                        ("luigi-best-mario",1),
                        ("kevin-garvey",1),
                        ("ryanIndustries1946",1),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",1),
                        ("Greatest-Earthbender-in-the-World",1),
                        ("BtVS",1),
                        ("DragonQueen",1)],},

            "kakarot-20180202-1700":
                {"game_type": 4,
                "free_slots": 0,
                "start": "2018-02-02 17:00",
                "end": "2018-02-02 19:00",
                "duration": 2,
                "street": "1 Kennedy Street",
                "city": "Glasgow",
                "postcode": "G4 0EB",
                "price": 6,
                "booked": 1,
                "host": "kakarot",
                "participants":
                        [("realMarioMario",1),
                        ("luigi-best-mario",1),
                        ("kevin-garvey",1),
                        ("ryanIndustries1946",1),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",1),
                        ("Greatest-Earthbender-in-the-World",1),
                        ("BtVS",1),
                        ("DragonQueen",1)],},

            "kakarot-20180203-1700":
                {"game_type": 4,
                "free_slots": 0,
                "start": "2018-02-03 17:00",
                "end": "2018-02-03 19:00",
                "duration": 2,
                "street": "1 Kennedy Street",
                "city": "Glasgow",
                "postcode": "G4 0EB",
                "price": 3,
                "booked": 1,
                "host": "kakarot",
                "participants":
                        [("realMarioMario",0),
                        ("luigi-best-mario",1),
                        ("kevin-garvey",1),
                        ("ryanIndustries1946",1),
                        ("kakarot",1),
                        ("testuser",1),
                        ("wonderWoman",1),
                        ("Greatest-Earthbender-in-the-World",1),
                        ("BtVS",1),
                        ("DragonQueen",1)],},

            "kakarot-20180204-1700":
                {"game_type": 1,
                "free_slots": 0,
                "start": "2018-02-04 17:00",
                "end": "2018-02-04 19:00",
                "duration": 2,
                "street": "66 Bankhead Dr",
                "city": "Edinburgh",
                "postcode": "EH11 4EQ",
                "price": 8,
                "booked": 1,
                "host": "kakarot",
                "participants":
                        [("realMarioMario",1),
                        ("luigi-best-mario",1),
                        ("kevin-garvey",1),
                        ("ryanIndustries1946",1),
                        ("kakarot",1)],},

            "ryanIndustries1946-20180226-1400":
                {"game_type": 0,
                "free_slots": 6,
                "start": "2018-02-26 14:00",
                "end": "2018-02-26 15:00",
                "duration": 1,
                "street": "66 Bankhead Dr",
                "city": "Edinburgh",
                "postcode": "EH11 4EQ",
                "price": 6.5,
                "booked": 1,
                "host": "ryanIndustries1946",
                "participants":
                        [("realMarioMario",1),
                        ("luigi-best-mario",1),
                        ("ryanIndustries1946",1),
                        ("kakarot",1)],},

            "ryanIndustries1946-20180228-1400":
                {"game_type": 0,
                "free_slots": 6,
                "start": "2018-02-28 14:00",
                "end": "2018-02-28 15:00",
                "duration": 1,
                "street": "66 Bankhead Dr",
                "city": "Edinburgh",
                "postcode": "EH11 4EQ",
                "price": 2,
                "booked": 1,
                "host": "ryanIndustries1946",
                "participants":
                        [("realMarioMario",1),
                        ("luigi-best-mario",1),
                        ("ryanIndustries1946",1),
                        ("kakarot",1)],},

            }


    for user, user_data in users.items():
        u = add_user(user, user_data["password"], user_data["email"], user_data["first_name"], user_data["last_name"])
        p = add_player(user, user_data["gender"], user_data["host_rating"], user_data["num_host_ratings"],
            user_data["punctuality"], user_data["likeability"], user_data["skill"], user_data["num_player_ratings"])

    for game, game_data in games.items():
        g = add_game(game,game_data["game_type"], game_data["free_slots"], game_data["start"],
            game_data["end"], game_data["duration"], game_data["street"], game_data["city"], game_data["postcode"],
            game_data["price"], game_data["booked"], game_data["host"])

        for player in game_data["participants"]:
            p = add_participant(game,player[0],player[1])



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


def add_user(username, password, email, first_name, last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.email = email
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

    # The following page helped solve the issue of a runtime warning appearing for using a naive datetime.
    # https://stackoverflow.com/questions/7065164/how-to-make-an-unaware-datetime-timezone-aware-in-python
    start = datetime.strptime(start, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.UTC)
    end = datetime.strptime(end, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.UTC)

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
