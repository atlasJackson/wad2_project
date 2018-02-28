from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from decimal import *
import datetime

class UserProfile(models.Model):
    # This line is required. Link UserProfile to a User model instance.
    user = models.OneToOneField(User)

    #The additional attributes we wish to include.
    #picture = models.ImageField(upload_to='profile_images', blank=True)

    #Override the __str__() method.
    def __str__(self):
        return self.user.username

class Player(models.Model):
    # Firstname, surname, email, password acquired from user model.
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

    game_id = models.IntegerField(default=0, unique=True)
    # Game type takes the following values:
    # 0 - Men's Competitive
    # 1 - Men's Friendly
    # 2 - Women's Competitive
    # 3 - Women's Friendly
    # 4 - Mixed Competitive
    # 5 - Mixed Friendly
    game_type = models.IntegerField(default=0)

    date = models.DateField(default=datetime.date.today)
    #start_time = 
    #end_time = 
    duration = models.BooleanField(default=True)
    
    street = models.CharField(max_length=128)
    place = models.CharField(max_length=128)
    postcode =models.CharField(max_length=128)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    booked = models.BooleanField(default=True)
    host =  models.ForeignKey(Player)

    #Override the __str__() method.
    def __str__(self):
        return self.game_id



