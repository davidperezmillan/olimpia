from django.contrib import admin

# Register your models here.
from .models import Fichas, Capitulos, Vistos


class FichasAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','estado','get_actions')
    # list_filter = ['nombre',]
    search_fields = ['nombre']
    
    def get_actions(self, obj):
        return ''
    
    get_actions.short_description = "Actions"

admin.site.register(Fichas, FichasAdmin)
# admin.site.register(Fichas)

class VistosAdmin(admin.ModelAdmin):
    
    list_display = ('id','temporada','capitulo','author','get_actions')
    list_filter = ['author', 'visto']
    search_fields = ['temporada__ficha__nombre'] # Try using user__username, according to the lookup API "follow" notation. 
        # https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    
    def get_actions(self, obj):
        return ''
    
    get_actions.short_description = "Actions"


admin.site.register(Vistos, VistosAdmin)
# admin.site.register(Vistos()




admin.site.register(Capitulos)



