#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  

import os, sys, re
import transmissionrpc
import urllib, urllib2
import requests
import json
import random
import bs4
from bs4 import BeautifulSoup
from datetime import datetime

# django & merc
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from merc.modelsCustom import P_History 

import merc.at.plugins.utilesplugins as utilesplugins
import merc.at.hilos.utiles

import logging
# logger = logging.getLogger(__name__)
logger = logging.getLogger("busquedas_especiales")





class Command(BaseCommand):
    
    ##
    # Varibles comunes
    path_url_principal = 'https://myporn.club/torrents/'
    path_url_torrent = 'https://myporn.club/torrent/'
    
    PATH_LOG=os.path.join(settings.BASE_DIR,'../data/olimpia')
    logger_INC = None
    logger_EXC = None
    
    
    def add_arguments(self, parser):
        parser.add_argument('author', nargs=1, type=str)
        
        # Named (optional) arguments
        parser.add_argument(
            '--test',
            action='store_true',
            dest='test',
            help='No enviamos nada a transmission',
        )
        
        parser.add_argument(
            '--lite',"-l",
            action='store_true',
            dest='lite',
            help='No guardamos links torrent',
        )
        
        parser.add_argument('-p','--pages', help='Paginas incluidas en la busqueda', dest="pages", type=int, default=1, choices=range(1,6))
        
        
        parser.add_argument('-i','--incluidos', help='tag incluidos', nargs='+', dest="incluidos")
        parser.add_argument('-e','--excluidos', help='tag excluidos', nargs='+', dest="excluidos")
        
        pass


    def handle(self, *args, **options):
        
        ## Parametros
        self.__getParams(options);
    

    
        listaTorrent = []
        listaNoTorrent  = []
    
        
        for npage in range(1,(self.pages+1)):
            ## Manejador
            url_principal = "{}{}".format(self.path_url_principal,npage)
            try:
                logger.debug("Vamos a buscar en {}".format(url_principal))
                page, proxy = utilesplugins.toggleproxy(url_principal)
                source = BeautifulSoup(page, "html.parser")
            except Exception, e:
                logging.fatal(e, exc_info=True)
                raise e
            torrents_list = source.find_all("div", {"class" : "torrents_list"})
            ## Recuperamos los elementos
            torrent_elements = torrents_list[0].find_all("div", {"class":"torrent_element"})
            for torrent_element in torrent_elements:
                item_torrent = {}
                ## Buscamos el titulo
                torrent_element_text_div = torrent_element.find_all("div", {"class":"torrent_element_text_div"})[0]
                ## Buscamos el enlace
                torrent_element_info = torrent_element.find_all("div",{"class":"torrent_element_info"})[0]
                ## Recuperamos titulo y tags
                title_all = torrent_element_text_div.find_all(lambda tit: tit.name == 'a' and tit.get('class') == ['tdn'])[0]
                title = title_all.getText()
                tags = [tag['data-key'].upper() for tag in title_all.find_all("i", {"data-key":True})]
                ## Recuperamos enlace
                alphaid = torrent_element_info["data-alphaid"]
                url_torrent = "{}{}".format(self.path_url_torrent,alphaid)
                item_torrent = {'title':title, 'tags':tags, 'alphaid': alphaid,'url_torrent':url_torrent, 'page': npage}
                listaNoTorrent.append(item_torrent)
    
    
                ## 
                try:
                    page, proxy = utilesplugins.toggleproxy(url_torrent)
                    source = BeautifulSoup(page, "html.parser")
                    torrent_div = source.find_all("div", {"class" : "torrent_div"})[0]
                    torrent_info_div = torrent_div.find_all("div", {"class" : "torrent_info_div"})[0]
                    torrent_download_div = torrent_div.find_all("div", {"class" : "torrent_download_div"})[0]
                except Exception, e:
		    logger.fatal(e, ext_info=True)
		    raise e
                try:
                    ##Recupermoas el video
                    torrent_links = torrent_info_div.find_all("div", {"class" : "torrent_links"})[0]
                    video = torrent_links["data-content"].split(",")[1]
                    item_torrent['video']=video
                except Exception, e:
                    logger.warn("No se ha encontrado el video")
                    pass
                ## Recuperamos el torrent
                td_btn = torrent_download_div.find_all("a", {"class" : "td_btn"})[0]['href']
                md_btn = torrent_download_div.find_all("a", {"class" : "md_btn"})[0]['href']
                item_torrent['torrent']=td_btn
                item_torrent['magnet']=md_btn
                
                if self.insideFilter(item_torrent['tags']):
                    # Comprobamos que no esta en la BBDD
                    created = P_History.objects.filter(title=item_torrent['title'],plugin=2, down=True).exists()
                    if created:
                        logger.info('Ya existia el registro')
                    else:
                        listaTorrent.append(item_torrent)
                
            
            
        logger.info("Listado de admitidos: {} items ".format(len(listaTorrent)))
        logger.info("Listado de excluidos: {} items ".format(len(listaNoTorrent)))
        for trrt in listaTorrent:
            if self.lite:
                registro = "::{}::{}::{}::".format(trrt['title'], trrt['url_torrent'], trrt['tags'])
            else:
                registro = "::{}::{}::{}::{}::".format(trrt['title'], trrt['url_torrent'],trrt['torrent'], trrt['tags'])
            self.logger_INC.info(registro)
        for trrt in listaNoTorrent:
            if self.lite:
                registro = "::{}::{}::{}::".format(trrt['title'], trrt['url_torrent'], trrt['tags'])
            else:
                registro = "::{}::{}::{}::{}::".format(trrt['title'], trrt['url_torrent'],trrt['torrent'], trrt['tags'])
            self.logger_EXC.info(registro)        

        if not self.test and listaTorrent:
            self.loopAddTorrent(listaTorrent)          



        # Construimos y enviamos el mensaje
        if not options['test']:
            msgHeader = "Hemos encontrado en yp {} de {} \n\r".format(len(listaTorrent), len(listaNoTorrent))
            sitems = ""
            sFinal = ""
            for item in listaTorrent:
                sitems = "{0}{1}.\t {2}  \n\r".format(sitems,item['title'].encode('utf-8').strip(), item["tags"]) 
            msg = "{0}{1}{2}".format(msgHeader,sitems, sFinal)
            merc.at.hilos.utiles.sendTelegram(msg, user=self.author, receivers=self.receivers)
    

   

    
    def __getParams(self, options):
        
        
        self.incluidos = options['incluidos'] or []
        self.excluidos = options['excluidos'] or []
        self.test = options["test"] or False
        self.lite = options["lite"] or False
        self.pages = options["pages"] or 1
        
        self.logger_INC = self.getHandlerIncluidosInfo(os.path.join(self.PATH_LOG, 'report'),"WTCHD_CLUB")
        self.logger_EXC = self.getHandlerExcluidosInfo(os.path.join(self.PATH_LOG, 'report'),"WTCHD_CLUB")
        
        for user in options['author']:
            logger.info('Ejecutando busqueda especial {}'.format(user))
            self.author = User.objects.get(username=user)
            logger.debug("Usuario : {}".format(self.author))
            self.receivers = merc.management.commands_utils.utilgetreceivers(self.author)

        logger.info("Numero de paginas a buscar: {pages}".format(pages=self.pages))
        logger.info("Vamos a incluir: {incluidos}".format(incluidos=self.incluidos))
        logger.info("Vamos a excluir: {excluidos}".format(excluidos=self.excluidos))
        if self.test:
            logger.info("MODO TEST")
            

    
    
    def insideFilter(self,tags):
        respuesta = False
        for incluido in self.incluidos:
            if incluido.upper() in tags:
                respuesta = True
                
        for excluido in self.excluidos:
            if excluido.upper() in tags:
                return False

        return respuesta
    
    
    def createRegData(self, reg):
        from merc.modelsCustom import P_History
        registry = P_History()
        registry.down=True
        registry.title=reg['title']
        registry.url=reg['url_torrent']
        registry.plugin=2
        registry.fecha=timezone.now()
        registry.save()
        logger.info('Se ha creado el registro {}'.format(registry))
    
    
    
    ### Helper  ### 
    def getHandlerExcluidosInfo(self, dirname,filename):
        logger.info("DENTRO {}".format("getHandlerExcluidosInfo"))
        from logging.handlers import TimedRotatingFileHandler
        from logging import FileHandler
        lFormatter = logging.Formatter('%(asctime)s - %(message)s')
        
        logger_EXC = logging.getLogger('loggerEXC')
        logger_EXC.setLevel(logging.INFO)
        lFormatter_EXC = lFormatter
        handlerE = FileHandler("{}/{:%H%M_%Y%m%d}_{}_EXCLUIDOS.dat".format(dirname,datetime.now(), filename), mode='w',)
        logger_EXC.addHandler(handlerE)

        return logger_EXC    
        
    def getHandlerIncluidosInfo(self,dirname, filename):
        logger.info("DENTRO {}".format("getHandlerIncluidosInfo"))
        from logging.handlers import TimedRotatingFileHandler
        from logging import FileHandler
        lFormatter = logging.Formatter('%(asctime)s - %(message)s')
        
        logger_INC = logging.getLogger('loggerINC')
        logger_INC.setLevel(logging.INFO)
        lFormatter_INC = lFormatter
        handlerI = FileHandler("{}/{:%H%M_%Y%m%d}_{}_INCLUIDOS.dat".format(dirname,datetime.now(), filename), mode='w',)
        logger_INC.addHandler(handlerI)

        return logger_INC    

















   
    # TRANSMISSION
    def loopAddTorrent(self,listaTorrent):
        logger.info("ENVIAMOS A TRANSMISSION")
        client = self.getClientTorrent()
        for item_torrent in listaTorrent:
            torrentAdded = self.addTorrent(client,item_torrent['torrent'])
            if torrentAdded:
                logger.info("Add torrent: {} :: {}".format(item_torrent['title'], item_torrent['tags']))
                self.createRegData(item_torrent) 
            pass
        pass
    
    def getClientTorrent(self,loggerLevel=logging.WARN):
        # Logger config
        logging.getLogger('transmissionrpc').setLevel(loggerLevel)
        for hand in logger.handlers:
            logging.getLogger('transmissionrpc').addHandler(hand)
        # Logger ends
        
        host = "85.53.90.10"
        port = "1701"
        user = "davidperezmillan"
        password = "clon9897"
        
        logger.info("Intentando conectar con : {0}@{1}:{2}".format(user,host,port))
        client = transmissionrpc.Client(host, port=port, user=user, password=password)
        logger.debug("download_dir {0}".format(client.get_session().download_dir))
        return client
    
    def addTorrent(self,client, url):
        options = {}
        options['paused']=False
        options["download_dir"] = "/media/maxtor/ides/autodown/{}/{:%Y%m%d}".format(os.path.splitext(os.path.basename(__file__))[0],datetime.now())
        #  urllib.quote and urllib.unquote 
        logger.info("Request torrent url: {}".format(url))
        torrentadd = client.add_torrent(url, **options)
        return torrentadd    
   
    
    
    
    
    
