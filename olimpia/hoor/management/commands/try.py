from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
log_Inc = logging.getLogger("inc")

# BBDD
from hoor.models import Descarga, Ficha, Profile, TorrentServer


from hoor.business.jano.launch import SearchLaunch
from hoor.business.jano.common.downJano import Down
 
class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        # # Positional arguments
        # parser.add_argument('author', nargs=1, type=str)
        
        # # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     help='Delete poll instead of closing it',
        # )
        pass

    def handle(self, *args, **options):
        
        logger.debug('Ejecutando comando try :')
        downs = []
        
        #Pruebas 
        # ficha_id = 5
        ficha_id = [3,4,5]
        #pruebas

        fichas = Ficha.objects.filter(id__in=ficha_id)
        
        for ficha in fichas:
            logger.debug("Ficha: {}".format(ficha.author))
            profile = Profile.objects.get(user=ficha.author) # Recupermos el perfil
            try:
                descarga = Descarga.objects.get(ficha=ficha)
            except Descarga.DoesNotExist:
                descarga = None
            
            
            logger.debug("Ficha a descarga : {ficha}".format(ficha=ficha))
            logger.debug("Profile  : {profile}".format(profile=profile))
            logger.debug("Descarga  : {descarga}".format(descarga=descarga))
            
            logger.debug("Datos que necesitamos")
            logger.debug("Ficha y descarga")
            logger.debug("Nombre (ficha.nombre) {nombre}".format(nombre=ficha.nombre))
            if descarga:
                logger.debug("Quality (descarga.quality) {quality}".format(quality=descarga.quality))
                logger.debug("ep_start (descarga.ep_start) {ep_start}".format(ep_start=descarga.ep_start))
                logger.debug("ep_end (descarga.ep_end) {ep_end}".format(ep_end=descarga.ep_end))
                logger.debug("Plugin propios de la descarga () {plugins}".format(plugins=descarga.plugins.all()))
            
            logger.debug("Autor")
            logger.debug("Plugins propios del autor () {plugins}".format(plugins=profile.plugins.all()))
            
            if descarga and descarga.plugins.all():
                logger.debug("Descargas -- Plugins () {plugins}".format(plugins=descarga.plugins.all()))
            
            if profile.plugins.all():
                logger.debug("Profile -- Plugins () {plugins}".format(plugins=profile.plugins.all()))
            
            
            
            
            # Create object SearchLaunch
            if descarga:
                down = Down()
                down.id_ficha = ficha.id
                down.nombre = ficha.nombre
                down.quality = descarga.quality
                down.ep_start = descarga.ep_start
                down.ep_end = descarga.ep_end
                if descarga and descarga.plugins.all():
                    down.plugins = descarga.plugins.all()
                elif profile.plugins.all():
                    down.plugins = profile.plugins.all()
                else:
                    down.plugins = []
                downs.append(down)
            
                
            
        log_Inc.info("Enviamos a descargar : {lista}".format(lista=downs))   
        SearchLaunch().execute(downs)    
        self.stdout.write('Successfully "{}"'.format(""))
        
        
