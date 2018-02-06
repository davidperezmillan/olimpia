from django.contrib import admin

# Register your models here.
from .models import Fichas, Capitulos


class FichasAdmin(admin.ModelAdmin):
    list_display = ('nombre','estado','get_actions_custom')
    list_filter = ['author',]
    search_fields = ['nombre']
    
    def get_actions_custom(self, obj):
        return ''
    
    get_actions_custom.short_description = "Actions"

admin.site.register(Fichas, FichasAdmin)
# admin.site.register(Fichas)

class CapitulosAdmin(admin.ModelAdmin):
    
    list_display = ('id','ficha','temporada','capitulo','get_actions_custom')
    # list_filter = ['visto','ficha__nombre',]
    search_fields = ['ficha__nombre'] # Try using user__username, according to the lookup API "follow" notation. 
        # https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    
    def get_actions_custom(self, obj):
        return ''
    
    get_actions_custom.short_description = "Actions"


admin.site.register(Capitulos, CapitulosAdmin)
# admin.site.register(Capitulos)



