# -*- coding: utf-8 -*-
"""
File: TEN_JD_PDD_DRAW_20.py(邀好友赢现金-领现金)
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-领现金');
@author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
@software: PyCharm
@file: TEN_JD_PDD_DRAW_20.py
"""



from utils .logger import setup_logger #line:11
from utils .X_API_EID_TOKEN import *#line:12
from utils .User_agent import generate_random_user_agent #line:13
import asyncio ,aiohttp ,re ,os ,sys ,threading ,concurrent .futures ,time ,json #line:14
from utils .jdCookie import get_cookies #line:15
from utils .__init__ import *#line:16
from tqdm import tqdm #line:17
import time #line:18
data =range (1 ,101 )#line:21
try :#line:24
    ck =get_cookies ()#line:25
    if not ck :#line:26
        sys .exit ()#line:27
except :#line:28
    print ("未获取到有效COOKIE,退出程序！")#line:29
    sys .exit ()#line:30
class TEN_JD_PDD_DRAW (object ):#line:33
    def __init__ (OOOOOO0OOOO0OO0OO ):#line:34
        OOOOOO0OOOO0OO0OO .log =setup_logger ()#line:35
        OOOOOO0OOOO0OO0OO .start =time .time ()#line:36
        OOOOOO0OOOO0OO0OO .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:37
        OOOOOO0OOOO0OO0OO .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:38
        OOOOOO0OOOO0OO0OO .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False
        OOOOOO0OOOO0OO0OO .numer_og =os .environ .get ("draw_numer")if os .environ .get ("draw_numer")else 3 #line:40
        OOOOOO0OOOO0OO0OO .activityUrl ="https://pro.m.jd.com"#line:41
        OOOOOO0OOOO0OO0OO .cookie =os .environ .get ("draw_cookie")if os .environ .get ("draw_cookie")else ck [0 ]#line:42
        OOOOOO0OOOO0OO0OO .linkId ='3orGfh1YkwNLksxOcN8zWQ'#line:43
        OOOOOO0OOOO0OO0OO .amount =0 #line:44
        OOOOOO0OOOO0OO0OO .leftAmount =0 #line:45
        OOOOOO0OOOO0OO0OO .verify_result =False #line:46
    async def retry_with_backoff (O0O0000OO0O00O0O0 ,O00O00O00OOOO0OOO ,O000000OO0OO0OO0O ,O0OO000OO00O000OO ,backoff_seconds =1 ):#line:48
        for OO0O00OO00OOO0000 in range (O000000OO0OO0OO0O ):#line:49
            try :#line:50
                return await O00O00O00OOOO0OOO ()#line:51
            except asyncio .TimeoutError :#line:52
                O0O0000OO0O00O0O0 .log .debug (f'第{OO0O00OO00OOO0000 + 1}次重试  {O0OO000OO00O000OO} 请求超时')#line:53
                await asyncio .sleep (backoff_seconds )#line:54
            except Exception as O0O0O0OO00OOO0O00 :#line:55
                O0O0000OO0O00O0O0 .log .debug (f'第{OO0O00OO00OOO0000 + 1}次重试 {O0OO000OO00O000OO}出错：{O0O0O0OO00OOO0O00}')#line:56
                await asyncio .sleep (backoff_seconds )#line:57
                if OO0O00OO00OOO0000 ==O000000OO0OO0OO0O :#line:58
                    O0O0000OO0O00O0O0 .log .error (f'{O0OO000OO00O000OO}重试{O000000OO0OO0OO0O}次后仍然发生异常')#line:59
                    return #line:60
    async def GET_POST (O00OO0OO00000O0O0 ,O0OO0OOO0O0O0000O ):#line:62
        async def OO0OO00O00O0OO00O ():#line:63
            async with aiohttp .ClientSession ()as OO0O0O0000OOOOO00 :#line:64
                if O0OO0OOO0O0O0000O ['method']=='get':#line:65
                    async with OO0O0O0000OOOOO00 .get (**O0OO0OOO0O0O0000O ['kwargs'])as O00000OOOO0OOO0OO :#line:66
                        O00O000000OO00000 =O00000OOOO0OOO0OO .status #line:67
                        O0O00O00OO000000O =await O00000OOOO0OOO0OO .text ()#line:68
                else :#line:69
                    async with OO0O0O0000OOOOO00 .post (**O0OO0OOO0O0O0000O ['kwargs'])as O00000OOOO0OOO0OO :#line:70
                        O00O000000OO00000 =O00000OOOO0OOO0OO .status #line:71
                        O0O00O00OO000000O =await O00000OOOO0OOO0OO .text ()#line:72
                if O00O000000OO00000 !=200 :#line:73
                    O00OO0OO00000O0O0 .log .debug (f'{O00O000000OO00000}:去重试')#line:74
                    return await O00OO0OO00000O0O0 .GET_POST (O0OO0OOO0O0O0000O )#line:75
                try :#line:76
                    O0OO000OO0OO0OOOO =json .loads (O0O00O00OO000000O )#line:77
                except :#line:78
                    O0OO000OO0OO0OOOO =O0O00O00OO000000O #line:79
                return O00O000000OO00000 ,O0O00O00OO000000O ,O0OO000OO0OO0OOOO #line:80
        return await O00OO0OO00000O0O0 .retry_with_backoff (OO0OO00O00O0OO00O ,3 ,f'GET_POST')#line:82
    async def verify (OOOO00OO0O00OOO00 ):#line:85
        async def O0OOOOOO0OO00O000 ():#line:86
            OOO00OO0O0O00000O ='https://api.ixu.cc/verify'#line:87
            async with aiohttp .ClientSession ()as O00OOO0O0O0000000 :#line:88
                async with O00OOO0O0O0000000 .get (OOO00OO0O0O00000O ,data ={'TOKEN':OOOO00OO0O00OOO00 .token },timeout =3 )as O00OOO00OO0OOO0O0 :#line:89
                    OOO0OOOOO00OO0OO0 =await O00OOO00OO0OOO0O0 .json ()#line:90
                    if O00OOO00OO0OOO0O0 .status ==200 :#line:91
                        OOOO00OO0O00OOO00 .verify_result =True #line:92
                        OOOO00OO0O00OOO00 .log .info (f'认证通过 UserId：{OOO0OOOOO00OO0OO0["user_id"]}')#line:93
                        return OOO0OOOOO00OO0OO0 #line:94
                    else :#line:95
                        OOOO00OO0O00OOO00 .log .error (f"授权未通过:{OOO0OOOOO00OO0OO0['error']}")#line:96
                        sys .exit ()#line:97
        return await OOOO00OO0O00OOO00 .retry_with_backoff (O0OOOOOO0OO00O000 ,3 ,'verify')#line:99
    async def Get_H5st (OOO00O0000O00O0OO ,O0O00O0OOOO00O0OO ,OOOO0O00000OO0O0O ,OO0O0O0OOOOOOOO0O ,O0OO0OOOOOOOO0O0O ):#line:101
        if OOO00O0000O00O0OO .verify_result !=True :#line:102
            await OOO00O0000O00O0OO .verify ()#line:103
        if OOO00O0000O00O0OO .verify_result !=True :#line:104
            OOO00O0000O00O0OO .log .error ("授权未通过 退出")#line:105
            sys .exit ()#line:106
        OOO0O0OO0OO000000 =generate_random_user_agent ()#line:107
        OO0OOO0OOOO0OOO0O ={'method':'','kwargs':{'url':'https://api.ouklc.com/api/h5st','params':{'functionId':O0O00O0OOOO00O0OO ,'body':json .dumps (OO0O0O0OOOOOOOO0O ),'ua':OOO0O0OO0OO000000 ,'pin':OOO00O0000O00O0OO .pt_pin (OOOO0O00000OO0O0O ),'appId':O0OO0OOOOOOOO0O0O }}}#line:120
        OO0000OOO000000OO ,O00OOOO0O00000O0O ,O0OO00000OOO0O000 =await OOO00O0000O00O0OO .GET_POST (OO0OOO0OOOO0OOO0O )#line:121
        if OO0000OOO000000OO !=200 :#line:122
            return await OOO00O0000O00O0OO .Get_H5st (O0O00O0OOOO00O0OO ,OOOO0O00000OO0O0O ,OO0O0O0OOOOOOOO0O ,OOO0O0OO0OO000000 ,O0OO0OOOOOOOO0O0O )#line:123
        OO0OOO0OOOO0OOO0O ={'method':'post','kwargs':{'url':f'https://api.m.jd.com','headers':{"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OOOO0O00000OO0O0O ,"User-Agent":OOO0O0OO0OO000000 },'data':O0OO00000OOO0O000 ["body"]}}#line:143
        OO0000OOO000000OO ,O00OOOO0O00000O0O ,O0OO00000OOO0O000 =await OOO00O0000O00O0OO .GET_POST (OO0OOO0OOOO0OOO0O )#line:144
        return O0OO00000OOO0O000 #line:145
    def pt_pin (OOO000O0O00OOO000 ,OOO0OO0OOO00OO0OO ):#line:150
        try :#line:151
            OOOO00000OOOOOOOO =re .compile (r'pt_pin=(.*?);').findall (OOO0OO0OOO00OO0OO )[0 ]#line:152
            OOOO00000OOOOOOOO =unquote_plus (OOOO00000OOOOOOOO )#line:153
        except IndexError :#line:154
            OOOO00000OOOOOOOO =re .compile (r'pin=(.*?);').findall (OOO0OO0OOO00OO0OO )[0 ]#line:155
            OOOO00000OOOOOOOO =unquote_plus (OOOO00000OOOOOOOO )#line:156
        return OOOO00000OOOOOOOO #line:157
    def convert_ms_to_hours_minutes (O00OOO000OOOOOOOO ,O000O0O00000O0000 ):#line:159
        OOO00OOOO00OOO0O0 =O000O0O00000O0000 //1000 #line:160
        OOO0OOOOO00O0OO00 ,OOO00OOOO00OOO0O0 =divmod (OOO00OOOO00OOO0O0 ,60 )#line:161
        O0OOOO0OOOOOO0OO0 ,OOO0OOOOO00O0OO00 =divmod (OOO0OOOOO00O0OO00 ,60 )#line:162
        return f'{O0OOOO0OOOOOO0OO0}小时{OOO0OOOOO00O0OO00}分'#line:163
    async def inviteFissionReceive (O00OO00O0OOOO0000 ,O0O0O0OO00O000000 ,OO00OO0OOO0O0O00O ):#line:164
        if O00OO00O0OOOO0000 .verify_result !=True :#line:165
            await O00OO00O0OOOO0000 .verify ()#line:166
        if O00OO00O0OOOO0000 .verify_result !=True :#line:167
            O00OO00O0OOOO0000 .log .error ("授权未通过 退出")#line:168
            sys .exit ()#line:169
        OOO00000OO0O0OOOO =generate_random_user_agent ()#line:170
        O00O0O0O0O00OO0OO ={'linkId':OO00OO0OOO0O0O00O ,}#line:173
        O0OOOOO00O00O000O =await O00OO00O0OOOO0000 .Get_H5st ('inviteFissionReceive',O0O0O0OO00O000000 ,O00O0O0O0O00OO0OO ,'02f8d')#line:174
        if O0OOOOO00O00O000O ['success']==False and O0OOOOO00O00O000O ['errMsg']=='活动太火爆，请稍候重试':#line:175
            OO0OOOO0O0O000OO0 =f'还差{O00OO00O0OOOO0000.leftAmount/O00OO00O0OOOO0000.amount}次'if O00OO00O0OOOO0000 .amount !=0 else '先去助力一次才能计算'#line:176
            O00OO00O0OOOO0000 .log .debug (f'没助理了 快去助理吧 {OO0OOOO0O0O000OO0}')#line:177
            await O00OO00O0OOOO0000 .superRedBagList (O0O0O0OO00O000000 ,OO00OO0OOO0O0O00O )#line:178
            return False #line:180
        if O0OOOOO00O00O000O ['success']and O0OOOOO00O00O000O ['code']==0 :#line:181
            O00OO00O0OOOO0000 .amount =float (O0OOOOO00O00O000O ["data"]["receiveList"][0 ]["amount"])#line:182
            O00OO00O0OOOO0000 .leftAmount =float (O0OOOOO00O00O000O ["data"]["leftAmount"])#line:183
            O00OO00O0OOOO0000 .log .info (f'领取中:{O0OOOOO00O00O000O["data"]["totalAmount"]} 当前:{O0OOOOO00O00O000O["data"]["amount"]} 获得:{O0OOOOO00O00O000O["data"]["receiveList"][0]["amount"]} 还差:{O0OOOOO00O00O000O["data"]["leftAmount"]}元/{O00OO00O0OOOO0000.leftAmount/O00OO00O0OOOO0000.amount}次 当前进度:{O0OOOOO00O00O000O["data"]["rate"]}%')#line:184
            if int (O0OOOOO00O00O000O ["data"]["rate"])==100 :#line:185
                O00OO00O0OOOO0000 .log .info (f'领取中:{O0OOOOO00O00O000O["data"]["totalAmount"]} 进度:{O0OOOOO00O00O000O["data"]["rate"]}% 退出!')#line:186
                await O00OO00O0OOOO0000 .superRedBagList (O0O0O0OO00O000000 ,OO00OO0OOO0O0O00O )#line:187
                return False #line:188
        return True #line:189
    async def apCashWithDraw (OO00000OO00O000OO ,O0OOO00OOO0000000 ,O00OO0O0O00O000OO ,O000000O0OOOOOOOO ,OO0OO000O00O0000O ,OO0OOOO0O00O00O00 ,OOO0OO0O00O0O00O0 ):#line:191
        if OO00000OO00O000OO .verify_result !=True :#line:192
            await OO00000OO00O000OO .verify ()#line:193
        if OO00000OO00O000OO .verify_result !=True :#line:194
            OO00000OO00O000OO .log .error ("授权未通过 退出")#line:195
            sys .exit ()#line:196
        OO00O00O000O0000O =generate_random_user_agent ()#line:197
        OOOO00OOO000OO00O =await OO00000OO00O000OO .Get_H5st ("apCashWithDraw",O00OO0O0O00O000OO ,{"linkId":O0OOO00OOO0000000 ,"businessSource":"NONE","base":{"id":O000000O0OOOOOOOO ,"business":"fission","poolBaseId":OO0OO000O00O0000O ,"prizeGroupId":OO0OOOO0O00O00O00 ,"prizeBaseId":OOO0OO0O00O0O00O0 ,"prizeType":4 }},'8c6ae')#line:213
        return OOOO00OOO000OO00O #line:214
    async def superRedBagList (O00O0OOO00OOOOO00 ,O00O00OO00OO00O00 ,OOOO0OO00000OOOOO ):#line:222
        if O00O0OOO00OOOOO00 .verify_result !=True :#line:223
            await O00O0OOO00OOOOO00 .verify ()#line:224
        if O00O0OOO00OOOOO00 .verify_result !=True :#line:225
            O00O0OOO00OOOOO00 .log .error ("授权未通过 退出")#line:226
            sys .exit ()#line:227
        OO0000O0OO00O0O00 =await O00O0OOO00OOOOO00 .Get_H5st ('superRedBagList',O00O00OO00OO00O00 ,{"pageNum":1 ,"pageSize":100 ,"linkId":OOOO0OO00000OOOOO ,"business":"fission"},'f2b1d')#line:230
        for OO000OO00OO0O00OO in OO0000O0OO00O0O00 ['data']['items']:#line:231
            OO00000OO00OO0OOO ,OOO000O0O0OOOOO0O ,OOO000O00000O00O0 ,OO0O00O0000OOO000 ,O0000OO0OOOO0O00O ,O0O0O0000O0OO0OO0 ,O0O0OOO00000OO000 ,O0OOO000OO0OO000O ,OO0O0O0OOO0OO0OO0 =(OO000OO00OO0O00OO ['id'],OO000OO00OO0O00OO ['amount'],OO000OO00OO0O00OO ['prizeType'],OO000OO00OO0O00OO ['state'],OO000OO00OO0O00OO ['prizeConfigName'],OO000OO00OO0O00OO ['prizeGroupId'],OO000OO00OO0O00OO ['poolBaseId'],OO000OO00OO0O00OO ['prizeBaseId'],OO000OO00OO0O00OO ['startTime'])#line:236
            if float (OOO000O0O0OOOOO0O )>1.0 :#line:238
                O00O0OOO00OOOOO00 .log .info (f"{OO0O0O0OOO0OO0OO0} {OOO000O0O0OOOOO0O}元 {'❌未提现' if OOO000O00000O00O0 == 4 and OO0O00O0000OOO000 != 3 else '✅已提现'}")#line:239
            if OOO000O00000O00O0 ==4 and OO0O00O0000OOO000 !=3 :#line:240
                OO0000O0OO00O0O00 =await O00O0OOO00OOOOO00 .apCashWithDraw (OOOO0OO00000OOOOO ,O00O00OO00OO00O00 ,OO00000OO00OO0OOO ,O0O0OOO00000OO000 ,O0O0O0000O0OO0OO0 ,O0OOO000OO0OO000O )#line:241
                if int (OO0000O0OO00O0O00 ['data']['status'])==310 :#line:242
                    O00O0OOO00OOOOO00 .log .info (f"✅{OOO000O0O0OOOOO0O}现金 提现成功")#line:243
                elif int (OO0000O0OO00O0O00 ['data']['status'])==50056 or int (OO0000O0OO00O0O00 ['data']['status'])==50001 :#line:244
                    O00O0OOO00OOOOO00 .log .warning (f"❌{OOO000O0O0OOOOO0O}现金 重新发起 提现失败:{OO0000O0OO00O0O00['data']['message']}")#line:245
                    time .sleep (3 )#line:246
                    await O00O0OOO00OOOOO00 .apCashWithDraw (OOOO0OO00000OOOOO ,O00O00OO00OO00O00 ,OO00000OO00OO0OOO ,O0O0OOO00000OO000 ,O0O0O0000O0OO0OO0 ,O0OOO000OO0OO000O )#line:247
                    if int (OO0000O0OO00O0O00 ['data']['status'])==310 :#line:248
                        O00O0OOO00OOOOO00 .log .info (f"✅{OOO000O0O0OOOOO0O}现金 提现成功")#line:249
                    else :#line:250
                        O00O0OOO00OOOOO00 .log .error (f"❌{OOO000O0O0OOOOO0O}现金 提现失败:{OO0000O0OO00O0O00['data']['message']}")#line:251
                else :#line:252
                    O00O0OOO00OOOOO00 .log .error (f"{OOO000O0O0OOOOO0O}现金 ❌提现错误:{OO0000O0OO00O0O00['data']['status']} {OO0000O0OO00O0O00['data']['message']}")#line:253
            else :#line:255
                continue #line:256
            time .sleep (1 )#line:257
    async def task_start (OOOOOO00OO00OO0O0 ):#line:258
        if OOOOOO00OO00OO0O0 .verify_result !=True :#line:259
            await OOOOOO00OO00OO0O0 .verify ()#line:260
        if OOOOOO00OO00OO0O0 .verify_result !=True :#line:261
            OOOOOO00OO00OO0O0 .log .error ("授权未通过 退出")#line:262
            sys .exit ()#line:263
        OOO0O0OOOO0OO0O00 =await OOOOOO00OO00OO0O0 .Get_H5st ('inviteFissionHome',OOOOOO00OO00OO0O0 .cookie ,{'linkId':OOOOOO00OO00OO0O0 .linkId ,"inviter":"",},'af89e')#line:264
        O00O0OOOOO0O0000O =OOO0O0OOOO0OO0O00 ['data']#line:265
        O0O0OOO0OO00OO00O =O00O0OOOOO0O0000O ['cashVo']#line:266
        OOOOOO00OO00OO0O0 .log .info (f"Name:{O0O0OOO0OO00OO00O['userInfo']['nickName']} 提现:{O0O0OOO0OO00OO00O['totalAmount']}元 当前:{O0O0OOO0OO00OO00O['amount']}元 进度{O0O0OOO0OO00OO00O['rate']}% 剩余时间:{OOOOOO00OO00OO0O0.convert_ms_to_hours_minutes(O00O0OOOOO0O0000O['countDownTime'])}")#line:267
        if int (O0O0OOO0OO00OO00O ['rate'])==100 :#line:268
            OOOOOO00OO00OO0O0 .log .info (f"本轮您已提现{O0O0OOO0OO00OO00O['totalAmount']}元了 等{OOOOOO00OO00OO0O0.convert_ms_to_hours_minutes(O00O0OOOOO0O0000O['countDownTime'])}后在来吧")#line:269
            await OOOOOO00OO00OO0O0 .superRedBagList (OOOOOO00OO00OO0O0 .cookie ,OOOOOO00OO00OO0O0 .linkId )#line:270
            return #line:271
        while True :#line:272
            O0000OO0OOO00OO0O =await OOOOOO00OO00OO0O0 .inviteFissionReceive (OOOOOO00OO00OO0O0 .cookie ,OOOOOO00OO00OO0O0 .linkId )#line:273
            if not O0000OO0OOO00OO0O :#line:274
                break #line:275
            time .sleep (1.5 )#line:276
if __name__ =='__main__':#line:279
    pdd =TEN_JD_PDD_DRAW ()#line:280
    loop =asyncio .get_event_loop ()#line:281
    loop .run_until_complete (pdd .task_start ())#line:282
    loop .close ()#line:283
