#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)



def buildName(fileName, dirName):
    
    
    cons_PATTERN = r"(_\d{3,4}_)"
    cons_PATTERNX = r"(\d{1,2}x\d\d)"
    cons_PATTERNVO = r"(\d{3,4})((VO))"
    cons_PATTERNCALIDADES = r"(\d{3,4})((720p|1024p))"
    cons_PATTERNCAP = r"(Cap.|cap.)(\d{3,4})"
    
    
    logger.debug("build name to {dirName}:{fileName}".format(dirName=dirName, fileName=fileName))
    patternResponse = "S{session}E{episode}"
    session, episode = None, None
    ext = fileName.split(".")[-1]
    
    if re.search(cons_PATTERN,fileName):
        logger.info("converterEpisodie: {}".format('Se han encontrado guiones'))
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
        logger.info("converterEpisodie: {}".format('Se han encontrado "x"'))
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
        logger.info("converterEpisodie: {}".format('Se han encontrado VO'))
        matches = re.search(cons_PATTERNVO,fileName)
        if matches:
            formatEpisode = matches.group(1)
            logger.info("formatEpisode: matches : {}".format(formatEpisode))
            if len(formatEpisode)==3:
               session=formatEpisode[:1].zfill(2)
               episode=formatEpisode[-2:].zfill(2)
            else:
                session=formatEpisode[:2].zfill(2)
                episode=formatEpisode[-2:].zfill(2)
    
                
    elif re.search(cons_PATTERNCALIDADES,fileName):         
        # Procesamiento de episodios especiales (recien llegados, etc)
        logger.info("converterEpisodie: {}".format('Se han encontrado calidades'))
        matches = re.search(cons_PATTERNCALIDADES,fileName)
        if matches:
            formatEpisode = matches.group(1)
            logger.info("formatEpisode: matches : {}".format(formatEpisode))
            if len(formatEpisode)==3:
               session=formatEpisode[:1].zfill(2)
               episode=formatEpisode[-2:].zfill(2)
            else:
                session=formatEpisode[:2].zfill(2)
                episode=formatEpisode[-2:].zfill(2)
            
    elif re.search(cons_PATTERNCAP,fileName):         
        # Procesamiento de episodios especiales (Pocoyo, etc)
        logger.info("converterEpisodie: {}".format('Se han encontrado Cap'))
        matches = re.search(cons_PATTERNCAP,fileName)
        if matches:
            formatEpisode = matches.group(0)
            logger.info("formatEpisode: matches : {}".format(formatEpisode))
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
    
    
    
    
    
# fileName = "MarvelsAS501_502VOSE_720p.mmg"
fileName = "Pocoyo - Temporada 1 [SatRIP][Cap.103-104][Spanish][www.newpct.com]/Pocoyo -  Temporada 1 [SatRIP][Cap.104][Spanish][www.newpct.com].avi"

cons_PATTERNCAP = r"(Cap.|cap.)(\d{3,4})"
matches = re.search(cons_PATTERNCAP,fileName)
if matches:
    print matches.group(2)


resp = buildName(fileName, "Session 5")
print resp;