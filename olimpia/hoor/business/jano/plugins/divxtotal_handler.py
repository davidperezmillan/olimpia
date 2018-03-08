#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from hoor.business.jano.common.downJano import Down, Plugins


# import urllib, urllib2
# import re
# from logging.handlers import RotatingFileHandler
# import bs4
# from bs4 import BeautifulSoup








class DivxtotalHandlerClass(object):
   
   
   def execute(self,down, filter=False):
      
      logger.debug("nombre : {down}".format(down=down.nombre))
      logger.debug("calidad : {down}".format(down=down.quality))
      logger.debug("comienzo : {down}".format(down=down.ep_start))
      logger.debug("final : {down}".format(down=down.ep_end))
       
      
   
   