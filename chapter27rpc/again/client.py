 #!/usr/bin/python
#-*- coding:utf-8 -*-
# listing27-3  注释  这个确定是可以的了
from xmlrpclib  import ServerProxy,Fault
from  cmd import Cmd
from random import choice #随机数
from  string import lowercase
from server   import Node, UNHANDLED #导入server.py
from threading import  Thread
from time import sleep
import sys
HEAD_START = 0.1 #Seconds
SECRET_LENGTH = 100

def randomString(length):
    """ pass  2019年 01月 23日 星期三 21:32:14 CST
返回给定长度的由字母组成的随机字符串  这里返回的密码为 len 99
In [5]: lowercase[:26]
Out[5]: 'abcdefghijklmnopqrstuvwxyz'

In [6]: lowercase[0:26]
Out[6]: 'abcdefghijklmnopqrstuvwxyz'

In [12]: chars
Out[12]: ['n', 'o']

In [13]: ''.join(chars)
Out[13]: 'no'


    """
    chars = []
    letters = lowercase[:26]
    while length >0 :
        length -= 1 # length=length-1
        chars.append(choice(letters)) # choice(letters) 每次只得一个字母
    return ''.join(chars)

class Client(Cmd):
    """
    
    """

    prompt = '>'


    def __init__(self,url,dirname,urlfile):
        """
设定 url, dirname, and urlfile ，并在单独的线程中启动Node服务器
In [8]: for line in open('./ufile'):
   ...:     line = line.strip()
   ...:     print line
www.a.com
www.b.com

        """

        Cmd.__init__(self)
        self.secret = randomString(SECRET_LENGTH)
        n = Node(url,dirname,self.secret)
        t = Thread(target = n._start) # 这个有空再看一下相关教程和视频才行
        t.setDaemon(1) #将该线程标记为守护进程 主线程完成就全退出
        t.start()
        # 让服务器先启动 Give
        sleep(HEAD_START)
        self.server = ServerProxy(url)
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)   # 直接加到 known set 里面 on server.py   2019年 01月 29日 星期二 23:12:11
        
    def do_fetch(self,arg):
        "调用服务器的fetch方法  #   here do_foo p415  arg 形参是是特定的么    不是，随便起名而已？      类方法一定有self       "
        try:
            self.server.fetch(arg,self.secret)
        except Fault, f:
            if f.faultCode != UNHANDLED: raise
            print "Couldn't find the file",arg

    def do_exit(self,arg):
        "Exit the program  do  的突然不太明白了  "
        print
        sys.exit()

    do_EOF = do_exit # 为什么是 = 呢

def main():
    urlfile,directory,url = sys.argv[1:] # 拆包 赋值， 这里开始 今晚才看到原来是导入了server 2019 01 22 pm
    client = Client(url,directory,urlfile)
    client.cmdloop()

if __name__ == '__main__': main()
