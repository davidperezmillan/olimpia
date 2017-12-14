import logging
from merc.at.hilos.genthread import GenTransmissionThread, GenTorrentThread
# Get an instance of a logger
logger = logging.getLogger(__name__)


def sendTelegramListAdded(lrequest, user=None):
    logger.debug(lrequest)
    if lrequest:
        sRequest = "'La trampa del Aire - El Mercenario' ha puesto en cola {0} torrent para su descargas [{1}]:   \n\r".format(len(lrequest), user if user else "")
        sFinal = "\n\rEspero que lo disfruteis, Gracias por utilizar 'La Trampa del Aire - El Mercenario'"
        sitems = ""
        for item in lrequest:
            sitems = "{0} -- {1}.  \n\r".format(sitems,item.name.encode('utf-8').strip()) 
        sRequest = "{0}{1}{2}".format(sRequest,sitems, sFinal)
    else:
        sRequest = 'Que pena el mercenario no ha encontrado nada que enviar [{}].....'.format( user if user else "")
    sendTelegram(sRequest, user)





def sendTelegram(mensaje='Interaccion', user=None):
    '''
    Y si anadimos un envio de Telegram cuando se anade una serie
    '''
    gtransmissionh = GenTransmissionThread(args=(mensaje), kwargs={'user':user})
    gtransmissionh.start()  
      
      
    
def findAndDestroy(series_update, torrentservers, user=None):
    
    gtorrenth = GenTorrentThread( kwargs={'series_update':series_update, 'torrentservers':torrentservers, 'user':user})
    gtorrenth.start()




