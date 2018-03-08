#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from hoor.business.jano.common.downJano import Down, Plugins,ResponsePlugin


# import urllib, urllib2
import re
# from logging.handlers import RotatingFileHandler
# import bs4
# from bs4 import BeautifulSoup








class TorrentRapidHandlerClass(object):
   
   
    def execute(self,down, filter=False):

        # down.nombre="Mom"
        # down.quality="HD"
        # down.ep_start="HDS00E00"
        # down.ep_end="HDS99E99"
        
        logger.debug("nombre : {down}".format(down=down.nombre))
        logger.debug("calidad : {down}".format(down=down.quality))
        logger.debug("comienzo : {down}".format(down=down.ep_start))
        logger.debug("final : {down}".format(down=down.ep_end))
        
        logger.info("Bucamos la serie {}".format(down.nombre))
        urlFirst = self.__findSerie(down)
        ## recuperamos la primera pagina
        source, lastPage = self.__getPages(urlFirst)
        
        valores=[]
        # Valores de la primera pagina
        bProcced,valores = self.__getlinks(source, down);
        bProccedFilter = bProcced if filter else True
        
        count = 2
        while count <= lastPage:
            url = urlFirst+"/pg/"+str(count) 
            source, lastPage = self.__getPages(url)
            bProcced,valor = self.__getlinks(source, down) ### TODO
            bProccedFilter = bProcced if filter else True
            valores.extend(valor)
            logger.info("links recuperados/filtrados en la pagina {0} de {1}".format(count, lastPage))
            count = count + 1
         
         
        logger.info("Encontramos la serie {} -> {} -> {}".format(down.nombre, url, lastPage))
        return valores
   
   
   
   
    def __findSerie(self, down):
        url = "http://torrentrapid.com/buscar"
        # Prepare the data
        titulo = '"{0}"'.format(down.nombre)
        if down.quality=="HD":
            quality="1469"
        elif down.quality=="VO":
            quality=""
        elif down.quality=="AL":
            quality=""
            titulo = '{0}'.format(down.nombre)
        else:
            quality="767"
      
        param = {'q' : titulo,"categoryIDR":quality, "ordenar":"Nombre", "inon":"Descendente"}
        logger.debug("Buscamos %s", param)        
        # recuperamos la pagina
        page = self.scrapForce(url,param)
        # parseamos la pagina
        source = self.parserHtml(page)
        
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        enlaces = buscar_list[0].find_all("a") or None
        if enlaces:
            enlace = enlaces[0]
            for bl_enlace in enlaces:
                valor = bl_enlace['title']
                pattern = ".*{0} - Temporada".format(titulo)
                logger.debug("Comprobamos en '{0}' para {1} ".format(valor, pattern))
                if re.match(pattern,valor):
                    logger.debug("encontrado")
                    enlace = bl_enlace
            urlResponse=enlace["href"] or None
            logger.debug("Hemos encontrado la url {}".format(urlResponse))
            return urlResponse
        else:
            logger.warn("No encontramos {}/{}, no descargamos nada".format(titulo, quality))
            return None
            
    def __getPages(self, url):
        logger.debug("Buscando en %s",url)
        page = self.scrapForce(url, None)
        #urllib.urlretrieve(url,"page["+self.nombreserie+"].html")
        source = self.parserHtml(page)
        
        pagination = source.find_all("ul", {"class": "pagination"})
        if len(pagination)==0:
            return 0
        itemlista = pagination[0].find_all("li")
        sItemLast=itemlista[-1].find("a")["href"]
        lastPage = sItemLast[sItemLast.rfind('/')+1:]
        # print "Utima posicion " + lastPage
        
        return source,int(lastPage)
        


    #  Gestion de links
    def __getlinks(self,source, down):
        bProcced = True;
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        infos = buscar_list[0].find_all("div",{"class":"info"}) # esto es una lista
        valores=[]
        for info in infos:
            tag = info.a["href"]
            title = info.a["title"]
            
            episodeLink = self.__getEpisodeLink(title, down)
            logger.debug("Episodio sacado del link %s ", episodeLink)
            if self.__filterEpisode(episodeLink, down):
                response = ResponsePlugin(title=down.nombre, link=tag, episode=episodeLink)
                valores.append(response)
            else:
                bProcced = False
        
        return bProcced, valores
            
    
    def __getEpisodeLink(self, titleLink, down):
        # Recuperamos el capitulo del link
        sessionCaps = re.findall('(Temporada\s\d{1,}|Capitulo\s\d{1,})', titleLink)
        # self.logger.debug("Session Capitulos %s", str(sessionCaps))
        temporada="00"
        capitulo="00"
        for sc in sessionCaps:
            # self.logger.debug("Buscamos en url '%s'",sc)
            if sc.startswith("Temporada"):
                temporada = re.findall('\d{1,}', sc)[0].zfill(2)
                # self.logger.debug("Temporada encontrada %s",temporada)
            elif sc.startswith("Capitulo"):
                capitulo= re.findall('\d{1,}', sc)[0].zfill(2)
                # self.logger.debug("Capitulo encontrada %s",capitulo)
                
        episodeLink="{0}S{1}E{02}".format(down.quality,temporada,capitulo)
        # self.logger.debug("Capitulo a recuperado %s", str(sc))
        return episodeLink
    
    
    def __filterEpisode(self, episodeLink, down):
        # Estos datos llegaran como...... NRS00E00
        
        logger.debug("[Filtrando] cap: %s entre %s y %s",episodeLink, down.ep_start, down.ep_end)
        if (down.ep_start is None): #si no hay episodios lo enviamos todo
            logger.info("No hay etiqueta de episodios, se descarga todo ")
            return True 
        else:
            
            # Preparar datos
            epstartquality, epstartsession, epstartepisode = self.converterEpisode(down.ep_start)
            ependquality, ependsession, ependepisode = self.converterEpisode(down.ep_end)
            eplinkquality, eplinksession, eplinkepisode = self.converterEpisode(episodeLink)
            
            inicio = int(epstartsession+epstartepisode) if epstartsession and epstartepisode else 0000
            final = int(ependsession+ependepisode) if ependsession and ependepisode else 9999
            elegido = int(eplinksession+eplinkepisode) if eplinksession and eplinkepisode else 0000
            
            if inicio <= elegido and final >= elegido:
                logger.info("[Aceptado] (%s) cap: %s para %s de %s",down.nombre, episodeLink, down.ep_start, down.ep_end)
                return True
            else:
                logger.info("[Rechazado] (%s) cap: %s para %s de  %s ",down.nombre, episodeLink, down.ep_start, down.ep_end)
                return False
    
     
            
            
            
            
            
   # Sacar de aqui:
    def scrapForce(self, url, param):
      
        import urllib, urllib2
        data = None
        if param:
            data = urllib.urlencode(param)
            # Send HTTP POST request
        req = urllib2.Request(url, data)
        page = urllib2.urlopen(req)
        return page
      
    def parserHtml(self,page):
        from bs4 import BeautifulSoup
        source = BeautifulSoup(page, "html.parser")
        return source
        
    
    def converterEpisode(self,episode): # El formato que recuperamos es por defecto NRS00E00
        if episode is None:
            return None, None, None # tenemos que itererar todo lo que enviamos!!!
        quality = episode[:2] or None
        session = episode[3:5] or None
        episode = episode[-2:] or None
        return quality, session, episode