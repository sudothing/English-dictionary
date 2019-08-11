#!/usr/bin/env python3
# coding=utf-8

'''
name:xin
email:qq875614260@163.com
data:2019-8-10
introduce:client
env:python3.5
'''

from socket import *
import time,sys,os


class Dict_client():
    '''成功连接客户端后，进行的工作'''
    def __init__(self,s):
        self.sockfd = s


    def login(self):
        #登录功能,成功返回True,失败返回False
        self.sockfd.send(b'L')
        name = input('请输入name:')
        self.sockfd.send(name.encode())
        password = input('请输入password:')
        self.sockfd.send(password.encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'ok':
            return True
        else:
            print(data)
            return False

    def do_sign_in(self):
        #注册功能
        self.sockfd.send(b'S')
        name = input("name:")
        self.sockfd.send(name.encode())
        password = input('password:')
        self.sockfd.send(password.encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'ok':
            print('注册成功')
        else:
            print(data)

    def do_poll(self):
        self.sockfd.send(b"P")
        word = input('请输入需要查询的单词：')
        self.sockfd.send(word.encode())
        data = self.sockfd.recv(1024).decode().split('###')
        if data[0] == 'ok':
            print(data[1])
        else:
            print('查询失败')


    def do_hist(self):
        self.sockfd.send(b'H')
        cmd = self.sockfd.recv(1024).decode()
        if cmd == 'ok':
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == '###':
                    return
                print(data)
        else:
            print(cmd)


    def do_quit(self):
        self.sockfd.send(b'Q')


    def do_sign_out(self):
        self.sockfd.send(b'O')


def main():
    ADDR = ('127.0.0.1',8888)
    s = socket(AF_INET,SOCK_STREAM)
    try:
        s.connect(ADDR)
    except:
        print('服务器链接失败')
        return
    work = Dict_client(s)
    while True:
        login_print()
        try:
            i = int(input('请选择功能：'))
        except ValueError:
            print('功能输入错误')
            continue
        if i == 1:
            if work.login():
                #登录成功后,进图二级界面和二级界面功能
                while True:
                    inquire_print()
                    try:
                        j = int(input('请选择功能：'))
                    except ValueError:
                        print('功能输入错误')
                        continue
                    if j == 1:
                        work.do_poll()
                    elif j == 2:
                        work.do_hist()
                    elif j == 3:
                        work.do_sign_out()
                        break
                    else:
                        print("功能输入有误")
            else:
                continue
        elif i == 2:
            work.do_sign_in()
        elif i == 3:
            work.do_quit()
            s.close()
            sys.exit('感谢使用')
        else:
            print("功能输入错误")


def login_print():
    line1 = "+-------------------------+"
    line2 = "|   1登录  2注册  3退出   |"
    print(line1)
    print(line2)
    print(line1)

def inquire_print():
    line1 = "+-------------------------+"
    line2 = "|   1查词  2历史  3注销   |"
    print(line1)
    print(line2)
    print(line1)

if __name__ == '__main__':
    main()