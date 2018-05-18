#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys,os
import datetime

# Comunnes
import importlib

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


# BBDD
from hoor.models import Descarga, Ficha, Profile, TorrentServer, TelegramChatIds

from hoor.business.jano.beans.pluginsBeans import RequestPluginBean, ResponsePluginBean, PluginBean
from hoor.business.jano.handler.torrentHandler import TorrentHandlerClass
from hoor.business.jano.handler.telegramHandler import TelegramNotifier, ReceiverTelegram


def handle(fichas):
    logger.debug('Ejecutado comando try para montar un lanzador de todo:')
    logger.debug("fichas {}".format(fichas))
    responseFounds = []
    responseTorrent = []
    profile=None
    
    
    for ficha in fichas:
        profileficha = Profile.objects.get(user=ficha.author) # Recupermos el perfil
        logger.debug("Profile para la ficha: {}".format(profileficha))
        if profile is None or profileficha!=profile:
            if profile is None or profile.server != profileficha.server:
                logger.info("Cambiamos de profile: {} --> {}".format(profile.server if profile else "", profileficha.server))
                # Vamos a cargar un cliente para todos los torrent
                # intentando que ganermos algo de rendimiento
                profile = profileficha
                server = profile.server
                torrentHandler = TorrentHandlerClass(host=server.host,port=server.port,user=server.user,password=server.password, logger=logger)
        else:
            logger.debug("Mantenemos el profile: {}".format(profile))

        
        try:
            descarga = Descarga.objects.get(ficha=ficha) # Recuperamos las descargas que existan en la ficha
        except Descarga.DoesNotExist:
            descarga = None
        
        logger.info("{}                                         **** Ficha a descarga **** : {ficha}".format(profile, ficha=ficha))
        logger.info("Descarga  : {descarga} Estado : {estado_descarga}".format(descarga=descarga, estado_descarga=descarga.estado_descarga if descarga else None))
        
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
                try:
                    pActiveFile = "hoor.business.jano.plugins.{0}".format(plugin.file)
                    logger.info( "Plugin active:{0}:{1} ".format(pActiveFile, plugin.clazz))
                    klass = getattr(importlib.import_module(pActiveFile), plugin.clazz)
                    # Instantiate the class (pass arguments to the constructor, if needed)
                    instance = klass()
                    instances.append(instance)
                except Exception, e:
                    logger.error("Se ha producido un error {}:{}".format(instance, e),exc_info=True)
            
            # Buscamos la serie
            founds = []
            # Vamos a iterar las series
            serie = RequestPluginBean(title=ficha.nombre,quality=descarga.quality, epstart=descarga.ep_start, epend=descarga.ep_end) # Mappeo
            logger.debug("Nombre de la serie: {} capitulo: {} final: {}".format(serie.title, serie.epstart, serie.epend))
            for instance in instances:
                try:
                    logger.debug("Plugin: {} ".format(instance))
                    founds.extend(instance.execute(serie))
                except Exception, e:
                    logger.error("Se ha producido un buscando la serie {} = {}:{}".format(instance, e, ficha.nombre),exc_info=True)
            
            # Lo que hemos encontrado
            responseFounds.extend(founds)
                
            founds.sort(key=lambda x: x.data.episode[2:], reverse=False) # Ordenamos los objetos encontrados, para transmission, telegram y BBDD
            for found in founds:
                # Descargamos los torrent
                logger.debug("Profile -- Server {server}".format(server=profile.server))
                server = profile.server
                if server:
                    try:
                        torrentResponse = torrentHandler.allAddTorrent([found.data],download_dir_path=server.download, space_disk=server.space_disk, paused=server.paused)    
                        if torrentResponse:
                            logger.info("Capitulos descagados : {} en descarga {} ".format(found.data.episode, descarga)) 
                            # Update
                            # # # Buscamos el siguiente capitulo
                            nextEp = None
                            nextEp = found.data.episode[:-2] + str(int(found.data.episode[-2:]) + 1).zfill(2)
                            descarga.ep_start = nextEp
                            descarga.save()
                            responseTorrent.append(found)
                    except Exception, e:
                        logger.error("Se ha producido un error al poner  {}:{}".format(instance, e),exc_info=True)
        else:
            logger.warn("No hay descarga para esta ficha {}".format(ficha))


    # Construimos la respuesta
    valuesFounds = ','.join("\n\r{} [{}]".format(str(v.data.title),str(v.data.episode)) for v in responseFounds)
    logger.debug("Encontrados : {}".format(valuesFounds))
    # valuesTorrent = ','.join("{}".format(str(v) for v in responseTorrent))
    logger.debug("Torrents : {}".format(responseTorrent))
    
    # Creamos el mensaje
    header = "Hemos lanzado el proceso {} de {}".format(datetime.datetime.now(), ficha.nombre)
    body = "\n\rHemos encontrado {} \n\rHemos grabado {}".format(valuesFounds,len(responseTorrent))
    msg ="{} {}".format(header, body)
    
    
    if profile.telegramCli is not None:
        
        logger.info("Tenemos receptores del mensaje {}".format(profile.telegramCli.all()))
        for receiver in profile.telegramCli.all():
            rec = utilgetreceivers(receiver)
            # Mandamos el mensaje
            logger.info("Rec: {}".format(rec))
            clazz = TelegramNotifier(token = '135486382:AAFb4fhTGDfy42FzO77HAoxPD6F0PLBGx2Y')
            grabars = clazz.notify(msg, receivers=rec) 
            for grabar in grabars:
                logger.info("Tendremos que grabar: {}".format(grabar))
                receiver.idtelegram = grabar.id
                receiver.save()
            
    return responseTorrent, responseFounds
    
    
    
def utilgetreceivers(rec):
    usernames=[]
    fullnames=[]
    groups=[]
    if rec.firstname:
        fullnames.append((rec.firstname,rec.surname))
    if rec.username:
        usernames.append(rec.username)
    if rec.group:
        groups.append(rec.group)    
    logger.info("{fullnames}{groups}{usernames}".format(fullnames=fullnames, groups=groups, usernames=usernames))
    return ReceiverTelegram(fullnames=fullnames, groups=groups, usernames=usernames)
    