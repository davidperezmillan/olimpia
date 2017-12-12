from django.contrib import admin

# unregister your models here.
from .models import Series, TelegramChatIds,TorrentServers, Plugins

admin.site.register(Series)
admin.site.register(TelegramChatIds)
admin.site.register(TorrentServers)
admin.site.register(Plugins)

