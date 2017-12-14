from __future__ import unicode_literals
 
from django.db import models
from django.utils import timezone
from django.conf import settings


class Series(models.Model):
    
    id = models.AutoField(primary_key=True)  # AutoField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='series_autor',
        blank=True, null=True,
    )
    nombre = models.CharField(max_length=200)  # Field name made lowercase. This field type is a guess.
    ep_start = models.CharField(max_length=8, default='NRS00E00',blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ep_end = models.CharField(max_length=8, default='NRS99E99', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    quality = models.CharField(max_length=2, default='NR')  # Field name made lowercase. This field type is a guess.
    ultima = models.DateTimeField(blank=True, null=True, auto_now_add=True)  # Field name made lowercase.
    paussed = models.NullBooleanField(default=False)  # Field name made lowercase.
    skipped = models.NullBooleanField(default=False)  # Field name made lowercase.
    
    def __unicode__(self):
        return "{0}{1}{2}{3}".format(self.nombre, self.quality, self.ep_start, self.ep_end)

    class Meta:
        verbose_name_plural = "series"
        managed = True
        db_table = 'series'
        unique_together = (('nombre', 'quality', 'author'))


class TelegramChatIds(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='telegram_chat_ids_autor',
        blank=True, null=True,
    )
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
        return str(self.id)
    
    class Meta:
        verbose_name_plural = "telegram_chat_ids"
        managed = True
        db_table = 'telegram_chat_ids'

        
class Plugins(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    name= models.CharField(blank=True, null=True, max_length=200)
    file= models.CharField(blank=True, null=True, max_length=200)
    clazz= models.CharField(blank=True, null=True, max_length=200) 
    active = models.NullBooleanField(default=False)  # Field name made lowercase.
    
    
    def __unicode__(self):
        return "{0}".format(self.name)
    
    class Meta:
        verbose_name_plural = "Plugins"
        managed = True
        db_table = 'plugins'
        
        
'''
  "torrent_server": {
            "torrent_active": true,
            "requirements": { "space_disk": [[999999999]] },
            "transmission": {
                "host": "[[url]]",
                "port": "[[port]]",
                "user": "[[user]]",
                "password": "[[pass]]",
                "options": {
                    "paused": false
                },
                "custom_options": {
                    "download_dir_path": "[[download_dir_path]]",
                    "download_dir_path_film": "[[download_dir_path_film]]"
                }
            }
        },
'''

class TorrentServers(models.Model):
    
    id = models.AutoField(primary_key=True)  # AutoField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='torrentservers_autor',
        blank=True, null=True,
    )
    torrent_active = models.NullBooleanField(default=False)  # Field name made lowercase.
    space_disk = models.IntegerField()
    host = models.CharField(blank=True, null=True, max_length=200)
    port = models.IntegerField()
    user = models.CharField(blank=True, null=True, max_length=200)
    password = models.CharField(blank=True, null=True, max_length=200)
    paused = models.NullBooleanField(default=False)  # Field name made lowercase.
    download = models.CharField(blank=True, null=True, max_length=200)
    plugins = models.ManyToManyField(Plugins, blank=True)
    
    def __unicode__(self):
        return "[{0}] {1}     {2}:{3}".format(self.author,self.user, self.host, self.port)
    
    
    class Meta:
        verbose_name_plural = "TorrentServers"
        managed = True
        db_table = 'torrentservers'
   
   
'''
"newpct1": {
    "file": "newpct1_handler",
    "clazz": "Newpct1HandlerClass"
},
"torrentrapid": {
    "file": "torrentrapid_handler",
    "clazz": "TorrentRapidHandlerClass"
}
'''