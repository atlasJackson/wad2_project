from django import forms
from django.contrib.auth.models import User
from fives.models import Player, Game


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class PlayerForm(forms.ModelForm):

    gender = forms.ChoiceField(choices=Player.GENDER_CHOICES, label="Gender: ")

    class Meta:
        model=Player
        fields = ('gender',)


class GameForm(forms.ModelForm):
   
    game_type = forms.ChoiceField(choices=Game.GAME_CHOICES, label="Match type: ");

    date = forms.DateField(widget=forms.SelectDateWidget(), label="Date: ")

    # Calculate end_time from start_time and duration
    start_time = forms.TimeField(widget=forms.TimeInput(), label="Start time: ")
    duration = forms.ChoiceField(choices=Game.DURATION_CHOICES, label="Duration: ")

    street = forms.CharField(max_length=128, label="Street & number: ")
    place = forms.CharField(max_length=128, label="City/Town: ")
    postcode = forms.CharField(max_length=128, label="Postocde: ")

    price = forms.DecimalField(widget=forms.TextInput(), label="Price/person: ")
    booked = forms.BooleanField(widget=forms.CheckboxInput(), label="Pitch booked? ")

    class Meta:
        model = Game
        exclude = ('game_id', 'host', 'end_time')
