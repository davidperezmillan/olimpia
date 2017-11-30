#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler
from prettytable import PrettyTable
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
    Table,
)


import utilities.constantes as cons
 
basepathlog = cons.basepathlog
loggername = 'airtrap'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
loggerfilename = basepathlog+loggername+'.log'


Base = declarative_base()  
databaseDefaultName = "{0}/data/followingseries.sqlite3".format(cons.basepath)

class series(Base):
    __tablename__='series'
    nombre = Column(String, primary_key=True)
    ep_start = Column(String, default='NRS01E00')
    ep_end = Column(String, default='')
    quality = Column(String, primary_key=True)
    ultima = Column(DateTime,  default=datetime.datetime.now)
    paussed = Column(Boolean,default=False)
    skipped = Column(Boolean,default=False)



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


class DatabaseAirTrap(object):   
    
    
    def __init__(self, databaseName=databaseDefaultName, logger=None):
    
        self.databaseName = databaseName
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(loggername)
            self.logger.setLevel(logging.DEBUG)
            self.formatter = logging.Formatter(defaulformatter)
        
            # self.handler = RotatingFileHandler(loggerfilename, maxBytes=2000, backupCount=3)
            # self.handler.setFormatter(self.formatter)
            # self.logger.addHandler(self.handler)
            
            self.ch = logging.StreamHandler()
            self.ch.setFormatter(self.formatter)        
            self.logger.addHandler(self.ch)
        
        self.engine = create_engine('sqlite:///{0}'.format(self.databaseName))
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)      

    def __display(self, tabla, statement):
    
        col_names = tabla.columns.keys()
        x = PrettyTable(col_names)
        for c in col_names:
            x.align[c] = 'l'
        x.padding_width = 2    
        for row in statement:
            fields = []
            for field in tabla.columns.keys():
                fields.append(getattr(row,field.lower()) or "")
            x.add_row(fields)
            
        tabstring = x.get_string()
        return tabstring
    
    
        
    def insert(self,serie, ep_start, ep_end=None):
        self.logger.debug("Grabamos : {} {} {}".format(serie, ep_start, ep_end))
        try:
            s= self.session()
            ep_end = ep_end if ep_end is not None else "{0}S99E99".format(ep_start[:2])
            item = series(nombre=serie,quality=ep_start[:2], ep_start=ep_start, ep_end=ep_end)
            # if ep_end:
            #     item = series(nombre=serie,quality=ep_start[:2], ep_start=ep_start, ep_end=ep_end)
            # else:
            #     item = series(nombre=serie,quality=ep_start[:2], ep_start=ep_start)
            response = s.add(item)
            s.commit()
            return response
            # self.select_all(True)
        except Exception as error:
            self.logger.error("Error al insert la tabla [%s]",error)
    
    def update(self, serie, ep_start, ep_end=None):
        try:
            s=self.session()
            ep_end = ep_end if ep_end is not None else "{0}S99E99".format(ep_start[:2])
            response = s.query(series).filter(series.nombre==serie, series.quality==ep_start[:2]).update({series.ep_start:ep_start, series.quality:ep_start[:2], series.ultima:datetime.datetime.now()})
            # if ep_end:
            #     response = s.query(series).filter(series.nombre==serie).update({series.ep_start:ep_start, series.quality:ep_start[:2], series.ep_end:ep_end, series.ultima:datetime.datetime.now()})
            # else:
            #     response = s.query(series).filter(series.nombre==serie).update({series.ep_start:ep_start, series.quality:ep_start[:2], series.ultima:datetime.datetime.now()})
            s.commit()
            return response
            # self.select_all(False)
        except Exception as error:
            self.logger.error("Error al update la tabla [%s]",error)
            
    def delete(self, serie=None, quality="NR", id=None):
        try:
            s=self.session()
            response = s.query(series).filter(series.nombre==serie, series.quality==quality).delete()
            s.commit()
            return response
        except Exception as error:
            self.logger.error("Error al delete de un registro [%s]",error)
    
    def truncate(self):
        try:
            s=self.session()
            statements = ["DELETE FROM series;", "VACUUM;"]
            for statement in statements:
                s.execute(statement)
            s.commit()
        except Exception as error:
            self.logger.error("Error al vaciar la tabla [%s]",error)
    
    
    def view_chat_ids(self, display=False):
        try:    
            s= self.session()
            statement = s.query(ChatIdEntry).all()
            print self.__display(ChatIdEntry.metadata.tables['telegram_chat_ids'], statement ) if display else "No hay representacion grafica" 
            return statement
        except Exception as error:
            self.logger.error("Error al view_chat_ids la tabla [%s]",error)
    
    
    
    def select_all(self,statement, display=False):
        try:    
            print self.__display(series.metadata.tables['series'], statement ) if display else "No hay representacion grafica" 
            return statement
        except Exception as error:
            self.logger.error("Error al selectAll la tabla [%s]",error)

    def select_noSkip(self, display=False):
        self.logger.info("Select no Skip")
        try:    
            s= self.session()
            statement = s.query(series).filter(series.skipped==False).order_by(series.ultima)
            print self.__display(series.metadata.tables['series'], statement ) if display else "No hay representacion grafica" 
            return statement
        except Exception as error:
            self.logger.error("Error al selectAll la tabla [%s]",error)

    def select(self, sql=None, display=False):
        if not sql:
            return self.select_noSkip(display=display)
        else:
            s= self.session()
            statement = s.query(series).from_statement(sql)
            return self.select_all(statement,display=display)
            



    
    

