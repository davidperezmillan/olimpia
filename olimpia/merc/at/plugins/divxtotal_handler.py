#!/usr/bin/python
import logging
import re
import bs4
from bs4 import BeautifulSoup

import utilesplugins as utilesplugins

from merc.at.beans.pluginsBeans import RequestPlugin
from merc.at.beans.pluginsBeans import ResponsePlugin

class EpisodiesBeanClass(object):
    
    def __init__(self,epstart=None, epend=None):
        self.epstart=epstart
        self.epend=epend



class DivxtotalHandlerClass(object):
   
   
    # Podemos incluir el proxy pero tenemos una lista que podemos utilzar en el utiles 
    # o no enviar nada y cogera los de por defecto
    
    # proxy = { 
    #       "http"  : "http://190.12.102.205:8080", 
    #     #   "https" : "http://190.12.102.205:8080"
    #     #   "ftp"   : "http://190.12.102.205:8080"
    #     }
    
    
    proxy = utilesplugins.proxies
   
    # EJECUTOR   
    def execute(self,request, filter=False):
        # try:
            self.logger.info(" ---> Processando con el plugin .... {0} -- {1}".format(request, filter))
    
            epstartquality, epstartsession, epstartepisode = utilesplugins.converterEpisode(request.epstart)
            ependquality, ependsession, ependepisode = utilesplugins.converterEpisode(request.epend)
            
            self.nombreserie=request.title
            self.quality=epstartquality if epstartquality else ependquality
            self.episodes=EpisodiesBeanClass(epstart=request.epstart, epend=request.epend)
            enlaces=[] # Respuesta
            
            # Recuperamos la pagina de busqueda
            url = 'http://www.divxtotal2.net/?s="{nombreserie}"'.format(nombreserie=self.nombreserie)
            try:
                page, self.proxy = utilesplugins.toggleproxy(url, proxies=self.proxy)
            except Exception, e:
                raise e
            # # Parse pagina principal
            source = BeautifulSoup(page, "html.parser")
            buscar_list = source.find_all("table", {"class" : "table"})
    
            links = buscar_list[0].find_all("a") or None
            if links:
                link = links[0]
                self.logger.info("enlaces : {}".format(link['href']))
                return self.__getpagtitulo(link['href'])
                
            else:
                self.logger.warn("No encontramos de {}, no descargamos nada".format(self.nombreserie))
                return False
        # except Exception, e:
        #     utilesplugins.handlerLoggerException(self.logger,msg="Error en el plugin",level=logging.ERROR)
        #     utilesplugins.handlerLoggerException(self.logger,level=logging.ERROR)
        #     raise e


    def __getpagtitulo(self, urltitulo):
        enlaces=[] # Respuesta
        try:
            pageTitulo, self.proxy = utilesplugins.toggleproxy(urltitulo, proxies=self.proxy)
        except Exception, e:
            raise e
        # self.logger.debug("pagetitle : {}".format(pageTitulo))
        source = BeautifulSoup(pageTitulo, "html.parser")
        divfichseriecapitulos = source.find("div", {"class" : "fichseriecapitulos"})
        divCapitulos = divfichseriecapitulos.find_all("div",  {'class': re.compile('table*')})
        
        
        for dcap in divCapitulos:
            self.logger.info("Encontrada Temporada: {}".format(dcap.find_previous_sibling('h3').getText()))
            lineas = dcap.find_all('tr')
            self.logger.debug("lineas : {}".format(len(lineas)))
            for linea in lineas:
                cap = linea.find('a')
                tag = cap['href']
                episodeLink =self.__converterEpisode(cap.getText()) 
                if self._filterEpisode(episodeLink):
                    self.logger.info("Encontrada capitulo : {} {}".format(episodeLink, cap['href']))
                    response = ResponsePlugin(title=self.nombreserie, link=tag, episode=episodeLink)
                    enlaces.append(response)
                
                
        return enlaces        
    
    
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
    
    def __converterEpisode(self,episodeLink ) :
        if re.search(r"(\d{1,2}x\d\d)",episodeLink):
            self.logger.debug("converterEpisodie: {}".format('Se han encontrado "x"'))
            matches = re.search(r"(\d{1,2}x\d\d)",episodeLink)
            if matches:
                formatEpisode = matches.group(0)
                if len(formatEpisode)==4:
                    session=matches.group(0)[:1].zfill(2)
                    episode=matches.group(0)[-2:].zfill(2)
                else:
                    session=matches.group(0)[:2].zfill(2)
                    episode=matches.group(0)[-2:].zfill(2)
        self.logger.info("{}S{}E{}".format(self.quality, session, episode))            
        return "{}S{}E{}".format(self.quality, session, episode)

    ## Constructor
    def __init__(self, logger=None):
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
    



