from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    photo = models.ImageField(upload_to='profiles/photos', blank=True)

    def __str__(self):
        return self.user.username

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return 'default-profile-photo.png'

    def is_male(self):
        return self.gender == self.MALE

    def is_female(self):
        return self.gender == self.FEMALE
