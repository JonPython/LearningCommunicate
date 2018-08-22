'''GUI>>>:
  1,建立一级界面调用main:
    1.1调用9各类型问题显示
    1.2调用热门问题显示
    1.3具体问题查看弹窗
    1.4设置广告位
  2,注册弹窗:
    2.1,判断关键字
    2.2,判断帐号密码长度
    2.3,注册失败提醒,注册成功可以直接显示登录窗
  3,登录弹窗:
    3.1,判断用户名密码是否合法
    3.2,发送验证用户名密码是否正确
    3.3,登录之后权限变更显示
  4,登录之后可以使用功能:
    4.1,同问权限,
    4.2,提问权限,
    4.3,回答权限
    4.4,查看我的提问,
    4.5,查看我问过的问题,
    4.6,查看我回答过的问题,
    4.7,申请增加分类
    4.8,查看问题人的个人信息
    4.9,给问题人留言
    4.10,未登录时,使用以上功能提醒注册
    4.11,判断问题和答案长度以及是否合法
'''
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
# from tkinter.simpledialog import askstring
from multiprocessing import Queue

BKG = '#F1F5FB'  # 一类背景色
BKG_out = '#EDD3BC'  # 二类背景色
l = ["Python", "数据库", "网络编程", "WEB", "GUI",
     "模块相关", "项目相关", "其他", '心情墙']  # 类型列表
LIMIT = 0  # 同问控制变量,同用户同问题只能点击一次
NAME = ''  # 登录权限控制变量
k = Queue()


# 主窗口
def main(q):
    root = tk.Tk()
    style1 = ttk.Style()
    style1.configure('BW.TLabel', background=BKG,
                     foreground='black')
    root.title('学习交流系统')
    root.geometry('1200x800')
    root.configure(background='#FFD8AD')
    #  广告位   ==========================================
    tex1 = tk.Text(root, width=60, height=19)
    photo = PhotoImage(file='./zhi_pian.png')
    tex1.insert(END, '\n')
    tex1.image_create(END, image=photo)
    tex1.place(relx=0.75, rely=0.748, width=300, height=200)
    #======================================================
    area1, area2, area3, area4 = layout(root)
    aroot(q, area1)
    broot(q, area2)
    croot(q, area3)
    droot(q, area4)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    size = (5, 12, (width-5)/5, (height-12)/12)
    size = '%dx%d+%d+%d' % size
    root.geometry(size)
    root.maxsize(1300, 900)
    root.minsize(1200, 800)
    root.mainloop()


# 分区布局
def layout(root):
    A1 = tk.Frame(root, width=1200, height=600, bg=BKG)
    A1.pack()
    A2 = tk.Frame(root, width=900, height=200, bg=BKG)
    A2.pack(side='left')
    A1x = ttk.Panedwindow(A1, orient='horizontal')
    A1x.pack(fill='both', expand='True')
    A2x = ttk.Panedwindow(A2, orient='horizontal')
    A2x.pack(fill='both', expand='True')
    area1 = tk.LabelFrame(A1x, text='问题分类', width=700,
                          height=600, bg=BKG)
    A1x.add(area1)
    area2 = tk.Frame(A1x, width=500,
                     height=600, background=BKG)
    A1x.add(area2)
    area3 = tk.Frame(A2x, width=800,
                     height=200, bg=BKG)
    A2x.add(area3)
    area4 = tk.Frame(A2x, width=100,
                     height=200, bg=BKG)
    A2x.add(area4)
    return area1, area2, area3, area4


