from __future__ import unicode_literals
 
from django.db import models
from django.utils import timezone
from django.conf import settings


class P_History(models.Model):
    
    id = models.AutoField(primary_key=True)  # AutoField?
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    down = models.NullBooleanField(default=False)  # Field name made lowercase.
    fecha = models.DateTimeField(blank=True, null=True, auto_now_add=True)  # Field name made lowercase.

    def __unicode__(self):
        return "{0} -- {1}".format(self.title, self.fecha)

    class Meta:
        verbose_name_plural = "P_History"
        managed = True
        unique_together = (('title','down'))

