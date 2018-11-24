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
     表示无法处理的查询异常 请求的异常  An exception that represents an unhandled query.
    """
    def __init__(self,message="Could not handle the query"):
        Fault.__init__(self,UNHANDLED,message)


class AccessDenied(Fault):
    """
    表示试图访问未 被授权的资源时引发的异常
    """

    def __init__(self, message="Access denied"):
        Fault.__init__(self,ACCESS_DENIED,message)

def inside(dir,name):
    """
    
    :param dir: 
    :param name: 
    :return: 
    """
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir,''))

def getPort(url):
    """
    """
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])


class Node:

	
    def __init__(self,url,dirname,secret):
		self.url = url
		self.dirname = dirname
		self.secret = secret 
		self.know = set()

    def query(self,query,history=[]):

        try:
            return self._handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH: raise
            return self._broadcast(query,history)

    def hello(self,other):
        """


        """




        self.know.add(othre)
        return 0

    def fetch(self,query,secret):
        """

        """
        if secret != self.secret: raise AccessDenied
        result = self.query(query)
        f = open(join(self.dirname,query),'w')
        f.write(result)
        f.close()
        return 0

    def _start(self):
        """

        """
        s = SimpleXMLRPCServer(("",getPort(self.url)),logRequests=Fault)
        s.register_instance(self)
        s.server_forever()

    def _hnadle(self,query):
        """

        """
        dir = self.dirname
        name = join(dir,query)
        if not isfile(name): raise UnhandledQuery
        if not  inside(dir,name): raise AccessDenied
        return open(name).read()

    def _broadcast(self, query,history):
        """

        """
        for other in self.know.copy():
            if other in  history: continue
            try:
                s = ServerProxy(other)
                return s.query(query,history)

            except Fault,f:
                if f.faultCode == UNHANDLED: pass
                else: self.know.remove(other)
            except:
                self.know.remvoe(other)
        raise UnhandledQuery

def main():
    url,directory,secret = sys.argv[1:]
    n =  Node(url,directory,secret)
    n._start()

if __name__ == '__main__': main()
                
        
        

        



			 
	 







