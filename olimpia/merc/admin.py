from django.contrib import admin

# unregister your models here.
from .models import Series, TelegramChatIds,TorrentServers, Plugins
from django.contrib.auth.models import User

from django.contrib.admin.helpers import ActionForm
from django import forms
from django.contrib.auth.models import User



admin.site.register(TelegramChatIds)



class TorrentServersAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','user','author', 'torrent_active')
    list_filter = ['author','torrent_active',]
    search_fields = ['user']


admin.site.register(TorrentServers, TorrentServersAdmin)


class PluginsAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','active', )
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




class ChangeUserForm(ActionForm):
    choices = [ ( p.id, '{0} {1}'.format( p.first_name, p.last_name ) if p.first_name else p.username,) for p in User.objects.all() ]
    author = forms.IntegerField(widget=forms.Select(choices=choices))
 

class SeriesAdmin(admin.ModelAdmin):
    
    def upper_case_name(self,obj):
        return ("%s %s" % (obj.nombre, obj.quality)).upper()
    
    upper_case_name.short_description = 'Nombre Completo'
    # ...
    list_display = ('id','upper_case_name','nombre', 'quality', 'author')
    list_filter = ['author','skipped','paussed','quality',]
    search_fields = ['nombre']
    action_form = ChangeUserForm
    actions = [change_owner, setSkipped]
    

admin.site.register(Series, SeriesAdmin)