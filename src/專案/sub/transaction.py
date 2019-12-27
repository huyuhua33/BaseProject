# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 17:06:01 2019

@author: Jason
"""
import sqlite3
import sub.mail
import random
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
            tmp="有人需要您的"+data[0]+"課( 課程代碼" + str(data[1]) + " )"
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
            email_sure=int(input("請至email確認驗證碼: "));
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
        print("    1.選課")
        print("    2.退課")
        print("    3.交易確認")
        print("    4.刪除對方已釋出之記錄")
        print("    5.刪除交易平台上記錄")
        print("    6.查看交易平台")
        print("    7.登出")
        print("    \n對方已釋出的課: ")
        print("課程名稱   課程代碼   預訂者帳號   退課方email   退課方帳號")
        conn = sqlite3.connect("tmp.db")
        table= conn.execute("SELECT * from users")
        table_tumple=table.fetchall()
        for data in table_tumple:
            if(data[2]==nid_address):
                print(data)
        print("-----底部-----\n")
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
            class_id=int(input("要處理的課程代碼: "))
            class_change=input("是否同意換這堂課( 1.是, 2.否 ): ")
            if(class_change=='1'):
                status=sure("class_table.db", class_id)
                if(status==1):
                    copy_SQlite("class_table.db", "tmp.db", class_id)
                    delete_SQlite("class_table.db", class_id)
                else:
                    print("驗證失敗")
            elif(class_change=='2'):
                update_SQlite("class_table.db", "0", class_id)
            else:
                print("輸入錯誤")
        elif(choice=="4"):
            class_id=int(input("課程代碼: "))
            delete_SQlite("tmp.db", class_id)
            print("刪除完成")
        elif(choice=="5"):
            class_id=int(input("課程代碼: "))
            status=sure("class_table.db", class_id)
            if(status==1):
                delete_SQlite("class_table.db", class_id)
                print("刪除完成")
            else:
                print("驗證失敗")
        elif(choice=="6"):
            print("課程名稱   課程代碼   預訂者帳號   退課方email   退課方帳號")
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
        w=input("是否繼續( 1.繼續, 2.退出 ): ")
        print("")
        if(w!="1" and w!=""):
            break
        
