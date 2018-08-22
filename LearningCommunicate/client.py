
'''客户端模块>>>(两个功能):
    1,导入前端界面,建立主进程运行前端界面
    2,发送前端各种点击请求,并接收服务器返回结果

  请求列表:
    1.一级界面请求:1,9类类型问题展示,
                 2,热门问题展示
                 3,注册
                 4,登录
                 5,查看具体问题
    2,二级界面请求:在登录之后可使用>>
                1,提问功能
                2,查看我的提问
                3,查看我回答的问题
                4,申请增加分类
    3,具体问题界面请求:
                1,回答问题
                2,点击同问
                3,查看个人信息
                4,给问题人留言
'''

from socket import *
from multiprocessing import Process, Queue
import signal
import gui1  # 导入交互界面
import os ,sys


# HOST=sys.argv[1]  #外部连接
# PORT = int(sys.argv[2])   #外部连接
HOST = '127.0.0.1'  # 绑定服务器地址,本地连接
PORT = 12333
ADDR = (HOST, PORT)
BUFFERSIZE = 1024

# 建立与服务器连接
s = socket(AF_INET, SOCK_STREAM, 0)
s.connect(ADDR)
# 忽略子进程退出
signal.signal(signal.SIGCHLD, signal.SIG_IGN)


# 接收前端点击请求
def main(q, s):
    while True:
        msg = q.get()
        msg.strip()
        L = msg.split('#.#')
        print(L)
        # 根据不同请求发送不同消息给服务端
        if L[0] == 'login':
            login(s, msg)
        elif L[0] == 'enter':
            enter(s, msg)
        elif L[0] == 'ask':
            ask(s, msg)
        elif L[0] == 'applyfor':
            applyfor(s, msg)
        elif L[0] == 'reply':
            reply(s, msg)
        elif L[0] == 'type':
            type1(s, msg)
        elif L[0] == 'mtype':
            type1(s, msg)
        elif L[0] == 'sameask':
            sameask(s, msg)
        elif L[0] == 'hot':
            hot(s, msg)
        elif L[0] == 'mhot':
            hot(s, msg)
        elif L[0] == 'answer':
            answer(s, msg)
        elif L[0] == 'question':
            question(s, msg)
        elif L[0] == 'single':
            single(s, msg)
        elif L[0] == 'show': 
            show(s, msg)
        elif L[0] == 'messageto':
            messageto(s,msg)
        elif L[0] == 'messageto2':
            messageto(s,msg)
        elif L[0] == 'message':
            message(s,msg)
        else:
            print('msg>>', msg)


# 请求留言信息
def message(s,msg):
    s.send(msg.encode())
    ss=s.recv(BUFFERSIZE*4).decode()
    gui1.k.put(ss)

# 发送留言信息
def messageto(s,msg):
    s.send(msg.encode())
    ss=s.recv(BUFFERSIZE).decode()
    if ss=='OK':
        gui1.k.put(ss)
    else:
        gui1.k.put('E')


# 个人信息展示
def show(s, msg):
    s.send(msg.encode())
    ss = s.recv(BUFFERSIZE).decode()
    l = ss.split('#.#')
    gui1.k.put(l)


# 发送回答请求,接受返回结果
def reply(s, msg):
    s.send(msg.encode())
    sid = s.recv(BUFFERSIZE).decode()
    if sid == 'E':
        gui1.k.put('NO')
    else:
        gui1.k.put('OK')


# 发送单个问题显示请求,接受返回结果
def single(s, msg):
    s.send(msg.encode())
    ss = ''
    while True:
        n = s.recv(BUFFERSIZE).decode()
        if n == 'O#K':
            break
        ss += n
    l = ss.split('#.#')
    gui1.k.put(l)


# 发送申请分类请求,接受返回结果
def applyfor(s, msg):
    s.send(msg.encode())
    n = s.recv(BUFFERSIZE)
    if n == b'O#K':
        gui1.k.put('OK')
    else:
        gui1.k.put('NO')


# 发送同问点击请求,接收返回结果
def sameask(s, msg):
    s.send(msg.encode())
    n = s.recv(BUFFERSIZE).decode()
    gui1.k.put(n)


# 发送具体类型问题的请求,接收返回结果
def type1(s, msg):
    s.send(msg.encode())
    msg = ''
    while True:
        ms = s.recv(BUFFERSIZE).decode()
        if ms == 'O#K':
            break
        msg += ms
    l = msg.split('#.#')
    gui1.k.put(l)


# 发送我的回答请求,接收返回结果
def answer(s, ss):
    s.send(ss.encode())
    msg = ''
    while True:
        ms = s.recv(BUFFERSIZE).decode()
        if ms == 'O#K':
            break
        msg += ms
    l = msg.split('#.#')
    gui1.k.put(l)


# 发送我的提问请求,接收返回结果
def question(s, ss):
    s.send(ss.encode())
    msg = ''
    while True:
        ms = s.recv(BUFFERSIZE).decode()
        if ms == 'O#K':
            break
        msg += ms
    l = msg.split('#.#')
    gui1.k.put(l)


# 发送提问请求
def ask(s, msg):
    s.send(msg.encode())
    n = s.recv(BUFFERSIZE)
    if n == b'O#K':
        gui1.k.put('OK')
    else:
        gui1.k.put('NO')


# 发送热门问题和查看更多热门问题请求,接收返回结果
def hot(s, msg):
    s.send(msg.encode())
    msg = ''
    while True:
        ms = s.recv(BUFFERSIZE).decode()
        if ms == 'O#K':
            break
        msg += ms
    l = msg.split('#.#')
    gui1.k.put(l)  # 调用前端显示窗口


# 发送登录请求,接收返回结果
def enter(s, msg):
    # 接收登录信息
    s.send(msg.encode())
    sig = s.recv(BUFFERSIZE).decode()
    if sig == 'E':  # 登录信息有误
        gui1.k.put('E')
    else:
        gui1.k.put(sig)  # 打开登录后的界面


# 发送注册请求,接收返回结果
def login(s, msg):
    # 接收注册信息
    s.send(msg.encode())
    sig = s.recv(BUFFERSIZE)
    if sig == b'succeed':
        gui1.k.put('OK')  # 如果信息为b'E',说明用户名已经存在
    else:
        gui1.k.put('mistake')  # 提醒注册成功


# 建立客户端和前端的消息队列
q = Queue()
# 建立子进程运行客户端
if __name__ == '__main__':
    p1 = Process(target=main, args=(q, s))
    p1.daemon = True
    p1.start()
# 运行前端用户界面:
gui1.main(q)