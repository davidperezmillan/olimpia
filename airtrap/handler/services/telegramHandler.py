#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import time
import logging
from logging.handlers import RotatingFileHandler

try:
    import telegram
    from telegram.error import TelegramError
    from telegram.utils.request import NetworkError
except ImportError:
    telegram = None

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from beans.databeans import ChatIdEntry
import utilities.constantes as cons


basepathlog = cons.basepathlog
loggername = 'telegramHandler'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
loggerfilename = basepathlog+loggername+'.log'

Base = declarative_base() 



class ConfigTelegramBean(object):
    
    def __str__(self):
        x = ['token={0}'.format(self.token)]
        if self.usernames:
            x.append('usernames={0}'.format(self.usernames))
        if self.fullnames:
            x.append('fullnames={0}'.format(self.fullnames))
        if self.groups:
            x.append('groups={0}'.format(self.groups))
        return ' '.join(x)
        
    def __init__(self, token = None, usernames=None, fullnames = None, groups = None):
        self.token = token
        self.usernames=usernames
        self.fullnames=fullnames
        self.groups=groups

''' Esta clase se importaria

class ChatIdEntry(Base):
    __tablename__ = 'telegram_chat_ids'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=True)
    firstname = Column(String, index=True, nullable=True)
    surname = Column(String, index=True, nullable=True)
    group = Column(String, index=True, nullable=True)

    def __str__(self):
        x = ['id={0}'.format(self.id)]
        if self.username:
            x.append('username={0}'.format(self.username))
        if self.firstname:
            x.append('firstname={0}'.format(self.firstname))
        if self.surname:
            x.append('surname={0}'.format(self.surname))
        if self.group:
            x.append('group={0}'.format(self.group))
        return ' '.join(x)
        
    def __init__(self, id = None, username=None, firstname=None,surname=None, group=None):
        self.id = id
        self.username=username
        self.firstname=firstname
        self.surname=surname
        self.group=group

'''

