from __future__ import unicode_literals

from django.db import models
# from django.utils import timezone
from django.conf import settings

# Create your models here.

choice_ficha_estado = (
    (0 , 'Descartada'),
    (1 , 'Activa'),
    (2 , 'Pendiente de nueva Temporada'),
    (3 , 'Cancelada'),
    (4 , 'Terminada'),
    )


class Fichas(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fichas_autor',
    )
    nombre = models.CharField(max_length=200)  # Field name made lowercase. This field type is a guess.
    estado = models.IntegerField(choices=choice_ficha_estado, default="0")   # Field name made lowercase. This field type is a guess.
    imagen = models.CharField(max_length=200, default="generico.jpg", blank=False, null=False)
    
    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "fichas"
        managed = True
        unique_together = (('nombre', 'author','estado',))

class Capitulos(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    ficha = models.ForeignKey(Fichas)
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
class Vistos(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    temporada = models.ForeignKey(Capitulos)
    capitulo = models.IntegerField()
    visto = models.NullBooleanField(default=False)  # Field name made lowercase.
    descargado = models.NullBooleanField(default=False)  # Field name made lowercase.
    
    def __unicode__(self):
        return "{0} [{1}x{2}]".format(self.temporada.ficha.nombre, str(self.temporada.temporada).zfill(2), str(self.capitulo).zfill(2))

    class Meta:
        verbose_name_plural = "Vistos"
        managed = True
        unique_together = (('temporada','capitulo'))
'''