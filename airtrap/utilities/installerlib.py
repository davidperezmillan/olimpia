#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pip #needed to use the pip functions
import sys

importNeeds = ['prettytable', 'sqlalchemy', 'transmissionrpc','python-telegram-bot', 'bs4']
responseImportNeeds = []


def __install(package, verbose):
    
    if verbose:
        # raw_input returns the empty string for "enter"
        yes = {'yes','y', 'ye', ''}
        no = {'no','n'}
        
        choice = raw_input("vamos a instalar {0} .....(Y/N) ".format(package)).lower()
        if choice in yes:
           pip.main(['install', "--user", package])
        elif choice in no:
           sys.stdout.write("No se va a instalar {0}".format(package))
        else:
           sys.stdout.write("Please respond with 'yes' or 'no'")
    else:
        pip.main(['install', "--user", package])
    


def __prettyPrintArray(encabezado, pie, lst):
    sItems = ""
    for item in lst:
        sItems = "{0} -- {1} \n\r".format(sItems,item) 
    sRequest = "{0}{1}{2}".format(encabezado,sItems, pie)
    return sRequest

def installImportNeed(verbose=False):
    for iNeeds in importNeeds:
        print 'Comprobando {0}'.format(iNeeds)
        try:
            __import__(iNeeds)
        except ImportError as e:
            __install(iNeeds, verbose)

    



