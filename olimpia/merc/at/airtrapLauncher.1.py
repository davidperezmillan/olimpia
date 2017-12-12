#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import imp,sys
import importlib

from merc.models import Series, TorrentServers, Plugins

from merc.at.beans.pluginsBeans import RequestPlugin
from merc.at.beans.pluginsBeans import ResponsePlugin
from merc.at.service.torrentHandler import TorrentHandlerClass



class AirTrapLauncher(object):
 
 
    
 
 
 
    def all(self,series_update):
        for serie in series_update:
            self.logger.info("Buscamos y descargamos : {0} - {1}".format(serie.nombre, serie.quality))
            self.unique(serie)
    
    
    def unique(self, serie):
        if self.clients:
            self.logger.info("Vamos a lanzar busqueda sobre [[ {0} ]] en {1} servidores".format(serie.nombre, len(self.clients)))
        
        pos = 0
        while (pos < len(self.clients)):
            trans = self.clients[pos][1]
            torrentserver = self.clients[pos][0]
            plugins = torrentserver.plugins.all()
            pluginsInstances = self.__getInstancesPluginsActive(plugins)
            
            if pluginsInstances:
                self.logger.info('plugins: {0}'.format(len(pluginsInstances)))
            else:
                self.logger.error('No tenemos plugins')
                raise Exception('No tenemos plugins activados para este servidor')
                

            request = RequestPlugin(title=serie.nombre, epstart=serie.ep_start, epend=serie.ep_end)
            lTorrents = []
            for instance in pluginsInstances:
                lTorrents.extend(instance.execute(request, filter=True)) # filtramos para tardar menos
    
            self.logger.info("Hemos recuperado [[ {} ]]".format(len(lTorrents)))
            if lTorrents:
                try:
                    return self.__launch_transmission(lTorrents,trans, torrentserver)
                except Exception as e:
                    self.logger.error(e)
                    raise e
            pos = pos + 1        
        return None
        




    def __launch_transmission(self, urls, trans, torrentserver):
        try:
            trans.allAddTorrent(urls,torrentserver)
        except Exception as e:
            raise e;



    def __getInstancesPluginsActive(self, plugins):
        # Gestionamos los plugins de la configuracion  
        instances = []
        for plugin in plugins:
            if plugin.active:
                pActiveFile = "merc.at.plugins.{0}".format(plugin.file)
                self.logger.debug( "Plugin active:{0}:{1} ".format(pActiveFile, plugin.clazz))
            
                klass = getattr(importlib.import_module(pActiveFile), plugin.clazz)
                # Instantiate the class (pass arguments to the constructor, if needed)
                instance = klass()
                instances.append(instance)
         
        return instances  
        
        
        
    def __getClientTorrents(self, torrentservers):
        clients_trans = []
        for torrentserver in torrentservers:
            try:
                clients_trans.append([torrentserver,TorrentHandlerClass(torrentserver)])
            except Exception, e:
                self.logger.warn(e)
        self.logger.debug(clients_trans) 
        return clients_trans
        

    ## Constructor
    def __init__(self, torrentservers, logger=None):
        
        if (logger):
            self.logger = logger
        else:
           self.logger = logging.getLogger(__name__)
        
        
        self.clients = self.__getClientTorrents(torrentservers)



    
