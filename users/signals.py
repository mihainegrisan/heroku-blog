from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from PIL import Image

# When a User is saved then send this signal(post_save)
# and the signal will be received by the receiver
# that will create the profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # instance is the User
    instance.profile.save()
