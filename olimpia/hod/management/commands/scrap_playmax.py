# encoding=utf8

import requests
import bs4
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError

# from django.contrib.auth.models import User
# import merc.management.commands_utils


# Create your views here.
# from merc.models import Series
from hod.models import Fichas, Capitulos


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
            series = Fichas.objects.filter(nombre=options['nombre'])[:1]
        elif options['id']:
            logger.info("buscamos por id {}".format(options['id']))
            series = Fichas.objects.filter(id=options['id'])[:1]
        else:
            logger.info("No estamos preparados, que va")
        
        session = options['session']
        self.handle_alt(series, session)
        


    def handle_alt(self, series, session):
        logger.info("{} init...".format(__name__))
        
        # Login
        apiKey = 'c2594eef2a33d6465e2b72fc' 
        scrap = ScrapPlaymax(apiKey)
        sid = scrap.call_login()
        if sid is None: 
            logger.error("No hemos conseguido logarnos")
            return 
            
        # Busqueda
        for serie in series:
            searchs = scrap.call_busqueda(serie.nombre,sid)
            if not searchs or searchs is None:
                logger.error("No tenemos fichas sobre {}".format(serie.nombre))
                continue 
            else:    
                # Recuperamos Ficha, de la primera coincidencia
                logger.debug("BORRAR {}".format(searchs))
                search = searchs[0]
                ficha_response = scrap.call_ficha(sid, search.Id.string)
                if ficha_response is None:
                    logger.error("No tenemos fichas sobre {}".format(serie.nombre))
                    return 
                else:
                    
                    
                    # Aqui tenemos la ficha
                    # Ahora bien, que hacemos 
                    # cogemos todas las sessiones o solo la que nos corresponte
                    if session:
                        seasons = scrap.getOneSeason(ficha_response, session)
                    else:
                        seasons = scrap.getSeason(ficha_response)
                    if seasons is None:
                        logger.error("No tenemos Temporadas sobre {}".format(serie.nombre))
                        return
                    else:
                        for season in seasons:
                            season_id = season.Id.string
                            episodes = scrap.getepisodeSeason(season)
                            if episodes is None:
                                logger.error("No tenemos Temporadas sobre {}".format(serie.nombre))
                                return  
                            else:
                                for episode in episodes:            
                                    temporada, created = Capitulos.objects.get_or_create(ficha=serie, temporada=season_id, capitulo=episode.Num.string)
                                    if created:
                                        temporada.descargado=False
                                        temporada.nombre=episode.Name.text
                                        logger.info('{} Se ha creado el capitulo {}'.format(__name__, temporada))  
                                    else:
                                        temporada.nombre=episode.Name.text
                                        logger.info('{} Se ha UPDATE el capitulo {}'.format(__name__, temporada))  
                                    temporada.save()
                                    
        
        
        logger.debug('Successfully "{}"'.format(__name__))
        



class ScrapPlaymax(object):        
        
    def call_login(self):
        logger.debug("LOGIN")
        params = {'apikey':self.apiKey,'username':'elderbar', 'password':'permilda'}
        # Creamos la peticion HTTP con GET:
        response = requests.get("https://playmax.mx/ucp.php?mode=login", params = params)
        if response.status_code == 200:
            logger.info("Login aceptado {}".format(response.status_code))
            source = BeautifulSoup(response.text, 'xml')
            return source.Sid.string
        else:
            return None
            
    def call_busqueda(self,nombre, sid):
        logger.debug("BUSQUEDA")
        params = {'apikey':self.apiKey,'buscar':nombre,'sid':sid, 'mode':['fichas']}
        # Creamos la peticion HTTP con GET:
        response = requests.get("https://playmax.mx/buscar.php", params = params)
        # Imprimimos el resultado si el codigo de estado HTTP es 200 (OK):
        if response.status_code == 200:
            source = BeautifulSoup(response.text, 'xml')
            fichas = source.find_all('Ficha')
            logger.info("Resultados de la busqueda {} Numero {}".format(nombre, len(fichas)))
            count = 1
            for ficha in fichas:
                logger.debug("-- {} -- Ficha {} id  {}".format(count, ficha.Title.text.encode("UTF-8", 'replace'), ficha.Id.string))
                count=count+1
            return fichas
        else:
            return None
            
            
    def call_ficha(self, sid, ficha_id):
        logger.debug("FICHA")
        params = {'apikey':self.apiKey,'sid':sid, 'f':ficha_id, 'api_in_new_structure' : '1'}
        # Creamos la peticion HTTP con GET:
        response = requests.get("https://playmax.mx/ficha.php", params = params)
        # Imprimimos el resultado si el codigo de estado HTTP es 200 (OK):
        if response.status_code == 200:
            source = BeautifulSoup(response.text, 'xml')
            logger.info("Ficha {}".format(source.Data.Info.Title.text.encode("UTF-8", 'replace')))
            return source
        else:
            return None


    def getSeason(self,ficha):
        logger.debug("SESSION")
        logger.debug("Busqueda Sessiones {} resultados".format(ficha.Data.Info.Title.text.encode("UTF-8", 'replace')))
        if ficha is None:
            return None;
        seasons = ficha.find_all('Season')
        for season in seasons:
            logger.debug("Session {} ".format(season.Id.string))
        return seasons
        
        
    def getOneSeason(self,ficha, session):
        logger.debug("SESSION")
        logger.debug("Busqueda Session {} resultados {}".format(session,ficha.Data.Info.Title.text.encode("UTF-8", 'replace')))
        if ficha is None:
            return None;
        season = ficha.find('Id', text=session).parent
        logger.info("Session {} ".format(season.Id.string))
        return [season]
        
   
    def getepisodeSeason(self, season):
        logger.debug("CAPITULOS")
        if season is None:
            return None;
        episodes = season.find_all('Episode')
        for episode in episodes:
            logger.info("Episodio: id: {} Nombre: {}".format(episode.Num.string, episode.Name.text.encode("UTF-8", 'replace')))
        return episodes

 
        
    def __str__(self):
        return ""
        # x=[]
        # if self.apiKey:
        #     x.append('apiKey={0}'.format(self.apiKey))
        # return ' '.join(x)

    def __init__(self,apiKey=None):
        self.apiKey=apiKey