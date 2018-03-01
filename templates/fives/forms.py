from django import forms
from django.contrib.auth.models import User
from fives.models import Player, Game

#class PlayerForm(forms.Modelform):

class GameForm(forms.ModelForm):

    game_type = forms.IntegerField()

    date = forms.DateField(widget=SelectDateWidget(empty_label=("Year", "Month", "Day")))

    start_time = forms.TimeField(widget=TimeInput())
    end_time = forms.TimeField(widget=TimeInput())
    duration = forms.BooleanField(widget=CheckboxInput())

    street = forms.CharField(max_length=128, help_text="Street name and number: ")
    place = forms.CharField(max_length=128, help_text="City/Town: ")
    postcode = forms.CharField(max_length=128, help_text="Postocde: ")

    price = forms.DecimalField(widget=TextInput())
    booked = forms.BooleanField(widget=CheckboxInput())

    class Meta:
        model = Game
        exclude = ('game_id', 'host',)