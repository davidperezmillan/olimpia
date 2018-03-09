#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys,os
import urllib, urllib2
import requests
import json
import random


# Get an instance of a logger
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s')
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# consoleHandler.setLevel(logging.DEBUG)
# logger.addHandler(consoleHandler)




# proxies_list = ["http://190.12.102.205:8080","139.255.101.242:8080","117.58.243.244:808","216.165.113.123:3128",] # No los tengo comprobados
proxies_list = ["http://190.12.102.205:8080",]

proxies = {
    'http': random.choice(proxies_list)
}



    

def __geturlrequest(url, values=None, proxies=None):
    try:
        logger.info("Intentado recupera la url por el metodo de requests")
        page = requests.get(url,proxies=proxies, data=json.dumps(values))
        if page.status_code != 200:
            logger.warn('No recuperada la pagina {}'.format(page.status_code))
            raise Exception('No recuperada la pagina {}'.format(page.status_code)) # Don't! If you catch, likely to hide bugs.
        return page.text
    except Exception, e:
        # No lanzamos el log porque luego lo cogemos
        # logger.warn("No hemos conseguido recuperar la reqiest por este metodo:  {}".format(str(e)))
        raise e

def __geturlurllib(url, values=None, proxies=None):
    try:
        logger.debug("Intentado recupera la url por el metodo de urllib2")
        proxy = urllib2.ProxyHandler(proxies)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        if values:
            req = urllib2.Request(url,data=urllib.urlencode(values))
        else:
            req = urllib2.Request(url)
        page = urllib2.urlopen(req)
        if page.getcode() != 200:
            logger.warn('No recuperada la pagina {}'.format(page.status_code))
            raise Exception('No recuperada la pagina {}'.format(page.status_code)) # Don't! If you catch, likely to hide bugs.
        return page
    except Exception, e:
        # No lanzamos el log porque luego lo cogemos
        # logger.warn("No hemos conseguido recuperar la urllib por este metodo:  {}".format(str(e)))
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
            raise e
    
        

def toggleproxy(url, values=None, proxies=proxies, methods=["requests","urllib"]):
    flag_proxy = None
    response = None
    
    if "requests" in methods and "urllib" in methods:
        try:
            logger.info("Lo intentamos sin proxy, todos los metodos")
            response = __geturlAll(url, values)           
        except Exception as e:
            logger.warn("Sin proxy no llegamos: {}".format(e))
            try:
                logger.info("Lo intentamos CON proxy, {proxies} todos los metodos".format(proxies=proxies))
                response = __geturlAll(url, values, proxies)
                flag_proxy = proxies
            except Exception as e:
                logger.warn("Con proxy no llegamos: {}".format(e))
    elif "requests" in methods:   
        try:
            logger.info("Lo intentamos sin proxy, metodo request")
            response = __geturlrequest(url, values)           
        except Exception as e:
            logger.warn("Sin proxy no llegamos: {}".format(e))
        
            try:
                logger.info("Lo intentamos CON proxy, {proxies} todos los metodos".format(proxies=proxies))
                response = __geturlrequest(url, values, proxies)
                flag_proxy = proxies
            except Exception as e:
                logger.warn("Con proxy no llegamos: {}".format(e))
    
    elif "urllib" in methods:
        try:
            logger.info("Lo intentamos sin proxy, metodo urllib")
            response = __geturlurllib(url, values)           
        except Exception as e:
            logger.warn("Sin proxy no llegamos: {}".format(e))
        
            try:
                logger.info("Lo intentamos CON proxy, {proxies} todos los metodos".format(proxies=proxies))
                response = __geturlurllib(url, values, proxies)
                flag_proxy = proxies
            except Exception as e:
                logger.warn("Con proxy no llegamos: {}".format(e))
    
    return response, flag_proxy
    
    
def converterEpisode(episode): # El formato que recuperamos es por defecto NRS00E00
    if episode is None:
        return None, None, None # tenemos que itererar todo lo que enviamos!!!
    quality = episode[:2] or None
    session = episode[3:5] or None
    episode = episode[-2:] or None
    return quality, session, episode

    
    
    
def handlerLoggerException(logger,msg=None,level=logging.WARN):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #  logging.log(level, msg[, *args[, **kwargs]])
    logger.log(level,msg, exc_type, fname, exc_tb.tb_lineno)