#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



class Common():
    
    def __str__(self):
        return self.__unicode__()


class Down(Common):
    
    id_ficha = ''
    nombre = ''
    quality = ''
    ep_start = ''
    ep_end = ''
    plugins =[]

    def __unicode__(self):
        return "{} - [{}-{}]".format(self.nombre, self.ep_start,self.ep_start)


class Plugins(Common):
    
    name=''
    file=''
    clazz=''
    active=False
    
    def __unicode__(self):
        return "{} - [{}]".format(self.name, self.active)


class ResponsePlugin(Common):
    
    def __init__(self, title=None, link=None,episode=None):
        self.title = title
        self.link=link
        self.episode=episode
        
    def __unicode__(self):
        x=[]
        if self.title:
            x.append('title={0}'.format(self.title))
        if self.link:
            x.append('link={0}'.format(self.link))
        if self.episode:
            x.append('episode={0}'.format(self.episode))
        return ' '.join(x)