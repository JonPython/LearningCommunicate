
'''服务器模块>>>
    1,建立服务器,持续运行,使用多进程处理并发机制
    2,导入数据库链接,操作数据库
    3,分类处理各类客户端请求调用函数
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
import multiprocessing as mp
import sys
import signal
import time
import question as qt  # 导入问题数据库

HOST = '0.0.0.0'
PORT = 12333
ADDR = (HOST, PORT)
BUFFERSIZE = 1024


# 建立服务端,
def waitconn():
    # 建立与客户端的链接
    so = socket()
    so.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    so.bind(ADDR)
    so.listen(5)
    # 忽略子进程退出,防止僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # 处理并发
    while True:
        try:
            co, addr = so.accept()
        except KeyboardInterrupt:
            co.close()
            sys.exit(0)
        except Exception:
            continue
        p = mp.Process(target=main, args=(co,))
        p.start()


# 连接数据库,处理客户端各种请求
def main(co):
    while True:
        data = co.recv(BUFFERSIZE).decode()
        L = data.split('#.#')
        print('OK',L)
        if L[0] == 'login':
            login(co, L)
        elif L[0] == 'enter':
            enter(co, L)
        elif L[0] == 'type':
            type1(co, L)
        elif L[0] == 'mtype':
            type1(co, L, 1)
        elif L[0] == 'sameask':
            sameask(co, L)
        elif L[0] == 'hot':
            hot(co)
        elif L[0] == 'mhot':
            hot(co, 1)
        elif L[0] == 'answer':
            answer(co, L)
        elif L[0] == 'ask':
            ask(co, L)
        elif L[0] == 'question':
            quest(co, L)
        elif L[0] == 'applyfor':
            applyfor(co, L)
        elif L[0] == 'single':
            single(co, L)
        elif L[0] == 'reply':
            reply(co, L)
        elif L[0] == 'show':
            show(co, L)
        elif L[0] == 'messageto':
            messageto(co,L)
        elif L[0] == 'messageto2':
            messageto2(co,L)
        elif L[0] == 'message':
            message(co,L)
        else:
            break


# 请求留言信息
def message(co,L):
    user=L[1]
    ss=qt.message(user)
    co.send(ss.encode())

# 接收留言信息
def messageto(co,L):
    sid=L[1]
    mes=L[2]
    name=L[3]
    if qt.messageto(sid,mes,name):
        co.send(b'OK')
    else:
        co.send(b'E')


# 接收留言信息
def messageto2(co,L):
    user=L[1]
    mes=L[2]
    name=L[3]
    if qt.messageto2(user,mes,name):
        co.send(b'OK')
    else:
        co.send(b'E')



# 个人信息展示
def show(co, L):
    l = L[1].split('*.*')
    sid = l[0]
    name, mail, bri, sex = qt.show(sid)
    ss = name+'#.#'+mail+'#.#'+bri+'#.#'+sex
    co.send(ss.encode())


# 处理回答问题请求,发送结果
def reply(co, L):
    l1 = L[1].split('*.*')
    sid = int(l1[0])
    name = L[2]
    solution = L[3]
    if qt.reply(sid, name, solution):
        co.send(b'OK')
    else:
        co.send(b'E')


# 接受单个问题请求,发送结果
def single(co, L):
    l1 = L[1].split('*.*')
    sid = int(l1[0])
    a1, b1 = qt.single(sid)
    try:
        ss = a1[0]+'*.*问: '+a1[1]+'#.#'
        co.send(ss.encode())
        for i, j in b1:
            ss = i+'*.*答: '+j+'#.#'
            co.send(ss.encode())
        time.sleep(0.1)
        co.send('O#K'.encode())
    except TypeError:
        co.send('O#K'.encode())


# 存储申请分类信息,发送结果
def applyfor(co, L):
    user = L[1]
    title = L[2]
    content = L[3]
    if qt.applyfor(user, title, content):
        co.send(b'O#K')
    else:
        co.send(b'E')


# 处理同问点击请求,发送结果
def sameask(co, L):
    l1 = L[1].split('*.*')
    uid = int(l1[0])
    name = L[-1]
    n = qt.sameask(uid, name)
    n = str(n)
    co.send(n.encode())


# 处理具体类型问题的请求,发送结果
def type1(co, L, m=0):
    ty = L[1]
    l = qt.type10(ty, m)
    if not l:
        co.send(b'O#K')
    else:
        for i in l:
            ms = str(i[0])+'*.*'+i[1]+'*.*'+str(i[2])+'#.#'
            co.send(ms.encode())
        time.sleep(0.1)
        co.send(b'O#K')


# 处理我的回答请求,发送结果
def answer(co, l1):
    name = l1[1]
    l = qt.answer(name)
    for i in l:
        ms = i+'#.#'
        co.send(ms.encode())
    time.sleep(0.1)
    co.send(b'O#K')


# 处理我的提问请求,发送结果
def quest(co, l1):
    name = l1[1]
    msg = qt.question(name)
    for i in msg:
        ms = i+'#.#'
        co.send(ms.encode())
    time.sleep(0.1)
    co.send(b'O#K')


# 处理提问请求
def ask(co, l):
    name = l[1]
    type1 = l[2]
    title = l[3]
    quest = l[4]
    # 调用问题方法插入到数据库
    if qt.ask(name, type1, title, quest):
        co.send(b'O#K')
    else:
        co.send(b'E')


# 处理热门问题请求
def hot(co, m=0):
    l = qt.hot(m)
    if not l:
        co.send(b'O#K')
    else:
        for i in l:
            ms = str(i[0])+'*.*'+i[1]+'*.*'+str(i[2])+'#.#'
            co.send(ms.encode())
        time.sleep(0.1)
        co.send(b'O#K')


# 处理登录请求
def enter(co, l):
    name = l[1]
    passwd = l[2]
    # 判断用户名,密码是否正确
    if qt.checking(name, passwd):
        co.send(name.encode())
    else:
        co.send(b'E')


# 处理注册请求
def login(co, l):
    # 通过user模块的isexist函数判断用户名是否存在
    name = l[1]
    mail = l[2]
    brithday = l[3]
    sex = l[4]
    passwd = l[5]
    if qt.isexist(name):
        # 将用户名密码写入数据库
        qt.userinsert(name, mail, brithday, sex, passwd)
        co.send(b'succeed')
    else:
        co.send(b'E')  # 用户名已存在发送b'E'


#运行服务器和数据库
if __name__ == '__main__':
    try:
        qt.makesql()
    except Exception as e:
        print(e)
    waitconn()
