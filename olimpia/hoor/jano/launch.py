#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



# n Series
# u Author
# u Torrent



class SearchLaunch:
    
    def __str__(self):
        x=[]
        if self.down:
            x.append('down={0}'.format(self.down))
        if self.plugins:
            x.append('plugins={0}'.format(self.plugins))
        return ' '.join(x)
    
    def __init__(self, down, plugins):
        self.down = down
        self.plugins = plugins
    
    
    
    
    def execute(self, descargas, profile=None):
        
        logger.debug("Estos en el Launch ")
        logger.debug("Fichas {}".format(descargas))
        logger.debug("Author {}".format(profile))
        
        for descarga in descargas:
            
            logger.debug("[Dentro del for] Serie {}".format(descarga))

            # El orden para recuperar los plugins
            # 
            # Series
            # Plugins
            # torrent
            # 
            
            if descarga.plugins and descarga.plugins.all():
                plugins_active = descarga.plugins.all()
                logger.info("Recuperamos los plugins de la descarga {}".format(plugins_active))
            elif profile.plugins and profile.plugins.all():
                plugins_active = profile.plugins.all()
                logger.info("Recuperamos los plugins del profile {}".format(plugins_active))
            else:
                raise Exception
                
           
            
            
        return None;