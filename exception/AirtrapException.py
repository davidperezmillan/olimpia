#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AirtrapException(Exception):
    preMessage = "[AirtrapException] INFORMA:"
    messageDefault = "{0} Error no controlado, pongase en contacto con el desarrollador".format(preMessage)
    def __init__(self, message=messageDefault, error=None):
        self.message = message

    def __str__(self):
        return "{0} {1}".format(self.preMessage,self.message)