#!/usr/bin/python
import logging
import urllib, urllib2
import re
from logging.handlers import RotatingFileHandler
import bs4
from bs4 import BeautifulSoup

import utilesplugins as utilesplugins

from merc.at.beans.pluginsBeans import RequestPlugin
from merc.at.beans.pluginsBeans import ResponsePlugin

class EpisodiesBeanClass(object):
    
    def __init__(self,epstart=None, epend=None):
        self.epstart=epstart
        self.epend=epend



class DivxtotalHandler(object):
   
   
    # EJECUTOR   
    def execute(self,request, filter=False):
        self.logger.info(" ---> Processando con el plugin .... {0} -- {1}".format(request, filter))

        epstartquality, epstartsession, epstartepisode = utilesplugins.converterEpisode(request.epstart)
        ependquality, ependsession, ependepisode = utilesplugins.converterEpisode(request.epend)
        
        nombreserie=request.title
        quality=epstartquality if epstartquality else ependquality
        episodes=EpisodiesBeanClass(epstart=request.epstart, epend=request.epend)
        enlaces=[] # Respuesta
        
        # Recuperamos la pagina de busqueda
        url = 'http://www.divxtotal2.net/?s={nombreserie}'.format(nombreserie=nombreserie)
        page = urllib2.urlopen(url).read()
        
        self.logger.info("page : {}".format(page))
        
        # # Parse pagina principal
        source = BeautifulSoup(page, "html.parser")
        buscar_list = source.find_all("table", {"class" : "table"})
    
        self.logger.info("buscar_list : {}".format(buscar_list))

        return enlaces


    ## Constructor
    def __init__(self, logger=None):
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
    



if __name__ == '__main__':
    
    dthandler = DivxtotalHandler()
    request = RequestPlugin(title='The BlackList', epstart='HDS05E00', epend='HDS99E99')
    dthandler.execute(request,filter=False)