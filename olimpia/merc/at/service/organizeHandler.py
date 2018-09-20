#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re, glob
import fnmatch
import logging
import subprocess
from logging.handlers import RotatingFileHandler


# reload(sys)  
# sys.setdefaultencoding('utf8')



class Organize(object):
    
    
    def restart_service(self):
        self.logger.info("Reinicio de los servicios")
        try:
            sudo_password = 'clon9897'
            fnull = open(os.devnull, 'w')
            cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE, stdin=fnull)
            # cmd2 = subprocess.Popen(['sudo','-S'] + ['sudo', 'service', 'minidlna', 'stop'], stdin=cmd1.stdout, stdout=subprocess.PIPE)
            cmd3 = subprocess.Popen(['sudo','-S'] + ['sudo', 'minidlnad', '-R', 'stop'], stdin=cmd1.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # cmd4 = subprocess.Popen(['sudo','-S'] + ['sudo', 'service', 'minidlna', 'start'], stdin=cmd1.stdout, stdout=subprocess.PIPE)
            output = cmd3.stdout.read().decode()
        except subprocess.CalledProcessError:
            # There was an error - command exited with non-zero code
            self.logger.error("Error en el processo de organizacion, reinicio del servidor dlna {} ".format(output))
        self.logger.info("Fin de reinicio de los servicios: {}".format(output))
        return output
    
    def proccess(self, urlData, urlMirror, delete=False):
        urlData = urlData if urlData.endswith('/') else "{}/".format(urlData)
        urlMirror = urlMirror if urlMirror.endswith('/') else "{}/".format(urlMirror)
        
        self.logger.info("Vamos a procesar la carpeta {0} para organizarlo en {1} y borraremos {2}".format(urlData, urlMirror, delete))
        
        if delete:
            self.deleteSymbolicsLinks(urlMirror)
        
        series = glob.glob(os.path.join(urlData,'*')) 
        series = filter(lambda f: os.path.isdir(f), series)
        for serie in series:
            self.prepare_proccess_serie(serie, urlMirror,delete=False)
        self.logger.info("Organizacion Terminada")
    
    
    def prepare_proccess_serie(self,urlDataSerie, urlMirrorPath, delete=False):
        # añadimos la barra al final de la ruta
        urlDataSerie = urlDataSerie if urlDataSerie.endswith('/') else "{}/".format(urlDataSerie)
        urlMirrorPath = urlMirrorPath if urlMirrorPath.endswith('/') else "{}/".format(urlMirrorPath)
        
        self.logger.debug("urlDataSerie : {} ".format(urlDataSerie))
        self.logger.debug("urlMirrorPath : {} ".format(urlMirrorPath))
        
        self.__proccess_serie(urlDataSerie, urlMirrorPath, delete)
        
        
    
    
    def __proccess_serie(self,urlDataSerie, urlMirrorPath, delete=False):
        self.logger.info("Serie {0} para organizarlo en {1}".format(urlDataSerie, urlMirrorPath))
        
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
                        self.logger.info("De {0} A {1}".format(file, os.path.join(dirpathmirror,filename)))
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
        
        
        cons_PATTERN = r"(_\d{3,4}_)"
        cons_PATTERNX = r"(\d{1,2}x\d\d)"
        cons_PATTERNVO = r"(\d{3,4})((VO))"
        cons_PATTERNCALIDADES = r"(\d{3,4})((720p|1024p))"
        cons_PATTERNCALIDADES2 = r"((720p|1024p))_(\d{3,4})"
        cons_PATTERNCAP = r"(Cap.|cap.)(\d{3,4})"
        
        
        self.logger.debug("build name to {dirName}:{fileName}".format(dirName=dirName, fileName=fileName))
        patternResponse = "S{session}E{episode}"
        session, episode = None, None
        ext = fileName.split(".")[-1]
        
        if re.search(cons_PATTERNCALIDADES2,fileName):         
            # Procesamiento de episodios especiales (recien llegados, etc)
            self.logger.info("converterEpisodie: {}".format('Se han encontrado calidades 2'))
            matches = re.search(cons_PATTERNCALIDADES2,fileName)
            if matches:
                formatEpisode = matches.group(3)
                self.logger.info("formatEpisode: matches : {}".format(formatEpisode))
                if len(formatEpisode)==3:
                   session=formatEpisode[:1].zfill(2)
                   episode=formatEpisode[-2:].zfill(2)
                else:
                    session=formatEpisode[:2].zfill(2)
                    episode=formatEpisode[-2:].zfill(2)
        
        elif re.search(cons_PATTERN,fileName):
            self.logger.info("converterEpisodie: {}".format('Se han encontrado guiones'))
            matches = re.search(cons_PATTERN,fileName)
            if matches:
                formatEpisode = matches.group(0)[1:-1]
                if len(formatEpisode)==3:
                    session=formatEpisode[:1].zfill(2)
                    episode=formatEpisode[-2:].zfill(2)
                else:
                    session=formatEpisode[:2].zfill(2)
                    episode=formatEpisode[-2:].zfill(2)
        elif re.search(cons_PATTERNX,fileName):
            self.logger.info("converterEpisodie: {}".format('Se han encontrado "x"'))
            matches = re.search(cons_PATTERNX,fileName)
            if matches:
                formatEpisode = matches.group(0)
                if len(formatEpisode)==4:
                    session=matches.group(0)[:1].zfill(2)
                    episode=matches.group(0)[-2:].zfill(2)
                else:
                    session=matches.group(0)[:2].zfill(2)
                    episode=matches.group(0)[-2:].zfill(2)
        
        elif re.search(cons_PATTERNVO,fileName):         
            # Procesamiento de episodios especiales (VO, etc)
            self.logger.info("converterEpisodie: {}".format('Se han encontrado VO'))
            matches = re.search(cons_PATTERNVO,fileName)
            if matches:
                formatEpisode = matches.group(1)
                self.logger.info("formatEpisode: matches : {}".format(formatEpisode))
                if len(formatEpisode)==3:
                   session=formatEpisode[:1].zfill(2)
                   episode=formatEpisode[-2:].zfill(2)
                else:
                    session=formatEpisode[:2].zfill(2)
                    episode=formatEpisode[-2:].zfill(2)
        
                    
        elif re.search(cons_PATTERNCALIDADES,fileName):         
            # Procesamiento de episodios especiales (recien llegados, etc)
            self.logger.info("converterEpisodie: {}".format('Se han encontrado calidades'))
            matches = re.search(cons_PATTERNCALIDADES,fileName)
            if matches:
                formatEpisode = matches.group(1)
                self.logger.info("formatEpisode: matches : {}".format(formatEpisode))
                if len(formatEpisode)==3:
                   session=formatEpisode[:1].zfill(2)
                   episode=formatEpisode[-2:].zfill(2)
                else:
                    session=formatEpisode[:2].zfill(2)
                    episode=formatEpisode[-2:].zfill(2)
                    
        elif re.search(cons_PATTERNCAP,fileName):         
            # Procesamiento de episodios especiales (Pocoyo, etc)
            self.logger.info("converterEpisodie: {}".format('Se han encontrado Cap'))
            matches = re.search(cons_PATTERNCAP,fileName)
            if matches:
                formatEpisode = matches.group(2)
                self.logger.info("formatEpisode: matches : {}".format(formatEpisode))
                if len(formatEpisode)==3:
                   session=formatEpisode[:1].zfill(2)
                   episode=formatEpisode[-2:].zfill(2)
                else:
                    session=formatEpisode[:2].zfill(2)
                    episode=formatEpisode[-2:].zfill(2)
    
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
            # Get an instance of a logger
            self.logger = logging.getLogger(__name__)
