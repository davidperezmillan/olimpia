#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import urllib, urllib2
import requests
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)



'''
import random
import requests

proxies_list = [List of IPs]

proxies = {
    'http': random.choice(proxies_list)
}
r = requests.get('http://10.1.7.70:8000', proxies=proxies)
'''


    

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
    
        

def toggleproxy(url, values=None, proxies=None, methods=["requests","urllib"]):
    flag_proxy = None
    response = None
    
    if "requests" in methods and "urllib" in methods:
        try:
            logger.info("Lo intentamos sin proxy, todos los metodos")
            response = __geturlAll(url, values)           
        except Exception as e:
            logger.warn("Sin proxy no llegamos: {}".format(e))
            try:
                logger.info("Lo intentamos CON proxy, todos los metodos")
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
                logger.info("Lo intentamos CON proxy, metodo request")
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
                logger.info("Lo intentamos CON proxy, metodo urllib")
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

    