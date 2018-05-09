#!/usr/bin/python
import logging
# import urllib, urllib2
import sys,re
import bs4
from bs4 import BeautifulSoup


from hoor.business.jano.beans.pluginsBeans import RequestPluginBean, ResponsePluginBean, DataResponseBean, ErrorResponseBean
import hoor.business.jano.utiles.pluginsUtiles as utiles


# Get an instance of a logger
# Incializamos en el init de la clase
logger = logging.getLogger(__name__)


class TorrentRapidHandlerClass(object):

    __URL_BUSCAR = "http://torrentrapid.com/buscar"
    __CALIDADES = {
		"HD" : "1469",
		"VO": "",
        "AL": "",
        "NR":"767",
	}
    proxy = None

    def execute(self, requestBean):
        # Objeto de respuesta
        self.requestBean=requestBean
        return self.__findSerie()


    def __findSerie(self):

        url = self.__URL_BUSCAR
        # Prepare the data
        tit=self.requestBean.title
        titulo = '"{0}"'.format(tit)
        if self.requestBean.quality in self.__CALIDADES:
            quality=self.__CALIDADES.get(self.requestBean.quality)
        else:
            quality=self.__CALIDADES.get(self.requestBean.quality)
        values = {'q' : titulo,"categoryIDR":quality, "ordenar":"Nombre", "inon":"Descendente"}
        logger.info("Buscamos {}".format(values))  
        ''' INIT proxys '''
        # data = urllib.urlencode(values)
        # # Send HTTP POST request
        # req = urllib2.Request(self.__URL_BUSCAR, data)
        # page = urllib2.urlopen(req)
        ''' END proxys'''
        page, proxyResponse = utiles.toggleproxy(url, values=values, proxies=self.proxy, methods=["urllib"])
        
        source = BeautifulSoup(page, "html.parser")
       
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        enlaces = buscar_list[0].find_all("a") or None
        
        # ##### recuperamos el titulo preciso
        link = utiles.getPreciseTitle(enlaces,self.requestBean.title, self.requestBean.quality)
        
        logger.info("link encontrado {}".format(link))   
        if not link:
            response = ResponsePluginBean()
            response.error.error="0001"
            response.error.desc="No se ha encontrado la serie"
            return response;
        
        return self.__findTorrent(link)
        
    def __findTorrent(self, link):
        
        resp, lastPage = self.__firstPage(link)
        if lastPage:
            count = 2
            while count <= lastPage:
                resp.extend(self.__otherPages(count, link))
                count = count + 1
        
        logger.info("Valores encontrado {}".format(resp))
        return resp

    # Lo sacaremos de aqui
    def __firstPage(self, url):
        logger.debug("Buscando en {}".format(url))
        ''' INIT proxys '''
        # page = urllib.urlopen(url)
        ''' END proxys'''
        #urllib.urlretrieve(url,"page["+self.nombreserie+"].html")
        page, proxyResponse = utiles.toggleproxy(url, proxies=self.proxy, methods=["urllib"])
        source = BeautifulSoup(page, "html.parser")
        
        # recuperamos la ultima pagina
        pagination = source.find_all("ul", {"class": "pagination"})
        if len(pagination)==0:
            lastPage=0
        else:
            itemlista = pagination[0].find_all("li")
            sItemLast=itemlista[-1].find("a")["href"]
            lastPage = sItemLast[sItemLast.rfind('/')+1:]
            
        logger.info("Posicion String : {}".format(lastPage))
        
        #  recuperamos los enlaces que tenemos en esta pagina
        valores = self.__getlinks(source)

        return valores, int(lastPage)
        
    def __otherPages(self,position, url):
        url = url+"/pg/"+str(position)
        logger.debug("Buscando en %s",url)
        ''' INIT proxys '''
        # page = urllib.urlopen(url)
        ''' END proxys'''
        #urllib.urlretrieve(url,"page["+self.nombreserie+"].html")
        page, proxyResponse = utiles.toggleproxy(url, proxies=self.proxy, methods=["urllib"])
        logger.debug("Position {}".format(str(position)))
        # urllib.urlretrieve(url,"page["+self.nombreserie+position+"].html")
        source = BeautifulSoup(page, "html.parser")
        
        #  recuperamos los enlaces que tenemos en esta pagina
        valores = self.__getlinks(source)
        return valores
    
    def __getlinks(self,source):
        buscar_list = source.find_all("ul", {"class" : "buscar-list"})
        infos = buscar_list[0].find_all("div",{"class":"info"}) # esto es una lista
        valores=[]
        for info in infos:
            tag = info.a["href"]
            title = info.a["title"]
            episodeLink, valid = self.__filterEpisode(title)
            if valid:
                ''' INIT proxys '''
                # req = urllib2.Request(tag) 
                # soup = BeautifulSoup(urllib2.urlopen(req), "html.parser")
                ''' END proxys'''

                
                page, proxyResponse = utiles.toggleproxy(tag, proxies=self.proxy, methods=["urllib"])
                soup = BeautifulSoup(page, "html.parser")
                redirMatch = re.match(r'.*?window\.location\.\href\s*=\s*\"([^"]+)\"', str(soup), re.M|re.S)
                if(redirMatch and "http" in redirMatch.group(1)):
                    tag = redirMatch.group(1)
                else:
                    tag = soup.title.string.encode('ascii', 'ignore').strip().replace('\n','')

                response = ResponsePluginBean()
                data = DataResponseBean(title=self.requestBean.title, link=tag, episode=episodeLink)
                response.data=data
                valores.append(response)
        return valores
   
    def __filterEpisode(self,titleLink):
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
        episodeLink="{0}S{1}E{02}".format(self.requestBean.quality,temporada,capitulo)
        
        # Estos datos llegaran como...... NRS00E00
        logger.debug("[Filtrando] cap: %s entre %s y %s",episodeLink, self.requestBean.epstart, self.requestBean.epend)
        if (self.requestBean.epstart is None): #si no hay episodios lo enviamos todo
            self.logger.info("No hay etiqueta de episodios, se descarga todo ")
            return True 
        else:
            # Preparar datos
            epstartquality, epstartsession, epstartepisode = utiles.converterEpisode(self.requestBean.epstart)
            ependquality, ependsession, ependepisode = utiles.converterEpisode(self.requestBean.epend)
            eplinkquality, eplinksession, eplinkepisode = utiles.converterEpisode(episodeLink)
            
            inicio = int(epstartsession+epstartepisode) if epstartsession and epstartepisode else 0000
            final = int(ependsession+ependepisode) if ependsession and ependepisode else 9999
            elegido = int(eplinksession+eplinkepisode) if eplinksession and eplinkepisode else 0000
            
            if inicio <= elegido and final >= elegido:
                logger.info("[Aceptado] ({}) cap: {} para {} de {}".format(self.requestBean.title, episodeLink, self.requestBean.epstart, self.requestBean.epend))
                return episodeLink,True
            else:
                self.logger.info("[Rechazado] ({}) cap: {} para {} de  {} ".format(self.requestBean.title, episodeLink, self.requestBean.epstart, self.requestBean.epend))
                return episodeLink,False
   
   

    ## Constructor
    def __init__(self, logger=logger):
        if (logger):
            self.logger = logger
        


if __name__ == "__main__":
    
    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)
    
    requestTry = RequestPluginBean(title="The Brave",quality="NR", epstart="NRS01E010") 
    trhc = TorrentRapidHandlerClass()
    respuesta = trhc.execute(requestTry)
    for item in respuesta:
        print "Respuesta final {}".format(item)
