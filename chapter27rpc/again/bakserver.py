#!/usr/bin/python
#-*- coding:utf-8 -*-
#= listing21-2.py 这个有问题要确定先
from xmlrpclib import ServerProxy, Fault
from os.path import join, abspath,isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

SimpleXMLRPCServer.allow_reuse_address =1

MAX_HISTORY_LENGTH = 6

UNHANDLED     = 100
ACCESS_DENIED = 200

class UnhandledQuery(Fault):
    """
表示不可处理请求的异常
    """
    def __init__(self,message="Cound not handle the query"):
        Fault.__init__(self, UNHANDLED, message)


class AccessDenied(Fault):
    """
here p416 如图用户试图访问未被授权的某些资源，就会引发异常

    """
    def __init__(self, message="Access denied"):
        Fault.__init__(self, ACCESS_DENIED, message)

def inside(dir, name):
    """
检查给定的目录中是否有给定的文件名  ,2019年 01月 25日 星期五 21:37:43  pass 
"""
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ''))

def getPort(url):
    """
    从URL中提取端口号 解说在simple_node.py  2019年 01月 30日 星期三 23:27:45 pass 
    """
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])

class Node:
    """
    A node in a peer-to-peer network.
    """
    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname = dirname
        self.secret = secret
        self.known = set()

    def query(self, query, history=[]):
        """
查询文件 , 可能会向其它已知节点请求帮助，将文件作为字符串返回 

        """
        try:
            return self._handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH: raise
            return self._broadcast(query, history)



    def hello(self, other):
        """
        用于将节点介绍给其它节点  在哪里用的呢    
        """
        self.known.add(other)
        return 0

    def fetch(self, query, secret):
        """
 
        """
        if secret != self.secret: raise AccessDenied
        result = self.query(query) #调用同一个类中的其它方法 要先self.方法名
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close()
        return 0

    def _start(self):
        """

        """
        s = SimpleXMLRPCServer("",getPort(self.url),logRequests= False)
        s.register_instance(self)
        s.serve_forever()

    def _handle(self, query):
        """
        2019年 01月 26日 星期六 23:09:19 CST        Used internally to handle queries. 内部使用 用于处理请求 
     负责查询的内部处理(检查文件是否在于于特定的node 获取数据等等)
        """
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name): raise UnhandledQuery
        if not inside(dir, name): raise AccessDenied
        return open(name).read()

    def _broadcast(self,query,history):
        """
        内部使用，用于将查询广播到所有已知节点 here 不明白原理呢
        """
        for other in self.known.copy():
            if other in history: continue
            try:
                s = ServerProxy(other)
                return s.query(query,history)

            except Fault, f:
                if f.faultCode == UNHANDLED: pass
                else: self.known.remove(other)
            except:
                self.known.remove(other)
        raise UnhandledQuery
            
def main():
    url, directory,  secret = sys.argv[1:]
    n = Node(url,directory,secret)
    n._start()
    
if __name__ == '__main__': main()

'''
解说 
def inside(dir,name):
    """
检查给定的目录中是否有给定的文件名
"""
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir,''))
    
In [2]: dir='/home/evan/kvm/'

In [3]: name='/home/evan/kvm/kvmsn'

In [4]: from os.path import join, abspath,isfile

In [5]: dir = abspath(dir)

In [6]: dir 
Out[6]: '/home/evan/kvm'

In [7]:  name = abspath(name)

In [8]: name
Out[8]: '/home/evan/kvm/kvmsn'

In [9]: join(dir,'')
Out[9]: '/home/evan/kvm/'

In [10]: name.startswith(join(dir,''))
Out[10]: True



result = self.query(query) #调用同一个类中的其它方法 要先self.方法名

调用同一个类中的其它方法 要先self.方法名
02. 私有方法
def __send(self):

class Dog:

    #私有方法
    def __send_msg(self):
        print("------正在发送短信------")

    #公有方法
    def send_msg(self, new_money):
        if new_money>10000:
            self.__send_msg()
        else:
            print("余额不足,请先充值 再发送短信")

dog = Dog()
dog.send_msg(100)



hello 方法 
In [11]:      def  hello(other):
    ...:     
    ...:           """     假设已知的URL的集合叫做known ,hello 方法非常 简单 只是把other加入到self.known 内,other是唯一的参数  一个URL 
    ...:     """
    ...:           known.add(other) #add() 方法用于给集合添加元素，如果添加的元素在集合中已存在，则不执行任何操作
    ...:  

In [12]:  hello(other)

In [13]: known
Out[13]: {'a.com'}


'''
                
          
