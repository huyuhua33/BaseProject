# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:00:44 2019
@author: Jason
"""
"""
from tkinter import *
def pik_class():
    print("test")
    lab2 = Label(window)
    lab2.pack()
def pull_class():
    print("test1")
def look_class():
    print("test2")    
window = Tk() 
window.title("測試")
window.geometry("150x150")
window.maxsize(150, 150)
window.minsize(150, 150)
lab1 = Label(window)
bun1 = Button(window, text="選課", command=pik_class)
bun2 = Button(window, text="退課", command=pull_class)
bun3 = Button(window, text="查看課表", command=look_class)
lab1.pack()
bun1.pack()
bun2.pack()
bun3.pack()
window.mainloop()
"""
import random
import sqlite3
import sub.mail
import sub.login
import getpass
import msvcrt,sys
import sub.sitleft as sit
import datetime
import time
"""
start_time=datetime.datetime.now()
stop_time=start_time+datetime.timedelta(minutes=5)
while (stop_time>datetime.datetime.now()):
    print(stop_time-datetime.datetime.now())
"""
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
    sql = '''Create table users( class_name text, class_id int, account text, email text)'''
    conn = sqlite3.connect("class_table.db")
    conn.execute(sql)
    conn.close()
    conn = sqlite3.connect("tmp.db")
    conn.execute(sql)
    conn.close()
def input_SQlite( SQL_name ,class_name, class_number, account , email):
    conn = sqlite3.connect(SQL_name)
    data=(class_name, class_number, account, email);
    sql='''insert into users values(?, ?, ?, ?)'''
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
    sql='''insert into users values(?, ?, ?, ?)'''
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
def transaction(nid_address, nid_password, email):  
    while(True):
        print("1.選課")
        print("2.退課")
        print("3.刪除交易平台上記錄")
        print("4.刪除對方已釋出之記錄")
        print("5.查看交易平台")
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
            class_name=input("甚麼課?")
            class_id=int(input("課程代碼: "))
            """
            檢查是否有這堂課
            """
            if(True):
                input_SQlite("class_table.db", class_name, class_id, "0", email)
                print("課成已加入交易平台")
        elif(choice=="3"):
            class_id=int(input("課程代碼: "))
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
            conn = sqlite3.connect("class_table.db")
            table= conn.execute("SELECT * from users")
            table_tumple=table.fetchall()
            for data in table_tumple:
                print(data)
                conn.close
        w=input("是否繼續(1.繼續): ")
        if(w!="1"):
            break
#creat_SQllite()

myfcu="https://myfcu.fcu.edu.tw/main/infomyfculogin.aspx"

while(True):
    nid_address=input("NID帳號: ")
    print("NID密碼: ")
    nid_password=pwd_input()
    print("")
    log=sub.login.loging(nid_address, nid_password)
    #print(log.text)
    status= sub.login.loging_check(log)
    if(status==False):
        print("帳密error")
        print("重新登入")
        continue
    email=input("請輸入email: ")
    make_sure=random.randint(10000, 99999)
    sub.mail.mail(email,0,make_sure,0,'0','0')
    print("已寄出驗證碼\n")
    start_time=datetime.datetime.now()
    stop_time=start_time+datetime.timedelta(minutes=5)
    while (stop_time>datetime.datetime.now()):
        print(stop_time-datetime.datetime.now())
        email_sure=int(input("請輸入驗證碼: "))
        if (email_sure==make_sure) :
            print("驗證成功")
            with open("login.txt", "w") as login:
                login.write(nid_address + ", " + nid_password + ", " + email);
                break
        else:
            print("驗證失敗")
            print("重新登入")
            break
    if(stop_time<=datetime.datetime.now()):
        print("驗證超時")
        print("重新登入")
    else :
        break
c = '''
    功能選擇: 
        2.交易平台
        3.課餘通知
    '''
choice = input(c)
if choice == 1:
    pass
elif choice == 2:
    transaction(nid_address,nid_password,email)
elif choice==3 :
    sit.send(email)
del nid_address, nid_password, email


