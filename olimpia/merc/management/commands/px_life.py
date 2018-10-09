#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  

import os, sys, re
import transmissionrpc
import urllib, urllib2
# import requests
# import json
# import random
# import bs4
from bs4 import BeautifulSoup
from datetime import datetime

# django & merc
from django.core.management.base import BaseCommand, CommandError
# from django.contrib.auth.models import User
# from django.utils import timezone
# from django.conf import settings

# from merc.modelsCustom import P_History 

import merc.at.plugins.utilesplugins as utilesplugins
# import merc.at.hilos.utiles


# merc.at.properties.cmdproperties
import merc.at.properties.cmdproperties as cmdproperties

import logging
logger = logging.getLogger(__name__)





class Command(BaseCommand):
    
    ##
    # Varibles comunes
    path_url_principal = 'https://myporn.club/torrents'
    path_url_torrent = 'https://myporn.club/torrent/'

    
    def add_arguments(self, parser):
        parser.add_argument('--down',action='store_true',dest='down', help='Descargamos las previos',)
        parser.add_argument('--test',action='store_true',dest='test', help='No enviamos nada a transmission',)
        parser.add_argument('-p','--pages', help='Paginas incluidas en la busqueda', dest="pages", type=int, default=1, choices=range(1,6))    
        parser.add_argument('-l','--life', help='Vida comparada', dest="life", type=float, default=1000,)
        pass


    def handle(self, *args, **options):
        
        
        self.pages = options["pages"] or 1
        
        listaNoTorrent = []
        listaTorrent = []
        
        logger.debug("Numero de paginas a buscar : {} ".format(self.pages))
        for npage in range(1,(self.pages+1)):
            url_principal = "{}/{}".format(self.path_url_principal,npage)
            try:
                logger.debug("Vamos a buscar en {}".format(url_principal))
                page, proxy = utilesplugins.toggleproxy(url_principal)
                utilesplugins.pintarFicheroHtml(page.encode('utf-8').strip(),"principal")
                source = BeautifulSoup(page, "html.parser")
                
            except Exception, e:
                logging.fatal(e, exc_info=True)
                raise e
          
            torrents_list = source.find_all("div", {"class" : "torrents_list"})
            torrent_elements = torrents_list[0].find_all("div", {"class":"torrent_element"})
            
            logger.debug("Hemos encontrado torrentes: {}".format(len(torrent_elements)))
            for torrent_element in torrent_elements:
                item_torrent = {}
                
                ## Buscamos el titulo
                torrent_element_text_div = torrent_element.find_all("div", {"class":"torrent_element_text_div"})[0]
                title_all = torrent_element_text_div.find_all(lambda tit: tit.name == 'a' and tit.get('class') == ['tdn'])[0]
                title = title_all.getText()
                ## Buscamos el enlace
                torrent_element_info = torrent_element.find_all("div",{"class":"torrent_element_info"})[0]
                ## Recuperamos titulo y tags
        
                tags = [tag['data-key'].upper() for tag in title_all.find_all("i", {"data-key":True})]
                ## Recuperamos enlace
                alphaid = torrent_element_info["data-alphaid"]
                url_torrent = "{}{}".format(self.path_url_torrent,alphaid)
                
                ## buscamos el tamano
                sLife = torrent_element_info.find_all(text=re.compile("\[size]"))[0].findNext("span",{"class":"teiv"}).text
                fLife = float(sLife.split()[0])
                item_torrent = {'title':title, 'tags':tags, 'alphaid': alphaid,'url_torrent':url_torrent, 'life':sLife}
                listaNoTorrent.append(item_torrent)
                
                
                ## Filtramos por duracion
                if fLife > options['life']:
                    logger.info("vida correcta {}".format(sLife))
                    
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
                        video = torrent_links["data-content"].split(",")[1].replace("\\\"", "")
                        item_torrent['video']="https:{}".format(video)
                    except Exception, e:
                        logger.warn("No se ha encontrado el video")
                        item_torrent['video']=None
                        pass
                    ## Recuperamos el torrent
                    td_btn = torrent_download_div.find_all("a", {"class" : "td_btn"})[0]['href']
                    md_btn = torrent_download_div.find_all("a", {"class" : "md_btn"})[0]['href']
                    item_torrent['torrent']=td_btn
                    item_torrent['magnet']=md_btn
                    
                    listaTorrent.append(item_torrent)
                
                else:
                    # logger.warn("Demasiado corto: {}".format(sLife))
                    pass
        
        
        if options['down']:        
            for torrent in listaTorrent:
                filepreview = "{}.mp3".format(torrent["alphaid"])
                filepathpreview = cmdproperties.CMD_PATH_DOWNLOAD_PREVIEW.format(filepreview)
                urllib.urlretrieve(torrent['video'], filepathpreview)
            
        if not options['test']:                
            self.loopAddTorrent(listaTorrent)  
        else:
            logger.warn("Modo test")
            for torrent in listaTorrent:
                logger.info("No descargado {} -- {} [{}]".format(torrent["alphaid"],torrent['video'], torrent['life']))
   
   
    
                
                
    # TRANSMISSION
    def loopAddTorrent(self,listaTorrent):
        logger.info("ENVIAMOS A TRANSMISSION")
        client = self.getClientTorrent()
        for item_torrent in listaTorrent:
            torrentAdded = self.addTorrent(client,item_torrent['torrent'])
            if torrentAdded:
                logger.info("Add torrent: {} :: {}".format(item_torrent['title'], item_torrent['tags']))
                # self.createRegData(item_torrent) 
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
    	options["download_dir"] = cmdproperties.CMD_PATH_DOWNLOAD_TORRENT.format(datetime.now(),os.path.splitext(os.path.basename(__file__))[0])
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
