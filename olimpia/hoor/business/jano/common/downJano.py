#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



class Common():
    
    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self

class Down(Common):
    
    id_ficha = ''
    nombre = ''
    quality = ''
    ep_start = ''
    ep_end = ''
    plugins =[]

    def __unicode__(self):
        return "{} - [{}-{}]".format(self.nombre, self.ep_start,self.ep_end)


class Plugins(Common):
    
    name=''
    file=''
    clazz=''
    active=False
    
    def __unicode__(self):
        return "{} - [{}]".format(self.name, self.active)


class RequestPlugin(Common):

    def __str__(self):
        x=[]
        if self.title:
            x.append('title={0}'.format(self.title))
        if self.epstart:
            x.append('epstart={0}'.format(self.epstart))
        if self.epend:
            x.append('epend={0}'.format(self.epend))
        if self.quality:
            x.append('quality={0}'.format(self.quality))  
        return ' '.join(x)

    def __init__(self,title=None, epstart="NRS00E00", epend=None, quality=''):
        self.title=title
        self.epstart=epstart
        self.epend=epend if epend is not None else "{0}S99E99".format(self.epstart[:2])
        self.quality=quality
        
        
        
class ResponsePlugin(Common):
    
    def __str__(self):
        x=[]
        if self.title:
            x.append('title={0}'.format(self.title))
        if self.link:
            x.append('link={0}'.format(self.link))
        if self.torrent:
            x.append('torrent={0}'.format(self.torrent))
        if self.episode:
            x.append('episode={0}'.format(self.episode))
        return ' '.join(x)
        
    def __init__(self, title=None, link=None,torrent=None,episode=None):
        self.title = title
        self.link=link
        self.torrent=torrent
        self.episode=episode