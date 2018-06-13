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
        
        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Borramos la carpeta origen',
        )
        parser.add_argument(
            '--nomsg',
            action='store_true',
            dest='nomsg',
            help='No enviamos msg-telegram',
        )
       


    def handle(self, *args, **options):
        for user in options['author']:
            logger.info('Ejecutando comando organize por peticion de {} con options {}'.format(user, options))
            
            author = User.objects.get(username=user)
            torrentservers = TorrentServers.objects.filter(author=author)
            merc.at.hilos.utiles.organizeProccess(author,args,options,torrentservers)
            self.stdout.write('Successfully "{}"'.format(user))