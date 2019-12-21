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
import sub.mailing as mail
import sub.main

def input_SQlite( SQL_name ,class_name, class_number, account ):
    conn = sqlite3.connect(SQL_name)
    data=(class_name, class_number, account);
    sql='''insert into users values(?, ?, ?)'''
    conn.execute(sql, data)
    conn.commit()
    conn.close()
def delete_SQlite(SQL_name, class_id):
    conn = sqlite3.connect(SQL_name)
    sql='''DELETE from users where class_id = ''' + class_id
    conn.execute(sql)
    conn.commit()
    conn.close()
def copy_SQlite(SQL_name1, SQL_name2, class_id):
    conn = sqlite3.connect(SQL_name1)
    conn2 = sqlite3.connect(SQL_name2)
    sql='''insert into users values(?, ?, ?)'''
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
        
#第一次創建用
"""
sql = '''Create table users( class_name text, class_id int, account text)'''
conn = sqlite3.connect("class_table.db")
conn.execute(sql)
conn.close()
conn = sqlite3.connect("tmp.db")
conn.execute(sql)
conn.close()
"""
#nid_address='D0713227'
#nid_password='Hu99881212123'
#email='d0713227@mail.fcu.edu.tw'

while(True):
    nid_address=input("NID帳號: ");
    nid_password=input("NID密碼: ");
    email=input("請輸入email: ");
    make_sure=random.randint(10000, 99999)

    sub.mailing.mail(email,0,make_sure,0)
    #tmp=sub.main.loging(nid_address, nid_password)
    #print(tmp.url)
    email_sure=int(input("請輸入驗證碼:"));
    if (email_sure==make_sure) :
        print("驗證成功")
        with open("login.txt", "w") as login:
            login.write(nid_address + ", " + nid_password + ", " + email);
        break
    else:
        print("驗證失敗")
        print("重新登入")
        
        
choice= input("選擇功能: ")

if(choice=="選課"):
    class_name=input("甚麼課?")
    class_id=input("課程代碼: ")
    find=copy_SQlite("class_table.db", "tmp.db", class_id)
    if(find==1):
       delete_SQlite("class_table.db",class_id)
       """
       傳email
       """
       print("已通知使用者")
    elif(find==0):
        print("交易平台尚無此課")
elif(choice=="退課"):
    class_name=input("甚麼課?")
    class_id=input("課程代碼: ")
    """
    檢查是否有這堂課
    """
    if(True):
        input_SQlite("class_table.db", class_name, class_id, nid_address)
        print("退課成功")
elif(choice=="查看課表"):
    conn = sqlite3.connect("class_table.db")
    table= conn.execute("SELECT * from users")
    table_tumple=table.fetchall()
    for data in table_tumple:
        print(data)
    conn.close    



