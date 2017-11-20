#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


def getfilesConfigJson(url, logger = None):
    with open(url, 'r') as file:
        data = json.load(file)
    return data

# Obsoleto
def dic_2_obj(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, dic_2_obj(j))
        elif isinstance(j, seqs):
            setattr(top, i, type(j)(dic_2_obj(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top
    
# Obsoleto
def getObjectToJson_manual(url):
    with open(url, 'r') as file:
        data = json.load(file)
    return dic_2_obj(data)


def getObjectToJson(url):
    try:
        from types import SimpleNamespace as Namespace
    except ImportError:
        # Python 2.x fallback
        from argparse import Namespace
    
    with open(url, 'r') as file:
        x = json.load(file, object_hook=lambda d: Namespace(**d))

    return x
    
    
def getObject(object, valor):
    return getattr(object, valor) if hasattr(object, valor)  else None
    
def switch(operaciones, valor,*parametros):
    return operaciones[valor](*parametros)    
    
    
def converterEpisode(episode): # El formato que recuperamos es por defecto NRS00E00
    if episode is None:
        return None, None, None # tenemos que itererar todo lo que enviamos!!!
    quality = episode[:2] or None
    session = episode[3:5] or None
    episode = episode[-2:] or None
    return quality, session, episode