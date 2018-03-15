from django import forms
from django.contrib.auth.models import User
from fives.models import Player, Game
import datetime


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class PlayerForm(forms.ModelForm):

    gender = forms.ChoiceField(choices=Player.GENDER_CHOICES, label="Gender")

    class Meta:
        model=Player
        fields = ('gender',)


class GameForm(forms.ModelForm):

    game_type = forms.ChoiceField(choices=Game.GAME_CHOICES, initial=Game.MENS_CP, label="Game type")

    date = forms.DateField()
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    duration = forms.ChoiceField(choices=Game.DURATION_CHOICES, initial=Game.ONE_HOUR, label="Duration")

    street = forms.CharField(max_length=128, label="Street & number")
    city = forms.CharField(max_length=128, label="City/Town")
    postcode = forms.CharField(max_length=128, label="Postcode")

    price = forms.DecimalField(widget=forms.TextInput(), label="Price/person")
    booked = forms.BooleanField(widget=forms.CheckboxInput(), initial=False, required=False, label="Pitch booked?")

    field_order=['game_type','date','time','suration','street','city','postcode', 'price', 'booked']

    class Meta:
        model = Game
        exclude = ('game_id', 'free_slots', 'host', 'latitude', 'longitude', 'end', 'custom_slug', 'start')

class RatingForm(forms.ModelForm):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    RATINGS=(
        (ONE, "1"),
        (TWO, "2"),
        (THREE, "3"),
        (FOUR, "4"),
        (FIVE, "5"),
    )
    skill = forms.ChoiceField(choices=RATINGS, initial=THREE)
    likeability = forms.ChoiceField(choices=RATINGS, initial=THREE)
    punctuality = forms.ChoiceField(choices=RATINGS, initial=THREE)

    class Meta:
        model = Player
        fields = ('skill', 'likeability', 'punctuality')