# A区部件
def aroot(q, area1):
    nb = ttk.Notebook(area1, style='BW.TLabel')
    nb.pack()
    l2 = []
    for x in l:
        i = tk.Frame(nb, bg=BKG)
        nb.add(i, text=x.center(int(144/len(l))-len(l)+5))
        y = tk.Frame(i, width=700, height=600, bg='#C4F2FF')
        y.pack(side='top')
        l2.append(y)

    def caodan(x, l3):
        liboxA = tk.Listbox(x, font=('Courier New', 16), bg=BKG_out,
                            width=60, height=23, selectmode='BROWSE')
        s1 = ttk.Scrollbar(x)
        liboxA['yscrollcommand'] = s1.set
        for j in l3:
            liboxA.insert(END, ' '+j)
        s1['command'] = liboxA.yview
        liboxA.pack(side='left')
        s1.pack(side='right', fill=Y)

        def gettitle(event):
            a = liboxA.curselection()
            titles = liboxA.get(a)
            single(q, str(titles))

        liboxA.bind('<Double-Button-1>', gettitle)

    for x in l2:
        caodan(x, type1(q, l[l2.index(x)]))


# B区控件
def broot(q, area2):
    def login1():
        login(q, B1)

    def enter1():
        enter(q, B1)

    def hot1():
        return hot(q)

    B1 = tk.Frame(area2, bg=BKG, width=600, height=30)
    B1.pack(side='top')
    la1 = tk.Label(B1, text='您尚未登陆...', font='黑体 12',
                   bg=BKG, fg='red')
    la1.place(relx=0.2, rely=0.2, width=150, height=30)
    # 注册区
    btn1 = tk.Button(B1, text='登录', bg=BKG, command=enter1)
    btn1.place(relx=0.65, width=70, height=30)
    btn2 = tk.Button(B1, text='注册', bg=BKG, command=login1)
    btn2.place(relx=0.8, width=70, height=30)
    # area2 热门问题区
    B2 = tk.LabelFrame(area2, text='热门问题', bg=BKG)
    B2.pack()

    def gettitle1(event):
        a = libox2.curselection()
        b = libox2.get(a)
        single(q, b)
    libox2 = tk.Listbox(B2, font=('Courier New', 14),
                        bg=BKG_out, width=33, height=24, selectmode='BROWSE')
    s3 = ttk.Scrollbar(B2)
    libox2['yscrollcommand'] = s3.set
    for it in hot1():
        libox2.insert(END, it)
    s3['command'] = libox2.yview
    libox2.pack(side='left')
    s3.pack(side='right', fill=Y)
    libox2.bind('<Double-Button-1>', gettitle1)


# C区部件
def croot(q, area3):
    A1 = tk.Frame(area3, bg=BKG, width=800, height=30)
    A1.pack(side='top')
    v = tk.StringVar()
    l.insert(0, '')
    v.set('Python')
    aa = ttk.OptionMenu(A1, v, *l)
    aa.place(relx=0, rely=0.1, width=90, height=28)
    aab = ttk.Label(A1, text='输入问题标题：', style='BW.TLabel')
    aab.place(relx=0.11, rely=0.1, width=90, height=30)
    tex = tk.Text(A1, width=90, height=1, font='黑体 14')
    tex.place(relx=0.22, rely=0.1, width=578, height=30)
    A2 = tk.Frame(area3, bg=BKG, width=800, height=168)
    A2.pack()
    lab1 = tk.Label(A2, text='我\n要\n提\n问', bg=BKG)
    lab1.place(relx=0, rely=0.1, width=30, height=90)
    tex1 = tk.Text(A2, width=122, height=15, font='黑体 14')
    tex1.place(relx=0.03, rely=0.04, width=730, height=150)

    def ask():
        if NAME == '':
            window1('请先登录!')
        else:
            type1 = v.get()
            title1 = tex.get('0.0', 'end')
            solution1 = tex1.get('0.0', 'end')
            if lengths(title1, solution1):
                window1('长度不合法')
            elif keywords(type1) or keywords(solution1):
                window1('包含非法字符')
            else:
                ask1(q, NAME, type1, title1, solution1)
    btn1 = tk.Button(A2, text=' \n提\n交\n', bg=BKG, command=ask)
    btn1.place(relx=0.96, rely=0.6, width=30, height=50)


