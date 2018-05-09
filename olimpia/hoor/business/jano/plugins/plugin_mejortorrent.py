#!/usr/bin/python
import logging
import urllib, urllib2
import sys,re
import bs4
from bs4 import BeautifulSoup


from hoor.business.jano.beans.pluginsBeans import RequestPluginBean, ResponsePluginBean, DataResponseBean, ErrorResponseBean
import hoor.business.jano.utiles.pluginsUtiles as utiles


# Get an instance of a logger
# Incializamos en el init de la clase
logger = logging.getLogger(__name__)



class EpisodiesBeanClass(object):
    
    def __init__(self,epstart=None, epend=None):
        self.epstart=epstart
        self.epend=epend



class MejorTorrentHandlerClass(object):
   
   
    # Podemos incluir el proxy pero tenemos una lista que podemos utilzar en el utiles 
    # o no enviar nada y cogera los de por defecto
    
    # proxy = { 
    #       "http"  : "http://190.12.102.205:8080", 
    #     #   "https" : "http://190.12.102.205:8080"
    #     #   "ftp"   : "http://190.12.102.205:8080"
    #     }
    
    
    proxy = utiles.proxies
   
    # EJECUTOR   
    def execute(self,request, filter=False):
        # try:
            self.logger.info(" ---> Processando con el plugin .... {0} -- {1}".format(request, filter))
    
            self.episodes=EpisodiesBeanClass(epstart=request.epstart, epend=request.epend)
            # Preparar datos
            epstartquality, epstartsession, epstartepisode = utiles.converterEpisode(self.episodes.epstart)
            ependquality, ependsession, ependepisode = utiles.converterEpisode(self.episodes.epend)
            
            self.nombreserie=request.title
            self.quality=epstartquality if epstartquality else ependquality
            
            enlaces=[] # Respuesta
            
            
            # Recuperamos la pagina de busqueda
            url = 'http://www.mejortorrent.com/secciones.php?sec=buscador&valor={nombreserie}'.format(nombreserie=self.nombreserie)
            try:
                page, self.proxy = utiles.toggleproxy(url, proxies=self.proxy)
                # utiles.pintarFicheroHtml(page.encode('utf-8').strip(),"buscar")
            except Exception, e:
                raise e
            # # Parse pagina principal
            source = BeautifulSoup(page, "html.parser")
            
            
            # Primero tenemos que recuperar todas las temporadas de la serie
            # segun la calidad que deseemos
            if self.quality!="NR":
                findPattern = r"(?i)\d{{1,}}-{}.*temporada-.{{4,5}}.html".format(self.nombreserie.replace(" ","."))
            else:
                findPattern = r"(?i)\d{{1,}}-{}.*temporada.html".format(self.nombreserie.replace(" ","."))
            self.logger.info("Patron de busqueda {}".format(findPattern))
            links = source.find_all("a",{"href":re.compile(findPattern)}) or None
            valores=[]
            for link in links:
                titulo_enlace = link.text
                pattern = r"(?i)(\d+)(.{1,}temporada)"
                sessionRecuperada=re.search(pattern,titulo_enlace).group(1).strip()
                
                # if sessionRecuperada and int(sessionRecuperada)>=int(epstartsession):
                if sessionRecuperada:
                    self.logger.info("Session recuperada: http://www.mejortorrent.com/{}".format(link["href"]))
                    valores.extend(self.__getSession(link["href"]))
            return valores
            
    def __getSession(self, url):
        url =  "http://www.mejortorrent.com/{}".format(url)
        try:
            page, self.proxy = utiles.toggleproxy(url, proxies=self.proxy)
            # utiles.pintarFicheroHtml(page.encode('utf-8').strip(),"session")
        except Exception, e:
            raise e
            
        source = BeautifulSoup(page, "html.parser")    
        
        findPattern = r"serie-episodio"
        links = source.find_all("a",{"href":re.compile(findPattern)}) or None
        valores=[]
        for link in links:
            rangos = link.text
            pattern = r"(\d{1,2})x(\d{1,2})"
            temporada = re.search(pattern,rangos).group(1)
            capitulo = re.search(pattern,rangos).group(2)
            episodeLink="{0}S{1}E{02}".format(self.quality,temporada.zfill(2),capitulo.zfill(2))
           
            if self.__filterEpisode(episodeLink):
                response = self.__getPageDownload(link["href"])
                response.data.episode=episodeLink
                valores.append(response)
        return valores



    
    
    def __filterEpisode(self, episodeLink):
        # Estos datos llegaran como...... NRS00E00
        
        self.logger.debug("[Filtrando] cap: %s entre %s y %s",episodeLink, self.episodes.epstart, self.episodes.epend)
        if (self.episodes is None): #si no hay episodios lo enviamos todo
            self.logger.info("No hay etiqueta de episodios, se descarga todo ")
            return True 
        else:
            
            # Preparar datos
            epstartquality, epstartsession, epstartepisode = utiles.converterEpisode(self.episodes.epstart)
            ependquality, ependsession, ependepisode = utiles.converterEpisode(self.episodes.epend)
            eplinkquality, eplinksession, eplinkepisode = utiles.converterEpisode(episodeLink)
            
            inicio = int(epstartsession+epstartepisode) if epstartsession and epstartepisode else 0000
            final = int(ependsession+ependepisode) if ependsession and ependepisode else 9999
            elegido = int(eplinksession+eplinkepisode) if eplinksession and eplinkepisode else 0000
            
            if inicio <= elegido and final >= elegido:
                self.logger.info("[Aceptado] (%s) cap: %s para %s de %s",self.nombreserie, episodeLink, self.episodes.epstart, self.episodes.epend)
                return True
            else:
                self.logger.info("[Rechazado] (%s) cap: %s para %s de  %s ",self.nombreserie, episodeLink, self.episodes.epstart, self.episodes.epend)
                return False
    
    
    
    def __getPageDownload(self, url):
        
        url =  "http://www.mejortorrent.com/{}".format(url) 
        try:
            page, self.proxy = utiles.toggleproxy(url, proxies=self.proxy)
            # utiles.pintarFicheroHtml(page.encode('utf-8').strip(),"down")
        except Exception, e:
            raise e
            
        source = BeautifulSoup(page, "html.parser")   
        findPattern = r"(?i)(sec=descargas).*(id=\d+)"
        link = source.find_all("a",{"href":re.compile(findPattern)})[0] or None
        
    
        url =  "http://www.mejortorrent.com/{}".format(link["href"]) 
        try:
            page, self.proxy = utiles.toggleproxy(url, proxies=self.proxy)
            # utiles.pintarFicheroHtml(page.encode('utf-8').strip(),"down")
        except Exception, e:
            raise e
            
        source = BeautifulSoup(page, "html.parser")  
        findPattern = r"(?i)(/uploads/)"
        link = source.find_all("a",{"href":re.compile(findPattern)})[0] or None
        tag =  "http://www.mejortorrent.com/{}".format(link["href"])
        # Construimos la respuesta
        response = ResponsePluginBean()
        data = DataResponseBean(title=self.nombreserie, link=tag)
        response.data=data
        return response
        

    ## Constructor
    def __init__(self, logger=None):
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
    

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)
    

    requestTry = RequestPluginBean(title="The Brave",quality="NR", epstart="NRS01E010") 
    trhc = MejorTorrentHandlerClass()
    respuesta = trhc.execute(requestTry)
    for item in respuesta:
        print "Respuesta final {}".format(item)


