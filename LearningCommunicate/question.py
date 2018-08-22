# coding="utf-8"

'''问题数据库>>>:
    1,使用库名Ifquestion
    2.1,建立问题总表userask,字段包含:
        1,uid(int主键,自增长),
        2,用户名user(非空),
        3,问题类型type(enum,包含:"Python","数据库","网络编程","WEB",
        "GUI","模块相关","项目相关","其他","心情墙")
        4,问题标题title(限制40个字)
        5,问题详情question(varchar(5000))
        6,图片字段img1 mediumblob
        7,'同问'计数使用number(int,默认为1)
        8,同问用户记录numusers(varchar(5000),默认为'')
    2.2,建立问题答案表solution,字段包含:
        答案id:aid(int主键自增长)
        问题唯一标识:sid(userask表uid)
        回答者:answers(char(20))
        问题答案:solutions(varchar(5000))
        图片字段:img2 mediumblob
    2.3,建立用户表users包含字段:
        用户名name(唯一性,非空,20)
        邮箱mail
        生日brithday
        性别sex
        密码password(非空,20)
        头像img3 blob
  以下为用户类功能:
    1,处理申请分类applyfor
    2,提供验证用户名唯一性调用函数isexist
    3,提供用户名,密码调用函数checking
    4,提供注册成功插入函数userinsert
    5,个人信息展示show
    6,对密码进行加密处理
  以下是问题类功能:       
    1,提供函数type10
    分别调用9个类型的问题,并按'同问'字段从大到小排序,返回uid,title,number
    2,提供函数sameask
      '同问'按钮点击后数值+1的功能,同一个id的问题同一用户只生效一次
    3,提供热门问题函数hot
      所有问题根据'同问'字段从大到小排序,返回uid,title,number
    4,提供用户回答过的问题调用函数answer,返回问题标题
    5,提供提问问题提交函数ask
      包含用户名,问题类型,问题标题以及问题详情,插入到总表.
    6,提供回答问题调用函数reply,插入答案
    7,提供用户提问过的问题调用函数question,返回uid,title,number
    8,提供单个显示问题调用函数single,
      包含用户名,问题详情,所有回答者和他们的答案
'''
import pymysql

db = pymysql.connect('localhost', 'root', '123456', charset="utf8")
cs = db.cursor()


# 一般情况下,库会另外提前单独创建,本函数是为在不同主机上调试使用
def makesql():
    # 创建Ifquestion库
    cs.execute('drop database Ifquestion;')  # 测试用
    cs.execute('''create database if not exists 
        Ifquestion default charset="utf8";''')
    cs.execute('''use Ifquestion;''')
    # 创建userask表,
    # uid,user,type,title,question,number,numbers
    # 图片字段img1 mediumblob
    cs.execute('''create table if not exists 
        userask(uid int primary key auto_increment,
        user char(20) not null,type enum(
        "Python","数据库","网络编程","WEB",
        "GUI","模块相关","项目相关","其他","心情墙"),
        title char(40),question varchar(5000),
        img1 mediumblob,
        number int default 1,
        numusers varchar(5000) default "",
        index(number)
        ) default charset="utf8";''')
    # 建立问题答案表solution
    # 问题id:sid(int)
    # 答案id:aid(int)
    # 所有回答者:answers(char(20)
    # 问题答案:solutions(varchar(5000))
    # 图片字段img2
    cs.execute('''create table if not exists 
        solution(aid int primary key auto_increment,
        sid int,answers char(20),
        solutions varchar(5000),
        img2 mediumblob,
        index(sid)) default charset="utf8";
        ''')
    # 建立用户表users包含字段:
    # 用户名name(唯一性,非空)
    # 邮箱mail
    # 生日brithday
    # 性别sex
    # 密码password(非空,最少6位)
    # 头像img3 blob
    cs.execute('''create table if not exists 
        users(name char(20) primary key,
        mail char(30),brithday char(20),
        sex enum('男','女','保密'),
        password char(20) not null,
        img3 blob);''')
    # 建立申请分类表applyfor,字段包含:
    # 用户名user,申请标题title,申请内容content(500字)
    cs.execute('''create table if not exists
        applyfor(user char(20),title char(40),
        content varchar(500));''')
    # 创建留言表message,字段包含:
    # 用户名user,内容content,留言者name
    cs.execute('''create table if not exists 
        message(user char(20),content varchar(1000),
        name char(20));''')
    # 创建留言记录表msghistory,字段包含:
    # 用户名user,内容content,留言者name
    cs.execute('''create table if not exists 
        msghistory(user char(20),content varchar(1000),
        name char(20));''')
    insert1()  # 测试用
    db.commit()


