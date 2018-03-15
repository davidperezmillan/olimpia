#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys,os

# Utiles
import urllib, urllib2
import requests
import json
import random

# Plugins
import re
import bs4
from bs4 import BeautifulSoup


#Anexo el Directorio en donde se encuentra la clase a llamar
sys.path.append('..')
#Importo la Clase
from plugins import Plugins

# Get an instance of a logger
logger = logging.getLogger(__name__)



       

url_find = 'http://torrentrapid.com/buscar'
searchpattern_info = {'tag':'div','filter':{'class':'info'}}
searchpattern_find = {'tag':'ul', 'filter' : {'class': 'buscar-list'}}
searchpattern_episodes = {'tag':'ul', 'filter' : {'class': 'buscar-list'}}

# Buscamos una serie
# Hemos optado por buscar 1 serie, mas arriba se buscara un conjunto de series
class TorrentRapid(Plugins):
    
    def find(self,serie, values=None, proxies=None):
        logger.info("Comenzamos busqueda de {}".format(serie))
        logger.debug("Proxy {}".format(proxies))
        
        list = []
        
        # Recuperamos la pagina de busqueda
        url = url_find
        try:
            page = self.geturlurllib(url, values=values,proxies=proxies)
        except Exception, e:
            logger.error('Error en find', exc_info=True)
            raise e
        # Parse pagina principal
        source = BeautifulSoup(page, "html.parser")
        buscar_list = source.find_all(searchpattern_find['tag'],**searchpattern_find["filter"])
        
        loggerfile.info(source)
        
        enlaces = buscar_list[0].find_all("div") or None
        if enlaces is None:
            raise Exception('No hay series con este titulo {}'.format(serie)) # Don't! If you catch, likely to hide bugs.
        for buscar in enlaces:
            item = {'name':buscar.find("h2").text.encode('utf-8').strip(), 'link':buscar.find("a")["href"]}
            list.append(item)
    
        logger.info("Resultados busqueda de {}".format(list))
        return list 
        
        
    def episodes(self,url, proxies=None):
        logger.info("Comenzamos busqueda de {}".format(url))
        list = []
        try:
            page = self.geturlurllib(url, values=None,proxies=proxies)
        except Exception, e:
            raise e
        source = BeautifulSoup(page, "html.parser")
        buscar_list = source.find_all(searchpattern_find['tag'],**searchpattern_find["filter"])
        enlaces = buscar_list[0].find_all(searchpattern_info['tag'], **searchpattern_info["filter"]) or None
        
        for buscar in enlaces:
            item = {'name':buscar.find("h2").text.encode('utf-8').strip(), 'link':buscar.find("a")["href"]}
            list.append(item)
        
        # Recuperamos la ultima pagina
        # Esto lo haremos por plugins
        pagination = source.find_all("ul", {"class": "pagination"})[0].find_all("li")[-1].find("a")['href']
        npag = pagination.split('/')[-1]
        
        logger.debug("Resultados busqueda de {}".format(list))
        return list, npag



    def execute(self, serie, values=None, proxies=None):
        lista = TorrentRapid().find(serie, values, proxies )
        episodes_lista, npag = TorrentRapid().episodes(lista[0]['link'], proxies)
        count = 2
        while count <= int(npag):
            url = "{}/pg/{}".format(lista[0]['link'],count)
            episodes_lista_2, npag_2 =TorrentRapid().episodes(url, proxies)
            episodes_lista.extend(episodes_lista_2)
            count = count + 1
        
        return episodes_lista
        



def main():
    
    serie = "Daredevil"
    quality = ["HD"]
    titulo = '"{0}"'.format(serie)
    if quality=="HD":
        quality="1469"
    elif quality=="VO":
        quality=""
    elif quality=="AL":
        quality=""
        titulo = '{0}'.format(serie)
    else:
        quality="767"
    values = {'q' : titulo,"categoryIDR":quality, "ordenar":"Nombre", "inon":"Descendente"}
    proxies = None
    # proxies_list = ["http://190.2.6.105:3130",]
    # proxies = {
    #     'http': proxies_list[0]
    # }




    # Buscar todos los episodios
    # episodes_lista = TorrentRapid().execute(serie,values=values, proxies=proxies)
    # for ep in episodes_lista:            
    #     logger.info("Capitulo : {}".format(ep['name']))
        
    # Ver lista de series
    listado = TorrentRapid().find("Top of the Lake",{'q' : "Top of the Lake","categoryIDR":'1469', "ordenar":"Nombre", "inon":"Ascendente"}, None )
    for elemento in listado:
        logger.info("Encontrado : {} con link {}".format(elemento['name'], elemento['link']))

    
    
    
    

if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)
    
    loggerfile = logging.getLogger('myapp')
    hdlr = logging.FileHandler('../../myapp.html', mode='w')
    # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # hdlr.setFormatter(formatter)
    loggerfile.addHandler(hdlr) 
    loggerfile.setLevel(logging.INFO)
    
    
    main()