#!/usr/bin/env python3
"""
File: TEN_JD_PDD.py(邀好友赢现金-助理)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-助理');
"""

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
    def __init__ (OO0OOO0O0OOOOO0OO ):#line:28
        OO0OOO0O0OOOOO0OO .log =setup_logger ()#line:29
        OO0OOO0O0OOOOO0OO .start =time .time ()#line:30
        OO0OOO0O0OOOOO0OO .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:32
        OO0OOO0O0OOOOO0OO .inviter =os .environ .get ("TEN_inviter")if os .environ .get ("TEN_inviter")else False #line:33
        OO0OOO0O0OOOOO0OO .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:34
        OO0OOO0O0OOOOO0OO .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:35
        OO0OOO0O0OOOOO0OO .semaphore =asyncio .Semaphore (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 10 )#line:36
        OO0OOO0O0OOOOO0OO .power_success =[]#line:37
        OO0OOO0O0OOOOO0OO .power_failure =[]#line:38
        OO0OOO0O0OOOOO0OO .not_log =[]#line:39
        OO0OOO0O0OOOOO0OO .exit_event =threading .Event ()#line:40
        OO0OOO0O0OOOOO0OO .coookie =ck [0 ]#line:41
        OO0OOO0O0OOOOO0OO .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:48
        OO0OOO0O0OOOOO0OO .verify_result =False #line:49
        OO0OOO0O0OOOOO0OO .linkId =[]#line:50
        OO0OOO0O0OOOOO0OO .inviter_help =''#line:51
        OO0OOO0O0OOOOO0OO .version ='1.3.6'#line:52
        OO0OOO0O0OOOOO0OO .exit_condition =300 #line:53
    def pt_pin (OOO0O0OOOOO0O0OO0 ,OOO0O0O000OO00OOO ):#line:55
        try :#line:56
            O000OOO0OOOO0000O =re .compile (r'pt_pin=(.*?);').findall (OOO0O0O000OO00OOO )[0 ]#line:57
            O000OOO0OOOO0000O =unquote_plus (O000OOO0OOOO0000O )#line:58
        except IndexError :#line:59
            O000OOO0OOOO0000O =re .compile (r'pin=(.*?);').findall (OOO0O0O000OO00OOO )[0 ]#line:60
            O000OOO0OOOO0000O =unquote_plus (O000OOO0OOOO0000O )#line:61
        return O000OOO0OOOO0000O #line:62
    def convert_ms_to_hours_minutes (O000OO0O0O0O00O0O ,O0O0O0O0O0OOO0O0O ):#line:64
        O0000000OOOOO0OOO =O0O0O0O0O0OOO0O0O //1000 #line:65
        O00000OO000O00000 ,O0000000OOOOO0OOO =divmod (O0000000OOOOO0OOO ,60 )#line:66
        O000O0OO0O0O00O00 ,O00000OO000O00000 =divmod (O00000OO000O00000 ,60 )#line:67
        return f'{O000O0OO0O0O00O00}:{O00000OO000O00000}'#line:68
    def list_of_groups (O0O0O0O0O0O0O0O00 ,O0OOOOOOO00O0O0OO ,OOO00O00O0O0O00OO ):#line:70
        O00O0O0O000O00000 =zip (*(iter (O0OOOOOOO00O0O0OO ),)*OOO00O00O0O0O00OO )#line:71
        O000OOOOO0O000O0O =[list (O0000OOOOO0000OOO )for O0000OOOOO0000OOO in O00O0O0O000O00000 ]#line:72
        OO00OOO0OOOOOOOO0 =len (O0OOOOOOO00O0O0OO )%OOO00O00O0O0O00OO #line:73
        O000OOOOO0O000O0O .append (O0OOOOOOO00O0O0OO [-OO00OOO0OOOOOOOO0 :])if OO00OOO0OOOOOOOO0 !=0 else O000OOOOO0O000O0O #line:74
        return O000OOOOO0O000O0O #line:75
    async def retry_with_backoff (OOO0O0OOOOOOO0O00 ,OOOO0O00O00OO0000 ,OO0000O0O0OOO00OO ,OOOOOOOOOO0OO00O0 ,backoff_seconds =0 ):#line:77
        for O00000000O00OOO0O in range (OO0000O0O0OOO00OO ):#line:78
            OO00O0O0O00OO0O0O =False #line:79
            try :#line:80
                return await OOOO0O00O00OO0000 ()#line:81
            except asyncio .TimeoutError :#line:82
                if not OO00O0O0O00OO0O0O :#line:83
                    OOO0O0OOOOOOO0O00 .log .debug (f'第{O00000000O00OOO0O + 1}次重试 {OOOOOOOOOO0OO00O0} 请求超时')#line:84
                    OO00O0O0O00OO0O0O =True #line:85
                await asyncio .sleep (backoff_seconds )#line:86
            except Exception as O0OO00OO0OO00O0OO :#line:87
                if not OO00O0O0O00OO0O0O :#line:88
                    OOO0O0OOOOOOO0O00 .log .debug (f'第{O00000000O00OOO0O + 1}次重试 {OOOOOOOOOO0OO00O0} 出错：{O0OO00OO0OO00O0OO}')#line:89
                    OO00O0O0O00OO0O0O =True #line:90
                await asyncio .sleep (backoff_seconds )#line:91
            if OO00O0O0O00OO0O0O and O00000000O00OOO0O ==OO0000O0O0OOO00OO -1 :#line:93
                OOO0O0OOOOOOO0O00 .log .error (f'{OOOOOOOOOO0OO00O0} 重试{OO0000O0O0OOO00OO}次后仍然发生异常')#line:94
                return False ,False ,False #line:95
    async def verify (OOOOOOO00O00OO0OO ):#line:97
        OOOOOOO00O00OO0OO .verify_result =True #line:98
    def parse_version (O0OOOO0O0OO0O00OO ,OO000000OO0O00O0O ):#line:114
        return list (map (int ,OO000000OO0O00O0O .split ('.')))#line:115
    def is_major_update (O0OO0O0000O0OO000 ,O0O0000OO00O0OOOO ,OO00OOOO00OO0O0O0 ):#line:117
        if O0O0000OO00O0OOOO [1 ]!=OO00OOOO00OO0O0O0 [1 ]:#line:118
            return True #line:119
        elif O0O0000OO00O0OOOO [0 ]!=OO00OOOO00OO0O0O0 [0 ]:#line:120
            return True #line:121
        else :#line:122
            return False #line:123
    def is_force_update (O000OO00O0O00000O ,O00O000OOO00OOOO0 ,OO00O0OOOO0O0OOOO ):#line:125
        if O000OO00O0O00000O .is_major_update (O00O000OOO00OOOO0 ,OO00O0OOOO0O0OOOO ):#line:126
            return True #line:127
        elif OO00O0OOOO0O0OOOO [2 ]-O00O000OOO00OOOO0 [2 ]>=3 :#line:128
            return True #line:129
        elif OO00O0OOOO0O0OOOO [2 ]<O00O000OOO00OOOO0 [2 ]:#line:130
            return True #line:131
        else :#line:132
            return False #line:133
    async def LinkId (O0OO00O00OOOO00OO ):#line:135
        async def OO0O0OOO0O0OOOO00 ():#line:136
            if O0OO00O00OOOO00OO .verify_result !=True :#line:137
                await O0OO00O00OOOO00OO .verify ()#line:138
            if O0OO00O00OOOO00OO .verify_result !=True :#line:139
                O0OO00O00OOOO00OO .log .error ("授权未通过 退出")#line:140
                sys .exit ()#line:141
            OOO0000OO0OO0OOOO ='https://api.ixu.cc/status/inviter.json'#line:142
            async with aiohttp .ClientSession ()as OOO0O0OOOOOOOOO0O :#line:143
                async with OOO0O0OOOOOOOOO0O .get (OOO0000OO0OO0OOOO ,params ={'TOKEN':O0OO00O00OOOO00OO .token },timeout =3 )as O000O0O000O0OO0O0 :#line:144
                    if O000O0O000O0OO0O0 .status ==200 :#line:145
                        O000OO0O0OOO00O0O =await O000O0O000O0OO0O0 .json ()#line:146
                        if O000OO0O0OOO00O0O ['stats']!='True':#line:147
                            O0OO00O00OOOO00OO .log .error (f"{O000OO0O0OOO00O0O['err_text']}")#line:148
                            sys .exit ()#line:149
                        O0OO00O00OOOO00OO .inviter_help =O000OO0O0OOO00O0O ['inviter']#line:150
                        if O0OO00O00OOOO00OO .is_force_update (O0OO00O00OOOO00OO .parse_version (O0OO00O00OOOO00OO .version ),O0OO00O00OOOO00OO .parse_version (O000OO0O0OOO00O0O ["version"])):#line:151
                            O0OO00O00OOOO00OO .log .error (f'强制更新 云端版本:{O000OO0O0OOO00O0O["version"]},当前版本:{O0OO00O00OOOO00OO.version} {O000OO0O0OOO00O0O["upload_text"]}')#line:153
                            sys .exit ()#line:154
                        else :#line:155
                            O0OO00O00OOOO00OO .log .debug (f'云端版本:{O000OO0O0OOO00O0O["version"]},当前版本:{O0OO00O00OOOO00OO.version}')#line:156
                        if len (O000OO0O0OOO00O0O ['text'])>0 :#line:157
                            O0OO00O00OOOO00OO .log .debug (f'那女孩对你说:{O000OO0O0OOO00O0O["text"]}')#line:158
                        if O0OO00O00OOOO00OO .scode =='ALL'or O0OO00O00OOOO00OO .scode =='all':#line:159
                            for OOO00O0OO0OOO0O00 in O000OO0O0OOO00O0O ['linkId']:#line:160
                                O0OO00O00OOOO00OO .linkId .append (OOO00O0OO0OOO0O00 )#line:161
                                O0OO00O00OOOO00OO .log .info (f'云端获取到linkId:{OOO00O0OO0OOO0O00}')#line:162
                            return True #line:163
                        else :#line:164
                            O0OO00O00OOOO00OO .linkId .append (O000OO0O0OOO00O0O ['linkId'][int (O0OO00O00OOOO00OO .scode )-1 ])#line:165
                            O0OO00O00OOOO00OO .log .info (f'云端获取到linkId:{O000OO0O0OOO00O0O["linkId"][int(O0OO00O00OOOO00OO.scode) - 1]}')#line:166
                            return True #line:167
                    else :#line:168
                        O0OO00O00OOOO00OO .log .error ('未获取到linkId 重试')#line:169
        return await O0OO00O00OOOO00OO .retry_with_backoff (OO0O0OOO0O0OOOO00 ,3 ,'linkId')#line:171
    async def Get_H5st (OO0O000OO00O000O0 ,O0O000OO000000OOO ,O0000O0O0O000O00O ,OO000O00O000OOO00 ,O0OO00O00OO00O000 ,OOO00OOOO0OO00O00 ):#line:173
        async def O00000OOO00OOO0O0 ():#line:174
            if OO0O000OO00O000O0 .verify_result !=True :#line:175
                OO0O000OO00O000O0 .log .error ("授权未通过 退出")#line:176
                sys .exit ()#line:177
            O00O0O00O000000O0 ='https://api.ouklc.com/api/h5st'#line:178
            OO00000O00O00O00O =OO0O000OO00O000O0 .pt_pin (OOO00OOOO0OO00O00 )#line:179
            OO00OOOOOOOO0OO0O ={'functionId':O0O000OO000000OOO ,'body':json .dumps (O0000O0O0O000O00O ),'ua':OO000O00O000OOO00 ,'pin':OO00000O00O00O00O ,'appId':O0OO00O00OO00O000 }#line:186
            async with aiohttp .ClientSession ()as O00O000O00OOOO0O0 :#line:187
                async with O00O000O00OOOO0O0 .get (O00O0O00O000000O0 ,params =OO00OOOOOOOO0OO0O ,timeout =10 )as O0OOOO0OOO0O00OOO :#line:188
                    if O0OOOO0OOO0O00OOO .status ==200 :#line:189
                        O0O00O00O00000OO0 =await O0OOOO0OOO0O00OOO .json ()#line:190
                        return O0O00O00O00000OO0 ['body']#line:192
                    else :#line:193
                        return await OO0O000OO00O000O0 .retry_with_backoff (O00000OOO00OOO0O0 ,3 ,'H5st')#line:194
        return await OO0O000OO00O000O0 .retry_with_backoff (O00000OOO00OOO0O0 ,3 ,'H5st')#line:196
    async def Get_H5_Api (O0000OO0000OOO000 ,O0O0O000O00O00000 ,O00OO00O0OOOOO00O ,OOO0O00O00O0O0O00 ,OO0OOO00O0O0OO000 ):#line:198
        async def O0O0OO0000000O0O0 (O0000O000O00O0OO0 ):#line:199
            if O0000OO0000OOO000 .verify_result !=True :#line:200
                O0000OO0000OOO000 .log .error ("授权未通过 退出")#line:201
                sys .exit ()#line:202
            O0OOO00OO00OOO0O0 =generate_random_user_agent ()#line:203
            OO00OOOOO0O000OO0 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OOO0O00O00O0O0O00 ,"User-Agent":O0OOO00OO00OOO0O0 }#line:215
            O00O0O0OOO000OOO0 =getUUID ("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")#line:216
            O0000O000O00O0OO0 =await O0000OO0000OOO000 .Get_H5st (O0O0O000O00O00000 ,O0000O000O00O0OO0 ,O0OOO00OO00OOO0O0 ,OO0OOO00O0O0OO000 ,OOO0O00O00O0O0O00 )#line:217
            O0O000O000OOO0O00 ="https://api.m.jd.com"#line:219
            async with aiohttp .ClientSession ()as OO0O00O0O0000O0O0 :#line:220
                if O0000OO0000OOO000 .proxy ==False :#line:221
                    async with OO0O00O0O0000O0O0 .post (O0O000O000OOO0O00 ,headers =OO00OOOOO0O000OO0 ,data =O0000O000O00O0OO0 ,timeout =5 )as O000OOOO0O000O00O :#line:222
                        if O000OOOO0O000O00O .status ==200 :#line:223
                            return await O000OOOO0O000O00O .json ()#line:224
                        else :#line:226
                            O0000OO0000OOO000 .log .error (f'重试 请求结果：{O000OOOO0O000O00O.status}')#line:227
                else :#line:228
                    async with OO0O00O0O0000O0O0 .post (O0O000O000OOO0O00 ,headers =OO00OOOOO0O000OO0 ,data =O0000O000O00O0OO0 ,timeout =5 ,proxy =O0000OO0000OOO000 .proxy )as O000OOOO0O000O00O :#line:229
                        if O000OOOO0O000O00O .status ==200 :#line:230
                            return await O000OOOO0O000O00O .json ()#line:231
                        else :#line:232
                            O0000OO0000OOO000 .log .error (f'重试 请求结果：{O000OOOO0O000O00O.status}')#line:233
                            await O0000OO0000OOO000 .Get_H5_Api (O0O0O000O00O00000 ,O0000O000O00O0OO0 ,OOO0O00O00O0O0O00 ,OO0OOO00O0O0OO000 )#line:234
        return await O0000OO0000OOO000 .retry_with_backoff (lambda :O0O0OO0000000O0O0 (O00OO00O0OOOOO00O ),3 ,'H5st_Api')#line:236
    async def Result (OOOO00O000O0OO000 ,O00O0OO00OO0O0OO0 ,OO00O0OOO00O0OOO0 ,O0OO00000OOO000OO ):#line:238
        if OOOO00O000O0OO000 .exit_condition and len (OOOO00O000O0OO000 .power_success )>=OOOO00O000O0OO000 .exit_condition :#line:239
            sys .exit ()#line:240
        async def OO00OOO0O000OOOOO ():#line:242
            O0000OOOOO0000000 =False #line:243
            if OOOO00O000O0OO000 .verify_result !=True :#line:244
                OOOO00O000O0OO000 .log .error ("授权未通过 退出")#line:245
                sys .exit ()#line:246
            for O000000O000O00OO0 in OOOO00O000O0OO000 .linkId :#line:247
                O0O0O000O00O0OO0O =await OOOO00O000O0OO000 .Get_H5_Api ("inviteFissionhelp",{'linkId':O000000O000O00OO0 ,"isJdApp":True ,'inviter':OO00O0OOO00O0OOO0 },O0OO00000OOO000OO ,'c5389')#line:250
                if int (O0O0O000O00O0OO0O ['code'])==0 :#line:251
                    for OOOO0OOOO000OO0OO ,OO00000O0000O0OO0 in OOOO00O000O0OO000 .helpResult :#line:252
                        if O0O0O000O00O0OO0O ['data']['helpResult']==int (OOOO0OOOO000OO0OO ):#line:253
                            O0000OOOOO0000000 =True #line:254
                            OOOO00O000O0OO000 .log .info (f"Id:{O000000O000O00OO0[:4] + '****' + O000000O000O00OO0[-4:]}|助理:{O0O0O000O00O0OO0O['data']['nickName']}|{O0O0O000O00O0OO0O['data']['helpResult']}|第{O00O0OO00OO0O0OO0}次|{OOOO00O000O0OO000.pt_pin(O0OO00000OOO000OO)}|{OO00000O0000O0OO0}")#line:256
                            if O0O0O000O00O0OO0O ['data']['helpResult']==1 :#line:257
                                OOOO00O000O0OO000 .power_success .append (O0OO00000OOO000OO )#line:258
                            else :#line:259
                                OOOO00O000O0OO000 .power_failure .append (O0OO00000OOO000OO )#line:260
                    if not O0000OOOOO0000000 :#line:261
                        OO00000O0000O0OO0 ='❌未知状态 (可能是活动未开启！！！)'#line:262
                        OOOO00O000O0OO000 .power_failure .append (O0OO00000OOO000OO )#line:263
                        OOOO00O000O0OO000 .log .info (f"Id:{O000000O000O00OO0[:4] + '****' + O000000O000O00OO0[-4:]}|助理:{O0O0O000O00O0OO0O['data']['nickName']}|{O0O0O000O00O0OO0O['data']['helpResult']}|第{O00O0OO00OO0O0OO0}次|{OOOO00O000O0OO000.pt_pin(O0OO00000OOO000OO)}|{OO00000O0000O0OO0}")#line:265
                else :#line:266
                    OOOO00O000O0OO000 .log .info (f"{OOOO00O000O0OO000.pt_pin(O0OO00000OOO000OO)}{O0O0O000O00O0OO0O['code']} 结果:💔{O0O0O000O00O0OO0O['errMsg']}")#line:267
                    OOOO00O000O0OO000 .not_log .append (O0OO00000OOO000OO )#line:268
        return await OOOO00O000O0OO000 .retry_with_backoff (OO00OOO0O000OOOOO ,3 ,'Result')#line:270
    async def main (OO000O00OOOO0OO00 ):#line:272
        await OO000O00OOOO0OO00 .verify ()#line:273
        await OO000O00OOOO0OO00 .LinkId ()#line:274
        if OO000O00OOOO0OO00 .verify_result !=True :#line:275
            await OO000O00OOOO0OO00 .verify ()#line:276
        if OO000O00OOOO0OO00 .verify_result !=True :#line:277
            OO000O00OOOO0OO00 .log .error ("授权未通过 退出")#line:278
            sys .exit ()#line:279
        for O0OOOOOOOO0O0OOO0 in OO000O00OOOO0OO00 .linkId :#line:280
            O000OO0O0000O000O =await OO000O00OOOO0OO00 .Get_H5_Api ("inviteFissionhelp",{'linkId':O0OOOOOOOO0O0OOO0 ,"isJdApp":True ,'inviter':OO000O00OOOO0OO00 .inviter_help },OO000O00OOOO0OO00 .coookie ,'c5389')#line:283
            if O000OO0O0000O000O ['success']==False and O000OO0O0000O000O ['code']==1000 :#line:284
                OO000O00OOOO0OO00 .log .info (f"{O000OO0O0000O000O['errMsg']}")#line:285
                sys .exit ()#line:286
            if O000OO0O0000O000O ['data']['helpResult']==1 :#line:287
                OO000O00OOOO0OO00 .log .info (f'{OO000O00OOOO0OO00.pt_pin(OO000O00OOOO0OO00.coookie)} ✅助力作者成功 谢谢你 你是个好人！！！')#line:288
            else :#line:289
                OO000O00OOOO0OO00 .log .info (f'{OO000O00OOOO0OO00.pt_pin(OO000O00OOOO0OO00.coookie)} ❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:290
        if OO000O00OOOO0OO00 .inviter ==False :#line:292
            for O0OOOOOOOO0O0OOO0 in OO000O00OOOO0OO00 .linkId :#line:293
                O000OO0O0000O000O =await OO000O00OOOO0OO00 .Get_H5_Api ('inviteFissionHome',{'linkId':O0OOOOOOOO0O0OOO0 ,"inviter":"",},OO000O00OOOO0OO00 .coookie ,'af89e')#line:295
                OO000O00OOOO0OO00 .log .info (f'{OO000O00OOOO0OO00.pt_pin(OO000O00OOOO0OO00.coookie)} ⏰剩余时间:{OO000O00OOOO0OO00.convert_ms_to_hours_minutes(O000OO0O0000O000O["data"]["countDownTime"])} 🎉已获取助力:{O000OO0O0000O000O["data"]["prizeNum"] + O000OO0O0000O000O["data"]["drawPrizeNum"]}次 ✅【LinkId】:{O0OOOOOOOO0O0OOO0}')#line:297
                OO000O00OOOO0OO00 .inviter =O000OO0O0000O000O ["data"]["inviter"]#line:298
                OO000O00OOOO0OO00 .log .info (f'{OO000O00OOOO0OO00.pt_pin(OO000O00OOOO0OO00.coookie)} ✅助理码: {OO000O00OOOO0OO00.inviter}')#line:299
        if OO000O00OOOO0OO00 .proxy !=False :#line:301
            OO000O00OOOO0OO00 .log .info (f"##############开始并发[线程数:{OO000O00OOOO0OO00.semaphore._value}]##############")#line:302
            OOO0O0OOO000OOO00 =[]#line:303
            async def O0O00000OOOO00O00 (OOO0OOO00OOO000O0 ,O00O0OO000O0OO00O ):#line:311
                async with OO000O00OOOO0OO00 .semaphore :#line:312
                    OOOO00O00OOOOO000 =asyncio .create_task (OO000O00OOOO0OO00 .Result (OOO0OOO00OOO000O0 ,OO000O00OOOO0OO00 .inviter ,O00O0OO000O0OO00O ))#line:313
                    if OO000O00OOOO0OO00 .exit_condition and len (OO000O00OOOO0OO00 .power_success )>=OO000O00OOOO0OO00 .exit_condition :#line:314
                        sys .exit ()#line:315
                    return await OOOO00O00OOOOO000 #line:316
            async def O0OOOOO0OOOO0OO0O ():#line:318
                OO000OO0OO00O0000 =[]#line:319
                for OO0OOO0O0OO0OOO0O ,O0OOO0OO0O00OOOOO in enumerate (ck ,1 ):#line:320
                    if OO000O00OOOO0OO00 .exit_condition and len (OO000O00OOOO0OO00 .power_success )>=OO000O00OOOO0OO00 .exit_condition :#line:321
                        sys .exit ()#line:322
                    O00000O0O00OO0O0O =asyncio .create_task (O0O00000OOOO00O00 (OO0OOO0O0OO0OOO0O ,O0OOO0OO0O00OOOOO ))#line:323
                    OO000OO0OO00O0000 .append (O00000O0O00OO0O0O )#line:324
                await asyncio .gather (*OO000OO0OO00O0000 )#line:326
            await O0OOOOO0OOOO0OO0O ()#line:329
        else :#line:335
            OO000O00OOOO0OO00 .log .info (f"##############开始任务##############")#line:336
            for O0O0OO00O00O0OOO0 ,OOOO000O0000OO00O in enumerate (ck ,1 ):#line:337
                await OO000O00OOOO0OO00 .Result (O0O0OO00O00O0OOO0 ,OO000O00OOOO0OO00 .inviter ,OOOO000O0000OO00O )#line:338
                if OO000O00OOOO0OO00 .exit_condition and len (OO000O00OOOO0OO00 .power_success )>=OO000O00OOOO0OO00 .exit_condition :#line:339
                    sys .exit ()#line:340
                await asyncio .sleep (0.5 )#line:341
        OO000O00OOOO0OO00 .log .info (f"##############清点人数##############")#line:343
        OO000O00OOOO0OO00 .log .info (f"✅助力成功:{len(OO000O00OOOO0OO00.power_success)}人 ❌助力失败:{len(OO000O00OOOO0OO00.power_failure)}人 💔未登录CK{len(OO000O00OOOO0OO00.not_log)}人")#line:345
        OO000O00OOOO0OO00 .log .info (f" ⏰耗时:{time.time() - OO000O00OOOO0OO00.start}")#line:346
if __name__ =='__main__':#line:349
    pdd =TEN_JD_PDD ()#line:350
    loop =asyncio .get_event_loop ()#line:351
    loop .run_until_complete (pdd .main ())#line:352
    loop .close ()#line:353
