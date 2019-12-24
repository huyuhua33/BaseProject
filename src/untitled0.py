# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 11:01:24 2019

@author: d0857
"""
from selenium import webdriver
import time
import random

socialList=['國際關係','地方自治','戀愛心理學','公民社會的政策參與','智慧財產之保護與實務','心理學整合與發展','教育的理論與實踐','經濟與生活','管理面面觀','生涯規劃']
peopleList=['人生哲學','人造環境欣賞','中國文物欣賞','佛家思想','詩詞欣賞','希臘羅馬神話故事與西洋藝術','中國文化遺產及其藝術','世界音樂文化','日本歷史與文化','文學與生活']
natorlList=['衛星科技應用','醫學與人生','化粧品科學與生活時尚','性別與心理衛生,材料與生活','智慧城市無所不在的監測系統','智慧城市實務分析','環境教育','音樂、語言與大腦','模擬亞太經合會']

IECSmust=random.randint(0,63)
IECSchoose=random.randint(0,28)
notIECSchoose=random.randint(0,9)
social=random.randint(0,0)
people=random.randint(0,10)
natrol=random.randint(0,10)
total=social+people+natrol
TorF=0
while (TorF==0):
    print("請輸入帳號密碼")
    username=input("帳號:")
    userpassword=input("密碼:")
    browser = webdriver.Chrome()
    browser.get("https://myfcu.fcu.edu.tw/main/infomyfculogin.aspx")
    browser.find_elements_by_class_name("barbtn")[1].click()
    browser.find_element_by_id("txtUserName").send_keys(username)
    browser.find_element_by_id("txtPassword").send_keys(userpassword)
    browser.find_element_by_id("OKButton").click()
    time.sleep(2)
    try:
        browser.find_element_by_id("FailureText")
        print("帳號或密碼有誤\n")
        browser.close()
        TorF=0
    except:
        browser.close()
        print("登入成功")
        TorF=1
print("院系必修:      63 已修得學分:",IECSmust)
if (IECSmust<63):
    print("繼續努力讀書和記得重修喔")
elif (IECSmust==63):
    print("你已經修好修滿了")
print("--------------------")
print("本系專業選修:  28 已修得學分:",IECSchoose)
if (IECSchoose<28):
    print("繼續努力讀書喔")
elif (IECSchoose==28):
    print("你已經修好修滿了")
print("--------------------")
print("非本系專業選修: 9 已修得學分:",notIECSchoose)
if (notIECSchoose<9):
    print("繼續努力讀書喔")
elif (notIECSchoose==9):
    print("你已經修好修滿了")
print("--------------------")
print("通識社會:       2 已修得學分:",social)
if (social<2):
    print("推薦課程:",socialList[random.randint(0,3)],socialList[random.randint(4,7)],socialList[random.randint(8,9)])
elif (social==2):
    print("你已經修好修滿了")
print("--------------------")
print("通識人文:       2 已修得學分:",people)
if (people<2):
    print("推薦課程:",peopleList[random.randint(0,3)],peopleList[random.randint(4,7)],peopleList[random.randint(8,9)])
elif (people==2):
    print("你已經修好修滿了")
print("--------------------")
print("通識自然:       2 已修得學分:",natrol)
if (natrol<2):
    print("推薦課程:",natorlList[random.randint(0,3)],natorlList[random.randint(4,7)],natorlList[random.randint(8,9)])
elif (natrol==2):
    print("你已經修好修滿了")
print("--------------------")
print("---通識合計---:12 已修得學分:",total)
if (total<12):
    print("推薦課程:",socialList[random.randint(0,9)],peopleList[random.randint(0,9)],natorlList[random.randint(0,9)])
elif (total==12):
    print("你已經修好修滿了")
print("--------------------")
