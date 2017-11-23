#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from handler.classHandlerGeneric import ClassHandlerGeneric # Herencia

import importlib
import logging
from logging.handlers import RotatingFileHandler

## DATA
import handler.data.config.builderUtils as builderUtils # Recuperamos config y plugins
import handler.data.dataHandler as dataHandler # Recuperamos datos para buscar

## Services
from handler.services.torrentHandler import TorrentHandlerClass
from handler.services.telegramHandler import TelegramNotifier, ConfigTelegramBean

# Custom Exception 
from exception.AirtrapException import AirtrapException

import utilities.constantes as cons
from handler.organizeHandler import Organize


basepathlog = cons.basepathlog
loggername = 'airtrapHandler'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
loggerfilename = basepathlog+loggername+'.log'

# Data esta en local

class AirTrapHandlerClass(object):
    
    
    def unique(self, args):
        try:
            lrequest = dataHandler.convertArgsBean(args) 
            lresponse, config = self.__execute(lrequest, test=args.test) 
            self.__organize(lresponse, config)
            self.__getServiceData(lresponse, test=args.test)
            self.__getServiceTelegram(lresponse, config, test=args.test)
        except AirtrapException, airError:
            raise airError
   
    def film(self, args):
        try:
            self.logger.info("Buscamos la pelicula {0}".format(args.film))
            lrequest = dataHandler.convertArgsBeanFilm(args) 
            lresponse, config = self.__execute(modo='film', lrequest=lrequest, test=args.test) 
            
            # self.__getServiceData(lresponse) ### Por ahora no modificamos la Base de datos
            self.__getServiceTelegram(lresponse, config,test=args.test)
        except AirtrapException, airError:
            raise airError
   
    
    def execute(self, args):
        try:
            lrequest = dataHandler.getdatabase(self.logger) 
            lresponse, config = self.__execute(lrequest, modo="serie", test=args.test)  
            self.__organize(lresponse, config)
            self.__getServiceData(lresponse,test=args.test)
            self.__getServiceTelegram(lresponse, config,test=args.test)
        except AirtrapException, airError:
            raise airError
    
    
    
    def test(self, args):
        try:
            lrequest = []
            lresponse, config = self.__execute(lrequest)    
            self.__getServiceTelegram(lresponse, config)
        except AirtrapException, airError:
            raise airError
    
    
    def __organize(self,lresponse, config):
        # if not lresponse:
        #     self.logger.warn("No organizamos nada")
        #     return
        if config.organize_service is None: # comprobamos que en la configuracion quieren organizar los enlaces
            self.logger.warn(AirtrapException("No existe o esta desactivada la configuracion para el servicio [organize], revise configuracion"))
            return 
        # Recuperamos los datos
        urlData = config.organize_service.data_path
        urlMirror = config.organize_service.mirror_path
        self.logger.info("CALL to organize({0},{1})".format(urlData, urlMirror))
        #organize = Organize(self.logger)
	organize = Organize()
        organize.proccess(urlData,urlMirror,False)
        
    
    def __execute(self, lrequest,  modo='serie', test=False):
        lresponse = []
        # ###### DATA
        # Recuperamos datos de configuracion
        config, plugins = builderUtils.allConfig(logger=self.logger)
        # recuperamos las instancias activas
        instances = self.__getPluginsActive(config, plugins)
        for instance in instances:
            lInstanceResponse = self.__getServiceTorrent(config=config, lrequest=lrequest,instance = instance, modo=modo, test=test) 
            lresponse.extend(lInstanceResponse)
            
        return lresponse, config
  
    def __getPluginsActive(self, config,plugins):
        # Gestionamos los plugins de la configuracion  
        instances = []
        for sActive in config.plugins_active:
            self.logger.debug("Recuperamos la configuracion del plugin %s", sActive)
            try:
                pActive = getattr(plugins.plugins, sActive) 
            except AttributeError:
                self.logger.error(AirtrapException("No existe configuracion para ese plugin[{0}], revise configuracion".format(sActive)).message)
                continue
            pActiveFile = "handler.plugins.{0}".format(pActive.file)
            self.logger.debug( "Plugin active:{0}:{1} ".format(pActiveFile, pActive.clazz))
        
            klass = getattr(importlib.import_module(pActiveFile), pActive.clazz)
            # Instantiate the class (pass arguments to the constructor, if needed)
            instance = klass(display=self.logger.getEffectiveLevel())
            instances.append(instance)
    
        return instances
        
    def __getServiceTorrent(self, config, lrequest, instance, modo, test=False):
        lResponse = []
        
        self.logger.info("test {}".format(test))
        
        if test is False:
            # vamos a generar un cliente torrent para toda la "sesion"
            if config.torrent_server is None: # el plugin siempre esta activo
                self.logger.warn(AirtrapException("No existe o esta desactivada la configuracion Transmission, revise configuracion"))
            else:
                clientTorrent = TorrentHandlerClass(config, self.logger)
        
        
        for request in lrequest:
            self.logger.info("Buscamos %s para %s - %s", request.title, request.epstart, request.epend)
            ## por titulo enviamos un execute a la instancia
            if modo=='serie':
                listResponse = instance.execute(request, filter=True) # filtramos para tardar menos
                #listResponse = instance.execute(request, filter=False)
            elif modo=='film':
                listResponse = instance.execute_film(request, filter=True)
        
            self.logger.info("{0} enlaces de {1}".format(len(listResponse),(request)))
        
            if test is False:
                self.logger.debug("Vamos a lanzar %d torrent de la serie: %s", len(listResponse), request.title)
                if config.torrent_server is None: # el plugin siempre esta activo
                    self.logger.warn(AirtrapException("No existe o esta desactivada la configuracion Transmission, revise configuracion"))
                else:
                    self.logger.debug("Torrent server active [OK data] ")
                    listTorrentResponse = clientTorrent.allAddTorrent(listResponse,config, modo=modo)
                    lResponse.extend(listTorrentResponse)
        
        return lResponse
    
    
    '''
    def __getServiceTorrent_film(self, config, lrequest, instance, test=False):
        lResponse = []
        
        if test is False:
            # vamos a generar un cliente torrent para toda la "sesion"
            if config.torrent_server is None: # el plugin siempre esta activo
                self.logger.warn(AirtrapException("No existe o esta desactivada la configuracion Transmission, revise configuracion"))
            else:
                clientTorrent = TorrentHandlerClass(config, self.logger)
        
        for request in lrequest:
            self.logger.debug("Buscamos %s para %s - %s", request.title, request.epstart, request.epend)
            ## por titulo enviamos un execute a la instancia
            listResponse = instance.execute_film(request, filter=True)
            
            self.logger.debug("Vamos a lanzar %d torrent de la serie: %s", len(listResponse), request.title)
            if config.torrent_server is None: # el plugin siempre esta activo
                self.logger.warn(AirtrapException("No existe o esta desactivada la configuracion Transmission, revise configuracion"))
            else:
                self.logger.debug("Torrent server active [OK data] ")
                listTorrentResponse = clientTorrent.allAddTorrent(listResponse,config)
                lResponse.extend(listTorrentResponse)
        
        return lResponse
    '''
    
        
    def __getServiceData(self,lrequest, test=False):
        
        if test: # en modo test no se graba nada en la base de datos
            return 
        
        self.logger.debug("Vamos a modificar %s registros de la base de datos: %s", len(lrequest), lrequest)
        from handler.data.databaseairtrap import DatabaseAirTrap
        database=DatabaseAirTrap(logger=self.logger)
        
        #Ordenamos el array
        lrequest.sort(key=lambda x: x.episode[2:], reverse=False)
        
        for request in lrequest:
            
            nextEp = request.episode[:-2] + str(int(request.episode[-2:]) + 1).zfill(2)
            
            self.logger.debug("Vamos modificar la base de datos %s", request)
            resp = database.update(request.title, nextEp)
            if resp>0:
                self.logger.info("%s Filas afectadas en [UPDATE] ",resp )
            else:
                resp = database.insert(request.title, nextEp)
                self.logger.info("%s Filas afectadas en [INSERT] ",resp )
    
    
    def __getServiceTelegram(self, lrequest, config, test=False):
        
        if test: # en modo test no se graba nada en la base de datos
            return 
        
        token = config.telegram_client.token
        fullnames = config.telegram_client.recipients.fullnames or None
        usernames = config.telegram_client.recipients.usernames or None
        groups = config.telegram_client.recipients.globals or None
        
        if lrequest:
            sRequest = "{1} 'La trampa del Aire' ha puesto en cola {0} torrent para su descargas :   \n\r".format(len(lrequest), "[TEST]" if test else "")
            sFinal = "\n\rEspero que lo disfruteis, Gracias por utilizar 'La Trampa del Aire'"
            sitems = ""
            for item in lrequest:
                sitems = "{0} -- {1} [{2}].  \n\r".format(sitems,item.title, item.episode) 
            sRequest = "{0}{1}{2}".format(sRequest,sitems, sFinal)
        else:
            sRequest = 'Que pena no tenemos nada que enviar .....'
       
        clazzTelegram = TelegramNotifier(logger=self.logger)
        config = ConfigTelegramBean(token = token, fullnames = fullnames, usernames=usernames, groups = groups)
        clazzTelegram.notify(sRequest, config) 
    
    ## Constructor
    def __init__(self, logger= None):
        
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
