#!/usr/bin/python
import logging
from logging.handlers import RotatingFileHandler


loggername = 'Series_TorrentHandlerClass'
loggerfilename = loggername+'.log'
stdfilename = loggername+'.std'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"



class Series_torrentsHandlerClass(object):
   
    
    def execute(self, titulo, titles):
        self.logger.info(" ---> Processando con el plugin ....")

        return {}





  ## Constructor
    def __init__(self, logger= None):
        
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(loggername)
            self.logger.setLevel(logging.DEBUG)
            self.formatter = logging.Formatter(defaulformatter)
        
            self.handler = RotatingFileHandler(loggerfilename, maxBytes=2000, backupCount=3)
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)
            
            self.ch = logging.StreamHandler()
            self.ch.setFormatter(self.formatter)        
            self.logger.addHandler(self.ch)
    