#测试用数据插入函数
def insert1():
    f = open('./wenjian.txt', 'r')
    f = f.read()
    cs.execute('''use Ifquestion;''')
    l = f.split('－－－－－－－－－－')
    try:
        for i in l:
            s = i.split('#.#')
            sql = '''insert into userask(user,type,title,question) 
            values('%s','%s','%s','%s');''' % (
                s[0][1:], s[1].strip(), s[2].strip(), s[3])
            cs.execute(sql)
        f.close()
        cs.execute('''insert into users(name,mail,brithday,sex,password)
             values('未知','666666@qq,com','01010101','保密','123456');''')
    except IndexError as e:
        pass


#-----------------用户类功能-------------------------
# 处理申请分类
def applyfor(user, title, content):
    try:
        cs.execute('''insert into applyfor values(
            '%s','%s','%s');''' % (user, title, content))
        return True
    except:
        return False


# 1.1,提供验证用户名唯一性调用函数isexist
def isexist(name):
    cs.execute('''select name from users  
        where name='%s';''' % name)
    n = cs.fetchone()
    if n == None:  # 如果不存在,说明用户名可用
        return True
    else:
        return False


# 1.2,提供用户名,密码验证函数checking
def checking(name, passwd):
    password = encryption(passwd)
    cs.execute('''select name,password from users  
        where name='%s' and password='%s';
        ''' % (name, password))
    n = cs.fetchone()
    if n == None:  # 如果不存在,说明用户名或密码不正确
        return False
    else:
        return True


# 1.3,提供注册成功插入函数userinsert
def userinsert(name, mail, brithday, sex, passwd):
    password = encryption(passwd)
    cs.execute('''insert into users(name,
        mail,brithday,sex,password) values(
        '%s','%s','%s','%s','%s');
        ''' % (name, mail, brithday, sex, password))


# 1.4,个人信息展示
def show(sid):
    cs.execute('''select user from userask where uid='%s';''' % sid)
    name = cs.fetchone()[0]
    cs.execute('''select mail,brithday,sex from users 
        where name='%s';''' % name)
    l = cs.fetchone()
    try:
        mail, bri, sex = l[0], l[1], l[2]
        return (name, mail, bri, sex)
    except TypeError:
        return ('未知','666666@qq,com','01010101','保密')


# 1.5,存储留言信息
def messageto(sid,mes,name):
    cs.execute('''select user from userask where uid='%s';''' % sid)
    user = cs.fetchone()[0]
    try:
        cs.execute('''insert into message(user,content,name) 
            values('%s','%s','%s');''' % (user,mes,name))
        cs.execute('''insert into msghistory(user,content,name) 
            values('%s','%s','%s');''' % (user,mes,name))
        return True
    except:
        return False


# 1.6,存储留言信息
def messageto2(user,mes,name):
    try:
        cs.execute('''insert into message(user,content,name) 
            values('%s','%s','%s');''' % (user,mes,name))
        return True
    except:
        return False


# 1.7,查询留言信息
def message(user):
    cs.execute('''select content,name from message where 
        user='%s';''' % user)
    l=cs.fetchall()
    if len(l)<1:
        return 'nothing'
    else:
        s=''
        for i in l:
            s+=(i[1]+'*.*留言: '+i[0]+'#.#')
        cs.execute('''delete from message where user='%s';
            ''' % user)
        return s


# 简单加密
def encryption(msg):
    s = msg[3]
    l = msg.split(s)
    s1 = chr(ord(s)+1)
    msg1 = s1.join(l)
    return msg1


# -----------------问题类功能-------------------------
# 1提供函数分别调用9个类型的问题,并按'同问'字段从大到小排序
def type10(type1, m):
    # 传参type1(python或web...)和m,分别返回 10个类型问题的
    # 标题（title) 同问(number)
    if m == 0:
        # 所有问题根据'同问'字段从大到小排序,取前十个记录的标题和同问数
        sql = '''select uid,title,number from userask where type='%s' 
        order by number desc limit 20;''' % type1
    elif m == 1:
        # 所有问题根据'同问'字段从大到小排序,取所有个记录的标题和同问数
        sql = '''select uid,title,number from userask where type='%s' 
        order by number desc ;''' % type1
    cs.execute(sql)
    n = cs.fetchall()
    return n


