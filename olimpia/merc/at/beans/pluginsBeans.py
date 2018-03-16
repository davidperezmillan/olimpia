#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time

class RequestPlugin(object):

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

    def __unicode__(self):
        return self.__str__()

    def __init__(self,title=None, epstart="NRS00E00", epend=None, quality=''):
        self.title=title
        self.epstart=epstart
        self.epend=epend if epend is not None else "{0}S99E99".format(self.epstart[:2])
        self.quality=quality
        
        
        
class ResponsePlugin(object):
    
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
        
    def __unicode__(self):
        return self.__str__()
        
            
    def __init__(self, title=None, link=None,torrent=None,episode=None):
        self.title = title
        self.link=link
        self.torrent=torrent
        self.episode=episode
        
        
        