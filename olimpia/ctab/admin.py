from django.contrib import admin

from django.conf.urls import include, url
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect

from .models import Tasks, DescripModelForm
from django.contrib.auth.models import User
from django.contrib import messages


from ctab.threads.genthread import TasksThread

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)



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
    list_display = ('descrip','act_button','activo','author', 'task','get_cron_raw')
    list_filter = ['author','activo']
    search_fields = ['descrip','task']
    actions = [toggleTasks, stopTasks,starTasks, ]
    form = DescripModelForm
    
    def get_cron_raw(self, obj):
        return "{minuto} {hora} {diames} {mes} {diasemana} ".format(minuto=obj.minuto, hora=obj.hora, diames=obj.diames, mes=obj.mes, diasemana=obj.diasemana)
    
    def get_urls(self):
        urls = super(TasksAdmin, self).get_urls()
        custom_urls = [
            url(r'^launch/(?P<task_id>[0-9]+)/$', self.process_launch, name='lanzar'),
            # url(
            #     r'^(?P<account_id>.+)/act_button/$',
            #     self.act_button,
            #     name='lanzar',
            # ),
        ]
        return custom_urls + urls
    
        
#   	def get_urls(self):
# 	    urls = super(TasksAdmin, self).get_urls()
# 	    my_urls = patterns(
# 	        '',
# 	        (r'^act_button/$', self.act_button)
# 	    )
#     	return my_urls + urls
	
    def act_button(self, obj):
        return format_html(
            '<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><a class="button" href="{}"><i class="fa fa-search"></i></a>',
            reverse('admin:lanzar', args=[obj.id]),
        )


    def process_launch(self, request, task_id, *args, **kwargs):
        
        tasks_thread = TasksThread(kwargs={'task_id':task_id})
        tasks_thread.start()
        
        # logger.info("Lanzamos el proceso {}".format(task_id))
        # task_ejecutable = Tasks.objects.get(id=task_id)
        # command, tOption = task_ejecutable.task.split(" ",1)
        # options = shlex.split(tOption)
        # logger.debug("{} {}".format(command,options))
        # try:
        #     call_command(command,*options)
        #     task_ejecutable.ultima = datetime.now()
        #     task_ejecutable.save()
        
        # except Exception, e:
        #      logger.error("ERROR EN LA TAREA {} ".format(task_ejecutable.descrip))
        
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    get_cron_raw.short_description = "Cron Raw"

    act_button.short_description = "ACT"
    # act_button.allow_tags = True


# admin.site.register(Tasks)
admin.site.register(Tasks, TasksAdmin)