#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import imp,sys
import importlib
from datetime import datetime


# from merc.at.service.torrentHandler import TorrentHandlerClass
from hoor.business.jano.service.organizeHandler import Organize
from hoor.business.jano.common.downJano import Down,Plugins, ResponsePlugin,RequestPlugin




class JanoLaucher(object):
 
 
    def organize(self, downpath, delete=False,  dirName=None):
        errors = []
        organize = Organize()
        try:
            if dirName:
                organize.proccess(dirName, "/media/maxtor/mirror", delete) 
            else:
                organize.proccess(downpath, "/media/maxtor/mirror", delete)    
        except Exception as e:
            self.logger.error("Error al organizar")
            errors.extend(["Error al organizar"]) 
        return errors
        
        
 
    def execute(self,downObj, filter=False):
        
        found = [] 
        added = [] 
        errors = []
        
        
        plugs = downObj.plugins 
        if plugs:
            self.logger.info('plugins activos : {0}'.format(len(plugs)))
        else:
            self.logger.error('No tenemos plugins')
            errors.extend(["No tenemos plugins"])
        
        found_serie = [] # Inicializamos por serie
        request = RequestPlugin(title=downObj.nombre, epstart=downObj.ep_start, epend=downObj.ep_end)

        for pg in plugs:
            instance = self.__getInstancesPluginsActive(pg)
            if instance:
                try:
                    found_serie =instance.execute(request, filter=filter) #  Podemos filtrar para tardar menos, pero tendremos menos registros
                    found.extend(found_serie) 
                    self.logger.info("********************* {} ".format(found))
                except Exception, e:
                    self.logger.error("El plugin a fallado {}: {}".format(instance, str(e)))
           

        self.logger.info("Hemos encontrado [[ {} ]] elementos para [[ {} ]] ".format(len(found), downObj.nombre))
       
        return found, errors

    # def __updateSeries(self,serie, lrequest):
        
    #     #Ordenamos el array
    #     lrequest.sort(key=lambda x: x.episode[2:], reverse=False)
        
    #     for request in lrequest:
    #         nextEp = request.episode[:-2] + str(int(request.episode[-2:]) + 1).zfill(2)
    #         self.logger.info("[UPDATE SERIES] {} a {} -- {}".format(serie.nombre, nextEp, datetime.now()))
    #         serie.ultima = datetime.now()
    #         serie.ep_start = nextEp
    #         serie.save()


    # def __launch_transmission(self, urls, cli, conf):
    #     try:
    #         return cli.allAddTorrent(urls,conf)
    #     except Exception as e:
    #         self.logger.error(e)
    #         raise e;



    def __getInstancesPluginsActive(self, plugin):
        # Gestionamos los plugins de la configuracion  
        if plugin.active:
            pActiveFile = "merc.at.plugins.{0}".format(plugin.file)
            self.logger.debug( "Plugin active:{0}:{1} ".format(pActiveFile, plugin.clazz))
        
            klass = getattr(importlib.import_module(pActiveFile), plugin.clazz)
            # Instantiate the class (pass arguments to the constructor, if needed)
            return klass()
        else:
            return None
        
        
        
    ## Constructor
    def __init__(self, logger=None):
        
        if (logger):
            self.logger = logger
        else:
           self.logger = logging.getLogger(__name__)
           
        self.logger2 = logging.getLogger('daily')
        



    