# D区部件
def droot(q, area4):
    def question():
        if NAME == '':
            window1('请先登录!')
        else:
            # 调用 【我 问过的】窗口
            question1(q, NAME)

    def answer():
        if NAME == '':
            window1('请先登录!')
        else:
            answer1(q, NAME)

    def applyfor():
        if NAME == '':
            window1('请先登录!')
        else:
            applyfor1(q, NAME)
    A1 = tk.Frame(area4, bg=BKG, width=100, height=198)
    A1.pack()
    btn1 = ttk.Button(A1, text='我\n问\n过\n的',
                      command=question)
    btn1.place(relx=0.01, rely=0.05, width=30, height=100)
    btn2 = ttk.Button(A1, text='我\n回\n答\n过\n的',
                      command=answer)
    btn2.place(relx=0.31, rely=0.2, width=30, height=100)
    btn3 = ttk.Button(A1, text='申\n请\n增\n加\n分\n类',
                      command=applyfor)
    btn3.place(relx=0.61, rely=0.35, width=30, height=110)


# 居中显示函数:
def zcenter(t1, a, b):
    t1.update_idletasks()
    x = (t1.winfo_screenwidth()-t1.winfo_reqwidth()) / a
    y = (t1.winfo_screenheight()-t1.winfo_reqheight()) / b
    t1.geometry("+%d+%d" % (x, y))


# 判断问题标题,和内容长度:
def lengths(a, b):
    if len(a) > 40 or len(a) < 6:
        return True
    elif len(b) > 5000 or len(b) < 6:
        return True
    elif len(a) == 0 or len(b) == 0:
        return True
    else:
        return False


# 注册弹窗
def login(q, B1):
    a = b = c = d = e = f = ''

    def for_abc(a, b, c, f):
        Zc = tk.Toplevel()
        Zc.title('注册窗')
        Zc.geometry('600x400')
        Af = tk.Frame(Zc, bg=BKG, width=600, height=400)
        Af.pack()
        lab1 = tk.Label(Af, text='用户名', bg=BKG)
        lab2 = tk.Label(Af, text='联系方式', bg=BKG)
        lab3 = tk.Label(Af, text='生日', bg=BKG)
        lab4 = tk.Label(Af, text='密码', bg=BKG)
        lab5 = tk.Label(Af, text='密码验证', bg=BKG)
        lab6 = tk.Label(Af, text='性别', bg=BKG)
        lab1.place(relx=0.3, rely=0.1, width=50, height=40)
        lab2.place(relx=0.3, rely=0.2, width=50, height=40)
        lab3.place(relx=0.3, rely=0.3, width=40, height=40)
        lab4.place(relx=0.3, rely=0.4, width=30, height=40)
        lab5.place(relx=0.3, rely=0.5, width=50, height=40)
        lab6.place(relx=0.3, rely=0.6, width=30, height=40)
        v = IntVar()
        v.set(0)
        rb1 = Radiobutton(Af, variable=v, text='女',
                          value=0, bg=BKG)
        rb1.place(relx=0.4, rely=0.6, width=50, height=40)
        rb2 = Radiobutton(Af, variable=v, text='男',
                          value=1, bg=BKG)
        rb2.place(relx=0.5, rely=0.6, width=50, height=40)
        rb3 = Radiobutton(Af, variable=v, text='保密',
                          value=2, bg=BKG)
        rb3.place(relx=0.6, rely=0.6, width=60, height=40)
        e1 = StringVar()
        e2 = StringVar()
        e3 = StringVar()
        ent1 = tk.Entry(Af, textvariable=e1)
        ent2 = tk.Entry(Af, textvariable=e2)
        ent3 = tk.Entry(Af, textvariable=e3)
        ent1.place(relx=0.4, rely=0.1, width=200, height=30)
        ent2.place(relx=0.4, rely=0.2, width=200, height=30)
        ent3.place(relx=0.4, rely=0.3, width=200, height=30)
        e1.set(a)
        e2.set(b)
        e3.set(c)
        ent4 = tk.Entry(Af, show='+')
        ent5 = tk.Entry(Af, show='-')
        ent4.place(relx=0.4, rely=0.4, width=200, height=30)
        ent5.place(relx=0.4, rely=0.5, width=200, height=30)

        def send1():
            a = ent1.get()
            b = ent2.get()
            c = ent3.get()
            d = ent4.get()
            e = ent5.get()
            f = v.get()
            if a == '' or b == '' or c == '' or d == '' or e == '':
                Zc.destroy()
                for_abc(a, b, c, f)
                return
            elif d != e:
                lab_x = tk.Label(Af, text='密码不一致！',
                                 fg='red', bg=BKG)
                lab_x.place(relx=0.75, rely=0.6, width=80, height=40)
                return
            ss = 'login'
            if f == 0:
                f = '女'
            elif f == 1:
                f = '男'
            else:
                f = '保密'
            for x in [str(a), str(b), str(c), f, str(d)]:
                ss += ('#.#' + x)
            if msgmistake(q, ss):
                text = '输入信息长度不得小于6大于20!'
                text2 = '\n或者包含以下关键字:"*.*","#.#"!'
                text += text2
                msgmistake1(text)
            else:
                succeed1(q, ss, Zc, B1)

        def reset1():
            Zc.destroy()
            login(q, B1)
        btn1 = tk.Button(Zc, text='确定', bg=BKG, command=send1)
        btn2 = tk.Button(Zc, text='重置', bg=BKG, command=reset1)
        btn1.place(relx=0.4, rely=0.75, width=90, height=30)
        btn2.place(relx=0.55, rely=0.75, width=90, height=30)
        zcenter(Zc, 2, 3)
        Zc.mainloop()

    for_abc(a, b, c, f)


