#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import socket
# global basepath
# basepathswitch = {
#     "davidperezmillan-olimpia-5687265" : "/home/ubuntu/conf/airtrap/",
#     "alpha_server":"/home/david/script/conf/airtrap/"
#     }
# basepathlogswitch = {
#     "davidperezmillan-olimpia-5687265" : "/home/ubuntu/logs/airtrap/",
#     "alpha_server":"/home/david/script/logs/airtrap/"
#     }

import os, sys
import ConfigParser
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    files = [os.path.join(BASE_DIR, 'utilities/airtrap_config.ini')]
    Config = ConfigParser.ConfigParser()
    dataset = Config.read(files)
    if len(dataset) != len(files):
        raise ValueError("No existe el alguno de los ficheros {0} de configuracion, creenlos con el formato que tiene en el ejemplo ".format(files))
    
    basepath= Config.get('PATH','basepath')
    basepathlog=Config.get('PATH','basepathlog')
    basepathlogplugins = '{0}/plugins/'.format(basepathlog)
    

except Exception as e:
    sys.exit(e)
   


