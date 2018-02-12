#!/usr/bin/env python
# -*- coding: utf-8 -*-
import transmissionrpc
import logging
from logging.handlers import RotatingFileHandler


class TorrentHandlerClass(object):
    
    
    def __client_init(self, torrentServer):
        if torrentServer.torrent_active:
            logging.getLogger('transmissionrpc').setLevel(self.logger.getEffectiveLevel())
            # formatter = logging.Formatter(defaulformatter)
            # ch = logging.StreamHandler()
            # ch.setFormatter(formatter)        
            for hand in self.logger.handlers:
                logging.getLogger('transmissionrpc').addHandler(hand)
            
            host = torrentServer.host
            port = torrentServer.port
            user = torrentServer.user
            password = torrentServer.password
            
            self.logger.info("Intentando conectar con : {0}{1}{2}{3}".format(host,port,user,password))
            client = transmissionrpc.Client(host, port=port, user=user, password=password)
            self.logger.debug("download_dir {0}".format(client.get_session().download_dir))
            return client
        else:
            return
        
    
    def allAddTorrent(self,urls,torrentServer):
        if torrentServer.torrent_active:
                
            disponible = True
            if torrentServer.space_disk:
                self.logger.debug("Calculamos el espacio que tenemos [%s]", torrentServer.space_disk)
                try:
                    download_dir_path = torrentServer.download
                    # download_dir_path = config.torrent_server.transmission.custom_options.download_dir_path
                except:
                    self.logger.warn("No hay download_dir_path, se descargara en el directorio por defecto")
                    download_dir_path = self.client.get_session("download_dir")
                if torrentServer.space_disk >= self.client.free_space(download_dir_path):
                    disponible = False
            else:
                self.logger.debug("Skip el espacio que tenemos")
            
            # if self.test: # Comprobamos que no estamos en modo test
            #     self.logTest.info("[TEST] Estamos en Modo TEST, no se descarga nada, pero deberiamos descargar")
            #     for descarga in urls:
            #         self.logTest.info("[TEST] %s:%s -- %s",descarga.title,descarga.episode,descarga.link)
            #     return 
            
            if disponible:
                # Gestion de opciones
                options = {}
                options['paused']=torrentServer.paused
                
                try: 
                    listTorrentResponse = []
                    for url in urls:
                        self.logger.debug("Enviando con : {} : {} : {}".format(url.title,url.episode, torrentServer.download))
                        try:
                            quality = url.episode[:2] or None
                            session = ("Session {0}".format(str(int(url.episode[3:5])).zfill(1)))
                            q = "_{0}".format(quality) if quality and quality=='VO' else ""
                            titulo = "{0}{1}".format(url.title,q)
                            options["download_dir"] = "{0}/{1}/{2}".format(torrentServer.download, titulo, session)

                        except Exception, e:
                            self.logger.error("No hay download_dir_path, se descargara en el directorio por defecto: {1}".format(e))
                            
                        self.logger.debug("Intentando descargar: %s:%s con la opciones: %s", url.title, url.episode, options)
                        
                        
                        torrentadd = self.client.add_torrent(url.link, **options)
                        self.logger.info("[GTorrent] %s %s %s %s", str(torrentadd), torrentadd.id, torrentadd.hashString, torrentadd.name)
                        self.logger.debug(filter(lambda aname: not aname.startswith('_'), dir(torrentadd)))
                        # if torrentadd.torrent-duplicate:
                        #     self.self.logger.info("[Torrent] Nos hemos encontado un torrent duplicado: %d:%s",torrentadd.torrent-duplicate.id, torrentadd.torrent-duplicate.name)
                        
                        
                        # Post Proceso unitario
                        self.__changeTorrent(torrentadd.id)
                        listTorrentResponse.append(torrentadd)
    
                except transmissionrpc.TransmissionError, e:
                    self.logger.error('Failed to add torrent "%s"' % e)
                    raise e
            
            # Post Proceso Total
            # sendmsgTelegram(listTorrentResponse)
            return listTorrentResponse
        else:
            return
    ########################### [END]  Transmission ######################################
         
    
    
    
    def __changeTorrent(self,id):
        tupleexclude = (".url", ".txt")
        self.logger.debug("Recuperamos el torrent : %d", id)
        torrentFiles = self.client.get_files(id)[id]
        self.logger.debug("id del torrent %s",torrentFiles)
        for narchivo in torrentFiles:
            self.logger.debug("id del fichero %d",narchivo)
            self.logger.debug("nombre del fichero %s",torrentFiles[narchivo]["name"])
            if (torrentFiles[narchivo]["name"].endswith(tupleexclude)):
                self.logger.info("[EXCLUIDO] : %s",torrentFiles[narchivo]["name"])
                opt_change={}
                opt_change["files_unwanted"]=[narchivo]
                # change_torrent(ids, timeout=None, **kwargs)
                self.client.change_torrent(id,**opt_change)



    
    
    ## Constructor
    def __init__(self, torrentServer = None, logger= None):
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)

        self.client = self.__client_init(torrentServer)