#!/usr/bin/env python
# -*- coding: utf-8 -*-


from hod.scrape.plugins.scrap_playmax_plugin import ScrapPlaymax
# Create your views here.
# from merc.models import Series
from hod.models import Fichas, Capitulos

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def getInfoOlimpia(series, session):
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