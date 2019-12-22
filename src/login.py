import requests
from bs4 import BeautifulSoup
import sub.search as search

Session_requests=requests.Session()
def loging(url,NID,Password):# loging
    r = Session_requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    VIEWSTATE = soup.find(id="__VIEWSTATE")["value"]
    VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")["value"]
    EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")["value"]

    # get verificationCode
    url_vcode = 'https://course.fcu.edu.tw/validateCode.aspx'
    r = Session_requests.get(url_vcode)
    v_code = r.headers['Set-Cookie'][slice(-12, -8)]
    # post to loging.aspx
    data = {
        '__EVENTTARGET': 'ctl00$Login1$LoginButton',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': VIEWSTATE,
        '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
        '__EVENTVALIDATION': EVENTVALIDATION,
        'ctl00$Login1$RadioButtonList1': 'zh-tw',
        'ctl00$Login1$UserName': NID,
        'ctl00$Login1$Password': Password,
        'ctl00$Login1$vcode': v_code,
        'ctl00$temp': ''
    }
    r = Session_requests.post('https://course.fcu.edu.tw/Login.aspx', data=data)  # url=html
    return r
    # loging finish
def searching(r,ID_D):
    # goto corse searchingd
    soup = BeautifulSoup(r.text, 'html.parser')
    VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
    VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
    EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']

    data = {
        'ctl00_ToolkitScriptManager1_HiddenField': '',
        'ctl00_MainContent_TabContainer1_ClientState': '{"ActiveTabIndex":2,"TabState":[true,true,true]}',
        '__EVENTTARGET': 'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$btnSearchOther',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': VIEWSTATE,
        '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
        '__EVENTVALIDATION': EVENTVALIDATION,
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDegree': '1',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDept': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlUnit': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlClass': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlWeek': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlPeriod': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbCourseName': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbTeacherName': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects': '1',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$cbShowSelected': 'on',
        'ctl00$MainContent$TabContainer1$tabSelected$tbSubID': ID_D,
        'ctl00$MainContent$TabContainer1$tabSelected$btnGetSub': '查詢',
        'ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState': 'false'
    }
    url_ADD = r.url.replace('.tw/?guid=', '.tw/AddWithdraw.aspx?guid=')
    r = Session_requests.post(url_ADD, data=data)
    return r
def choising(r):
    soup = BeautifulSoup(r.text, 'html.parser')

    data = {
        'ctl00_ToolkitScriptManager1_HiddenField': '',
        'ctl00_MainContent_TabContainer1_ClientState': '{"ActiveTabIndex":2,"TabState":[true,true,true]}',
        '__EVENTTARGET': 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd',
        '__EVENTARGUMENT': 'addCourse$0',
        '__LASTFOCUS': '',
        '__VIEWSTATE': soup.find(id="__VIEWSTATE")["value"],
        '__VIEWSTATEGENERATOR': soup.find(id="__VIEWSTATEGENERATOR")["value"],
        '__EVENTVALIDATION': soup.find(id="__EVENTVALIDATION")["value"],
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDegree': '1',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDept': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlUnit': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlClass': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlWeek': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlPeriod': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbCourseName': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbTeacherName': '',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects': '1',
        'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$cbShowSelected': 'on'
    }
    r = Session_requests.post(r.url, data=data)
    return r
def loging_check(r):
    w = r.text.find("錯誤")
    if w == -1:
        return True
    else:
        return False






'''

url='https://course.fcu.edu.tw/'
url_vcode='https://course.fcu.edu.tw/validateCode.aspx'


ID_D=input("please input four num course ID:")
left=search.m_left_get(ID_D)
if left<0:
    message="No space for you"
else:
    message="seat left:"+str(left)
print(message)

# if cannot loging
# try
r=loging(url)
r=searching(r)
r=choising(r)

soup=BeautifulSoup(r.text, 'html.parser')
susses=soup.find_all(string="登記成功")

try:
    if susses[0]=='登記成功':
        print('登記成功')
        sys.exit()
except:
    print('fail')
'''



