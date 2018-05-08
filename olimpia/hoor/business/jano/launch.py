#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys,os

# Comunnes
import importlib

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


# BBDD
from hoor.models import Descarga, Ficha, Profile, TorrentServer

from hoor.business.jano.beans.pluginsBeans import RequestPluginBean, ResponsePluginBean, PluginBean
from hoor.business.jano.handler.torrentHandler import TorrentHandlerClass


def handle(fichas):
    logger.debug('Ejecutado comando try para montar un lanzador de todo:')
    logger.debug("fichas {}".format(fichas))
    responseFounds = []
    
    for ficha in fichas:
        profile = Profile.objects.get(user=ficha.author) # Recupermos el perfil
        logger.info("____________________________ Ficha: {} --> {}".format(profile, ficha.nombre))
        try:
            descarga = Descarga.objects.get(ficha=ficha) # Recuperamos las descargas que existan en la ficha
        except Descarga.DoesNotExist:
            descarga = None
        
        logger.debug("Ficha a descarga : {ficha}".format(ficha=ficha))
        logger.debug("Profile  : {profile}".format(profile=profile))
        logger.debug("Descarga  : {descarga} Estado : {estado_descarga}".format(descarga=descarga, estado_descarga=descarga.estado_descarga if descarga else None))
        
        # Si existe descarga lo intentamos
        if descarga and descarga.estado_descarga==True:
            logger.info("Intentamos la descarga de la ficha {}".format(ficha))
            
            logger.debug("Quality (descarga.quality) {quality}".format(quality=descarga.quality))
            logger.debug("ep_start (descarga.ep_start) {ep_start}".format(ep_start=descarga.ep_start))
            logger.debug("ep_end (descarga.ep_end) {ep_end}".format(ep_end=descarga.ep_end))
        
            if descarga.plugins.all():
                logger.debug("Descargas -- Plugins () {plugins}".format(plugins=descarga.plugins.filter(active=True)))
                pluginsActivos = descarga.plugins.all()
            elif profile.plugins.all():
                logger.debug("Profile -- Plugins () {plugins}".format(plugins=profile.plugins.filter(active=True)))
                pluginsActivos = profile.plugins.all()
            else:
                pluginsActivos = None
            logger.debug("Plugins () {plugins}".format(plugins=pluginsActivos))
            
            
            # Recuperamos los plugins activos segun orden (Descarga, perfil)
            instances = []
            for plugin in pluginsActivos:
                pActiveFile = "hoor.business.jano.plugins.{0}".format(plugin.file)
                logger.info( "Plugin active:{0}:{1} ".format(pActiveFile, plugin.clazz))
                klass = getattr(importlib.import_module(pActiveFile), plugin.clazz)
                # Instantiate the class (pass arguments to the constructor, if needed)
                instance = klass()
                instances.append(instance)
            
            # Buscamos la serie
            founds = []
            # Vamos a iterar las series
            serie = RequestPluginBean(title=ficha.nombre,quality=descarga.quality, epstart=descarga.ep_start, epend=descarga.ep_end) # Mappeo
            logger.debug("Nombre de la serie: {} capitulo: {} final: {}".format(serie.title, serie.epstart, serie.epend))
            for instance in instances:
                logger.debug("Plugin: {} ".format(instance))
                founds.extend(instance.execute(serie))
                # OOOOJOOOO     devolver, sin lanzar el torrent, no lo veo
                responseFounds.extend(founds)
            
            
            # Descargamos los torrent
            logger.debug("Profile -- Server {server}".format(server=profile.server))
            server = profile.server
            torrentHandler = TorrentHandlerClass(host=server.host,port=server.port,user=server.user,password=server.password, logger=logger)
            listTorrentResponse = torrentHandler.allAddTorrent([o.data for o in founds],download_dir_path=server.download, space_disk=server.space_disk, paused=server.paused)    
            logger.info("Capitulos descagados : {} ".format(listTorrentResponse)) 
            
            
            
            # Mandar el Mensaje
            logger.info("Mandar el mensaje : {} ".format(founds))                 
                
        else:
            logger.warn("No hay descarga para esta ficha {}".format(ficha))

    return responseFounds