#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_loreal_Daily.py(loreal_每日抢_缓存)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 56 9,19 * * *
new Env('loreal_每日抢_缓存');
"""

import requests ,re ,random ,json ,sys ,os ,time ,threading ,concurrent .futures #line:9
from utils .sign import *#line:10
from fake_useragent import UserAgent #line:12
from jdCookie import get_cookies #line:13
from datetime import datetime ,timedelta #line:14
class Daily :#line:15
    def __init__ (O00OO00OOOO00O0OO ):#line:16
        O00OO00OOOO00O0OO .ua =UserAgent ()#line:17
        O00OO00OOOO00O0OO .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:18
        O00OO00OOOO00O0OO .proxies ={'http':f'{O00OO00OOOO00O0OO.proxy}','https':f'{O00OO00OOOO00O0OO.proxy}',}#line:22
        O00OO00OOOO00O0OO .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else sys .exit ('❌TOKEN未设置')#line:23
        O00OO00OOOO00O0OO .activiturl =os .environ .get ("jd_loreal_Daily")if os .environ .get ("jd_loreal_Daily")else sys .exit ('❌未获取到jd_loreal_Daily变量 程序自动退出')#line:24
        O00OO00OOOO00O0OO .activityId =re .findall ('activityId=(\d+)',O00OO00OOOO00O0OO .activiturl )[0 ]#line:25
        O00OO00OOOO00O0OO .time_list =["10:00","20:00"]#line:26
        O00OO00OOOO00O0OO .token_activities ={}#line:27
        O00OO00OOOO00O0OO .start =''#line:28
        O00OO00OOOO00O0OO .pause =False #line:29
        O00OO00OOOO00O0OO .verify =False #line:30
    def verif (O000O00OO0OOOO0OO ):#line:32
        try :#line:33
            O000O00OO0OOOO0OO .verify =verify (O000O00OO0OOOO0OO .token )#line:34
            if O000O00OO0OOOO0OO .verify !=True :#line:35
                sys .exit ('❌授权未通过 程序自动退出！！！')#line:36
            return O000O00OO0OOOO0OO .verify #line:37
        except Exception as OO0OO0O0O000OO0O0 :#line:38
            print (f'验证授权失败： {OO0OO0O0O000OO0O0}')#line:39
    def save_json_data (O00OOO000000OOOO0 ,OOO0O0O0O00OOOOO0 ,OOOOO00O0OOOOOOOO ):#line:40
        with open (OOOOO00O0OOOOOOOO ,'w',encoding ='utf-8')as OOO0OOOOO0O0OOOO0 :#line:42
            json .dump (OOO0O0O0O00OOOOO0 ,OOO0OOOOO0O0OOOO0 ,ensure_ascii =False ,indent =4 )#line:43
    def load_json_data (O00O0OOOO00O00OOO ,OO0O00O00OO0O00OO ):#line:45
        with open (OO0O00O00OO0O00OO ,'r',encoding ='utf-8')as OOO00OO0OO0O000O0 :#line:47
            OO0O0000OOOOOOO0O =json .load (OOO00OO0OO0O000O0 )#line:48
        return OO0O0000OOOOOOO0O #line:49
    def data_timeout (OOO0OOOOOO00OOO0O ,O00000OO00000OO0O ):#line:50
        O0O00O0O0OOOOO000 =datetime .fromtimestamp (O00000OO00000OO0O /1000 )#line:51
        OO0O00O00O00OOOOO =O0O00O0O0OOOOO000 .strftime ("%Y-%m-%d %H:%M:%S")#line:52
        return OO0O00O00O00OOOOO #line:53
    def post_Token (O000OO0OOO000O000 ,OO00OO0O000000OO0 ):#line:54
        if O000OO0OOO000O000 .verify !=True :#line:55
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:56
        OO0O00000O0OOOOOO ='https://api.m.jd.com/client.action'#line:57
        OOOOO00O0O0O00O0O ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':O000OO0OOO000O000 .ua .safari ,'Cookie':OO00OO0O000000OO0 ,'Host':'api.m.jd.com','Referer':'','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:68
        O00O0OO00O000O00O =get_sign ('isvObfuscator',{'id':'','url':'https://lzkj-isv.isvjcloud.com'})#line:69
        if O000OO0OOO000O000 .proxy !=False :#line:70
            OOOO0OO000000O000 =requests .post (url =OO0O00000O0OOOOOO ,headers =OOOOO00O0O0O00O0O ,data =O00O0OO00O000O00O ,proxies =O000OO0OOO000O000 .proxies )#line:71
        else :#line:72
            OOOO0OO000000O000 =requests .post (url =OO0O00000O0OOOOOO ,headers =OOOOO00O0O0O00O0O ,data =O00O0OO00O000O00O )#line:73
        if OOOO0OO000000O000 .status_code !=200 :#line:74
            sys .exit (f'❌ 获取Token失败:{OOOO0OO000000O000.status_code}, 程序将自动退出！！')#line:75
        if 'token'in OOOO0OO000000O000 .json ():#line:76
            O000OO0OOO000O000 .token =OOOO0OO000000O000 .json ()['token']#line:78
        else :#line:79
            print (OOOO0OO000000O000 .json ())#line:80
    def get_Token (O0O00000OOOOOOO0O ,OOO00OOOO00OOOO0O ,O00OOO0O0OO0OO000 ,O00OO0OO000O00O00 ,O0OOOOO0OOOOO000O ):#line:82
        if O0O00000OOOOOOO0O .verify !=True :#line:83
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:84
        O000O0O0O00000OO0 ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login'#line:85
        O000O000O0OOOO0OO ={"status":"0","activityId":OOO00OOOO00OOOO0O ,"source":"01","tokenPin":O0O00000OOOOOOO0O .token ,"shareUserId":""}#line:86
        OO00OOOOO0O000OOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/json;charset=UTF-8','Origin':f'https://lzkj-isv.isvjcloud.com','User-Agent':O0O00000OOOOOOO0O .ua .safari ,'Connection':'keep-alive','Referer':O00OOO0O0OO0OO000 ,}#line:97
        if O0O00000OOOOOOO0O .proxy !=False :#line:98
            OO0OOOOOOOO00000O =requests .post (url =O000O0O0O00000OO0 ,headers =OO00OOOOO0O000OOO ,data =json .dumps (O000O000O0OOOO0OO ),proxies =O0O00000OOOOOOO0O .proxies )#line:99
        else :#line:100
            OO0OOOOOOOO00000O =requests .post (url =O000O0O0O00000OO0 ,headers =OO00OOOOO0O000OOO ,data =json .dumps (O000O000O0OOOO0OO ))#line:101
        if OO0OOOOOOOO00000O .status_code !=200 :#line:102
            sys .exit (f'❌ 登录失败:{OO0OOOOOOOO00000O.status_code}, 程序将自动退出！！')#line:103
        O0O00OOO000O0O0O0 ={"start_time":O0OOOOO0OOOOO000O ,"activityId":OOO00OOOO00OOOO0O ,"prizeInfoId":O00OO0OO000O00O00 ,"token":OO0OOOOOOOO00000O .json ()['data']['token'],"url":O00OOO0O0OO0OO000 ,}#line:110
        O0O00000OOOOOOO0O .token_activities [OOO00OOOO00OOOO0O ]=O0O00OOO000O0O0O0 #line:111
        return 200 ,OO0OOOOOOOO00000O .json ()['data']['token'],OO0OOOOOOOO00000O .json ()['data']['userPin']#line:112
    def post_activity (O0OOOOOOOOO000000 ,OOOO0O0OOOOO00OOO ,O00O0O000O0OOO0O0 ,OOO0OOO000O0O000O ):#line:114
        if O0OOOOOOOOO000000 .verify !=True :#line:115
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:116
        O0OO00OO0OO0O000O ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/dailyGrabs/activity'#line:117
        O0O00O00O00OO000O ={"accept":"application/json, text/plain, */*","accept-language":"zh-CN,zh;q=0.9,en;q=0.8","content-type":"application/json;charset=UTF-8","sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-origin","token":OOOO0O0OOOOO00OOO ,"Referer":O00O0O000O0OOO0O0 ,"Referrer-Policy":"strict-origin-when-cross-origin",}#line:128
        if O0OOOOOOOOO000000 .proxy !=False :#line:129
            OOOO0OO0O0OOOO00O =requests .post (url =O0OO00OO0OO0O000O ,headers =O0O00O00O00OO000O ,data ={},proxies =O0OOOOOOOOO000000 .proxies )#line:130
        else :#line:131
            OOOO0OO0O0OOOO00O =requests .post (url =O0OO00OO0OO0O000O ,headers =O0O00O00O00OO000O ,data ={})#line:132
        if OOOO0OO0O0OOOO00O .status_code ==200 :#line:133
            OOOO0OO0O0OOOO00O =OOOO0OO0O0OOOO00O .json ()['data']#line:134
            O0000OOOO0O0O0000 =O0OOOOOOOOO000000 .data_timeout (OOOO0OO0O0OOOO00O ['activityStartTime'])#line:135
            OO0000OOO0OO0000O =O0OOOOOOOOO000000 .data_timeout (OOOO0OO0O0OOOO00O ['activityEndTime'])#line:136
            O0OOOOOOOOO000000 .start =O0OOOOOOOOO000000 .data_timeout (OOOO0OO0O0OOOO00O ['lotteryTime'])#line:137
            print ('-'*15 ,'记录缓存','-'*16 )#line:138
            print (f'开抢时间: {O0OOOOOOOOO000000.start} \n抢购详细: {OOOO0OO0O0OOOO00O["prizeName"]}  抢购数量: {OOOO0OO0O0OOOO00O["hours"]}个  已抢成功：{OOOO0OO0O0OOOO00O["userCount"]}个\n活动时间: {O0000OOOO0O0O0000} - {OO0000OOO0OO0000O}')#line:139
            print ("-"*40 )#line:140
            OO00OOO0000OOOO0O =O0OOOOOOOOO000000 .load_json_data ('activity_info.json')#line:142
            O0O0O00OOOO0O000O ={"id":OOO0OOO000O0O000O ,"prizeInfoId":OOOO0OO0O0OOOO00O ['prizeInfoId'],"start":datetime .strptime (O0OOOOOOOOO000000 .start ,'%Y-%m-%d %H:%M:%S').strftime ('%H:%M:%S'),"prizeName":OOOO0OO0O0OOOO00O ['prizeName'],"hours":OOOO0OO0O0OOOO00O ['hours'],"userCount":OOOO0OO0O0OOOO00O ['userCount'],"StartTime":O0000OOOO0O0O0000 ,"EndTime":OO0000OOO0OO0000O ,"activiturl":O00O0O000O0OOO0O0 }#line:153
            OO00OOO0000OOOO0O [O0OOOOOOOOO000000 .activityId ]=O0O0O00OOOO0O000O #line:154
            O0OOOOOOOOO000000 .save_json_data (OO00OOO0000OOOO0O ,'activity_info.json')#line:156
            return OOOO0OO0O0OOOO00O #line:157
    def get_dayReceive (O0OOO0OOOOO00000O ,OOOOOOO0O0O0O0OOO ,O0000000O0OOO0OOO ,O0O0OO0O0000O0O00 ):#line:159
        if O0OOO0OOOOO00000O .verify !=True :#line:160
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:161
        OO0O0O0O00O00OO00 ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/dailyGrabs/dayReceive'#line:163
        OOO0O00OOO00OOO00 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':O0000000O0OOO0OOO ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':O0OOO0OOOOO00000O .ua .safari ,'Connection':'keep-alive','Referer':O0O0OO0O0000O0O00 ,}#line:175
        OO00O0OO0O0OO0O0O ={'prizeInfoId':OOOOOOO0O0O0O0OOO }#line:178
        if O0OOO0OOOOO00000O .proxy !=False :#line:179
            OO00OO00O00O00000 =requests .post (url =OO0O0O0O00O00OO00 ,headers =OOO0O00OOO00OOO00 ,data =json .dumps (OO00O0OO0O0OO0O0O ),proxies =O0OOO0OOOOO00000O .proxies )#line:180
        else :#line:181
            OO00OO00O00O00000 =requests .post (url =OO0O0O0O00O00OO00 ,headers =OOO0O00OOO00OOO00 ,data =json .dumps (OO00O0OO0O0OO0O0O ))#line:182
        if OO00OO00O00O00000 .status_code ==200 :#line:183
            OO00O0OO0O0OO0O0O =OO00OO00O00O00000 .json ()#line:185
            if 'resp_msg'in OO00O0OO0O0OO0O0O and OO00O0OO0O0OO0O0O ['resp_msg']:#line:186
                print (datetime .now (),f'PZID:{OOOOOOO0O0O0O0OOO}',f'❌领取失败:{OO00O0OO0O0OO0O0O["resp_msg"]}')#line:187
            elif 'data'in OO00O0OO0O0OO0O0O and 'result'in OO00O0OO0O0OO0O0O ['data']and OO00O0OO0O0OO0O0O ['data']['result']:#line:188
                try :#line:190
                    print (datetime .now (),f'PZID:{OOOOOOO0O0O0O0OOO}',f"✔️领取成功:{OO00O0OO0O0OO0O0O['data']['prizeName']}")#line:191
                except Exception as O0OO0O0O00OOOO000 :#line:192
                    print (datetime .now (),f'PZID:{OOOOOOO0O0O0O0OOO}',OO00OO00O00O00000 .json ())#line:193
                    print (O0OO0O0O00OOOO000 )#line:194
            else :#line:196
                print (datetime .now (),f'PZID:{OOOOOOO0O0O0O0OOO}','💭新鲜空气')#line:197
        else :#line:199
            print (datetime .now (),f'PZID:{OOOOOOO0O0O0O0OOO}',f"dayReceive：{OO00OO00O00O00000.status_code}")#line:200
    def cache_Daily (OOO00O0O0000O00O0 ):#line:202
        if OOO00O0O0000O00O0 .verify !=True :#line:203
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:204
        OOO00O0O0000O00O0 .token_activities ={}#line:205
        with open ('activity_info.json',encoding ="utf-8")as OOOOO0OOOO0O00O0O :#line:206
            O0O00000OOO0OOO0O =json .load (OOOOO0OOOO0O00O0O )#line:207
        OOO00O0O0000O00O0 .post_Token (get_cookies ()[0 ])#line:208
        time .sleep (1 )#line:209
        OOO00O0000OOOOO00 =datetime .now ().date ()#line:210
        for O0O000O00O0OO000O in O0O00000OOO0OOO0O :#line:211
            O00O0000O0O00000O =datetime .strptime (O0O00000OOO0OOO0O [O0O000O00O0OO000O ]['EndTime'],'%Y-%m-%d %H:%M:%S')#line:212
            if datetime .now ()>O00O0000O0O00000O :#line:213
                continue #line:214
            O0O00OOO0O00OO00O =datetime .strptime (O0O00000OOO0OOO0O [O0O000O00O0OO000O ]['start'],"%H:%M:%S").time ()#line:215
            if datetime .now ()<datetime .combine (OOO00O0000OOOOO00 ,O0O00OOO0O00OO00O ):#line:216
                OOO0000OO0O0O0O00 =datetime .combine (OOO00O0000OOOOO00 ,O0O00OOO0O00OO00O )-datetime .now ()#line:217
                O0000OOO0O0O0OO00 =OOO0000OO0O0O0O00 .total_seconds ()//60 #line:218
                if O0000OOO0O0O0OO00 <=5 :#line:219
                    OOO00O0O0000O00O0 .get_Token (O0O00000OOO0OOO0O [O0O000O00O0OO000O ]['id'],O0O00000OOO0OOO0O [O0O000O00O0OO000O ]['activiturl'],O0O00000OOO0OOO0O [O0O000O00O0OO000O ]['prizeInfoId'],datetime .combine (OOO00O0000OOOOO00 ,O0O00OOO0O00OO00O ))#line:221
        print (f"读取缓存文件成功 有{len(OOO00O0O0000O00O0.token_activities)}个任务")#line:222
        OOOO00O0O0OO0O0OO =False #line:223
        for O0O000O00O0OO000O in OOO00O0O0000O00O0 .token_activities :#line:224
            OO000O0O000OOOOO0 =OOO00O0O0000O00O0 .token_activities [O0O000O00O0OO000O ]['start_time']#line:225
            O000OOOO0O000OOO0 =datetime .now ()#line:226
            if O000OOOO0O000OOO0 <OO000O0O000OOOOO0 and not OOOO00O0O0OO0O0OO :#line:227
                OOO0000OO0O0O0O00 =OO000O0O000OOOOO0 -O000OOOO0O000OOO0 #line:228
                O0000OOO0O0O0OO00 =OOO0000OO0O0O0O00 .total_seconds ()//60 #line:229
                if O0000OOO0O0O0OO00 <=5 :#line:230
                    OOO0OOOOOOOOO00OO =O000OOOO0O000OOO0 .strftime ("%Y-%m-%d %H:%M:%S")#line:231
                    O000O00O00OO00OO0 =(OO000O0O000OOOOO0 -O000OOOO0O000OOO0 ).total_seconds ()-0.3 #line:232
                    print (f"当前时间:{OOO0OOOOOOOOO00OO} 需等待: {O000O00O00OO00OO0}秒")#line:233
                    print ('-'*40 )#line:234
                    time .sleep (O000O00O00OO00OO0 )#line:235
                    OOOO00O0O0OO0O0OO =True #line:236
                else :#line:237
                    print (f"活动开始时间是{OO000O0O000OOOOO0}哦！！！")#line:238
        print ('-'*15 ,'倒计时结束','-'*15 )#line:239
        """ 线程并发 """#line:243
        OO0O0000O0OOO0O00 =time .time ()#line:244
        for O0OOO0OO0OOO0O0OO in range (1 ,20 ):#line:245
            O00000OO0OOO00O0O =[]#line:246
            for O0O000O00O0OO000O in OOO00O0O0000O00O0 .token_activities :#line:247
                OOO0000OO0000OOOO =threading .Thread (target =OOO00O0O0000O00O0 .get_dayReceive ,args =(OOO00O0O0000O00O0 .token_activities [O0O000O00O0OO000O ]["prizeInfoId"],OOO00O0O0000O00O0 .token_activities [O0O000O00O0OO000O ]["token"],OOO00O0O0000O00O0 .token_activities [O0O000O00O0OO000O ]["url"]))#line:250
                O00000OO0OOO00O0O .append (OOO0000OO0000OOOO )#line:251
            for OO000000O0O0OOO0O in O00000OO0OOO00O0O :#line:252
                OO000000O0O0OOO0O .start ()#line:253
            for OO000000O0O0OOO0O in O00000OO0OOO00O0O :#line:254
                OO000000O0O0OOO0O .join ()#line:255
        print (f'耗时：{time.time() - OO0O0000O0OOO0O00}')#line:256
    def main (OOOO0O0OOO0OOOO00 ):#line:259
        OOOO0O0OOO0OOOO00 .verif ()#line:260
        if OOOO0O0OOO0OOOO00 .verify !=True :#line:261
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:262
        OOO0O0O0O00O000OO =datetime .now ().time ()#line:263
        O000000O000O000OO =False #line:264
        for OO0000OO0OO0O00OO in OOOO0O0OOO0OOOO00 .time_list :#line:265
            OO00O00OO0OOOOO00 =datetime .strptime (OO0000OO0OO0O00OO ,"%H:%M").time ()#line:266
            O0O0OO0000000OO0O =datetime .combine (datetime .now ().date (),OO00O00OO0OOOOO00 )-datetime .combine (datetime .now ().date (),OOO0O0O0O00O000OO )#line:268
            O0O0O0O0O000O00O0 =abs (O0O0OO0000000OO0O .total_seconds ())//60 #line:269
            if O0O0O0O0O000O00O0 <=5 :#line:270
                print ('-'*40 )#line:271
                print (f"当前时间接近于 {OO0000OO0OO0O00OO} 开始读取缓存文件")#line:272
                OOOO0O0OOO0OOOO00 .cache_Daily ()#line:273
                O000000O000O000OO =True #line:274
            else :#line:275
                if not O000000O000O000OO :#line:276
                    OOOO0O0OOO0OOOO00 .post_Token (get_cookies ()[0 ])#line:277
                    time .sleep (1 )#line:278
                    OO0O00O0O0O0OOO0O =OOOO0O0OOO0OOOO00 .get_Token (OOOO0O0OOO0OOOO00 .activityId ,OOOO0O0OOO0OOOO00 .activiturl ,0 ,0 )[1 ]#line:279
                    OOOO0O0OOO0OOOO00 .post_activity (OO0O00O0O0O0OOO0O ,OOOO0O0OOO0OOOO00 .activiturl ,OOOO0O0OOO0OOOO00 .activityId )#line:280
                    O000000O000O000OO =True #line:281
s =Daily ()#line:283
s .main ()#line:284
