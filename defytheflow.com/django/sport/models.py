from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    date = models.DateField(auto_now=False)
    body_part1 = models.CharField(max_length=100, blank=False)
    num_exercises1 = models.PositiveSmallIntegerField(blank=False)
    body_part2 = models.CharField(max_length=100, blank=True, null=True)
    num_exercises2 = models.PositiveSmallIntegerField(blank=True, null=True)
    cardio = models.CharField(max_length=100, blank=True, null=True)
    cardio_load = models.CharField(max_length=100, blank=True, null=True)
    summary = models.TextField()

    def __str__(self):
        return str(self.date)


