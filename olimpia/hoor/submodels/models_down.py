from __future__ import unicode_literals

from django.db import models
# from django.utils import timezone
from django.conf import settings


from .models_ficha import Ficha



choice_quality = (
    ( 'NR','Normal',),
    ( 'HD','High Definition',),
    ( 'VO','Version Original',),
    ( 'AL','Alternativo (Dificil busqueda)',),
    )


# Create your models here.
class Plugin(models.Model):
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



class Descarga(models.Model):
    ## Descarga
    id = models.AutoField(primary_key=True)  # AutoField?
    ficha = models.OneToOneField(Ficha)
    ep_start = models.CharField(max_length=8, default='NRS00E00',blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ep_end = models.CharField(max_length=8, default='NRS99E99', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    quality = models.CharField(max_length=2, choices=choice_quality, blank=False, null=False)  # Field name made lowercase. This field type is a guess.
    ultima = models.DateTimeField(blank=True, null=True, auto_now_add=True)  # Field name made lowercase.
    estado_descarga = models.NullBooleanField(default=False)  # Field name made lowercase.
    plugins = models.ManyToManyField(Plugin, blank=True, limit_choices_to = {'active': True})

    def __unicode__(self):
        return "{0}".format(self.ficha.nombre)
    
    class Meta:
        verbose_name_plural = "Descargas"
        managed = True



