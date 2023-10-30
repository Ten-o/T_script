#!/usr/bin/env python3
"""
File: TEN_JD_PDD.py(邀好友赢现金-助理)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-助理');
"""
#!/usr/bin/env python3
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
    def __init__ (OO0O00000O0O00OO0 ):#line:28
        OO0O00000O0O00OO0 .log =setup_logger ()#line:29
        OO0O00000O0O00OO0 .start =time .time ()#line:30
        OO0O00000O0O00OO0 .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:32
        OO0O00000O0O00OO0 .inviter =os .environ .get ("TEN_inviter")if os .environ .get ("TEN_inviter")else False #line:33
        OO0O00000O0O00OO0 .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:34
        OO0O00000O0O00OO0 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:35
        OO0O00000O0O00OO0 .semaphore =asyncio .Semaphore (int (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 50 ))#line:36
        OO0O00000O0O00OO0 .power_success =[]#line:37
        OO0O00000O0O00OO0 .power_failure =[]#line:38
        OO0O00000O0O00OO0 .not_log =[]#line:39
        OO0O00000O0O00OO0 .exit_event =threading .Event ()#line:40
        OO0O00000O0O00OO0 .coookie =ck [0 ]#line:41
        OO0O00000O0O00OO0 .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:48
        OO0O00000O0O00OO0 .verify_result =False #line:49
        OO0O00000O0O00OO0 .linkId =[]#line:50
        OO0O00000O0O00OO0 .inviter_help =''#line:51
        OO0O00000O0O00OO0 .version ='1.3.6'#line:52
        OO0O00000O0O00OO0 .exit_condition =9999 #line:53
        OO0O00000O0O00OO0 .lock =threading .Lock ()#line:54
    def pt_pin (OO00000O000OO0OOO ,O0O0000OOO00000OO ):#line:56
        try :#line:57
            O0O0OO0OOOO0OO000 =re .compile (r'pt_pin=(.*?);').findall (O0O0000OOO00000OO )[0 ]#line:58
            O0O0OO0OOOO0OO000 =unquote_plus (O0O0OO0OOOO0OO000 )#line:59
        except IndexError :#line:60
            O0O0OO0OOOO0OO000 =re .compile (r'pin=(.*?);').findall (O0O0000OOO00000OO )[0 ]#line:61
            O0O0OO0OOOO0OO000 =unquote_plus (O0O0OO0OOOO0OO000 )#line:62
        return O0O0OO0OOOO0OO000 #line:63
    def convert_ms_to_hours_minutes (OOOO0O0O0OO00O00O ,O0O00OO00O0OO00O0 ):#line:77
        OOO0OO00O0O0O000O =O0O00OO00O0OO00O0 //1000 #line:78
        OOOOOOO00O0OOOOOO ,OOO0OO00O0O0O000O =divmod (OOO0OO00O0O0O000O ,60 )#line:79
        OOO0OO00OO0000OO0 ,OOOOOOO00O0OOOOOO =divmod (OOOOOOO00O0OOOOOO ,60 )#line:80
        return f'{OOO0OO00OO0000OO0}:{OOOOOOO00O0OOOOOO}'#line:81
    def list_of_groups (O0OOO00O0O0OO0O0O ,O0000O0OOO0OO0OO0 ,O0OOOO0O00OO0O0O0 ):#line:83
        O000OO0OO0OOO00OO =zip (*(iter (O0000O0OOO0OO0OO0 ),)*O0OOOO0O00OO0O0O0 )#line:84
        O0OO00O00OOOOO0OO =[list (OOO0O00O0OO0OO0O0 )for OOO0O00O0OO0OO0O0 in O000OO0OO0OOO00OO ]#line:85
        O0OO0O0OO0O00O0O0 =len (O0000O0OOO0OO0OO0 )%O0OOOO0O00OO0O0O0 #line:86
        O0OO00O00OOOOO0OO .append (O0000O0OOO0OO0OO0 [-O0OO0O0OO0O00O0O0 :])if O0OO0O0OO0O00O0O0 !=0 else O0OO00O00OOOOO0OO #line:87
        return O0OO00O00OOOOO0OO #line:88
    async def retry_with_backoff (OOOOOOOO0O00O000O ,O0OOO000O000000OO ,OOO0O0O00OO0OO0O0 ,OOOO00000OO0OOO00 ,backoff_seconds =0 ):#line:90
        for OO00OO00OOOOO0O00 in range (OOO0O0O00OO0OO0O0 ):#line:91
            O0O0O00O00OOO00O0 =False #line:92
            try :#line:93
                return await O0OOO000O000000OO ()#line:94
            except asyncio .TimeoutError :#line:95
                if not O0O0O00O00OOO00O0 :#line:96
                    OOOOOOOO0O00O000O .log .warning (f'第{OO00OO00OOOOO0O00 + 1}次重试 {OOOO00000OO0OOO00} 请求超时')#line:97
                    O0O0O00O00OOO00O0 =True #line:98
                await asyncio .sleep (backoff_seconds )#line:99
            except Exception as OO0O0OO0O0O0OO0OO :#line:100
                if not O0O0O00O00OOO00O0 :#line:101
                    OOOOOOOO0O00O000O .log .warning (f'第{OO00OO00OOOOO0O00 + 1}次重试 {OOOO00000OO0OOO00} 出错：{OO0O0OO0O0O0OO0OO}')#line:102
                    O0O0O00O00OOO00O0 =True #line:103
                await asyncio .sleep (backoff_seconds )#line:104
            if O0O0O00O00OOO00O0 and OO00OO00OOOOO0O00 ==OOO0O0O00OO0OO0O0 -1 :#line:106
                OOOOOOOO0O00O000O .log .error (f'{OOOO00000OO0OOO00} 重试{OOO0O0O00OO0OO0O0}次后仍然发生异常')#line:107
                return False ,False ,False #line:108
    async def verify (O000OOOOOOO00OO00 ):#line:111
        O000OOOOOOO00OO00 .verify_result =True #line:112
        async def OO000O0OOOOOOOOO0 ():#line:113
            OOO0OOO0OOO00000O ='https://api.ixu.cc/verify'#line:114
            async with aiohttp .ClientSession ()as OO0O000O0000000O0 :#line:115
                async with OO0O000O0000000O0 .get (OOO0OOO0OOO00000O ,data ={'TOKEN':O000OOOOOOO00OO00 .token },timeout =3 )as OO0O00O0O000O00O0 :#line:116
                    OOOOO0OOOOO000O00 =await OO0O00O0O000O00O0 .json ()#line:117
                    if OO0O00O0O000O00O0 .status ==200 :#line:118
                        O000OOOOOOO00OO00 .verify_result =True #line:119
                        O000OOOOOOO00OO00 .log .info (f'认证通过 UserId：{OOOOO0OOOOO000O00["user_id"]}')#line:120
                        return OOOOO0OOOOO000O00 #line:121
                    else :#line:122
                        O000OOOOOOO00OO00 .log .error (f"授权未通过:{OOOOO0OOOOO000O00['error']}")#line:123
                        sys .exit ()#line:124
        return await O000OOOOOOO00OO00 .retry_with_backoff (OO000O0OOOOOOOOO0 ,3 ,'verify')#line:126
    def parse_version (OO0OOOO0000O0000O ,O0O00O0O000OOO00O ):#line:128
        return list (map (int ,O0O00O0O000OOO00O .split ('.')))#line:129
    def is_major_update (OO0OO00OOOOOOOO00 ,OO0O0O000OO000000 ,O00OO0OO00O00O0OO ):#line:131
        if OO0O0O000OO000000 [1 ]!=O00OO0OO00O00O0OO [1 ]:#line:132
            return True #line:133
        elif OO0O0O000OO000000 [0 ]!=O00OO0OO00O00O0OO [0 ]:#line:134
            return True #line:135
        else :#line:136
            return False #line:137
    def is_force_update (O000OO00O0OOO00OO ,OOO000OO00000OO0O ,O00O0OOO0OOO00000 ):#line:139
        if O000OO00O0OOO00OO .is_major_update (OOO000OO00000OO0O ,O00O0OOO0OOO00000 ):#line:140
            return True #line:141
        elif O00O0OOO0OOO00000 [2 ]-OOO000OO00000OO0O [2 ]>=3 :#line:142
            return True #line:143
        elif O00O0OOO0OOO00000 [2 ]<OOO000OO00000OO0O [2 ]:#line:144
            return True #line:145
        else :#line:146
            return False #line:147
    async def LinkId (O0O0O00O00OOO0OO0 ):#line:149
        async def OO0O0O0OOOO000O00 ():#line:150
            if O0O0O00O00OOO0OO0 .verify_result !=True :#line:151
                await O0O0O00O00OOO0OO0 .verify ()#line:152
            if O0O0O00O00OOO0OO0 .verify_result !=True :#line:153
                O0O0O00O00OOO0OO0 .log .error ("授权未通过 退出")#line:154
                sys .exit ()#line:155
            OO000O0O000OOOOO0 ='https://api.ixu.cc/status/inviter.json'#line:156
            async with aiohttp .ClientSession ()as OO0O00OO000000OO0 :#line:157
                async with OO0O00OO000000OO0 .get (OO000O0O000OOOOO0 ,timeout =3 )as O00O0O000OO0O0000 :#line:158
                    if O00O0O000OO0O0000 .status ==200 :#line:159
                        OO0OOOO00O0O000O0 =await O00O0O000OO0O0000 .json ()#line:160
                        if OO0OOOO00O0O000O0 ['stats']!='True':#line:161
                            O0O0O00O00OOO0OO0 .log .error (f"{OO0OOOO00O0O000O0['err_text']}")#line:162
                            sys .exit ()#line:163
                        O0O0O00O00OOO0OO0 .inviter_help =OO0OOOO00O0O000O0 ['inviter']#line:164
                        if O0O0O00O00OOO0OO0 .is_force_update (O0O0O00O00OOO0OO0 .parse_version (O0O0O00O00OOO0OO0 .version ),O0O0O00O00OOO0OO0 .parse_version (OO0OOOO00O0O000O0 ["version"])):#line:165
                            O0O0O00O00OOO0OO0 .log .error (f'强制更新 云端版本:{OO0OOOO00O0O000O0["version"]},当前版本:{O0O0O00O00OOO0OO0.version} {OO0OOOO00O0O000O0["upload_text"]}')#line:167
                            sys .exit ()#line:168
                        else :#line:169
                            O0O0O00O00OOO0OO0 .log .debug (f'云端版本:{OO0OOOO00O0O000O0["version"]},当前版本:{O0O0O00O00OOO0OO0.version}')#line:170
                        if len (OO0OOOO00O0O000O0 ['text'])>0 :#line:171
                            O0O0O00O00OOO0OO0 .log .debug (f'那女孩对你说:{OO0OOOO00O0O000O0["text"]}')#line:172
                        if O0O0O00O00OOO0OO0 .scode =='ALL'or O0O0O00O00OOO0OO0 .scode =='all':#line:173
                            for OO0OOOO0O0O0O0OO0 in OO0OOOO00O0O000O0 ['linkId']:#line:174
                                O0O0O00O00OOO0OO0 .linkId .append (OO0OOOO0O0O0O0OO0 )#line:175
                                O0O0O00O00OOO0OO0 .log .info (f'云端获取到linkId:{OO0OOOO0O0O0O0OO0}')#line:176
                            return True #line:177
                        else :#line:178
                            O0O0O00O00OOO0OO0 .linkId .append (OO0OOOO00O0O000O0 ['linkId'][int (O0O0O00O00OOO0OO0 .scode )-1 ])#line:179
                            O0O0O00O00OOO0OO0 .log .info (f'云端获取到linkId:{OO0OOOO00O0O000O0["linkId"][int(O0O0O00O00OOO0OO0.scode) - 1]}')#line:180
                            return True #line:181
                    else :#line:182
                        O0O0O00O00OOO0OO0 .log .error ('未获取到linkId 重试')#line:183
        return await O0O0O00O00OOO0OO0 .retry_with_backoff (OO0O0O0OOOO000O00 ,3 ,'linkId')#line:185
    async def Get_H5st (O00OOO0OOOOO0O0OO ,O00000OOOOOO000O0 ,O00O0OO0OO00O0O00 ,OO00OOO000O000OO0 ,O0OO000O00OOOOOOO ,OO00000O0000OOOOO ):#line:187
        async def O0OOO00O00OOOO00O ():#line:188
            if O00OOO0OOOOO0O0OO .verify_result !=True :#line:189
                O00OOO0OOOOO0O0OO .log .error ("授权未通过 退出")#line:190
                sys .exit ()#line:191
            O0O0OOO0OO0OO00OO ='https://api.ouklc.com/api/h5st'#line:192
            O00O0OO00O000OO0O =O00OOO0OOOOO0O0OO .pt_pin (OO00000O0000OOOOO )#line:193
            OOOOOO000OO0O0O00 ={'functionId':O00000OOOOOO000O0 ,'body':json .dumps (O00O0OO0OO00O0O00 ),'ua':OO00OOO000O000OO0 ,'pin':O00O0OO00O000OO0O ,'appId':O0OO000O00OOOOOOO }#line:200
            async with aiohttp .ClientSession ()as O000OO0O00000000O :#line:201
                async with O000OO0O00000000O .get (O0O0OOO0OO0OO00OO ,params =OOOOOO000OO0O0O00 ,timeout =10 )as OOOO00O0OOO00O000 :#line:202
                    if OOOO00O0OOO00O000 .status ==200 :#line:203
                        O000O0O0OOO0OOOO0 =await OOOO00O0OOO00O000 .json ()#line:204
                        return O000O0O0OOO0OOOO0 ['body']#line:205
                    else :#line:206
                        return await O00OOO0OOOOO0O0OO .retry_with_backoff (O0OOO00O00OOOO00O ,3 ,'H5st')#line:207
        return await O00OOO0OOOOO0O0OO .retry_with_backoff (O0OOO00O00OOOO00O ,3 ,'H5st')#line:209
    async def Get_H5_Api (O0O00O0000000000O ,O00O000000O0OOO0O ,OO0O00O0O00O00O0O ,O0000OO000OO00OO0 ,O0OOO00O0O0O0OO0O ):#line:211
        async def OO0OOO0O00OO00000 (O0000O0O0O00OOOOO ):#line:212
            if O0O00O0000000000O .verify_result !=True :#line:213
                O0O00O0000000000O .log .error ("授权未通过 退出")#line:214
                sys .exit ()#line:215
            OOO0O0O00O00OOO00 =generate_random_user_agent ()#line:216
            O0OOOOOO0OO0OOOO0 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":O0000OO000OO00OO0 ,"User-Agent":OOO0O0O00O00OOO00 }#line:228
            OO0O0OOOOOO00OOO0 =getUUID ("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")#line:229
            O0000O0O0O00OOOOO =await O0O00O0000000000O .Get_H5st (O00O000000O0OOO0O ,O0000O0O0O00OOOOO ,OOO0O0O00O00OOO00 ,O0OOO00O0O0O0OO0O ,O0000OO000OO00OO0 )#line:230
            OO00O00OOOO00OO00 ="https://api.m.jd.com"#line:232
            async with aiohttp .ClientSession ()as OOOO0OO00O00OO0O0 :#line:233
                if O0O00O0000000000O .proxy ==False :#line:234
                    async with OOOO0OO00O00OO0O0 .post (OO00O00OOOO00OO00 ,headers =O0OOOOOO0OO0OOOO0 ,data =O0000O0O0O00OOOOO ,timeout =5 )as O000OOOO00OOOOOOO :#line:235
                        if O000OOOO00OOOOOOO .status ==200 :#line:236
                            return await O000OOOO00OOOOOOO .json ()#line:237
                        else :#line:239
                            O0O00O0000000000O .log .error (f'重试 请求结果：{O000OOOO00OOOOOOO.status}')#line:240
                else :#line:241
                    async with OOOO0OO00O00OO0O0 .post (OO00O00OOOO00OO00 ,headers =O0OOOOOO0OO0OOOO0 ,data =O0000O0O0O00OOOOO ,timeout =5 ,proxy =O0O00O0000000000O .proxy )as O000OOOO00OOOOOOO :#line:242
                        if O000OOOO00OOOOOOO .status ==200 :#line:243
                            return await O000OOOO00OOOOOOO .json ()#line:244
                        else :#line:245
                            O0O00O0000000000O .log .error (f'重试 请求结果：{O000OOOO00OOOOOOO.status}')#line:246
                            await O0O00O0000000000O .Get_H5_Api (O00O000000O0OOO0O ,O0000O0O0O00OOOOO ,O0000OO000OO00OO0 ,O0OOO00O0O0O0OO0O )#line:247
        return await O0O00O0000000000O .retry_with_backoff (lambda :OO0OOO0O00OO00000 (OO0O00O0O00O00O0O ),3 ,'H5st_Api')#line:249
    async def Result (O00O000000O0OOO00 ,OO000O0OOOOOO00OO ,OO000O0O0OOO00O00 ,OO0O0OO0OO0000OO0 ):#line:251
        if O00O000000O0OOO00 .exit_condition and len (O00O000000O0OOO00 .power_success )>=O00O000000O0OOO00 .exit_condition :#line:252
            sys .exit ()#line:253
        async def OOO0000O0OOO0OO0O ():#line:255
            O0OO0O0O0OOO000O0 =False #line:256
            if O00O000000O0OOO00 .verify_result !=True :#line:257
                O00O000000O0OOO00 .log .error ("授权未通过 退出")#line:258
                sys .exit ()#line:259
            for O00OOO00O00O00OOO in O00O000000O0OOO00 .linkId :#line:260
                OOOO000O0O00OO0O0 =await O00O000000O0OOO00 .Get_H5_Api ("inviteFissionhelp",{'linkId':O00OOO00O00O00OOO ,"isJdApp":True ,'inviter':OO000O0O0OOO00O00 },OO0O0OO0OO0000OO0 ,'c5389')#line:263
                if int (OOOO000O0O00OO0O0 ['code'])==0 :#line:264
                    for OOOOO000O0O00O000 ,O0000O0OO0O000000 in O00O000000O0OOO00 .helpResult :#line:265
                        if OOOO000O0O00OO0O0 ['data']['helpResult']==int (OOOOO000O0O00O000 ):#line:266
                            O0OO0O0O0OOO000O0 =True #line:267
                            O00O000000O0OOO00 .log .info (f"Id:{O00OOO00O00O00OOO[:4] + '****' + O00OOO00O00O00OOO[-4:]}|助理:{OOOO000O0O00OO0O0['data']['nickName']}|{OOOO000O0O00OO0O0['data']['helpResult']}|第{OO000O0OOOOOO00OO}次|{O00O000000O0OOO00.pt_pin(OO0O0OO0OO0000OO0)}|{O0000O0OO0O000000}")#line:269
                            if OOOO000O0O00OO0O0 ['data']['helpResult']==1 :#line:270
                                O00O000000O0OOO00 .power_success .append (OO0O0OO0OO0000OO0 )#line:271
                            else :#line:272
                                O00O000000O0OOO00 .power_failure .append (OO0O0OO0OO0000OO0 )#line:273
                    if not O0OO0O0O0OOO000O0 :#line:274
                        O0000O0OO0O000000 ='❌未知状态 (可能是活动未开启！！！)'#line:275
                        O00O000000O0OOO00 .power_failure .append (OO0O0OO0OO0000OO0 )#line:276
                        O00O000000O0OOO00 .log .info (f"Id:{O00OOO00O00O00OOO[:4] + '****' + O00OOO00O00O00OOO[-4:]}|助理:{OOOO000O0O00OO0O0['data']['nickName']}|{OOOO000O0O00OO0O0['data']['helpResult']}|第{OO000O0OOOOOO00OO}次|{O00O000000O0OOO00.pt_pin(OO0O0OO0OO0000OO0)}|{O0000O0OO0O000000}")#line:278
                else :#line:279
                    O00O000000O0OOO00 .log .info (f"{O00O000000O0OOO00.pt_pin(OO0O0OO0OO0000OO0)}{OOOO000O0O00OO0O0['code']} 结果:💔{OOOO000O0O00OO0O0['errMsg']}")#line:280
                    O00O000000O0OOO00 .not_log .append (OO0O0OO0OO0000OO0 )#line:281
        return await O00O000000O0OOO00 .retry_with_backoff (OOO0000O0OOO0OO0O ,3 ,'Result')#line:283
    async def main (OO00OOO0OOOO0O00O ):#line:285
        await OO00OOO0OOOO0O00O .verify ()#line:286
        await OO00OOO0OOOO0O00O .LinkId ()#line:287
        if OO00OOO0OOOO0O00O .verify_result !=True :#line:288
            await OO00OOO0OOOO0O00O .verify ()#line:289
        if OO00OOO0OOOO0O00O .verify_result !=True :#line:290
            OO00OOO0OOOO0O00O .log .error ("授权未通过 退出")#line:291
            sys .exit ()#line:292
        for O0O000OO0OO0O00OO in OO00OOO0OOOO0O00O .linkId :#line:293
            O0OO00O0O0O0OOOOO =await OO00OOO0OOOO0O00O .Get_H5_Api ("inviteFissionhelp",{'linkId':O0O000OO0OO0O00OO ,"isJdApp":True ,'inviter':OO00OOO0OOOO0O00O .inviter_help },OO00OOO0OOOO0O00O .coookie ,'c5389')#line:296
            if O0OO00O0O0O0OOOOO ['success']==False and O0OO00O0O0O0OOOOO ['code']==1000 :#line:297
                OO00OOO0OOOO0O00O .log .info (f"{O0OO00O0O0O0OOOOO['errMsg']}")#line:298
                sys .exit ()#line:299
            if O0OO00O0O0O0OOOOO ['data']['helpResult']==1 :#line:300
                OO00OOO0OOOO0O00O .log .info (f'{OO00OOO0OOOO0O00O.pt_pin(OO00OOO0OOOO0O00O.coookie)} ✅助力作者成功 谢谢你 你是个好人！！！')#line:301
            else :#line:302
                OO00OOO0OOOO0O00O .log .info (f'{OO00OOO0OOOO0O00O.pt_pin(OO00OOO0OOOO0O00O.coookie)} ❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:303
        if OO00OOO0OOOO0O00O .inviter ==False :#line:305
            for O0O000OO0OO0O00OO in OO00OOO0OOOO0O00O .linkId :#line:306
                O0OO00O0O0O0OOOOO =await OO00OOO0OOOO0O00O .Get_H5_Api ('inviteFissionHome',{'linkId':O0O000OO0OO0O00OO ,"inviter":"",},OO00OOO0OOOO0O00O .coookie ,'af89e')#line:308
                OO00OOO0OOOO0O00O .log .info (f'{OO00OOO0OOOO0O00O.pt_pin(OO00OOO0OOOO0O00O.coookie)} ⏰剩余时间:{OO00OOO0OOOO0O00O.convert_ms_to_hours_minutes(O0OO00O0O0O0OOOOO["data"]["countDownTime"])} 🎉已获取助力:{O0OO00O0O0O0OOOOO["data"]["prizeNum"] + O0OO00O0O0O0OOOOO["data"]["drawPrizeNum"]}次 ✅【LinkId】:{O0O000OO0OO0O00OO}')#line:310
                OO00OOO0OOOO0O00O .inviter =O0OO00O0O0O0OOOOO ["data"]["inviter"]#line:311
            OO00OOO0OOOO0O00O .log .info (f'{OO00OOO0OOOO0O00O.pt_pin(OO00OOO0OOOO0O00O.coookie)} ✅助理码: {OO00OOO0OOOO0O00O.inviter}')#line:312
        if OO00OOO0OOOO0O00O .proxy !=False :#line:314
            OO00OOO0OOOO0O00O .log .info (f"##############开始并发[线程数:{OO00OOO0OOOO0O00O.semaphore._value}]##############")#line:315
            O0O00O00OO0OOO0O0 =[]#line:316
            async def O0O0O00OOO0OO0000 (OO0000O00O0O000O0 ,O0OO00OO00OO000O0 ):#line:324
                async with OO00OOO0OOOO0O00O .semaphore :#line:325
                    OOOO0OOO0O00OO0OO =asyncio .create_task (OO00OOO0OOOO0O00O .Result (OO0000O00O0O000O0 ,OO00OOO0OOOO0O00O .inviter ,O0OO00OO00OO000O0 ))#line:326
                    if OO00OOO0OOOO0O00O .exit_condition and len (OO00OOO0OOOO0O00O .power_success )>=OO00OOO0OOOO0O00O .exit_condition :#line:327
                        sys .exit ()#line:328
                    return await OOOO0OOO0O00OO0OO #line:329
            async def O00O00OO000OOOO00 ():#line:331
                OOOOOO000OO0OO00O =[]#line:332
                for O0OOO00O0O000OOOO ,OO0OO00O00O0000O0 in enumerate (ck ,1 ):#line:333
                    if OO00OOO0OOOO0O00O .exit_condition and len (OO00OOO0OOOO0O00O .power_success )>=OO00OOO0OOOO0O00O .exit_condition :#line:334
                        sys .exit ()#line:335
                    OO0OOOO00OOOO0000 =asyncio .create_task (O0O0O00OOO0OO0000 (O0OOO00O0O000OOOO ,OO0OO00O00O0000O0 ))#line:336
                    OOOOOO000OO0OO00O .append (OO0OOOO00OOOO0000 )#line:337
                await asyncio .gather (*OOOOOO000OO0OO00O )#line:339
            await O00O00OO000OOOO00 ()#line:342
        else :#line:348
            OO00OOO0OOOO0O00O .log .info (f"##############开始任务##############")#line:349
            for OOO0OOO00000OOO0O ,OOOOO00O0OO0OOO00 in enumerate (ck ,1 ):#line:350
                await OO00OOO0OOOO0O00O .Result (OOO0OOO00000OOO0O ,OO00OOO0OOOO0O00O .inviter ,OOOOO00O0OO0OOO00 )#line:351
                if OO00OOO0OOOO0O00O .exit_condition and len (OO00OOO0OOOO0O00O .power_success )>=OO00OOO0OOOO0O00O .exit_condition :#line:352
                    sys .exit ()#line:353
                await asyncio .sleep (0.5 )#line:354
        OO00OOO0OOOO0O00O .log .info (f"##############清点人数##############")#line:356
        OO00OOO0OOOO0O00O .log .info (f"✅助力成功:{len(OO00OOO0OOOO0O00O.power_success)}人 ❌助力失败:{len(OO00OOO0OOOO0O00O.power_failure)}人 💔未登录CK{len(OO00OOO0OOOO0O00O.not_log)}人")#line:358
        OO00OOO0OOOO0O00O .log .info (f" ⏰耗时:{time.time() - OO00OOO0OOOO0O00O.start}")#line:359
if __name__ =='__main__':#line:362
    pdd =TEN_JD_PDD ()#line:363
    loop =asyncio .get_event_loop ()#line:364
    loop .run_until_complete (pdd .main ())#line:365
    loop .close ()#line:366
