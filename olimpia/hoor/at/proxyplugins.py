#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import urllib, urllib2
import requests

import bs4
from bs4 import BeautifulSoup



# Get an instance of a logger
logger = logging.getLogger(__name__)



def main():
    pass


    

if __name__ == "__main__":
    url = 'http://www.divxtotal2.net/?s="{nombreserie}'.format(nombreserie='Mom')
    
    # my code here
    http_proxy  = "http://190.12.102.205:8080"
    # https_proxy = "http://190.12.102.205:8080"
    # ftp_proxy   = "http://190.12.102.205:8080"
    
    proxyDict = { 
                  "http"  : http_proxy, 
                #   "https" : https_proxy, 
                #   "ftp"   : ftp_proxy
                }
                
                
                
                
                
    # page = requests.get(url)
    # print("page 1 : {}".format(page))
    
    # source = BeautifulSoup(page.text, "html.parser")
    # buscar_list = source.find_all("table", {"class" : "table"})
    # print buscar_list
                
    # page = requests.get(url,proxies=proxyDict)
    # print("page 2: {}".format(page))
    
    # source = BeautifulSoup(page.text, "html.parser")
    # buscar_list = source.find_all("table", {"class" : "table"})
    # print buscar_list
    
    
    

    proxy = urllib2.ProxyHandler(proxyDict)
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

    url = "http://newpct1.com/buscar"
    # Prepare the data
    titulo="Mom"
    quality="1469"
    values = {'q' : '"'+titulo+'"',"categoryIDR":quality, "ordenar":"Nombre", "inon":"Ascendente"}
    
    print("Buscamos {}".format(values))
    data = urllib.urlencode(values)
    print("Buscamos {}".format(data))
    # Send HTTP POST request
    req = urllib2.Request(url, data)
    print("Buscamos {}".format(req))
    page = urllib2.urlopen(req)
    print("Encontramos {}".format(page))
    source = BeautifulSoup(page, "html.parser")
    print source
    


    
    
    
    