from django.contrib import admin

# Register your models here.
from .models import Ficha, Capitulo, Plugin, Profile, Document


admin.site.register(Profile)
admin.site.register(Document)


class FichaAdmin(admin.ModelAdmin):
    list_display = ('nombre','estado','get_actions_custom')
    list_filter = ['author',]
    search_fields = ['nombre']
    
    def get_actions_custom(self, obj):
        return ''
    
    get_actions_custom.short_description = "Actions"

admin.site.register(Ficha, FichaAdmin)
# admin.site.register(Ficha)

class CapituloAdmin(admin.ModelAdmin):
    
    list_display = ('id','ficha','temporada','capitulo','get_actions_custom')
    # list_filter = ['visto','ficha__nombre',]
    search_fields = ['ficha__nombre'] # Try using user__username, according to the lookup API "follow" notation. 
        # https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    
    def get_actions_custom(self, obj):
        return ''
    
    get_actions_custom.short_description = "Actions"


admin.site.register(Capitulo, CapituloAdmin)
# admin.site.register(Capitulos)


class PluginAdmin(admin.ModelAdmin):
    # ...
    list_display = ('name','file','clazz','active', )
    list_filter = ['active',]
    search_fields = ['name']


admin.site.register(Plugin,PluginAdmin)

