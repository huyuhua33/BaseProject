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
    �H�U�Ƶ{�����Υ���B�z
"""
#����B�z�����(True�|����)
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
                print("�w�g�g�L", int(now - t), "��")
                time.sleep(1)
        else:
            break
def c_main(enable, registerhtml):#y ����Ǧ~ sms 1 or 2
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
            left = sub.search.c_left_for_register(r)
            print('��ҥN���G', i, " with ", left ,"left.")
            if left > 0 :
               sub.register.register(enable, registerhtml, i)
def send(email, ID):
    r = mailing.mail(email, 1, 0, ID)
    while (r == -1):
        print("��J���~")
        ID = input("�п�J�d�ߦ�m����ҥN�X:")
        r = mailing.mail(email, 1, 0, ID)
    return 0

def check_timeout():
    #�]�w����ɶ��I
    start_time=datetime.datetime.now()
    stop_time=start_time+datetime.timedelta(minutes=5)
    while(True):
        if(thread_in_time==True):
            #�w�{�Ҧ��\
            break
        if(stop_time<=datetime.datetime.now()):
            #�ɶ���F
            thread_over_time=True
            print("���ҶW��")
            print("���s�n�J")
            print("��J���N���~��")
            break
"""
    �H�U�Ƶ{����U�n�J�\��A�S����B�z
"""
#�����W�d���A�ϥ�cmd�ɱK�X�̽���
def pwd_input():    
    chars = []   
    while True:  
        try:  
            newChar = msvcrt.getch().decode(encoding="utf-8")  
        except:  
            return input("�A�ܥi�ण�O�bcmd�R�O��U�B��A�K�X��J�N��������:")  
        if newChar in "\r\n": # �p�G�O����A�h��J����               
             break   
        elif newChar == "\b": # �p�G�O�h��A�h�R���K�X�����@��åB�R���@�ӬP��   
             if chars:    
                 del chars[-1]   
                 msvcrt.putch("\b".encode(encoding="utf-8")) # ���Ц^�h�@��  
                 msvcrt.putch( " ".encode(encoding="utf-8")) # ��X�@�ӪŮ��л\��Ӫ��P��  
                 msvcrt.putch("\b".encode(encoding="utf-8")) # ���Ц^�h�@��ǳƱ����s����J                   
        else:  
            chars.append(newChar)  
            msvcrt.putch("*".encode(encoding="utf-8")) # ��ܬ��P��  
    return ("".join(chars) )  

#�Ĥ@���Ы�sql��
def creat_SQllite():
    #�إ߸�Ʈw
    sql = '''Create table users( class_name text, class_id int, account text, email text, push_account text)'''
    conn = sqlite3.connect("class_table.db")  #�s����Ʈw
    conn.execute(sql)  #������O
    conn.close()  #������Ʈw
    conn = sqlite3.connect("tmp.db")
    conn.execute(sql)
    conn.close()

#�Ĥ@������бNcreat�\�ॴ�}
#creat_SQllite()
while(True): 
    print("NID�b��: ")
    nid_address=input("")
    print("")
    print("NID�K�X: ")
    nid_password=pwd_input() #cmd�U�B����J
    print("")
    print("")
    #�p�ɶ}�l�A�Y�n�J�ήɶW�L10�����A�����n�J�\��ɡA�A�n�J�Ǯըt��
    time_check=datetime.datetime.now()
    reset_time=time_check+datetime.timedelta(minutes=10)
    #�T�{�b�K�O�_���T
    status=sub.search.c_check(nid_address, nid_password,'108','1')
    if(status==False):
        print("�b�Kerror")
        print("���s�n�J")
        continue
    email=input("�п�Jemail: ")
    make_sure=random.randint(10000, 99999)  #random�{�ҽX
    sub.mail.mail(email,0,make_sure,0)   #�Hemail�H�{��email���u���
    print("�w�H�X���ҽX\n")
    threading.Thread(target=check_timeout).start() #�W�L���������{�ҡA���ҶW�ɡA
    email_sure=input("�п�J���ҽX: ")
    if (thread_over_time==True):
        continue
    elif (int(email_sure)==make_sure) :  #�{�ҽX���
        thread_in_time=True
        print("���Ҧ��\")
        break
    else:
        print("���ҥ���")
        print("���s�n�J")
        continue
    if(datetime.datetime.now()>reset_time):
         sub.login.loging(nid_address, nid_password) #�W�L10�����A���s�n�J
while(True):
    #�\����
    c = '''
    �\����: 
        1.�n�X
        2.������x
        3.�Ҿl�q��
        4.���˽ҵ{�d��
        5.�}�l���
        
    �п�ܥ\��: '''
    choice = input(c)
    if choice == '1':
        break
    elif choice == '2':
        sub.transaction.transaction(nid_address,nid_password,email)
    elif choice=='3' :
        ID = input("�п�J�d�ߦ�m����ҥN�X:")
        send(email, ID)
    elif choice == '4':
        gsi.MyfcuLogin(nid_address,nid_password)
    elif choice == '5':
        if(enable==False):
            enable, html = sub.login2.login_start(nid_address,nid_password)  
            threading.Thread(target=timeUpdate, args=(enable, html)).start()
            threading.Thread(target=c_main, args=(enable, html)).start()
        else:
            print("�w�g�n�J��Ҩt�ΤF")
    else:
        print("Input error, please try again")
stop_thread=True #�����B�z
del nid_address, nid_password, email #�R���ϥΪ̭Ӹ