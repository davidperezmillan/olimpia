#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from hoor.models import Ficha, Capitulo, Descarga

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# privado
def get_series_slope(user, estado):
    slope_series = []
     ## Recuperamos todas las series del usuario
    fichas = Ficha.objects.filter(author=user).filter(estado=estado)
    
    for ficha in fichas:
        logger.debug("ficha : {}".format(ficha))
        obj = Capitulo.objects.filter(ficha=ficha).filter(visto=False).filter(descargado=True).order_by('capitulo')[:1]
        if obj:
            logger.debug("captitulos pendientes : {}".format(obj[0].ficha.nombre))
            slope_series.append(obj)
    # slope_series = Vistos.objects.filter(temporada__ficha__author=request.user).filter(visto=False)  # No es broma, se puede seguir la tabla para arriba  """temporada__ficha__author"""
    logger.debug("slope_series : {}".format(slope_series))
    return slope_series;

# privado
def get_session_slope(user, estado):
    slope_series = []
     ## Recuperamos todas las series del usuario
    fichas = Ficha.objects.filter(author=user).filter(estado=estado)
    
    for ficha in fichas:
        logger.debug("ficha : {}".format(ficha))
        obj = Capitulo.objects.filter(ficha=ficha).filter(visto=False).order_by('capitulo')[:1]
        if obj:
            logger.debug("captitulos pendientes : {}".format(obj[0].ficha.nombre))
            slope_series.append(obj)
    # slope_series = Vistos.objects.filter(temporada__ficha__author=request.user).filter(visto=False)  # No es broma, se puede seguir la tabla para arriba  """temporada__ficha__author"""
    logger.debug("slope_series : {}".format(slope_series))
    return slope_series;

    
# def get_series_ficha_old(ficha):
#     slope_series_ficha= Capitulo.objects.filter(ficha=ficha).filter(visto=False).order_by('capitulo')
#     logger.debug("captitulos pendientes : {}".format(slope_series_ficha))
#     return slope_series_ficha;

# privado
def get_series_ficha(ficha):
    slope_series_ficha = []
    temporadas =  Capitulo.objects.values('temporada').distinct().filter(ficha=ficha).order_by('temporada')
    for temporada in temporadas:
        my_dict = {'temporada':temporada, 'capitulos' : Capitulo.objects.filter(ficha=ficha).filter(temporada=temporada['temporada']).order_by('capitulo')}
        slope_series_ficha.extend([my_dict])
        
    logger.debug("Temporadas pendientes : {}".format((slope_series_ficha)))
    # slope_series_ficha= Capitulos.objects.filter(ficha=ficha).filter(visto=False).order_by('temporada','capitulo')
    # logger.debug("captitulos pendientes : {}".format(slope_series_ficha))
    return slope_series_ficha;


# privado
def get_series_down_ficha(ficha):
    logger.debug("Estamos en get_series_down_ficha")
    down_series_ficha=Descarga.objects.filter(ficha=ficha)
    logger.debug("get_series_down_ficha: {}".format(down_series_ficha))
    return down_series_ficha[0] if down_series_ficha else None

 