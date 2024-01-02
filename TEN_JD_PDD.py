#!/usr/bin/env python3
"""
File: TEN_JD_PDD.py(邀好友赢现金-助理)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-助理');
"""#!/usr/bin/env python3
""#line:9
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
    def __init__ (O0OO00000OOO0O000 ):#line:28
        O0OO00000OOO0O000 .log =setup_logger ()#line:29
        O0OO00000OOO0O000 .start =time .time ()#line:30
        O0OO00000OOO0O000 .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:32
        O0OO00000OOO0O000 .inviter =os .environ .get ("TEN_inviter")if os .environ .get ("TEN_inviter")else False #line:33
        O0OO00000OOO0O000 .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 3 #line:34
        O0OO00000OOO0O000 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:35
        O0OO00000OOO0O000 .semaphore =asyncio .Semaphore (int (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 30 ))#line:36
        O0OO00000OOO0O000 .power_success =[]#line:37
        O0OO00000OOO0O000 .power_failure =[]#line:38
        O0OO00000OOO0O000 .not_log =[]#line:39
        O0OO00000OOO0O000 .exit_event =threading .Event ()#line:40
        O0OO00000OOO0O000 .coookie =ck [0 ]#line:41
        O0OO00000OOO0O000 .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:48
        O0OO00000OOO0O000 .verify_result =False #line:49
        O0OO00000OOO0O000 .linkId =[]#line:50
        O0OO00000OOO0O000 .inviter_help =''#line:51
        O0OO00000OOO0O000 .version ='1.3.6'#line:52
        O0OO00000OOO0O000 .exit_condition =int (os .environ .get ("TEN_EXIT")if os .environ .get ("TEN_EXIT")else 9999 )#line:53
        O0OO00000OOO0O000 .lock =threading .Lock ()#line:54
    def pt_pin (OO0000O0O00OOO00O ,OOOOO00O0OOOO0OO0 ):#line:56
        try :#line:57
            O0O00O0O00OO000O0 =re .compile (r'pt_pin=(.*?);').findall (OOOOO00O0OOOO0OO0 )[0 ]#line:58
            O0O00O0O00OO000O0 =unquote_plus (O0O00O0O00OO000O0 )#line:59
        except IndexError :#line:60
            O0O00O0O00OO000O0 =re .compile (r'pin=(.*?);').findall (OOOOO00O0OOOO0OO0 )[0 ]#line:61
            O0O00O0O00OO000O0 =unquote_plus (O0O00O0O00OO000O0 )#line:62
        return O0O00O0O00OO000O0 #line:63
    def convert_ms_to_hours_minutes (O0OO0O0O00000OOOO ,OOOO0O00O000O00OO ):#line:77
        OO00O00O0OOO0O0O0 =OOOO0O00O000O00OO //1000 #line:78
        O0OO0OOOOO00O0O0O ,OO00O00O0OOO0O0O0 =divmod (OO00O00O0OOO0O0O0 ,60 )#line:79
        O0O0O00OOOOOOO00O ,O0OO0OOOOO00O0O0O =divmod (O0OO0OOOOO00O0O0O ,60 )#line:80
        return f'{O0O0O00OOOOOOO00O}:{O0OO0OOOOO00O0O0O}'#line:81
    def list_of_groups (OO0O0000000O00OOO ,O0OOOOO0O00000O00 ,OOOOOOO0OOOOOOO00 ):#line:83
        O0OOOO0OOO0OOOO00 =zip (*(iter (O0OOOOO0O00000O00 ),)*OOOOOOO0OOOOOOO00 )#line:84
        O000O0OO0OOOOO0O0 =[list (OOO00O0O0000O000O )for OOO00O0O0000O000O in O0OOOO0OOO0OOOO00 ]#line:85
        O0000OO000O0O0O00 =len (O0OOOOO0O00000O00 )%OOOOOOO0OOOOOOO00 #line:86
        O000O0OO0OOOOO0O0 .append (O0OOOOO0O00000O00 [-O0000OO000O0O0O00 :])if O0000OO000O0O0O00 !=0 else O000O0OO0OOOOO0O0 #line:87
        return O000O0OO0OOOOO0O0 #line:88
    async def retry_with_backoff (O0O0000OOO00O000O ,OO0000O0O000O0000 ,O0OOOOO0OOO0O000O ,OOOOOO0OOO00OO0O0 ,backoff_seconds =0 ):#line:90
        for O00O0000O000O0OO0 in range (O0OOOOO0OOO0O000O ):#line:91
            O00000O0000OOOO00 =False #line:92
            try :#line:93
                return await OO0000O0O000O0000 ()#line:94
            except asyncio .TimeoutError :#line:95
                if not O00000O0000OOOO00 :#line:96
                    O0O0000OOO00O000O .log .warning (f'第{O00O0000O000O0OO0 + 1}次重试 {OOOOOO0OOO00OO0O0} 请求超时')#line:97
                    O00000O0000OOOO00 =True #line:98
                await asyncio .sleep (backoff_seconds )#line:99
            except Exception as O000000O0OO000OOO :#line:100
                if not O00000O0000OOOO00 :#line:101
                    O0O0000OOO00O000O .log .warning (f'第{O00O0000O000O0OO0 + 1}次重试 {OOOOOO0OOO00OO0O0} 出错：{O000000O0OO000OOO}')#line:102
                    O00000O0000OOOO00 =True #line:103
                await asyncio .sleep (backoff_seconds )#line:104
            if O00000O0000OOOO00 and O00O0000O000O0OO0 ==O0OOOOO0OOO0O000O -1 :#line:106
                O0O0000OOO00O000O .log .error (f'{OOOOOO0OOO00OO0O0} 重试{O0OOOOO0OOO0O000O}次后仍然发生异常')#line:107
                return False ,False ,False #line:108
    async def verify (OO0000000O000O0OO ):#line:111
        OO0000000O000O0OO .verify_result =True #line:112
        async def OO00O0OO000O0OO00 ():#line:113
            O00OOO00OOOO00OOO ='https://api.ixu.cc/verify'#line:114
            async with aiohttp .ClientSession ()as O00O0OO0O0O00OOOO :#line:115
                async with O00O0OO0O0O00OOOO .get (O00OOO00OOOO00OOO ,data ={'TOKEN':OO0000000O000O0OO .token },timeout =3 )as O000000O0O0OO0OO0 :#line:116
                    O00OOOO00O0O0O00O =await O000000O0O0OO0OO0 .json ()#line:117
                    if O000000O0O0OO0OO0 .status ==200 :#line:118
                        OO0000000O000O0OO .verify_result =True #line:119
                        OO0000000O000O0OO .log .info (f'认证通过 UserId：{O00OOOO00O0O0O00O["user_id"]}')#line:120
                        return O00OOOO00O0O0O00O #line:121
                    else :#line:122
                        OO0000000O000O0OO .log .error (f"授权未通过:{O00OOOO00O0O0O00O['error']}")#line:123
                        sys .exit ()#line:124
        return await OO0000000O000O0OO .retry_with_backoff (OO00O0OO000O0OO00 ,3 ,'verify')#line:126
    def parse_version (O000O000OO0OOOOOO ,OO000O0O0O0O00O0O ):#line:128
        return list (map (int ,OO000O0O0O0O00O0O .split ('.')))#line:129
    def is_major_update (OOOOO0OO000O0OOO0 ,O000OOO00OO0OO000 ,OOOO000OOO0000000 ):#line:131
        if O000OOO00OO0OO000 [1 ]!=OOOO000OOO0000000 [1 ]:#line:132
            return True #line:133
        elif O000OOO00OO0OO000 [0 ]!=OOOO000OOO0000000 [0 ]:#line:134
            return True #line:135
        else :#line:136
            return False #line:137
    def is_force_update (OO0O00OO000OOO00O ,OOO0O0O0000000O00 ,O0O000O0O0OO000OO ):#line:139
        if OO0O00OO000OOO00O .is_major_update (OOO0O0O0000000O00 ,O0O000O0O0OO000OO ):#line:140
            return True #line:141
        elif O0O000O0O0OO000OO [2 ]-OOO0O0O0000000O00 [2 ]>=3 :#line:142
            return True #line:143
        elif O0O000O0O0OO000OO [2 ]<OOO0O0O0000000O00 [2 ]:#line:144
            return True #line:145
        else :#line:146
            return False #line:147
    async def LinkId (O00O0OO00O00OOO0O ):#line:149
        async def OOO0O00O0OOOO0000 ():#line:150
            if O00O0OO00O00OOO0O .verify_result !=True :#line:151
                await O00O0OO00O00OOO0O .verify ()#line:152
            if O00O0OO00O00OOO0O .verify_result !=True :#line:153
                O00O0OO00O00OOO0O .log .error ("授权未通过 退出")#line:154
                sys .exit ()#line:155
            OO0O000O00OOOO0O0 ='https://api.ixu.cc/status/inviter.json'#line:156
            async with aiohttp .ClientSession ()as OOOOOO00OO0OO0OOO :#line:157
                async with OOOOOO00OO0OO0OOO .get (OO0O000O00OOOO0O0 ,timeout =3 )as OO0OOO00O0O0O0OOO :#line:158
                    if OO0OOO00O0O0O0OOO .status ==200 :#line:159
                        O0OOO0O0OO0O00000 =await OO0OOO00O0O0O0OOO .json ()#line:160
                        if O0OOO0O0OO0O00000 ['stats']!='True':#line:161
                            O00O0OO00O00OOO0O .log .error (f"{O0OOO0O0OO0O00000['err_text']}")#line:162
                            sys .exit ()#line:163
                        O00O0OO00O00OOO0O .inviter_help =O0OOO0O0OO0O00000 ['inviter']#line:164
                        if O00O0OO00O00OOO0O .is_force_update (O00O0OO00O00OOO0O .parse_version (O00O0OO00O00OOO0O .version ),O00O0OO00O00OOO0O .parse_version (O0OOO0O0OO0O00000 ["version"])):#line:165
                            O00O0OO00O00OOO0O .log .error (f'强制更新 云端版本:{O0OOO0O0OO0O00000["version"]},当前版本:{O00O0OO00O00OOO0O.version} {O0OOO0O0OO0O00000["upload_text"]}')#line:167
                            sys .exit ()#line:168
                        else :#line:169
                            O00O0OO00O00OOO0O .log .debug (f'云端版本:{O0OOO0O0OO0O00000["version"]},当前版本:{O00O0OO00O00OOO0O.version}')#line:170
                        if len (O0OOO0O0OO0O00000 ['text'])>0 :#line:171
                            O00O0OO00O00OOO0O .log .debug (f'那女孩对你说:{O0OOO0O0OO0O00000["text"]}')#line:172
                        if O00O0OO00O00OOO0O .scode =='ALL'or O00O0OO00O00OOO0O .scode =='all':#line:173
                            for O00OO0OO00O0O0OOO in O0OOO0O0OO0O00000 ['linkId']:#line:174
                                O00O0OO00O00OOO0O .linkId .append (O00OO0OO00O0O0OOO )#line:175
                                O00O0OO00O00OOO0O .log .info (f'云端获取到linkId:{O00OO0OO00O0O0OOO}')#line:176
                            return True #line:177
                        else :#line:178
                            O00O0OO00O00OOO0O .linkId .append (O0OOO0O0OO0O00000 ['linkId'][int (O00O0OO00O00OOO0O .scode )-1 ])#line:179
                            O00O0OO00O00OOO0O .log .info (f'云端获取到linkId:{O0OOO0O0OO0O00000["linkId"][int(O00O0OO00O00OOO0O.scode) - 1]}')#line:180
                            return True #line:181
                    else :#line:182
                        O00O0OO00O00OOO0O .log .error ('未获取到linkId 重试')#line:183
        return await O00O0OO00O00OOO0O .retry_with_backoff (OOO0O00O0OOOO0000 ,3 ,'linkId')#line:185
    async def Get_H5st (O0OOO00OO0000O0O0 ,OO000OOO00OOOO000 ,O0OOO000OO0O0OO00 ,OOOO0000OOOO000O0 ,O00OOO00O000OOO00 ,OOO0O0O0OO000OO00 ):#line:187
        async def O00O0O00O0O00000O ():#line:188
            if O0OOO00OO0000O0O0 .verify_result !=True :#line:189
                O0OOO00OO0000O0O0 .log .error ("授权未通过 退出")#line:190
                sys .exit ()#line:191
            O0OOO00O000O0O0OO ='https://api.ouklc.com/api/h5st'#line:192
            OO0O0O00OOO0OO00O =O0OOO00OO0000O0O0 .pt_pin (OOO0O0O0OO000OO00 )#line:193
            O0OOO0OOO0O0OOOOO ={'functionId':OO000OOO00OOOO000 ,'body':json .dumps (O0OOO000OO0O0OO00 ),'ua':OOOO0000OOOO000O0 ,'pin':OO0O0O00OOO0OO00O ,'appId':O00OOO00O000OOO00 }#line:200
            async with aiohttp .ClientSession ()as O00000OO0000OOOO0 :#line:201
                async with O00000OO0000OOOO0 .get (O0OOO00O000O0O0OO ,params =O0OOO0OOO0O0OOOOO ,timeout =10 )as O00O000OOO000O0OO :#line:202
                    if O00O000OOO000O0OO .status ==200 :#line:203
                        O0OO00OO00000O0OO =await O00O000OOO000O0OO .json ()#line:204
                        return O0OO00OO00000O0OO ['body']#line:205
                    else :#line:206
                        return await O0OOO00OO0000O0O0 .retry_with_backoff (O00O0O00O0O00000O ,3 ,'H5st')#line:207
        return await O0OOO00OO0000O0O0 .retry_with_backoff (O00O0O00O0O00000O ,3 ,'H5st')#line:209
    async def Get_H5_Api (O000O00O00OOOOO0O ,OOOOOO0O00O0O0O0O ,OOOOO0OOOO0OOO000 ,O00O0O00OOOOO0O00 ,O0O0O00O000000O00 ):#line:211
        async def O00O000OOO0OOOOOO (O0OO0O0OOO00OO0O0 ):#line:212
            if O000O00O00OOOOO0O .verify_result !=True :#line:213
                O000O00O00OOOOO0O .log .error ("授权未通过 退出")#line:214
                sys .exit ()#line:215
            O0O0O0O00OO0OO0OO =generate_random_user_agent ()#line:216
            O0O00O0OO0OO0O0OO ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":O00O0O00OOOOO0O00 ,"User-Agent":O0O0O0O00OO0OO0OO }#line:228
            OO000O0OOO0O00OO0 =getUUID ("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")#line:229
            O0OO0O0OOO00OO0O0 =await O000O00O00OOOOO0O .Get_H5st (OOOOOO0O00O0O0O0O ,O0OO0O0OOO00OO0O0 ,O0O0O0O00OO0OO0OO ,O0O0O00O000000O00 ,O00O0O00OOOOO0O00 )#line:230
            O00OO0O0OO00OOOOO ="https://api.m.jd.com"#line:232
            async with aiohttp .ClientSession ()as O0O00O00O00O0O0O0 :#line:233
                if O000O00O00OOOOO0O .proxy ==False :#line:234
                    async with O0O00O00O00O0O0O0 .post (O00OO0O0OO00OOOOO ,headers =O0O00O0OO0OO0O0OO ,data =O0OO0O0OOO00OO0O0 ,timeout =5 )as O00000O0OOO0O0OOO :#line:235
                        if O00000O0OOO0O0OOO .status ==200 :#line:236
                            return await O00000O0OOO0O0OOO .json ()#line:237
                        else :#line:239
                            O000O00O00OOOOO0O .log .error (f'重试 请求结果：{O00000O0OOO0O0OOO.status}')#line:240
                else :#line:241
                    async with O0O00O00O00O0O0O0 .post (O00OO0O0OO00OOOOO ,headers =O0O00O0OO0OO0O0OO ,data =O0OO0O0OOO00OO0O0 ,timeout =5 ,proxy =O000O00O00OOOOO0O .proxy )as O00000O0OOO0O0OOO :#line:242
                        if O00000O0OOO0O0OOO .status ==200 :#line:243
                            return await O00000O0OOO0O0OOO .json ()#line:244
                        else :#line:245
                            O000O00O00OOOOO0O .log .error (f'重试 请求结果：{O00000O0OOO0O0OOO.status}')#line:246
                            await O000O00O00OOOOO0O .Get_H5_Api (OOOOOO0O00O0O0O0O ,O0OO0O0OOO00OO0O0 ,O00O0O00OOOOO0O00 ,O0O0O00O000000O00 )#line:247
        return await O000O00O00OOOOO0O .retry_with_backoff (lambda :O00O000OOO0OOOOOO (OOOOO0OOOO0OOO000 ),3 ,'H5st_Api')#line:249
    async def Result (OO000OO00OO00OOO0 ,OOOO0O0000000OOO0 ,OOO000OO00O0000O0 ,OOOOOO000OOO0OOO0 ):#line:251
        if OO000OO00OO00OOO0 .exit_condition and len (OO000OO00OO00OOO0 .power_success )>=OO000OO00OO00OOO0 .exit_condition :#line:252
            sys .exit ()#line:253
        async def O00OO0OO0O0OO00OO ():#line:255
            OO00OOO00OO000000 =False #line:256
            if OO000OO00OO00OOO0 .verify_result !=True :#line:257
                OO000OO00OO00OOO0 .log .error ("授权未通过 退出")#line:258
                sys .exit ()#line:259
            for O0000OOO0000OOOO0 in OO000OO00OO00OOO0 .linkId :#line:260
                OOO0000O0OOOO000O =await OO000OO00OO00OOO0 .Get_H5_Api ("inviteFissionhelp",{'linkId':O0000OOO0000OOOO0 ,"isJdApp":True ,'inviter':OOO000OO00O0000O0 },OOOOOO000OOO0OOO0 ,'c5389')#line:263
                if int (OOO0000O0OOOO000O ['code'])==0 :#line:264
                    for OO00OOO0OOO000OO0 ,O0O0O0OO0000OO000 in OO000OO00OO00OOO0 .helpResult :#line:265
                        if OOO0000O0OOOO000O ['data']['helpResult']==int (OO00OOO0OOO000OO0 ):#line:266
                            OO00OOO00OO000000 =True #line:267
                            OO000OO00OO00OOO0 .log .info (f"Id:{O0000OOO0000OOOO0[:4] + '****' + O0000OOO0000OOOO0[-4:]}|助理:{OOO0000O0OOOO000O['data']['nickName']}|{OOO0000O0OOOO000O['data']['helpResult']}|第{OOOO0O0000000OOO0}次|{OO000OO00OO00OOO0.pt_pin(OOOOOO000OOO0OOO0)}|{O0O0O0OO0000OO000}")#line:269
                            if OOO0000O0OOOO000O ['data']['helpResult']==1 :#line:270
                                OO000OO00OO00OOO0 .power_success .append (OOOOOO000OOO0OOO0 )#line:271
                            else :#line:272
                                OO000OO00OO00OOO0 .power_failure .append (OOOOOO000OOO0OOO0 )#line:273
                    if not OO00OOO00OO000000 :#line:274
                        O0O0O0OO0000OO000 ='❌未知状态 (可能是活动未开启！！！)'#line:275
                        OO000OO00OO00OOO0 .power_failure .append (OOOOOO000OOO0OOO0 )#line:276
                        OO000OO00OO00OOO0 .log .info (f"Id:{O0000OOO0000OOOO0[:4] + '****' + O0000OOO0000OOOO0[-4:]}|助理:{OOO0000O0OOOO000O['data']['nickName']}|{OOO0000O0OOOO000O['data']['helpResult']}|第{OOOO0O0000000OOO0}次|{OO000OO00OO00OOO0.pt_pin(OOOOOO000OOO0OOO0)}|{O0O0O0OO0000OO000}")#line:278
                else :#line:279
                    OO000OO00OO00OOO0 .log .info (f"{OO000OO00OO00OOO0.pt_pin(OOOOOO000OOO0OOO0)}{OOO0000O0OOOO000O['code']} 结果:💔{OOO0000O0OOOO000O['errMsg']}")#line:280
                    OO000OO00OO00OOO0 .not_log .append (OOOOOO000OOO0OOO0 )#line:281
        return await OO000OO00OO00OOO0 .retry_with_backoff (O00OO0OO0O0OO00OO ,3 ,'Result')#line:283
    async def main (OOOO0O0O0O000OOO0 ):#line:285
        await OOOO0O0O0O000OOO0 .verify ()#line:286
        await OOOO0O0O0O000OOO0 .LinkId ()#line:287
        if OOOO0O0O0O000OOO0 .verify_result !=True :#line:288
            await OOOO0O0O0O000OOO0 .verify ()#line:289
        if OOOO0O0O0O000OOO0 .verify_result !=True :#line:290
            OOOO0O0O0O000OOO0 .log .error ("授权未通过 退出")#line:291
            sys .exit ()#line:292
        for O0O0OO00000O00000 in OOOO0O0O0O000OOO0 .linkId :#line:293
            OO000OOOO0OO0OOO0 =await OOOO0O0O0O000OOO0 .Get_H5_Api ("inviteFissionhelp",{'linkId':O0O0OO00000O00000 ,"isJdApp":True ,'inviter':OOOO0O0O0O000OOO0 .inviter_help },OOOO0O0O0O000OOO0 .coookie ,'c5389')#line:296
            if OO000OOOO0OO0OOO0 ['success']==False and OO000OOOO0OO0OOO0 ['code']==1000 :#line:297
                OOOO0O0O0O000OOO0 .log .info (f"{OO000OOOO0OO0OOO0['errMsg']}")#line:298
                sys .exit ()#line:299
            if OO000OOOO0OO0OOO0 ['data']['helpResult']==1 :#line:300
                OOOO0O0O0O000OOO0 .log .info (f'{OOOO0O0O0O000OOO0.pt_pin(OOOO0O0O0O000OOO0.coookie)} ✅助力作者成功 谢谢你 你是个好人！！！')#line:301
            else :#line:302
                OOOO0O0O0O000OOO0 .log .info (f'{OOOO0O0O0O000OOO0.pt_pin(OOOO0O0O0O000OOO0.coookie)} ❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:303
        if OOOO0O0O0O000OOO0 .inviter ==False :#line:305
            for O0O0OO00000O00000 in OOOO0O0O0O000OOO0 .linkId :#line:306
                OO000OOOO0OO0OOO0 =await OOOO0O0O0O000OOO0 .Get_H5_Api ('inviteFissionHome',{'linkId':O0O0OO00000O00000 ,"inviter":"",},OOOO0O0O0O000OOO0 .coookie ,'eb67b')#line:308
                OOOO0O0O0O000OOO0 .log .info (f'{OOOO0O0O0O000OOO0.pt_pin(OOOO0O0O0O000OOO0.coookie)} ⏰剩余时间:{OOOO0O0O0O000OOO0.convert_ms_to_hours_minutes(OO000OOOO0OO0OOO0["data"]["countDownTime"])} 🎉已获取助力:{OO000OOOO0OO0OOO0["data"]["prizeNum"] + OO000OOOO0OO0OOO0["data"]["drawPrizeNum"]}次 ✅【LinkId】:{O0O0OO00000O00000}')#line:310
                OOOO0O0O0O000OOO0 .inviter =OO000OOOO0OO0OOO0 ["data"]["inviter"]#line:311
            OOOO0O0O0O000OOO0 .log .info (f'{OOOO0O0O0O000OOO0.pt_pin(OOOO0O0O0O000OOO0.coookie)} ✅助理码: {OOOO0O0O0O000OOO0.inviter}')#line:312
        if OOOO0O0O0O000OOO0 .proxy !=False :#line:314
            OOOO0O0O0O000OOO0 .log .info (f"##############开始并发[线程数:{OOOO0O0O0O000OOO0.semaphore._value}]##############")#line:315
            OOOOO0OOO0000OOO0 =[]#line:316
            async def O0OO0000000O0O0O0 (OOO00O000OOOOO0OO ,OOO0O0OO00OOOOO00 ):#line:324
                async with OOOO0O0O0O000OOO0 .semaphore :#line:325
                    O00000O0O0O000OOO =asyncio .create_task (OOOO0O0O0O000OOO0 .Result (OOO00O000OOOOO0OO ,OOOO0O0O0O000OOO0 .inviter ,OOO0O0OO00OOOOO00 ))#line:326
                    if OOOO0O0O0O000OOO0 .exit_condition and len (OOOO0O0O0O000OOO0 .power_success )>=OOOO0O0O0O000OOO0 .exit_condition :#line:327
                        sys .exit ()#line:328
                    return await O00000O0O0O000OOO #line:329
            async def O0OOO0OO0O0O00OOO ():#line:331
                OO00000O0000O000O =[]#line:332
                for O00OO0OOO0000OOOO ,OOO0O00O0000OOOOO in enumerate (ck ,1 ):#line:333
                    if OOOO0O0O0O000OOO0 .exit_condition and len (OOOO0O0O0O000OOO0 .power_success )>=OOOO0O0O0O000OOO0 .exit_condition :#line:334
                        sys .exit ()#line:335
                    OOOO0OO0OO0O0OOOO =asyncio .create_task (O0OO0000000O0O0O0 (O00OO0OOO0000OOOO ,OOO0O00O0000OOOOO ))#line:336
                    OO00000O0000O000O .append (OOOO0OO0OO0O0OOOO )#line:337
                await asyncio .gather (*OO00000O0000O000O )#line:339
            await O0OOO0OO0O0O00OOO ()#line:342
        else :#line:348
            OOOO0O0O0O000OOO0 .log .info (f"##############开始任务##############")#line:349
            for OOO0O0OO000OOO0O0 ,OO00O0O0000OOOO00 in enumerate (ck ,1 ):#line:350
                await OOOO0O0O0O000OOO0 .Result (OOO0O0OO000OOO0O0 ,OOOO0O0O0O000OOO0 .inviter ,OO00O0O0000OOOO00 )#line:351
                if OOOO0O0O0O000OOO0 .exit_condition and len (OOOO0O0O0O000OOO0 .power_success )>=OOOO0O0O0O000OOO0 .exit_condition :#line:352
                    sys .exit ()#line:353
                await asyncio .sleep (0.5 )#line:354
        OOOO0O0O0O000OOO0 .log .info (f"##############清点人数##############")#line:356
        OOOO0O0O0O000OOO0 .log .info (f"✅助力成功:{len(OOOO0O0O0O000OOO0.power_success)}人 ❌助力失败:{len(OOOO0O0O0O000OOO0.power_failure)}人 💔未登录CK{len(OOOO0O0O0O000OOO0.not_log)}人")#line:358
        OOOO0O0O0O000OOO0 .log .info (f" ⏰耗时:{time.time() - OOOO0O0O0O000OOO0.start}")#line:359
if __name__ =='__main__':#line:362
    pdd =TEN_JD_PDD ()#line:363
    loop =asyncio .get_event_loop ()#line:364
    loop .run_until_complete (pdd .main ())#line:365
    loop .close ()#line:366