# 注册信息不合法弹窗
def msgmistake1(m):
    A1 = tk.Tk()
    A1.title('')
    A1.geometry('500x200')
    tk.Label(A1, text=m, font='宋体 15').place(relx=0.2, rely=0.25)
    zcenter(A1, 2.4, 2.9)

    def close():
        A1.destroy()
    tk.Button(A1, text='确认', command=close).place(
        relx=0.42, rely=0.55)
    A1.mainloop()


# 判断帐号密码长度
def length(m):
    if len(m) < 6 or len(m) > 20:
        return True
    else:
        return False


# 判断关键字
def keywords(m):
    if '*.*' in m:
        return True
    elif '#.#' in m:
        return True
    elif '管理员' in m:
        return True
    else:
        return False


# 判断注册信息是否合法
def msgmistake(q, msg):
    L = msg.split('#.#')
    if length(L[1]) or length(L[5]):
        return True
    elif keywords(L[1]+L[2]+L[3]+L[4]+L[5]):
        return True
    else:
        return False


# 注册成功弹窗:
def succeed1(q, s, Zc, B1):
    q.put(s)
    n = k.get()

    def enter1():
        A1.destroy()
        Zc.destroy()
        enter(q, B1)
    if n == 'OK':
        A1 = tk.Tk()
        A1.title('xx')
        A1.geometry('500x200')
        tk.Label(A1,
                 text=' 注册成功!',
                 font='宋体 20').place(relx=0.35, rely=0.25)
        zcenter(A1, 2.4, 2.9)
        tk.Button(A1, text='马上登录', command=enter1).place(
            relx=0.42, rely=0.55)
        A1.mainloop()
    else:
        window1('用户名已经存在')


