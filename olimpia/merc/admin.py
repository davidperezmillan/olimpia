from django.contrib import admin

import re

# unregister your models here.
from .models import Series, TelegramChatIds,TorrentServers, Plugins, TransmissionReceivers
from .modelsCustom import P_History
from django.contrib.auth.models import User

from django.contrib.admin.helpers import ActionForm
from django import forms
from django.contrib.auth.models import User



admin.site.register(TelegramChatIds)



class TorrentServersAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','user','author', 'torrent_active', 'get_plugins')
    list_filter = ['author','torrent_active',]
    search_fields = ['user']
    
    def get_plugins(self, obj):
        return ",\n".join([p.name for p in obj.plugins.all()])
    
    get_plugins.short_description = "Plugins"

admin.site.register(TorrentServers, TorrentServersAdmin)


class PluginsAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','file','clazz','active', )
    list_filter = ['active',]
    search_fields = ['name']


admin.site.register(Plugins,PluginsAdmin)



def setSkipped(self, request,queryset):
    rows_updated = queryset.update(skipped=True)
    message_bit = "{} elementos".format(rows_updated)
    self.message_user(request, "%s marcador como skipped." % message_bit)

setSkipped.short_description = "Parar la descarga" 


def change_owner(self, request, queryset):
    rows_updated = queryset.update(author=request.POST['author'])
    message_bit = "{} elementos".format(rows_updated)
    self.message_user(request, "%s cambiados de author." % message_bit)

change_owner.short_description = "Cambia propietario"




# class ChangeUserForm(ActionForm):
#     choices = [ ( p.id, '{0} {1}'.format( p.first_name, p.last_name ) if p.first_name else p.username,) for p in User.objects.all() ]
#     author = forms.IntegerField(widget=forms.Select(choices=choices))
 

class SeriesAdmin(admin.ModelAdmin):
    
    def upper_case_name(self,obj):
        return ("%s %s" % (obj.nombre, obj.quality)).upper()
    
    upper_case_name.short_description = 'Nombre Completo'
    # ...
    list_display = ('id','upper_case_name','nombre', 'quality', 'author','get_skipped', 'get_complete')
    list_filter = ['author','skipped','paussed','quality',]
    search_fields = ['nombre']
    # action_form = ChangeUserForm
    actions = [change_owner, setSkipped]
    
    def get_complete(self, obj):
        return True if re.search("S99E99",obj.ep_end) else False
            
    get_complete.boolean = True
    get_complete.short_description = "Full"

    def get_skipped(self, obj):
        return False if obj.skipped else True
    
    get_skipped.boolean = True
    get_skipped.short_description = "Pausado"

admin.site.register(Series, SeriesAdmin)



class TransmissionReceiversAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','__unicode__','author','transmission_active')
    list_filter = ['author','transmission_active',]
    # search_fields = ['user']

admin.site.register(TransmissionReceivers, TransmissionReceiversAdmin)




admin.site.register(P_History)