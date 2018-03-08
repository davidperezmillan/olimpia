#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import bs4
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError

import hoor.business.scrape.handler_scrap
# Create your views here.
# from merc.models import Series
from hoor.models import Ficha


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
 
class Command(BaseCommand):
    
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        # Positional arguments
        # parser.add_argument('nombre', nargs='1', type=str)
        
        # Named (optional) arguments
        parser.add_argument('--nombre',  nargs='?', default=False)
        parser.add_argument('--id',  nargs='?', default=False)
        parser.add_argument('--session',  nargs='?', default=False)

    def handle(self, *args, **options):
        logger.info("init...")
        logger.info("{} params".format(options))
        
        if options['nombre']:
            logger.info("buscamos por nombre {}".format(options['nombre']))
            series = Ficha.objects.filter(nombre=options['nombre'])[:1]
        elif options['id']:
            logger.info("buscamos por id {}".format(options['id']))
            series = Ficha.objects.filter(id=options['id'])[:1]
        else:
            logger.info("No estamos preparados, que va")
            return
        
        session = options['session']
        hoor.business.scrape.handler_scrap.getInfoOlimpia(series, session)
        




