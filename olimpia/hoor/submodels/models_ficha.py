from __future__ import unicode_literals

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


from django.db import models
# from django.utils import timezone
from django.conf import settings


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




choice_ficha_estado = (
    (0 , 'Descartada'),
    (1 , 'Activa'),
    (2 , 'Pendiente de nueva Temporada'),
    (3 , 'Cancelada'),
    (4 , 'Terminada'),
    )
    
    
# choice_quality = (
#     ( 'NR','Normal',),
#     ( 'HD','High Definition',),
#     ( 'VO','Version Original',),
#     ( 'AL','Alternativo (Dificil busqueda)',),
#     )

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
    
    
    # ## Descarga
    # ep_start = models.CharField(max_length=8, default='NRS00E00',blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    # ep_end = models.CharField(max_length=8, default='NRS99E99', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    # quality = models.CharField(max_length=2, choices=choice_quality, default='NR')  # Field name made lowercase. This field type is a guess.
    # ultima = models.DateTimeField(blank=True, null=True, auto_now_add=True)  # Field name made lowercase.
    # estado_descarga = models.NullBooleanField(default=False)  # Field name made lowercase.
    # plugins = models.ManyToManyField(Plugin, blank=True)
    
    
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
        



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    logger.debug('documents/{0}/{1}'.format(instance.ficha.nombre, instance.filename))
    return 'documents/{0}/{1}'.format(instance.ficha.nombre, instance.filename)


class Document(models.Model):
    ficha = models.ForeignKey(
        Ficha,
        on_delete=models.CASCADE,
        related_name='document_ficha',
    )
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to=user_directory_path)
    
    
    def __unicode__(self):
        return "{0}".format(self.filename)
    
    class Meta:
        verbose_name_plural = "Documents"
        managed = True



