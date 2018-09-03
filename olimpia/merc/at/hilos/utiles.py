import logging
import merc.at.properties.msgproperties as msgproperties
from merc.at.hilos.genthread import GenTransmissionThread, GenTorrentThread
# Get an instance of a logger
logger = logging.getLogger(__name__)


def sendTelegramListAdded(lrequest,serie=None, user=None,receivers=None):
    logger.debug(lrequest)
    msg_telegram = msgproperties.MSG_TELEGRAM
    
    if lrequest:
        sRequest = msg_telegram["header"].format(len(lrequest), user if user else "")
        sFinal = msg_telegram["footer"]
        sitems = ""
        for item in lrequest:
            sitems = msg_telegram["item"].format(sitems,item.name.encode('utf-8').strip()) 
        sRequest = "{0}{1}{2}".format(sRequest,sitems, sFinal)
    else:
        sRequest = msg_telegram["nothing"].format(serie if serie else "'varios titulos'", user if user else "")
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

def organizeProccess(author,args, options, torrentservers):
    # torrentservers = TorrentServers.objects.filter(author=author)
    logger.info('Ejecutando comando organize por peticion de {} con options {}'.format(author, options))
    import merc.management.commands_utils
    receivers = merc.management.commands_utils.utilgetreceivers(author)
    try:
        if options:
            airtraporganize_thread = merc.at.hilos.genthread.AirTrapOrganizeThread(kwargs={'delete':options['delete'],'torrentservers':torrentservers, 'restart':options['restart']})
            airtraporganize_thread.start()
            if (options['nomsg'] is False):
                merc.at.hilos.utiles.sendTelegram(msgproperties.MSG_TELEGRAM["organize"], user=author, receivers=receivers)
        else:
            airtraporganize_thread = merc.at.hilos.genthread.AirTrapOrganizeThread(kwargs={'delete':False,'torrentservers':torrentservers, 'restart':False})
            airtraporganize_thread.start()
            merc.at.hilos.utiles.sendTelegram(msgproperties.MSG_TELEGRAM["organize"], user=author, receivers=receivers)
    except Exception, e:
        logger.error(e)
    
    return 

