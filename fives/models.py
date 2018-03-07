from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from decimal import *
import datetime
import uuid

class UserProfile(models.Model):
    # This line is required. Link UserProfile to a User model instance.
    user = models.OneToOneField(User)

    #The additional attributes we wish to include.
    #picture = models.ImageField(upload_to='profile_images', blank=True)

    #Override the __str__() method.
    def __str__(self):
        return self.user.username

class Player(models.Model):
    # Firstname, surname, email, password acquired from user model?
    #firstname =
    #surname =
    #email =
    #password =
    user = models.OneToOneField(UserProfile)
    #user_id = models.IntegerField(default=0, unique=True)

    # gender - T/F: M/F
    gender = models.BooleanField(default=True)

    host_rating = models.IntegerField(default=0)
    num_host_ratings = models.IntegerField(default=0)

    reliability = models.IntegerField(default=0)
    likeability = models.IntegerField(default=0)
    skill = models.IntegerField(default=0)
    num_player_ratings = models.IntegerField(default=0)

#FIX - Override the __str__() method.
    def __str__(self):
        return self.user_id


class Game(models.Model):
    # UUIDField creates unique id for each game
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)

    # Game types take the following values in order to reference integer field:
    MENS_CP = 0
    MENS_FR = 1
    WOMENS_CP = 2
    WOMENS_FR = 3
    MIXED_CP = 4
    MIXED_FR = 5

    GAME_CHOICES = (
        (MENS_CP, "Men's Competitive"),
        (MENS_FR, "Men's Friendly"),
        (WOMENS_CP, "Women's Competitive"),
        (WOMENS_FR, "Women's Friendly"),
        (MIXED_CP, "Mixed Competitive"),
        (MIXED_FR, "Mixed Friendly"),
    )

    game_type = models.IntegerField(choices=GAME_CHOICES, default=MENS_CP)

    # Date and time entries
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.BooleanField(default=True)

    # Address entries
    street = models.CharField(max_length=128)
    place = models.CharField(max_length=128)
    postcode = models.CharField(max_length=128)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Booked is true if the pitch has been booked and false if it has not.
    booked = models.BooleanField(default=False)
    # Host uses foreign key from Player class
    host = models.ForeignKey(Player)

    #Override the __str__() method.
    def __str__(self):
        return self.game_id
