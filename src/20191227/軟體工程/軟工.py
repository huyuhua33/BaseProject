# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:00:44 2019
@author: Jason
"""
import sub.login
import sub.login2
import sub.timer
import sub.register
import sub.register
import random
import sqlite3
import getpass
import msvcrt,sys
import sub.sitleft as sit
import datetime
import time
import sub.grade_assiment as gsi
import threading
import sub.mail as mailing
import json
import requests
"""
start_time=datetime.datetime.now()
stop_time=start_time+datetime.timedelta(minutes=5)
while (stop_time>datetime.datetime.now()):
    print(stop_time-datetime.datetime.now())
"""
stop_thread=False
thread_in_time=False
thread_over_time=False
#網路上的
def pwd_input():    
    chars = []   
    while True:  
        try:  
            newChar = msvcrt.getch().decode(encoding="utf-8")  
        except:  
            return input("你很可能不是在cmd命令行下運行，密碼輸入將不能隱藏:")  
        if newChar in "\r\n": # 如果是換行，則輸入結束               
             break   
        elif newChar == "\b": # 如果是退格，則刪除密碼末尾一位並且刪除一個星號   
             if chars:    
                 del chars[-1]   
                 msvcrt.putch("\b".encode(encoding="utf-8")) # 光標回退一格  
                 msvcrt.putch( " ".encode(encoding="utf-8")) # 輸出一個空格覆蓋原來的星號  
                 msvcrt.putch("\b".encode(encoding="utf-8")) # 光標回退一格準備接受新的輸入                   
        else:  
            chars.append(newChar)  
            msvcrt.putch("*".encode(encoding="utf-8")) # 顯示為星號  
    return ("".join(chars) )  

#第一次創建用
def creat_SQllite():
    sql = '''Create table users( class_name text, class_id int, account text, email text, push_account text)'''
    conn = sqlite3.connect("class_table.db")
    conn.execute(sql)
    conn.close()
    conn = sqlite3.connect("tmp.db")
    conn.execute(sql)
    conn.close()
def input_SQlite( SQL_name ,class_name, class_number, account , email, push_account):
    conn = sqlite3.connect(SQL_name)
    data=(class_name, class_number, account, email, push_account);
    sql='''insert into users values(?, ?, ?, ?, ?)'''
    conn.execute(sql, data)
    conn.commit()
    conn.close()
def delete_SQlite(SQL_name, class_id):
    conn = sqlite3.connect(SQL_name)
    sql='''DELETE from users where class_id = ''' + str(class_id)
    conn.execute(sql)
    conn.commit()
    conn.close()
    conn.close()
def update_SQlite(SQL_name, account, class_id):
    conn = sqlite3.connect(SQL_name)
    sql="UPDATE users set account = '" + account + "' where class_id =" + str(class_id)
    conn.execute(sql)
    conn.commit()
    conn.close()
def sand(SQL_name, class_id):
    conn = sqlite3.connect(SQL_name)
    table= conn.execute("SELECT * from users")
    table_tumple=table.fetchall()
    for data in table_tumple:
        if(data[1]==class_id):
            tmp="有人需要您的"+data[0]+"課(" + str(data[1]) + ")"
            tmp=tmp+"，請盡快釋放此課程並在交易平台上刪除"
            sub.mail.mail(data[3],0,tmp,0)
            conn.close()
            return 1
    conn.close()
    return 0
def copy_SQlite(SQL_name1, SQL_name2, class_id):
    conn = sqlite3.connect(SQL_name1)
    conn2 = sqlite3.connect(SQL_name2)
    sql='''insert into users values(?, ?, ?, ?, ?)'''
    table= conn.execute("SELECT * from users")
    table_tumple=table.fetchall()
    for data in table_tumple:
        if(data[1]==class_id):
            print("交換中")
            conn2.execute(sql, data)
            conn2.commit()
            conn2.close()
            conn.close()
            return 1
    conn2.close()
    conn.close()
    return 0
def sure(SQL_name, class_id):
    conn = sqlite3.connect(SQL_name)
    table= conn.execute("SELECT * from users")
    table_tumple=table.fetchall()
    for data in table_tumple:
        if(data[1]==class_id):
            make_sure=random.randint(10000, 99999)
            sub.mail.mail(data[3],0,make_sure,0)
            email_sure=int(input("請輸入驗證碼:"));
            if (email_sure==make_sure) :
                conn.close()
                return 1
    conn.close()
    return 0
def makesure_your_commit(SQL_name, pull_address):
    conn = sqlite3.connect(SQL_name)
    table= conn.execute("SELECT * from users")
    table_tumple=table.fetchall()
    print("您的待確認課程:")
    for data in table_tumple:
        if(data[4]==pull_address and data[2]!='0'):
            print(data)
    conn.close()
    return 0
def transaction(nid_address, nid_password, email):  
    while(True):
        print("1.選課")
        print("2.退課")
        print("3.交易確認")
        print("4.刪除對方已釋出之記錄")
        print("5.刪除交易平台上記錄")
        print("6.查看交易平台")
        print("7.登出")
        print("\n對方已釋出的課: ")
        conn = sqlite3.connect("tmp.db")
        table= conn.execute("SELECT * from users")
        table_tumple=table.fetchall()
        for data in table_tumple:
            if(data[2]==nid_address):
                print(data)
        print("-----底部-----")
    
        choice= input("選擇功能(數字): ")
        if(choice=="1"):
            class_name=input("甚麼課?")
            class_id=int(input("課程代碼: "))
            find=sand("class_table.db", class_id)
            if(find==1):
                print("已通知使用者")
                update_SQlite("class_table.db", nid_address , class_id)
            elif(find==0):
                print("交易平台尚無此課") 
        elif(choice=="2"):
            while(True):
                class_name=input("甚麼課?")
                class_id=int(input("課程代碼: "))
                class_check=sub.mail.class_check(class_id)
                if(class_check==0):
                    break
                else:
                    print("查無此課程")
            if(True):
                input_SQlite("class_table.db", class_name, class_id, "0", email, nid_address)
                print("課程已加入交易平台")
        elif(choice=="3"):
            makesure_your_commit("class_table.db", nid_address)
            class_id=int(input("確認要釋放的課程代碼: "))
            status=sure("class_table.db", class_id)
            if(status==1):
                copy_SQlite("class_table.db", "tmp.db", class_id)
                delete_SQlite("class_table.db", class_id)
            else:
                print("驗證失敗")
        elif(choice=="4"):
            class_id=int(input("課程代碼: "))
            delete_SQlite("tmp.db", class_id)
        elif(choice=="5"):
            class_id=int(input("課程代碼: "))
            status=sure("class_table.db", class_id)
            if(status==1):
                copy_SQlite("class_table.db", "tmp.db", class_id)
                delete_SQlite("class_table.db", class_id)
            else:
                print("驗證失敗")
        elif(choice=="6"):
            conn = sqlite3.connect("class_table.db")
            table= conn.execute("SELECT * from users")
            table_tumple=table.fetchall()
            for data in table_tumple:
                print(data)
            conn.close
        elif(choice=="7"):
            print("")
        else:
            print("查無此功能")
        w=input("是否繼續(1.繼續): ")
        if(w!="1"):
            break
        
def timeUpdate(enable, registerhtml):
    t = time.time()
    while True:
        if stop_thread:
            break
        if enable:
            now = time.time()
            if (now - t) >= 30:
                sub.register.register(enable, registerhtml)
                t = time.time()
            elif int(now - t) % 10 == 0:
                print("已經經過", int(now - t), "秒")
                time.sleep(1)
        else:
            break
def c_main(enable, registerhtml):#y 民國學年 sms 1 or 2
    Session_requests=requests.Session()
    header = {'Content-Type': 'application/json'}
    while True:
        if stop_thread or not(enable):
            break
        for i in sub.register.courseIDs:
            url='https://coursesearch03.fcu.edu.tw/Service/Search.asmx/GetType2Result'
            Request_Payload={
                "baseOptions":{"lang":"cht","year":"108","sms":"2"},
                "typeOptions":{"code":{"enabled":True,"value":str(i)},
                               "weekPeriod":{"enabled":False,"week":"*","period":"*"},
                               "course":{"enabled":False,"value":""},
                               "teacher":{"enabled":False,"value":""},
                               "useEnglish":{"enabled":False},
                               "specificSubject":{"enabled":False,"value":"1"}
                               }
            }
            r=Session_requests.post(url,headers=header,data=json.dumps(Request_Payload))
            left = sub.search.c_left(r)
            print('選課代號：', i, " with ", left ,"left.")
            if left > 0 :
                sub.register.register(enable, registerhtml, i)
def send(email, ID):
    r = mailing.mail(email, 1, 0, ID)
    while (r == -1):
        print("輸入錯誤")
        ID = input("請輸入查詢位置之選課代碼:")
        r = mailing.mail(email, 1, 0, ID)
    return 0
def check_timeout():
    start_time=datetime.datetime.now()
    stop_time=start_time+datetime.timedelta(minutes=5)
    while(True):
        if(thread_in_time==True):
            break
        if(stop_time<=datetime.datetime.now()):
            thread_over_time=True
            print("驗證超時")
            print("重新登入")
            print("輸入任意健繼續")
            break
#creat_SQllite()
while(True): 
    nid_address=input("NID帳號: ")
    print("NID密碼: ")
    nid_password=pwd_input()
    print("")
    time_check=datetime.datetime.now()
    reset_time=time_check+datetime.timedelta(minutes=10)
    status=sub.search.c_check(nid_address, nid_password,'108','1')
    if(status==False):
        print("帳密error")
        print("重新登入")
        continue
    email=input("請輸入email: ")
    make_sure=random.randint(10000, 99999)
    sub.mail.mail(email,0,make_sure,0)
    print(make_sure)
    print("已寄出驗證碼\n")
    #start_time=datetime.datetime.now()
    #stop_time=start_time+datetime.timedelta(minutes=5)
    threading.Thread(target=check_timeout).start()
    email_sure=input("請輸入驗證碼: ")
    if (thread_over_time==True):
        continue
    elif (int(email_sure)==make_sure) :
        thread_in_time=True
        print("驗證成功")
        break
    else:
        print("驗證失敗")
        print("重新登入")
        continue
    if(datetime.datetime.now()>reset_time):
         sub.login.loging(nid_address, nid_password)

while(True):
    c = '''
    功能選擇: 
        1.登出
        2.交易平台
        3.課餘通知
        4.推薦課程查詢
        5.開始選課
    '''
    choice = input(c)
    
    if choice == '1':
        break
    elif choice == '2':
        transaction(nid_address,nid_password,email)
    elif choice=='3' :
        ID = input("請輸入查詢位置之選課代碼:")
        send(email, ID)
    elif choice == '4':
        gsi.MyfcuLogin(nid_address,nid_password)
    elif choice == '5':
        enable, html = sub.login2.login_start(nid_address,nid_password)
        threading.Thread(target=timeUpdate, args=(enable, html)).start()
        threading.Thread(target=c_main, args=(enable, html)).start()
    else:
        print("Input error, please try again")
stop_thread=True
del nid_address, nid_password, email


