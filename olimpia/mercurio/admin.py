from django.contrib import admin

# Register your models here.
from .models import Genero
from .models import Series
from .models import TelegramChatIds

admin.site.register(Genero)
admin.site.register(Series)
admin.site.register(TelegramChatIds)