# 登录弹窗
def enter(q, B1):
    Zc = tk.Toplevel()
    Zc.title('登陆窗')
    Zc.geometry('600x400')
    Af = tk.Frame(Zc, bg=BKG, width=600, height=400)
    Af.pack()
    lab1 = tk.Label(Af, text='账户', bg=BKG)
    lab2 = tk.Label(Af, text='密码', bg=BKG)
    ent1 = tk.Entry(Af)
    ent2 = tk.Entry(Af, show='+')

    def send1():
        a = ent1.get()
        b = ent2.get()
        global NAME
        if length(a) or length(b):
            window1('长度不正确')
        elif succeed(q, a, b):
            window1('帐号或密码不正确')
        elif keywords(a) or keywords(b):
            window1('包含非法字符')
        elif NAME != '':
            window1('已经登录')
        else:
            NAME = str(a)
            la1 = tk.Label(B1, text=NAME+'：已登录',
                           font='黑体 12', bg=BKG, fg='lightblue')
            la1.place(relx=0.2, rely=0.2, width=150, height=30)
            Zc.destroy()
            message(a,q)

    def cancel():
        Zc.destroy()

    btn1 = tk.Button(Af, text='确定', bg=BKG, command=send1)
    btn2 = tk.Button(Af, text='取消', bg=BKG, command=cancel)
    lab1.place(relx=0.3, rely=0.2, width=30, height=40)
    ent1.place(relx=0.4, rely=0.2, width=200, height=30)
    lab2.place(relx=0.3, rely=0.3, width=30, height=40)
    ent2.place(relx=0.4, rely=0.3, width=200, height=30)
    btn1.place(relx=0.4, rely=0.5, width=90, height=30)
    btn2.place(relx=0.55, rely=0.5, width=90, height=30)
    zcenter(Zc, 2, 3)
    Zc.mainloop()


# 回复留言信息存储
def messageto2(q,user,mes,name):
    m='messageto2#.#%s#.#%s#.#%s' % (user,mes,name)
    q.put(m)
    ss=k.get()
    if ss=='OK':
        return True
    else:
        return False

        
# 接受留言信息
def message(a,q):
    m='message#.#%s' % a
    q.put(m)
    ss=k.get()
    def makemsg():
        def messageto1():
            mes=tt2.get('0.0','end')
            nonlocal l
            me=l[0].split("*.*")
            name=me[0]
            messageto2(q,name,mes,a)
            window1('回复成功!')
        t1 = tk.Tk()
        t1.title('留言信息')
        t1.geometry('800x500')
        f2 = tk.Frame(t1)
        f2.pack(side='top')
        tt = tk.Text(f2, font='黑体 16',
                     width=64, height=9, bg='lightblue')
        ts = ttk.Scrollbar(f2)
        tt['yscrollcommand'] = ts.set        
        tt.insert(END, ' '+j)
        ts['command'] = tt.yview
        tt.pack(side='left')
        ts.pack(side='right', fill=Y)
        f4 = tk.Frame(t1, width=780, height=40, bg='lightblue')
        f4.pack(side='bottom')
        la1 = tk.Label(f4, text='表达和沟通是最重要的事,找不到态度就回到真诚',
                       font='黑体 14', width=58)
        la1.pack(side='left')
        tbt2 = tk.Button(f4, text='回 复', width=50,
                         command=messageto1)
        tbt2.pack(side='right')
        f3 = tk.Frame(t1)
        f3.pack(side='bottom')
        tt2 = tk.Text(f3, font='黑体 16',
                      width=64, height=4, bg='white')
        ts2 = ttk.Scrollbar(f3)
        tt2['yscrollcommand'] = ts2.set
        ts2['command'] = tt2.yview
        tt2.pack(side='left')
        ts2.pack(side='right', fill=Y)
        zcenter(t1, 1.5, 2.7)

    if ss=='nothing':
        pass
    else:
        l=ss.split('#.#')        
        for j in l:
            if j=='':
                break
            else:
                makemsg()


# 判断用户名密码是否正确
def succeed(q, a, b):
    m = 'enter#.#%s#.#%s' % (a, b)
    q.put(m)
    n = k.get()
    if n == 'E':
        return True
    else:
        return False


# 热门问题函数:
def hot(q):
    m = 'hot#.#'
    q.put(m)
    L = k.get()
    return L


# 类型调用函数
def type1(q, x):
    m = 'mtype#.#%s' % x
    q.put(m)
    L = k.get()
    return L


