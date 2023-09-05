#!/usr/bin/env python3
""#line:9
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
    def __init__ (OOOOOOOOOOO0OOO0O ):#line:26
        OOOOOOOOOOO0OOO0O .log =setup_logger ()#line:27
        OOOOOOOOOOO0OOO0O .start =time .time ()#line:28
        OOOOOOOOOOO0OOO0O .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else 'b471c520-7adb-4716-9aac-dd2f8b623694' #line:30
        OOOOOOOOOOO0OOO0O .inviter =os .environ .get ("TEN_inviter")if os .environ .get ("TEN_inviter")else False #line:31
        OOOOOOOOOOO0OOO0O .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:32
        OOOOOOOOOOO0OOO0O .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:33
        OOOOOOOOOOO0OOO0O .semaphore =asyncio .Semaphore (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 3 )#line:34
        OOOOOOOOOOO0OOO0O .power_success =[]#line:35
        OOOOOOOOOOO0OOO0O .power_failure =[]#line:36
        OOOOOOOOOOO0OOO0O .not_log =[]#line:37
        OOOOOOOOOOO0OOO0O .exit_event =threading .Event ()#line:38
        OOOOOOOOOOO0OOO0O .coookie =ck [0 ]#line:39
        OOOOOOOOOOO0OOO0O .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:46
        OOOOOOOOOOO0OOO0O .verify_result =False #line:47
        OOOOOOOOOOO0OOO0O .linkId =[]#line:48
        OOOOOOOOOOO0OOO0O .inviter_help =''#line:49
        OOOOOOOOOOO0OOO0O .version ='1.3.5'#line:50
    def pt_pin (OOO00O000000000OO ,OO000O00OOO0OO0OO ):#line:52
        try :#line:53
            O00O0000OOO000OOO =re .compile (r'pt_pin=(.*?);').findall (OO000O00OOO0OO0OO )[0 ]#line:54
            O00O0000OOO000OOO =unquote_plus (O00O0000OOO000OOO )#line:55
        except IndexError :#line:56
            O00O0000OOO000OOO =re .compile (r'pin=(.*?);').findall (OO000O00OOO0OO0OO )[0 ]#line:57
            O00O0000OOO000OOO =unquote_plus (O00O0000OOO000OOO )#line:58
        return O00O0000OOO000OOO #line:59
    def convert_ms_to_hours_minutes (O0OOO00O00OO0OO0O ,OO0000OOOO000O0OO ):#line:60
        O0OOOO00OO0O0O00O =OO0000OOOO000O0OO //1000 #line:61
        OOOO00OOO00000OOO ,O0OOOO00OO0O0O00O =divmod (O0OOOO00OO0O0O00O ,60 )#line:62
        O00O000O00OOOO0OO ,OOOO00OOO00000OOO =divmod (OOOO00OOO00000OOO ,60 )#line:63
        return f'{O00O000O00OOOO0OO}:{OOOO00OOO00000OOO}'#line:64
    def list_of_groups (OO00OO0OO00O0OO00 ,O0OOOO0O0OO0000O0 ,O0000O000OOOOO0O0 ):#line:66
        OOOOOOO0OOO00O00O =zip (*(iter (O0OOOO0O0OO0000O0 ),)*O0000O000OOOOO0O0 )#line:67
        O0OO0O000000OOOOO =[list (O000OO0OOOOO0OO0O )for O000OO0OOOOO0OO0O in OOOOOOO0OOO00O00O ]#line:68
        OOO0OO0OOO00O0000 =len (O0OOOO0O0OO0000O0 )%O0000O000OOOOO0O0 #line:69
        O0OO0O000000OOOOO .append (O0OOOO0O0OO0000O0 [-OOO0OO0OOO00O0000 :])if OOO0OO0OOO00O0000 !=0 else O0OO0O000000OOOOO #line:70
        return O0OO0O000000OOOOO #line:71
    async def retry_with_backoff (O0OOO0O0OOO00OO00 ,O00O000O00O0OO00O ,OO00O0O00OO0OOO0O ,O0000OOO0OOOO00OO ,backoff_seconds =2 ):#line:73
        for O00O00000OOOOOOOO in range (OO00O0O00OO0OOO0O ):#line:75
            try :#line:76
                return await O00O000O00O0OO00O ()#line:77
            except asyncio .TimeoutError :#line:78
                O0OOO0O0OOO00OO00 .log .debug (f'第{O00O00000OOOOOOOO + 1}次重试  {O0000OOO0OOOO00OO} 请求超时')#line:79
                await asyncio .sleep (backoff_seconds )#line:80
            except Exception as O000000O0O000O00O :#line:81
                O0OOO0O0OOO00OO00 .log .debug (f'第{O00O00000OOOOOOOO + 1}次重试 {O0000OOO0OOOO00OO}出错：{O000000O0O000O00O}')#line:82
                await asyncio .sleep (backoff_seconds )#line:83
                if O00O00000OOOOOOOO ==OO00O0O00OO0OOO0O :#line:84
                    O0OOO0O0OOO00OO00 .log .error (f'{O0000OOO0OOOO00OO}重试{OO00O0O00OO0OOO0O}次后仍然发生异常')#line:85
                    return #line:86
    async def verify (O00OOOO0OOO00O000 ):#line:88
        async def OOOOO0OOO00O00O00 ():#line:89
            OO000OO0OO00OOOO0 ='https://api.ixu.cc/verify'#line:90
            async with aiohttp .ClientSession ()as O00O000OO0000OO0O :#line:91
                async with O00O000OO0000OO0O .get (OO000OO0OO00OOOO0 ,data ={'TOKEN':O00OOOO0OOO00O000 .token },timeout =3 )as O000O000O00O0OOO0 :#line:92
                    OO00OO00000O0OO00 =await O000O000O00O0OOO0 .json ()#line:93
                    if O000O000O00O0OOO0 .status ==200 :#line:94
                        O00OOOO0OOO00O000 .verify_result =True #line:95
                        O00OOOO0OOO00O000 .log .info (f'认证通过 UserId：{OO00OO00000O0OO00["user_id"]}')#line:96
                        return OO00OO00000O0OO00 #line:97
                    else :#line:98
                        O00OOOO0OOO00O000 .log .error (f"授权未通过:{OO00OO00000O0OO00['error']}")#line:99
                        sys .exit ()#line:100
        return await O00OOOO0OOO00O000 .retry_with_backoff (OOOOO0OOO00O00O00 ,3 ,'verify')#line:102
    def parse_version (OOO0OO00OO0O00OO0 ,OOO00000O0OOOO0O0 ):#line:104
        return list (map (int ,OOO00000O0OOOO0O0 .split ('.')))#line:105
    def is_major_update (O0OOO0OOO0OOO0O00 ,O00O00O000O00O000 ,O0O0O0OOOO0000O00 ):#line:107
        if O00O00O000O00O000 [1 ]!=O0O0O0OOOO0000O00 [1 ]:#line:108
            return True #line:109
        elif O00O00O000O00O000 [0 ]!=O0O0O0OOOO0000O00 [0 ]:#line:110
            return True #line:111
        else :#line:112
            return False #line:113
    def is_force_update (OOOO0O0O0O000O0OO ,O0O00000O0O00OO00 ,O0O000O0O0O00O000 ):#line:115
        if OOOO0O0O0O000O0OO .is_major_update (O0O00000O0O00OO00 ,O0O000O0O0O00O000 ):#line:116
            return True #line:117
        elif O0O00000O0O00OO00 [2 ]!=O0O000O0O0O00O000 [2 ]and O0O000O0O0O00O000 [2 ]>=3 :#line:118
            return True #line:119
        else :#line:120
            return False #line:121
    async def LinkId (O00OO00OO0OOO0000 ):#line:123
        async def O0OO00O000OOOO000 ():#line:124
            if O00OO00OO0OOO0000 .verify_result !=True :#line:125
                await O00OO00OO0OOO0000 .verify ()#line:126
            if O00OO00OO0OOO0000 .verify_result !=True :#line:127
                O00OO00OO0OOO0000 .log .error ("授权未通过 退出")#line:128
                sys .exit ()#line:129
            OO000OO00OOO0O000 ='https://api.ixu.cc/status/inviter.json'#line:130
            async with aiohttp .ClientSession ()as OOO0OO00O0O00O000 :#line:131
                async with OOO0OO00O0O00O000 .get (OO000OO00OOO0O000 ,params ={'TOKEN':O00OO00OO0OOO0000 .token },timeout =3 )as OO000OOO000O0OOO0 :#line:132
                    if OO000OOO000O0OOO0 .status ==200 :#line:133
                        OO00O00OOOOO0O0OO =await OO000OOO000O0OOO0 .json ()#line:134
                        if OO00O00OOOOO0O0OO ['stats']!='True':#line:135
                            O00OO00OO0OOO0000 .log .error (f"{OO00O00OOOOO0O0OO['err_text']}")#line:136
                            sys .exit ()#line:137
                        O00OO00OO0OOO0000 .inviter_help =OO00O00OOOOO0O0OO ['inviter']#line:138
                        if O00OO00OO0OOO0000 .is_force_update (O00OO00OO0OOO0000 .parse_version (O00OO00OO0OOO0000 .version ),O00OO00OO0OOO0000 .parse_version (OO00O00OOOOO0O0OO ["version"])):#line:139
                            O00OO00OO0OOO0000 .log .error (f'强制更新 云端版本:{OO00O00OOOOO0O0OO["version"]},当前版本:{O00OO00OO0OOO0000.version} {OO00O00OOOOO0O0OO["upload_text"]}')#line:140
                            sys .exit ()#line:141
                        else :#line:142
                            O00OO00OO0OOO0000 .log .debug (f'云端版本:{OO00O00OOOOO0O0OO["version"]},当前版本:{O00OO00OO0OOO0000.version}')#line:143
                        if len (OO00O00OOOOO0O0OO ['text'])>0 :#line:144
                            O00OO00OO0OOO0000 .log .debug (f'那女孩对你说:{OO00O00OOOOO0O0OO["text"]}')#line:145
                        if O00OO00OO0OOO0000 .scode =='ALL'or O00OO00OO0OOO0000 .scode =='all':#line:146
                            for O0OOOO000OO00O000 in OO00O00OOOOO0O0OO ['linkId']:#line:147
                                O00OO00OO0OOO0000 .linkId .append (O0OOOO000OO00O000 )#line:148
                                O00OO00OO0OOO0000 .log .info (f'云端获取到linkId:{O0OOOO000OO00O000}')#line:149
                            return True #line:150
                        else :#line:151
                            O00OO00OO0OOO0000 .linkId .append (OO00O00OOOOO0O0OO ['linkId'][int (O00OO00OO0OOO0000 .scode )-1 ])#line:152
                            O00OO00OO0OOO0000 .log .info (f'云端获取到linkId:{OO00O00OOOOO0O0OO["linkId"][int(O00OO00OO0OOO0000.scode) - 1]}')#line:153
                            return True #line:154
                    else :#line:155
                        O00OO00OO0OOO0000 .log .error ('未获取到linkId 重试')#line:156
        return await O00OO00OO0OOO0000 .retry_with_backoff (O0OO00O000OOOO000 ,3 ,'linkId')#line:157
    async def Get_H5st (OO0O0OOO0O0000O00 ,O00OOO00OOOOO0O0O ,OO0OOOO0OO0000OOO ,OOOO000O0OO000O0O ,O0000000OO00O0OOO ,OO0O00O000OO0O0O0 ):#line:162
        async def O00O0OOO0OO0O0OO0 ():#line:163
            if OO0O0OOO0O0000O00 .verify_result !=True :#line:164
                OO0O0OOO0O0000O00 .log .error ("授权未通过 退出")#line:165
                sys .exit ()#line:166
            OOO0O00O00O0O0OOO ='https://api.ouklc.com/api/h5st'#line:167
            OOOOO00OOOO000OOO =OO0O0OOO0O0000O00 .pt_pin (OO0O00O000OO0O0O0 )#line:168
            OOOO00OOOO00O000O ={'functionId':O00OOO00OOOOO0O0O ,'body':json .dumps (OO0OOOO0OO0000OOO ),'ua':OOOO000O0OO000O0O ,'pin':OOOOO00OOOO000OOO ,'appId':O0000000OO00O0OOO }#line:175
            async with aiohttp .ClientSession ()as OOO00OOOO0O00OOO0 :#line:176
                async with OOO00OOOO0O00OOO0 .get (OOO0O00O00O0O0OOO ,params =OOOO00OOOO00O000O ,timeout =10 )as O0OO0O0O0O0OOO0O0 :#line:177
                    if O0OO0O0O0O0OOO0O0 .status ==200 :#line:178
                        O0000O0O0O00O00OO =await O0OO0O0O0O0OOO0O0 .json ()#line:179
                        return O0000O0O0O00O00OO ['body']#line:180
                    else :#line:181
                        return await OO0O0OOO0O0000O00 .retry_with_backoff (O00O0OOO0OO0O0OO0 ,3 ,'H5st')#line:182
        return await OO0O0OOO0O0000O00 .retry_with_backoff (O00O0OOO0OO0O0OO0 ,3 ,'H5st')#line:184
    async def Get_H5_Api (OO00OO00O0O00O000 ,O0O00O00OO000O000 ,O0OOO0O00OO000000 ,O0OOOO0OOO0O0OO0O ,OOO0OO0O0O0000OOO ):#line:188
            async def OOO0O0OO000O0OO00 (O0000OO0OO0O000OO ):#line:189
                if OO00OO00O0O00O000 .verify_result !=True :#line:190
                    OO00OO00O0O00O000 .log .error ("授权未通过 退出")#line:191
                    sys .exit ()#line:192
                OOOO0000O0O000O00 =generate_random_user_agent ()#line:193
                OOO00OO0OO00OO000 ={"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/","Origin":"https://prodev.m.jd.com","Cookie":O0OOOO0OOO0O0OO0O ,"User-Agent":OOOO0000O0O000O00 }#line:205
                O0O00O0OO0O000OOO =getUUID ("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")#line:206
                O0000OO0OO0O000OO =await OO00OO00O0O00O000 .Get_H5st (O0O00O00OO000O000 ,O0000OO0OO0O000OO ,OOOO0000O0O000O00 ,OOO0OO0O0O0000OOO ,O0OOOO0OOO0O0OO0O )#line:207
                OOO0O0O00O0OOO00O =str (O0000OO0OO0O000OO )+"&x-api-eid-token="+cache_eid_token ()+f"&uuid={O0O00O0OO0O000OOO}&"#line:208
                OOOOOO0O000O0O0O0 ="https://api.m.jd.com"#line:209
                async with aiohttp .ClientSession ()as O0O00OOO0OO0O00O0 :#line:210
                    if OO00OO00O0O00O000 .proxy ==False :#line:211
                        async with O0O00OOO0OO0O00O0 .post (OOOOOO0O000O0O0O0 ,headers =OOO00OO0OO00OO000 ,data =OOO0O0O00O0OOO00O ,timeout =5 )as O000000O0O0OOOO0O :#line:212
                            if O000000O0O0OOOO0O .status ==200 :#line:213
                                return await O000000O0O0OOOO0O .json ()#line:214
                            else :#line:215
                                OO00OO00O0O00O000 .log .error (f'重试 请求结果：{O000000O0O0OOOO0O.status}')#line:216
                    else :#line:218
                        async with O0O00OOO0OO0O00O0 .post (OOOOOO0O000O0O0O0 ,headers =OOO00OO0OO00OO000 ,data =OOO0O0O00O0OOO00O ,timeout =5 ,proxy =OO00OO00O0O00O000 .proxy )as O000000O0O0OOOO0O :#line:219
                            if O000000O0O0OOOO0O .status ==200 :#line:220
                                return await O000000O0O0OOOO0O .json ()#line:221
                            else :#line:222
                                OO00OO00O0O00O000 .log .error (f'重试 请求结果：{O000000O0O0OOOO0O.status}')#line:223
                                await OO00OO00O0O00O000 .Get_H5_Api (O0O00O00OO000O000 ,OOO0O0O00O0OOO00O ,O0OOOO0OOO0O0OO0O ,OOO0OO0O0O0000OOO )#line:224
            return await OO00OO00O0O00O000 .retry_with_backoff (lambda :OOO0O0OO000O0OO00 (O0OOO0O00OO000000 ),3 ,'H5st_Api')#line:226
    async def Result (OO0OOOOOO0O0OOO0O ,OOOO00O0OOOO00O0O ,OOOOOO0O000OO0OO0 ):#line:228
        async def OO0O00000O0OOO00O ():#line:229
                if OO0OOOOOO0O0OOO0O .verify_result !=True :#line:230
                    OO0OOOOOO0O0OOO0O .log .error ("授权未通过 退出")#line:231
                    sys .exit ()#line:232
                for OO0000O00OO0000OO in OO0OOOOOO0O0OOO0O .linkId :#line:233
                    O0000O0OOO0O00OOO =await OO0OOOOOO0O0OOO0O .Get_H5_Api ("inviteFissionBeforeHome",{'linkId':OO0000O00OO0000OO ,"isJdApp":True ,'inviter':OOOO00O0OOOO00O0O },OOOOOO0O000OO0OO0 ,'02f8d')#line:234
                    if int (O0000O0OOO0O00OOO ['code'])==0 :#line:235
                        for OO0O0OOO0OOO0O0OO ,OOOOOO00O000OO000 in OO0OOOOOO0O0OOO0O .helpResult :#line:236
                            if O0000O0OOO0O00OOO ['data']['helpResult']==int (OO0O0OOO0OOO0O0OO ):#line:237
                                O0OO0OOOO00O0OOOO =True #line:238
                                OO0OOOOOO0O0OOO0O .log .info (f"{OO0OOOOOO0O0OOO0O.pt_pin(OOOOOO0O000OO0OO0)} linkId:{OO0000O00OO0000OO} 助理:{O0000O0OOO0O00OOO['data']['nickName']} 结果:{O0000O0OOO0O00OOO['data']['helpResult']} {OOOOOO00O000OO000}")#line:239
                                if O0000O0OOO0O00OOO ['data']['helpResult']==1 :#line:240
                                    OO0OOOOOO0O0OOO0O .power_success .append (OOOOOO0O000OO0OO0 )#line:241
                                else :#line:242
                                    OO0OOOOOO0O0OOO0O .power_failure .append (OOOOOO0O000OO0OO0 )#line:243
                        if not O0OO0OOOO00O0OOOO :#line:244
                            OOOOOO00O000OO000 ='❌未知状态 (可能是活动未开启！！！)'#line:245
                            OO0OOOOOO0O0OOO0O .power_failure .append (OOOOOO0O000OO0OO0 )#line:246
                            OO0OOOOOO0O0OOO0O .log .info (f"{OO0OOOOOO0O0OOO0O.pt_pin(OOOOOO0O000OO0OO0)} linkId:{OO0000O00OO0000OO} 助理:{O0000O0OOO0O00OOO['data']['nickName']} 结果:{O0000O0OOO0O00OOO['data']['helpResult']} {OOOOOO00O000OO000}")#line:247
                    else :#line:248
                        OO0OOOOOO0O0OOO0O .log .info (f"{OO0OOOOOO0O0OOO0O.pt_pin(OOOOOO0O000OO0OO0)}{O0000O0OOO0O00OOO['code']} 结果:💔{O0000O0OOO0O00OOO['errMsg']}")#line:249
                        OO0OOOOOO0O0OOO0O .not_log .append (OOOOOO0O000OO0OO0 )#line:250
        return await OO0OOOOOO0O0OOO0O .retry_with_backoff (OO0O00000O0OOO00O ,3 ,'Result')#line:251
    async def main (O000O0OOO0OO000O0 ):#line:254
        await O000O0OOO0OO000O0 .verify ()#line:255
        await O000O0OOO0OO000O0 .LinkId ()#line:256
        if O000O0OOO0OO000O0 .verify_result !=True :#line:257
            await O000O0OOO0OO000O0 .verify ()#line:258
        if O000O0OOO0OO000O0 .verify_result !=True :#line:259
            O000O0OOO0OO000O0 .log .error ("授权未通过 退出")#line:260
            sys .exit ()#line:261
        for O0O00O00O0O00O0OO in O000O0OOO0OO000O0 .linkId :#line:262
            O0O0O00O00O0O00OO =await O000O0OOO0OO000O0 .Get_H5_Api ("inviteFissionBeforeHome",{'linkId':O0O00O00O0O00O0OO ,"isJdApp":True ,'inviter':O000O0OOO0OO000O0 .inviter_help },O000O0OOO0OO000O0 .coookie ,'02f8d')#line:265
        if O0O0O00O00O0O00OO ['success']==False and O0O0O00O00O0O00OO ['code']==1000 :#line:266
            O000O0OOO0OO000O0 .log .info (f"{O0O0O00O00O0O00OO['errMsg']}")#line:267
            sys .exit ()#line:268
        if O0O0O00O00O0O00OO ['data']['helpResult']==1 :#line:269
            O000O0OOO0OO000O0 .log .info (f'{O000O0OOO0OO000O0.pt_pin(O000O0OOO0OO000O0.coookie)}✅助力作者成功 谢谢你 你是个好人！！！')#line:270
        else :#line:271
            O000O0OOO0OO000O0 .log .info (f'{O000O0OOO0OO000O0.pt_pin(O000O0OOO0OO000O0.coookie)}❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')#line:272
        if O000O0OOO0OO000O0 .inviter ==False :#line:274
            for O0O00O00O0O00O0OO in O000O0OOO0OO000O0 .linkId :#line:275
                O0O0O00O00O0O00OO =await O000O0OOO0OO000O0 .Get_H5_Api ('inviteFissionHome',{'linkId':O0O00O00O0O00O0OO ,"inviter":"",},O000O0OOO0OO000O0 .coookie ,'af89e')#line:276
                O000O0OOO0OO000O0 .log .info (f'{O000O0OOO0OO000O0.pt_pin(O000O0OOO0OO000O0.coookie)}⏰剩余时间:{O000O0OOO0OO000O0.convert_ms_to_hours_minutes(O0O0O00O00O0O00OO["data"]["countDownTime"])} 🎉已获取助力:{O0O0O00O00O0O00OO["data"]["prizeNum"] + O0O0O00O00O0O00OO["data"]["drawPrizeNum"]}次 ✅【LinkId】:{O0O00O00O0O00O0OO}')#line:277
            O000O0OOO0OO000O0 .inviter =O0O0O00O00O0O00OO ["data"]["inviter"]#line:278
        if O000O0OOO0OO000O0 .proxy !=False :#line:279
            O000O0OOO0OO000O0 .log .info (f"##############开始并发##############")#line:280
            O00O000OO0O00O00O =[]#line:281
            for O0OOO00OOO0OOO0O0 ,O000OOO000O000O0O in enumerate (ck ,1 ):#line:282
                async with O000O0OOO0OO000O0 .semaphore :#line:283
                    O0O000OOO0OOO00OO =asyncio .create_task (O000O0OOO0OO000O0 .Result (O000O0OOO0OO000O0 .inviter ,O000OOO000O000O0O ))#line:284
                    O00O000OO0O00O00O .append (O0O000OOO0OOO00OO )#line:285
            await asyncio .gather (*O00O000OO0O00O00O )#line:287
        else :#line:288
            O000O0OOO0OO000O0 .log .info (f"##############开始任务##############")#line:289
            for O0OOO00OOO0OOO0O0 ,O000OOO000O000O0O in enumerate (ck ,1 ):#line:290
                await O000O0OOO0OO000O0 .Result (O000O0OOO0OO000O0 .inviter ,O000OOO000O000O0O )#line:291
                await asyncio .sleep (0.5 )#line:292
        O000O0OOO0OO000O0 .log .info (f"##############清点人数##############")#line:294
        O000O0OOO0OO000O0 .log .info (f"✅助力成功:{len(O000O0OOO0OO000O0.power_success)}人 ❌助力失败:{len(O000O0OOO0OO000O0.power_failure)}人 💔未登录CK{len(O000O0OOO0OO000O0.not_log)}人")#line:295
        O000O0OOO0OO000O0 .log .info (f" ⏰耗时:{time.time() - O000O0OOO0OO000O0.start}")#line:296
if __name__ =='__main__':#line:298
    pdd =TEN_JD_PDD ()#line:299
    loop =asyncio .get_event_loop ()#line:300
    loop .run_until_complete (pdd .main ())#line:301
    loop .close ()#line:302
