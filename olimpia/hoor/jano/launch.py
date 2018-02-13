#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



# n Series
# u Author
# u Torrent


class DownObject:
    
    nombre = ''
    quality = ''
    ep_start = ''
    ep_end = ''
    plugins =[]



class SearchLaunch:
 
    
    def execute(self, downObject):
        
        logger.debug("downObject {downObject}".format(downObject=downObject))
        logger.debug("downObject. plugins {plugins}".format(plugins=downObject.plugins))
            
        return None;