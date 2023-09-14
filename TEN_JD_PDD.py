#!/usr/bin/env python3
"""
File: TEN_JD_PDD.py(邀好友赢现金-助理)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-助理');
"""
from utils .logger import setup_logger #line:11
from utils .X_API_EID_TOKEN import *#line:12
from utils .User_agent import *#line:13
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
    def __init__ (O00000O00OO00O0O0 ):#line:26
        O00000O00OO00O0O0 .log =setup_logger ()#line:27
        O00000O00OO00O0O0 .start =time .time ()#line:28
        O00000O00OO00O0O0 .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:30
        O00000O00OO00O0O0 .inviter =os .environ .get ("TEN_inviter")if os .environ .get ("TEN_inviter")else False #line:31
        O00000O00OO00O0O0 .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:32
        O00000O00OO00O0O0 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:33
        O00000O00OO00O0O0 .semaphore =asyncio .Semaphore (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 30 )#line:34
        O00000O00OO00O0O0 .power_success =[]#line:35
        O00000O00OO00O0O0 .power_failure =[]#line:36
        O00000O00OO00O0O0 .not_log =[]#line:37
        O00000O00OO00O0O0 .exit_event =threading .Event ()#line:38
        O00000O00OO00O0O0 .coookie =ck [0 ]#line:39
        O00000O00OO00O0O0 .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:46
        O00000O00OO00O0O0 .verify_result =False #line:47
        O00000O00OO00O0O0 .linkId =[]#line:48
        O00000O00OO00O0O0 .inviter_help =''#line:49
        O00000O00OO00O0O0 .version ='1.3.6'#line:50
    def pt_pin (O000000OO0000000O ,O0000OO0OOOOO00OO ):#line:52
        try :#line:53
            OOO00OOO0O000000O =re .compile (r'pt_pin=(.*?);').findall (O0000OO0OOOOO00OO )[0 ]#line:54
            OOO00OOO0O000000O =unquote_plus (OOO00OOO0O000000O )#line:55
        except IndexError :#line:56
            OOO00OOO0O000000O =re .compile (r'pin=(.*?);').findall (O0000OO0OOOOO00OO )[0 ]#line:57
            OOO00OOO0O000000O =unquote_plus (OOO00OOO0O000000O )#line:58
        return OOO00OOO0O000000O #line:59
    def convert_ms_to_hours_minutes (OO00OO0OO0O0OOO0O ,OOO0O0O00OO0OO00O ):#line:60
        O00000OOOO0OOOO0O =OOO0O0O00OO0OO00O //1000 #line:61
        O00O0OOO0OOO00OO0 ,O00000OOOO0OOOO0O =divmod (O00000OOOO0OOOO0O ,60 )#line:62
        O00O000OO0OOO00O0 ,O00O0OOO0OOO00OO0 =divmod (O00O0OOO0OOO00OO0 ,60 )#line:63
        return f'{O00O000OO0OOO00O0}:{O00O0OOO0OOO00OO0}'#line:64
    def list_of_groups (O0O000O00000O000O ,OO0O0OO0O0OO0OOO0 ,OO0O000OOO0OOOOO0 ):#line:66
        O00OOO000OO0OO000 =zip (*(iter (OO0O0OO0O0OO0OOO0 ),)*OO0O000OOO0OOOOO0 )#line:67
        O000000000OOOOOO0 =[list (O0O0O00000O000OOO )for O0O0O00000O000OOO in O00OOO000OO0OO000 ]#line:68
        O0O0O00O0OO0O000O =len (OO0O0OO0O0OO0OOO0 )%OO0O000OOO0OOOOO0 #line:69
        O000000000OOOOOO0 .append (OO0O0OO0O0OO0OOO0 [-O0O0O00O0OO0O000O :])if O0O0O00O0OO0O000O !=0 else O000000000OOOOOO0 #line:70
        return O000000000OOOOOO0 #line:71
    async def retry_with_backoff (OO0O00000OO0O00O0 ,OOOOOOO0OOOO000OO ,O0O0O0O0OO00000OO ,O00000O0OO000O00O ,backoff_seconds =2 ):#line:73
        for OO00O0OO00O00OO00 in range (O0O0O0O0OO00000OO ):#line:75
            try :#line:76
                return await OOOOOOO0OOOO000OO ()#line:77
            except asyncio .TimeoutError :#line:78
                OO0O00000OO0O00O0 .log .debug (f'第{OO00O0OO00O00OO00 + 1}次重试  {O00000O0OO000O00O} 请求超时')#line:79
                await asyncio .sleep (backoff_seconds )#line:80
            except Exception as O0OOO00OO000OO0O0 :#line:81
                OO0O00000OO0O00O0 .log .debug (f'第{OO00O0OO00O00OO00 + 1}次重试 {O00000O0OO000O00O}出错：{O0OOO00OO000OO0O0}')#line:82
                await asyncio .sleep (backoff_seconds )#line:83
                if OO00O0OO00O00OO00 ==O0O0O0O0OO00000OO :#line:84
                    OO0O00000OO0O00O0 .log .error (f'{O00000O0OO000O00O}重试{O0O0O0O0OO00000OO}次后仍然发生异常')#line:85
                    return #line:86
    async def verify (OOOOOOO0OO00OO00O ):#line:88
        async def OOO0O0O0O00OO000O ():#line:89
            OO0OOO000O00O000O ='https://api.ixu.cc/verify'#line:90
            async with aiohttp .ClientSession ()as OO00OO0OO0O00OOOO :#line:91
                async with OO00OO0OO0O00OOOO .get (OO0OOO000O00O000O ,data ={'TOKEN':OOOOOOO0OO00OO00O .token },timeout =3 )as OOOOO000OOOO0000O :#line:92
                    OOOO00O00OOO0O0O0 =await OOOOO000OOOO0000O .json ()#line:93
                    if OOOOO000OOOO0000O .status ==200 :#line:94
                        OOOOOOO0OO00OO00O .verify_result =True #line:95
                        OOOOOOO0OO00OO00O .log .info (f'认证通过 UserId：{OOOO00O00OOO0O0O0["user_id"]}')#line:96
                        return OOOO00O00OOO0O0O0 #line:97
                    else :#line:98
                        OOOOOOO0OO00OO00O .log .error (f"授权未通过:{OOOO00O00OOO0O0O0['error']}")#line:99
                        sys .exit ()#line:100
        return await OOOOOOO0OO00OO00O .retry_with_backoff (OOO0O0O0O00OO000O ,3 ,'verify')#line:102
    def parse_version (OOO0OO00O000O0000 ,O0OOOO00O0O0O00OO ):#line:104
        return list (map (int ,O0OOOO00O0O0O00OO .split ('.')))#line:105
    def is_major_update (O0OO00O00OO000000 ,O0O000OOOOOO0O000 ,O0000OO0OOOOOO00O ):#line:107
        if O0O000OOOOOO0O000 [1 ]!=O0000OO0OOOOOO00O [1 ]:#line:108
            return True #line:109
        elif O0O000OOOOOO0O000 [0 ]!=O0000OO0OOOOOO00O [0 ]:#line:110
            return True #line:111
        else :#line:112
            return False #line:113
    def is_force_update (OOO0O00O0000OO00O ,OOOO0O000O0OOO000 ,O0OO00OOO00OO00OO ):#line:115
        if OOO0O00O0000OO00O .is_major_update (OOOO0O000O0OOO000 ,O0OO00OOO00OO00OO ):#line:116
            return True #line:117
        elif O0OO00OOO00OO00OO [2 ]-OOOO0O000O0OOO000 [2 ]>=3 :#line:118
            return True #line:119
        elif O0OO00OOO00OO00OO [2 ]<OOOO0O000O0OOO000 [2 ]:#line:120
            return True #line:121
        else :#line:122
            return False #line:123
    async def LinkId (O0OO0OOO00O0000O0 ):#line:125
        async def O0OO00OO0OO0O0OO0 ():#line:126
            if O0OO0OOO00O0000O0 .verify_result !=True :#line:127
                await O0OO0OOO00O0000O0 .verify ()#line:128
            if O0OO0OOO00O0000O0 .verify_result !=True :#line:129
                O0OO0OOO00O0000O0 .log .error ("授权未通过 退出")#line:130
                sys .exit ()#line:131
            OOO0OO0O0O0OO0OOO ='https://api.ixu.cc/status/inviter.json'#line:132
            async with aiohttp .ClientSession ()as O000O0O0OO000O000 :#line:133
                async with O000O0O0OO000O000 .get (OOO0OO0O0O0OO0OOO ,params ={'TOKEN':O0OO0OOO00O0000O0 .token },timeout =3 )as O0OOO0O00000000O0 :#line:134
                    if O0OOO0O00000000O0 .status ==200 :#line:135
                        OO00O00O0OO000000 =await O0OOO0O00000000O0 .json ()#line:136
                        if OO00O00O0OO000000 ['stats']!='True':#line:137
                            O0OO0OOO00O0000O0 .log .error (f"{OO00O00O0OO000000['err_text']}")#line:138
                            sys .exit ()#line:139
                        O0OO0OOO00O0000O0 .inviter_help =OO00O00O0OO000000 ['inviter']#line:140
                        if O0OO0OOO00O0000O0 .is_force_update (O0OO0OOO00O0000O0 .parse_version (O0OO0OOO00O0000O0 .version ),O0OO0OOO00O0000O0 .parse_version (OO00O00O0OO000000 ["version"])):#line:141
                            O0OO0OOO00O0000O0 .log .error (f'强制更新 云端版本:{OO00O00O0OO000000["version"]},当前版本:{O0OO0OOO00O0000O0.version} {OO00O00O0OO000000["upload_text"]}')#line:142
                            sys .exit ()#line:143
                        else :#line:144
                            O0OO0OOO00O0000O0 .log .debug (f'云端版本:{OO00O00O0OO000000["version"]},当前版本:{O0OO0OOO00O0000O0.version}')#line:145
                        if len (OO00O00O0OO000000 ['text'])>0 :#line:146
                            O0OO0OOO00O0000O0 .log .debug (f'那女孩对你说:{OO00O00O0OO000000["text"]}')#line:147
                        if O0OO0OOO00O0000O0 .scode =='ALL'or O0OO0OOO00O0000O0 .scode =='all':#line:148
                            for O0O0000OO000O0O00 in OO00O00O0OO000000 ['linkId']:#line:149
                                O0OO0OOO00O0000O0 .linkId .append (O0O0000OO000O0O00 )#line:150
                                O0OO0OOO00O0000O0 .log .info (f'云端获取到linkId:{O0O0000OO000O0O00}')#line:151
                            return True #line:152
                        else :#line:153
                            O0OO0OOO00O0000O0 .linkId .append (OO00O00O0OO000000 ['linkId'][int (O0OO0OOO00O0000O0 .scode )-1 ])#line:154
                            O0OO0OOO00O0000O0 .log .info (f'云端获取到linkId:{OO00O00O0OO000000["linkId"][int(O0OO0OOO00O0000O0.scode) - 1]}')#line:155
                            return True #line:156
                    else :#line:157
                        O0OO0OOO00O0000O0 .log .error ('未获取到linkId 重试')#line:158
        return await O0OO0OOO00O0000O0 .retry_with_backoff (O0OO00OO0OO0O0OO0 ,3 ,'linkId')#line:159
    async def Get_H5st (OOO0OOO0000000OO0 ,O0OOOO0OOOOO0O0O0 ,OOOOOOOO000000OOO ,OO0OO000O000OO00O ,O0O00O0O00OO0O00O ,OOO0OO0O0OO000OO0 ):#line:164
        async def OO00O0O000OOO000O ():#line:165
            if OOO0OOO0000000OO0 .verify_result !=True :#line:166
                OOO0OOO0000000OO0 .log .error ("授权未通过 退出")#line:167
                sys .exit ()#line:168
            O00O0O000OOO0O0O0 ='https://api.ouklc.com/api/h5st'#line:169
            O000O00OO00OO00O0 =OOO0OOO0000000OO0 .pt_pin (OOO0OO0O0OO000OO0 )#line:170
            OO0O0O0OO0O0O0OOO ={'functionId':O0OOOO0OOOOO0O0O0 ,'body':json .dumps (OOOOOOOO000000OOO ),'ua':OO0OO000O000OO00O ,'pin':O000O00OO00OO00O0 ,'appId':O0O00O0O00OO0O00O }#line:177
            async with aiohttp .ClientSession ()as OO0000OOO0O0OOOOO :#line:178
                async with OO0000OOO0O0OOOOO .get (O00O0O000OOO0O0O0 ,params =OO0O0O0OO0O0O0OOO ,timeout =10 )as O000O0OOO0O00O0O0 :#line:179
                    if O000O0OOO0O00O0O0 .status ==200 :#line:180
                        OOO00OOO0O0O0OOOO =await O000O0OOO0O00O0O0 .json ()#line:181
                        return OOO00OOO0O0O0OOOO ['body']#line:183
                    else :#line:184
                        return await OOO0OOO0000000OO0 .retry_with_backoff (OO00O0O000OOO000O ,3 ,'H5st')#line:185
        return await OOO0OOO0000000OO0 .retry_with_backoff (OO00O0O000OOO000O ,3 ,'H5st')#line:187
    async def Get_H5_Api (OOOOOO0OO0O0OO000 ,OO000O00O00O0O0O0 ,O0O0O00OOOOOOO000 ,O000O0OO0OO0OOO0O ,O0OO00OOO00O00O00 ):#line:191
            async def OO0O0O000O0OO00O0 (OO0OOOO00OO00OO00 ):#line:192
                if OOOOOO0OO0O0OO000 .verify_result !=True :#line:193
                    OOOOOO0OO0O0OO000 .log .error ("授权未通过 退出")#line:194
                    sys .exit ()#line:195
                OOOOO0O00000OO0O0 =generate_random_user_agent ()#line:196
                OO00O0000OOO00OO0 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":O000O0OO0OO0OOO0O ,"User-Agent":OOOOO0O00000OO0O0 }#line:208
                OOO00OO0OOOOOO0OO =getUUID ("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")#line:209
                OO0OOOO00OO00OO00 =await OOOOOO0OO0O0OO000 .Get_H5st (OO000O00O00O0O0O0 ,OO0OOOO00OO00OO00 ,OOOOO0O00000OO0O0 ,O0OO00OOO00O00O00 ,O000O0OO0OO0OOO0O )#line:210
                O0O00OOOOO0OOOOO0 ="https://api.m.jd.com"#line:212
                async with aiohttp .ClientSession ()as OO00OOOOO0O0OO0O0 :#line:213
                    if OOOOOO0OO0O0OO000 .proxy ==False :#line:214
                        async with OO00OOOOO0O0OO0O0 .post (O0O00OOOOO0OOOOO0 ,headers =OO00O0000OOO00OO0 ,data =OO0OOOO00OO00OO00 ,timeout =5 )as OO0000O0OO00OOO0O :#line:215
                            if OO0000O0OO00OOO0O .status ==200 :#line:216
                                return await OO0000O0OO00OOO0O .json ()#line:217
                            else :#line:219
                                OOOOOO0OO0O0OO000 .log .error (f'重试 请求结果：{OO0000O0OO00OOO0O.status}')#line:220
                    else :#line:221
                        async with OO00OOOOO0O0OO0O0 .post (O0O00OOOOO0OOOOO0 ,headers =OO00O0000OOO00OO0 ,data =OO0OOOO00OO00OO00 ,timeout =5 ,proxy =OOOOOO0OO0O0OO000 .proxy )as OO0000O0OO00OOO0O :#line:222
                            if OO0000O0OO00OOO0O .status ==200 :#line:223
                                return await OO0000O0OO00OOO0O .json ()#line:224
                            else :#line:225
                                OOOOOO0OO0O0OO000 .log .error (f'重试 请求结果：{OO0000O0OO00OOO0O.status}')#line:226
                                await OOOOOO0OO0O0OO000 .Get_H5_Api (OO000O00O00O0O0O0 ,OO0OOOO00OO00OO00 ,O000O0OO0OO0OOO0O ,O0OO00OOO00O00O00 )#line:227
            return await OOOOOO0OO0O0OO000 .retry_with_backoff (lambda :OO0O0O000O0OO00O0 (O0O0O00OOOOOOO000 ),3 ,'H5st_Api')#line:229
    async def Result (OOOOO0OOO00O0OO00 ,OO000O0O0OO000OOO ,OO0000O000OO00OO0 ,OOOOOO0O0OO0OO0O0 ):#line:231
        async def OO0O000OOO0O00OO0 ():#line:232
            OOOO0O000OOO0O0O0 =False #line:233
            if OOOOO0OOO00O0OO00 .verify_result !=True :#line:234
                OOOOO0OOO00O0OO00 .log .error ("授权未通过 退出")#line:235
                sys .exit ()#line:236
            for OOOO0O00O000O000O in OOOOO0OOO00O0OO00 .linkId :#line:237
                O0O0O000O00OO0000 =await OOOOO0OOO00O0OO00 .Get_H5_Api ("inviteFissionBeforeHome",{'linkId':OOOO0O00O000O000O ,"isJdApp":True ,'inviter':OO0000O000OO00OO0 },OOOOOO0O0OO0OO0O0 ,'02f8d')#line:238
                if int (O0O0O000O00OO0000 ['code'])==0 :#line:239
                    for O0000OOOOOOOOO00O ,O00OO0OOOO0OO0O00 in OOOOO0OOO00O0OO00 .helpResult :#line:240
                        if O0O0O000O00OO0000 ['data']['helpResult']==int (O0000OOOOOOOOO00O ):#line:241
                            OOOO0O000OOO0O0O0 =True #line:242
                            OOOOO0OOO00O0OO00 .log .info (f"第{OO000O0O0OO000OOO}次 Id:{OOOO0O00O000O000O} 助理:{O0O0O000O00OO0000['data']['nickName']}|{O0O0O000O00OO0000['data']['helpResult']}|{OOOOO0OOO00O0OO00.pt_pin(OOOOOO0O0OO0OO0O0)}|{O00OO0OOOO0OO0O00}")#line:243
                            if O0O0O000O00OO0000 ['data']['helpResult']==1 :#line:244
                                OOOOO0OOO00O0OO00 .power_success .append (OOOOOO0O0OO0OO0O0 )#line:245
                            else :#line:246
                                OOOOO0OOO00O0OO00 .power_failure .append (OOOOOO0O0OO0OO0O0 )#line:247
                    if not OOOO0O000OOO0O0O0 :#line:248
                        O00OO0OOOO0OO0O00 ='❌未知状态 (可能是活动未开启！！！)'#line:249
                        OOOOO0OOO00O0OO00 .power_failure .append (OOOOOO0O0OO0OO0O0 )#line:250
                        OOOOO0OOO00O0OO00 .log .info (f"第{OO000O0O0OO000OOO}次 Id:{OOOO0O00O000O000O} 助理:{O0O0O000O00OO0000['data']['nickName']}|{O0O0O000O00OO0000['data']['helpResult']}|{OOOOO0OOO00O0OO00.pt_pin(OOOOOO0O0OO0OO0O0)}|{O00OO0OOOO0OO0O00}")#line:251
                else :#line:252
                    OOOOO0OOO00O0OO00 .log .info (f"{OOOOO0OOO00O0OO00.pt_pin(OOOOOO0O0OO0OO0O0)}{O0O0O000O00OO0000['code']} 结果:💔{O0O0O000O00OO0000['errMsg']}")#line:253
                    OOOOO0OOO00O0OO00 .not_log .append (OOOOOO0O0OO0OO0O0 )#line:254
        return await OOOOO0OOO00O0OO00 .retry_with_backoff (OO0O000OOO0O00OO0 ,3 ,'Result')#line:255
    async def main (O000O0OOOO0OOO000 ):#line:258
        await O000O0OOOO0OOO000 .verify ()#line:259
        await O000O0OOOO0OOO000 .LinkId ()#line:260
        if O000O0OOOO0OOO000 .verify_result !=True :#line:261
            await O000O0OOOO0OOO000 .verify ()#line:262
        if O000O0OOOO0OOO000 .verify_result !=True :#line:263
            O000O0OOOO0OOO000 .log .error ("授权未通过 退出")#line:264
            sys .exit ()#line:265
        for O000OO0OOO0000OO0 in O000O0OOOO0OOO000 .linkId :#line:266
            OOOOOO00O000O00O0 =await O000O0OOOO0OOO000 .Get_H5_Api ("inviteFissionBeforeHome",{'linkId':O000OO0OOO0000OO0 ,"isJdApp":True ,'inviter':O000O0OOOO0OOO000 .inviter_help },O000O0OOOO0OOO000 .coookie ,'02f8d')#line:269
        if OOOOOO00O000O00O0 ['success']==False and OOOOOO00O000O00O0 ['code']==1000 :#line:270
            O000O0OOOO0OOO000 .log .info (f"{OOOOOO00O000O00O0['errMsg']}")#line:271
            sys .exit ()#line:272
        if OOOOOO00O000O00O0 ['data']['helpResult']==1 :#line:273
            O000O0OOOO0OOO000 .log .info (f'{O000O0OOOO0OOO000.pt_pin(O000O0OOOO0OOO000.coookie)}✅助力作者成功 谢谢你 你是个好人！！！')#line:274
        else :#line:275
            O000O0OOOO0OOO000 .log .info (f'{O000O0OOOO0OOO000.pt_pin(O000O0OOOO0OOO000.coookie)}❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:276
        if O000O0OOOO0OOO000 .inviter ==False :#line:278
            for O000OO0OOO0000OO0 in O000O0OOOO0OOO000 .linkId :#line:279
                OOOOOO00O000O00O0 =await O000O0OOOO0OOO000 .Get_H5_Api ('inviteFissionHome',{'linkId':O000OO0OOO0000OO0 ,"inviter":"",},O000O0OOOO0OOO000 .coookie ,'af89e')#line:280
                O000O0OOOO0OOO000 .log .info (f'{O000O0OOOO0OOO000.pt_pin(O000O0OOOO0OOO000.coookie)}⏰剩余时间:{O000O0OOOO0OOO000.convert_ms_to_hours_minutes(OOOOOO00O000O00O0["data"]["countDownTime"])} 🎉已获取助力:{OOOOOO00O000O00O0["data"]["prizeNum"] + OOOOOO00O000O00O0["data"]["drawPrizeNum"]}次 ✅【LinkId】:{O000OO0OOO0000OO0}')#line:281
            O000O0OOOO0OOO000 .inviter =OOOOOO00O000O00O0 ["data"]["inviter"]#line:282
        if O000O0OOOO0OOO000 .proxy !=False :#line:283
            O000O0OOOO0OOO000 .log .info (f"##############开始并发[线程数:{O000O0OOOO0OOO000.semaphore._value}]##############")#line:284
            O00OO0OOO00000OO0 =[]#line:285
            async def O00O000O0O00OO000 (O00OO0O0OOO000000 ,O0O00O0OOOOOOOO0O ):#line:293
                async with O000O0OOOO0OOO000 .semaphore :#line:294
                    O0000O00O00000O00 =asyncio .create_task (O000O0OOOO0OOO000 .Result (O00OO0O0OOO000000 ,O000O0OOOO0OOO000 .inviter ,O0O00O0OOOOOOOO0O ))#line:295
                    return await O0000O00O00000O00 #line:296
            for OO000000OOOO0OO0O ,O00O0OOO00OOO0000 in enumerate (ck ,1 ):#line:299
                O0OO0OO0OOO0OOOOO =asyncio .create_task (O00O000O0O00OO000 (OO000000OOOO0OO0O ,O00O0OOO00OOO0000 ))#line:300
                O00OO0OOO00000OO0 .append (O0OO0OO0OOO0OOOOO )#line:301
            O00O0OO00O00OOOO0 =await asyncio .gather (*O00OO0OOO00000OO0 )#line:303
        else :#line:304
            O000O0OOOO0OOO000 .log .info (f"##############开始任务##############")#line:305
            for OO000000OOOO0OO0O ,O00O0OOO00OOO0000 in enumerate (ck ,1 ):#line:306
                await O000O0OOOO0OOO000 .Result (OO000000OOOO0OO0O ,O000O0OOOO0OOO000 .inviter ,O00O0OOO00OOO0000 )#line:307
                await asyncio .sleep (0.5 )#line:308
        O000O0OOOO0OOO000 .log .info (f"##############清点人数##############")#line:310
        O000O0OOOO0OOO000 .log .info (f"✅助力成功:{len(O000O0OOOO0OOO000.power_success)}人 ❌助力失败:{len(O000O0OOOO0OOO000.power_failure)}人 💔未登录CK{len(O000O0OOOO0OOO000.not_log)}人")#line:311
        O000O0OOOO0OOO000 .log .info (f" ⏰耗时:{time.time() - O000O0OOOO0OOO000.start}")#line:312
if __name__ =='__main__':#line:314
    pdd =TEN_JD_PDD ()#line:315
    loop =asyncio .get_event_loop ()#line:316
    loop .run_until_complete (pdd .main ())#line:317
    loop .close ()#line:318
