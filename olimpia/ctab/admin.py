from django.contrib import admin

from .models import Tasks, DescripModelForm
from django.contrib.auth.models import User
from django.contrib import messages

# Register your models here.


def toggleTasks(self, request, queryset):
    for t in queryset:
        t.activo=not t.activo
        t.save()
    # rows_updated = queryset.update(activo=False)
    # message_bit = "{} elementos".format(rows_updated)
    # self.message_user(request, "{} tareas marcadas".format(message_bit))

toggleTasks.short_description = "Cambiar estado de las tareas" 


def stopTasks(self, request, queryset):
    rows_updated = queryset.update(activo=False)
    message_bit = "{} elementos".format(rows_updated)
    self.message_user(request, "{} tareas marcadas".format(message_bit))

stopTasks.short_description = "Desactivar las tareas" 


def starTasks(self, request, queryset):
    rows_updated = queryset.update(activo=True)
    message_bit = "{} elementos".format(rows_updated)
    self.message_user(request, "{} tareas marcadas".format(message_bit), level=messages.INFO)

starTasks.short_description = "Activar las tareas" 


class TasksAdmin(admin.ModelAdmin):
    # ...
    list_display = ('descrip','author', 'task','activo','get_cron_raw')
    list_filter = ['author','activo']
    search_fields = ['descrip','task']
    actions = [toggleTasks, stopTasks,starTasks, ]
    form = DescripModelForm
    
    def get_cron_raw(self, obj):
        return "{minuto} {hora} {diames} {mes} {diasemana} ".format(minuto=obj.minuto, hora=obj.hora, diames=obj.diames, mes=obj.mes, diasemana=obj.diasemana)
    
    get_cron_raw.short_description = "Cron Raw"


# admin.site.register(Tasks)
admin.site.register(Tasks, TasksAdmin)