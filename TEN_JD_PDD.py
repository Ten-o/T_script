#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: TEN_JD_PDD.py(邀好友赢现金-助理)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-助理');
"""
from utils .logger import setup_logger #line:11
from utils .X_API_EID_TOKEN import *#line:12
from utils .User_agent import generate_random_user_agent #line:13
import asyncio ,aiohttp ,re ,os ,sys ,threading ,concurrent .futures ,time ,json #line:14
from utils .jdCookie import get_cookies #line:15
try :#line:17
    ck =get_cookies ()#line:18
    if not ck :#line:19
        sys .exit ()#line:20
except :#line:21
    print ("未获取到有效COOKIE,退出程序！")#line:22
    sys .exit ()#line:23
class TEN_JD_PDD :#line:25
    def __init__ (OO0000O000O0OO0OO ):#line:26
        OO0000O000O0OO0OO .log =setup_logger ()#line:27
        OO0000O000O0OO0OO .start =time .time ()#line:28
        OO0000O000O0OO0OO .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else ''#line:30
        OO0000O000O0OO0OO .inviter =os .environ .get ("TEN_inviter")if os .environ .get ("TEN_inviter")else False #line:31
        OO0000O000O0OO0OO .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:32
        OO0000O000O0OO0OO .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:33
        OO0000O000O0OO0OO .semaphore =asyncio .Semaphore (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 3 )#line:34
        OO0000O000O0OO0OO .power_success =[]#line:35
        OO0000O000O0OO0OO .power_failure =[]#line:36
        OO0000O000O0OO0OO .not_log =[]#line:37
        OO0000O000O0OO0OO .exit_event =threading .Event ()#line:38
        OO0000O000O0OO0OO .coookie =ck [0 ]#line:39
        OO0000O000O0OO0OO .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:46
        OO0000O000O0OO0OO .verify_result = False #line:47
        OO0000O000O0OO0OO .linkId =[]#line:48
        OO0000O000O0OO0OO .inviter_help =''#line:49
        OO0000O000O0OO0OO .version ='1.3.0'#line:50
    def pt_pin (O0OOOOO0OO0OOOOOO ,OOOOO000O0000OO00 ):#line:52
        try :#line:53
            O00O0O000O00O000O =re .compile (r'pt_pin=(.*?);').findall (OOOOO000O0000OO00 )[0 ]#line:54
            O00O0O000O00O000O =unquote_plus (O00O0O000O00O000O )#line:55
        except IndexError :#line:56
            O00O0O000O00O000O =re .compile (r'pin=(.*?);').findall (OOOOO000O0000OO00 )[0 ]#line:57
            O00O0O000O00O000O =unquote_plus (O00O0O000O00O000O )#line:58
        return O00O0O000O00O000O #line:59
    def convert_ms_to_hours_minutes (OOOOOOO000OO0O0O0 ,OO00O00000OOOO0O0 ):#line:60
        O000O0O00000O0OO0 =OO00O00000OOOO0O0 //1000 #line:61
        OO0OO0OO0O0O0000O ,O000O0O00000O0OO0 =divmod (O000O0O00000O0OO0 ,60 )#line:62
        O0OO0OOO0O00OOOO0 ,OO0OO0OO0O0O0000O =divmod (OO0OO0OO0O0O0000O ,60 )#line:63
        return f'{O0OO0OOO0O00OOOO0}:{OO0OO0OO0O0O0000O}'#line:64
    def list_of_groups (OO00O00000OO0O000 ,OOO0O0O0O0000000O ,OOO0OOO0OO00O00OO ):#line:66
        OO000O0OOOO00OO00 =zip (*(iter (OOO0O0O0O0000000O ),)*OOO0OOO0OO00O00OO )#line:67
        O00OO0OOO00OOOO0O =[list (OO00O0O00O0O0OOOO )for OO00O0O00O0O0OOOO in OO000O0OOOO00OO00 ]#line:68
        OO000O00O0OO000OO =len (OOO0O0O0O0000000O )%OOO0OOO0OO00O00OO #line:69
        O00OO0OOO00OOOO0O .append (OOO0O0O0O0000000O [-OO000O00O0OO000OO :])if OO000O00O0OO000OO !=0 else O00OO0OOO00OOOO0O #line:70
        return O00OO0OOO00OOOO0O #line:71
    async def retry_with_backoff (OOO0O0000OO00O00O ,OO0000O00O000OO00 ,OOO0O00OOOO0000O0 ,OOO0O0O0OOOOO0O00 ,backoff_seconds =2 ):#line:73
        for OO0O00O00O0O00O0O in range (OOO0O00OOOO0000O0 ):#line:75
            try :#line:76
                return await OO0000O00O000OO00 ()#line:77
            except asyncio .TimeoutError :#line:78
                OOO0O0000OO00O00O .log .debug (f'第{OO0O00O00O0O00O0O + 1}次重试  {OOO0O0O0OOOOO0O00} 请求超时')#line:79
                await asyncio .sleep (backoff_seconds )#line:80
            except Exception as OOOOOOOOOO00O0OO0 :#line:81
                OOO0O0000OO00O00O .log .debug (f'第{OO0O00O00O0O00O0O + 1}次重试 {OOO0O0O0OOOOO0O00}出错：{OOOOOOOOOO00O0OO0}')#line:82
                await asyncio .sleep (backoff_seconds )#line:83
                if OO0O00O00O0O00O0O ==OOO0O00OOOO0000O0 :#line:84
                    OOO0O0000OO00O00O .log .error (f'{OOO0O0O0OOOOO0O00}重试{OOO0O00OOOO0000O0}次后仍然发生异常')#line:85
                    return #line:86
    async def verify (OO00OOO0O00O0OO0O ):#line:88
        async def O000OOOOO00O00000 ():#line:89
            O00O0OO0OO0OOOO0O ='https://api.ixu.cc/verify'#line:90
            async with aiohttp .ClientSession ()as O0OOOOO000O00OO0O :#line:91
                async with O0OOOOO000O00OO0O .get (O00O0OO0OO0OOOO0O ,data ={'TOKEN':OO00OOO0O00O0OO0O .token },timeout =3 )as O0O00O0O00OOOOOOO :#line:92
                    O0OO00O000O00OOOO =await O0O00O0O00OOOOOOO .json ()#line:93
                    if O0O00O0O00OOOOOOO .status ==200 :#line:94
                        OO00OOO0O00O0OO0O .verify_result =True #line:95
                        OO00OOO0O00O0OO0O .log .info (f'认证通过 UserId：{O0OO00O000O00OOOO["user_id"]}')#line:96
                        return O0OO00O000O00OOOO #line:97
                    else :#line:98
                        OO00OOO0O00O0OO0O .log .error (f"授权未通过:{O0OO00O000O00OOOO['error']}")#line:99
                        sys .exit ()#line:100
        return await OO00OOO0O00O0OO0O .retry_with_backoff (O000OOOOO00O00000 ,3 ,'verify')#line:102
    def is_version_nearby (O000O0OOOOO00OO00 ,OOOOOOOO000OOO0OO ,OO000OOOO000OO0O0 ,threshold =3 ):#line:104
        try :#line:105
            OOOO00OO0OO0O00OO =list (map (int ,OOOOOOOO000OOO0OO .split ('.')))#line:106
            O0000OO0O00O0OOOO =list (map (int ,OO000OOOO000OO0O0 .split ('.')))#line:107
            if len (OOOO00OO0OO0O00OO )!=len (O0000OO0O00O0OOOO ):#line:109
                return False #line:110
            for OO00OOO0OO0OOOOO0 ,O000OOOO00O00O0O0 in zip (OOOO00OO0OO0O00OO ,O0000OO0O00O0OOOO ):#line:112
                if abs (OO00OOO0OO0OOOOO0 -O000OOOO00O00O0O0 )>threshold :#line:113
                    return False #line:114
            return True #line:116
        except ValueError :#line:117
            return False #line:118
    async def LinkId (OO0OO00O0O00OO00O ):#line:120
        async def O0000OO000OOOOO00 ():#line:121
            if OO0OO00O0O00OO00O .verify_result !=True :#line:122
                await OO0OO00O0O00OO00O .verify ()#line:123
            if OO0OO00O0O00OO00O .verify_result !=True :#line:124
                OO0OO00O0O00OO00O .log .error ("授权未通过 退出")#line:125
                sys .exit ()#line:126
            O0O0000O00OOOO0OO ='https://api.ixu.cc/status/inviter.json'#line:127
            async with aiohttp .ClientSession ()as OOOOO000OOO0000OO :#line:128
                async with OOOOO000OOO0000OO .get (O0O0000O00OOOO0OO ,params ={'TOKEN':OO0OO00O0O00OO00O .token },timeout =3 )as O0O0O00OOO00OOOO0 :#line:129
                    if O0O0O00OOO00OOOO0 .status ==200 :#line:130
                        OO00OOO0OO0000000 =await O0O0O00OOO00OOOO0 .json ()#line:131
                        if OO00OOO0OO0000000 ['stats']!='True':#line:132
                            OO0OO00O0O00OO00O .log .error (f"{OO00OOO0OO0000000['err_text']}")#line:133
                            sys .exit ()#line:134
                        OO0OO00O0O00OO00O .inviter_help =OO00OOO0OO0000000 ['inviter']#line:135
                        if OO0OO00O0O00OO00O .is_version_nearby (OO00OOO0OO0000000 ['version'],OO0OO00O0O00OO00O .version )!=True :#line:136
                            OO0OO00O0O00OO00O .log .error (f'云端版本:{OO00OOO0OO0000000["version"]},当前版本:{OO0OO00O0O00OO00O.version} {OO00OOO0OO0000000["upload_text"]}')#line:137
                            sys .exit ()#line:138
                        if len (OO00OOO0OO0000000 ['text'])>0 :#line:139
                            OO0OO00O0O00OO00O .log .debug (f'那女孩对你说:{OO00OOO0OO0000000["text"]}')#line:140
                        if OO0OO00O0O00OO00O .scode =='ALL'or OO0OO00O0O00OO00O .scode =='all':#line:141
                            for OOO0OO0OO00000O00 in OO00OOO0OO0000000 ['linkId']:#line:142
                                OO0OO00O0O00OO00O .linkId .append (OOO0OO0OO00000O00 )#line:143
                                OO0OO00O0O00OO00O .log .info (f'云端获取到linkId:{OOO0OO0OO00000O00}')#line:144
                            return True #line:145
                        else :#line:146
                            OO0OO00O0O00OO00O .linkId .append (OO00OOO0OO0000000 ['linkId'][int (OO0OO00O0O00OO00O .scode )-1 ])#line:147
                            OO0OO00O0O00OO00O .log .info (f'云端获取到linkId:{OO00OOO0OO0000000["linkId"][int(OO0OO00O0O00OO00O.scode) - 1]}')#line:148
                            return True #line:149
                    else :#line:150
                        OO0OO00O0O00OO00O .log .error ('未获取到linkId 重试')#line:151
        return await OO0OO00O0O00OO00O .retry_with_backoff (O0000OO000OOOOO00 ,3 ,'linkId')#line:152
    async def Get_H5st (O000OOO0OO00OO0O0 ,O0OO0OOOO000OOOO0 ,O00OOO00O00OOOOO0 ,OOO0O00O000O000OO ,O000O0000O0O000OO ,OOO0O0000O0OO00OO ):#line:157
        async def O0O0O0OO0OO0O00O0 ():#line:158
            if O000OOO0OO00OO0O0 .verify_result !=True :#line:159
                O000OOO0OO00OO0O0 .log .error ("授权未通过 退出")#line:160
                sys .exit ()#line:161
            O0000OOOOO0O0O0O0 ='https://api.ouklc.com/api/h5st'#line:162
            OOO0O00OO000O00O0 =O000OOO0OO00OO0O0 .pt_pin (OOO0O0000O0OO00OO )#line:163
            OO00OOO00OOOOO000 ={'functionId':O0OO0OOOO000OOOO0 ,'body':json .dumps (O00OOO00O00OOOOO0 ),'ua':OOO0O00O000O000OO ,'pin':OOO0O00OO000O00O0 ,'appId':O000O0000O0O000OO }#line:170
            async with aiohttp .ClientSession ()as OOOOOO00O0O00OO00 :#line:172
                async with OOOOOO00O0O00OO00 .get (O0000OOOOO0O0O0O0 ,params =OO00OOO00OOOOO000 ,timeout =10 )as OO00OO0O0OO0OOO00 :#line:173
                    if OO00OO0O0OO0OOO00 .status ==200 :#line:174
                        OO00O000O0OO0O0OO =await OO00OO0O0OO0OOO00 .json ()#line:175
                        return OO00O000O0OO0O0OO ['body']#line:176
                    else :#line:177
                        return await O000OOO0OO00OO0O0 .retry_with_backoff (O0O0O0OO0OO0O00O0 ,3 ,'H5st')#line:178
        return await O000OOO0OO00OO0O0 .retry_with_backoff (O0O0O0OO0OO0O00O0 ,3 ,'H5st')#line:180
    async def Get_H5_Api (OO00O0O00000OOO0O ,OOOO0000OOO00O00O ,OO0O000O0OOOO0O0O ,OO00OOOOOOOOO0OO0 ,O0OOO0O0OOO000OO0 ):#line:184
            async def O0OOO0000000OOOO0 (O00OO0O0O000O00O0 ):#line:185
                if OO00O0O00000OOO0O .verify_result !=True :#line:186
                    OO00O0O00000OOO0O .log .error ("授权未通过 退出")#line:187
                    sys .exit ()#line:188
                O00OO00O0000000OO =generate_random_user_agent ()#line:189
                O00O0OOO00O00OO0O ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/","Origin":"https://prodev.m.jd.com","Cookie":OO00OOOOOOOOO0OO0 ,"User-Agent":O00OO00O0000000OO }#line:201
                O0000000O0000OO0O =getUUID ("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")#line:202
                O00OO0O0O000O00O0 =await OO00O0O00000OOO0O .Get_H5st (OOOO0000OOO00O00O ,O00OO0O0O000O00O0 ,O00OO00O0000000OO ,O0OOO0O0OOO000OO0 ,OO00OOOOOOOOO0OO0 )#line:203
                O00000O00OO0OOO00 =str (O00OO0O0O000O00O0 )+"&x-api-eid-token="+cache_eid_token ()+f"&uuid={O0000000O0000OO0O}&"#line:204
                OOOO0OOO0000OO00O ="https://api.m.jd.com"#line:205
                async with aiohttp .ClientSession ()as OOO0OOO00O0OO0000 :#line:206
                    if OO00O0O00000OOO0O .proxy ==False :#line:207
                        async with OOO0OOO00O0OO0000 .post (OOOO0OOO0000OO00O ,headers =O00O0OOO00O00OO0O ,data =O00000O00OO0OOO00 ,timeout =5 )as O0OOOOO0OO00O00OO :#line:208
                            if O0OOOOO0OO00O00OO .status ==200 :#line:209
                                return await O0OOOOO0OO00O00OO .json ()#line:210
                            else :#line:211
                                OO00O0O00000OOO0O .log .error (f'重试 请求结果：{O0OOOOO0OO00O00OO.status}')#line:212
                    else :#line:214
                        async with OOO0OOO00O0OO0000 .post (OOOO0OOO0000OO00O ,headers =O00O0OOO00O00OO0O ,data =O00000O00OO0OOO00 ,timeout =5 ,proxy =OO00O0O00000OOO0O .proxy )as O0OOOOO0OO00O00OO :#line:215
                            if O0OOOOO0OO00O00OO .status ==200 :#line:216
                                return await O0OOOOO0OO00O00OO .json ()#line:217
                            else :#line:218
                                OO00O0O00000OOO0O .log .error (f'重试 请求结果：{O0OOOOO0OO00O00OO.status}')#line:219
                                await OO00O0O00000OOO0O .Get_H5_Api (OOOO0000OOO00O00O ,O00000O00OO0OOO00 ,OO00OOOOOOOOO0OO0 ,O0OOO0O0OOO000OO0 )#line:220
            return await OO00O0O00000OOO0O .retry_with_backoff (lambda :O0OOO0000000OOOO0 (OO0O000O0OOOO0O0O ),3 ,'H5st_Api')#line:222
    async def Result (O0O0OOOOOOOOO0000 ,O000000OOOO0OOOOO ,OO0OOO00O0OOO0O00 ):#line:224
        async def O0O000O0O0O0O0OOO ():#line:225
                if O0O0OOOOOOOOO0000 .verify_result !=True :#line:226
                    O0O0OOOOOOOOO0000 .log .error ("授权未通过 退出")#line:227
                    sys .exit ()#line:228
                for O0000OOO000OO0OO0 in O0O0OOOOOOOOO0000 .linkId :#line:229
                    O00O0O0O0O0O0O0OO =await O0O0OOOOOOOOO0000 .Get_H5_Api ("inviteFissionBeforeHome",{'linkId':O0000OOO000OO0OO0 ,"isJdApp":True ,'inviter':O000000OOOO0OOOOO },OO0OOO00O0OOO0O00 ,'02f8d')#line:230
                    if int (O00O0O0O0O0O0O0OO ['code'])==0 :#line:231
                        for O0OO000OO000000OO ,O0O0000OOOOOO0O00 in O0O0OOOOOOOOO0000 .helpResult :#line:232
                            if O00O0O0O0O0O0O0OO ['data']['helpResult']==int (O0OO000OO000000OO ):#line:233
                                O000OOOO00000OO0O =True #line:234
                                O0O0OOOOOOOOO0000 .log .info (f"{O0O0OOOOOOOOO0000.pt_pin(OO0OOO00O0OOO0O00)} linkId:{O0000OOO000OO0OO0} 助理:{O00O0O0O0O0O0O0OO['data']['nickName']} 结果:{O00O0O0O0O0O0O0OO['data']['helpResult']} {O0O0000OOOOOO0O00}")#line:235
                                if O00O0O0O0O0O0O0OO ['data']['helpResult']==1 :#line:236
                                    O0O0OOOOOOOOO0000 .power_success .append (OO0OOO00O0OOO0O00 )#line:237
                                else :#line:238
                                    O0O0OOOOOOOOO0000 .power_failure .append (OO0OOO00O0OOO0O00 )#line:239
                        if not O000OOOO00000OO0O :#line:240
                            O0O0000OOOOOO0O00 ='❌未知状态 (可能是活动未开启！！！)'#line:241
                            O0O0OOOOOOOOO0000 .power_failure .append (OO0OOO00O0OOO0O00 )#line:242
                            O0O0OOOOOOOOO0000 .log .info (f"{O0O0OOOOOOOOO0000.pt_pin(OO0OOO00O0OOO0O00)} linkId:{O0000OOO000OO0OO0} 助理:{O00O0O0O0O0O0O0OO['data']['nickName']} 结果:{O00O0O0O0O0O0O0OO['data']['helpResult']} {O0O0000OOOOOO0O00}")#line:243
                    else :#line:244
                        O0O0OOOOOOOOO0000 .log .info (f"{O0O0OOOOOOOOO0000.pt_pin(OO0OOO00O0OOO0O00)}{O00O0O0O0O0O0O0OO['code']} 结果:💔{O00O0O0O0O0O0O0OO['errMsg']}")#line:245
                        O0O0OOOOOOOOO0000 .not_log .append (OO0OOO00O0OOO0O00 )#line:246
        return await O0O0OOOOOOOOO0000 .retry_with_backoff (O0O000O0O0O0O0OOO ,3 ,'Result')#line:247
    async def main (OOO00000O0O0OOO0O ):#line:250
        await OOO00000O0O0OOO0O .verify ()#line:251
        await OOO00000O0O0OOO0O .LinkId ()#line:252
        if OOO00000O0O0OOO0O .verify_result !=True :#line:253
            await OOO00000O0O0OOO0O .verify ()#line:254
        if OOO00000O0O0OOO0O .verify_result !=True :#line:255
            OOO00000O0O0OOO0O .log .error ("授权未通过 退出")#line:256
            sys .exit ()#line:257
        for OO000O0OO0OO0O000 in OOO00000O0O0OOO0O .linkId :#line:258
            OO0O00000O00OO000 =await OOO00000O0O0OOO0O .Get_H5_Api ("inviteFissionBeforeHome",{'linkId':OO000O0OO0OO0O000 ,"isJdApp":True ,'inviter':OOO00000O0O0OOO0O .inviter_help },OOO00000O0O0OOO0O .coookie ,'02f8d')#line:261
        if OO0O00000O00OO000 ['success']==False and OO0O00000O00OO000 ['code']==1000 :#line:262
            OOO00000O0O0OOO0O .log .info (f"{OO0O00000O00OO000['errMsg']}")#line:263
            sys .exit ()#line:264
        if OO0O00000O00OO000 ['data']['helpResult']==1 :#line:265
            OOO00000O0O0OOO0O .log .info (f'{OOO00000O0O0OOO0O.pt_pin(OOO00000O0O0OOO0O.coookie)}✅助力作者成功 谢谢你 你是个好人！！！')#line:266
        else :#line:267
            OOO00000O0O0OOO0O .log .info (f'{OOO00000O0O0OOO0O.pt_pin(OOO00000O0O0OOO0O.coookie)}❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:268
        if OOO00000O0O0OOO0O .inviter ==False :#line:270
            OO0O00000O00OO000 =await OOO00000O0O0OOO0O .Get_H5_Api ('inviteFissionHome',{'linkId':OOO00000O0O0OOO0O .linkId [0 ],"inviter":"",},OOO00000O0O0OOO0O .coookie ,'af89e')#line:271
            OOO00000O0O0OOO0O .log .info (f'{OOO00000O0O0OOO0O.pt_pin(OOO00000O0O0OOO0O.coookie)}⏰剩余时间:{OOO00000O0O0OOO0O.convert_ms_to_hours_minutes(OO0O00000O00OO000["data"]["countDownTime"])} 🎉已获取助力:{OO0O00000O00OO000["data"]["prizeNum"] + OO0O00000O00OO000["data"]["drawPrizeNum"]}次 ✅【助力码】:{OO0O00000O00OO000["data"]["inviter"]}')#line:272
            OOO00000O0O0OOO0O .inviter =OO0O00000O00OO000 ["data"]["inviter"]#line:273
        if OOO00000O0O0OOO0O .proxy !=False :#line:274
            OOO00000O0O0OOO0O .log .info (f"##############开始并发##############")#line:275
            OO00OOOO0O0OOOOOO =[]#line:276
            for OO0OOOOO000OO00OO ,OO0OOO00000OOO0OO in enumerate (ck ,1 ):#line:277
                async with OOO00000O0O0OOO0O .semaphore :#line:278
                    O00O00OO000O00O0O =asyncio .create_task (OOO00000O0O0OOO0O .Result (OOO00000O0O0OOO0O .inviter ,OO0OOO00000OOO0OO ))#line:279
                    OO00OOOO0O0OOOOOO .append (O00O00OO000O00O0O )#line:280
            await asyncio .gather (*OO00OOOO0O0OOOOOO )#line:282
        else :#line:283
            OOO00000O0O0OOO0O .log .info (f"##############开始任务##############")#line:284
            for OO0OOOOO000OO00OO ,OO0OOO00000OOO0OO in enumerate (ck ,1 ):#line:285
                await OOO00000O0O0OOO0O .Result (OOO00000O0O0OOO0O .inviter ,OO0OOO00000OOO0OO )#line:286
                await asyncio.sleep(0.5)

        OOO00000O0O0OOO0O .log .info (f"##############清点人数##############")#line:288
        OOO00000O0O0OOO0O .log .info (f"✅助力成功:{len(OOO00000O0O0OOO0O.power_success)}人 ❌助力失败:{len(OOO00000O0O0OOO0O.power_failure)}人 💔未登录CK{len(OOO00000O0O0OOO0O.not_log)}人")#line:289
        OOO00000O0O0OOO0O .log .info (f" ⏰耗时:{time.time() - OOO00000O0O0OOO0O.start}")#line:290

if __name__ =='__main__':#line:292
    pdd =TEN_JD_PDD ()#line:293
    loop =asyncio .get_event_loop ()#line:294
    loop .run_until_complete (pdd .main ())#line:295
    loop .close ()#line:296
