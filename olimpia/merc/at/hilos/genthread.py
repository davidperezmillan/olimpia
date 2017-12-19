import logging
import threading
import merc.at.hilos.utiles
# Get an instance of a logger
logger = logging.getLogger(__name__)

from merc.at.airtrapLauncher import AirTrapLauncher
from merc.at.service.telegramHandler import TelegramNotifier, ReceiverTelegram


class GenTorrentThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return
    
    def run(self):
        
        logger.debug('kwargs: {}'.format(self.kwargs))    
        logger.debug('series_update: {}'.format(self.kwargs['series_update']))
        logger.debug('torrentservers: {}'.format(self.kwargs['torrentservers']))
        logger.debug('user: {}'.format(self.kwargs['user']))
        
        torrentservers = self.kwargs['torrentservers']
        series_update = self.kwargs['series_update']
        filter_find = self.kwargs.get('filter_find',False)
        
        launcher = AirTrapLauncher(torrentservers)
        torrent_found, torrent_added, errors = launcher.execute(series_update, filter_find)
        logger.debug("Torrent_found : {}".format(torrent_found))
        logger.debug("torrent_added : {}".format(torrent_added))
        context = {'torrent_found': torrent_found, 'torrent_added': torrent_added, 'errors_messages':errors}
        merc.at.hilos.utiles.sendTelegramListAdded(torrent_added, user=self.kwargs['user'])
        return
    
class GenTransmissionThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return
    
    
    
    def run(self):
        import sys, os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        RUTA = os.path.join(BASE_DIR, '../../../airtrap')
        sys.path.insert(0,RUTA)
        # from handler.services.telegramHandler import TelegramNotifier, ConfigTelegramBean
        logger.debug('user: {}'.format(self.kwargs['user']))
        
        clazz = TelegramNotifier(token = '135486382:AAFb4fhTGDfy42FzO77HAoxPD6F0PLBGx2Y', user=self.kwargs['user'])
        config = ReceiverTelegram(fullnames = [("David","Perez Millan")])
        clazz.notify(self.args, config)
        return   