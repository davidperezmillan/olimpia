# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
 

from django.db import models
from django.utils import timezone


class Genero(models.Model):
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(db_column='NOMBRE', max_length=200,  unique=True)  # Field name made lowercase. This field type is a guess.

    def __unicode__(self):
        return "{0}".format(self.nombre)

    class Meta:
        verbose_name_plural = "genero"
        managed = True
        db_table = 'genero'
        



class Series(models.Model):
    
    id = models.AutoField(primary_key=True)  # AutoField?
    nombre = models.CharField(max_length=200)  # Field name made lowercase. This field type is a guess.
    ep_start = models.CharField(max_length=8, default='NRS00E00',blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ep_end = models.CharField(max_length=8, default='NRS99E99', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    quality = models.CharField(max_length=2, default='NR')  # Field name made lowercase. This field type is a guess.
    ultima = models.DateTimeField(blank=True, null=True, auto_now_add=True)  # Field name made lowercase.
    paussed = models.NullBooleanField(default=False)  # Field name made lowercase.
    skipped = models.NullBooleanField(default=False)  # Field name made lowercase.
    # genero  = models.ForeignKey(Genero, on_delete=models.CASCADE, default=0)
    genero  = models.ManyToManyField(Genero)
    
    def __unicode__(self):
        return "{0}{1}{2}{3}".format(self.nombre, self.quality, self.ep_start, self.ep_end)

    class Meta:
        verbose_name_plural = "series"
        managed = True
        db_table = 'series'
        unique_together = (('nombre', 'quality'))


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
        db_table = 'telegram_chat_ids'
