import requests
import json

Session_requests=requests.Session()
header = {'Content-Type': 'application/json'}
def c_main(code):
    url='https://coursesearch03.fcu.edu.tw/Service/Search.asmx/GetType2Result'
    s_code=code
    Request_Payload={
        "baseOptions":{"lang":"cht","year":108,"sms":1},
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

    Left = r.json()['d'].find('scr_acptcnt')
    Max = r.json()['d'].find('scr_precnt')
    m_Left = int(r.json()['d'][Left + 13:Left + 15])
    m_Max = int(r.json()['d'][Max + 12:Max + 14])
    left = m_Max - m_Left
    return left