from __future__ import unicode_literals

from django.db import models
from django import forms
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Tasks(models.Model):
    
    
    # Minuto (0-59)
    # Hora (0-23)
    # Dia del mes (1-31)
    # Mes del anno (1-12)
    # Dia de la semana (0-7, 0 y 7 es Domingo)
    # Comando/Script/tarea a ejecutar

    id = models.AutoField(primary_key=True)  # AutoField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks_author',
        blank=True, null=True,
    )
    minuto = models.CharField(max_length=20, default="*")  # Field name made lowercase. This field type is a guess.
    hora = models.CharField(max_length=20, default="*")  # Field name made lowercase. This field type is a guess.
    diames = models.CharField(max_length=20, default="*")  # Field name made lowercase. This field type is a guess.
    mes = models.CharField(max_length=20, default="*")  # Field name made lowercase. This field type is a guess.
    diasemana = models.CharField(max_length=20, default="*")  # Field name made lowercase. This field type is a guess.
    task = models.CharField(max_length=200)
    descrip = models.CharField(max_length=200, default=task)
    activo = models.NullBooleanField(default=False)
    ultima = models.DateTimeField(blank=True, null=True)  # Field name made lowercase.
    
    def __unicode__(self):
        if self.descrip:
            return "{info}".format(info=self.descrip)
        else:
            return "{info}".format(info=self.task)

    class Meta:
        verbose_name_plural = "Tasks"
        managed = True
        db_table = 'tasks'



class DescripModelForm( forms.ModelForm ):
    descrip = forms.CharField( widget=forms.Textarea(attrs={'cols': 120, 'rows': 10}), )
    task = forms.CharField( widget=forms.Textarea(attrs={'cols': 120, 'rows': 3}), )
    class Meta:
        model = Tasks
        fields = '__all__' # Or a list of the fields that you want to include in your form

