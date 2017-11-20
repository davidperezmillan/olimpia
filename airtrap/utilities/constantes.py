#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

global basepath
basepathswitch = {
    "alpha_server":"/home/david/script/conf/airtrap"
    }
basepathlogswitch = {
    "alpha_server":"/home/david/script/logs/airtrap"
    }

basepath=basepathswitch[socket.gethostname()]
basepathlog = basepathlogswitch[socket.gethostname()]
basepathlogplugins = '{0}/plugins/'.format(basepathlog)




