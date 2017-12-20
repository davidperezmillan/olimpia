from django.contrib import admin

# unregister your models here.
from .models import Series, TelegramChatIds,TorrentServers, Plugins


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


class SeriesAdmin(admin.ModelAdmin):
    
    def upper_case_name(self,obj):
        return ("%s %s" % (obj.nombre, obj.quality)).upper()
    
    upper_case_name.short_description = 'Nombre Completo'
    # ...
    list_display = ('id','upper_case_name','nombre', 'quality', 'author')
    list_filter = ['author','skipped','paussed','quality',]
    search_fields = ['nombre']
    
    
admin.site.register(Series, SeriesAdmin)