#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import imp,sys
import importlib

from merc.models import Series, TorrentServers, Plugins

from merc.at.beans.pluginsBeans import RequestPlugin
from merc.at.beans.pluginsBeans import ResponsePlugin
from merc.at.service.torrentHandler import TorrentHandlerClass




class ClientTorrents():
    
    def __str__(self):
        x=[]
        if self.conf:
            x.append('conf={0}'.format(self.conf))
        if self.client:
            x.append('client={0}'.format(self.client))
        if self.plugins:
            x.append('plugins={0}'.format(self.plugins))
        return ' '.join(x)
    
    def __init__(self, conf,client, plugins):
        self.client = client
        self.conf = conf
        self.plugins = plugins

class AirTrapLauncher(object):
 
    def execute(self,series_update):
        
        found = []
        added = []
        errors = []
        
        for clnt in self.clients:
            plugs = clnt.plugins 
            
            if plugs:
                self.logger.info('plugins: {0}'.format(len(plugs)))
            else:
                self.logger.error('No tenemos plugins')
                errors.extend(["No tenemos plugins"])
            
            for serie in series_update:
                request = RequestPlugin(title=serie.nombre, epstart=serie.ep_start, epend=serie.ep_end)

                for instance in plugs:
                    found_serie =instance.execute(request, filter=True) 
                    found.extend(found_serie) # filtramos para tardar menos
                   
    
                self.logger.info("Hemos encontrado [[ {} ]] elementos para descargar".format(len(found)))
                if found:
                    try:
                        added.extend(self.__launch_transmission(found,clnt.client, clnt.conf))
                        self.__updateSeries(serie, found_serie)
                    except Exception as e:
                        self.logger.error("No hay o no esta activado el cliente para torrent")
                        errors.extend(["No hay o no esta activado el cliente para torrent"])           
            
                
        
        return found, added, errors

    def __updateSeries(self,serie, lrequest):
        
        #Ordenamos el array
        lrequest.sort(key=lambda x: x.episode[2:], reverse=False)
        
        for request in lrequest:
            
            nextEp = request.episode[:-2] + str(int(request.episode[-2:]) + 1).zfill(2)
            serie.ep_start = nextEp
            serie.save()


    def __launch_transmission(self, urls, cli, conf):
        try:
            return cli.allAddTorrent(urls,conf)
        except Exception as e:
            self.logger.error(e)
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
                conf = torrentserver # Datos recuperados de la base de datos (incluye plugins)
                plg = torrentserver.plugins.all() # recuperamos los plugins
                plg_active = self.__getInstancesPluginsActive(plg) # instanciamos los plugins
                cln = TorrentHandlerClass(torrentserver) # instanciamos el cliente
                # add to list
                clients_trans.append(ClientTorrents(conf=conf, client=cln, plugins=plg_active))
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
        self.logger.debug("Clientes torrent seleccionados : {0}".format(self.clients));



    