'''
DOC:

Pagina principal o listado

torrents_list
    torrent_element
        torrent_element_text_div
        torrent_element_info
        
        
Pagina del torrent
		<div class='torrent_div'>
		<div class='torrent_text'></div>
		<div class='torrent_info_div'>
			<div>[hash_info]:d5c92d68f20aae31324c28d44b698025c23ba11c</div>
			<div>[name]:<span class='tname_span'>Alexis.Texas.And.Jayden.Jaymes.Take.On.Johnny.Sin.s.Throbbing.Shaft.Elegant.Angel.Threesome.mp4</span></div>
			<div>[size]:<span class='tsize_span'>306.18 Mb</span></div>
			<div>[hits]:48</div>
			<div>[views]:89</div>
			<div>[seeders]:<span class='teiv_seeders'>2</span></div>
			<div>[leechers]:<span class='teiv_leechers'>0</span></div>
			<div>[last checked]:2 minutes ago</div>
			<div>[uploaded]:17 hours ago</div>
			<div>[uploader]:<a href='/CrisRocco_yps' class='tdn transition torrent_uploader'><span class='uploader_logo' style='background-color:#1FBBBB;color:#BBBBBB'>C</span><span class='uploader_nick'>@CrisRocco_yps</span></a></div>
			<div class='torrent_links' data-mode='show'
			 data-content='[\"//yps.to/post/5b422ab572c1f.html\",\"//s14.trafficdeposit.com/blog/vid/5943d98de5718/5b422ab572c1f/vidthumb.mp4\",\"//s14.trafficdeposit.com/blog/vid/5943d98de5718/5b422ab572c1f/full.jpg\"]'>[links +]</div>
			<div class='torrent_links_content' id='torrent_links_content'></div>
			<div class='torrent_content' data-mode='show' data-content='{\"Alexis.Texas.And.Jayden.Jaymes.Take.On.Johnny.Sin.s.Throbbing.Shaft.Elegant.Angel.Threesome.mp4\":321051933}'>[content +]</div>
			<div class='torrent_content_content' id='torrent_content_content'></div>
		</div>
				<div class='torrent_download_div'>
		<a class='tdn d_btn td_btn' onclick="hit('ev8oSMSK')" 
			href='http://ct1.myporn.club/download.php?uid=5b16d660501f8&tid=ev8oSMSK&fn=Alexis.Texas.And.Jayden.Jaymes.Take.On.Johnny.Sin.s.Throbbing.Shaft.Elegant.Angel.Threesome.mp4'>TORRENT DOWNLOAD
		</a>
		<a class='tdn d_btn md_btn' onclick="hit('ev8oSMSK')" 
			href='magnet:?xt=urn:btih:d5c92d68f20aae31324c28d44b698025c23ba11c&dn=Alexis.Texas.And.Jayden.Jaymes.Take.On.Johnny.Sin.s.Throbbing.Shaft.Elegant.Angel.Threesome.mp4&xl=321051933&tr=udp://tracker1.myporn.club:9337/announce&tr=udp://tracker.opentrackr.org:1337/announce'>MAGNET DOWNLOAD
		</a>
	</div>


'''
