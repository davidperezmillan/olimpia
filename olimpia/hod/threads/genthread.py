import threading

import hod.scrape.handler_scrap

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)




class ScrapThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return
    
    def run(self):
        fichas = self.kwargs['fichas']
        session_id = self.kwargs['session_id']
        hod.scrape.handler_scrap.getInfoOlimpia(fichas, session_id) # No se envia session todos las sessiones
        
        
      