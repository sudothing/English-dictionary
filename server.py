#!/usr/bin/env python3
# coding=utf-8

'''
name:xin
email:qq875614260@163.com
data:2019-8-10
introduce:server
env:python3.5
'''

from socket import *
import time,sys,os,signal,pymysql


dict_text = './dict.txt'

class Dict_server():
    '''成功连接客户端后，进行的工作'''
    def __init__(self,c):
        self.confd = c
        self.db = pymysql.connect(host='localhost',
            user='root',password='123456',
            database='English_dict',charset='utf8')

    def login(self):
        #登录功能,成功返回True,失败返回False
        #登录成功发送成功反馈后再查词
        #登录失败发送失败反馈
        self.name = self.confd.recv(1024).decode()
        password = self.confd.recv(1024).decode()
        cur = self.db.cursor()
        sql = 'select name,password from user where name=%s'
        cur.execute(sql,[self.name])
        data = cur.fetchall()
        if not data or data[0][1] != password:
            self.confd.send('信息有误,登录失败'.encode())
            return False
        else:
            self.confd.send(b'ok')
            return True


    def sign_in(self):
        #处理客户端的注册
        name = self.confd.recv(1024).decode()
        password = self.confd.recv(1024).decode()
        sql = 'insert into user(name,password) values(%s,%s);'
        cur = self.db.cursor()
        try:
            cur.execute(sql,[name,password])
            self.db.commit()
        except Exception as e:
            self.confd.send(str(e).encode())
        else:
            self.confd.send(b'ok')

    def do_poll(self):
        word = self.confd.recv(1024).decode()
        sql = 'select word,explains from dict where word=%s'
        cur = self.db.cursor()
        cur.execute(sql,[word])
        data = cur.fetchall()
        if not data or data[0][0] != word:
            self.confd.send('查询失败'.encode())
        else:
            try:
                sql = 'insert into hist(name,word) values(%s,%s)'
                cur.execute(sql,[self.name,word])
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
            explains = 'ok###' + data[0][1]
            self.confd.send(explains.encode())


    def do_hist(self):
        sql = 'select name,word,time from hist where name=%s limit 10;'
        cur = self.db.cursor()
        cur.execute(sql,[self.name])
        data = cur.fetchall()
        if not data:
            self.confd.send('无信息'.encode())
        else:
            self.confd.send(b'ok')
            time.sleep(0.1)
            for i in data:
                self.confd.send('|'.join(i[0:2]).encode())
                time.sleep(0.1)
            self.confd.send('###'.encode())


def main():
    #创建套接字
    ADDR = ('127.0.0.1',8888)
    s = socket(AF_INET,SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        try:
            c,addr = s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print('服务器异常',e)
            continue
        pid = os.fork()
        #创建子进程
        if pid == 0:
            s.close()
            work = Dict_server(c)
            while True:
                data = c.recv(1024).decode()
                if not data or data == 'Q':
                    c.close()
                    sys.exit('客户端退出')
                elif data == 'L':
                    if work.login():
                        #登录成功进入二级功能
                        while True:
                            cmd = c.recv(1024).decode()
                            if cmd == 'P':
                                work.do_poll()
                            elif cmd == 'O':
                                break
                            elif cmd == 'H':
                                work.do_hist()

                elif data == 'S':
                    work.sign_in()
        else:
            c.close()
            continue



if __name__ == '__main__':
    main()