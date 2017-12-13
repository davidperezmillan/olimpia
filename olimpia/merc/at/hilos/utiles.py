import logging
from merc.at.hilos.genthread import GenTransmissionThread, GenTorrentThread
# Get an instance of a logger
logger = logging.getLogger(__name__)


def sendTelegramListAdded(lrequest):
    logger.debug(lrequest)
    if lrequest:
        sRequest = "'La trampa del Aire - El Mercenario' ha puesto en cola {0} torrent para su descargas :   \n\r".format(len(lrequest))
        sFinal = "\n\rEspero que lo disfruteis, Gracias por utilizar 'La Trampa del Aire - El Mercenario'"
        sitems = ""
        for item in lrequest:
            sitems = "{0} -- {1}.  \n\r".format(sitems,item.name.encode('utf-8').strip()) 
        sRequest = "{0}{1}{2}".format(sRequest,sitems, sFinal)
    else:
        sRequest = 'Que pena no tenemos nada que enviar .....'
    sendTelegram(sRequest)





def sendTelegram(mensaje='Interaccion'):
    '''
    Y si anadimos un envio de Telegram cuando se anade una serie
    '''
    gtransmissionh = GenTransmissionThread(args=(mensaje), kwargs={})
    gtransmissionh.start()  
      
      
    
def findAndDestroy(series_update, torrentservers):
    
    gtorrenth = GenTorrentThread( kwargs={'series_update':series_update, 'torrentservers':torrentservers})
    gtorrenth.start()




