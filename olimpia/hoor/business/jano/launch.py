#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import importlib

# Get an instance of a logger
logger = logging.getLogger(__name__)

from hoor.business.jano.common.downJano import Down, Plugins


# n Series
# u Author
# u Torrent


class SearchLaunch:
 
    pathPlugin = "hoor.business.jano.plugins." 
    
    def execute(self, downs):
        
        for down in downs:
            logger.info("downObject : {down}".format(down=down))
            plugins = down.plugins
            for plugin in plugins:
                logger.info("downObject({down}).plugins : {plugin}".format(down=down,plugin=plugin))
                #  Podemos filtrar para tardar menos, pero tendremos menos registros
                if plugin.active:
                    instance = self.__getInstancePlugin(plugin)
                    found_serie = instance.execute(down, filter=filter) 
                    print "EXACTO {}".format(found_serie)
        
        return None;
        
        
        
    def __getInstancePlugin(self, plugin):
        # Gestionamos los plugins de la configuracion  
        pActiveFile = "{pathPlugin}{filePlugin}".format(pathPlugin=self.pathPlugin,filePlugin=plugin.file)
        logger.debug( "Plugin active: from {0} import {1} ".format(pActiveFile, plugin.clazz))
        klass = getattr(importlib.import_module(pActiveFile), plugin.clazz)
        # Instantiate the class (pass arguments to the constructor, if needed)
        instance = klass()
        return instance  




