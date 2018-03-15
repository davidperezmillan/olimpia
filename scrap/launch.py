#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys,os


# Get an instance of a logger
logger = logging.getLogger(__name__)




# proxies_list = ["http://190.12.102.205:8080","139.255.101.242:8080","117.58.243.244:808","216.165.113.123:3128",] # No los tengo comprobados
# proxies_list = ["http://190.12.102.205:8080",] # Argentina de siempre
# proxies_list = ["http://183.88.195.231:8080",]
proxies_list = ["http://190.2.6.105:3130",]

# proxies_list = ["http://94.16.123.176:8080",""]

proxies = {
    'http': proxies_list[0]
}



series = ["Mom",]


def main():
    logger.debug("Vamos a intentar montar un plugin en condiciones")
    
    
    
    





if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)
    main()