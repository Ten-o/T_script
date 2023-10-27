#!/usr/bin/env python3
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
import time #line:16
try :#line:18
    ck =get_cookies ()#line:19
    if not ck :#line:20
        sys .exit ()#line:21
except :#line:22
    print ("未获取到有效COOKIE,退出程序！")#line:23
    sys .exit ()#line:24
class TEN_JD_PDD_DRAW (object ):#line:27
    def __init__ (O0OO0000O000000OO ):#line:28
        O0OO0000O000000OO .log =setup_logger ()#line:29
        O0OO0000O000000OO .start =time .time ()#line:30
        O0OO0000O000000OO .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:31
        O0OO0000O000000OO .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:32
        O0OO0000O000000OO .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:33
        O0OO0000O000000OO .numer_og =os .environ .get ("draw_numer")if os .environ .get ("draw_numer")else 3 #line:34
        O0OO0000O000000OO .activityUrl ="https://pro.m.jd.com"#line:35
        O0OO0000O000000OO .cookie =os .environ .get ("draw_cookie")if os .environ .get ("draw_cookie")else ck [0 ]#line:36
        O0OO0000O000000OO .linkId =[]#line:37
        O0OO0000O000000OO .amount =0 #line:38
        O0OO0000O000000OO .leftAmount =0 #line:39
        O0OO0000O000000OO .verify_result =False #line:40
        O0OO0000O000000OO .txj_status =False #line:41
        O0OO0000O000000OO .inviter =''#line:42
        O0OO0000O000000OO .power_success =[]#line:43
        O0OO0000O000000OO .power_failure =[]#line:44
        O0OO0000O000000OO .redpacket =[]#line:45
        O0OO0000O000000OO .cash =[]#line:46
        O0OO0000O000000OO .cash_redpacket =[]#line:47
        O0OO0000O000000OO .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:54
        O0OO0000O000000OO .rewardType ={1 :{'msg':'优惠券🎫'},2 :{'msg':'红包🧧'},6 :{'msg':'惊喜小礼包🎫'},}#line:59
        O0OO0000O000000OO .successful =[]#line:60
    async def retry_with_backoff (OO0O00O0OO00OOO00 ,OOO000000O0O0O000 ,O00O0OOO0OO000O00 ,O0OO000OO0O0O0000 ,backoff_seconds =1 ):#line:62
        for O0000O0000O0000OO in range (O00O0OOO0OO000O00 ):#line:63
            try :#line:64
                return await OOO000000O0O0O000 ()#line:65
            except asyncio .TimeoutError :#line:66
                OO0O00O0OO00OOO00 .log .debug (f'第{O0000O0000O0000OO + 1}次重试  {O0OO000OO0O0O0000} 请求超时')#line:67
                await asyncio .sleep (backoff_seconds )#line:68
            except Exception as O0OO0000OO0OOOO0O :#line:69
                OO0O00O0OO00OOO00 .log .debug (f'第{O0000O0000O0000OO + 1}次重试 {O0OO000OO0O0O0000}出错：{O0OO0000OO0OOOO0O}')#line:70
                await asyncio .sleep (backoff_seconds )#line:71
                if O0000O0000O0000OO ==O00O0OOO0OO000O00 :#line:72
                    OO0O00O0OO00OOO00 .log .error (f'{O0OO000OO0O0O0000}重试{O00O0OOO0OO000O00}次后仍然发生异常')#line:73
                    return #line:74
    async def GET_POST (O00O0O000O00O0OO0 ,O0OO0O0OO0O0000O0 ,num =1 ):#line:76
        async def O00OOOO0OOO00O0OO ():#line:77
            async with aiohttp .ClientSession ()as OO0OO00OO000OO00O :#line:78
                if O0OO0O0OO0O0000O0 ['method']=='get':#line:79
                    async with OO0OO00OO000OO00O .get (**O0OO0O0OO0O0000O0 ['kwargs'])as O00OOOOO0OOOO0000 :#line:80
                        OOO0O00O00OO00O0O =O00OOOOO0OOOO0000 .status #line:81
                        OO00O0O00O00OOO0O =await O00OOOOO0OOOO0000 .text ()#line:82
                else :#line:83
                    async with OO0OO00OO000OO00O .post (**O0OO0O0OO0O0000O0 ['kwargs'])as O00OOOOO0OOOO0000 :#line:84
                        OOO0O00O00OO00O0O =O00OOOOO0OOOO0000 .status #line:85
                        OO00O0O00O00OOO0O =await O00OOOOO0OOOO0000 .text ()#line:86
                if OOO0O00O00OO00O0O !=200 :#line:87
                    await asyncio .sleep (3 )#line:88
                    if num >3 :#line:89
                        O00O0O000O00O0OO0 .log .warning (f'{OOO0O00O00OO00O0O}:状态超出3次')#line:90
                        return False ,False ,False #line:91
                    O00O0O000O00O0OO0 .log .debug (f'{OOO0O00O00OO00O0O}:去重试 第{num}次')#line:92
                    return await O00O0O000O00O0OO0 .GET_POST (O0OO0O0OO0O0000O0 ,num +1 )#line:93
                try :#line:94
                    OO00O00O0OO00O0O0 =json .loads (OO00O0O00O00OOO0O )#line:95
                except :#line:96
                    OO00O00O0OO00O0O0 =OO00O0O00O00OOO0O #line:97
                return OOO0O00O00OO00O0O ,OO00O0O00O00OOO0O ,OO00O00O0OO00O0O0 #line:98
        return await O00O0O000O00O0OO0 .retry_with_backoff (O00OOOO0OOO00O0OO ,3 ,f'GET_POST')#line:100
    async def verify (OOO000O0OOO000OOO ):#line:102
        async def OOOO0OOO00OOO0O00 ():#line:103
            O000000O0O0OOO00O ='https://api.ixu.cc/verify'#line:104
            async with aiohttp .ClientSession ()as O0OO00O0O0000000O :#line:105
                async with O0OO00O0O0000000O .get (O000000O0O0OOO00O ,data ={'TOKEN':OOO000O0OOO000OOO .token },timeout =3 )as OOO000000OOO0OOO0 :#line:106
                    OO00OOO00OOOO0O0O =await OOO000000OOO0OOO0 .json ()#line:107
                    if OOO000000OOO0OOO0 .status ==200 :#line:108
                        OOO000O0OOO000OOO .verify_result =True #line:109
                        OOO000O0OOO000OOO .log .info (f'认证通过 UserId：{OO00OOO00OOOO0O0O["user_id"]}')#line:110
                        return OO00OOO00OOOO0O0O #line:111
                    else :#line:112
                        OOO000O0OOO000OOO .log .error (f"授权未通过:{OO00OOO00OOOO0O0O['error']}")#line:113
                        sys .exit ()#line:114
        return await OOO000O0OOO000OOO .retry_with_backoff (OOOO0OOO00OOO0O00 ,3 ,'verify')#line:116
    async def Get_H5st (OO0O00000O00O0O00 ,OO000OOO0OO0OOO0O ,OOOOOOOOOO00O0OO0 ,O00O000O000OO0OOO ,O000O00O000OO0O0O ):#line:118
        if OO0O00000O00O0O00 .verify_result !=True :#line:119
            await OO0O00000O00O0O00 .verify ()#line:120
        if OO0O00000O00O0O00 .verify_result !=True :#line:121
            OO0O00000O00O0O00 .log .error ("授权未通过 退出")#line:122
            sys .exit ()#line:123
        OOOOOOOOOO0OOOO00 =generate_random_user_agent ()#line:124
        O0000000OO00000OO ={'method':'','kwargs':{'url':'https://api.ouklc.com/api/h5st','params':{'functionId':OO000OOO0OO0OOO0O ,'body':json .dumps (O00O000O000OO0OOO ),'ua':OOOOOOOOOO0OOOO00 ,'pin':OO0O00000O00O0O00 .pt_pin (OOOOOOOOOO00O0OO0 ),'appId':O000O00O000OO0O0O }}}#line:137
        O00OOOOO0OO0OOO00 ,OOO0O0O0OO0OOO0OO ,O0O00OO0OOOOOO0OO =await OO0O00000O00O0O00 .GET_POST (O0000000OO00000OO )#line:138
        if O00OOOOO0OO0OOO00 !=200 :#line:140
            return await OO0O00000O00O0O00 .Get_H5st (OO000OOO0OO0OOO0O ,OOOOOOOOOO00O0OO0 ,O00O000O000OO0OOO ,O000O00O000OO0O0O )#line:141
        O0000000OO00000OO ={'method':'post','kwargs':{'url':f'https://api.m.jd.com','headers':{"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OOOOOOOOOO00O0OO0 ,"User-Agent":OOOOOOOOOO0OOOO00 },'data':O0O00OO0OOOOOO0OO ["body"]}}#line:161
        O00OOOOO0OO0OOO00 ,OOO0O0O0OO0OOO0OO ,O0O00OO0OOOOOO0OO =await OO0O00000O00O0O00 .GET_POST (O0000000OO00000OO )#line:162
        return O0O00OO0OOOOOO0OO #line:163
    def pt_pin (OOO00O0O00O0O0OOO ,OO0O0OO00O00OO0OO ):#line:165
        try :#line:166
            OOOOOO0000O00000O =re .compile (r'pt_pin=(.*?);').findall (OO0O0OO00O00OO0OO )[0 ]#line:167
            OOOOOO0000O00000O =unquote_plus (OOOOOO0000O00000O )#line:168
        except IndexError :#line:169
            OOOOOO0000O00000O =re .compile (r'pin=(.*?);').findall (OO0O0OO00O00OO0OO )[0 ]#line:170
            OOOOOO0000O00000O =unquote_plus (OOOOOO0000O00000O )#line:171
        return OOOOOO0000O00000O #line:172
    def convert_ms_to_hours_minutes (OOOOOO000O0O0OOOO ,O000OOOOOOOOOOOO0 ):#line:174
        OOO0O0000OOO000O0 =O000OOOOOOOOOOOO0 //1000 #line:175
        O00000O0O00O0O000 ,OOO0O0000OOO000O0 =divmod (OOO0O0000OOO000O0 ,60 )#line:176
        OOO00000OO0O000O0 ,O00000O0O00O0O000 =divmod (O00000O0O00O0O000 ,60 )#line:177
        return f'{OOO00000OO0O000O0}小时{O00000O0O00O0O000}分'#line:178
    async def inviteFissionReceive (O0OO000O0OOOOO00O ,O0O00OOOOOO0OO0OO ,OOO000OO0O0OOOOOO ,page =1 ):#line:180
        if O0OO000O0OOOOO00O .verify_result !=True :#line:181
            await O0OO000O0OOOOO00O .verify ()#line:182
        if O0OO000O0OOOOO00O .verify_result !=True :#line:183
            O0OO000O0OOOOO00O .log .error ("授权未通过 退出")#line:184
            sys .exit ()#line:185
        OOO0OOOOO0000000O =generate_random_user_agent ()#line:186
        O000O00OO0OO00OO0 ={'linkId':OOO000OO0O0OOOOOO ,}#line:189
        OOOO0O000O0000000 =await O0OO000O0OOOOO00O .Get_H5st ('inviteFissionReceive',O0O00OOOOOO0OO0OO ,O000O00OO0OO00OO0 ,'02f8d')#line:190
        if OOOO0O000O0000000 ['success']==False and OOOO0O000O0000000 ['errMsg']=='活动太火爆，请稍候重试':#line:191
            O00000000OO0O00OO =f'还差{O0OO000O0OOOOO00O.leftAmount / O0OO000O0OOOOO00O.amount}次'if O0OO000O0OOOOO00O .amount !=0 else '先去助力一次才能计算需要人数'#line:192
            O0OO000O0OOOOO00O .log .debug (f'没助理了 快去助理吧 {O00000000OO0O00OO}')#line:193
            await O0OO000O0OOOOO00O .superRedBagList (O0O00OOOOOO0OO0OO ,OOO000OO0O0OOOOOO ,page )#line:194
            return False #line:195
        if OOOO0O000O0000000 ['success']and OOOO0O000O0000000 ['code']==0 :#line:201
            O0OO000O0OOOOO00O .amount =float (OOOO0O000O0000000 ["data"]["receiveList"][0 ]["amount"])#line:202
            O0OO000O0OOOOO00O .leftAmount =float (OOOO0O000O0000000 ["data"]["leftAmount"])#line:203
            O0OO000O0OOOOO00O .log .info (f'领取中:{OOOO0O000O0000000["data"]["totalAmount"]} 当前:{OOOO0O000O0000000["data"]["amount"]} 获得:{OOOO0O000O0000000["data"]["receiveList"][0]["amount"]} 还差:{OOOO0O000O0000000["data"]["leftAmount"]}元/{O0OO000O0OOOOO00O.leftAmount / O0OO000O0OOOOO00O.amount}次 当前进度:{OOOO0O000O0000000["data"]["rate"]}%')#line:205
            if int (OOOO0O000O0000000 ["data"]["rate"])==100 :#line:206
                O0OO000O0OOOOO00O .log .info (f'领取中:{OOOO0O000O0000000["data"]["totalAmount"]} 进度:{OOOO0O000O0000000["data"]["rate"]}% 退出!')#line:207
                await O0OO000O0OOOOO00O .superRedBagList (O0O00OOOOOO0OO0OO ,OOO000OO0O0OOOOOO ,page )#line:208
                return False #line:209
        return True #line:210
    async def apCashWithDraw (O00O00OOOOOO00O0O ,OOOOO0000O0O0O00O ,O0OOO0O0O0OO0OO0O ,O000O0O0OO0O0O00O ,O00O00O0000O0OO00 ,O00O00O0O00000OO0 ,OO00000OOOO00O0O0 ):#line:212
        if O00O00OOOOOO00O0O .verify_result !=True :#line:213
            await O00O00OOOOOO00O0O .verify ()#line:214
        if O00O00OOOOOO00O0O .verify_result !=True :#line:215
            O00O00OOOOOO00O0O .log .error ("授权未通过 退出")#line:216
            sys .exit ()#line:217
        O0O0O00O0O00OOO00 =generate_random_user_agent ()#line:218
        OO0OOO0OO000OO0O0 =await O00O00OOOOOO00O0O .Get_H5st ("apCashWithDraw",O0OOO0O0O0OO0OO0O ,{"linkId":OOOOO0000O0O0O00O ,"businessSource":"NONE","base":{"id":O000O0O0OO0O0O00O ,"business":"fission","poolBaseId":O00O00O0000O0OO00 ,"prizeGroupId":O00O00O0O00000OO0 ,"prizeBaseId":OO00000OOOO00O0O0 ,"prizeType":4 }},'8c6ae')#line:234
        return OO0OOO0OO000OO0O0 #line:235
    async def inviteFissionBeforeHome (O0O000OO0OO0O00O0 ,num =1 ):#line:237
        OOO000O000OO00O00 =False #line:238
        for OO000O0OO00O0OOO0 in ck :#line:239
            if len (O0O000OO0OO0O00O0 .power_success )>=num :#line:240
                return await O0O000OO0OO0O00O0 .inviteFissionReceive (O0O000OO0OO0O00O0 .cookie ,O0O000OO0OO0O00O0 .linkId )#line:241
            O0O000O00OO00000O =await O0O000OO0OO0O00O0 .Get_H5st ("inviteFissionBeforeHome",OO000O0OO00O0OOO0 ,{'linkId':O0O000OO0OO0O00O0 .linkId ,"isJdApp":True ,'inviter':O0O000OO0OO0O00O0 .inviter },'02f8d',)#line:244
            if int (O0O000O00OO00000O ['code'])==0 :#line:245
                for OO000OO000OOO0OO0 ,O0000OOOO0O0O000O in O0O000OO0OO0O00O0 .helpResult :#line:246
                    if O0O000O00OO00000O ['data']['helpResult']==int (OO000OO000OOO0OO0 ):#line:247
                        OOO000O000OO00O00 =True #line:248
                        O0O000OO0OO0O00O0 .log .info (f"Id:{O0O000OO0OO0O00O0.linkId[:4] + '****' + O0O000OO0OO0O00O0.linkId[-4:]}|助理:{O0O000O00OO00000O['data']['nickName']}|{O0O000O00OO00000O['data']['helpResult']}|{O0O000OO0OO0O00O0.pt_pin(OO000O0OO00O0OOO0)}|{O0000OOOO0O0O000O}")#line:250
                        if O0O000O00OO00000O ['data']['helpResult']==1 :#line:251
                            O0O000OO0OO0O00O0 .power_success .append (OO000O0OO00O0OOO0 )#line:252
                        else :#line:253
                            O0O000OO0OO0O00O0 .power_failure .append (OO000O0OO00O0OOO0 )#line:254
                    if not OOO000O000OO00O00 :#line:255
                        O0000OOOO0O0O000O ='❌未知状态 (可能是活动未开启！！！)'#line:256
                        O0O000OO0OO0O00O0 .power_failure .append (OO000O0OO00O0OOO0 )#line:257
                        O0O000OO0OO0O00O0 .log .info (f"Id:{O0O000OO0OO0O00O0.linkId[:4] + '****' + O0O000OO0OO0O00O0.linkId[-4:]}|助理:{O0O000O00OO00000O['data']['nickName']}|{O0O000O00OO00000O['data']['helpResult']}|{O0O000OO0OO0O00O0.pt_pin(OO000O0OO00O0OOO0)}|{O0000OOOO0O0O000O}")#line:259
            else :#line:260
                O0O000OO0OO0O00O0 .log .info (f"{O0O000OO0OO0O00O0.pt_pin(OO000O0OO00O0OOO0)}{O0O000O00OO00000O['code']} 结果:💔{O0O000O00OO00000O['errMsg']}")#line:261
    async def superRedBagList (OOOO0O0O00OO000OO ,O0O00O00O0000OO0O ,O000O000OO0000O00 ,O00O0O0OO00O00OO0 ):#line:263
        if OOOO0O0O00OO000OO .verify_result !=True :#line:264
            await OOOO0O0O00OO000OO .verify ()#line:265
        if OOOO0O0O00OO000OO .verify_result !=True :#line:266
            OOOO0O0O00OO000OO .log .error ("授权未通过 退出")#line:267
            sys .exit ()#line:268
        OO0O0O0O0000OO00O =await OOOO0O0O00OO000OO .Get_H5st ('superRedBagList',O0O00O00O0000OO0O ,{"pageNum":O00O0O0OO00O00OO0 ,"pageSize":200 ,"linkId":O000O000OO0000O00 ,"business":"fission"},'f2b1d')#line:271
        OOOO0O0O00OO000OO .log .info (f"开始提取{O00O0O0OO00O00OO0}页, 共{len(OO0O0O0O0000OO00O['data']['items'])}条记录")#line:272
        if len (OO0O0O0O0000OO00O ['data']['items'])==0 :#line:273
            return False #line:274
        for OOO0O0O0000OOO000 in OO0O0O0O0000OO00O ['data']['items']:#line:275
            OO0OO0OOO0OO00O0O ,OO00OO0O000O0O0OO ,OOOOOO00OOOOOOO00 ,OO0000OOOOOOOO0OO ,O0000OOOOO0OOO000 ,OOOO0OO000OO00OOO ,OOOOO000OO0OO000O ,O0O0OO0OO00OOOOOO ,O0O00O0OO000O00O0 =(OOO0O0O0000OOO000 ['id'],OOO0O0O0000OOO000 ['amount'],OOO0O0O0000OOO000 ['prizeType'],OOO0O0O0000OOO000 ['state'],OOO0O0O0000OOO000 ['prizeConfigName'],OOO0O0O0000OOO000 ['prizeGroupId'],OOO0O0O0000OOO000 ['poolBaseId'],OOO0O0O0000OOO000 ['prizeBaseId'],OOO0O0O0000OOO000 ['startTime'])#line:280
            if float (OO00OO0O000O0O0OO )>1.0 :#line:281
                OOOO0O0O00OO000OO .log .info (f"{O0O00O0OO000O00O0} {OO00OO0O000O0O0OO}元 {'❌未提现' if OOOOOO00OOOOOOO00 == 4 and OO0000OOOOOOOO0OO != 3 else '✅已提现'}")#line:282
            if OOOOOO00OOOOOOO00 ==4 and OO0000OOOOOOOO0OO !=3 :#line:283
                OO0O0O0O0000OO00O =await OOOO0O0O00OO000OO .apCashWithDraw (O000O000OO0000O00 ,O0O00O00O0000OO0O ,OO0OO0OOO0OO00O0O ,OOOOO000OO0OO000O ,OOOO0OO000OO00OOO ,O0O0OO0OO00OOOOOO )#line:284
                if int (OO0O0O0O0000OO00O ['data']['status'])==310 :#line:286
                    OOOO0O0O00OO000OO .log .info (f"✅{OO00OO0O000O0O0OO}现金💵 提现成功")#line:287
                    OOOO0O0O00OO000OO .successful .append (OO00OO0O000O0O0OO )#line:288
                elif int (OO0O0O0O0000OO00O ['data']['status'])==50056 or int (OO0O0O0O0000OO00O ['data']['status'])==50001 :#line:289
                    OOOO0O0O00OO000OO .log .warning (f"❌{OO00OO0O000O0O0OO}现金💵 重新发起 提现失败:{OO0O0O0O0000OO00O['data']['message']}")#line:290
                    time .sleep (3 )#line:291
                    await OOOO0O0O00OO000OO .apCashWithDraw (O000O000OO0000O00 ,O0O00O00O0000OO0O ,OO0OO0OOO0OO00O0O ,OOOOO000OO0OO000O ,OOOO0OO000OO00OOO ,O0O0OO0OO00OOOOOO )#line:292
                    if int (OO0O0O0O0000OO00O ['data']['status'])==310 :#line:293
                        OOOO0O0O00OO000OO .log .info (f"✅{OO00OO0O000O0O0OO}现金💵 提现成功")#line:294
                        OOOO0O0O00OO000OO .successful .append (OO00OO0O000O0O0OO )#line:295
                    else :#line:296
                        OOOO0O0O00OO000OO .log .error (f"❌{OO00OO0O000O0O0OO}现金💵 提现失败:{OO0O0O0O0000OO00O['data']['message']}")#line:297
                elif '金额超过自然月上限'in OO0O0O0O0000OO00O ['data']['message']:#line:298
                    OOOO0O0O00OO000OO .log .info (f"{OO00OO0O000O0O0OO}现金:{OO0O0O0O0000OO00O['data']['message']}:去兑换红包")#line:299
                    await OOOO0O0O00OO000OO .apRecompenseDrawPrize (O000O000OO0000O00 ,O0O00O00O0000OO0O ,OO0OO0OOO0OO00O0O ,OOOOO000OO0OO000O ,OOOO0OO000OO00OOO ,O0O0OO0OO00OOOOOO ,OO00OO0O000O0O0OO )#line:300
                else :#line:301
                    OOOO0O0O00OO000OO .log .error (f"{OO00OO0O000O0O0OO}现金 ❌提现错误:{OO0O0O0O0000OO00O['data']['status']} {OO0O0O0O0000OO00O['data']['message']}")#line:302
            else :#line:304
                continue #line:305
            await asyncio .sleep (0.5 )#line:306
    async def apRecompenseDrawPrize (OOO0OO0OOOOOO000O ,OO0OO0OOO0OO0O000 ,OOO0OO0000O0O0OO0 ,O0OO0000000O000O0 ,O00O0O0000O00O0OO ,O0O00O0OOOO00OOOO ,OOO0OOOO0OO00OO00 ,OO00O0000000O0O0O ):#line:309
        O00OOO00O0O0OO0O0 =await OOO0OO0OOOOOO000O .Get_H5st ('apRecompenseDrawPrize',OOO0OO0000O0O0OO0 ,{"linkId":OO0OO0OOO0OO0O000 ,"businessSource":"fission","drawRecordId":O0OO0000000O000O0 ,"business":"fission","poolId":O00O0O0000O00O0OO ,"prizeGroupId":O0O00O0OOOO00OOOO ,"prizeId":OOO0OOOO0OO00OO00 ,},'8c6ae')#line:319
        if O00OOO00O0O0OO0O0 ['success']and int (O00OOO00O0O0OO0O0 ['data']['resCode'])==0 :#line:320
            OOO0OO0OOOOOO000O .log .info (f"{OO00O0000000O0O0O}现金:🧧红包兑换成功")#line:321
            OOO0OO0OOOOOO000O .cash_redpacket .append (OO00O0000000O0O0O )#line:322
        else :#line:323
            OOO0OO0OOOOOO000O .log .info (f"{OO00O0000000O0O0O}现金:🧧红包兑换失败 {O00OOO00O0O0OO0O0}")#line:324
    async def Fission_Draw (OO00O0000O0O00O0O ,OO000O000OO0OOO0O ,O0O0000O00OO0OO00 ):#line:326
        OO00O0000O0O00O0O .log .info (f"****************开始抽奖****************")#line:327
        while True :#line:328
            OO00OO00OOO0OOO0O =await OO00O0000O0O00O0O .Get_H5st ('inviteFissionDrawPrize',OO000O000OO0OOO0O ,{"linkId":O0O0000O00OO0OO00 },'c02c6')#line:331
            if not OO00OO00OOO0OOO0O ['success']:#line:333
                if "抽奖次数已用完"in OO00OO00OOO0OOO0O ['errMsg']:#line:334
                    OO00O0000O0O00O0O .log .debug (f"⚠️抽奖次数已用完")#line:335
                    break #line:336
                elif "本场活动已结束"in OO00OO00OOO0OOO0O ['errMsg']:#line:337
                    OO00O0000O0O00O0O .log .debug (f"⏰本场活动已结束了,快去重新开始吧")#line:338
                    sys .exit ()#line:339
            try :#line:340
                if int (OO00OO00OOO0OOO0O ['data']['rewardType'])in OO00O0000O0O00O0O .rewardType :#line:343
                    OO00O0000O0O00O0O .log .info (f"获得:{OO00OO00OOO0OOO0O['data']['prizeValue']}元{OO00O0000O0O00O0O.rewardType[int(OO00OO00OOO0OOO0O['data']['rewardType'])]['msg']}")#line:345
                    if int (OO00OO00OOO0OOO0O ['data']['rewardType'])==2 :#line:346
                        OO00O0000O0O00O0O .redpacket .append (float (OO00OO00OOO0OOO0O ['data']['prizeValue']))#line:347
                else :#line:348
                    OO00O0000O0O00O0O .log .info (f"获得:{OO00OO00OOO0OOO0O['data']['prizeValue']}元现金💵")#line:349
                    OO00O0000O0O00O0O .cash .append (float (OO00OO00OOO0OOO0O ['data']['prizeValue']))#line:350
            except Exception as OOOO0O000O0OO00O0 :#line:351
                OO00O0000O0O00O0O .log .error (f'(未知物品):{OO00OO00OOO0OOO0O}')#line:352
            await asyncio .sleep (0.3 )#line:353
        OO00O0000O0O00O0O .log .info (f"抽奖结束: 💵现金:{'{:.2f}'.format(sum([float(O0O000O00000OO0OO) for O0O000O00000OO0OO in OO00O0000O0O00O0O.cash]))}元, 🧧红包:{'{:.2f}'.format(sum([float(O0OO0OO000OO0OO00) for O0OO0OO000OO0OO00 in OO00O0000O0O00O0O.redpacket]))}元")#line:355
        OO00O0000O0O00O0O .log .info (f"****************开始提现****************")#line:356
        OOOOOO000O0OOOOO0 =0 #line:357
        while True :#line:358
            OOOOOO000O0OOOOO0 =OOOOOO000O0OOOOO0 +1 #line:359
            OO00O000OO000OOO0 =await OO00O0000O0O00O0O .superRedBagList (OO000O000OO0OOO0O ,O0O0000O00OO0OO00 ,OOOOOO000O0OOOOO0 )#line:360
            await asyncio .sleep (1 )#line:361
            if not OO00O000OO000OOO0 :#line:362
                break #line:363
        OO0O0O00OOOO00O00 =('提现结束: ')+(f"💵现金:{'{:.2f}'.format(sum([float(OOOOO00000OO00OO0) for OOOOO00000OO00OO0 in OO00O0000O0O00O0O.successful]))}元/")+(f"🧧兑换红包:{'{:.2f}'.format(sum([float(OOOO000OO00000000) for OOOO000OO00000000 in OO00O0000O0O00O0O.cash_redpacket]))}元/共计红包:{'{:.2f}'.format(sum([float(OOO00OOO0O0O00O0O) for OOO00OOO0O0O00O0O in OO00O0000O0O00O0O.redpacket + OO00O0000O0O00O0O.cash_redpacket]))}")#line:369
        if not OO00O0000O0O00O0O .successful and not OO00O0000O0O00O0O .cash_redpacket :#line:370
            OO0O0O00OOOO00O00 ='提现结束: 一毛都没有哦！'#line:371
        OO00O0000O0O00O0O .log .info (OO0O0O00OOOO00O00 )#line:372
    async def add_LinkId (O0OOO0O0O000O0O0O ):#line:374
        async def O0000000O0000O0OO ():#line:375
            if O0OOO0O0O000O0O0O .verify_result !=True :#line:376
                await O0OOO0O0O000O0O0O .verify ()#line:377
            if O0OOO0O0O000O0O0O .verify_result !=True :#line:378
                O0OOO0O0O000O0O0O .log .error ("授权未通过 退出")#line:379
                sys .exit ()#line:380
            O00O0OOOOO0OO0O0O ='https://api.ixu.cc/status/inviter.json'#line:381
            async with aiohttp .ClientSession ()as OO00OO0OO000OO00O :#line:382
                async with OO00OO0OO000OO00O .get (O00O0OOOOO0OO0O0O ,timeout =5 )as OO0O00OO0O000O00O :#line:383
                    if OO0O00OO0O000O00O .status ==200 :#line:384
                        O0000OOO0O0OOOOOO =await OO0O00OO0O000O00O .json ()#line:385
                        if O0000OOO0O0OOOOOO ['stats']!='True':#line:386
                            O0OOO0O0O000O0O0O .log .error (f"{O0000OOO0O0OOOOOO['err_text']}")#line:387
                            sys .exit ()#line:388
                        O0OOO0O0O000O0O0O .inviter_help =O0000OOO0O0OOOOOO ['inviter']#line:389
                        if len (O0000OOO0O0OOOOOO ['text'])>0 :#line:390
                            O0OOO0O0O000O0O0O .log .debug (f'那女孩对你说:{O0000OOO0O0OOOOOO["text"]}')#line:391
                        if O0OOO0O0O000O0O0O .scode =='ALL'or O0OOO0O0O000O0O0O .scode =='all':#line:392
                            for O00OO0O0O0000O00O in O0000OOO0O0OOOOOO ['linkId']:#line:393
                                O0OOO0O0O000O0O0O .linkId .append (O00OO0O0O0000O00O )#line:394
                                O0OOO0O0O000O0O0O .log .info (f'云端获取到linkId:{O00OO0O0O0000O00O}')#line:395
                            return True #line:396
                        else :#line:397
                            O0OOO0O0O000O0O0O .linkId .append (O0000OOO0O0OOOOOO ['linkId'][int (O0OOO0O0O000O0O0O .scode )-1 ])#line:398
                            O0OOO0O0O000O0O0O .log .info (f'云端获取到linkId:{O0000OOO0O0OOOOOO["linkId"][int(O0OOO0O0O000O0O0O.scode) - 1]}')#line:399
                            return True #line:400
                    else :#line:401
                        O0OOO0O0O000O0O0O .log .error ('未获取到linkId 重试')#line:402
        return await O0OOO0O0O000O0O0O .retry_with_backoff (O0000000O0000O0OO ,3 ,'linkId')#line:404
    async def task_start (O00OOOOO0OOOOO00O ):#line:406
        if O00OOOOO0OOOOO00O .verify_result !=True :#line:407
            await O00OOOOO0OOOOO00O .verify ()#line:408
        if O00OOOOO0OOOOO00O .verify_result !=True :#line:409
            O00OOOOO0OOOOO00O .log .error ("授权未通过 退出")#line:410
            sys .exit ()#line:411
        await O00OOOOO0OOOOO00O .add_LinkId ()#line:412
        OO0OO0OOO00OO000O =O00OOOOO0OOOOO00O .cookie #line:415
        if O00OOOOO0OOOOO00O .txj_status :#line:416
            try :#line:417
                O00O0O0000OOOOO0O =await O00OOOOO0OOOOO00O .Get_H5st ('inviteFissionHome',OO0OO0OOO00OO000O ,{'linkId':O00OOOOO0OOOOO00O .linkId [0 ],"inviter":"",},'af89e')#line:419
                if not O00O0O0000OOOOO0O ['success']and O00O0O0000OOOOO0O ['errMsg']=='未登录':#line:421
                    O00OOOOO0OOOOO00O .log .error (f"{O00O0O0000OOOOO0O['errMsg']}")#line:422
                    return #line:423
                O0O0000OO0O00OOO0 =O00O0O0000OOOOO0O ['data']#line:424
                if O0O0000OO0O00OOO0 ['cashVo']!=None :#line:425
                    OO00OOOOO00O0O0O0 =O0O0000OO0O00OOO0 ['cashVo']#line:426
                    O00OOOOO0OOOOO00O .log .info (f"Name:{OO00OOOOO00O0O0O0['userInfo']['nickName']} 已助理:{O0O0000OO0O00OOO0['prizeNum']} 提现:{OO00OOOOO00O0O0O0['totalAmount']}元 当前:{OO00OOOOO00O0O0O0['amount']}元 进度{OO00OOOOO00O0O0O0['rate']}% 剩余时间:{O00OOOOO0OOOOO00O.convert_ms_to_hours_minutes(O0O0000OO0O00OOO0['countDownTime'])}")#line:428
                    if int (OO00OOOOO00O0O0O0 ['rate'])==100 :#line:429
                        O00OOOOO0OOOOO00O .log .info (f"本轮您已提现{OO00OOOOO00O0O0O0['totalAmount']}元了 等{O00OOOOO0OOOOO00O.convert_ms_to_hours_minutes(O0O0000OO0O00OOO0['countDownTime'])}后在来吧")#line:431
                        await O00OOOOO0OOOOO00O .superRedBagList (OO0OO0OOO00OO000O ,O00OOOOO0OOOOO00O .linkId [0 ],1 )#line:432
                        return #line:433
                else :#line:434
                    O00OOOOO0OOOOO00O .log .error ('哦和 黑号了哦')#line:435
                while True :#line:437
                    OOOO000OO00O0000O =await O00OOOOO0OOOOO00O .inviteFissionReceive (OO0OO0OOO00OO000O ,O00OOOOO0OOOOO00O .linkId [0 ])#line:438
                    if not OOOO000OO00O0000O :#line:439
                        break #line:440
                    time .sleep (0.3 )#line:441
            except Exception as O00O0O00OOOOOOOO0 :#line:442
                O00OOOOO0OOOOO00O .log .error ('黑号')#line:443
        else :#line:444
            for OOOOO00O00O0OO00O in O00OOOOO0OOOOO00O .linkId :#line:445
                O00OOOOO0OOOOO00O .log .info (f'开始执行 LinkId:{OOOOO00O00O0OO00O}')#line:446
                await O00OOOOO0OOOOO00O .Fission_Draw (OO0OO0OOO00OO000O ,OOOOO00O00O0OO00O )#line:447
if __name__ =='__main__':#line:450
    pdd =TEN_JD_PDD_DRAW ()#line:451
    loop =asyncio .get_event_loop ()#line:452
    loop .run_until_complete (pdd .task_start ())#line:453
    loop .close ()#line:454
