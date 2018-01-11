from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from merc.models import Series, TorrentServers, Plugins, TelegramChatIds
from merc.forms import SeriesForm, TorrentServersForm, SeriesFindForm
from merc.at.airtrapLauncher import AirTrapLauncher

import merc.at.hilos.utiles
import merc.management.commands.commands_utils


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
 
class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('author', nargs='+', type=str)

        # # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     help='Delete poll instead of closing it',
        # )
 
 
    def handle(self, *args, **options):
        for user in options['author']:
            logger.debug('Ejecutando comando Busqueda por peticion de {}'.format(user))
            author = User.objects.get(username=user)
            logger.debug("Usuario : {}".format(author))
            
            series_update = Series.objects.filter(author=author).filter(skipped=False)
            logger.debug('series_update: {}'.format(series_update))
            torrentservers = TorrentServers.objects.filter(author=author)
            logger.debug('torrentservers: {}'.format(torrentservers))
            receivers = merc.management.commands.commands_utils.utilgetreceivers(author)
            logger.debug('receivers: {}'.format(receivers))
            
            try:
                #  merc.at.hilos.utiles.findAndDestroy(series_update, torrentservers, filter_find=True, user=author)
                 merc.at.hilos.utiles.findAndDestroy(series_update, torrentservers, filter_find=False, user=author, receivers=receivers)
            except Exception, e:
                strError = "Se ha produccido un error en el proceso del mercenario"
                logger.error(e)
                merc.at.hilos.utiles.sendTelegram(strError, author, receivers=receivers)
    
            self.stdout.write('Successfully "{}"'.format(author))