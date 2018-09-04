from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from merc.models import Series


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
 
class Command(BaseCommand):
    help = "Gestionar las series, \n\r por ahora solo agregar"
 
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('author', type=str)
        
        parser.add_argument('-a','--add', help='Series adds', nargs='+', dest="adds")
        parser.add_argument('-f','--file', help='File Series adds', dest="file")
        
        # # Named (optional) arguments
        parser.add_argument(
            '--nouser',
            action='store_true',
            dest='nouser',
            help='No agregamos si otro usuario tiene la serie',
        )
        # parser.add_argument(
        #     '--restart',
        #     action='store_true',
        #     dest='restart',
        #     help='Pedimos el reinicio de los servicios',
        # )
        # parser.add_argument(
        #     '--nomsg',
        #     action='store_true',
        #     dest='nomsg',
        #     help='No enviamos msg-telegram',
        # )
       


    def handle(self, *args, **options):
        
        if options['author']:
            author = User.objects.get(username=options['author'])
            if options['file']:
                options['adds'] = self.get_series_files(options['file'])
            
            for nombreSerie in options['adds']:
                
                # limpieza
                
                
                # calidad
                quality = "NR"
                if nombreSerie.endswith("_VO"):
                    quality = "VO"
                    nombreSerie = nombreSerie.replace("_VO", "").strip()
                
                if options['nouser']:
                    serie, created = Series.objects.get_or_create(nombre=nombreSerie) 
                else:
                    serie, created = Series.objects.get_or_create(nombre=nombreSerie, author=author) 
                if created:
                    logger.info("Agregamos {}".format(nombreSerie))
                    serie.skipped = True
                    serie.save()
                else:
                    logger.info("La serie ya esta creada {}".format(nombreSerie))
            
            self.stdout.write('Finalizado "{}"'.format(str(author)))
        
        
    def get_series_files(self, file):
        with open(file) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content] 
        return content