# 单个问题显示:
def single(q, titles):
    # 同问函数:
    if len(titles) < 6:
        return

    def sameask1():
        global LIMIT
        if NAME == '':
            window1('请先登录!')
        elif LIMIT == 0:            
            LIMIT = 1
            n = sameask(q, titles, NAME)
            l = titles.split('*.*')
            m = l[0]+'*.*'+l[1]+'*.*'+n
            t1.destroy()
            single(q, m)
        elif LIMIT== 1:
            LIMIT=0
        else:
            pass

    def reply1():
        a = tt2.get('0.0', 'end')
        if NAME == '':
            window1('请先登录!')
        else:
            reply(q, titles, a, NAME)
            t1.destroy()

    def show1():
        if NAME == '':
            window1('请先登录')
        else:
            show(q, titles, NAME)

    m = 'single#.#'+titles
    q.put(m)
    solution = k.get()
    t1 = tk.Tk()
    t1.title('具体问题')
    t1.geometry('800x500')
    f1 = tk.Frame(t1, width=780, height=30)
    f1.pack(side='top')
    te1 = tk.Text(f1, font='黑体 16', width=49,
                  height=1, bg='lightblue')
    te1.insert(INSERT, titles, solution)
    te1.pack(side='left')
    l = titles.split('*.*')
    n = l[2]
    tbt2 = tk.Button(f1, text='同问 (%s)' % n, font='宋体 11',
                     height=1, command=sameask1)
    tbt2.pack(side='left')
    tbt1 = tk.Button(f1, text='联系本人', font='宋体 11', width=9,
                     height=1, command=show1)
    tbt1.pack(side='left')
    f2 = tk.Frame(t1)
    f2.pack(side='top')
    tt = tk.Text(f2, font='黑体 16',
                 width=64, height=9, bg='lightblue')
    ts = ttk.Scrollbar(f2)
    tt['yscrollcommand'] = ts.set
    lim = 0
    for j in solution:
        if lim == 0:
            tt.insert(END, ' '+j+'\n')
            lim = 1
        else:
            tt.insert(END, ' '+j)
    ts['command'] = tt.yview
    tt.pack(side='left')
    ts.pack(side='right', fill=Y)
    # def gettitle(event):
    #         a=tt.curselection()
    #         title=tt.get(a)
    #         show(q,title,NAME)
    # tt.bind('<Double-Button-1>',gettitle)
    f4 = tk.Frame(t1, width=780, height=40, bg='lightblue')
    f4.pack(side='bottom')
    la1 = tk.Label(f4, text='表达和沟通是最重要的事,找不到态度就回到真诚',
                   font='黑体 14', width=58)
    la1.pack(side='left')
    tbt2 = tk.Button(f4, text='回 复', width=50,
                     command=reply1)
    tbt2.pack(side='right')
    f3 = tk.Frame(t1)
    f3.pack(side='bottom')
    tt2 = tk.Text(f3, font='黑体 16',
                  width=64, height=4, bg='white')
    ts2 = ttk.Scrollbar(f3)
    tt2['yscrollcommand'] = ts2.set
    ts2['command'] = tt2.yview
    tt2.pack(side='left')
    ts2.pack(side='right', fill=Y)
    zcenter(t1, 1.5, 2.7)


# 同问函数
def sameask(q, title, name):
    m = 'sameask#.#'+title+'#.#'+name
    q.put(m)
    n = k.get()
    return n


# 回复问题函数:
def reply(q, title, solution, name):
    m = 'reply#.#'+title+'#.#'+name+'#.#'+solution
    q.put(m)
    n = k.get()
    if n == 'OK':
        single(q, title)
    else:
        window1('含有非法字符')


#发送留言
def messageto(q,sid,mes,name):
    m='messageto#.#%s#.#%s#.#%s' % (sid,mes,name)
    q.put(m)
    ss=k.get()
    if ss=='OK':
        return True
    else:
        return False


