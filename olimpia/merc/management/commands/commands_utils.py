from merc.models import Series, TorrentServers, Plugins, TelegramChatIds,TransmissionReceivers
from merc.at.service.telegramHandler import ReceiverTelegram
import merc.at.hilos.utiles

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def utilgetreceivers(user):
    usernames=[]
    fullnames=[]
    groups=[]
    receivers = TransmissionReceivers.objects.filter(author=user).filter(transmission_active=True)
    for rec in receivers:
        usernames.append(rec.username)
        fullnames.append(merc.at.hilos.utiles.getAndBuildFullnames(rec.fullname))
        groups.append(rec.group)
        
    logger.info("{fullnames}{groups}{usernames}".format(fullnames=fullnames, groups=groups, usernames=usernames))
    return ReceiverTelegram(fullnames=fullnames, groups=groups, usernames=usernames)