# 2实现同问功能函数
# 提供'同问'按钮点击后数值+1的功能,同一个id的问题同一用户只生效一次
def sameask(uid, name):
    try:
        cs.execute('''select numusers from userask where uid=%d
            ''' % uid)
        s = cs.fetchone()[0]
        cs.execute('''select number from userask where uid=%d
            ''' % uid)
        n = cs.fetchone()[0]
        # 判断是否已经点击过按钮
        if (name in s) or ((len(s)+len(name)) > 5000):
            return n
        else:
            # 增加同问用户
            cs.execute('''update userask set numusers='%s' where
                 uid=%d''' % (s+name, uid))
            # 更改同问人数数量
            cs.execute('''update userask set number=%d where 
                uid=%d''' % (n+1, uid))
            return n+1
    except TypeError:
        return 1


# 3提供热门问题调用函数,所有问题根据'同问'字段从大到小排序
def hot(m):
    if m == 0:
        # 所有问题根据'同问'字段从大到小排序,取前十个记录的标题
        sql = '''select uid,title,number from userask 
        order by number desc limit 20;'''
    elif m == 1:
        # 所有问题根据'同问'字段从大到小排序,取所有的记录的标题
        sql = '''select uid,title,number from userask 
        order by number desc ;'''
    cs.execute(sql)
    n = cs.fetchall()
    return n


# 4提供用户回答过的问题调用函数,包含,问题标题
def answer(name):
    # name为提供用户名,取此用户名下的 问题类型,问提标题,同问计数 问题
    sql = '''select sid from solution 
    where answers='%s';''' % name
    cs.execute(sql)
    n = cs.fetchall()
    l = []
    for i in n:
        uid = i[0]
        cs.execute('''select uid,title,number from userask 
            where uid='%d';''' % uid)
        uid, title, number = cs.fetchone()
        l1 = str(uid)+'*.*'+title+'*.*'+str(number)
        l.append(l1)
    return l


# 5提供提问问题提交插入函数,包含用户名,问题类型,问题标题
# 以及问题详情,插入到总表.
def ask(name, type1, title, question):
    try:
        # 插入语句
        title = title.strip()
        question = question.strip()
        sql = '''insert into userask(user,type,title,question) 
        values('%s','%s','%s','%s');''' % (name, type1, title, question)
        cs.execute(sql)
        db.commit()
        return True
    except:
        return False


# 6提供回答问题调用函数,插入答案表
def reply(sid, name, solution):
    try:
        sql = '''insert into solution(sid,answers,solutions) 
        values('%d','%s','%s');''' % (sid, name, solution)
        cs.execute(sql)
        db.commit()
        return True
    except:
        return False


# 7提供用户提问过的问题调用函数,包含问题标题,
def question(name):
    # name为提供用户名,
    sql = '''select title from userask 
    where user='%s';''' % name
    cs.execute(sql)
    n = cs.fetchall()
    l = []
    for i in n:
        title = i[0]
        cs.execute('''select uid,number from userask 
            where user='%s' and title='%s';''' % (name, title))
        uid, number = cs.fetchone()
        l1 = str(uid)+'*.*'+title+'*.*'+str(number)
        l.append(l1)
    return l


# 8提供单个显示问题调用函数,包含用户名,问题详情,
# 所有答案(包含回答者用户名)
def single(uid):
    sql = '''select user,question from 
    userask where uid=%d;''' % uid
    cs.execute(sql)
    a = cs.fetchone()  # 问题的用户名,问题详情
    sql = '''select answers,solutions from solution 
    where sid='%d' limit 10;''' % uid
    cs.execute(sql)
    b = cs.fetchall()  # 问题的所有答案
    return (a, b)


# 9答案回复互动函数
# def revert(aid,rev):
#     try:
#         cs.execute('''select solutions from
#             solution where aid=%d;''' % aid)
#         a=cs.fetchone()
#         ss=a[0]+'#.#'+rev
#         cs.execute('''update solution set
#             solutions='%s';''' % ss)
#         return True
#     except:
#         return False
