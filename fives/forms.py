from django import forms
from django.core.validators import RegexValidator, validate_email
from django.contrib.auth.models import User
from fives.models import Player, Game
import datetime


class UserForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    username = forms.CharField(max_length=128, validators=[alphanumeric], widget=forms.TextInput(attrs={'autofocus':'true'}))
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class PlayerForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Player.GENDER_CHOICES, label="Gender")

    class Meta:
        model=Player
        fields = ('gender',)

class GameForm(forms.ModelForm):

    game_type = forms.ChoiceField(choices=Game.GAME_CHOICES, initial=Game.MENS_CP, label="Game type")

    date = forms.DateField(widget=forms.TextInput(attrs={'type':'text'}))
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Time (hh:mm)")
    duration = forms.ChoiceField(choices=Game.DURATION_CHOICES, initial=Game.ONE_HOUR, label="Duration")

    street = forms.CharField(max_length=128, label="Street & number")
    city = forms.CharField(max_length=128, label="City/Town")
    postcode = forms.CharField(max_length=128, label="Postcode")

    price = forms.DecimalField(label="Price/person", initial=0, min_value=0, max_value=20)
    booked = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}), initial=False, required=False, label="Pitch booked?")

    field_order=['game_type','date','time','duration','street','city','postcode', 'price', 'booked']

    class Meta:
        model = Game
        exclude = ('game_id', 'free_slots', 'host', 'latitude', 'longitude', 'end', 'custom_slug', 'start')

class RatingForm(forms.ModelForm):
    skill = forms.ChoiceField(choices=Player.RATINGS, initial=Player.THREE)
    likeability = forms.ChoiceField(choices=Player.RATINGS, initial=Player.THREE)
    punctuality = forms.ChoiceField(choices=Player.RATINGS, initial=Player.THREE)

    class Meta:
        model = Player
        fields = ('skill', 'likeability', 'punctuality')

class RateHostForm(forms.ModelForm):
    host_rating = forms.ChoiceField(choices=Player.RATINGS, initial=Player.THREE)

    class Meta:
        model = Player
        fields = ('host_rating',)

class EditUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class FilterForm(forms.ModelForm):
    game_type = forms.ChoiceField(choices=Game.GAME_CHOICES, initial=Game.MENS_CP)

    class Meta:
        model = Game
        fields = ('game_type', )
