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



def __geturlrequest(url, values=None, proxies=None):
    try:
        logger.info("Intentado recupera la url por el metodo de requests")
        page = requests.get(url,proxies=proxies, data=json.dumps(values))
        if page.status_code != 200:
            raise Exception('No recuperada la pagina {}'.format(page.status_code)) # Don't! If you catch, likely to hide bugs.
        return page.text
    except Exception, e:
        raise e

def __geturlurllib(url, values=None, proxies=None):
    try:
        logger.info("Intentado recupera la url por el metodo de urllib2")
        proxy = urllib2.ProxyHandler(proxies)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        if values:
            req = urllib2.Request(url,data=urllib.urlencode(values))
        else:
            req = urllib2.Request(url)
        page = urllib2.urlopen(req)
        logger.info(page.getcode())
        if page.getcode() != 200:
            raise Exception('No recuperada la pagina {}'.format(page.status_code)) # Don't! If you catch, likely to hide bugs.
        return page
    except Exception, e:
        raise e

def __geturlAll(url, values=None, proxies=None):
    try:
       response = __geturlrequest(url, values, proxies)
       return response
    except Exception, e:
        logger.warn("No hemos conseguido recuperar la request por este metodo {}".format(str(e)))
        try:
          response = __geturlurllib(url,values,proxies)
          return response
        except Exception, e:
            logger.warn("No hemos conseguido recuperar la urllib por este metodo:  {}".format(str(e)))
    
        

def toggleproxy(url, values=None, proxies=None, methods=["requests","urllib"]):
    flag_proxy = None
    response = None
    
    if "requests" in methods and "urllib" in methods:
        try:
            logger.debug("Lo intentamos sin proxy, todos los metodos")
            response = __geturlAll(url, values)           
        except Exception as e:
            logger.warn("Sin proxy no llegamos: {}".format(e),  exc_info=True)
            try:
                logger.debug("Lo intentamos CON proxy, todos los metodos")
                response = __geturlAll(url, values, proxies)
                flag_proxy = proxies
            except Exception as e:
                logger.warn("Con proxy no llegamos: {}".format(e))
    elif "requests" in methods:   
        try:
            logger.debug("Lo intentamos sin proxy, metodo request")
            response = __geturlrequest(url, values)           
        except Exception as e:
            logger.warn("Sin proxy no llegamos: {}".format(e),  exc_info=True)
        
            try:
                logger.debug("Lo intentamos CON proxy, metodo request")
                response = __geturlrequest(url, values, proxies)
                flag_proxy = proxies
            except Exception as e:
                logger.warn("Con proxy no llegamos: {}".format(e))
    
    elif "urllib" in methods:
        try:
            logger.debug("Lo intentamos sin proxy, metodo urllib")
            response = __geturlurllib(url, values)           
        except Exception as e:
            logger.warn("Sin proxy no llegamos: {}".format(e),  exc_info=True)
        
            try:
                logger.debug("Lo intentamos CON proxy, metodo urllib")
                response = __geturlurllib(url, values, proxies)
                flag_proxy = proxies
            except Exception as e:
                logger.warn("Con proxy no llegamos: {}".format(e))
    
    return response, flag_proxy


if __name__ == "__main__":
    
    proxy = { 
              "http"  : "http://190.12.102.205:8080", 
            #   "https" : "http://190.12.102.205:8080"
            #   "ftp"   : "http://190.12.102.205:8080"
            }
    
    
    
    url = 'http://www.divxtotal2.net/?s="{nombreserie}'.format(nombreserie='Mom')
    logger.info(url)
    response, flag_proxy = toggleproxy(url,proxy)
    if response:
        logger.info("Pagina Encontrada")
        source = BeautifulSoup(response, "html.parser")
        buscar_list = source.find_all("table", {"class" : "table"})
        links = buscar_list[0].find_all("a") or None
        for link in links:
            logger.info("enlaces : {}".format(link['href']))
        logFile.info(response)
    
    
    url = "http://torrentrapid.com/buscar"
    logger.info(url)
    titulo='Mom'
    values = {'q' : '"{}"'.format(titulo)}
    response, flag_proxy = toggleproxy(url, proxies=proxy, values=values)
    if response:
        logger.info("Pagina Encontrada")
        source = BeautifulSoup(response, "html.parser")
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        buscarlista = buscar_list[0]
        for buscar in buscarlista:
            logger.info("enlaces : {}".format(buscar))
        logFile.info(response)
    
    
    
    
    url = "http://nada/buscar"
    # Prepare the data
    titulo='Mom'
    values = {'q' : '"{}"'.format(titulo)}
    response, flag_proxy = toggleproxy(url, proxies=proxy, values=values,methods=["urllib"])
    
    source = BeautifulSoup(response, "html.parser")
    buscar_list = source.find_all("ul", {"class" : "buscar-list"})
    logFile.info(source)
    