"""
@author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
@software: PyCharm
@file: jd_loreal_Daily.py
@time: 2023/7/14 10:14
"""

import requests ,re ,random ,json ,sys ,os ,time ,threading ,concurrent .futures #line:9:import requests, re, random, json, sys, os, time, threading, concurrent.futures
from utils .sign import *#line:10:from utils.sign import *
from fake_useragent import UserAgent #line:12:from fake_useragent import UserAgent
from jdCookie import get_cookies #line:13:from jdCookie import get_cookies
from datetime import datetime ,timedelta #line:14:from datetime import datetime,  timedelta
class Daily :#line:15:class Daily:
    def __init__ (OOO000OOOOO000O0O ):#line:16:def __init__(self):
        OOO000OOOOO000O0O .ua =UserAgent ()#line:17:self.ua = UserAgent()
        OOO000OOOOO000O0O .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:19:self.proxy = os.environ.get("TEN_proxy") if os.environ.get("TEN_proxy") else False
        OOO000OOOOO000O0O .proxies ={'http':f'{OOO000OOOOO000O0O.proxy}','https':f'{OOO000OOOOO000O0O.proxy}',}#line:23:}
        OOO000OOOOO000O0O .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else sys .exit ('❌TOKEN未设置')#line:24:self.token = os.environ.get("TEN_TOKEN") if os.environ.get("TEN_TOKEN") else sys.exit('❌TOKEN未设置')
        OOO000OOOOO000O0O .activiturl =os .environ .get ("jd_loreal_Daily")if os .environ .get ("jd_loreal_Daily")else print ('❌未获取到jd_loreal_Daily变量 程序自动退出')#line:25:self.activiturl = os.environ.get("jd_loreal_Daily") if os.environ.get("jd_loreal_Daily") else print('❌未获取到jd_loreal_Daily变量 程序自动退出')
        OOO000OOOOO000O0O .activityId =re .findall ('activityId=(\d+)',OOO000OOOOO000O0O .activiturl )[0 ]#line:26:self.activityId = re.findall('activityId=(\d+)', self.activiturl)[0]
        OOO000OOOOO000O0O .time_list =["10:00","20:00"]#line:27:self.time_list = ["10:00", "20:00"]
        OOO000OOOOO000O0O .token_activities ={}#line:28:self.token_activities = {}
        OOO000OOOOO000O0O .start =''#line:29:self.start = ''
        OOO000OOOOO000O0O .pause =False #line:30:self.pause = False
        OOO000OOOOO000O0O .verify =False #line:31:self.verify = False
    def verif (OO0OO00O0000000OO ):#line:33:def verif(self):
        try :#line:34:try:
            OO0OO00O0000000OO .verify =verify (OO0OO00O0000000OO .token )#line:35:self.verify = verify(self.token)
            if OO0OO00O0000000OO .verify !=True :#line:36:if self.verify != True:
                sys .exit ('❌授权未通过 程序自动退出！！！')#line:37:sys.exit('❌授权未通过 程序自动退出！！！')
            return OO0OO00O0000000OO .verify #line:38:return self.verify
        except Exception as O0OOO0O0OOOOOO0O0 :#line:39:except Exception as e:
            print (f'验证授权失败： {O0OOO0O0OOOOOO0O0}')#line:40:print(f'验证授权失败： {e}')
    def save_json_data (O000000OO00OO0OOO ,O0O0000O0O0000000 ,OOOOO0OO000000OO0 ):#line:41:def save_json_data(self, data, filename):
        with open (OOOOO0OO000000OO0 ,'w',encoding ='utf-8')as O000O0O00O0O0OO00 :#line:43:with open(filename, 'w', encoding='utf-8') as file:
            json .dump (O0O0000O0O0000000 ,O000O0O00O0O0OO00 ,ensure_ascii =False ,indent =4 )#line:44:json.dump(data, file, ensure_ascii=False, indent=4)
    def load_json_data (OO0O000OO000OOO00 ,OOO0OOOOOOOOO0O0O ):#line:46:def load_json_data(self, filename):
        with open (OOO0OOOOOOOOO0O0O ,'r',encoding ='utf-8')as OOOO0O0OO000O0O00 :#line:48:with open(filename, 'r', encoding='utf-8') as file:
            O00OOOO00O0OOOOO0 =json .load (OOOO0O0OO000O0O00 )#line:49:data = json.load(file)
        return O00OOOO00O0OOOOO0 #line:50:return data
    def data_timeout (OO0O0OO0OOOOOOOO0 ,O000O0O00O00O0OO0 ):#line:51:def data_timeout(self, time):
        OOO00000O00OOO0O0 =datetime .fromtimestamp (O000O0O00O00O0OO0 /1000 )#line:52:dt = datetime.fromtimestamp(time / 1000)
        O0OOOOOO00OOO0000 =OOO00000O00OOO0O0 .strftime ("%Y-%m-%d %H:%M:%S")#line:53:formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
        return O0OOOOOO00OOO0000 #line:54:return formatted_datetime
    def post_Token (OO00000000O0OO00O ,O0OOO0O000O0000OO ):#line:55:def post_Token(self, ck):
        if OO00000000O0OO00O .verify !=True :#line:56:if self.verify != True:
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:57:sys.exit('❌授权未通过 程序自动退出！！！')
        O000O0OO0OOO0O000 ='https://api.m.jd.com/client.action'#line:58:url = 'https://api.m.jd.com/client.action'
        OOO000O00O000O0O0 ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':OO00000000O0OO00O .ua .safari ,'Cookie':O0OOO0O000O0000OO ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:69:}
        OOOO0O000O0O0000O =get_sign ('isvObfuscator',{'id':'','url':'https://lzkj-isv.isvjcloud.com'})#line:70:body = get_sign('isvObfuscator', {'id': '', 'url': 'https://lzkj-isv.isvjcloud.com'})
        if OO00000000O0OO00O .proxy !=False :#line:71:if self.proxy != False:
            O0OOO00000O000O00 =requests .post (url =O000O0OO0OOO0O000 ,headers =OOO000O00O000O0O0 ,data =OOOO0O000O0O0000O ,proxies =OO00000000O0OO00O .proxies )#line:72:res = requests.post(url=url, headers=headers, data=body, proxies=self.proxies)
        else :#line:73:else:
            O0OOO00000O000O00 =requests .post (url =O000O0OO0OOO0O000 ,headers =OOO000O00O000O0O0 ,data =OOOO0O000O0O0000O )#line:74:res = requests.post(url=url, headers=headers, data=body)
        if O0OOO00000O000O00 .status_code !=200 :#line:75:if res.status_code != 200:
            sys .exit (f'❌ 获取Token失败:{O0OOO00000O000O00.status_code}, 程序将自动退出！！')#line:76:sys.exit(f'❌ 获取Token失败:{res.status_code}, 程序将自动退出！！')
        if 'token'in O0OOO00000O000O00 .json ():#line:77:if 'token' in res.json():
            OO00000000O0OO00O .token =O0OOO00000O000O00 .json ()['token']#line:79:self.token = res.json()['token']
        else :#line:80:else:
            print (O0OOO00000O000O00 .json ())#line:81:print(res.json())
    def get_Token (OOO0O0OO0OO0O0O00 ,OOO0OOOOO0O0OOO0O ,O00OO0O0OOO00OO0O ,O0O0O0000O0OO0OOO ,OOOOOO0OO00O0O000 ):#line:83:def get_Token(self, activityId,  activiturl, prizeInfoId, start_time):
        if OOO0O0OO0OO0O0O00 .verify !=True :#line:84:if self.verify != True:
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:85:sys.exit('❌授权未通过 程序自动退出！！！')
        O0O000O00OOO0OOOO ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login'#line:86:url = 'https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login'
        OO00OO00O0OOO00OO ={"status":"0","activityId":OOO0OOOOO0O0OOO0O ,"source":"01","tokenPin":OOO0O0OO0OO0O0O00 .token ,"shareUserId":""}#line:87:body = {"status": "0", "activityId": activityId, "source": "01", "tokenPin": self.token, "shareUserId": ""}
        O00O0OO000O0000O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/json;charset=UTF-8','Origin':f'https://lzkj-isv.isvjcloud.com','User-Agent':OOO0O0OO0OO0O0O00 .ua .safari ,'Connection':'keep-alive','Referer':O00OO0O0OOO00OO0O ,}#line:98:}
        if OOO0O0OO0OO0O0O00 .proxy !=False :#line:99:if self.proxy != False:
            O0O000OO0OO0OO00O =requests .post (url =O0O000O00OOO0OOOO ,headers =O00O0OO000O0000O0 ,data =json .dumps (OO00OO00O0OOO00OO ),proxies =OOO0O0OO0OO0O0O00 .proxies )#line:100:res = requests.post(url=url, headers=headers, data=json.dumps(body), proxies=self.proxies)
        else :#line:101:else:
            O0O000OO0OO0OO00O =requests .post (url =O0O000O00OOO0OOOO ,headers =O00O0OO000O0000O0 ,data =json .dumps (OO00OO00O0OOO00OO ))#line:102:res = requests.post(url=url, headers=headers, data=json.dumps(body))
        if O0O000OO0OO0OO00O .status_code !=200 :#line:103:if res.status_code != 200:
            sys .exit (f'❌ 登录失败:{O0O000OO0OO0OO00O.status_code}, 程序将自动退出！！')#line:104:sys.exit(f'❌ 登录失败:{res.status_code}, 程序将自动退出！！')
        O0OO0000OO0O000OO ={"start_time":OOOOOO0OO00O0O000 ,"activityId":OOO0OOOOO0O0OOO0O ,"prizeInfoId":O0O0O0000O0OO0OOO ,"token":O0O000OO0OO0OO00O .json ()['data']['token'],"url":O00OO0O0OOO00OO0O ,}#line:111:}
        OOO0O0OO0OO0O0O00 .token_activities [OOO0OOOOO0O0OOO0O ]=O0OO0000OO0O000OO #line:112:self.token_activities[activityId] = data_json
        return 200 ,O0O000OO0OO0OO00O .json ()['data']['token'],O0O000OO0OO0OO00O .json ()['data']['userPin']#line:113:return 200, res.json()['data']['token'], res.json()['data']['userPin']
    def post_activity (OOOOOO0OO0O0000OO ,OO0OOOO0000OO0OOO ,OOOOOO0O0OO00O000 ,O0O0OOOO0OO0O0OOO ):#line:115:def post_activity(self, token, activiturl, activityId):
        if OOOOOO0OO0O0000OO .verify !=True :#line:116:if self.verify != True:
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:117:sys.exit('❌授权未通过 程序自动退出！！！')
        OO0OO0OO000OO0OOO ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/dailyGrabs/activity'#line:118:url = 'https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/dailyGrabs/activity'
        OOO0O0OO0OO0OO0O0 ={"accept":"application/json, text/plain, */*","accept-language":"zh-CN,zh;q=0.9,en;q=0.8","content-type":"application/json;charset=UTF-8","sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-origin","token":OO0OOOO0000OO0OOO ,"Referer":OOOOOO0O0OO00O000 ,"Referrer-Policy":"strict-origin-when-cross-origin",}#line:129:}
        if OOOOOO0OO0O0000OO .proxy !=False :#line:130:if self.proxy != False:
            O00OOO0O000OOO000 =requests .post (url =OO0OO0OO000OO0OOO ,headers =OOO0O0OO0OO0OO0O0 ,data ={},proxies =OOOOOO0OO0O0000OO .proxies )#line:131:res = requests.post(url=url, headers=headers, data={}, proxies=self.proxies)
        else :#line:132:else:
            O00OOO0O000OOO000 =requests .post (url =OO0OO0OO000OO0OOO ,headers =OOO0O0OO0OO0OO0O0 ,data ={})#line:133:res = requests.post(url=url, headers=headers, data={})
        if O00OOO0O000OOO000 .status_code ==200 :#line:134:if res.status_code == 200:
            O00OOO0O000OOO000 =O00OOO0O000OOO000 .json ()['data']#line:135:res = res.json()['data']
            O0OO0OO00O0O0OOO0 =OOOOOO0OO0O0000OO .data_timeout (O00OOO0O000OOO000 ['activityStartTime'])#line:136:StartTime = self.data_timeout(res['activityStartTime'])
            OOOO000OO00OO000O =OOOOOO0OO0O0000OO .data_timeout (O00OOO0O000OOO000 ['activityEndTime'])#line:137:EndTime = self.data_timeout(res['activityEndTime'])
            OOOOOO0OO0O0000OO .start =OOOOOO0OO0O0000OO .data_timeout (O00OOO0O000OOO000 ['lotteryTime'])#line:138:self.start = self.data_timeout(res['lotteryTime'])
            print ('-'*15 ,'记录缓存','-'*16 )#line:139:print('-' * 15,'记录缓存','-' * 16)
            print (f'开抢时间: {OOOOOO0OO0O0000OO.start} \n抢购详细: {O00OOO0O000OOO000["prizeName"]}  抢购数量: {O00OOO0O000OOO000["hours"]}个  已抢成功：{O00OOO0O000OOO000["userCount"]}个\n活动时间: {O0OO0OO00O0O0OOO0} - {OOOO000OO00OO000O}')#line:140:print(f'开抢时间: {self.start} \n抢购详细: {res["prizeName"]}  抢购数量: {res["hours"]}个  已抢成功：{res["userCount"]}个\n活动时间: {StartTime} - {EndTime}')
            print ("-"*40 )#line:141:print("-" * 40)
            OOOOOO0OOO0OOO00O =OOOOOO0OO0O0000OO .load_json_data ('activity_info.json')#line:143:existing_data = self.load_json_data('activity_info.json')
            O00000OO0OO0O0OOO ={"id":O0O0OOOO0OO0O0OOO ,"prizeInfoId":O00OOO0O000OOO000 ['prizeInfoId'],"start":datetime .strptime (OOOOOO0OO0O0000OO .start ,'%Y-%m-%d %H:%M:%S').strftime ('%H:%M:%S'),"prizeName":O00OOO0O000OOO000 ['prizeName'],"hours":O00OOO0O000OOO000 ['hours'],"userCount":O00OOO0O000OOO000 ['userCount'],"StartTime":O0OO0OO00O0O0OOO0 ,"EndTime":OOOO000OO00OO000O ,"activiturl":OOOOOO0O0OO00O000 }#line:154:}
            OOOOOO0OOO0OOO00O [OOOOOO0OO0O0000OO .activityId ]=O00000OO0OO0O0OOO #line:155:existing_data[self.activityId] = json_data
            OOOOOO0OO0O0000OO .save_json_data (OOOOOO0OOO0OOO00O ,'activity_info.json')#line:157:self.save_json_data(existing_data, 'activity_info.json')
            return O00OOO0O000OOO000 #line:158:return res
    def get_dayReceive (OO0000O0OOOO000OO ,O000O0OO00O00O00O ,O00OO0OOO00OO0O00 ,O00OO0O0OO0OO0O0O ):#line:160:def get_dayReceive(self, prizeInfoId, token, activiturl):
        if OO0000O0OOOO000OO .verify !=True :#line:161:if self.verify != True:
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:162:sys.exit('❌授权未通过 程序自动退出！！！')
        O0OOOO0OOO0OO0O0O ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/dailyGrabs/dayReceive'#line:164:url = 'https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/dailyGrabs/dayReceive'
        O000000000000O0O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O00OO0OOO00OO0O00 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':OO0000O0OOOO000OO .ua .safari ,'Connection':'keep-alive','Referer':O00OO0O0OO0OO0O0O ,}#line:176:}
        OOO0000000000O0OO ={'prizeInfoId':O000O0OO00O00O00O }#line:179:}
        if OO0000O0OOOO000OO .proxy !=False :#line:180:if self.proxy != False:
            OO0OO0O00OO0O0OO0 =requests .post (url =O0OOOO0OOO0OO0O0O ,headers =O000000000000O0O0 ,data =json .dumps (OOO0000000000O0OO ),proxies =OO0000O0OOOO000OO .proxies )#line:181:res = requests.post(url=url, headers=headers, data=json.dumps(data), proxies=self.proxies)
        else :#line:182:else:
            OO0OO0O00OO0O0OO0 =requests .post (url =O0OOOO0OOO0OO0O0O ,headers =O000000000000O0O0 ,data =json .dumps (OOO0000000000O0OO ))#line:183:res = requests.post(url=url, headers=headers,data=json.dumps(data))
        if OO0OO0O00OO0O0OO0 .status_code ==200 :#line:184:if res.status_code == 200:
            OOO0000000000O0OO =OO0OO0O00OO0O0OO0 .json ()#line:186:data = res.json()
            if 'resp_msg'in OOO0000000000O0OO and OOO0000000000O0OO ['resp_msg']:#line:187:if 'resp_msg' in data and data['resp_msg']:
                print (datetime .now (),f'PZID:{O000O0OO00O00O00O}',f'❌领取失败:{OOO0000000000O0OO["resp_msg"]}')#line:188:print(datetime.now(), f'PZID:{prizeInfoId}',f'❌领取失败:{data["resp_msg"]}')
            elif 'data'in OOO0000000000O0OO and 'result'in OOO0000000000O0OO ['data']and OOO0000000000O0OO ['data']['result']:#line:189:elif 'data' in data and 'result' in data['data'] and data['data']['result']:
                try :#line:191:try:
                    print (datetime .now (),f'PZID:{O000O0OO00O00O00O}',f"✔️领取成功:{OOO0000000000O0OO['data']['prizeName']}")#line:192:print(datetime.now(), f'PZID:{prizeInfoId}',f"✔️领取成功:{data['data']['prizeName']}")
                except Exception as O00000OO0O0O00O00 :#line:193:except Exception as e:
                    print (datetime .now (),f'PZID:{O000O0OO00O00O00O}',OO0OO0O00OO0O0OO0 .json ())#line:194:print(datetime.now(), f'PZID:{prizeInfoId}', res.json())
                    print (O00000OO0O0O00O00 )#line:195:print(e)
            else :#line:197:else:
                print (datetime .now (),f'PZID:{O000O0OO00O00O00O}','💭新鲜空气')#line:198:print(datetime.now(), f'PZID:{prizeInfoId}', '💭新鲜空气')
        else :#line:200:else:
            print (datetime .now (),f'PZID:{O000O0OO00O00O00O}',f"dayReceive：{OO0OO0O00OO0O0OO0.status_code}")#line:201:print(datetime.now(), f'PZID:{prizeInfoId}',f"dayReceive：{res.status_code}")
    def cache_Daily (O0OO00OOO000O0O0O ):#line:203:def cache_Daily(self):
        if O0OO00OOO000O0O0O .verify !=True :#line:204:if self.verify != True:
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:205:sys.exit('❌授权未通过 程序自动退出！！！')
        O0OO00OOO000O0O0O .token_activities ={}#line:206:self.token_activities = {}
        with open ('activity_info.json',encoding ="utf-8")as O0O00OO000O00000O :#line:207:with open('activity_info.json', encoding="utf-8") as file:
            O0OO00OO0O00OO000 =json .load (O0O00OO000O00000O )#line:208:data = json.load(file)
        O0OO00OOO000O0O0O .post_Token (get_cookies ()[0 ])#line:209:self.post_Token(get_cookies()[0])
        time .sleep (1 )#line:210:time.sleep(1)
        OOO0O00O00OO0OOO0 =datetime .now ().date ()#line:211:today = datetime.now().date()
        for O0O000OO0O0OO0O0O in O0OO00OO0O00OO000 :#line:212:for i in data:
            O0OOOO0O00OO0O000 =datetime .strptime (O0OO00OO0O00OO000 [O0O000OO0O0OO0O0O ]['start'],"%H:%M:%S").time ()#line:213:start_time = datetime.strptime(data[i]['start'], "%H:%M:%S").time()
            if datetime .now ()<datetime .combine (OOO0O00O00OO0OOO0 ,O0OOOO0O00OO0O000 ):#line:214:if datetime.now() < datetime.combine(today, start_time):
                OO00OO000000OO000 =datetime .combine (OOO0O00O00OO0OOO0 ,O0OOOO0O00OO0O000 )-datetime .now ()#line:215:time_difference = datetime.combine(today, start_time) - datetime.now()
                OOO00000OOO00O000 =OO00OO000000OO000 .total_seconds ()//60 #line:216:time_difference_minutes = time_difference.total_seconds() // 60
                if OOO00000OOO00O000 <=5 :#line:217:if time_difference_minutes <= 5:
                    O0OO00OOO000O0O0O .get_Token (O0OO00OO0O00OO000 [O0O000OO0O0OO0O0O ]['id'],O0OO00OO0O00OO000 [O0O000OO0O0OO0O0O ]['activiturl'],O0OO00OO0O00OO000 [O0O000OO0O0OO0O0O ]['prizeInfoId'],datetime .combine (OOO0O00O00OO0OOO0 ,O0OOOO0O00OO0O000 ))#line:219:self.get_Token(data[i]['id'], data[i]['activiturl'], data[i]['prizeInfoId'], datetime.combine(today,start_time))
        print (f"读取缓存文件成功 有{len(O0OO00OOO000O0O0O.token_activities)}个任务")#line:220:print(f"读取缓存文件成功 有{len(self.token_activities)}个任务")
        O00O00OO0OOO00O0O =False #line:221:paused = False  # 标记是否已经执行过暂停操作
        for O0O000OO0O0OO0O0O in O0OO00OOO000O0O0O .token_activities :#line:222:for i in self.token_activities:
            OO00O0O00OO00O0OO =O0OO00OOO000O0O0O .token_activities [O0O000OO0O0OO0O0O ]['start_time']#line:223:target_time = self.token_activities[i]['start_time']
            OO0000OO0OOO0O0O0 =datetime .now ()#line:224:current_time = datetime.now()  # 获取当前时间
            if OO0000OO0OOO0O0O0 <OO00O0O00OO00O0OO and not O00O00OO0OOO00O0O :#line:225:if current_time < target_time and not paused:
                OO00OO000000OO000 =OO00O0O00OO00O0OO -OO0000OO0OOO0O0O0 #line:226:time_difference = target_time - current_time  # 计算时间差
                OOO00000OOO00O000 =OO00OO000000OO000 .total_seconds ()//60 #line:227:time_difference_minutes = time_difference.total_seconds() // 60  # 转换为分钟
                if OOO00000OOO00O000 <=5 :#line:228:if time_difference_minutes <= 5:
                    O0O00O0O00OO0O0OO =OO0000OO0OOO0O0O0 .strftime ("%Y-%m-%d %H:%M:%S")#line:229:seconds = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    OOO0OOO00O0OO0OO0 =(OO00O0O00OO00O0OO -OO0000OO0OOO0O0O0 ).total_seconds ()-0.3 #line:230:wait_time = (target_time - current_time).total_seconds() - 0.3  # 计算需要等待的秒数
                    print (f"当前时间:{O0O00O0O00OO0O0OO} 需等待: {OOO0OOO00O0OO0OO0}秒")#line:231:print(f"当前时间:{seconds} 需等待: {wait_time}秒")
                    print ('-'*40 )#line:232:print('-' * 40)
                    time .sleep (OOO0OOO00O0OO0OO0 )#line:233:time.sleep(wait_time)
                    O00O00OO0OOO00O0O =True #line:234:paused = True  # 标记已经执行过暂停操作
                else :#line:235:else:
                    print (f"活动开始时间是{OO00O0O00OO00O0OO}哦！！！")#line:236:print(f"活动开始时间是{target_time}哦！！！")
        print ('-'*15 ,'倒计时结束','-'*15 )#line:237:print('-' * 15, '倒计时结束', '-' * 15)
        """ 线程并发 """#line:241:""" 线程并发 """
        O00000OO00O00OOO0 =time .time ()#line:242:start = time.time()
        for OOO00000OOOO0OOO0 in range (1 ,20 ):#line:243:for f in range(1, 20):
            O00000O0O000O0OO0 =[]#line:244:threads = []
            for O0O000OO0O0OO0O0O in O0OO00OOO000O0O0O .token_activities :#line:245:for i in self.token_activities:
                O00O00OO00O00O0OO =threading .Thread (target =O0OO00OOO000O0O0O .get_dayReceive ,args =(O0OO00OOO000O0O0O .token_activities [O0O000OO0O0OO0O0O ]["prizeInfoId"],O0OO00OOO000O0O0O .token_activities [O0O000OO0O0OO0O0O ]["token"],O0OO00OOO000O0O0O .token_activities [O0O000OO0O0OO0O0O ]["url"]))#line:248:self.token_activities[i]["url"]))
                O00000O0O000O0OO0 .append (O00O00OO00O00O0OO )#line:249:threads.append(thread_one)  # 线程池添加线程
            for O00OO00OO00O000O0 in O00000O0O000O0OO0 :#line:250:for t in threads:
                O00OO00OO00O000O0 .start ()#line:251:t.start()
            for O00OO00OO00O000O0 in O00000O0O000O0OO0 :#line:252:for t in threads:
                O00OO00OO00O000O0 .join ()#line:253:t.join()
        print (f'耗时：{time.time() - O00000OO00O00OOO0}')#line:254:print(f'耗时：{time.time() - start}')
    def main (O00O0O0OO0O0OO0O0 ):#line:257:def main(self):
        O00O0O0OO0O0OO0O0 .verif ()#line:258:self.verif()
        if O00O0O0OO0O0OO0O0 .verify !=True :#line:259:if self.verify != True:
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:260:sys.exit('❌授权未通过 程序自动退出！！！')
        OOOOO00OOOO00OO0O =datetime .now ().time ()#line:261:current_time = datetime.now().time()
        O0O0000000OOOO0OO =False #line:262:paused = False
        for OO000OOO00OO0O0OO in O00O0O0OO0O0OO0O0 .time_list :#line:263:for time_str in self.time_list:
            OO00000OOO0OOOO0O =datetime .strptime (OO000OOO00OO0O0OO ,"%H:%M").time ()#line:264:time_item = datetime.strptime(time_str, "%H:%M").time()
            OO000O00O0000OOOO =datetime .combine (datetime .now ().date (),OO00000OOO0OOOO0O )-datetime .combine (datetime .now ().date (),OOOOO00OOOO00OO0O )#line:266:datetime.now().date(), current_time)
            O00O000O00O00000O =abs (OO000O00O0000OOOO .total_seconds ())//60 #line:267:time_difference_minutes = abs(time_difference.total_seconds()) // 60
            if O00O000O00O00000O <=5 :#line:268:if time_difference_minutes <= 5:
                print ('-'*40 )#line:269:print('-' * 40)
                print (f"当前时间接近于 {OO000OOO00OO0O0OO} 开始读取缓存文件")#line:270:print(f"当前时间接近于 {time_str} 开始读取缓存文件")
                O00O0O0OO0O0OO0O0 .cache_Daily ()#line:271:self.cache_Daily()
                O0O0000000OOOO0OO =True #line:272:paused = True
            else :#line:273:else:
                if not O0O0000000OOOO0OO :#line:274:if not paused:
                    O00O0O0OO0O0OO0O0 .post_Token (get_cookies ()[0 ])#line:275:self.post_Token(get_cookies()[0])
                    time .sleep (1 )#line:276:time.sleep(1)
                    O000000OO0O0OOO00 =O00O0O0OO0O0OO0O0 .get_Token (O00O0O0OO0O0OO0O0 .activityId ,O00O0O0OO0O0OO0O0 .activiturl ,0 ,0 )[1 ]#line:277:Token = self.get_Token(self.activityId, self.activiturl, 0, 0)[1]
                    O00O0O0OO0O0OO0O0 .post_activity (O000000OO0O0OOO00 ,O00O0O0OO0O0OO0O0 .activiturl ,O00O0O0OO0O0OO0O0 .activityId )#line:278:self.post_activity(Token, self.activiturl, self.activityId)
                    O0O0000000OOOO0OO =True #line:279:paused = True
s =Daily ()

#模式1
s.main()

#模式2 死循环
# while True:
#     current_time = datetime.now().time()
#     for time_str in s.time_list:
#         time_item = datetime.strptime(time_str, "%H:%M").time()
#         target_time = datetime.combine(datetime.now().date(), time_item) - timedelta(minutes=5)
#         if current_time >= target_time.time() and current_time <= time_item:
#             s.main()
#         else:
#             print(f'当前时间：{datetime.now()}, 未到设定时间: {time_item}')
#     time.sleep(120)