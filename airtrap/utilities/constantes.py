#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

global basepath
basepathswitch = {
    "davidperezmillan-olimpia-5687265" : "/home/ubuntu/conf/airtrap/",
    "alpha_server":"/home/david/script/conf/airtrap/"
    }
basepathlogswitch = {
    "davidperezmillan-olimpia-5687265" : "/home/ubuntu/logs/airtrap/",
    "alpha_server":"/home/david/script/logs/airtrap/"
    }

basepath=basepathswitch[socket.gethostname()]
basepathlog = basepathlogswitch[socket.gethostname()]
basepathlogplugins = '{0}/plugins/'.format(basepathlog)



