import threading

from ctab.models import Tasks, DescripModelForm
from datetime import datetime
import re, shlex

# Importacion para llamar a comandos
from django.core.management import call_command
from django.utils import timezone

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)




class TasksThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return
    
    def run(self):
        task_id = self.kwargs['task_id']
        
        logger.info("Lanzamos el proceso {}".format(task_id))
        task_ejecutable = Tasks.objects.get(id=task_id)
        command, tOption = task_ejecutable.task.split(" ",1)
        options = shlex.split(tOption)
        logger.debug("{} {}".format(command,options))
        try:
            call_command(command,*options)
            task_ejecutable.ultima = timezone.now()
            task_ejecutable.save()
        
        except Exception, e:
            logger.error("ERROR EN LA TAREA {} ".format(task_ejecutable.descrip))
        
        
        # torrentservers = self.kwargs['torrentservers']
        # series_update = self.kwargs['series_update']
        # user = self.kwargs['user']
        # receivers = self.kwargs.get('receivers',None)
        # filter_find = self.kwargs.get('filter_find',False)
        
        # logger.debug('kwargs: {}'.format(self.kwargs))    
        # logger.debug('Vamos a lanzar una busqueda para {} en los servidores {} habilitados para el user {}: opcion de filtrado:{}'.format(len(series_update), torrentservers, user, filter_find))

        # launcher = AirTrapLauncher(torrentservers)
        # torrent_found, torrent_added, errors = launcher.execute(series_update, filter=filter_find)
        # logger.debug("Torrent_found : {}".format(torrent_found))
        # logger.debug("torrent_added : {}".format(torrent_added))
        # context = {'torrent_found': torrent_found, 'torrent_added': torrent_added, 'errors_messages':errors}
        # merc.at.hilos.utiles.sendTelegramListAdded(torrent_added, user=user, receivers=receivers)
        # return
