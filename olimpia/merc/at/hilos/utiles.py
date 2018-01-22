import logging
from merc.at.hilos.genthread import GenTransmissionThread, GenTorrentThread
# Get an instance of a logger
logger = logging.getLogger(__name__)


def sendTelegramListAdded(lrequest,serie=None, user=None,receivers=None):
    logger.debug(lrequest)
    if lrequest:
        sRequest = "'El Mercenario' ha puesto en cola {0} torrent para su descargas [{1}]:   \n\r".format(len(lrequest), user if user else "")
        sFinal = "\n\rEspero que lo disfruteis, Gracias por utilizar 'La Trampa del Aire - El Mercenario'"
        sitems = ""
        for item in lrequest:
            sitems = "{0} -- {1}.  \n\r".format(sitems,item.name.encode('utf-8').strip()) 
        sRequest = "{0}{1}{2}".format(sRequest,sitems, sFinal)
    else:
        sRequest = "Que pena 'El Mercenario' no ha encontrado nada de {} que enviar [{}].....".format(serie if serie else "'varios titulos'", user if user else "")
    sendTelegram(sRequest, user, receivers)


def sendTelegram(mensaje='Interaccion', user=None, receivers=None):
    '''
    Y si anadimos un envio de Telegram cuando se anade una serie
    '''
    from merc.at.service.telegramHandler import ReceiverTelegram
    # receivers = receivers if receivers else ReceiverTelegram(fullnames=[("David","Perez Millan")], groups=['Down'])
    receivers = receivers if receivers else ReceiverTelegram(fullnames=[("David","Perez Millan")])
    
    gtransmissionh = GenTransmissionThread(args=(mensaje), kwargs={'user':user, 'receivers':receivers})
    gtransmissionh.start()  
      



      
    
def findAndDestroy(series_update, torrentservers, filter_find=False, user=None, receivers=None):
    
    gtorrenth = GenTorrentThread( kwargs={'series_update':series_update, 'torrentservers':torrentservers, 'user':user,'filter_find':filter_find, 'receivers':receivers})
    gtorrenth.start()




