from django.core.management.base import BaseCommand, CommandError
import logging

from django.contrib.auth.models import User
from merc.models import Series, TorrentServers, Plugins, TelegramChatIds
from merc.forms import SeriesForm, TorrentServersForm, SeriesFindForm
from merc.at.airtrapLauncher import AirTrapLauncher

import merc.at.hilos.utiles

# Get an instance of a logger
logger = logging.getLogger(__name__)
 
class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('author', nargs='1', type=str)
        
        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete poll instead of closing it',
        )


    def handle(self, *args, **options):
        logger.debug('Ejecutando comando organize por peticion de {} con options {}'.format('david', options['delete']))
        
        author = User.objects.get(username=options['david'])
        torrentservers = TorrentServers.objects.filter(author=author)
        try:
            launcher = AirTrapLauncher(torrentservers)
            errors = launcher.organize(options['delete'])
        except Exception, e:
            logger.error(e)
        
        merc.at.hilos.utiles.sendTelegram("Hemos organizado la libreria", author)
        
        self.stdout.write('Successfully "{}"'.format('david'))