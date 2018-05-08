from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404

# Comunnes


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
logger = logging.getLogger("inc")

# BBDD
from django.contrib.auth.models import User
from hoor.models import Ficha
import hoor.business.jano.launch as launcher

class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        # # Positional arguments
        # parser.add_argument('author', nargs=1, type=str)
        parser.add_argument('author', nargs='+', type=str)
        
        # # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     help='Delete poll instead of closing it',
        # )
        pass

    def handle(self, *args, **options):
        for user in options['author']:
            logger.debug('Ejecutando comando Busqueda por peticion de {}'.format(user))
            author = User.objects.get(username=user)
            logger.debug("Usuario : {}".format(author))
            
            fichas = Ficha.objects.filter(author=author).filter(estado=1)
            respuesta = launcher.handle(fichas)
            # debemos updatear
            for resp in respuesta:
                logger.info("Updateariamos {}".format(resp))
        
        
        
        
        
        
        
        
        
        
        
        
        
        '''
        logger.debug('Ejecutado comando try para montar un lanzador de todo:')
        
        # recuperamos la fichas que queremos lanzar (Todas)
        fichas = Ficha.objects.filter(author=1).filter(estado=1)
        logger.debug("fichas {}".format(fichas))
        for ficha in fichas:
            profile = Profile.objects.get(user=ficha.author) # Recupermos el perfil
            logger.info("____________________________ Ficha: {} --> {}".format(ficha.author, profile))
            try:
                descarga = Descarga.objects.get(ficha=ficha) # Recuperamos las descargas que existan en la ficha
            except Descarga.DoesNotExist:
                descarga = None
            
            logger.debug("Ficha a descarga : {ficha}".format(ficha=ficha))
            logger.debug("Profile  : {profile}".format(profile=profile))
            logger.debug("Descarga  : {descarga}".format(descarga=descarga))
            
            # Si existe descarga lo intentamos
            if descarga:
                logger.info("Intentamos la descarga de la ficha {}".format(ficha))
                
                logger.debug("Quality (descarga.quality) {quality}".format(quality=descarga.quality))
                logger.debug("ep_start (descarga.ep_start) {ep_start}".format(ep_start=descarga.ep_start))
                logger.debug("ep_end (descarga.ep_end) {ep_end}".format(ep_end=descarga.ep_end))
            
                if descarga.plugins.all():
                    logger.debug("Descargas -- Plugins () {plugins}".format(plugins=descarga.plugins.filter(active=True)))
                    pluginsActivos = descarga.plugins.all()
                elif profile.plugins.all():
                    logger.debug("Profile -- Plugins () {plugins}".format(plugins=profile.plugins.filter(active=True)))
                    pluginsActivos = profile.plugins.all()
                else:
                    pluginsActivos = None
                logger.debug("Plugins () {plugins}".format(plugins=pluginsActivos))
                
                
                # Recuperamos los plugins activos segun orden (Descarga, perfil)
                instances = []
                for plugin in pluginsActivos:
                    pActiveFile = "hoor.business.jano.plugins.{0}".format(plugin.file)
                    logger.info( "Plugin active:{0}:{1} ".format(pActiveFile, plugin.clazz))
                    klass = getattr(importlib.import_module(pActiveFile), plugin.clazz)
                    # Instantiate the class (pass arguments to the constructor, if needed)
                    instance = klass()
                    instances.append(instance)
                
                # Buscamos la serie
                founds = []
                # Vamos a iterar las series
                serie = RequestPluginBean(title=ficha.nombre,quality=descarga.quality, epstart=descarga.ep_start, epend=descarga.ep_end) # Mappeo
                logger.debug("Nombre de la serie: {} capitulo: {} final: {}".format(serie.title, serie.epstart, serie.epend))
                for instance in instances:
                    logger.debug("Plugin: {} ".format(instance))
                    founds.extend(instance.execute(serie))
                
                
                # Descargamos los torrent
                logger.debug("Profile -- Server {server}".format(server=profile.server))
                server = profile.server
                torrentHandler = TorrentHandlerClass(host=server.host,port=server.port,user=server.user,password=server.password, logger=logger)
                listTorrentResponse = torrentHandler.allAddTorrent([o.data for o in founds],download_dir_path=server.download, space_disk=server.space_disk, paused=server.paused)    
                logger.info("Capitulos descagados : {} ".format(listTorrentResponse))    
                    
                    
            else:
                logger.warn("No hay descarga para esta ficha {}".format(ficha))

            
        # self.stdout.write('Successfully "{}"'.format(founds))   
        '''
            
    

            
            
            
       

        
