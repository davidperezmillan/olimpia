#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, sys, os
# Utiles
import urllib, urllib2, requests
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)



class Plugins(object):
    
    
    
    
    def geturlurllib(self,url, values=None, proxies=None):
        try:
            logger.info("Intentado recupera la url por el metodo de urllib2 [{}]-{} --- {}  ".format(proxies,url, values))
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
            
     
     
    def geturlrequest(self, url, values=None, proxies=None):
        try:
            logger.info("Intentado recupera la url por el metodo de requests [{}]-{} --- {}  ".format(proxies,url, values))
            page = requests.get(url,proxies=proxies, data=json.dumps(values))
            if page.status_code != 200:
                logger.warn('No recuperada la pagina {}'.format(page.status_code))
                raise Exception('No recuperada la pagina {}'.format(page.status_code)) # Don't! If you catch, likely to hide bugs.
            return page.text
        except Exception, e:
            # No lanzamos el log porque luego lo cogemos
            # logger.warn("No hemos conseguido recuperar la reqiest por este metodo:  {}".format(str(e)))
            raise e       
   
