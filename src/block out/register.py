import requests
from bs4 import BeautifulSoup
import ctypes

session = requests.session()
courseIDs = []


def regist(registHtml, courseID=0000):
    # search the course for register
    soup = BeautifulSoup(registHtml.text, 'html.parser')
    data = {'ctl00_ToolkitScriptManager1_HiddenField': '',
            'ctl00_MainContent_TabContainer1_ClientState': '{"ActiveTabIndex":2,"TabState":[true,true,true]}',
            '__EVENTTARGET': 'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$btnSearchOther',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': soup.find(id='__VIEWSTATE')['value'],
            '__VIEWSTATEGENERATOR': soup.find(id='__VIEWSTATEGENERATOR')['value'],
            '__EVENTVALIDATION': soup.find(id='__EVENTVALIDATION')['value'],
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
            'ctl00$MainContent$TabContainer1$tabSelected$tbSubID': courseID,
            'ctl00$MainContent$TabContainer1$tabSelected$btnGetSub': '查詢',
            'ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState': 'false'}

    # url is changed
    new_url = registHtml.url[0:registHtml.url.find('?guid')] + 'AddWithdraw.aspx' + registHtml.url[registHtml.url.find('?guid'):]
    new_Html = session.post(new_url, data=data)

    # re-get the floating value
    # register it
    soup = BeautifulSoup(new_Html.text, 'html.parser')
    courseIDs = soup.select('td.gvAddWithdrawCellOne').text
    data = {'ctl00_ToolkitScriptManager1_HiddenField': '',
            'ctl00_MainContent_TabContainer1_ClientState': '{"ActiveTabIndex":2,"TabState":[true,true,true]}',
            '__EVENTTARGET': 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd',
            '__EVENTARGUMENT': 'addCourse$0',
            '__LASTFOCUS': '',
            '__VIEWSTATE': soup.find(id='__VIEWSTATE')['value'],
            '__VIEWSTATEGENERATOR': soup.find(id='__VIEWSTATEGENERATOR')['value'],
            '__EVENTVALIDATION': soup.find(id='__EVENTVALIDATION')['value'],
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
    result = session.post(new_Html.url, data=data)

    # analysis the result of post, if it's successful, remove this ID ,or go on
    result = BeautifulSoup(result.text, 'html.parser')
    status = result.select('.msg.B1')
    if status[0].text.find('成功') != -1:
        courseIDs.remove(courseID)
        ctypes.windll.user32.MessageBoxW(0, str(courseID)+'加選成功', 'success', 0)

    return new_Html
