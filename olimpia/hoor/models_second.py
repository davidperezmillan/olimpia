from __future__ import unicode_literals

from django.db import models
# from django.utils import timezone
from django.conf import settings

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




def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'documents/%d%m%Y/{0}'.format(filename)


class Document(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to=user_directory_path)
    
    
    def __unicode__(self):
        return "{0}".format(self.filename)
    
    class Meta:
        verbose_name_plural = "Documents"
        managed = True
