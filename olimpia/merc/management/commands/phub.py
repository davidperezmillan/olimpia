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

import merc.at.plugins.utilesplugins as utilesplugins
import merc.at.hilos.utiles

import logging
logger = logging.getLogger(__name__)


def coords(s):
    try:
        valores = map(str, s.split(','))
        return valores
    except Exception, e:
        raise e


class Command(BaseCommand):
    
    # Variables que necesitamos
    # ### Lanzador
    urlPattern = "http://pornleech.is"
    # urlListadoPattern = "?page=catalogue&main=68&category=66"
    urlListadoPattern = "?page=catalogue&main=68&category=64;65;66"  # videos y Videos HD
    
    
    # ### criteria
    PATH_LOG=os.path.dirname(os.path.abspath(__file__))
    PATH_TORRENT=os.path.dirname(os.path.abspath(__file__))
    
    excluidos =  ["BISEXUAL", "LESBIAN", "INTERRACIAL", "SOLO", "JAV"]   
    incluidos = [["THREESOME", "BIG TITS"],]
    
    
    help = "Para buscar, lo que buscar debes hacer:" 
 
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('author', nargs=1, type=str)
        
        
        
        # Named (optional) arguments
        parser.add_argument(
            '--test',
            action='store_true',
            dest='test',
            help='No enviamos nada a transmission',
        )
        
        parser.add_argument('-i','--incluidos', help='tag incluidos', nargs='+', dest="incluidos")
        parser.add_argument('-e','--excluidos', help='tag excluidos', nargs='+', dest="excluidos")
        
        parser.add_argument('-c', '--cord', help="Coordinate", dest="cord", type=coords, nargs="+")
        
        
        
        # parser.add_argument(
        #     '--nomsg',
        #     action='store_true',
        #     dest='nomsg',
        #     help='No enviamos msg-telegram',
        # )
        pass


    def handle(self, *args, **options):
        for user in options['author']:
            logger.info('Ejecutando busqueda especial {}'.format(user))
            author = User.objects.get(username=user)
            logger.debug("Usuario : {}".format(author))
            receivers = merc.management.commands_utils.utilgetreceivers(author)

        
        
        
            if options['incluidos']:
                self.incluidos = options['incluidos'] 
                if options['cord']:
                    for cordenadas in options['cord']:
                        self.incluidos.append(cordenadas)
            else:
                if options['cord']:
                    self.incluidos = options['cord']
                
            
            
            # if options['cord']:
            #     self.incluidos = options['cord']
            #     if options['incluidos']:
            #         self.incluidos = self.incluidos,options['incluidos']
            # else:
            #     if options['incluidos']:
            #         self.incluidos = options['incluidos']
                    
                    
            #  ESTOS ESTAN CLAROS
            if options['excluidos']:
                self.excluidos=options['excluidos']
            
    
                
                
            logger.info("Vamos a incluir: {incluidos}".format(incluidos=self.incluidos))
            logger.info("Vamos a excluir: {excluidos}".format(excluidos=self.excluidos))
            
            
            # Vamos a buscar lo que buscamos
            # Recuperamos la pagina de busqueda
            url = "{}/{}".format(self.urlPattern, self.urlListadoPattern)
            try:
                page, proxy = utilesplugins.toggleproxy(url)
                # pintarFicheroHtml(page.encode('utf-8').strip(),"catalogue")
            except Exception, e:
                raise e
            # Parse pagina principal
            source = BeautifulSoup(page, "html.parser")
            # buscar_list = source.find_all("table", {"class" : "lista"})
            buscar_list = source.find_all("table", {"class" : "lista"})
            
        
            listaTorrent = []
            
            count = 3
            while count < len(buscar_list):
                reg = buscar_list[count]
                if not self.isBeforeDay(reg) :
                    count=count+1
                    break    
                
                '''
                filter, title = insideFilter(reg)
                if not filter:
                    count=count+1
                    continue
                '''    
                
                sUrlShow=reg.find_all("td",{"class":"header"})[0].find("a")['href']
                url = "{}/{}".format(self.urlPattern, sUrlShow)
                try:
                    page, proxy = utilesplugins.toggleproxy(url)
                    # pintarFicheroHtml(page.encode('utf-8').strip(),"show")
                except Exception, e:
                    raise e
                # Parse pagina principal
                source = BeautifulSoup(page, "html.parser")
                urlTorrent = source.find_all("a", href=re.compile("^download.php"))[0]["href"]
                # print source.find_all("a", id=lambda value: value and value.startswith("download.php"))
                
                url = "{}/{}".format(self.urlPattern,urlTorrent)
                
                filter, title, category = self.insideFilter(reg)
                if filter:
                    file_name = '{}/torrent{}.torrent'.format(self.PATH_TORRENT, count)
                    r = requests.get(url, stream=True)
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content():
                            f.write(chunk)
                    listaTorrent.append({"title":title,"file_name":file_name,"url":url.strip(),"category":category})
                else:
                    # logger_EXC.info("::{}::{}::{}::".format(title.strip(), url.strip(), category))
                    pass
                    
                
                
                count=count+1
            ''' probando el cliente '''
            # client = getClientTorrent()
            # addTorrent(client, "http://torrentrapid.com/descargar-torrent/106685_-1523920896-the-brave----temporada-1--hdtv-720p-ac3-5-1/")
            ''' funciona correctamente '''
        
            logger.info("Encontrados : {}".format(listaTorrent))
            
            if not options['test']:
                self.loopAddTorrent(listaTorrent)
            
            
            for i in range(len(buscar_list)):
                try: 
                    os.remove('{}/torrent{}.torrent'.format(self.PATH_TORRENT, i)) 
                except:
                    # logger.warn("No existe")
                    pass
       
       
            merc.at.hilos.utiles.sendTelegram("Hemos encontrado {} ".format(len(listaTorrent)), author, receivers=receivers)
        

            
    def isBeforeDay(self,reg):
        # Parseamos y comprobamos la fecha
        tdFecha = reg.find_all("td",{"class":"lista"})
        fecha=tdFecha[7].text
        war_start = fecha.split(" ")[0]
        dateWar=datetime.strptime(war_start, '%d/%m/%Y')
        isdate = (dateWar.date() == datetime.today().date())
        if isdate:
            logger.debug("El dia : {} es hoy".format(dateWar))
        else:
            logger.debug("No lo es")
        
        # return False
        return isdate
        
    
    def insideFilter(self,reg):
        
        respuesta = False;
        category = []
        title = reg.find_all("td",{"class":"header"})[0].find_all("a")[0].text
        sUrlShow = "{}/{}".format(self.urlPattern, reg.find_all("td",{"class":"header"})[0].find("a")['href'])
        iElements = reg.find_all("td",{"class":"header"})[0].find_all("i")
        for iElement in iElements:
            aElement = iElement.find("a").text
            category.append(aElement.upper())
        
    
        if not category:
            return False, title, category
        
        for inc in self.incluidos:
            if isinstance(inc, (tuple, list, dict, set)):
                # Si es una lista
                # preguntamos si existen los tag
                if not respuesta:
                    respuesta = self.checkIsAllTag(inc, category)
            elif isinstance(inc, (str,basestring)):
                if str(inc).upper() in category:
                    respuesta = True
                    
                    
                    
        # for exc in excluidosCategory:    
        #     if exc.upper() in excluidosCategory:
        #         logger.warn("[RECHAZADO] -> Category: {} == {}".format(category, exc.upper()))
        #         return False, title
        # for excTitle in excluidosTitle:
        #     if excTitle.upper() in title.upper():
        #         logger.warn("[RECHAZADO] -> Title: {} ".format(title))
        #         return False, title
        
        for exc in self.excluidos:    
            if exc.upper() in category or exc.upper() in title.upper():
                respuesta = False
        
        if respuesta:
            logger.info("[ACEPTADO] -> Title: {} --> Category: {}".format(title, category))
            # logger_INC.info("::{}::{}::{}::".format(title.strip(),sUrlShow.strip(),category))
        else:
            logger.warn("[RECHAZADO] -> Title: {} --> Category: {}".format(title, category))
            # logger_EXC.info("[RECHAZADO] -> Title: {} --> Category: {} :: {}".format(title, category, sUrlShow))
            pass
            
        return respuesta, title, category


    def checkIsAllTag(self, tags, category):
        for tag in tags:
            if tag.upper() not in category:
                return False
        return True
        
        
        
    # TRANSMISSION
    def loopAddTorrent(self,listaTorrent):
        logger.info("ENVIAMOS A TRANSMISSION")
        client = self.getClientTorrent()
        for torrent in listaTorrent:
            self.addTorrent(client,torrent["file_name"])
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
        options["download_dir"] = "{0}".format("/media/maxtor/ides/autodown")
        #  urllib.quote and urllib.unquote 
        logger.info("Add torrent url: {}".format(url))
        torrentadd = client.add_torrent(url, **options)
        return torrentadd    