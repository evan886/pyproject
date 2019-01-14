#!/usr/bin/python
#-*- coding:utf-8 -*- # p411 还有要看一下 最好全理解 每行代码 
from xmlrpclib import ServerProxy
from os.path import join, isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys
import os 
MAX_HISTORY_LENGTH = 6
OK = 1
FAIL = 2
EMPTY = ''

def getPort(url):
    """ 
     here 2018年 12月 11日 星期二 23:18:39 CST extracts the port from a URL 用 在URL中提取端口
    https://www.cnblogs.com/stemon/p/6602185.html url解析库--urlparse
    In [5]: url = 'http://localhost:4242'
In [6]: name = urlparse(url)[1]
In [7]: print name
localhost:4242
In [8]: parts = name.split(':')
In [9]: parts[-1]
Out[9]: '4242'
   #这个func 我还是不太懂 从url中提取端口号 P412 
如果 
    In [10]: name = urlparse(url)

In [11]: print name 
ParseResult(scheme='http', netloc='localhost:4242', path='', params='', query='', fragment='')
    
    """
    name = urlparse(url)[1]  #[1] 要的第二元素  可能是个列表  localhost:4242
    parts = name.split(':')
    return int(parts[-1])

class Node:
     """ 
     p2p网络中的节点
集合（set）是一个无序的不重复元素序列
     http://www.runoob.com/python3/python3-set.html
     https://blog.csdn.net/business122/article/details/7541486
     
     set set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
要创建一个set，需要提供一个list作为输入集合：

https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868193482529754158abf734c00bba97c87f89a263b000
     """
     def __init__(self,url,dirname,secret):
         self.url = url
         self.dirname = dirname
         self.secret = secret
         self.known = set() # 集合（set）是一个无序的不重复元素序列

     def query(self,query,history=[]):
         print '11111'
         """
             查询文件，可能会向其它已知节点请求帮助 将文件作为字符串返回 ; 历史记录在一开始调用query的时候是空的  所以 是空列表
         """
         code, data = self._handle(query)
         if code == OK:
             #print data
             return code, data

         else:
             #_handle 内部查找不到的情况 
             history = history + [self.url]
             if len(history) >= MAX_HISTORY_LENGTH:
                 return FAIL, EMPTY
             return self._broadcast(query,history)

     def  hello(self,other):
          """     假设已知的URL的集合叫做known ,hello 方法非常 简单 只是把other加入到self.known 内,other是唯一的参数  一个URL     """
          self.known.add(other) #add() 方法用于给集合添加元素，如果添加的元素在集合中已存在，则不执行任何操作
          return OK
      
     def fetch(self, query,secret):
         """
         code, data 是元组 (code,data) ,   query 的返回值定义为一对元组  #look here 20181120
         """
         if secret != self.secret: return FAIL
         code, data = self.query(query)
         if code == OK:
             f = open(join(self.dirname,query),'w') #here /hoe/e.txt os.path.join 
             #f = open(os.path.join(self.dirname,query),'w') # join 全换成os.paht.join if import os 
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
         负责查询的内部处理(检查文件是否在于于特定的node 获取数据等等)
         """
         dir = self.dirname
         name = join(dir,query)  #here   /home/evan/1.php
         print name  #here
         if  not isfile(name): return  FAIL, EMPTY
         return  name,OK, open(name).read()

     def _broadcast(self,query, history):
         """
         2019here self.url 加入到history   self.known.copy() self.known的一个副本 不会在迭代过程中修改设置 安全一些地
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
    #n.query('test.txt')

if __name__ == "__main__":
    main()

"""
In [1]: t=[1,2,3,4]

In [2]: t[1:]
Out[2]: [2, 3, 4]


已确定  这个在 listing27-1.py 中通过了 

sys.argv[1:]   here is   http://localhost:4242 files1 secret1  3 point 

mkdir  files1 files2 ; touch files2/test.txt
python simple_node.py  http://localhost:4242 files1 secret1

python simple_node.py  http://localhost:4243 files2 secret2

#on ipython
from xmlrpclib import *
mypeer = ServerProxy('http://localhost:4242')

In [6]: mypeer.query('test.txt')
Out[6]: [2, '']

code , data = mypeer.query('test.txt')  # not date     #这是用到query 方法 然后?

In [10]: code 
Out[10]: 1


 otherpeer = ServerProxy('http://localhost:4243')
code, data = otherpeer.query('test.txt') #2019年 01月 14日 星期一 16:17:35 CST  有时不行，先不理这个就是查询test.txt 

In [10]: code 
Out[10]: 1


code 
Out[4]: 2  # touch files2/test.txt 少了这个 

cat  files2/test.txt 
'this is a test\\n\n'


In [14]: data
Out[14]: 'this is a test\\n\n' #要手工添加呀  


p414 把第一个节点介绍给第二个 
In [15]: mypeer.hello('http://localhost:4243')
Out[15]: 1

In [16]: mypeer.query('test.txt')
Out[16]: [1, 'this is a test\\n\n']


p415
In [17]: mypeer.fetch('test.txt','secret1')
Out[17]: 1

 ls files1/
test.txt




#是有个fun没写完 
Fault: <Fault 1: "<type 'exceptions.NameError'>:global name 'query' is not defined">
"""
