#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time, re, logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def getPreciseTitle(enlaces, titulo, quality="NR"):
    if enlaces:
        # Pillamos el primer enlace
        enlace = enlaces[0]
        # Hemos encontrado enlaces....
        # ahora vamos ajustar el enlace mas exacto
        for enl in enlaces:
            tit_consegido = __getTitleLink(enl,quality)
            logger.debug("Titulo Encontrado : {} vs {} == {}  ".format(tit_consegido.upper(), titulo.upper(), tit_consegido.upper() == titulo.upper()))
            if tit_consegido.upper() == titulo.upper():
                logger.debug("Titulo Exacto Encontrado : {}".format(tit_consegido))
                enlace = enl
                break;
        
        url=enlace["href"] or None
        logger.debug("Hemos encontrado la url {}".format(url))
        return url
    else:
        logger.debug("No encontramos {}, no descargamos nada".format(titulo))
        return False

def __getTitleLink(enl, quality):
    titulo_enlace = enl['title']
    if quality=="HD" or quality=="VO" or quality=="AL":
        pattern = "(\S+)\s(\S+)\s(\S+)(.*)(-.Temporada.\d)"
        tit_consegido = re.search(pattern,titulo_enlace).group(4).strip()
    else:
        pattern = "(\S+)\s(\S+)(.*)(-.Temporada.\d)"
        tit_consegido = re.search(pattern,titulo_enlace).group(3).strip()
    
    return tit_consegido


def converterEpisode(episode): # El formato que recuperamos es por defecto NRS00E00
    if episode is None:
        return None, None, None # tenemos que itererar todo lo que enviamos!!!
    quality = episode[:2] or None
    session = episode[3:5] or None
    episode = episode[-2:] or None
    return quality, session, episode