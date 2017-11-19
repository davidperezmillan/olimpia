#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler

import utilities.utiles as utiles
from exception.AirtrapException import AirtrapException
import utilities.constantes as cons

basepathlog = cons.basepathlog
loggername = 'configbuilder'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
loggerfilename = basepathlog+loggername+'.log'

url = "{0}/conf/config.json".format(cons.basepath)

class Config(object):

   
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
            
        try:    
            templateObject = utiles.getObjectToJson(url)
            self.call_templates(templateObject, self.logger)
            
            self.torrent_server, self.space_disk = self.call_torrent_server(self.logger)
            self.plugins_active= self.call_plugins_active(self.logger)
            self.telegram_client = self.call_telegram_client(self.logger)
            self.organize_service = self.call_organize_service(self.logger)
        except AirtrapException as airtrapError:
            raise airtrapError
    
    
    def call_templates(self, templateObject, logger=None):
        self.templates = utiles.getObject(templateObject,"templates")
    
    def call_torrent_server(self, logger= None):
        
        # Parametros que tiene que salir 
        torrent_server=None
        space_disk=None
        
        ## aqui vamos a comprobar la configuracion del templates torrent_server
        
        torrent_server = utiles.getObject(self.templates, "torrent_server")
        if torrent_server is None:
           torrent_server=None 
        else:
            # Si torrent_active es falso todo la etiqueta es None
            torrent_active = utiles.getObject(torrent_server, "torrent_active")
            if torrent_active is None or torrent_active is False:
                torrent_server = None
            
        # si existe un requerimiento debe existir un .space_disk 
        if utiles.getObject(torrent_server, "requirements") is not None:
            space_disk = utiles.getObject(torrent_server.requirements, "space_disk")
            if space_disk is None:
                raise AirtrapException("si existe un requerimiento tiene que existir un limite de espacio")
        
        if torrent_server:
            transmission = utiles.getObject(torrent_server, "transmission")
            if transmission is None:
                raise AirtrapException("No existe configuracion para [transmission], revise configuracion")
            if utiles.getObject(transmission, "host") is None:
                transmission.host="localhost" ## Lo ponemos por defecto
                # raise AirtrapException("No existe configuracion para [host], revise configuracion")
            if utiles.getObject(transmission, "port") is None:
                transmission.port="9091" ## Lo ponemos por defecto
                # raise AirtrapException("No existe configuracion para [port], revise configuracion")
            if utiles.getObject(transmission, "user") is None:
                raise AirtrapException("No existe configuracion para [user], revise configuracion")
            if utiles.getObject(transmission, "password") is None:
                raise AirtrapException("No existe configuracion para [password], revise configuracion")

        return torrent_server, space_disk

    
    def call_plugins_active(self, logger = None): 
        plugins_active = utiles.getObject(self.templates,"plugins_active")
        if plugins_active is None: 
            raise AirtrapException("No existe configuracion [config] para plugins activos, revise configuracion ")
            
        return plugins_active
  
    
    def call_telegram_client(self, logger= None):
  
        # Parametros que tiene que salir 
        telegram_client=None
        
        
         ## aqui vamos a comprobar la configuracion del templates torrent_server
        
        telegram_client = utiles.getObject(self.templates, "telegram_client")
        if telegram_client is None:
           telegram_client=None 
        else:
            # Si telegram_active es falso todo la etiqueta es None
            telegram_active = utiles.getObject(telegram_client, "telegram_active")
            if telegram_active is None or telegram_active is False:
                telegram_client = None
            
        if telegram_client:
            token = utiles.getObject(telegram_client, "token")
            if token is None:
                raise AirtrapException("No existe configuracion para [token], revise configuracion")
            recipients = utiles.getObject(telegram_client, "recipients")
            if recipients is None:
                raise AirtrapException("No existe configuracion para [recipients], revise configuracion")
            if utiles.getObject(recipients, "fullnames") is None:
                recipients.fullnames=None
            else:
                respuesta=[]
                for arr in utiles.getObject(recipients, "fullnames"):
                    tarr = tuple(arr)
                    respuesta.append(tarr) 
                recipients.fullnames=respuesta
            if utiles.getObject(recipients, "usernames") is None:
                recipients.usernames=None
            if utiles.getObject(recipients, "globals") is None:
                recipients.globals=None              
                
        return telegram_client

    def call_organize_service(self,logger = None):
        
        organize_service= None
        
        organize_service = utiles.getObject(self.templates, "organize_service")
        if organize_service is None:
            return None
        # Si torrent_active es falso todo la etiqueta es None
        organize_active = utiles.getObject(organize_service, "organize_active")
        if organize_active is None or organize_active is False:
            return None
        # mirror_path
        mirror_path = utiles.getObject(organize_service,"mirror_path")
        if mirror_path is None:
            raise AirtrapException("No existe configuracion para [mirror_path], revise configuracion")
        # data_path
        data_path = utiles.getObject(organize_service,"data_path")
        if data_path is None:
            raise AirtrapException("No existe configuracion para [data_path], revise configuracion")
        
        return organize_service
        
        
        
if __name__ == '__main__':
    
    config = Config("conf/config.json")
    print config.templates
    print config.plugins_active
    print config.torrent_server        