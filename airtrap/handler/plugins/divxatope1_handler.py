#!/usr/bin/python
import logging
import urllib,urllib2
import re
from logging.handlers import RotatingFileHandler
from bs4 import BeautifulSoup

import sys



loggername = 'divxatope1_handler'
loggerfilename = loggername+'.log'
stdfilename = loggername+'.std'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"



class Divxatope1HandlerClass(object):
   
    
    
    def firstpage(self):
        url = "http://www.divxatope1.com/"+self.quality+"/"+self.nombreserie
        self.logger.info("Buscando en %s",url)
        page = urllib.urlopen(url)
        urllib.urlretrieve(url,"page["+self.nombreserie+"].html")
        source = BeautifulSoup(page, "html.parser")
        return source
        
    def otherPages(self,position):
        url = "http://divxatope1.com/"+self.quality+"/"+self.nombreserie+"//pg/"+str(position)
        page = urllib.urlopen(url)
        urllib.urlretrieve(url,"page["+self.nombreserie+position+"].html")
        source = BeautifulSoup(page, "html.parser")
        return source
    
    
    def getLastPage(self,source):
        pagination = source.find_all("ul", {"class": "pagination"})
        if len(pagination)==0:
            return 0
        itemlista = pagination[0].find_all("li")
        sItemLast=itemlista[-1].find("a")["href"]
        lastPage = sItemLast[sItemLast.rfind('/')+1:]
        # print "Utima posicion " + lastPage
        return int(lastPage)
    
    def getlinks(self,source):
        
        chapters = source.find_all("ul", {"class" : "chapters"})
        # self.logger.debug(chapters[0])
        infos=chapters[0].find_all("div",{"class":"chap-desc"}) # esto es una lista
        valores=[]
        for info in infos:
            # print info
            item = info.find_all("a",{"class":"chap-title"})
            tag = info.a["href"]
            
            title = info.a["title"]
            titulo = re.findall('(Temporada\s\d{1,}|Capitulo\s\d{1,})', title)
            
            self.logger.debug("titulo %s", str(titulo))
            
            for tit in titulo:
                if tit.startswith("Temporada"):
                    temporada = re.findall('\d{1,}', tit)[0].zfill(1)
                elif tit.startswith("Capitulo"):
                    capitulo= re.findall('\d{1,}', tit)[0].zfill(2)
            
            cap = temporada + capitulo
            
            
            # filtrado por capitulos y temporadas
            if self.filtrarCapitulos(cap):
                valores.append([cap, tag])
        
        return valores
        
    def filtrarCapitulos(self,tempCap):
        self.logger.debug("[Filtrando] cap: %d ",int(tempCap))
        if (self.episodios is None): #si no hay episodios lo enviamos todo
            self.logger.info("[No hay etiqueta de episodios ] %s",tempCap)
            return True 
        else:    
            inicioTag = self.episodios.get("inicio") or None
            if inicioTag is not None:
                inicioTemporada = str(inicioTag.get("temporada") or "1")
                inicioCapitulo = str(inicioTag.get("capitulo") or "00")
                inicio = int(inicioTemporada+inicioCapitulo.zfill(2))
                self.logger.debug("inicio : %d",inicio)
            else:
                inicio = 100
                self.logger.debug("inicio : %d",inicio)
               
            finTag = self.episodios.get("final") or None
            if finTag is not None:
                finTemporada = str(finTag.get("temporada") or "99")
                finCapitulos = str(finTag.get("capitulo") or "99")
                final = int(finTemporada+finCapitulos.zfill(2))
                self.logger.debug("Final : %d",final)
            else:
                final = 9999
                self.logger.debug("Final : %d",final)
                
            
            iCap = int(tempCap)
            
            if inicio <= iCap and final >= iCap:
                self.logger.info("[Aceptado] cap: %d %s",iCap, self.nombreserie)
                return True
            else:
                self.logger.debug("[Rechazado] cap: %d ",iCap)
                return False
            

                
        
        
    def getTorrentFiles(self,tag):
        
        url = tag[1]

        req = urllib2.Request(url) 
        soup = BeautifulSoup(urllib2.urlopen(req), "html.parser")
        redirMatch = re.match(r'.*?window\.location\.\href\s*=\s*\"([^"]+)\"', str(soup), re.M|re.S)
        if(redirMatch and "http" in redirMatch.group(1)):
            url = redirMatch.group(1)
            return url
        else:
            return soup.title.string.encode('ascii', 'ignore').strip().replace('\n','')
            
        # page2 = urllib.urlopen(url)
        # urllib.urlretrieve(url,'texto.html') 
        # source2 = BeautifulSoup(page2, "html.parser")
        # tag2 = source2.find("a",{"class": "btn-torrent"})['href']
        # return tag2   
        
    
    
    
    
    
    def execute(self, titulo, titles):
        self.logger.info(" ---> Processando con el plugin ....")
        self.logger.info("Titulos a buscar %s", titulo )
        
        self.nombreserie = titulo.replace(" ","-").lower() if titulo else None
        if self.nombreserie is None: return {}
        self.logger.info("Titulo formateado %s", self.nombreserie)
        quality = titles["quality"] if  "quality" in titles.keys() and titles["quality"] else None
        if quality=="HD":
            self.quality="descargar-seriehd"
        else:
            self.quality="series"
        self.episodios=titles["episodios"] if "episodios" in titles.keys() and titles["episodios"] else None
        
        fPage = self.firstpage()
        lastPage = self.getLastPage(fPage)
        
        valores = self.getlinks(fPage);
        self.logger.info("links recuperados/filtrados en la primera pagina %s" ,str(valores))
        
        
        count = 2
        while count <= lastPage:
            source = self.otherPages(count)
            valores.extend(self.getlinks(source))
            self.logger.info("links recuperados/filtrados en la primera pagina %d : %s" ,count,str(valores))
            count = count + 1
            
        self.logger.info("links recuperados/filtrados %s" ,str(valores))
        
        
        enlaces=[]
        for valor in valores:
            tagTorrent = self.getTorrentFiles(valor)
            self.logger.info("url torrent %s", tagTorrent)
            enlaces.append(tagTorrent)
            

        return enlaces




    ## Constructor
    def __init__(self, logger= None):
        
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(loggername)
            self.logger.setLevel(logging.DEBUG)
            self.formatter = logging.Formatter(defaulformatter)
        
            self.handler = RotatingFileHandler(loggerfilename, maxBytes=2000, backupCount=3)
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)
            
            self.ch = logging.StreamHandler()
            self.ch.setFormatter(self.formatter)        
            self.logger.addHandler(self.ch)
    
