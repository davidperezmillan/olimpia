#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import urllib, urllib2
import requests
import json

import bs4
from bs4 import BeautifulSoup

# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

logFile = logging.getLogger("file")
logFile.setLevel(logging.DEBUG)
logFormatterFile = logging.Formatter('%(message)s')
fileHandler = logging.FileHandler('paginaresultante.html')
fileHandler.setFormatter(logFormatterFile)
fileHandler.setLevel(logging.DEBUG)
logFile.addHandler(fileHandler)


        
'''
            r.request.allow_redirects  r.request.headers          r.request.response
            r.request.auth             r.request.hooks            r.request.send
            r.request.cert             r.request.method           r.request.sent
            r.request.config           r.request.params           r.request.session
            r.request.cookies          r.request.path_url         r.request.timeout
            r.request.data             r.request.prefetch         r.request.url
            r.request.deregister_hook  r.request.proxies          r.request.verify
            r.request.files            r.request.redirect         
            r.request.full_url         r.request.register_hook        
        
'''
import plugins.utilesplugins as utilesplugins


if __name__ == "__main__":
    
    # proxy = { 
    #           "http"  : "http://190.12.102.205:8080", 
    #         #   "https" : "http://190.12.102.205:8080"
    #         #   "ftp"   : "http://190.12.102.205:8080"
    #         }
    
    
    logger.info("************************************** INI DIVTOTAL ****************************") 
    url = 'http://www.divxtotal2.net/?s="{nombreserie}'.format(nombreserie='Mom')
    logger.info(url)
    response, flag_proxy = utilesplugins.toggleproxy(url)
    if response:
        logger.info("Pagina Encontrada")
        source = BeautifulSoup(response, "html.parser")
        buscar_list = source.find_all("table", {"class" : "table"})
        links = buscar_list[0].find_all("a") or None
        logFile.info(response)
    logger.info("************************************** FINAL DIVTOTAL ****************************") 
    
    
    logger.info("************************************** INI torrentrapid ****************************") 
    url = "http://torrentrapid.com/buscar"
    logger.info(url)
    titulo='Mom'
    values = {'q' : '"{}"'.format(titulo)}
    response, flag_proxy = utilesplugins.toggleproxy(url, values=values)
    if response:
        logger.info("Pagina Encontrada")
        source = BeautifulSoup(response, "html.parser")
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        buscarlista = buscar_list[0]
        logFile.info(response)
    logger.info("************************************** FINAL torrentrapid ****************************") 
    
    
    logger.info("************************************** INI NADA ****************************")  
    url = "http://nada/buscar"
    # Prepare the data
    titulo='Mom'
    values = {'q' : '"{}"'.format(titulo)}
    response, flag_proxy = utilesplugins.toggleproxy(url,values=values,methods=["urllib"])
    
    source = BeautifulSoup(response, "html.parser")
    buscar_list = source.find_all("ul", {"class" : "buscar-list"})
    logFile.info(source)
    logger.info("************************************** FINAL NADA ****************************") 