databaseDefaultName = "{0}/conf/data/followingseries.sqlite3".format(cons.basepath)
class TelegramNotifier(object):

    _token = None
    _usernames = None
    _fullnames = None
    _groups = None
    _bot = None
    _databaseName = databaseDefaultName


    def notify(self, title, message, config):
        self._token = config.token
        chat_ids = self._real_init(config)
        if not chat_ids:
            return
        self._send_msgs(message, chat_ids)
        ## de Propina
        self._get_bot_updates()

    def _parse_config(self, config):
        self._token = config.token
        self._parse_mode = "markdown"
        self._usernames = config.usernames or []
        self._fullnames = config.fullnames or []
        self._groups = config.groups or []

    def _real_init(self, client):
        self._enforce_telegram_plugin_ver()
        self._parse_config(client)
        self.logger.info('token=%s, parse_mode=%s, usernames=%s, fullnames=%s, groups=%s', self._token,
                       self._parse_mode, self._usernames, self._fullnames, self._groups)
        self._init_bot()
        chat_ids = self._get_chat_ids_n_update_db()
        return chat_ids

    def _init_bot(self):
        self._bot = telegram.Bot(self._token)
        self._check_token()

    def _check_token(self):
        try:
            self._bot.getMe()
        except UnicodeDecodeError as e:
            self.logger.info('bot.getMe() raised: %s', repr(e))
            raise Exception('invalid bot token')
        except (NetworkError, TelegramError) as e:
            self.logger.error('Could not connect Telegram servers at this time, please try again later: %s', e.message)

    @staticmethod
    def _enforce_telegram_plugin_ver():
        if telegram is None:
            raise Exception('missing python-telegram-bot pkg')
        elif not hasattr(telegram, str('__version__')):
            raise Exception('invalid or old python-telegram-bot pkg')
        # elif LooseVersion(telegram.__version__) < native_str(_MIN_TELEGRAM_VER):
        #     raise Exception('old python-telegram-bot ({0})'.format(telegram.__version__))

    def _send_msgs(self, msg, chat_ids):
        kwargs = dict()
        if self._parse_mode == 'markdown':
            kwargs['parse_mode'] = telegram.ParseMode.MARKDOWN
        elif self._parse_mode == 'html':
            kwargs['parse_mode'] = telegram.ParseMode.HTML
        for chat_id in (x.id for x in chat_ids):
            try:
                self.logger.info('sending msg to telegram servers: %s', msg)
                self._bot.sendMessage(chat_id=chat_id, text=msg, **kwargs)
            except TelegramError as e:
                if kwargs.get('parse_mode'):
                    self.logger.warning('Failed to render message using parse mode %s. Falling back to basic parsing: %s',
                                     kwargs['parse_mode'], e.message)
                    del kwargs['parse_mode']
                    try:
                        self._bot.sendMessage(chat_id=chat_id, text=msg, **kwargs)
                    except TelegramError as e:
                        raise Exception(e.message)
                else:
                    raise Exception(e.message)

    def _get_chat_ids_n_update_db(self):

        usernames = self._usernames[:]
        fullnames = self._fullnames[:]
        groups = self._groups[:]
        chat_ids, has_new_chat_ids = self._get_chat_ids(usernames, fullnames, groups)
        self.logger.debug('chat_ids=%s', chat_ids)

        if not chat_ids:
            raise Exception('no chat id found, try manually sending the bot any message to initialize the chat')
        else:
            if usernames:
                self.logger.warning('no chat id found for usernames: %s', usernames)
            if fullnames:
                self.logger.warning('no chat id found for fullnames: %s', fullnames)
            if groups:
                self.logger.warning('no chat id found for groups: %s', groups)
            if has_new_chat_ids:
                self.logger.info('chat id found for groups: %s', chat_ids)
                self._update_db(chat_ids)

        return chat_ids
    
    def _get_chat_ids(self, usernames, fullnames, groups):
        self.logger.debug('loading cached chat ids')
        chat_ids = self._get_cached_chat_ids(usernames, fullnames, groups)
        self.logger.debug('found {0} cached chat_ids: {1}'.format(len(chat_ids), ['{0}'.format(x) for x in chat_ids]))

        if not (usernames or fullnames or groups):
            self.logger.debug('all chat ids found in cache')
            return chat_ids, False

        self.logger.debug('loading new chat ids')
        new_chat_ids = list(self._get_new_chat_ids(usernames, fullnames, groups))
        self.logger.debug('found {0} new chat_ids: {1}'.format(len(new_chat_ids), ['{0}'.format(x) for x in new_chat_ids]))

        chat_ids.extend(new_chat_ids)
        return chat_ids, bool(new_chat_ids)


    #  BBDD RECUPERAR
    def _get_cached_chat_ids(self, usernames, fullnames, groups):
        self.logger.debug('Try get data Chats')
        session= self.session()
        chat_ids = list()
        cached_usernames = dict((x.username, x)
                                for x in session.query(ChatIdEntry).filter(ChatIdEntry.username != None).all())
        cached_fullnames = dict(((x.firstname, x.surname), x)
                                for x in session.query(ChatIdEntry).filter(ChatIdEntry.firstname != None).all())
        cached_groups = dict((x.group, x)
                             for x in session.query(ChatIdEntry).filter(ChatIdEntry.group != None).all())

        len_ = len(usernames)
        for i, username in enumerate(reversed(usernames)):
            item = cached_usernames.get(username)
            if item:
                chat_ids.append(item)
                usernames.pop(len_ - i - 1)

        len_ = len(fullnames)
        for i, fullname in enumerate(reversed(fullnames)):
            item = cached_fullnames.get(fullname)
            if item:
                chat_ids.append(item)
                fullnames.pop(len_ - i - 1)

        len_ = len(groups)
        for i, grp in enumerate(reversed(groups)):
            item = cached_groups.get(grp)
            if item:
                chat_ids.append(item)
                groups.pop(len_ - i - 1)

        return chat_ids
    
    #  BBDD UPDATEAR
    def _update_db(self,chat_ids):
        self.logger.debug('saving updated chat_ids to db')
        session= self.session()
        # avoid duplicate chat_ids. (this is possible if configuration specified both username & fullname
        chat_ids_d = dict((x.id, x) for x in chat_ids)
        session.add_all(iter(chat_ids_d.values()))
        session.commit()
    
    
    def _get_new_chat_ids(self, usernames, fullnames, groups):
        self.logger.debug('Try get new Chats')
        upd_usernames, upd_fullnames, upd_groups = self._get_bot_updates()


        len_ = len(usernames)
        for i, username in enumerate(reversed(usernames)):
            chat = upd_usernames.get(username)
            if chat is not None:
                entry = ChatIdEntry(id=chat.id, username=chat.username, firstname=chat.first_name,
                                    surname=chat.last_name)
                yield entry
                usernames.pop(len_ - i - 1)

        len_ = len(fullnames)
        for i, fullname in enumerate(reversed(fullnames)):
            chat = upd_fullnames.get(fullname)
            if chat is not None:
                entry = ChatIdEntry(id=chat.id, username=chat.username, firstname=chat.first_name,
                                    surname=chat.last_name)
                yield entry
                fullnames.pop(len_ - i - 1)

        len_ = len(groups)
        for i, grp in enumerate(reversed(groups)):
            chat = upd_groups.get(grp)
            if chat is not None:
                entry = ChatIdEntry(id=chat.id, group=chat.title)
                yield entry
                groups.pop(len_ - i - 1)

    def _get_bot_updates(self):
        self.logger.debug('Update BBDD')
        # highly unlikely, but if there are more than 100 msgs waiting for the bot, we should not miss one
        updates = []
        last_upd = 0
        while 1:
            ups = self._bot.getUpdates(last_upd, limit=100)
            updates.extend(ups)
            if len(ups) < 100:
                break
            last_upd = ups[-1].update_id

        usernames = dict()
        fullnames = dict()
        groups = dict()
        for update in updates:
            self.logger.debug('Update BBDD {0}'.format(update))
            if update.message:
                chat = update.message.chat
            elif update.edited_message:
                chat = update.edited_message.chat
            elif update.channel_post:
                chat = update.channel_post.chat
            else:
                raise Exception('Unknown update type encountered: %s' % update)

            if chat.type == 'private':
                usernames[chat.username] = chat
                fullnames[(chat.first_name, chat.last_name)] = chat
            elif chat.type in ('group', 'supergroup' or 'channel'):
                groups[chat.title] = chat
            else:
                self.logger.warning('unknown chat type: %s}', type(chat))

        return usernames, fullnames, groups


    def __init__(self, databaseName=databaseDefaultName, logger = None):
    
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(loggername)
            self.logger.setLevel(logging.DEBUG)
            self.formatter = logging.Formatter(defaulformatter)
    
    
            self.ch = logging.StreamHandler()
            self.ch.setFormatter(self.formatter)        
            self.logger.addHandler(self.ch)
        
        self._databaseName = databaseName
        self.engine = create_engine('sqlite:///{0}'.format(self._databaseName))
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)   

if __name__ == '__main__':
    clazz = TelegramNotifier()
    config = ConfigTelegramBean(token = '135486382:AAFb4fhTGDfy42FzO77HAoxPD6F0PLBGx2Y', fullnames = [("David","Perez Millan")], groups = [("Down")])
    clazz.notify("Titulo", "Mensaje de prueba", config)
