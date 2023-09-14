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
    def __init__ (OOO000OO00OOO00O0 ):#line:26
        OOO000OO00OOO00O0 .log =setup_logger ()#line:27
        OOO000OO00OOO00O0 .start =time .time ()#line:28
        OOO000OO00OOO00O0 .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:30
        OOO000OO00OOO00O0 .inviter =os .environ .get ("TEN_inviter")if os .environ .get ("TEN_inviter")else False #line:31
        OOO000OO00OOO00O0 .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:32
        OOO000OO00OOO00O0 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:33
        OOO000OO00OOO00O0 .semaphore =asyncio .Semaphore (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 30 )#line:34
        OOO000OO00OOO00O0 .power_success =[]#line:35
        OOO000OO00OOO00O0 .power_failure =[]#line:36
        OOO000OO00OOO00O0 .not_log =[]#line:37
        OOO000OO00OOO00O0 .exit_event =threading .Event ()#line:38
        OOO000OO00OOO00O0 .coookie =ck [0 ]#line:39
        OOO000OO00OOO00O0 .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:46
        OOO000OO00OOO00O0 .verify_result =False #line:47
        OOO000OO00OOO00O0 .linkId =[]#line:48
        OOO000OO00OOO00O0 .inviter_help =''#line:49
        OOO000OO00OOO00O0 .version ='1.3.6'#line:50
    def pt_pin (O00OO0OOO00O00O0O ,O0OOOO0OOO0000OO0 ):#line:52
        try :#line:53
            O0OO0O0O0OOOOOOO0 =re .compile (r'pt_pin=(.*?);').findall (O0OOOO0OOO0000OO0 )[0 ]#line:54
            O0OO0O0O0OOOOOOO0 =unquote_plus (O0OO0O0O0OOOOOOO0 )#line:55
        except IndexError :#line:56
            O0OO0O0O0OOOOOOO0 =re .compile (r'pin=(.*?);').findall (O0OOOO0OOO0000OO0 )[0 ]#line:57
            O0OO0O0O0OOOOOOO0 =unquote_plus (O0OO0O0O0OOOOOOO0 )#line:58
        return O0OO0O0O0OOOOOOO0 #line:59
    def convert_ms_to_hours_minutes (O0O0O0OOO00O00O00 ,OO00OOOOO00O00O0O ):#line:60
        O0OOO0O000000O000 =OO00OOOOO00O00O0O //1000 #line:61
        O0O0000O00OOO000O ,O0OOO0O000000O000 =divmod (O0OOO0O000000O000 ,60 )#line:62
        O0OO0O00O0OO00OO0 ,O0O0000O00OOO000O =divmod (O0O0000O00OOO000O ,60 )#line:63
        return f'{O0OO0O00O0OO00OO0}:{O0O0000O00OOO000O}'#line:64
    def list_of_groups (OOOO00000OO0O00OO ,O0O00OO00O00000OO ,O0OO000O0O000OO00 ):#line:66
        OOO0000O00O00O00O =zip (*(iter (O0O00OO00O00000OO ),)*O0OO000O0O000OO00 )#line:67
        O000OOOOO0O0OOOO0 =[list (OOO00OOOO0OOO0000 )for OOO00OOOO0OOO0000 in OOO0000O00O00O00O ]#line:68
        OOO0O0O0O0OO00OO0 =len (O0O00OO00O00000OO )%O0OO000O0O000OO00 #line:69
        O000OOOOO0O0OOOO0 .append (O0O00OO00O00000OO [-OOO0O0O0O0OO00OO0 :])if OOO0O0O0O0OO00OO0 !=0 else O000OOOOO0O0OOOO0 #line:70
        return O000OOOOO0O0OOOO0 #line:71
    async def retry_with_backoff (OO000OOO0000OOOOO ,OO000OO0OO0O0O000 ,OO0OO0OO0OOO0OO0O ,OOO00OO0OOO000OOO ,backoff_seconds =2 ):#line:73
        for O0OO000OOOOO00O00 in range (OO0OO0OO0OOO0OO0O ):#line:75
            try :#line:76
                return await OO000OO0OO0O0O000 ()#line:77
            except asyncio .TimeoutError :#line:78
                OO000OOO0000OOOOO .log .debug (f'第{O0OO000OOOOO00O00 + 1}次重试  {OOO00OO0OOO000OOO} 请求超时')#line:79
                await asyncio .sleep (backoff_seconds )#line:80
            except Exception as OO000O0OO0000O0O0 :#line:81
                OO000OOO0000OOOOO .log .debug (f'第{O0OO000OOOOO00O00 + 1}次重试 {OOO00OO0OOO000OOO}出错：{OO000O0OO0000O0O0}')#line:82
                await asyncio .sleep (backoff_seconds )#line:83
                if O0OO000OOOOO00O00 ==OO0OO0OO0OOO0OO0O :#line:84
                    OO000OOO0000OOOOO .log .error (f'{OOO00OO0OOO000OOO}重试{OO0OO0OO0OOO0OO0O}次后仍然发生异常')#line:85
                    return #line:86
    async def verify (O00O0OOO0OO00OOOO ):#line:88
        async def OO0OOO00OOOO00000 ():#line:89
            O00O0000O000O0OOO ='https://api.ixu.cc/verify'#line:90
            async with aiohttp .ClientSession ()as OOOO0OO00O00O00O0 :#line:91
                async with OOOO0OO00O00O00O0 .get (O00O0000O000O0OOO ,data ={'TOKEN':O00O0OOO0OO00OOOO .token },timeout =3 )as O0O000O00000OOOO0 :#line:92
                    OO0OOOOOO0OO0O0O0 =await O0O000O00000OOOO0 .json ()#line:93
                    if O0O000O00000OOOO0 .status ==200 :#line:94
                        O00O0OOO0OO00OOOO .verify_result =True #line:95
                        O00O0OOO0OO00OOOO .log .info (f'认证通过 UserId：{OO0OOOOOO0OO0O0O0["user_id"]}')#line:96
                        return OO0OOOOOO0OO0O0O0 #line:97
                    else :#line:98
                        O00O0OOO0OO00OOOO .log .error (f"授权未通过:{OO0OOOOOO0OO0O0O0['error']}")#line:99
                        sys .exit ()#line:100
        return await O00O0OOO0OO00OOOO .retry_with_backoff (OO0OOO00OOOO00000 ,3 ,'verify')#line:102
    def parse_version (OO00000O00O0OO000 ,OO0OO0000O0O0O0OO ):#line:104
        return list (map (int ,OO0OO0000O0O0O0OO .split ('.')))#line:105
    def is_major_update (O0OO0OO00O00000OO ,OO000000OO0O00000 ,OOOOO0OOO000000O0 ):#line:107
        if OO000000OO0O00000 [1 ]!=OOOOO0OOO000000O0 [1 ]:#line:108
            return True #line:109
        elif OO000000OO0O00000 [0 ]!=OOOOO0OOO000000O0 [0 ]:#line:110
            return True #line:111
        else :#line:112
            return False #line:113
    def is_force_update (O00OO0OO00OO0O0OO ,OO0O0OOO0O0O0OO00 ,OOO000OO0O0O0O0OO ):#line:115
        if O00OO0OO00OO0O0OO .is_major_update (OO0O0OOO0O0O0OO00 ,OOO000OO0O0O0O0OO ):#line:116
            return True #line:117
        elif OOO000OO0O0O0O0OO [2 ]-OO0O0OOO0O0O0OO00 [2 ]>=3 :#line:118
            return True #line:119
        elif OOO000OO0O0O0O0OO [2 ]<OO0O0OOO0O0O0OO00 [2 ]:#line:120
            return True #line:121
        else :#line:122
            return False #line:123
    async def LinkId (OOOOOOO00OO000O0O ):#line:125
        async def O0OOOOO0O00OO000O ():#line:126
            if OOOOOOO00OO000O0O .verify_result !=True :#line:127
                await OOOOOOO00OO000O0O .verify ()#line:128
            if OOOOOOO00OO000O0O .verify_result !=True :#line:129
                OOOOOOO00OO000O0O .log .error ("授权未通过 退出")#line:130
                sys .exit ()#line:131
            OO0OO00OO00O0OO00 ='https://api.ixu.cc/status/inviter.json'#line:132
            async with aiohttp .ClientSession ()as O00O0O00O00OOOOOO :#line:133
                async with O00O0O00O00OOOOOO .get (OO0OO00OO00O0OO00 ,params ={'TOKEN':OOOOOOO00OO000O0O .token },timeout =3 )as O0O0000O000O0OO00 :#line:134
                    if O0O0000O000O0OO00 .status ==200 :#line:135
                        OOOOO0OO00O00O0O0 =await O0O0000O000O0OO00 .json ()#line:136
                        if OOOOO0OO00O00O0O0 ['stats']!='True':#line:137
                            OOOOOOO00OO000O0O .log .error (f"{OOOOO0OO00O00O0O0['err_text']}")#line:138
                            sys .exit ()#line:139
                        OOOOOOO00OO000O0O .inviter_help =OOOOO0OO00O00O0O0 ['inviter']#line:140
                        if OOOOOOO00OO000O0O .is_force_update (OOOOOOO00OO000O0O .parse_version (OOOOOOO00OO000O0O .version ),OOOOOOO00OO000O0O .parse_version (OOOOO0OO00O00O0O0 ["version"])):#line:141
                            OOOOOOO00OO000O0O .log .error (f'强制更新 云端版本:{OOOOO0OO00O00O0O0["version"]},当前版本:{OOOOOOO00OO000O0O.version} {OOOOO0OO00O00O0O0["upload_text"]}')#line:142
                            sys .exit ()#line:143
                        else :#line:144
                            OOOOOOO00OO000O0O .log .debug (f'云端版本:{OOOOO0OO00O00O0O0["version"]},当前版本:{OOOOOOO00OO000O0O.version}')#line:145
                        if len (OOOOO0OO00O00O0O0 ['text'])>0 :#line:146
                            OOOOOOO00OO000O0O .log .debug (f'那女孩对你说:{OOOOO0OO00O00O0O0["text"]}')#line:147
                        if OOOOOOO00OO000O0O .scode =='ALL'or OOOOOOO00OO000O0O .scode =='all':#line:148
                            for O0OO0OOOO0000OOOO in OOOOO0OO00O00O0O0 ['linkId']:#line:149
                                OOOOOOO00OO000O0O .linkId .append (O0OO0OOOO0000OOOO )#line:150
                                OOOOOOO00OO000O0O .log .info (f'云端获取到linkId:{O0OO0OOOO0000OOOO}')#line:151
                            return True #line:152
                        else :#line:153
                            OOOOOOO00OO000O0O .linkId .append (OOOOO0OO00O00O0O0 ['linkId'][int (OOOOOOO00OO000O0O .scode )-1 ])#line:154
                            OOOOOOO00OO000O0O .log .info (f'云端获取到linkId:{OOOOO0OO00O00O0O0["linkId"][int(OOOOOOO00OO000O0O.scode) - 1]}')#line:155
                            return True #line:156
                    else :#line:157
                        OOOOOOO00OO000O0O .log .error ('未获取到linkId 重试')#line:158
        return await OOOOOOO00OO000O0O .retry_with_backoff (O0OOOOO0O00OO000O ,3 ,'linkId')#line:159
    async def Get_H5st (O00OO0O00OO00OO0O ,O00OO0OOOO00OO00O ,O000OO00O0OOOO0OO ,OO00000O0O0OOOO00 ,O0OOOO000O000OO0O ,OOOO00OO00OOO0O0O ):#line:164
        async def OO00OO00O0O0OO0OO ():#line:165
            if O00OO0O00OO00OO0O .verify_result !=True :#line:166
                O00OO0O00OO00OO0O .log .error ("授权未通过 退出")#line:167
                sys .exit ()#line:168
            O00000O0000OOOOO0 ='https://api.ouklc.com/api/h5st'#line:169
            O00OOO00000OO0000 =O00OO0O00OO00OO0O .pt_pin (OOOO00OO00OOO0O0O )#line:170
            OO0O0OO000O00OOO0 ={'functionId':O00OO0OOOO00OO00O ,'body':json .dumps (O000OO00O0OOOO0OO ),'ua':OO00000O0O0OOOO00 ,'pin':O00OOO00000OO0000 ,'appId':O0OOOO000O000OO0O }#line:177
            async with aiohttp .ClientSession ()as OOO00O00O0O000OO0 :#line:178
                async with OOO00O00O0O000OO0 .get (O00000O0000OOOOO0 ,params =OO0O0OO000O00OOO0 ,timeout =10 )as OOOO000OOOO0OOOOO :#line:179
                    if OOOO000OOOO0OOOOO .status ==200 :#line:180
                        O00OOO0OO00OO00O0 =await OOOO000OOOO0OOOOO .json ()#line:181
                        return O00OOO0OO00OO00O0 ['body']#line:183
                    else :#line:184
                        return await O00OO0O00OO00OO0O .retry_with_backoff (OO00OO00O0O0OO0OO ,3 ,'H5st')#line:185
        return await O00OO0O00OO00OO0O .retry_with_backoff (OO00OO00O0O0OO0OO ,3 ,'H5st')#line:187
    async def Get_H5_Api (O00OOO00000O0OO00 ,O00OOOOOOO0OO0O00 ,OOO000OO0O000OO00 ,OOOOO000O0OOOOOO0 ,O0O0O0000O000OO0O ):#line:191
            async def OOOO0OO0O0O000OO0 (O000OOOO000O00O0O ):#line:192
                if O00OOO00000O0OO00 .verify_result !=True :#line:193
                    O00OOO00000O0OO00 .log .error ("授权未通过 退出")#line:194
                    sys .exit ()#line:195
                OOO000O00O00O000O =generate_random_user_agent ()#line:196
                O0O000OOO00O0OOO0 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OOOOO000O0OOOOOO0 ,"User-Agent":OOO000O00O00O000O }#line:208
                OOO0O0OO0O0OOOO0O =getUUID ("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")#line:209
                O000OOOO000O00O0O =await O00OOO00000O0OO00 .Get_H5st (O00OOOOOOO0OO0O00 ,O000OOOO000O00O0O ,OOO000O00O00O000O ,O0O0O0000O000OO0O ,OOOOO000O0OOOOOO0 )#line:210
                OOOO00O0OO0OOO0O0 ="https://api.m.jd.com"#line:212
                async with aiohttp .ClientSession ()as OOO0O0OO000OOOOO0 :#line:213
                    if O00OOO00000O0OO00 .proxy ==False :#line:214
                        async with OOO0O0OO000OOOOO0 .post (OOOO00O0OO0OOO0O0 ,headers =O0O000OOO00O0OOO0 ,data =json .dumps (O000OOOO000O00O0O ),timeout =5 )as O0000O00OOOOO00OO :#line:215
                            if O0000O00OOOOO00OO .status ==200 :#line:216
                                return await O0000O00OOOOO00OO .json ()#line:217
                            else :#line:219
                                O00OOO00000O0OO00 .log .error (f'重试 请求结果：{O0000O00OOOOO00OO.status}')#line:220
                    else :#line:222
                        async with OOO0O0OO000OOOOO0 .post (OOOO00O0OO0OOO0O0 ,headers =O0O000OOO00O0OOO0 ,data =O000OOOO000O00O0O ,timeout =5 ,proxy =O00OOO00000O0OO00 .proxy )as O0000O00OOOOO00OO :#line:223
                            if O0000O00OOOOO00OO .status ==200 :#line:224
                                return await O0000O00OOOOO00OO .json ()#line:225
                            else :#line:226
                                O00OOO00000O0OO00 .log .error (f'重试 请求结果：{O0000O00OOOOO00OO.status}')#line:227
                                await O00OOO00000O0OO00 .Get_H5_Api (O00OOOOOOO0OO0O00 ,O000OOOO000O00O0O ,OOOOO000O0OOOOOO0 ,O0O0O0000O000OO0O )#line:228
            return await O00OOO00000O0OO00 .retry_with_backoff (lambda :OOOO0OO0O0O000OO0 (OOO000OO0O000OO00 ),3 ,'H5st_Api')#line:230
    async def Result (O000OO0OO000OOO00 ,O000O0OO0OOOO0000 ,O0O0OOOOO0OO0000O ,O00O0OO00OO0OO000 ):#line:232
        async def O00OO00OO0O0O000O ():#line:233
                if O000OO0OO000OOO00 .verify_result !=True :#line:234
                    O000OO0OO000OOO00 .log .error ("授权未通过 退出")#line:235
                    sys .exit ()#line:236
                for O00O00OO0000O0O0O in O000OO0OO000OOO00 .linkId :#line:237
                    O000OOOOOOO0O000O =await O000OO0OO000OOO00 .Get_H5_Api ("inviteFissionBeforeHome",{'linkId':O00O00OO0000O0O0O ,"isJdApp":True ,'inviter':O0O0OOOOO0OO0000O },O00O0OO00OO0OO000 ,'02f8d')#line:238
                    if int (O000OOOOOOO0O000O ['code'])==0 :#line:239
                        for OO0OO00O000OO00OO ,OO0OO0O0O0OOOOOOO in O000OO0OO000OOO00 .helpResult :#line:240
                            if O000OOOOOOO0O000O ['data']['helpResult']==int (OO0OO00O000OO00OO ):#line:241
                                OOO0OO0OOOOOO00O0 =True #line:242
                                O000OO0OO000OOO00 .log .info (f"第{O000O0OO0OOOO0000}次 Id:{O00O00OO0000O0O0O} 助理:{O000OOOOOOO0O000O['data']['nickName']}|{O000OOOOOOO0O000O['data']['helpResult']}|{O000OO0OO000OOO00.pt_pin(O00O0OO00OO0OO000)}|{OO0OO0O0O0OOOOOOO}")#line:243
                                if O000OOOOOOO0O000O ['data']['helpResult']==1 :#line:244
                                    O000OO0OO000OOO00 .power_success .append (O00O0OO00OO0OO000 )#line:245
                                else :#line:246
                                    O000OO0OO000OOO00 .power_failure .append (O00O0OO00OO0OO000 )#line:247
                        if not OOO0OO0OOOOOO00O0 :#line:248
                            OO0OO0O0O0OOOOOOO ='❌未知状态 (可能是活动未开启！！！)'#line:249
                            O000OO0OO000OOO00 .power_failure .append (O00O0OO00OO0OO000 )#line:250
                            O000OO0OO000OOO00 .log .info (f"第{O000O0OO0OOOO0000}次 Id:{O00O00OO0000O0O0O} 助理:{O000OOOOOOO0O000O['data']['nickName']}|{O000OOOOOOO0O000O['data']['helpResult']}|{O000OO0OO000OOO00.pt_pin(O00O0OO00OO0OO000)}|{OO0OO0O0O0OOOOOOO}")#line:251
                    else :#line:252
                        O000OO0OO000OOO00 .log .info (f"{O000OO0OO000OOO00.pt_pin(O00O0OO00OO0OO000)}{O000OOOOOOO0O000O['code']} 结果:💔{O000OOOOOOO0O000O['errMsg']}")#line:253
                        O000OO0OO000OOO00 .not_log .append (O00O0OO00OO0OO000 )#line:254
        return await O000OO0OO000OOO00 .retry_with_backoff (O00OO00OO0O0O000O ,3 ,'Result')#line:255
    async def main (OO00O00OOOO0OO0OO ):#line:258
        await OO00O00OOOO0OO0OO .verify ()#line:259
        await OO00O00OOOO0OO0OO .LinkId ()#line:260
        if OO00O00OOOO0OO0OO .verify_result !=True :#line:261
            await OO00O00OOOO0OO0OO .verify ()#line:262
        if OO00O00OOOO0OO0OO .verify_result !=True :#line:263
            OO00O00OOOO0OO0OO .log .error ("授权未通过 退出")#line:264
            sys .exit ()#line:265
        if OO00O00OOOO0OO0OO .inviter ==False :#line:278
            for O0O000OO000OO0O00 in OO00O00OOOO0OO0OO .linkId :#line:279
                OO00OOOO000OOOO00 =await OO00O00OOOO0OO0OO .Get_H5_Api ('inviteFissionHome',{'linkId':O0O000OO000OO0O00 ,"inviter":"",},OO00O00OOOO0OO0OO .coookie ,'af89e')#line:280
                OO00O00OOOO0OO0OO .log .info (f'{OO00O00OOOO0OO0OO.pt_pin(OO00O00OOOO0OO0OO.coookie)}⏰剩余时间:{OO00O00OOOO0OO0OO.convert_ms_to_hours_minutes(OO00OOOO000OOOO00["data"]["countDownTime"])} 🎉已获取助力:{OO00OOOO000OOOO00["data"]["prizeNum"] + OO00OOOO000OOOO00["data"]["drawPrizeNum"]}次 ✅【LinkId】:{O0O000OO000OO0O00}')#line:281
            OO00O00OOOO0OO0OO .inviter =OO00OOOO000OOOO00 ["data"]["inviter"]#line:282
        if OO00O00OOOO0OO0OO .proxy !=False :#line:283
            OO00O00OOOO0OO0OO .log .info (f"##############开始并发[线程数:{OO00O00OOOO0OO0OO.semaphore._value}]##############")#line:284
            O0O00OO0O0O0O0O00 =[]#line:285
            async def OOOOO0OO0O0OOO0OO (O0OOO00O0O0O0O0O0 ,O0OOOOO0OO00OOO00 ):#line:293
                async with OO00O00OOOO0OO0OO .semaphore :#line:294
                    OO0OOO000000OOO00 =asyncio .create_task (OO00O00OOOO0OO0OO .Result (O0OOO00O0O0O0O0O0 ,OO00O00OOOO0OO0OO .inviter ,O0OOOOO0OO00OOO00 ))#line:295
                    return await OO0OOO000000OOO00 #line:296
            for OOOO000OOOOOO0O0O ,OOO0O0OOOOO0OOOOO in enumerate (ck ,1 ):#line:299
                OO0O0OO000OOOOOOO =asyncio .create_task (OOOOO0OO0O0OOO0OO (OOOO000OOOOOO0O0O ,OOO0O0OOOOO0OOOOO ))#line:300
                O0O00OO0O0O0O0O00 .append (OO0O0OO000OOOOOOO )#line:301
            O0000O00OO0000OOO =await asyncio .gather (*O0O00OO0O0O0O0O00 )#line:303
        else :#line:306
            OO00O00OOOO0OO0OO .log .info (f"##############开始任务##############")#line:307
            for OOOO000OOOOOO0O0O ,OOO0O0OOOOO0OOOOO in enumerate (ck ,1 ):#line:308
                await OO00O00OOOO0OO0OO .Result (OOOO000OOOOOO0O0O ,OO00O00OOOO0OO0OO .inviter ,OOO0O0OOOOO0OOOOO )#line:309
                await asyncio .sleep (0.5 )#line:310
        OO00O00OOOO0OO0OO .log .info (f"##############清点人数##############")#line:312
        OO00O00OOOO0OO0OO .log .info (f"✅助力成功:{len(OO00O00OOOO0OO0OO.power_success)}人 ❌助力失败:{len(OO00O00OOOO0OO0OO.power_failure)}人 💔未登录CK{len(OO00O00OOOO0OO0OO.not_log)}人")#line:313
        OO00O00OOOO0OO0OO .log .info (f" ⏰耗时:{time.time() - OO00O00OOOO0OO0OO.start}")#line:314
if __name__ =='__main__':#line:316
    pdd =TEN_JD_PDD ()#line:317
    loop =asyncio .get_event_loop ()#line:318
    loop .run_until_complete (pdd .main ())#line:319
    loop .close ()#line:320
