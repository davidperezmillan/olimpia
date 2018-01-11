from django.core.management.base import BaseCommand, CommandError

# from django.contrib.auth.models import User
# from merc.models import Series, TorrentServers, Plugins, TelegramChatIds
# from merc.forms import SeriesForm, TorrentServersForm, SeriesFindForm
# from merc.at.airtrapLauncher import AirTrapLauncher

# import merc.at.hilos.utiles
# import merc.management.commands.commands_utils

from merc.at.plugins.divxtotal_handler import DivxtotalHandler, RequestPlugin

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


 
class Command(BaseCommand):
    help = "Vamos a buscar todos las series"
 
    def add_arguments(self, parser):
        pass
        # Positional arguments
        # parser.add_argument('author', nargs='+', type=str)

        # # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     help='Delete poll instead of closing it',
        # )
 
 
    def handle(self, *args, **options):
        
        self.stdout.write('launchplugin {}'.format(''))
        
        dthandler = DivxtotalHandler(logger)
        request = RequestPlugin(title='The BlackList', epstart='HDS05E00', epend='HDS99E99')
        dthandler.execute(request,filter=False)