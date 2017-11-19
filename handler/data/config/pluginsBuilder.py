#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler

import utilities.utiles as utiles
import conf.constantes as cons

basepathlog = cons.basepathlog
loggername = 'pluginsBuilder'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
loggerfilename = basepathlog+loggername+'.log'

url = "{0}/conf/plugins.json".format(cons.basepath)

class Plugins(object):

   
     ## Constructor
    def __init__(self, url = url, logger= None, test=False):
        

        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(loggername)
            self.logger.setLevel(logging.DEBUG)
            self.formatter = logging.Formatter(defaulformatter)
        
            # self.handler = logging.FileHandler(self.mcbconstants.basepathlog+"mycrybotdaemon.out")
            self.handler = RotatingFileHandler(loggerfilename, maxBytes=2000, backupCount=3)
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)
            
            self.ch = logging.StreamHandler()
            self.ch.setFormatter(self.formatter)        
            self.logger.addHandler(self.ch)
    
        pluginsObject = utiles.getObjectToJson(url)
        self.call_plugins(pluginsObject, self.logger)
    
    
    def call_plugins(self, pluginsObject, logger=None):
        self.pathtolib = utiles.getObject(pluginsObject,"pathtolib")
        self.plugins = utiles.getObject(pluginsObject,"plugins")
    
    
if __name__ == '__main__':
    
    plugins = Plugins()
    print plugins.pathtolib
    print plugins.plugins