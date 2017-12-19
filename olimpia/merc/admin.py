from django.contrib import admin

# unregister your models here.
from .models import Series, TelegramChatIds,TorrentServers, Plugins


admin.site.register(TelegramChatIds)
admin.site.register(TorrentServers)
admin.site.register(Plugins)





class SeriesAdmin(admin.ModelAdmin):
    
    def upper_case_name(self,obj):
        return ("%s %s" % (obj.nombre, obj.quality)).upper()
    
    upper_case_name.short_description = 'Nombre Completo'
    # ...
    list_display = ('id','upper_case_name','nombre', 'quality', 'author')
    list_filter = ['author','skipped','paussed','quality',]
    search_fields = ['nombre']
    
    
admin.site.register(Series, SeriesAdmin)