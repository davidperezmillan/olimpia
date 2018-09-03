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
        
        torrentservers = self.kwargs['torrentservers']
        series_update = self.kwargs['series_update']
        user = self.kwargs['user']
        receivers = self.kwargs.get('receivers',None)
        filter_find = self.kwargs.get('filter_find',False)
        
        logger.debug('kwargs: {}'.format(self.kwargs))    
        logger.debug('Vamos a lanzar una busqueda para {} en los servidores {} habilitados para el user {}: opcion de filtrado:{}'.format(len(series_update), torrentservers, user, filter_find))

        launcher = AirTrapLauncher(torrentservers)
        torrent_found, torrent_added, errors = launcher.execute(series_update, filter=filter_find)
        logger.debug("Torrent_found : {}".format(torrent_found))
        logger.debug("torrent_added : {}".format(torrent_added))
        context = {'torrent_found': torrent_found, 'torrent_added': torrent_added, 'errors_messages':errors}
        merc.at.hilos.utiles.sendTelegramListAdded(torrent_added, user=user, receivers=receivers)
        return
    
class GenTransmissionThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return
    
    
    
    def run(self):
        user = self.kwargs['user']
        config = self.kwargs['receivers']
        logger.debug('user: {}:receivers {}'.format(user, config))
        
        clazz = TelegramNotifier(token = '135486382:AAFb4fhTGDfy42FzO77HAoxPD6F0PLBGx2Y', user=user)
        clazz.notify(self.args, config)
        return   
    
    
    
class AirTrapOrganizeThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return
    
    def run(self):
        torrentservers = self.kwargs['torrentservers']
        delete = self.kwargs['delete']
        restart = self.kwargs['restart']
        launcher = AirTrapLauncher(torrentservers, logger)
        launcher.organize(delete=delete, restart=restart)
        