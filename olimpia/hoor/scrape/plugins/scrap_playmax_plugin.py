#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import bs4
from bs4 import BeautifulSoup

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
 
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