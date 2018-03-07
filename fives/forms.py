from django import forms
from django.contrib.auth.models import User
from fives.models import Player, Game

GAME_CHOICES = (
    ('MENS_CP', "Men's Competitive"),
    ('MENS_FR', "Men's Friendly"),
    ('WOMENS_CP', "Women's Competitive"),
    ('WOMENS_FR', "Women's Friendly"),
    ('MIXED_CP', "Mixed Competitive"),
    ('MIXED_FR', "Mixed Friendly"),
)

#class PlayerForm(forms.Modelform):

class GameForm(forms.ModelForm):

    game_type = forms.ChoiceField(choices=GAME_CHOICES, label="Match type:");

    date = forms.DateField(widget=forms.SelectDateWidget(), label="Date:")

    start_time = forms.TimeField(widget=forms.TimeInput(), label="Start time:")
    end_time = forms.TimeField(widget=forms.HiddenInput(), )
    duration = forms.BooleanField(widget=forms.CheckboxInput(), label="Duration")

    street = forms.CharField(max_length=128, label="Street & number: ")
    place = forms.CharField(max_length=128, label="City/Town: ")
    postcode = forms.CharField(max_length=128, label="Postocde: ")

    price = forms.DecimalField(widget=forms.TextInput(), label="Price/person")
    booked = forms.BooleanField(widget=forms.CheckboxInput(), label="Pitch booked?")

    class Meta:
        model = Game
        exclude = ('game_id', 'host', 'end_time')
