from django.contrib import admin

# Register your models here.
from .models import Ficha, Capitulo, Plugin, Profile, Document, Descarga


admin.site.register(Profile)
admin.site.register(Document)


class DescargaFormInline(admin.StackedInline):
    model = Descarga
    extra = 0
    classes = ['collapse']
    
# class DescargaAdmin(admin.ModelAdmin):
#   pass

# admin.site.register(Descarga, DescargaAdmin)    
admin.site.register(Descarga)




class CapituloFormInline(admin.TabularInline):
    model = Capitulo
    extra = 10
    classes = ['collapse']

class CapituloAdmin(admin.ModelAdmin):
    
    list_display = ('ficha','temporada','capitulo','get_actions_custom')
    # list_filter = ['visto','ficha__nombre',]
    search_fields = ['ficha__nombre'] # Try using user__username, according to the lookup API "follow" notation. 
        # https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    
    def get_actions_custom(self, obj):
        return ''
    
    get_actions_custom.short_description = "Actions"


admin.site.register(Capitulo, CapituloAdmin)
# admin.site.register(Capitulos)







class FichaAdmin(admin.ModelAdmin):
    
    fieldsets = (
        (None, {
            'fields': ('author', ('nombre', 'estado'), 'imagen')
        }),
        # ('Advanced options', {
        #     'classes': ('collapse',),
        #     'fields': (),
        # }),
    )
    
    
    list_display = ('nombre','author','estado','get_actions_custom')
    list_filter = ['author','estado']
    search_fields = ['nombre']
    save_on_top = True
    
    inlines = [DescargaFormInline,CapituloFormInline]
    
    
    def get_actions_custom(self, obj):
        return ''
    
    get_actions_custom.short_description = "Actions"

admin.site.register(Ficha, FichaAdmin)
# admin.site.register(Ficha)




class PluginAdmin(admin.ModelAdmin):
    # ...
    list_display = ('name','file','clazz','active', )
    list_filter = ['active',]
    search_fields = ['name']


admin.site.register(Plugin,PluginAdmin)

