#!/usr/bin/python
import logging
import urllib, urllib2
import sys,re
import bs4
from bs4 import BeautifulSoup


#Anexo el Directorio en donde se encuentra la clase a llamar
sys.path.append('..')
#Importo la Clase
from beans.pluginsBeans import RequestPluginBean, ResponsePluginBean
import utiles.pluginsUtiles as utiles


# Get an instance of a logger
# Incializamos en el init de la clase
logger = logging.getLogger(__name__)


class TorrentRapidHandlerClass(object):

    __URL_BUSCAR = "http://torrentrapid.com/buscar"
    __CALIDADES = {
		"HD" : "1469",
		"VO": "",
        "AL": "",
        "NR":"767"
	}

    def execute(self, requestBean):
        # Objeto de respuesta
        responseBean = ResponsePluginBean()
        link = self.__findSerie(requestBean)
        logger.info("link encontrado {}".format(link))   
        if not link:
            responseBean.error.error="0001"
            responseBean.error.desc="No se ha encontrado la serie"
            return responseBean;
        
        self.__findTorrent(link, requestBean)
            



    def __findTorrent(self, link, requestBean):
        
        sources=[]
        source, lastPage = self.__firstPage(link)
        sources.append(source)
        count = 2
        while count <= lastPage:
            sources.append(self.__otherPages(count, link))
            count = count + 1
            
        pass


    # Lo sacaremos de aqui
    def __firstPage(self, url):
        logger.debug("Buscando en {}".format(url))
        page = urllib.urlopen(url)
        #urllib.urlretrieve(url,"page["+self.nombreserie+"].html")
        source = BeautifulSoup(page, "html.parser")
        
        # recuperamos la ultima pagina
        pagination = source.find_all("ul", {"class": "pagination"})
        if len(pagination)==0:
            return 0
        itemlista = pagination[0].find_all("li")
        sItemLast=itemlista[-1].find("a")["href"]
        lastPage = sItemLast[sItemLast.rfind('/')+1:]
        # print "Utima posicion " + lastPage
        return source, int(lastPage)
        
    def __otherPages(self,position, url):
        url = url+"/pg/"+str(position)
        logger.debug("Buscando en %s",url)
        page = urllib.urlopen(url)
        logger.debug("Position {}".format(str(position)))
        # urllib.urlretrieve(url,"page["+self.nombreserie+position+"].html")
        source = BeautifulSoup(page, "html.parser")
        return source
    
    def __getlinks(self,source, requestBean):
        bProcced = True;
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        infos = buscar_list[0].find_all("div",{"class":"info"}) # esto es una lista
        valores=[]
        for info in infos:
            tag = info.a["href"]
            title = info.a["title"]
            
            episodeLink = requestBean._getEpisodeLink(title)
            self.logger.debug("Episodio sacado del link %s ", episodeLink)
            if self._filterEpisode(episodeLink):
                response = ResponsePlugin(title=self.nombreserie, link=tag, episode=episodeLink)
                valores.append(response)
            else:
                bProcced = False
        
        return bProcced, valores
   
   
    def _filterEpisode(self, episodeLink, requestBean):
        # Estos datos llegaran como...... NRS00E00
        
        logger.debug("[Filtrando] cap: %s entre %s y %s",episodeLink, requestBean.epstart, requestBean.epend)
        if (requestBean.epstart is None): #si no hay episodios lo enviamos todo
            self.logger.info("No hay etiqueta de episodios, se descarga todo ")
            return True 
        else:
            # Preparar datos
            epstartquality, epstartsession, epstartepisode = utiles.converterEpisode(requestBean.epstart)
            ependquality, ependsession, ependepisode = utiles.converterEpisode(requestBean.epend)
            eplinkquality, eplinksession, eplinkepisode = utiles.converterEpisode(episodeLink)
            
            inicio = int(epstartsession+epstartepisode) if epstartsession and epstartepisode else 0000
            final = int(ependsession+ependepisode) if ependsession and ependepisode else 9999
            elegido = int(eplinksession+eplinkepisode) if eplinksession and eplinkepisode else 0000
            
            if inicio <= elegido and final >= elegido:
                logger.info("[Aceptado] (%s) cap: %s para %s de %s",requestBean.title, episodeLink, requestBean.epstart, self.episodes.epend)
                return True
            else:
                self.logger.info("[Rechazado] (%s) cap: %s para %s de  %s ",self.nombreserie, episodeLink, self.episodes.epstart, self.episodes.epend)
                return False
   
   
    # Recuperamos el temporada y el episodio del link recuperado   
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
        return temporada, capitulo


    def __findSerie(self, requestBean):

        url = self.__URL_BUSCAR
        # Prepare the data
        tit=requestBean.title
        titulo = '"{0}"'.format(tit)
        if requestBean.quality in self.__CALIDADES:
            quality=self.__CALIDADES.get(requestBean.quality)
        else:
            quality=self.__CALIDADES.get(requestBean.quality)
        values = {'q' : titulo,"categoryIDR":quality, "ordenar":"Nombre", "inon":"Descendente"}
        logger.info("Buscamos {}".format(values))        
        data = urllib.urlencode(values)
        # Send HTTP POST request
        req = urllib2.Request(self.__URL_BUSCAR, data)
        page = urllib2.urlopen(req)
        source = BeautifulSoup(page, "html.parser")
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        enlaces = buscar_list[0].find_all("a") or None
        
        # ##### recuperamos el titulo preciso
        link = utiles.getPreciseTitle(enlaces,requestBean.title, requestBean.quality)
        return link


    ## Constructor
    def __init__(self, logger= logger):
        if (logger):
            self.logger = logger


if __name__ == "__main__":
    
    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)
    
    trhc = TorrentRapidHandlerClass()
    requestTry = RequestPluginBean(title="The Brave",quality="NR") 
    respuesta = trhc.execute(requestTry)
    print "Respuesta final {}".format(respuesta)
