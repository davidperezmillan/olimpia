from __future__ import unicode_literals

from django.db import models
# from django.utils import timezone
from django.conf import settings

# Create your models here.

class Fichas(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    nombre = models.CharField(max_length=200)  # Field name made lowercase. This field type is a guess.
    estado = models.CharField(max_length=2,choices=(('0', 'Pendiente nueva temporada'), ('1', 'Siguiendo'), ('2', 'Cancelada'),), default="0")   # Field name made lowercase. This field type is a guess.
    
    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "fichas"
        managed = True
        unique_together = (('nombre', 'estado',))

class Capitulos(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    ficha = models.ForeignKey(Fichas)
    temporada = models.IntegerField()
    capitulo = models.IntegerField()
    nombre = models.CharField(max_length=200,blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    
    def __unicode__(self):
        return "{0} [{1}x{2}] - {3}".format(self.ficha.nombre, str(self.temporada).zfill(2), str(self.capitulo).zfill(2), self.nombre if self.nombre else "")

    class Meta:
        verbose_name_plural = "Capitulos"
        managed = True
        unique_together = (('ficha', 'temporada','capitulo'))
        
        
class Vistos(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vistos_autor',
        blank=True, null=True,
    )
    capitulo = models.OneToOneField(
        Capitulos,
        on_delete=models.CASCADE,
        # primary_key=True,
    )
    visto = models.NullBooleanField(default=False)  # Field name made lowercase.
    descargado = models.NullBooleanField(default=False)  # Field name made lowercase.
    
    def __unicode__(self):
        return "{0} {1}".format(self.author, self.capitulo)

    class Meta:
        verbose_name_plural = "Vistos"
        managed = True
        unique_together = (('author','capitulo'))