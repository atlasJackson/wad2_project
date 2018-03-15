from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from decimal import *
import datetime
import uuid

# One-to-one relationship with user model
class Player(models.Model):
    # Username, firstname, surname, email, password acquired from user model
    user = models.OneToOneField(User)

    # Gender uses boolean values for male/female
    MALE = True
    FEMALE = False

    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    RATINGS = (
        (ONE, "1"),
        (TWO, "2"),
        (THREE, "3"),
        (FOUR, "4"),
        (FIVE, "5"),
    )

    gender = models.BooleanField(choices=GENDER_CHOICES, default=MALE)

    host_rating = models.IntegerField(default=0)
    num_host_ratings = models.IntegerField(default=0)

    punctuality = models.IntegerField(default=0)
    likeability = models.IntegerField(default=0)
    skill = models.IntegerField(default=0)
    num_player_ratings = models.IntegerField(default=0)

    # Override the __str__() method.
    def __str__(self):
        return self.user.username

    def __unicode__(self): # For Python 2, use __unicode__too
        return self.user.username


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
    # Number of available slots in Game - default is 9 since host is automatically added.
    free_slots = models.IntegerField(default=9)

    # Date and time entries
    start = models.DateTimeField(default=None)
    end = models.DateTimeField(default=None)

    # Duration of 1 hour is false, 2 hours is true. Used to calculate endtime in form.
    ONE_HOUR = 1
    TWO_HOURS = 2

    DURATION_CHOICES = (
        (ONE_HOUR, "1 hour"),
        (TWO_HOURS, "2 hours"),
    )

    # Changed from boolean to integer to allow future expansion.
    duration = models.IntegerField(choices=DURATION_CHOICES, default=ONE_HOUR)

    # Address entries
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    postcode = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default = 0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default = 0)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Booked is true if the pitch has been booked and false if it has not.
    # Allows the option for people to organise a game at a public park (such as teens or children).
    booked = models.BooleanField(default=False)
    # Host uses foreign key from Player class
    host = models.ForeignKey(User)
    # A customized slug field: username-date-time
    custom_slug = models.CharField(max_length=128, unique=True)

    #Override the __str__() method.
    def __str__(self):
        return str(self.host) + " " + str(self.start) + " " + str(self.game_id)[:6]

    def clean(self):
        # Don't allow more than 10 participants in a game.
        if self.free_slots == 0:
            # Prevent player adding themselves to the game.
            print("No slots left")

    # This method is called each time a game is saved/created, and the custom_slug is automatically generated.
    def save(self, *args, **kwargs):
        #self.custom_slug = str(self.host.username) + "-" + self.date.strftime("%Y") + self.date.strftime("%m") + self.date.strftime("%d") + "-" + self.start_time.strftime("%H") + self.start_time.strftime("%M")
        self.custom_slug = str(self.host.username) + "-" + self.start.strftime('%Y%m%d-%H%M')
        super(Game, self).save(*args, **kwargs)


class Participation(models.Model):
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    rated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.player) + " " + str(self.game) + " " + str(self.rated)
