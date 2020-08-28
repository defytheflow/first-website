from django import forms

from .models import Workout


class WorkoutForm(forms.Form):
    date = forms.DateField()
    body_part1 = forms.CharField()
    num_exercises1 = forms.IntegerField()
    body_part2 = forms.CharField()
    num_exercises2 = forms.IntegerField()
    cardio = forms.CharField()
    cardio_load = forms.CharField()
    summary = forms.Textarea()


class WorkoutModelForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'body_part1', 'num_exercises1', 'body_part2',
                  'num_exercises2', 'cardio', 'cardio_load', 'summary']
