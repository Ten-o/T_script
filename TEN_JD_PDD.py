#!/usr/bin/env python3
"""
File: TEN_JD_PDD.py(邀好友赢现金-助理)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-助理');
"""

import random #line:10
from utils .logger import setup_logger #line:12
from utils .X_API_EID_TOKEN import *#line:13
from utils .User_agent import *#line:14
import asyncio ,aiohttp ,re ,os ,sys ,threading ,concurrent .futures ,time ,json #line:15
from utils .jdCookie import get_cookies #line:16
try :#line:18
    ck =get_cookies ()#line:19
    if not ck :#line:20
        sys .exit ()#line:21
except :#line:22
    print ("未获取到有效COOKIE,退出程序！")#line:23
    sys .exit ()#line:24
class TEN_JD_PDD :#line:27
    def __init__ (O0O0OO0OO0O000O0O ):#line:28
        O0O0OO0OO0O000O0O .log =setup_logger ()#line:29
        O0O0OO0OO0O000O0O .start =time .time ()#line:30
        O0O0OO0OO0O000O0O .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:32
        O0O0OO0OO0O000O0O .inviter =os .environ .get ("TEN_inviter")if os .environ .get ("TEN_inviter")else False #line:33
        O0O0OO0OO0O000O0O .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:34
        O0O0OO0OO0O000O0O .proxy_url =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:35
        O0O0OO0OO0O000O0O .semaphore =asyncio .Semaphore (int (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 50 ))#line:36
        O0O0OO0OO0O000O0O .proxy =[]#line:37
        O0O0OO0OO0O000O0O .power_success =[]#line:38
        O0O0OO0OO0O000O0O .power_failure =[]#line:39
        O0O0OO0OO0O000O0O .not_log =[]#line:40
        O0O0OO0OO0O000O0O .exit_event =threading .Event ()#line:41
        O0O0OO0OO0O000O0O .coookie =ck [0 ]#line:42
        O0O0OO0OO0O000O0O .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:49
        O0O0OO0OO0O000O0O .verify_result =False #line:50
        O0O0OO0OO0O000O0O .linkId =[]#line:51
        O0O0OO0OO0O000O0O .inviter_help =''#line:52
        O0O0OO0OO0O000O0O .version ='1.3.6'#line:53
        O0O0OO0OO0O000O0O .exit_condition =300 #line:54
        O0O0OO0OO0O000O0O .lock =threading .Lock ()#line:55
    def pt_pin (O00OO0O0O0OO000O0 ,O0O000OO0000OO0O0 ):#line:57
        try :#line:58
            O0OO0O0O0000O00O0 =re .compile (r'pt_pin=(.*?);').findall (O0O000OO0000OO0O0 )[0 ]#line:59
            O0OO0O0O0000O00O0 =unquote_plus (O0OO0O0O0000O00O0 )#line:60
        except IndexError :#line:61
            O0OO0O0O0000O00O0 =re .compile (r'pin=(.*?);').findall (O0O000OO0000OO0O0 )[0 ]#line:62
            O0OO0O0O0000O00O0 =unquote_plus (O0OO0O0O0000O00O0 )#line:63
        return O0OO0O0O0000O00O0 #line:64
    def fetch_proxies_from_api (OOOO00O0O00OOOO0O ):#line:67
        try :#line:68
            OO0OOO00OOOO00O00 =requests .get (OOOO00O0O00OOOO0O .proxy_url ,timeout =5 )#line:69
            O0O000OO0O000OO0O =OO0OOO00OOOO00O00 .text .splitlines ()#line:70
            OOOO00O0O00OOOO0O .log .debug (f'获取到代理IP：{len(O0O000OO0O000OO0O)}个')#line:71
            with OOOO00O0O00OOOO0O .lock :#line:72
                OOOO00O0O00OOOO0O .proxy =O0O000OO0O000OO0O #line:73
        except Exception as OO000000O0O00O0OO :#line:74
            OOOO00O0O00OOOO0O .log .error (f'无法获取代理列表: {str(OO000000O0O00O0OO)}')#line:75
    def convert_ms_to_hours_minutes (OO0O0O0OO0OO0OO00 ,OO0OO0OOO0O000OO0 ):#line:78
        OO0OOO00OOOOOO0OO =OO0OO0OOO0O000OO0 //1000 #line:79
        OO0000OO0000OOOOO ,OO0OOO00OOOOOO0OO =divmod (OO0OOO00OOOOOO0OO ,60 )#line:80
        O000OOO0O00O0OO0O ,OO0000OO0000OOOOO =divmod (OO0000OO0000OOOOO ,60 )#line:81
        return f'{O000OOO0O00O0OO0O}:{OO0000OO0000OOOOO}'#line:82
    def list_of_groups (OOO00O0000000OOO0 ,OOO0OO0OO0O0000O0 ,OOOO000O00000O000 ):#line:84
        OOOO00OOOOO000000 =zip (*(iter (OOO0OO0OO0O0000O0 ),)*OOOO000O00000O000 )#line:85
        OOO0OO00OO0OO0OOO =[list (O00OO0OO00OOOO000 )for O00OO0OO00OOOO000 in OOOO00OOOOO000000 ]#line:86
        OO0OO0OO0O00OO0O0 =len (OOO0OO0OO0O0000O0 )%OOOO000O00000O000 #line:87
        OOO0OO00OO0OO0OOO .append (OOO0OO0OO0O0000O0 [-OO0OO0OO0O00OO0O0 :])if OO0OO0OO0O00OO0O0 !=0 else OOO0OO00OO0OO0OOO #line:88
        return OOO0OO00OO0OO0OOO #line:89
    async def retry_with_backoff (OOO00000000000OO0 ,OOO0O00O0O000OOO0 ,OOO0000O0O00000O0 ,OOOO0OOOOO0O0OO00 ,backoff_seconds =0 ):#line:91
        for O0O0000O0OO00OOO0 in range (OOO0000O0O00000O0 ):#line:92
            O00OO000OO00OO0OO =False #line:93
            try :#line:94
                return await OOO0O00O0O000OOO0 ()#line:95
            except asyncio .TimeoutError :#line:96
                if not O00OO000OO00OO0OO :#line:97
                    OOO00000000000OO0 .log .warning (f'第{O0O0000O0OO00OOO0 + 1}次重试 {OOOO0OOOOO0O0OO00} 请求超时')#line:98
                    O00OO000OO00OO0OO =True #line:99
                await asyncio .sleep (backoff_seconds )#line:100
            except Exception as O0O0OOO000O0OO0OO :#line:101
                if not O00OO000OO00OO0OO :#line:102
                    OOO00000000000OO0 .log .warning (f'第{O0O0000O0OO00OOO0 + 1}次重试 {OOOO0OOOOO0O0OO00} 出错：{O0O0OOO000O0OO0OO}')#line:103
                    O00OO000OO00OO0OO =True #line:104
                await asyncio .sleep (backoff_seconds )#line:105
            if O00OO000OO00OO0OO and O0O0000O0OO00OOO0 ==OOO0000O0O00000O0 -1 :#line:107
                OOO00000000000OO0 .log .error (f'{OOOO0OOOOO0O0OO00} 重试{OOO0000O0O00000O0}次后仍然发生异常')#line:108
                return False ,False ,False #line:109
    async def verify (OOO0OOO0O0O00O000 ):#line:112
        OOO0OOO0O0O00O000 .verify_result =True #line:113
        async def OO0000OOOO00O000O ():#line:114
            O0O0000OOO0OOO000 ='https://api.ixu.cc/verify'#line:115
            async with aiohttp .ClientSession ()as O00OO0O000O0O00O0 :#line:116
                async with O00OO0O000O0O00O0 .get (O0O0000OOO0OOO000 ,data ={'TOKEN':OOO0OOO0O0O00O000 .token },timeout =3 )as O0O0OOOOOOO00O0OO :#line:117
                    O00O00O0OO000OOOO =await O0O0OOOOOOO00O0OO .json ()#line:118
                    if O0O0OOOOOOO00O0OO .status ==200 :#line:119
                        OOO0OOO0O0O00O000 .verify_result =True #line:120
                        OOO0OOO0O0O00O000 .log .info (f'认证通过 UserId：{O00O00O0OO000OOOO["user_id"]}')#line:121
                        return O00O00O0OO000OOOO #line:122
                    else :#line:123
                        OOO0OOO0O0O00O000 .log .error (f"授权未通过:{O00O00O0OO000OOOO['error']}")#line:124
                        sys .exit ()#line:125
        return await OOO0OOO0O0O00O000 .retry_with_backoff (OO0000OOOO00O000O ,3 ,'verify')#line:127
    def parse_version (O00000O0OO000OO00 ,OOO0O000O00OOO00O ):#line:129
        return list (map (int ,OOO0O000O00OOO00O .split ('.')))#line:130
    def is_major_update (O000O00O0OO00O0O0 ,O0OO0OO00O0000OO0 ,O0O0O000000OO0OOO ):#line:132
        if O0OO0OO00O0000OO0 [1 ]!=O0O0O000000OO0OOO [1 ]:#line:133
            return True #line:134
        elif O0OO0OO00O0000OO0 [0 ]!=O0O0O000000OO0OOO [0 ]:#line:135
            return True #line:136
        else :#line:137
            return False #line:138
    def is_force_update (O0O00000000O0OOO0 ,O0OOOOO000OOOO00O ,OOO00O0O00OOOOO00 ):#line:140
        if O0O00000000O0OOO0 .is_major_update (O0OOOOO000OOOO00O ,OOO00O0O00OOOOO00 ):#line:141
            return True #line:142
        elif OOO00O0O00OOOOO00 [2 ]-O0OOOOO000OOOO00O [2 ]>=3 :#line:143
            return True #line:144
        elif OOO00O0O00OOOOO00 [2 ]<O0OOOOO000OOOO00O [2 ]:#line:145
            return True #line:146
        else :#line:147
            return False #line:148
    async def LinkId (OO0OOO0O000O0O000 ):#line:150
        async def OOO0O0OOO00OO000O ():#line:151
            if OO0OOO0O000O0O000 .verify_result !=True :#line:152
                await OO0OOO0O000O0O000 .verify ()#line:153
            if OO0OOO0O000O0O000 .verify_result !=True :#line:154
                OO0OOO0O000O0O000 .log .error ("授权未通过 退出")#line:155
                sys .exit ()#line:156
            OO00OOO0000000OO0 ='https://api.ixu.cc/status/inviter.json'#line:157
            async with aiohttp .ClientSession ()as OO00000000OOO0O0O :#line:158
                async with OO00000000OOO0O0O .get (OO00OOO0000000OO0 ,params ={'TOKEN':OO0OOO0O000O0O000 .token },timeout =3 )as OO0O0OOOOO0000OOO :#line:159
                    if OO0O0OOOOO0000OOO .status ==200 :#line:160
                        OOO00OO0O00OOO0O0 =await OO0O0OOOOO0000OOO .json ()#line:161
                        if OOO00OO0O00OOO0O0 ['stats']!='True':#line:162
                            OO0OOO0O000O0O000 .log .error (f"{OOO00OO0O00OOO0O0['err_text']}")#line:163
                            sys .exit ()#line:164
                        OO0OOO0O000O0O000 .inviter_help =OOO00OO0O00OOO0O0 ['inviter']#line:165
                        if OO0OOO0O000O0O000 .is_force_update (OO0OOO0O000O0O000 .parse_version (OO0OOO0O000O0O000 .version ),OO0OOO0O000O0O000 .parse_version (OOO00OO0O00OOO0O0 ["version"])):#line:166
                            OO0OOO0O000O0O000 .log .error (f'强制更新 云端版本:{OOO00OO0O00OOO0O0["version"]},当前版本:{OO0OOO0O000O0O000.version} {OOO00OO0O00OOO0O0["upload_text"]}')#line:168
                            sys .exit ()#line:169
                        else :#line:170
                            OO0OOO0O000O0O000 .log .debug (f'云端版本:{OOO00OO0O00OOO0O0["version"]},当前版本:{OO0OOO0O000O0O000.version}')#line:171
                        if len (OOO00OO0O00OOO0O0 ['text'])>0 :#line:172
                            OO0OOO0O000O0O000 .log .debug (f'那女孩对你说:{OOO00OO0O00OOO0O0["text"]}')#line:173
                        if OO0OOO0O000O0O000 .scode =='ALL'or OO0OOO0O000O0O000 .scode =='all':#line:174
                            for OO0O0OO000OO0OOOO in OOO00OO0O00OOO0O0 ['linkId']:#line:175
                                OO0OOO0O000O0O000 .linkId .append (OO0O0OO000OO0OOOO )#line:176
                                OO0OOO0O000O0O000 .log .info (f'云端获取到linkId:{OO0O0OO000OO0OOOO}')#line:177
                            return True #line:178
                        else :#line:179
                            OO0OOO0O000O0O000 .linkId .append (OOO00OO0O00OOO0O0 ['linkId'][int (OO0OOO0O000O0O000 .scode )-1 ])#line:180
                            OO0OOO0O000O0O000 .log .info (f'云端获取到linkId:{OOO00OO0O00OOO0O0["linkId"][int(OO0OOO0O000O0O000.scode) - 1]}')#line:181
                            return True #line:182
                    else :#line:183
                        OO0OOO0O000O0O000 .log .error ('未获取到linkId 重试')#line:184
        return await OO0OOO0O000O0O000 .retry_with_backoff (OOO0O0OOO00OO000O ,3 ,'linkId')#line:186
    async def Get_H5st (O0000O000OO0O00O0 ,O0O0OO000000OO0OO ,O00OO000OOOO00OOO ,OO0O0O0OO0000OOO0 ,OO00O000OO00000OO ,OOO0OO0O00OO0000O ):#line:188
        async def O00000OO00OOO0000 ():#line:189
            if O0000O000OO0O00O0 .verify_result !=True :#line:190
                O0000O000OO0O00O0 .log .error ("授权未通过 退出")#line:191
                sys .exit ()#line:192
            OOO00O000O0000OO0 ='https://api.ouklc.com/api/h5st'#line:193
            OOOO00OOO0000OO0O =O0000O000OO0O00O0 .pt_pin (OOO0OO0O00OO0000O )#line:194
            O0OOOOO0000O0000O ={'functionId':O0O0OO000000OO0OO ,'body':json .dumps (O00OO000OOOO00OOO ),'ua':OO0O0O0OO0000OOO0 ,'pin':OOOO00OOO0000OO0O ,'appId':OO00O000OO00000OO }#line:201
            async with aiohttp .ClientSession ()as OOOOOO0O000O000O0 :#line:202
                async with OOOOOO0O000O000O0 .get (OOO00O000O0000OO0 ,params =O0OOOOO0000O0000O ,timeout =10 )as OOOO00O0OO00O0O00 :#line:203
                    if OOOO00O0OO00O0O00 .status ==200 :#line:204
                        OO0000O000OO000O0 =await OOOO00O0OO00O0O00 .json ()#line:205
                        return OO0000O000OO000O0 ['body']#line:207
                    else :#line:208
                        return await O0000O000OO0O00O0 .retry_with_backoff (O00000OO00OOO0000 ,3 ,'H5st')#line:209
        return await O0000O000OO0O00O0 .retry_with_backoff (O00000OO00OOO0000 ,3 ,'H5st')#line:211
    async def Get_H5_Api (OOO000O00OO0OOO0O ,OO0000000OO00O0O0 ,O0O0O00OOO00000OO ,O0O0OO00OO0OOO00O ,OOO000O0OOO0O00OO ):#line:213
        async def OO0OO0O0O0O00OO0O (OO00O0O0O0O00OO0O ):#line:214
            if OOO000O00OO0OOO0O .verify_result !=True :#line:215
                OOO000O00OO0OOO0O .log .error ("授权未通过 退出")#line:216
                sys .exit ()#line:217
            O000OOO00O0O0OOOO =generate_random_user_agent ()#line:218
            OOOO00O0O0OOO0OOO ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":O0O0OO00OO0OOO00O ,"User-Agent":O000OOO00O0O0OOOO }#line:230
            OOOOO00000O000OOO =getUUID ("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")#line:231
            OO00O0O0O0O00OO0O =await OOO000O00OO0OOO0O .Get_H5st (OO0000000OO00O0O0 ,OO00O0O0O0O00OO0O ,O000OOO00O0O0OOOO ,OOO000O0OOO0O00OO ,O0O0OO00OO0OOO00O )#line:232
            O0O0OOO0OOOO000O0 ="https://api.m.jd.com"#line:234
            async with aiohttp .ClientSession ()as O0O0000O0O000O000 :#line:235
                if OOO000O00OO0OOO0O .proxy ==False :#line:236
                    async with O0O0000O0O000O000 .post (O0O0OOO0OOOO000O0 ,headers =OOOO00O0O0OOO0OOO ,data =OO00O0O0O0O00OO0O ,timeout =5 )as O00OO0O00O0O0O00O :#line:237
                        if O00OO0O00O0O0O00O .status ==200 :#line:238
                            return await O00OO0O00O0O0O00O .json ()#line:239
                        else :#line:241
                            OOO000O00OO0OOO0O .log .error (f'重试 请求结果：{O00OO0O00O0O0O00O.status}')#line:242
                else :#line:243
                    if len (OOO000O00OO0OOO0O .proxy )<1 :#line:244
                        OOO000O00OO0OOO0O .fetch_proxies_from_api ()#line:245
                    OOOO0OO0OO0OOO00O =random .choice (OOO000O00OO0OOO0O .proxy )#line:246
                    async with O0O0000O0O000O000 .post (O0O0OOO0OOOO000O0 ,headers =OOOO00O0O0OOO0OOO ,data =OO00O0O0O0O00OO0O ,timeout =5 ,proxy ='http://'+OOOO0OO0OO0OOO00O )as O00OO0O00O0O0O00O :#line:247
                        if O00OO0O00O0O0O00O .status ==200 :#line:248
                            return await O00OO0O00O0O0O00O .json ()#line:249
                        else :#line:250
                            OOO000O00OO0OOO0O .log .error (f'重试 请求结果：{O00OO0O00O0O0O00O.status}')#line:251
                            await OOO000O00OO0OOO0O .Get_H5_Api (OO0000000OO00O0O0 ,OO00O0O0O0O00OO0O ,O0O0OO00OO0OOO00O ,OOO000O0OOO0O00OO )#line:252
                            with OOO000O00OO0OOO0O .lock :#line:253
                                OOO000O00OO0OOO0O .proxy .remove (OOOO0OO0OO0OOO00O )#line:254
        return await OOO000O00OO0OOO0O .retry_with_backoff (lambda :OO0OO0O0O0O00OO0O (O0O0O00OOO00000OO ),3 ,'H5st_Api')#line:256
    async def Result (O00O0O000O0000OOO ,O0OO0O0O0OO000000 ,OOO0O000O0O0OO0O0 ,O00OO00000O0O0OO0 ):#line:258
        if O00O0O000O0000OOO .exit_condition and len (O00O0O000O0000OOO .power_success )>=O00O0O000O0000OOO .exit_condition :#line:259
            sys .exit ()#line:260
        async def OOO00OOOOO0O0000O ():#line:262
            O0OOOOOO0O00O00O0 =False #line:263
            if O00O0O000O0000OOO .verify_result !=True :#line:264
                O00O0O000O0000OOO .log .error ("授权未通过 退出")#line:265
                sys .exit ()#line:266
            for O00O000O0O000OO00 in O00O0O000O0000OOO .linkId :#line:267
                O000OO0OO00OOOO0O =await O00O0O000O0000OOO .Get_H5_Api ("inviteFissionhelp",{'linkId':O00O000O0O000OO00 ,"isJdApp":True ,'inviter':OOO0O000O0O0OO0O0 },O00OO00000O0O0OO0 ,'c5389')#line:270
                if int (O000OO0OO00OOOO0O ['code'])==0 :#line:271
                    for OO000OOO0OOO00O0O ,O0O0O0OOOOOOO00OO in O00O0O000O0000OOO .helpResult :#line:272
                        if O000OO0OO00OOOO0O ['data']['helpResult']==int (OO000OOO0OOO00O0O ):#line:273
                            O0OOOOOO0O00O00O0 =True #line:274
                            O00O0O000O0000OOO .log .info (f"Id:{O00O000O0O000OO00[:4] + '****' + O00O000O0O000OO00[-4:]}|助理:{O000OO0OO00OOOO0O['data']['nickName']}|{O000OO0OO00OOOO0O['data']['helpResult']}|第{O0OO0O0O0OO000000}次|{O00O0O000O0000OOO.pt_pin(O00OO00000O0O0OO0)}|{O0O0O0OOOOOOO00OO}")#line:276
                            if O000OO0OO00OOOO0O ['data']['helpResult']==1 :#line:277
                                O00O0O000O0000OOO .power_success .append (O00OO00000O0O0OO0 )#line:278
                            else :#line:279
                                O00O0O000O0000OOO .power_failure .append (O00OO00000O0O0OO0 )#line:280
                    if not O0OOOOOO0O00O00O0 :#line:281
                        O0O0O0OOOOOOO00OO ='❌未知状态 (可能是活动未开启！！！)'#line:282
                        O00O0O000O0000OOO .power_failure .append (O00OO00000O0O0OO0 )#line:283
                        O00O0O000O0000OOO .log .info (f"Id:{O00O000O0O000OO00[:4] + '****' + O00O000O0O000OO00[-4:]}|助理:{O000OO0OO00OOOO0O['data']['nickName']}|{O000OO0OO00OOOO0O['data']['helpResult']}|第{O0OO0O0O0OO000000}次|{O00O0O000O0000OOO.pt_pin(O00OO00000O0O0OO0)}|{O0O0O0OOOOOOO00OO}")#line:285
                else :#line:286
                    O00O0O000O0000OOO .log .info (f"{O00O0O000O0000OOO.pt_pin(O00OO00000O0O0OO0)}{O000OO0OO00OOOO0O['code']} 结果:💔{O000OO0OO00OOOO0O['errMsg']}")#line:287
                    O00O0O000O0000OOO .not_log .append (O00OO00000O0O0OO0 )#line:288
        return await O00O0O000O0000OOO .retry_with_backoff (OOO00OOOOO0O0000O ,3 ,'Result')#line:290
    async def main (OO0O000OOO0O0O00O ):#line:292
        await OO0O000OOO0O0O00O .verify ()#line:293
        await OO0O000OOO0O0O00O .LinkId ()#line:294
        if OO0O000OOO0O0O00O .verify_result !=True :#line:295
            await OO0O000OOO0O0O00O .verify ()#line:296
        if OO0O000OOO0O0O00O .verify_result !=True :#line:297
            OO0O000OOO0O0O00O .log .error ("授权未通过 退出")#line:298
            sys .exit ()#line:299
        for O0OOOOOOO0O0O0O00 in OO0O000OOO0O0O00O .linkId :#line:300
            O0O0O00000000OO0O =await OO0O000OOO0O0O00O .Get_H5_Api ("inviteFissionhelp",{'linkId':O0OOOOOOO0O0O0O00 ,"isJdApp":True ,'inviter':OO0O000OOO0O0O00O .inviter_help },OO0O000OOO0O0O00O .coookie ,'c5389')#line:303
            if O0O0O00000000OO0O ['success']==False and O0O0O00000000OO0O ['code']==1000 :#line:304
                OO0O000OOO0O0O00O .log .info (f"{O0O0O00000000OO0O['errMsg']}")#line:305
                sys .exit ()#line:306
            if O0O0O00000000OO0O ['data']['helpResult']==1 :#line:307
                OO0O000OOO0O0O00O .log .info (f'{OO0O000OOO0O0O00O.pt_pin(OO0O000OOO0O0O00O.coookie)} ✅助力作者成功 谢谢你 你是个好人！！！')#line:308
            else :#line:309
                OO0O000OOO0O0O00O .log .info (f'{OO0O000OOO0O0O00O.pt_pin(OO0O000OOO0O0O00O.coookie)} ❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:310
        if OO0O000OOO0O0O00O .inviter ==False :#line:312
            for O0OOOOOOO0O0O0O00 in OO0O000OOO0O0O00O .linkId :#line:313
                O0O0O00000000OO0O =await OO0O000OOO0O0O00O .Get_H5_Api ('inviteFissionHome',{'linkId':O0OOOOOOO0O0O0O00 ,"inviter":"",},OO0O000OOO0O0O00O .coookie ,'af89e')#line:315
                OO0O000OOO0O0O00O .log .info (f'{OO0O000OOO0O0O00O.pt_pin(OO0O000OOO0O0O00O.coookie)} ⏰剩余时间:{OO0O000OOO0O0O00O.convert_ms_to_hours_minutes(O0O0O00000000OO0O["data"]["countDownTime"])} 🎉已获取助力:{O0O0O00000000OO0O["data"]["prizeNum"] + O0O0O00000000OO0O["data"]["drawPrizeNum"]}次 ✅【LinkId】:{O0OOOOOOO0O0O0O00}')#line:317
                OO0O000OOO0O0O00O .inviter =O0O0O00000000OO0O ["data"]["inviter"]#line:318
            OO0O000OOO0O0O00O .log .info (f'{OO0O000OOO0O0O00O.pt_pin(OO0O000OOO0O0O00O.coookie)} ✅助理码: {OO0O000OOO0O0O00O.inviter}')#line:319
        if OO0O000OOO0O0O00O .proxy !=False :#line:321
            OO0O000OOO0O0O00O .log .info (f"##############开始并发[线程数:{OO0O000OOO0O0O00O.semaphore._value}]##############")#line:322
            O0O0O0O0000OOOOO0 =[]#line:323
            async def OO00OO0OO00O000O0 (O0O0O0OO000000O00 ,O0OO0O0OOO0OOO0O0 ):#line:331
                async with OO0O000OOO0O0O00O .semaphore :#line:332
                    OO00O0OOOO0O0000O =asyncio .create_task (OO0O000OOO0O0O00O .Result (O0O0O0OO000000O00 ,OO0O000OOO0O0O00O .inviter ,O0OO0O0OOO0OOO0O0 ))#line:333
                    if OO0O000OOO0O0O00O .exit_condition and len (OO0O000OOO0O0O00O .power_success )>=OO0O000OOO0O0O00O .exit_condition :#line:334
                        sys .exit ()#line:335
                    return await OO00O0OOOO0O0000O #line:336
            async def OO0O0OO0000O0000O ():#line:338
                O0O00O00OO0O0OOOO =[]#line:339
                for O0OO0OO00OOOO0000 ,OO0OOOOOO0OO0O0O0 in enumerate (ck ,1 ):#line:340
                    if OO0O000OOO0O0O00O .exit_condition and len (OO0O000OOO0O0O00O .power_success )>=OO0O000OOO0O0O00O .exit_condition :#line:341
                        sys .exit ()#line:342
                    OOO00OO00O0OOO000 =asyncio .create_task (OO00OO0OO00O000O0 (O0OO0OO00OOOO0000 ,OO0OOOOOO0OO0O0O0 ))#line:343
                    O0O00O00OO0O0OOOO .append (OOO00OO00O0OOO000 )#line:344
                await asyncio .gather (*O0O00O00OO0O0OOOO )#line:346
            await OO0O0OO0000O0000O ()#line:349
        else :#line:355
            OO0O000OOO0O0O00O .log .info (f"##############开始任务##############")#line:356
            for O00OOOOO00O000000 ,OOO0O000O0O0OOO00 in enumerate (ck ,1 ):#line:357
                await OO0O000OOO0O0O00O .Result (O00OOOOO00O000000 ,OO0O000OOO0O0O00O .inviter ,OOO0O000O0O0OOO00 )#line:358
                if OO0O000OOO0O0O00O .exit_condition and len (OO0O000OOO0O0O00O .power_success )>=OO0O000OOO0O0O00O .exit_condition :#line:359
                    sys .exit ()#line:360
                await asyncio .sleep (0.5 )#line:361
        OO0O000OOO0O0O00O .log .info (f"##############清点人数##############")#line:363
        OO0O000OOO0O0O00O .log .info (f"✅助力成功:{len(OO0O000OOO0O0O00O.power_success)}人 ❌助力失败:{len(OO0O000OOO0O0O00O.power_failure)}人 💔未登录CK{len(OO0O000OOO0O0O00O.not_log)}人")#line:365
        OO0O000OOO0O0O00O .log .info (f" ⏰耗时:{time.time() - OO0O000OOO0O0O00O.start}")#line:366
if __name__ =='__main__':#line:369
    pdd =TEN_JD_PDD ()#line:370
    loop =asyncio .get_event_loop ()#line:371
    loop .run_until_complete (pdd .main ())#line:372
    loop .close ()#line:373
