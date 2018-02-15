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
        full = getAndBuildFullnames(rec.fullname)
        if rec.username:
            usernames.append(rec.username)
        if full:   
            fullnames.append(full)
        if rec.group:
            groups.append(rec.group)
        
    logger.info("{fullnames}{groups}{usernames}".format(fullnames=fullnames, groups=groups, usernames=usernames))
    return ReceiverTelegram(fullnames=fullnames, groups=groups, usernames=usernames)
    
    
def getAndBuildFullnames(destinatario):
    if destinatario:
        dest = destinatario.split(' ',1)
        firstname = dest[0]
        surname = dest[1] if len(dest)>1 else ""
        return firstname,surname    
    return None,None