# 查看个人信息弹窗,发送离线消息:
def show(q, title, name):
    def oneanswer():
        mes=tt2.get('0.0', 'end')
        if keywords(mes):
            window1('包含非法字符!')
        else:
            l=title.split('*.*')
            sid=l[0]
            if messageto(q,sid,mes,name):
                window1('留言发送成功!')
            else:
                window1('留言发送失败!')
        
    m = 'show#.#'+title+'#.#'+name
    q.put(m)
    msg = k.get()
    name1, mail, bri, sex = msg[0], msg[1], msg[2], msg[3]
    t1 = tk.Tk()
    t1.title('信息')
    t1.geometry('800x500')
    f1 = tk.LabelFrame(t1, width=780, height=330)
    f1.pack(side='top')
    lab1 = tk.Label(f1, text='  用户名：', font='宋体 15')
    lab2 = tk.Label(f1, text='联系方式：', font='宋体 15')
    lab3 = tk.Label(f1, text='    生日：', font='宋体 15')
    lab4 = tk.Label(f1, text='    性别：', font='宋体 15')
    lab6 = tk.Label(f1, text='照\n片', font='宋体 17')
    lab1.place(relx=0.01, rely=0.2, width=100, height=40)
    lab2.place(relx=0.01, rely=0.3, width=100, height=40)
    lab3.place(relx=0.01, rely=0.4, width=100, height=40)
    lab4.place(relx=0.01, rely=0.5, width=100, height=40)
    lab6.place(relx=0.5, rely=0.3, width=40, height=100)
    lab1 = tk.Label(f1, text=name1)
    lab2 = tk.Label(f1, text=mail)
    lab3 = tk.Label(f1, text=bri)
    lab4 = tk.Label(f1, text=sex)
    lab6 = tk.Label(f1, text='')
    lab1.place(relx=0.2, rely=0.2, width=200, height=40)
    lab2.place(relx=0.2, rely=0.3, width=200, height=40)
    lab3.place(relx=0.2, rely=0.4, width=200, height=40)
    lab4.place(relx=0.2, rely=0.5, width=200, height=40)
    lab6.place(relx=0.6, rely=0.3, width=220, height=120)
    f4 = tk.Frame(t1, width=780, height=40, bg='white')
    f4.pack(side='bottom')
    la1 = tk.Label(f4, text='畅所欲言', font='黑体 16', width=50)
    la1.pack(side='left')
    tbt2 = tk.Button(f4, text=' 留 言 ', width=30,
                     command=oneanswer)
    tbt2.pack(side='right')
    f3 = tk.Frame(t1)
    f3.pack(side='top')
    tt2 = tk.Text(f3, font='黑体 16',
                  width=69, height=8, bg='white')
    ts2 = ttk.Scrollbar(f3)
    tt2['yscrollcommand'] = ts2.set
    ts2['command'] = tt2.yview
    tt2.pack(side='left')
    ts2.pack(side='right', fill=Y)
    zcenter(t1, 1.79, 2.3)
    t1.mainloop()


# 提交问题
def ask1(q, name, type1, title1, solution1):
    m = 'ask#.#'+name+'#.#'+type1+'#.#'+title1+'#.#'+solution1
    q.put(m)
    n = k.get()
    if n == 'OK':
        window1('提交成功')
    else:
        window1('提交失败')


# 我问过的问题弹窗
def question1(q, m):
    F1 = tk.Tk()
    F1.title('我问过的问题')
    F1.geometry('800x600')
    B2 = tk.LabelFrame(F1, text='我问过的问题', bg=BKG)
    B2.pack()

    def gettitle1(event):
        a = libox2.curselection()
        b = libox2.get(a)
        single(q, b)
    libox2 = tk.Listbox(B2, font=('Courier New', 14),
                        bg=BKG_out, width=72, height=25, selectmode='BROWSE')
    s3 = ttk.Scrollbar(B2)
    libox2['yscrollcommand'] = s3.set
    for it in question2(q, m):
        libox2.insert(END, it)
    s3['command'] = libox2.yview
    libox2.pack(side='left')
    s3.pack(side='right', fill=Y)
    libox2.bind('<Double-Button-1>', gettitle1)
    zcenter(F1, 1.85, 2.7)
    F1.mainloop()


