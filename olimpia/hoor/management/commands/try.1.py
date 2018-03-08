from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# BBDD
from hoor.models import Descarga, Ficha, Profile, TorrentServer


from hoor.jano.launch import SearchLaunch, DownObject
 
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
        
        #Pruebas 
        ficha_id = 34
        #pruebas
        
        fichas = Ficha.objects.filter(id=ficha_id)[:1]
        
        for ficha in fichas:
            logger.debug("Ficha: {}".format(ficha.author))
            profile = Profile.objects.get(user=ficha.author) # Recupermos el perfil
            descarga = Descarga.objects.get(ficha=ficha) # Recuperamos la descarga OK
            
            
            logger.info("Ficha a descarga : {ficha}".format(ficha=ficha))
            logger.info("Profile  : {profile}".format(profile=profile))
            logger.info("Descarga  : {descarga}".format(descarga=descarga))
            
            logger.info("Datos que necesitamos")
            logger.info("Ficha y descarga")
            logger.info("Nombre (ficha.nombre) {nombre}".format(nombre=ficha.nombre))
            logger.info("Quality (descarga.quality) {quality}".format(quality=descarga.quality))
            logger.info("ep_start (descarga.ep_start) {ep_start}".format(ep_start=descarga.ep_start))
            logger.info("ep_end (descarga.ep_end) {ep_end}".format(ep_end=descarga.ep_end))
            logger.info("Plugin propios de la descarga () {plugins}".format(plugins=descarga.plugins.all()))
            
            logger.info("Autor")
            logger.info("Plugins propios del autor () {plugins}".format(plugins=profile.plugins.all()))
            
            if descarga.plugins.all():
                logger.info("Descargas -- Plugins () {plugins}".format(plugins=descarga.plugins.all()))
            
            if profile.plugins.all():
                logger.info("Profile -- Plugins () {plugins}".format(plugins=profile.plugins.all()))
            
            
            
            
            # Create object SearchLaunch
            downObject = DownObject()
            downObject.nombre = ficha.nombre
            downObject.quality = descarga.quality
            downObject.ep_start = descarga.ep_start
            downObject.ep_end = descarga.ep_end
            if descarga.plugins.all():
                downObject.plugins = descarga.plugins.all()
            elif profile.plugins.all():
                downObject.plugins = profile.plugins.all()
            else:
                downObject.plugins = []
            
            SearchLaunch().execute(downObject)
            
            
            
        self.stdout.write('Successfully "{}"'.format(""))
        
        
        
        
class JanoDescarga:
    
    profile =[]
    plugins = []