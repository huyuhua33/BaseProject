# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:00:44 2019
@author: Jason
"""
import sub.login
import sub.login2
import sub.timer
import sub.register
import sub.transaction
import sub.sitleft as sit
import random
import sqlite3
#import getpass
import msvcrt,sys
import datetime
import time
import sub.grade_assiment as gsi
import threading
import sub.mail as mailing
import json
import requests
#
enable=False

"""
    以下副程式接用平行處理
"""
#平行處理停止用(True會關閉)
stop_thread=False
thread_in_time=False
thread_over_time=False
    
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
        #if stop_thread or not(enable):
        #    break
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
#            print('選課代號：', i, " with ", left ,"left.")
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
    #設定停止時間點
    start_time=datetime.datetime.now()
    stop_time=start_time+datetime.timedelta(minutes=5)
    while(True):
        if(thread_in_time==True):
            #已認證成功
            break
        if(stop_time<=datetime.datetime.now()):
            #時間到了
            thread_over_time=True
            print("驗證超時")
            print("重新登入")
            print("輸入任意健繼續")
            break
"""
    以下副程式協助登入功能，沒平行處理
"""
#網路上查的，使用cmd時密碼屏蔽用
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

#第一次創建sql用
def creat_SQllite():
    #建立資料庫
    sql = '''Create table users( class_name text, class_id int, account text, email text, push_account text)'''
    conn = sqlite3.connect("class_table.db")  #連結資料庫
    conn.execute(sql)  #執行指令
    conn.close()  #關閉資料庫
    conn = sqlite3.connect("tmp.db")
    conn.execute(sql)
    conn.close()

#第一次執行請將creat功能打開
#creat_SQllite()
while(True): 
    print("NID帳號: ")
    nid_address=input("")
    print("")
    print("NID密碼: ")
    nid_password=pwd_input() #cmd下遮蔽輸入
    print("")
    print("")
    #計時開始，若登入用時超過10分鐘，結束登入功能時，再登入學校系統
    time_check=datetime.datetime.now()
    reset_time=time_check+datetime.timedelta(minutes=10)
    #確認帳密是否正確
    status=sub.search.c_check(nid_address, nid_password,'108','1')
    if(status==False):
        print("帳密error")
        print("重新登入")
        continue
    email=input("請輸入email: ")
    make_sure=random.randint(10000, 99999)  #random認證碼
    sub.mail.mail(email,0,make_sure,0)   #寄email以認證email的真實性
    print("已寄出驗證碼\n")
    threading.Thread(target=check_timeout).start() #超過五分鐘未認證，驗證超時，
    email_sure=input("請輸入驗證碼: ")
    if (thread_over_time==True):
        continue
    elif (int(email_sure)==make_sure) :  #認證碼比對
        thread_in_time=True
        print("驗證成功")
        break
    else:
        print("驗證失敗")
        print("重新登入")
        continue
    if(datetime.datetime.now()>reset_time):
         sub.login.loging(nid_address, nid_password) #超過10分鐘，重新登入
while(True):
    #功能選單
    c = '''
    功能選擇: 
        1.登出
        2.交易平台
        3.課餘通知
        4.推薦課程查詢
        5.開始選課
        
    請選擇功能: '''
    choice = input(c)
    if choice == '1':
        break
    elif choice == '2':
        sub.transaction.transaction(nid_address,nid_password,email)
    elif choice=='3' :
        ID = input("請輸入查詢位置之選課代碼:")
        send(email, ID)
    elif choice == '4':
        gsi.MyfcuLogin(nid_address,nid_password)
    elif choice == '5':
        if(enable==False):
            enable, html = sub.login2.login_start(nid_address,nid_password)  
            threading.Thread(target=timeUpdate, args=(enable, html)).start()
            threading.Thread(target=c_main, args=(enable, html)).start()
        else:
            print("已經登入選課系統了")
    else:
        print("Input error, please try again")
stop_thread=True #停止平行處理
del nid_address, nid_password, email #刪掉使用者個資


