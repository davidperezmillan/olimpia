from __future__ import unicode_literals

from django.db import models
# from django.utils import timezone
from django.conf import settings


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from .models_down import Plugin

class TelegramChatIds(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='telegramchatids_autor',
    # )
    idtelegram = models.IntegerField(blank=True, null=True,)
    username = models.CharField(blank=True, null=True, max_length=200) # This field type is a guess.
    firstname = models.CharField(blank=True, null=True, max_length=200)  # This field type is a guess.
    surname = models.CharField(blank=True, null=True, max_length=200)  # This field type is a guess.
    group = models.CharField(blank=True, null=True, max_length=200)  # This field type is a guess.

    def __unicode__(self):
        if self.username:
            return self.username
        if self.surname or self.firstname:
            return "{0} {1}".format(self.firstname,self.surname)
        if self.group:
            return self.group
        return str(self.idtelegram)
    
    class Meta:
        verbose_name_plural = "telegramchatids"
        managed = True
        # db_table = 'telegram_chat_ids'


class TorrentServer(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    torrent_active = models.NullBooleanField(default=False)  # Field name made lowercase.
    space_disk = models.IntegerField()
    host = models.CharField(blank=True, null=True, max_length=200)
    port = models.IntegerField()
    user = models.CharField(blank=True, null=True, max_length=200)
    password = models.CharField(blank=True, null=True, max_length=200)
    paused = models.NullBooleanField(default=False)  # Field name made lowercase.
    download = models.CharField(blank=True, null=True, max_length=200)
    
    def __unicode__(self):
        return " {0}@{1}:{2}".format(self.user, self.host, self.port)
    
    
    class Meta:
        verbose_name_plural = "TorrentServers"
        managed = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    plugins = models.ManyToManyField(Plugin, limit_choices_to = {'active': True})
    # server = models.OneToOneField(TorrentServer, blank=True, null=True)
    server = models.ForeignKey(TorrentServer, on_delete=models.CASCADE,blank=True, null=True)
    # telegramCli = models.ManyToManyField(TelegramChatIds, blank=True,limit_choices_to = {'author': user})
    telegramCli = models.ManyToManyField(TelegramChatIds, blank=True)

    
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


