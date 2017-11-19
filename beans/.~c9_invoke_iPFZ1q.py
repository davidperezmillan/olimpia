#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import time
import logging
from logging.handlers import RotatingFileHandler


class RequestPlugin(object):

    def __str__(self):
        x=[]
        if self.title:
            x.append('title={0}'.format(self.title))
        if self.epstrat:
            x.append('epstrat={0}'.format(self.epstrat))
        if self.epend:
            x.append('epend={0}'.format(self.epend))            
        return ' '.join(x)

    def __init__(self,title=None, epstrat=None, epend=None):
        self.title=title
        self.epstrat=epstrat
        self.epend=epend
        
        
        
class ResponsePlugin(object):
    
    def __str__(self):
        x=[]
        if self.title:
            x.append('title={0}'.format(self.title))
        if self.link:
            x.append('link={0}'.format(self.link))
        if self.episode:
            x.append('episode={0}'.format(self.episode))
        return ' '.join(x)
        
    def __init__(self, title=None, link=None,episode=None):
        self.title = title
        self.link=link
        self.episode=episode



































