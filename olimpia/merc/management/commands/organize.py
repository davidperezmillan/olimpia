from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from merc.models import Series, TorrentServers, Plugins, TelegramChatIds
from merc.forms import SeriesForm, TorrentServersForm, SeriesFindForm
from merc.at.airtrapLauncher import AirTrapLauncher

import merc.at.hilos.utiles
import merc.management.commands_utils

import merc.views

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
 
class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('author', nargs=1, type=str)
        parser.add_argument('dirName', nargs='?', default=None, type=str)
        
        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Borramos la carpeta origen',
        )
       


    def handle(self, *args, **options):
        for user in options['author']:
            logger.debug('Ejecutando comando organize por peticion de {} con options {}'.format(user, options['delete']))
            
            author = User.objects.get(username=user)
            merc.views.organizeProccess(author,args,options)
            
            # torrentservers = TorrentServers.objects.filter(author=author)
            # receivers = merc.management.commands_utils.utilgetreceivers(author)
            # try:
            #     launcher = AirTrapLauncher(torrentservers)
            #     errors = launcher.organize(options['delete'])
            # except Exception, e:
            #     logger.error(e)
            
            # merc.at.hilos.utiles.sendTelegram("Hemos organizado la libreria", user=author, receivers=receivers)
        
            self.stdout.write('Successfully "{}"'.format(user))