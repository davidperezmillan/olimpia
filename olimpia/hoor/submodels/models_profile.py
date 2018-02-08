from __future__ import unicode_literals

from django.db import models
# from django.utils import timezone
from django.conf import settings


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from .models_down import Plugin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    plugins = models.ManyToManyField(Plugin, blank=True)

    
    def __unicode__(self):
        return "{0}".format(self.user)
    
    class Meta:
        verbose_name_plural = "profiles"
        managed = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


