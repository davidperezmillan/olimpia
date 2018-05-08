#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import transmissionrpc
import logging

# Get an instance of a logger
# Incializamos en el init de la clase
logger = logging.getLogger(__name__)


class TorrentHandlerClass(object):
    
    
    def getClientTorrent(self, host, port, user, password):
            logging.getLogger('transmissionrpc').setLevel(self.logger.getEffectiveLevel())
            # formatter = logging.Formatter(defaulformatter)
            # ch = logging.StreamHandler()
            # ch.setFormatter(formatter)        
            for hand in logger.handlers:
                logging.getLogger('transmissionrpc').addHandler(hand)

            logger.info("Intentando conectar con : {0}{1}{2}{3}".format(host,port,user,password))
            client = transmissionrpc.Client(host, port=port, user=user, password=password)
            logger.debug("download_dir {0}".format(client.get_session().download_dir))
            return client
    
    
    
    
    
    def allAddTorrent(self,urls,download_dir_path=None, space_disk=None, paused=False):
        disponible = True
        if space_disk:
            logger.debug("Calculamos el espacio que tenemos [%s]", space_disk)
            if download_dir_path: 
                logger.warn("No hay download_dir_path, se descargara en el directorio por defecto")
                download_dir_path = self.client.get_session("download_dir")
            if space_disk >= self.client.free_space(download_dir_path):
                    disponible = False
        else:
            self.logger.debug("Skip el espacio que tenemos")
            
        if disponible:
            # Gestion de opciones
            options = {}
            options['paused']=paused
            try: 
                listTorrentResponse = []
                for url in urls:
                    logger.debug("Enviando con : {} : {} : {}".format(url.title,url.episode, download_dir_path))
                    try:
                        quality = url.episode[:2] or None
                        session = ("Session {0}".format(str(int(url.episode[3:5])).zfill(1)))
                        q = "_{0}".format(quality) if quality and quality=='VO' else ""
                        titulo = "{0}{1}".format(url.title,q)
                        options["download_dir"] = "{0}/{1}/{2}".format(download_dir_path, titulo, session)
                    except Exception, e:
                        logger.error("No hay download_dir_path, se descargara en el directorio por defecto: {1}".format(e))
                    
                    logger.debug("Intentando descargar: %s:%s con la opciones: %s", url.title, url.episode, options)
                
                    self.logger.info("[GTorrent] Elegimos Torrent {} o link {}".format(url.torrent, url.link))
                    if url.link:
                        self.logger.info("[GTorrent] Desde url {}".format(url.link))
                        torrentadd = self.client.add_torrent(url.link, **options)
                    elif url.torrent:
                        self.logger.info("[GTorrent] Desde fichero {}".format(url.torrent))
                        torrentadd = self.client.add_torrent(url.torrent, **options)
                    else:
                        self.logger.error('Failed to add torrent "{}"'.format(e))
                        raise e 
                            
                    self.logger.info("[GTorrent] %s %s %s %s", str(torrentadd), torrentadd.id, torrentadd.hashString, torrentadd.name)
                    self.logger.debug(filter(lambda aname: not aname.startswith('_'), dir(torrentadd)))
                        
                    # Post Proceso unitario
                    self.__changeTorrent(torrentadd.id)
                    listTorrentResponse.append(torrentadd)
    
            except transmissionrpc.TransmissionError, e:
                self.logger.error('Failed to add torrent "%s"' % e)
                os.remove(url.torrent)
                raise e
            if url.torrent:
                os.remove(url.torrent)
            # Post Proceso Total
            # sendmsgTelegram(listTorrentResponse)
            return listTorrentResponse
    ########################### [END]  Transmission ######################################
         
    
    
    
    
    def __changeTorrent(self,id):
        tupleexclude = (".url", ".txt")
        logger.debug("Recuperamos el torrent : %d", id)
        torrentFiles = self.client.get_files(id)[id]
        logger.debug("id del torrent %s",torrentFiles)
        for narchivo in torrentFiles:
            logger.debug("id del fichero %d",narchivo)
            logger.debug("nombre del fichero %s",torrentFiles[narchivo]["name"])
            if (torrentFiles[narchivo]["name"].endswith(tupleexclude)):
                logger.info("[EXCLUIDO] : %s",torrentFiles[narchivo]["name"])
                opt_change={}
                opt_change["files_unwanted"]=[narchivo]
                # change_torrent(ids, timeout=None, **kwargs)
                self.client.change_torrent(id,**opt_change)

    ## Constructor
    def __init__(self, host, port, user, password,logger=None):
        if (logger):
            self.logger = logger
        self.client = self.getClientTorrent(host, port, user, password)
