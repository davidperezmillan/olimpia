from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404

# Comunes
import json
from pprint import pprint

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
log_Inc = logging.getLogger("inc")

# BBDD
from django.contrib.auth.models import User
from hoor.models import Ficha, Descarga

# Jano 
 
class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        # # Positional arguments
        parser.add_argument('author', nargs=1, type=str)
        
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
        
            with open('data.json') as f:
                datas = json.load(f)
            
            
            for dataUpdate in datas:
                logger.info("Nombre: {} Start: {} End: {} Quality: {}".format(dataUpdate["nombre"], dataUpdate["ep_start"], dataUpdate["ep_end"], dataUpdate["quality"]))
                # Ficha con este Nombre, Author y Estado ya existe.
                logger.debug("paussed: {} skipped: {} VS: {}".format(dataUpdate["paussed"],dataUpdate["skipped"],dataUpdate["paussed"]=="1" or dataUpdate["skipped"]=="1"))
                if dataUpdate["paussed"]=="1" or dataUpdate["skipped"]=="1":
                    estado=0
                else:
                    estado=1
                
                try:
                    autorReg = dataUpdate["author_id"]
                    author = User.objects.get(id=autorReg)
                    logger.debug("Usuario Registro : {}".format(author))    
                except Exception, e:
                    logger.error("Se ha producido un error al recuperar el usuario  {}:{}".format(dataUpdate["author_id"], author),exc_info=True)
                
                ficha, fichaCreated = Ficha.objects.get_or_create(nombre=dataUpdate["nombre"], author=author)
                ficha.estado=estado
                ficha.save()    
                logger.info("Ficha {} con id {}".format(dataUpdate["nombre"], ficha.id))

                # Entonces grabamos la descarga
                descarga, downCreated = Descarga.objects.get_or_create(ficha=ficha )
                descarga.ep_start=dataUpdate["ep_start"]
                descarga.ep_end=dataUpdate["ep_end"]
                descarga.quality=dataUpdate["quality"]
                descarga.estado_descarga=True
                descarga.save()
                logger.info("Descarga {} con id {}".format(dataUpdate["nombre"], descarga.id))
                    
                
        
