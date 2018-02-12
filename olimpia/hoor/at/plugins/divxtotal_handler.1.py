#!/usr/bin/python
import logging
import urllib, urllib2
import re
from logging.handlers import RotatingFileHandler
import bs4
from bs4 import BeautifulSoup

import utilesplugins as utilesplugins

from merc.at.beans.pluginsBeans import RequestPlugin
from merc.at.beans.pluginsBeans import ResponsePlugin

class EpisodiesBeanClass(object):
    
    def __init__(self,epstart=None, epend=None):
        self.epstart=epstart
        self.epend=epend



class DivxtotalHandler(object):
   
    def _findSerie(self):
        url = "http://www.divxtotal2.net/"
        # Prepare the data
        titulo=self.nombreserie
        values = {'s':'"'+titulo+'"'}
        self.logger.info("Buscamos %s", values)        
        data = urllib.urlencode(values)
        # Send HTTP POST request
        req = urllib2.Request(url, data)
        page = urllib2.urlopen(req)

        # # Parse pagina principal
        # source = BeautifulSoup(page, "html.parser")
        # buscar_list = source.find_all("table", {"class" : "table"})
        
        # enlaces = buscar_list[0].find_all("a") or None
        # if enlaces:
        #     enlace = enlaces[0]
        #     for bl_enlace in enlaces:
        #         valor = bl_enlace['title']
        #         pattern = ".*{0} - Temporada".format(titulo)
        #         self.logger.debug("Comprobamos en '{0}' para {1} ".format(valor, pattern))
        #         if re.match(pattern,valor):
        #             self.logger.debug("encontrado")
        #             enlace = bl_enlace
        #     self.url=enlace["href"] or None
        #     self.logger.info("Hemos encontrado la url %s", self.url)
        #     return True
        # else:
        #     self.logger.warn("No encontramos %s/%s, no descargamos nada", titulo)
        #     return False

    def _firstpage(self):
        url = self.url
        self.logger.debug("Buscando en %s",url)
        page = urllib.urlopen(url)
        #urllib.urlretrieve(url,"page["+self.nombreserie+"].html")
        source = BeautifulSoup(page, "html.parser")
        return source
        
    def _otherPages(self,position):
        url = self.url+"/pg/"+str(position)
        self.logger.debug("Buscando en %s",url)
        page = urllib.urlopen(url)
        self.logger.debug("Position %s :Nombre %s", str(position), self.nombreserie)
        # urllib.urlretrieve(url,"page["+self.nombreserie+position+"].html")
        source = BeautifulSoup(page, "html.parser")
        return source
    
    def _getLastPage(self,source):
        pagination = source.find_all("ul", {"class": "pagination"})
        if len(pagination)==0:
            return 0
        itemlista = pagination[0].find_all("li")
        sItemLast=itemlista[-1].find("a")["href"]
        lastPage = sItemLast[sItemLast.rfind('/')+1:]
        # print "Utima posicion " + lastPage
        return int(lastPage)


    #  Gestion de links
    def _getlinks(self,source):
        bProcced = True;
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        infos = buscar_list[0].find_all("div",{"class":"info"}) # esto es una lista
        valores=[]
        for info in infos:
            tag = info.a["href"]
            title = info.a["title"]
            
            episodeLink = self._getEpisodeLink(title)
            self.logger.debug("Episodio sacado del link %s ", episodeLink)
            if self._filterEpisode(episodeLink):
                response = ResponsePlugin(title=self.nombreserie, link=tag, episode=episodeLink)
                valores.append(response)
            else:
                bProcced = False
        
        return bProcced, valores
            
    def _getEpisodeLink(self, titleLink):
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
                
        episodeLink="{0}S{1}E{02}".format(self.quality,temporada,capitulo)
        # self.logger.debug("Capitulo a recuperado %s", str(sc))
        return episodeLink
    
    def _filterEpisode(self, episodeLink):
        # Estos datos llegaran como...... NRS00E00
        
        self.logger.debug("[Filtrando] cap: %s entre %s y %s",episodeLink, self.episodes.epstart, self.episodes.epend)
        if (self.episodes is None): #si no hay episodios lo enviamos todo
            self.logger.info("No hay etiqueta de episodios, se descarga todo ")
            return True 
        else:
            
            # Preparar datos
            epstartquality, epstartsession, epstartepisode = utilesplugins.converterEpisode(self.episodes.epstart)
            ependquality, ependsession, ependepisode = utilesplugins.converterEpisode(self.episodes.epend)
            eplinkquality, eplinksession, eplinkepisode = utilesplugins.converterEpisode(episodeLink)
            
            inicio = int(epstartsession+epstartepisode) if epstartsession and epstartepisode else 0000
            final = int(ependsession+ependepisode) if ependsession and ependepisode else 9999
            elegido = int(eplinksession+eplinkepisode) if eplinksession and eplinkepisode else 0000
            
            if inicio <= elegido and final >= elegido:
                self.logger.info("[Aceptado] (%s) cap: %s para %s de %s",self.nombreserie, episodeLink, self.episodes.epstart, self.episodes.epend)
                return True
            else:
                self.logger.info("[Rechazado] (%s) cap: %s para %s de  %s ",self.nombreserie, episodeLink, self.episodes.epstart, self.episodes.epend)
                return False
        
    def _getTorrentFiles(self,item):
        url = item.link
        req = urllib2.Request(url) 
        soup = BeautifulSoup(urllib2.urlopen(req), "html.parser")
        redirMatch = re.match(r'.*?window\.location\.\href\s*=\s*\"([^"]+)\"', str(soup), re.M|re.S)
        if(redirMatch and "http" in redirMatch.group(1)):
            url = redirMatch.group(1)
            item.link = url
            return item
        else:
            item.link = soup.title.string.encode('ascii', 'ignore').strip().replace('\n','')
            return item
            
    # EJECUTOR   
    def execute(self,request, filter=False):
        self.logger.info(" ---> Processando con el plugin .... {0} -- {1}".format(request, filter))

        epstartquality, epstartsession, epstartepisode = utilesplugins.converterEpisode(request.epstart)
        ependquality, ependsession, ependepisode = utilesplugins.converterEpisode(request.epend)
        
        self.nombreserie=request.title
        self.quality=epstartquality if epstartquality else ependquality
        self.episodes=EpisodiesBeanClass(epstart=request.epstart, epend=request.epend)
        enlaces=[] # Respuesta
        
        
        # Empezamos la busqueda
        if self._findSerie():
            # Recuperamos la primera pagina
            fPage = self._firstpage()
            # Recuperamos el numero de paginas
            lastPage = self._getLastPage(fPage)
            
            # Valores de la primera pagina
            bProcced,valores = self._getlinks(fPage);
            bProccedFilter = bProcced if filter else True
            
            self.logger.info("links recuperados/filtrados en la pagina 1 de {0} : {1} -- {2}".format(lastPage, len(valores),bProccedFilter))
            
            # Valores de n pagina
            count = 2
            while count <= lastPage and bProccedFilter:
                source = self._otherPages(count)
                bProcced,valor = self._getlinks(source)
                bProccedFilter = bProcced if filter else True
                valores.extend(valor)
                self.logger.info("links recuperados/filtrados en la pagina {0} de {1} : {2} -- {3}".format(count, lastPage, len(valores),bProccedFilter))
                count = count + 1
    
            self.logger.debug("links recuperados/filtrados en la paginas %d : %d" ,count,len(valores))            
            self.logger.debug("links recuperados/filtrados %s" ,str(valores))
            
            self.logger.info("Recuperando {0} torrent, esto puede tardar un poco, tenga paciencia".format(len(valores)))
            for valor in valores:
                tagTorrent = self._getTorrentFiles(valor)
                self.logger.debug("url torrent %s", tagTorrent)
                enlaces.append(tagTorrent)

        return enlaces


    ## Constructor
    def __init__(self, logger=None):
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
    



if __name__ == '__main__':
    
    dthandler = DivxtotalHandler()
    request = RequestPlugin(title='The BlackList', epstart='HDS05E00', epend='HDS99E99')
    dthandler.execute(request,filter=False)