from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    ''' For every new created User create a Profile. '''
    if created:
        Profile.objects.create(user=instance).save()
