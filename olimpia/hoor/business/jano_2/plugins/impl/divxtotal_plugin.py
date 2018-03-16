#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys,os
import traceback

# Utiles

# Plugins
import re
import bs4
from bs4 import BeautifulSoup


#Anexo el Directorio en donde se encuentra la clase a llamar
# sys.path.append('..')
#Importo la Clase
from hoor.business.jano.plugins.plugins import Plugins

# Get an instance of a logger
logger = logging.getLogger(__name__)



url_find = 'http://www.divxtotal2.net/?s={nombreserie}'
searchpattern_find = {'tag':'table', 'filter' : {'class': 'table'}}

# Buscamos una serie
# Hemos optado por buscar 1 serie, mas arriba se buscara un conjunto de series
class DivxTotal(Plugins):
    
    def find(self,serie, values=None, proxies=None):
        logger.info("Comenzamos busqueda de {}".format(serie))
        logger.debug("Proxy {}".format(proxies))
        list = []
        # Recuperamos la pagina de busqueda
        url = url_find.format(nombreserie=serie)
        try:
            page = self.geturlrequest(url, values=values,proxies=proxies)
        except Exception, e:
            # logger.error('Error en find', exc_info=True)
            traceback.print_tb(sys.exc_info()[2])
            raise e
            
        # Parse pagina principal
        source = BeautifulSoup(page, "html.parser")
        buscar_list = source.find_all(searchpattern_find['tag'],**searchpattern_find["filter"])
        
        enlaces = buscar_list[0].find_all("tr") or None
        for buscar in enlaces:
            item = {'name':buscar.find("td").find("a").text.encode('utf-8').strip(), 'link':buscar.find("td").find("a")["href"]}
            list.append(item)
    
        # logger.info("Resultados busqueda de {}".format(list))
        return list 
        
      
    def searchEpisode(self,):
        pass


    def execute(self, serie, values=None, proxies=None):
        lista = self.find(serie, values, proxies )
        episodes_lista, npag = self.episodes(lista[0]['link'], proxies)
        count = 2
        while count <= int(npag):
            url = "{}/pg/{}".format(lista[0]['link'],count)
            episodes_lista_2, npag_2 =self.episodes(url, proxies)
            episodes_lista.extend(episodes_lista_2)
            count = count + 1
        
        return episodes_lista   


def main():
    series = ["Broad City"]
    for serie in series:
        values = None
        proxies_list = ["http://190.12.102.205:8080",] # Argentina de siempre
        proxies = {
            'http': proxies_list[0]
        }
        episodes_lista = DivxTotal().execute(serie,values=values, proxies=proxies)
        for ep in episodes_lista:            
            logger.info("Capitulo : {}".format(ep['name']))
    
    
    

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
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