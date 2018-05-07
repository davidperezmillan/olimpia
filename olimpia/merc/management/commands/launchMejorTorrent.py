#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

# from django.contrib.auth.models import User
# from merc.models import Series, TorrentServers, Plugins, TelegramChatIds
# from merc.forms import SeriesForm, TorrentServersForm, SeriesFindForm
# from merc.at.airtrapLauncher import AirTrapLauncher

# import merc.at.hilos.utiles
# import merc.management.commands_utils

from merc.at.plugins.mejortorrent_handler import MejorTorrentHandlerClass, RequestPlugin

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


 
class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        pass
       
 
 
    def handle(self, *args, **options):
        
        request = RequestPlugin(title="The Walking dead",epstart="NRS02E00", epend="NRS02E99") 
        # request = RequestPlugin(title="Jessica Jones",epstart="HDS02E00") 
        trhc = MejorTorrentHandlerClass()
        respuesta = trhc.execute(request)
        if respuesta:
            for item in respuesta:
                print "Respuesta final {}".format(item)