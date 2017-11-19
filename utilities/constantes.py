#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

global basepath
basepathswitch = {
    "davidperezmillan-metascrap-2716814":"/home/ubuntu/workspace/airtrap",
    "davidperezmillan-mycrybot-5060192":"/home/ubuntu/workspace/airtrap",
    "alpha_server":"/home/david/script/conf/airtrap"
    }
basepath=basepathswitch[socket.gethostname()]
basepathlog = '{0}/logs/'.format(basepath)
basepathlogplugins = '{0}/logs/plugins/'.format(basepath)




