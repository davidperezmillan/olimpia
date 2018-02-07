from __future__ import unicode_literals

from django.db import models
# from django.utils import timezone
from django.conf import settings


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from .models_second import *
# from models_second import Plugin

from .models_profile import *
# from models_profile import Profile


choice_ficha_estado = (
    (0 , 'Descartada'),
    (1 , 'Activa'),
    (2 , 'Pendiente de nueva Temporada'),
    (3 , 'Cancelada'),
    (4 , 'Terminada'),
    )
    
    
choice_quality = (
    ( 'NR','Normal',),
    ( 'HD','High Definition',),
    ( 'VO','Version Original',),
    ( 'AL','Alternativo (Dificil busqueda)',),
    )

class Ficha(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fichas_autor',
    )
    nombre = models.CharField(max_length=200)  # Field name made lowercase. This field type is a guess.
    estado = models.IntegerField(choices=choice_ficha_estado, default="0")   # Field name made lowercase. This field type is a guess.
    imagen = models.CharField(max_length=200, default="generico.jpg", blank=False, null=False)
    
    
    ## Descarga
    ep_start = models.CharField(max_length=8, default='NRS00E00',blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ep_end = models.CharField(max_length=8, default='NRS99E99', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    quality = models.CharField(max_length=2, choices=choice_quality, default='NR')  # Field name made lowercase. This field type is a guess.
    ultima = models.DateTimeField(blank=True, null=True, auto_now_add=True)  # Field name made lowercase.
    paussed = models.NullBooleanField(default=False)  # Field name made lowercase.
    skipped = models.NullBooleanField(default=False)  # Field name made lowercase.
    plugins = models.ManyToManyField(Plugin, blank=True)
    
    
    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Fichas"
        managed = True
        unique_together = (('nombre', 'author','estado',))

class Capitulo(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    ficha = models.ForeignKey(Ficha)
    temporada = models.IntegerField()
    capitulo = models.IntegerField()
    nombre = models.CharField(max_length=200,blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    visto = models.NullBooleanField(default=False)  # Field name made lowercase.
    descargado = models.NullBooleanField(default=False)  # Field name made lowercase.
    
    def __unicode__(self):
        return "{0} [Temporada {1}X{2}] - {3}".format(self.ficha.nombre, str(self.temporada).zfill(2), str(self.capitulo).zfill(2), self.nombre if self.nombre else "")

    class Meta:
        verbose_name_plural = "Capitulos"
        managed = True
        unique_together = (('ficha', 'temporada', 'capitulo',))
        








'''
class TelegramChatIds(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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

'''        

        
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
   
   
class TransmissionReceivers(models.Model):
    
    id = models.AutoField(primary_key=True)  # AutoField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transmissionreceivers_autor',
        blank=True, null=True,
    )
    transmission_active = models.NullBooleanField(default=False)  # Field name made lowercase.
    username = models.CharField(blank=True, null=True, max_length=200)
    fullname = models.CharField(blank=True, null=True, max_length=200)
    group = models.CharField(blank=True, null=True, max_length=200)
    
    
    def __unicode__(self):
        rep = ""
        if self.username:
            rep = "Username: {}".format(self.username)
        elif self.fullname:
            rep = "Fullname: {}".format(self.fullname)
        elif self.group:
            rep = "Group: {}".format(self.group)
        
        return rep
    
    
    class Meta:
        verbose_name_plural = "TransmissionReceivers"
        managed = True
'''