# 我问过的问题
def question2(q, m):
    n = 'question#.#' + m
    q.put(n)
    l = k.get()
    return l


# 我回答过的问题弹窗
def answer1(q, m):
    F1 = tk.Tk()
    F1.title('我回答过的问题')
    F1.geometry('800x600')
    B2 = tk.LabelFrame(F1, text='我回答过的问题', bg=BKG)
    B2.pack()

    def gettitle1(event):
        a = libox2.curselection()
        b = libox2.get(a)
        single(q, b)
    libox2 = tk.Listbox(B2, font=('Courier New', 14),
                        bg=BKG_out, width=72, height=25, selectmode='BROWSE')
    s3 = ttk.Scrollbar(B2)
    libox2['yscrollcommand'] = s3.set
    for it in answer2(q, m):
        libox2.insert(END, it)
    s3['command'] = libox2.yview
    libox2.pack(side='left')
    s3.pack(side='right', fill=Y)
    libox2.bind('<Double-Button-1>', gettitle1)
    zcenter(F1, 1.85, 2.7)
    F1.mainloop()


# 我回答过的问题
def answer2(q, m):
    n = 'answer#.#' + m
    q.put(n)
    l = k.get()
    return l


# 申请增加分类弹窗
def applyfor1(q, m):
    F1 = tk.Tk()
    F1.title('申请增加分类')
    F1.geometry('800x400')
    A1 = tk.Frame(F1, bg=BKG, width=800, height=400)
    A1.pack()

    def diaoyong():
        a1 = tex1.get('0.0', 'end')
        # a2 = tex2.get()
        a3 = tex3.get('0.0', 'end')
        if keywords(a1) or keywords(a3):
            window1('包含非法字符')
        elif lengths(a1, a3):
            window1('长度错误')
        else:
            name = NAME
            applyfor2(q, name, a1, a3)

    la1 = tk.Label(A1, text='标 题:', bg=BKG)
    la1.place(relx=0.01, rely=0.02, width=50, height=40)
    la2 = tk.Label(A1, text='姓 名:', bg=BKG)
    la2.place(relx=0.75, rely=0.02, width=50, height=40)

    tex1 = tk.Text(A1, width=90, height=1, font='黑体 14')
    tex1.place(relx=0.01, rely=0.1, width=578, height=30)

    tex2 = tk.Text(A1, width=90, height=1, font='黑体 14')
    tex2.place(relx=0.75, rely=0.1, width=140, height=30)

    tex3 = tk.Text(A1, width=100, height=25)
    tex3.place(relx=0.01, rely=0.23, width=732, height=290)

    btn1 = tk.Button(A1, text=' \n\n提\n交\n\n',
                     bg='white', command=diaoyong)
    btn1.place(relx=0.95, rely=0.6, width=30, height=80)
    zcenter(F1, 1.87, 2.7)
    F1.mainloop()


# 申请增加分类
def applyfor2(q, name, title, solution):
    m = 'applyfor#.#'+name+'#.#'+title+'#.#'+solution
    q.put(m)
    n = k.get()
    if n == 'OK':
        window1('提交成功')
    else:
        window1('提交失败')


# 通用提醒弹窗:
def window1(m):
    A1 = tk.Tk()
    A1.title('')
    A1.geometry('500x200')
    tk.Label(A1, text=m, font='宋体 20').place(relx=0.35, rely=0.3)
    zcenter(A1, 2.4, 2.9)

    def close():
        A1.destroy()
    tk.Button(A1, text='确认', command=close).place(
        relx=0.42, rely=0.55)
    A1.mainloop()
