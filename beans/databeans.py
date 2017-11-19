#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Sequence,
    Float, 
)


Base = declarative_base() 

class series(Base):
    __tablename__='SERIES'
    nombre = Column('NOMBRE',String, primary_key=True)
    ep = Column('EP',String, default='NRS01E00')
    quality = Column('QUALITY',String, primary_key=True)
    ultima = Column('ULTIMA',DateTime,  default=datetime.datetime.now)
    paussed = Column('PAUSSED',Boolean,default=False)
    skipped = Column('SKIPPED',Boolean,default=False)


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
  