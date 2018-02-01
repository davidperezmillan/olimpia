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

admin.site.register(Vistos)
admin.site.register(Capitulos)



