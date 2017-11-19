#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler

# import utiles.utiles as utiles
from handler.data.config.pluginsBuilder import Plugins
from handler.data.config.configBuilder import Config

from exception.AirtrapException import AirtrapException
import conf.constantes as cons


def allConfig(logger=None):
    try:
        # Gestion de configuracion
        config = Config("{0}/conf/config.json".format(cons.basepath), logger)
        logger.debug("Config (method): %s", filter(lambda aname: not aname.startswith('_'), dir(config)))
        
    
        #  Gestion de plugins
        # plugins = Plugins("conf/plugins.json", logger) 
        plugins = Plugins("{0}/conf/plugins.json".format(cons.basepath),logger=logger) # tendiamos que probar
        logger.debug("Plugins (method): %s",  filter(lambda aname: not aname.startswith('_'), dir(plugins)))
    
        
        logger.debug("config: %s",config)
        logger.debug("plugins: %s",plugins)
        return config, plugins
    except AirtrapException as airtrapError:
        raise airtrapError
    
# def checkConfig(logger=None):
#     config, plugins = allConfig(logger)
#     if config.plugins_active is None: 
#         raise AirtrapException("No existe configuracion [config] para plugins activos, revise configuracion ")
#     if plugins.plugins is None:
#         raise AirtrapException("No existe configuracion [plugins] para ese plugin, revise configuracion")
    
#     if utiles.getObject(config.torrent_server, "requirements") is not None:
#         if utiles.getObject(config.torrent_server.requirements, "space_disk") is None: 
#              raise AirtrapException("si existe un requerimiento tiene que existir un limite de espacio")
    
        
#     return config, plugins