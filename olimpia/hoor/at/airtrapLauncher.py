#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import imp,sys
import importlib
from datetime import datetime


from merc.models import Series, TorrentServers, Plugins

from merc.at.beans.pluginsBeans import RequestPlugin
from merc.at.beans.pluginsBeans import ResponsePlugin
from merc.at.service.torrentHandler import TorrentHandlerClass
from merc.at.service.organizeHandler import Organize




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
 
 
    def organize(self, delete=False):
        errors = []
        organize = Organize()
        for clnt in self.clients:
            try:
                organize.proccess(clnt.conf.download, "/media/maxtor/mirror", delete)    
            except Exception as e:
                self.logger.error("Error al organizar")
                errors.extend(["Error al organizar"]) 
        
        return errors
 
    def execute(self,series_update, filter=False):
        
        found = [] 
        added = [] 
        errors = []
        
        for clnt in self.clients:
            self.logger.info('conf_clnt: {0}'.format(clnt.conf))
            plugs = clnt.plugins 
            
            if plugs:
                self.logger.info('plugins: {0}'.format(len(plugs)))
            else:
                self.logger.error('No tenemos plugins')
                errors.extend(["No tenemos plugins"])
            
            for serie in series_update:
                found_serie = [] # Inicializamos por serie
                added_serie = [] # Inicializamos por serie
                request = RequestPlugin(title=serie.nombre, epstart=serie.ep_start, epend=serie.ep_end)

                for instance in plugs:
                    found_serie =instance.execute(request, filter=filter) #  Podemos filtrar para tardar menos, pero tendremos menos registros
                    found.extend(found_serie) 
                   
    
                self.logger.info("Hemos encontrado [[ {} ]] para [[ {} ]] elementos para descargar".format(len(found), serie.nombre))
                if found_serie:
                    try:
                        added_serie = self.__launch_transmission(found_serie,clnt.client, clnt.conf)
                        added.extend(added_serie)
                        self.logger2.info("{} {}".format(serie,found_serie))
                        self.__updateSeries(serie, found_serie)
                    except Exception as e:
                        self.logger.error("No hay o no esta activado el cliente para torrent")
                        errors.extend(["No hay o no esta activado el cliente para torrent"])           
                    # try:
                    #   pass
                    # except Exception as e:
                    #     self.logger.exception("message")("No se ha updateado la serie")
                    #     errors.extend(["No se ha updateado la serie {}".format(serie.nombre)])   
                
        
        return found, added, errors

    def __updateSeries(self,serie, lrequest):
        
        #Ordenamos el array
        lrequest.sort(key=lambda x: x.episode[2:], reverse=False)
        
        for request in lrequest:
            nextEp = request.episode[:-2] + str(int(request.episode[-2:]) + 1).zfill(2)
            self.logger.info("[UPDATE SERIES] {} a {} -- {}".format(serie.nombre, nextEp, datetime.now()))
            serie.ultima = datetime.now()
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
           
        self.logger2 = logging.getLogger('daily')
        
        self.clients = self.__getClientTorrents(torrentservers)
        self.logger.debug("Clientes torrent seleccionados : {0}".format(self.clients));



    