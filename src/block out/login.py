import requests
from bs4 import BeautifulSoup
import ctypes

session = requests.session()

# data of user
userName = ''
password = ''


def login():
    userName = input('NID account number：')
    password = input('NID password：')

    # url of course and certification
    url = 'https://course.fcu.edu.tw/'
    certification_url = 'https://course.fcu.edu.tw/validateCode.aspx'

    # get course code and certification number
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    viewState = soup.find(id='__VIEWSTATE')['value']
    viewStateGenerator = soup.find(id='__VIEWSTATEGENERATOR')['value']
    eventValidation = soup.find(id='__EVENTVALIDATION')['value']

    session.get(certification_url)
    vcode = session.cookies.get_dict()['CheckCode']

    # prepare data to post to login
    data = {'__EVENTTARGET': 'ctl00$Login1$LoginButton',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewState,
            '__VIEWSTATEGENERATOR': viewStateGenerator,
            '__EVENTVALIDATION': eventValidation,
            'ctl00$Login1$RadioButtonList1': 'zh-tw',
            'ctl00$Login1$UserName': userName,
            'ctl00$Login1$Password': password,
            'ctl00$Login1$vcode': vcode,
            'ctl00$temp': ''}

    html = session.post(url, data=data)

    return html


def login_start():

    html = login()

    # input error
    if html.text.find('錯誤') != -1:
        ctypes.windll.user32.MessageBoxW(0, "帳號或密碼錯誤", 'Error', 0)
        return -1, ''

    # the time is not allowed
    elif html.text.find('目前不是開放時間') != -1:
        ctypes.windll.user32.MessageBoxW(0, '目前不是開放時間', 'Error', 0)
        return -1, ''

    else:
        ctypes.windll.user32.MessageBoxW(0, '登入成功', 'Success', 0)
        return 0, html
