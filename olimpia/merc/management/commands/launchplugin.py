from django.core.management.base import BaseCommand, CommandError

# from django.contrib.auth.models import User
# from merc.models import Series, TorrentServers, Plugins, TelegramChatIds
# from merc.forms import SeriesForm, TorrentServersForm, SeriesFindForm
# from merc.at.airtrapLauncher import AirTrapLauncher

# import merc.at.hilos.utiles
# import merc.management.commands_utils

from merc.at.plugins.torrentrapid_handler import TorrentRapidHandlerClass, RequestPlugin

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


 
class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        pass
        # Positional arguments
        parser.add_argument('title', nargs=1, type=str)
        parser.add_argument('quality', nargs=1, type=str)

        # # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     help='Delete poll instead of closing it',
        # )
 
 
    def handle(self, *args, **options):
        
        self.stdout.write('launchplugin {}'.format(''))
        
        dthandler = TorrentRapidHandlerClass(logger)
        title = "{}".format(options['title'][0])
        epstart = "{}S00E00".format( options['quality'][0])
        epend = "{}S99E99".format( options['quality'][0])
        request = RequestPlugin(title=title, epstart=epstart, epend=epend)
        self.stdout.write("Respuesta : {} ".format(dthandler.execute(request,filter=False)))