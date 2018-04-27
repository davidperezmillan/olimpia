from django.contrib import admin

from .models import Tasks, DescripModelForm
from django.contrib.auth.models import User

# Register your models here.




class TasksAdmin(admin.ModelAdmin):
    # ...
    list_display = ('descrip','author', 'task','activo','get_cron_raw')
    list_filter = ['author','activo']
    search_fields = ['descrip','task']
    form = DescripModelForm
    
    def get_cron_raw(self, obj):
        return "{minuto} {hora} {diames} {mes} {diasemana} ".format(minuto=obj.minuto, hora=obj.hora, diames=obj.diames, mes=obj.mes, diasemana=obj.diasemana)
    
    get_cron_raw.short_description = "Cron Raw"


# admin.site.register(Tasks)
admin.site.register(Tasks, TasksAdmin)