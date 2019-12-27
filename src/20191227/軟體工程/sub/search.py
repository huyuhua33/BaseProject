import requests
import json

Session_requests=requests.Session()
header = {'Content-Type': 'application/json'}
def c_main(s_code,y,sms):#y 民國學年 sms 1 or 2
    url='https://coursesearch03.fcu.edu.tw/Service/Search.asmx/GetType2Result'
    Request_Payload={
        "baseOptions":{"lang":"cht","year":y,"sms":sms},
        "typeOptions":{"code":{"enabled":True,"value":s_code},
                       "weekPeriod":{"enabled":False,"week":"*","period":"*"},
                       "course":{"enabled":False,"value":""},
                       "teacher":{"enabled":False,"value":""},
                       "useEnglish":{"enabled":False},
                       "specificSubject":{"enabled":False,"value":"1"}
                       }
    }
    r=Session_requests.post(url,headers=header,data=json.dumps(Request_Payload))
    return r

def c_name(r):
    string=r.json()['d']
    name=string.find('sub_name')
    n_right=string.find('"',name+len('"sub_name":'))
    n_left=string.find('"',name)
    return string[n_left+3:n_right]
def c_left(r):
    #print(r.text)
    #print(r)
    Left = r.json()['d'].find('scr_acptcnt')
    Max = r.json()['d'].find('scr_precnt')
    m_Left = int(r.json()['d'][Left + 13:Left + 15])
    m_Max = int(r.json()['d'][Max + 12:Max + 14])
    left = m_Max - m_Left
    if left <= 0:
        return 0
    else:
        return left
def c_check(NID,PW,year,sms):#y 民國學年 sms 1 or 2
    url='https://coursesearch03.fcu.edu.tw/Service/Auth.asmx/login'
    Request_Payload={"id":NID,"password":PW,"baseOptions":{"lang":"cht","year":year,"sms":sms}}
    r=Session_requests.post(url,headers=header,data=json.dumps(Request_Payload))
    ch = -1
    ch = r.text.find("\"status\\\":0")
    if ch is not -1 :
        return True
    else:
        return False    


