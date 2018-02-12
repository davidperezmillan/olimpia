from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
from .models import Ficha, Capitulo, Plugin, Profile, Document, Descarga, TorrentServer




# Descargas
class DescargaFormInline(admin.StackedInline):
    model = Descarga
    extra = 0
    classes = ['collapse']
    
admin.site.register(Descarga)

# Capitulos
class CapituloFormInline(admin.TabularInline):
    model = Capitulo
    extra = 10
    classes = ['collapse']

class CapituloAdmin(admin.ModelAdmin):
    list_display = ('ficha','temporada','capitulo','get_actions_custom')
    search_fields = ['ficha__nombre'] # Try using user__username, according to the lookup API "follow" notation. 
        # https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    
    def get_actions_custom(self, obj):
        return ''
    
    get_actions_custom.short_description = "Actions"

admin.site.register(Capitulo, CapituloAdmin)


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





class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class TorrentServerAdmin(admin.ModelAdmin):
    # ...
    list_display = ('__unicode__',  'torrent_active',)
    list_filter = ['torrent_active',]
    search_fields = ['user']
    

admin.site.register(TorrentServer, TorrentServerAdmin)



admin.site.register(Document)