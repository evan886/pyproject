#!/usr/bin/python
#-*- coding:utf-8 -*-
# 注释
from xmlrpc import ServerProxy, False
from  cmd import Cmd
from random import choice
from  string import lowercase
from server import Node, UNHANDLED
from threading import  Thread
from time import sleep
import sys

HEAD_START = 0.1 #Seconds
SECRET_LENGTH = 100

def randomString(length):
    """

    """
    chars = []
    letters = lowercase[:26]
    while length >0 :
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)

class Client(Cmd):
    """
    
    """

    prompt = '>'


    def __init__(self,url,dirname,urlfile):
        """

        """
        Cmd.__init__(self)
        self.secret = randomString(SECRET_LENGTH)
        n = Node(url,dirname,self.secret)
        t = Thread(target = n._start)
        t.setDaemon(1)
        t.start()
        # Give
        sleep(HEAD_START)
        
