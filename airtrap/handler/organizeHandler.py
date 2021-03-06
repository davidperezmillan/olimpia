#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re, glob
import fnmatch
import logging
from logging.handlers import RotatingFileHandler
import utilities.constantes as cons

reload(sys)  
sys.setdefaultencoding('utf8')

basepathlog = cons.basepathlog
loggername = 'organize'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
loggerfilename = basepathlog+loggername+'.log'

class Organize(object):
    
    
    def proccess(self, urlData, urlMirror, delete=False):
        urlData = urlData if urlData.endswith('/') else "{}/".format(urlData)
        urlMirror = urlMirror if urlMirror.endswith('/') else "{}/".format(urlMirror)
        
        self.logger.info("Vamos a procesar {0} para organizarlo en {1}".format(urlData, urlMirror))
        
        if delete:
            self.deleteSymbolicsLinks(urlMirror)
        
        series = glob.glob(os.path.join(urlData,'*')) 
        series = filter(lambda f: os.path.isdir(f), series)
        for serie in series:
            self.proccess_serie(serie, urlMirror,delete=False)
        self.logger.info("Organizacion Terminada")
    
    def proccess_serie(self,urlDataSerie, urlMirrorPath, delete=False):
        urlDataSerie = urlDataSerie if urlDataSerie.endswith('/') else "{}/".format(urlDataSerie)
        urlMirrorPath = urlMirrorPath if urlMirrorPath.endswith('/') else "{}/".format(urlMirrorPath)
        
        self.logger.info("Vamos a procesar {0} para organizarlo en {1}".format(urlDataSerie, urlMirrorPath))
        
        # create folder structure 
        seriePath = os.path.basename(os.path.normpath(urlDataSerie))
        outputpath = os.path.join(urlMirrorPath,seriePath)
        # outputpath = "{urlMirrorPath}/{seriePath}/".format(urlMirrorPath=urlMirrorPath,seriePath=seriePath)
        
        includes = ['*.avi', '*.mkv','*.mp*'] # for files only
        includes = r'|'.join([fnmatch.translate(x) for x in includes])
        # excludes = ['Session'] # for dirs and files
        # excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'
        
        
        if delete:
            self.deleteSymbolicsLinks(outputpath)
        
        
        
        dirsSessions = glob.glob(os.path.join(urlDataSerie,'Session*'))
        # print dirsSessions
        for dirSession in dirsSessions:
            self.logger.debug("directorio a tratar {0}".format(dirSession))
            for root, dirs, files in os.walk(dirSession):
                try:
                    # exclude/include files
                    files = [os.path.join(root, f) for f in files]
                    files = [f for f in files if re.match(includes, f)]
                    
                    for file in files:
                        filename = os.path.basename(file)
                        # new structure folder
                        dirpathmirror = os.path.join(dirSession.replace(urlDataSerie[:-1], outputpath)) # quitamos la barra del final
                        self.logger.debug("De {0} remplazmos {1} por {2} = {3}".format(dirSession,urlDataSerie[:-1],outputpath, dirpathmirror))
                        if not os.path.exists(dirpathmirror):
                            os.makedirs(dirpathmirror)  # create the dir if not exists
                        # self.__copyDirectory(dirSession,dirpathmirror)
                        serieName = dirpathmirror.split("/")[-2]
                        filename = self.buildName(filename, serieName)
                        self.logger.info("{0} - {1}".format(file, os.path.join(dirpathmirror,filename)))
                        os.symlink(file, os.path.join(dirpathmirror,filename))
                        # os.symlink(file, os.path.join(dirpathmirror,filename))
                except Exception, e:
                    self.logger.warn("[Warn] {0} :  {1}".format(e, os.path.join(dirpathmirror,filename)))
            
        self.logger.info("Organizacion Terminada {0}".format(urlDataSerie))    
        

    def deleteSymbolicsLinks(self,urlMirror):
        self.logger.info("Procedemos a borrar el directorio espejo {0}".format(urlMirror))
        for root, dirs, files in os.walk(urlMirror):
            files = filter(lambda f:os.path.islink(os.path.join(root, f)),files)
            for f in files:
                os.unlink(os.path.join(root, f)) 
        #  borrado de directorios
        for root, dirs, files in  reversed(list(os.walk(urlMirror))):
            dirs.sort(reverse=False)
            for dir in dirs:
                directorio = os.path.join(root,dir)
                if not os.listdir(directorio):
                    self.logger.info("Diretorio {0} esta vacio y sera borrado".format(directorio))
                    os.rmdir(directorio)

    def buildName(self,fileName, dirName):
        self.logger.debug("build name to {dirName}:{fileName}".format(dirName=dirName, fileName=fileName))
        patternResponse = "S{session}E{episode}"
        session, episode = None, None
        ext = fileName.split(".")[-1]
    
        matches = re.search(r"(_\d{3,4}_)",fileName)
        if matches:
            formatEpisode = matches.group(0)[1:-1]
            if len(formatEpisode)==3:
                session=formatEpisode[:1].zfill(2)
                episode=formatEpisode[-2:].zfill(2)
            else:
                session=formatEpisode[:2].zfill(2)
                episode=formatEpisode[-2:].zfill(2)
        
        matches = re.search(r"(\d{1,2}x\d\d)",fileName)
        if matches:
            formatEpisode = matches.group(0)
            if len(formatEpisode)==4:
                session=matches.group(0)[:1].zfill(2)
                episode=matches.group(0)[-2:].zfill(2)
            else:
                session=matches.group(0)[:2].zfill(2)
                episode=matches.group(0)[-2:].zfill(2)
    
        if session and episode:
            fullEpisode = patternResponse.format(session=session,episode=episode)
            response = "{dirname}_{episode}.{ext}".format(dirname=dirName.strip().replace(' ', ''), episode=fullEpisode, ext=ext)
        else:
            response = fileName
        return response


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
            
            #self.ch = logging.StreamHandler()
            #self.ch.setFormatter(self.formatter)        
            #self.logger.addHandler(self.ch)

