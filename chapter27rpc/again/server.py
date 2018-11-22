#!/usr/bin/python
#-*- coding:utf-8 -*-
#= listing21-2.py
from xmlrpclib import ServerProxy, Fault
from os.path import join, abspath,isfile
from  SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED = 100
ACCESS_DENIED = 200

class UnhandledQuery(Fault):
    """
    An exception that represents an unhandled query.
    """
