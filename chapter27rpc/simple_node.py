#!/usr/bin/python
#-*- coding:utf-8 -*-
from xmlrpclib import ServerProxy
from os.path import join, isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys
MAX_HISTORY_LENGTH = 6

OK = 1
FAIL = 2
EMPTY = ''

#这个func 我还是不太懂
def getPort(url):
    """ 
    extracts the port from a URL 用 在URL中提取端口
    https://vimsky.com/article/3522.html Python urlparse函数详解 
    http://blog.51cto.com/yucanghai/1695439 web模块学习-- urlparse
    https://www.cnblogs.com/stemon/p/6602185.html url解析库--urlparse
    """
    name = urlparse(url)[1]  #[1] 要的第二元素  可能是个列表
    parts = name.split(':')
    return int(parts[-1])

class Node:
     """ 
     p2p网络中的节点
     
     
集合（set）是一个无序的不重复元素序列
     http://www.runoob.com/python3/python3-set.html
     
     https://blog.csdn.net/business122/article/details/7541486
     
     set
set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。

要创建一个set，需要提供一个list作为输入集合：

https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868193482529754158abf734c00bba97c87f89a263b000
     """
     def __init__(self,url,dirname,secret):
         self.url = url
         self.dirname = dirname
         self.secret = secret
         self.known = set() # 集合（set）是一个无序的不重复元素序列

     def query(self,query,history=[]):
         """
             查询文件，可能会向其它已知节点请求帮助 将文件作为字符串返回
         """
         code, data = self._handle(query)
         if code == OK:
             return code, data
         else:
             history = history + [self.url]
             if len(history) >= MAX_HISTORY_LENGTH:
                 return FAIL, EMPTY
             return self._broadcast(query,history)

     def  hello(self,other):
          """
            pass
  假设已知的URL的集合叫做known ,hello 方法非常 简单 只是把other加入到self.known 内,other是唯一的参数  一个URL 
          """
          self.known.add(other) #add() 方法用于给集合添加元素，如果添加的元素在集合中已存在，则不执行任何操作
          return OK
      
     def fetch(self, query,secret):
         """
         look here 20181120
         code, data 是元组 (code,data)
         """
         if secret != self.secret: return FAIL
         code, data = self.query(query)
         if code == OK:
             f = open(join(self.dirname,query),'w')
             f.write(data)
             f.close()
             return OK
         else:
             return FAIL

     def _start(self):
         """
         """
         s = SimpleXMLRPCServer(("",getPort(self.url)),logRequests=False)
         s.register_instance(self)
         s.serve_forever()
        
     def _handle(self, query):
         """
         """
         dir = self.dirname
         name = join(dir,query)
         if  not isfile(name): return  FAIL, EMPTY
         return  OK, open(name).read()

     def _broadcast(self,query, history):
         """
         here20181026
         """
         for other in self.known.copy():
             if other in history: continue
             try:
                 s = ServerProxy(other)
                 code, data = s.query(query,history)
                 if code == OK:
                     return code,data
             except:
                 self.known.remove(other)
         return FAIL, EMPTY

def main():
    url,directory, secret = sys.argv[1:]
    n = Node(url,directory,secret)
    n._start()

if __name__ == "__main__":
    main()

'''
python simple_node.py  http://localhost:4242 files1 secret1

python simple_node.py  http://localhost:4243 files2 secret2





#on ipython
from xmlrpclib import *
mypeer = ServerProxy('http://localhost:4242')
code , date = mypeer.query('test.txt')
code 
Out[4]: 2



In [5]: otherpeer = ServerProxy('http://localhost:4243')

In [6]: code, data = otherpeer.query('test.txt')

In [7]: code 
Out[7]: 2

In [8]: data
Out[8]: ''

In [9]: mypeer.query('test.txt')
Out[9]: [2, '']






#是有个fun没写完 
Fault: <Fault 1: "<type 'exceptions.NameError'>:global name 'query' is not defined">





'''
