"""
File: TEN_JD_PDD.py(邀好友赢现金-抽奖)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-抽奖');
"""


from utils .logger import setup_logger #line:11
from utils .X_API_EID_TOKEN import *#line:12
from utils .User_agent import generate_random_user_agent #line:13
import asyncio ,aiohttp ,re ,os ,sys ,threading ,concurrent .futures ,time ,json #line:14
from utils .jdCookie import get_cookies #line:15
import time #line:16
try :#line:19
    ck =get_cookies ()#line:20
    if not ck :#line:21
        sys .exit ()#line:22
except :#line:23
    print ("未获取到有效COOKIE,退出程序！")#line:24
    sys .exit ()#line:25
class TEN_JD_PDD_DRAW (object ):#line:28
    def __init__ (OO0O000OO000O000O ):#line:29
        OO0O000OO000O000O .log =setup_logger ()#line:30
        OO0O000OO000O000O .start =time .time ()#line:31
        OO0O000OO000O000O .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:32
        OO0O000OO000O000O .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:33
        OO0O000OO000O000O .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:34
        OO0O000OO000O000O .numer_og =os .environ .get ("draw_numer")if os .environ .get ("draw_numer")else 3 #line:35
        OO0O000OO000O000O .activityUrl ="https://pro.m.jd.com"#line:36
        OO0O000OO000O000O .cookie =os .environ .get ("draw_cookie")if os .environ .get ("draw_cookie")else ck [0 ]#line:37
        OO0O000OO000O000O .linkId =[]#line:38
        OO0O000OO000O000O .amount =0 #line:39
        OO0O000OO000O000O .leftAmount =0 #line:40
        OO0O000OO000O000O .verify_result =False #line:41
        OO0O000OO000O000O .txj_status =False #line:42
        OO0O000OO000O000O .inviter =''#line:43
        OO0O000OO000O000O .power_success =[]#line:44
        OO0O000OO000O000O .power_failure =[]#line:45
        OO0O000OO000O000O .redpacket =[]#line:46
        OO0O000OO000O000O .cash =[]#line:47
        OO0O000OO000O000O .cash_redpacket =[]#line:48
        OO0O000OO000O000O .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:55
        OO0O000OO000O000O .rewardType ={1 :{'msg':'优惠券🎫'},2 :{'msg':'红包🧧'},6 :{'msg':'惊喜小礼包🎫'},}#line:60
        OO0O000OO000O000O .successful =[]#line:61
    async def retry_with_backoff (O000O000O0O0O00O0 ,O0O0000O0000O0000 ,OOOOO000000000O0O ,O0O0O0000O00O0O00 ,backoff_seconds =1 ):#line:63
        for OOOO000O00OOOO0O0 in range (OOOOO000000000O0O ):#line:64
            try :#line:65
                return await O0O0000O0000O0000 ()#line:66
            except asyncio .TimeoutError :#line:67
                O000O000O0O0O00O0 .log .debug (f'第{OOOO000O00OOOO0O0 + 1}次重试  {O0O0O0000O00O0O00} 请求超时')#line:68
                await asyncio .sleep (backoff_seconds )#line:69
            except Exception as O00OO000O0O00OO00 :#line:70
                O000O000O0O0O00O0 .log .debug (f'第{OOOO000O00OOOO0O0 + 1}次重试 {O0O0O0000O00O0O00}出错：{O00OO000O0O00OO00}')#line:71
                await asyncio .sleep (backoff_seconds )#line:72
                if OOOO000O00OOOO0O0 ==OOOOO000000000O0O :#line:73
                    O000O000O0O0O00O0 .log .error (f'{O0O0O0000O00O0O00}重试{OOOOO000000000O0O}次后仍然发生异常')#line:74
                    return #line:75
    async def GET_POST (O0O0OO0O000O00O00 ,O0000O0OO0OOOOO0O ,num =1 ):#line:77
        async def OOO0OO0O0OO000O00 ():#line:78
            async with aiohttp .ClientSession ()as O00O0000OO00OOOO0 :#line:79
                if O0000O0OO0OOOOO0O ['method']=='get':#line:80
                    async with O00O0000OO00OOOO0 .get (**O0000O0OO0OOOOO0O ['kwargs'])as OO0O00O0000O00O00 :#line:81
                        OO00OO0OO0O0OO0OO =OO0O00O0000O00O00 .status #line:82
                        O000O000O00000000 =await OO0O00O0000O00O00 .text ()#line:83
                else :#line:84
                    async with O00O0000OO00OOOO0 .post (**O0000O0OO0OOOOO0O ['kwargs'])as OO0O00O0000O00O00 :#line:85
                        OO00OO0OO0O0OO0OO =OO0O00O0000O00O00 .status #line:86
                        O000O000O00000000 =await OO0O00O0000O00O00 .text ()#line:87
                if OO00OO0OO0O0OO0OO !=200 :#line:88
                    await asyncio .sleep (3 )#line:89
                    if num >3 :#line:90
                        O0O0OO0O000O00O00 .log .warning (f'{OO00OO0OO0O0OO0OO}:状态超出3次')#line:91
                        return False ,False ,False #line:92
                    O0O0OO0O000O00O00 .log .debug (f'{OO00OO0OO0O0OO0OO}:去重试 第{num}次')#line:93
                    return await O0O0OO0O000O00O00 .GET_POST (O0000O0OO0OOOOO0O ,num +1 )#line:94
                try :#line:95
                    O00OOOOO0OO0OOO00 =json .loads (O000O000O00000000 )#line:96
                except :#line:97
                    O00OOOOO0OO0OOO00 =O000O000O00000000 #line:98
                return OO00OO0OO0O0OO0OO ,O000O000O00000000 ,O00OOOOO0OO0OOO00 #line:99
        return await O0O0OO0O000O00O00 .retry_with_backoff (OOO0OO0O0OO000O00 ,3 ,f'GET_POST')#line:101
    async def verify (OO0O000000OO0O0O0 ):#line:103
        async def OOOOOOO00OOO0O0OO ():#line:104
            O0OOOO00O000OOO0O ='https://api.ixu.cc/verify'#line:105
            async with aiohttp .ClientSession ()as OO0OOOO0O0O0O0OOO :#line:106
                async with OO0OOOO0O0O0O0OOO .get (O0OOOO00O000OOO0O ,data ={'TOKEN':OO0O000000OO0O0O0 .token },timeout =3 )as O0000O000OO0OOO00 :#line:107
                    OO0OO00O00OO00O0O =await O0000O000OO0OOO00 .json ()#line:108
                    if O0000O000OO0OOO00 .status ==200 :#line:109
                        OO0O000000OO0O0O0 .verify_result =True #line:110
                        OO0O000000OO0O0O0 .log .info (f'认证通过 UserId：{OO0OO00O00OO00O0O["user_id"]}')#line:111
                        return OO0OO00O00OO00O0O #line:112
                    else :#line:113
                        OO0O000000OO0O0O0 .log .error (f"授权未通过:{OO0OO00O00OO00O0O['error']}")#line:114
                        sys .exit ()#line:115
        return await OO0O000000OO0O0O0 .retry_with_backoff (OOOOOOO00OOO0O0OO ,3 ,'verify')#line:117
    async def Get_H5st (O00OOO000OO0O0OOO ,OO000OO0OO0O0O000 ,OOOOO00OO0O00O0OO ,O0O00O0OO0OO00OOO ,OOO0000O0O00OOO0O ):#line:119
        if O00OOO000OO0O0OOO .verify_result !=True :#line:120
            await O00OOO000OO0O0OOO .verify ()#line:121
        if O00OOO000OO0O0OOO .verify_result !=True :#line:122
            O00OOO000OO0O0OOO .log .error ("授权未通过 退出")#line:123
            sys .exit ()#line:124
        O000O0OO000OO000O =generate_random_user_agent ()#line:125
        O0O0OO0OO0OOO000O ={'method':'','kwargs':{'url':'https://api.ouklc.com/api/h5st','params':{'functionId':OO000OO0OO0O0O000 ,'body':json .dumps (O0O00O0OO0OO00OOO ),'ua':O000O0OO000OO000O ,'pin':O00OOO000OO0O0OOO .pt_pin (OOOOO00OO0O00O0OO ),'appId':OOO0000O0O00OOO0O }}}#line:138
        O0000O00O00OO000O ,OOO00000000OO0OO0 ,OO0000OO00OOOOO0O =await O00OOO000OO0O0OOO .GET_POST (O0O0OO0OO0OOO000O )#line:139
        if O0000O00O00OO000O !=200 :#line:140
            return await O00OOO000OO0O0OOO .Get_H5st (OO000OO0OO0O0O000 ,OOOOO00OO0O00O0OO ,O0O00O0OO0OO00OOO ,OOO0000O0O00OOO0O )#line:141
        O0O0OO0OO0OOO000O ={'method':'post','kwargs':{'url':f'https://api.m.jd.com','headers':{"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OOOOO00OO0O00O0OO ,"User-Agent":O000O0OO000OO000O },'data':OO0000OO00OOOOO0O ["body"]}}#line:161
        O0000O00O00OO000O ,OOO00000000OO0OO0 ,OO0000OO00OOOOO0O =await O00OOO000OO0O0OOO .GET_POST (O0O0OO0OO0OOO000O )#line:162
        return OO0000OO00OOOOO0O #line:163
    def pt_pin (OOO000O0O0O00O00O ,O0000OOOO0000O0O0 ):#line:165
        try :#line:166
            OO0O0O0OO0O0OOO0O =re .compile (r'pt_pin=(.*?);').findall (O0000OOOO0000O0O0 )[0 ]#line:167
            OO0O0O0OO0O0OOO0O =unquote_plus (OO0O0O0OO0O0OOO0O )#line:168
        except IndexError :#line:169
            OO0O0O0OO0O0OOO0O =re .compile (r'pin=(.*?);').findall (O0000OOOO0000O0O0 )[0 ]#line:170
            OO0O0O0OO0O0OOO0O =unquote_plus (OO0O0O0OO0O0OOO0O )#line:171
        return OO0O0O0OO0O0OOO0O #line:172
    def convert_ms_to_hours_minutes (OOOOO00O0O00OOOOO ,O0OO00OO000O0OO00 ):#line:174
        OO0O00O0000O0000O =O0OO00OO000O0OO00 //1000 #line:175
        O00OOOO0000O00OOO ,OO0O00O0000O0000O =divmod (OO0O00O0000O0000O ,60 )#line:176
        O0OOO0O0OO0O0OOO0 ,O00OOOO0000O00OOO =divmod (O00OOOO0000O00OOO ,60 )#line:177
        return f'{O0OOO0O0OO0O0OOO0}小时{O00OOOO0000O00OOO}分'#line:178
    async def inviteFissionReceive (O000000O00O000OOO ,O0O0O0O0O00O0OO0O ,OOO00OOOOO0O000O0 ,page =1 ):#line:180
        if O000000O00O000OOO .verify_result !=True :#line:181
            await O000000O00O000OOO .verify ()#line:182
        if O000000O00O000OOO .verify_result !=True :#line:183
            O000000O00O000OOO .log .error ("授权未通过 退出")#line:184
            sys .exit ()#line:185
        OOO0O00O000O0OOO0 =generate_random_user_agent ()#line:186
        OOO0OO000OO0OO0OO ={'linkId':OOO00OOOOO0O000O0 ,}#line:189
        OO000OOO00OOOOOO0 =await O000000O00O000OOO .Get_H5st ('inviteFissionReceive',O0O0O0O0O00O0OO0O ,OOO0OO000OO0OO0OO ,'02f8d')#line:190
        if OO000OOO00OOOOOO0 ['success']==False and OO000OOO00OOOOOO0 ['errMsg']=='活动太火爆，请稍候重试':#line:191
            OOO0O0OO0O0O000O0 =f'还差{O000000O00O000OOO.leftAmount / O000000O00O000OOO.amount}次'if O000000O00O000OOO .amount !=0 else '先去助力一次才能计算需要人数'#line:192
            O000000O00O000OOO .log .debug (f'没助理了 快去助理吧 {OOO0O0OO0O0O000O0}')#line:193
            await O000000O00O000OOO .superRedBagList (O0O0O0O0O00O0OO0O ,OOO00OOOOO0O000O0 ,page )#line:194
            return False #line:195
        if OO000OOO00OOOOOO0 ['success']and OO000OOO00OOOOOO0 ['code']==0 :#line:201
            O000000O00O000OOO .amount =float (OO000OOO00OOOOOO0 ["data"]["receiveList"][0 ]["amount"])#line:202
            O000000O00O000OOO .leftAmount =float (OO000OOO00OOOOOO0 ["data"]["leftAmount"])#line:203
            O000000O00O000OOO .log .info (f'领取中:{OO000OOO00OOOOOO0["data"]["totalAmount"]} 当前:{OO000OOO00OOOOOO0["data"]["amount"]} 获得:{OO000OOO00OOOOOO0["data"]["receiveList"][0]["amount"]} 还差:{OO000OOO00OOOOOO0["data"]["leftAmount"]}元/{O000000O00O000OOO.leftAmount / O000000O00O000OOO.amount}次 当前进度:{OO000OOO00OOOOOO0["data"]["rate"]}%')#line:205
            if int (OO000OOO00OOOOOO0 ["data"]["rate"])==100 :#line:206
                O000000O00O000OOO .log .info (f'领取中:{OO000OOO00OOOOOO0["data"]["totalAmount"]} 进度:{OO000OOO00OOOOOO0["data"]["rate"]}% 退出!')#line:207
                await O000000O00O000OOO .superRedBagList (O0O0O0O0O00O0OO0O ,OOO00OOOOO0O000O0 ,page )#line:208
                return False #line:209
        return True #line:210
    async def apCashWithDraw (O00OOO00000000OO0 ,OO0000O0OO0OOO0OO ,OOO0OOOO00O0O0OOO ,OO0O00O0O0OO0000O ,OO0O00OO000OOOOOO ,OO000O000OOOO0OOO ,O00O0O0O00OO00O00 ):#line:212
        if O00OOO00000000OO0 .verify_result !=True :#line:213
            await O00OOO00000000OO0 .verify ()#line:214
        if O00OOO00000000OO0 .verify_result !=True :#line:215
            O00OOO00000000OO0 .log .error ("授权未通过 退出")#line:216
            sys .exit ()#line:217
        OO00O000O0000O0O0 =generate_random_user_agent ()#line:218
        O00O00O00O000O000 =await O00OOO00000000OO0 .Get_H5st ("apCashWithDraw",OOO0OOOO00O0O0OOO ,{"linkId":OO0000O0OO0OOO0OO ,"businessSource":"NONE","base":{"id":OO0O00O0O0OO0000O ,"business":"fission","poolBaseId":OO0O00OO000OOOOOO ,"prizeGroupId":OO000O000OOOO0OOO ,"prizeBaseId":O00O0O0O00OO00O00 ,"prizeType":4 }},'8c6ae')#line:234
        return O00O00O00O000O000 #line:235
    async def inviteFissionBeforeHome (O00O00OO00O00O0O0 ,num =1 ):#line:237
        OOO00OO0000000000 =False #line:238
        for OO0000OOO0O00000O in ck :#line:239
            if len (O00O00OO00O00O0O0 .power_success )>=num :#line:240
                return await O00O00OO00O00O0O0 .inviteFissionReceive (O00O00OO00O00O0O0 .cookie ,O00O00OO00O00O0O0 .linkId )#line:241
            OO00O0OO0OO0O0O0O =await O00O00OO00O00O0O0 .Get_H5st ("inviteFissionBeforeHome",OO0000OOO0O00000O ,{'linkId':O00O00OO00O00O0O0 .linkId ,"isJdApp":True ,'inviter':O00O00OO00O00O0O0 .inviter },'02f8d',)#line:244
            if int (OO00O0OO0OO0O0O0O ['code'])==0 :#line:245
                for OOO00OO0O000OOOOO ,OOOO0000OOO0O00O0 in O00O00OO00O00O0O0 .helpResult :#line:246
                    if OO00O0OO0OO0O0O0O ['data']['helpResult']==int (OOO00OO0O000OOOOO ):#line:247
                        OOO00OO0000000000 =True #line:248
                        O00O00OO00O00O0O0 .log .info (f"Id:{O00O00OO00O00O0O0.linkId[:4] + '****' + O00O00OO00O00O0O0.linkId[-4:]}|助理:{OO00O0OO0OO0O0O0O['data']['nickName']}|{OO00O0OO0OO0O0O0O['data']['helpResult']}|{O00O00OO00O00O0O0.pt_pin(OO0000OOO0O00000O)}|{OOOO0000OOO0O00O0}")#line:250
                        if OO00O0OO0OO0O0O0O ['data']['helpResult']==1 :#line:251
                            O00O00OO00O00O0O0 .power_success .append (OO0000OOO0O00000O )#line:252
                        else :#line:253
                            O00O00OO00O00O0O0 .power_failure .append (OO0000OOO0O00000O )#line:254
                    if not OOO00OO0000000000 :#line:255
                        OOOO0000OOO0O00O0 ='❌未知状态 (可能是活动未开启！！！)'#line:256
                        O00O00OO00O00O0O0 .power_failure .append (OO0000OOO0O00000O )#line:257
                        O00O00OO00O00O0O0 .log .info (f"Id:{O00O00OO00O00O0O0.linkId[:4] + '****' + O00O00OO00O00O0O0.linkId[-4:]}|助理:{OO00O0OO0OO0O0O0O['data']['nickName']}|{OO00O0OO0OO0O0O0O['data']['helpResult']}|{O00O00OO00O00O0O0.pt_pin(OO0000OOO0O00000O)}|{OOOO0000OOO0O00O0}")#line:259
            else :#line:260
                O00O00OO00O00O0O0 .log .info (f"{O00O00OO00O00O0O0.pt_pin(OO0000OOO0O00000O)}{OO00O0OO0OO0O0O0O['code']} 结果:💔{OO00O0OO0OO0O0O0O['errMsg']}")#line:261
    async def superRedBagList (O00O0O0O0O0OOOO0O ,OO0O00O0O0O000OOO ,OOO000OOOO00OOOO0 ,OO000OO0OOOOO0OO0 ):#line:263
        if O00O0O0O0O0OOOO0O .verify_result !=True :#line:264
            await O00O0O0O0O0OOOO0O .verify ()#line:265
        if O00O0O0O0O0OOOO0O .verify_result !=True :#line:266
            O00O0O0O0O0OOOO0O .log .error ("授权未通过 退出")#line:267
            sys .exit ()#line:268
        OOOOO0OO00OO0O000 =await O00O0O0O0O0OOOO0O .Get_H5st ('superRedBagList',OO0O00O0O0O000OOO ,{"pageNum":OO000OO0OOOOO0OO0 ,"pageSize":200 ,"linkId":OOO000OOOO00OOOO0 ,"business":"fission"},'f2b1d')#line:271
        O00O0O0O0O0OOOO0O .log .info (f"开始提取{OO000OO0OOOOO0OO0}页, 共{len(OOOOO0OO00OO0O000['data']['items'])}条记录")#line:272
        if len (OOOOO0OO00OO0O000 ['data']['items'])==0 :#line:273
            return False #line:274
        for O0OOOOO0O00O0O000 in OOOOO0OO00OO0O000 ['data']['items']:#line:275
            OOOO0O0OO0OOO0OOO ,O000OOO00O0OOOOO0 ,OO00OO00OOOO0OOO0 ,O00O000OOO000OOO0 ,OO0O00O0OO00O0OOO ,O0OO0O0OOOOO00O00 ,O0O0O00O0OO00O0O0 ,O0O0OO0OO00OOOOO0 ,OOOOOO0O0OOO0O0OO =(O0OOOOO0O00O0O000 ['id'],O0OOOOO0O00O0O000 ['amount'],O0OOOOO0O00O0O000 ['prizeType'],O0OOOOO0O00O0O000 ['state'],O0OOOOO0O00O0O000 ['prizeConfigName'],O0OOOOO0O00O0O000 ['prizeGroupId'],O0OOOOO0O00O0O000 ['poolBaseId'],O0OOOOO0O00O0O000 ['prizeBaseId'],O0OOOOO0O00O0O000 ['startTime'])#line:280
            if float (O000OOO00O0OOOOO0 )>1.0 :#line:281
                O00O0O0O0O0OOOO0O .log .info (f"{OOOOOO0O0OOO0O0OO} {O000OOO00O0OOOOO0}元 {'❌未提现' if OO00OO00OOOO0OOO0 == 4 and O00O000OOO000OOO0 != 3 else '✅已提现'}")#line:282
            if OO00OO00OOOO0OOO0 ==4 and O00O000OOO000OOO0 !=3 :#line:283
                OOOOO0OO00OO0O000 =await O00O0O0O0O0OOOO0O .apCashWithDraw (OOO000OOOO00OOOO0 ,OO0O00O0O0O000OOO ,OOOO0O0OO0OOO0OOO ,O0O0O00O0OO00O0O0 ,O0OO0O0OOOOO00O00 ,O0O0OO0OO00OOOOO0 )#line:284
                if int (OOOOO0OO00OO0O000 ['data']['status'])==310 :#line:286
                    O00O0O0O0O0OOOO0O .log .info (f"✅{O000OOO00O0OOOOO0}现金💵 提现成功")#line:287
                    O00O0O0O0O0OOOO0O .successful .append (O000OOO00O0OOOOO0 )#line:288
                elif int (OOOOO0OO00OO0O000 ['data']['status'])==50056 or int (OOOOO0OO00OO0O000 ['data']['status'])==50001 :#line:289
                    O00O0O0O0O0OOOO0O .log .warning (f"❌{O000OOO00O0OOOOO0}现金💵 重新发起 提现失败:{OOOOO0OO00OO0O000['data']['message']}")#line:290
                    time .sleep (3 )#line:291
                    await O00O0O0O0O0OOOO0O .apCashWithDraw (OOO000OOOO00OOOO0 ,OO0O00O0O0O000OOO ,OOOO0O0OO0OOO0OOO ,O0O0O00O0OO00O0O0 ,O0OO0O0OOOOO00O00 ,O0O0OO0OO00OOOOO0 )#line:292
                    if int (OOOOO0OO00OO0O000 ['data']['status'])==310 :#line:293
                        O00O0O0O0O0OOOO0O .log .info (f"✅{O000OOO00O0OOOOO0}现金💵 提现成功")#line:294
                        O00O0O0O0O0OOOO0O .successful .append (O000OOO00O0OOOOO0 )#line:295
                    else :#line:296
                        O00O0O0O0O0OOOO0O .log .error (f"❌{O000OOO00O0OOOOO0}现金💵 提现失败:{OOOOO0OO00OO0O000['data']['message']}")#line:297
                elif '金额超过自然月上限'in OOOOO0OO00OO0O000 ['data']['message']:#line:298
                    O00O0O0O0O0OOOO0O .log .info (f"{O000OOO00O0OOOOO0}现金:{OOOOO0OO00OO0O000['data']['message']}:去兑换红包")#line:299
                    await O00O0O0O0O0OOOO0O .apRecompenseDrawPrize (OOO000OOOO00OOOO0 ,OO0O00O0O0O000OOO ,OOOO0O0OO0OOO0OOO ,O0O0O00O0OO00O0O0 ,O0OO0O0OOOOO00O00 ,O0O0OO0OO00OOOOO0 ,O000OOO00O0OOOOO0 )#line:300
                else :#line:301
                    O00O0O0O0O0OOOO0O .log .error (f"{O000OOO00O0OOOOO0}现金 ❌提现错误:{OOOOO0OO00OO0O000['data']['status']} {OOOOO0OO00OO0O000['data']['message']}")#line:302
            else :#line:304
                continue #line:305
            await asyncio .sleep (0.5 )#line:306
    async def apRecompenseDrawPrize (O000O000OO000000O ,OO0O0000000OO0O00 ,O0O00OO0OO00OO0OO ,O000O0O0OOOO00O0O ,OO0OO0OO00O000OOO ,OO0OO0000O0O0O00O ,OOO0000OOOO000O00 ,OOOO0OO00O000O000 ):#line:308
        OO0O0O0OO00OO0O00 =await O000O000OO000000O .Get_H5st ('apRecompenseDrawPrize',O0O00OO0OO00OO0OO ,{"linkId":OO0O0000000OO0O00 ,"businessSource":"fission","drawRecordId":O000O0O0OOOO00O0O ,"business":"fission","poolId":OO0OO0OO00O000OOO ,"prizeGroupId":OO0OO0000O0O0O00O ,"prizeId":OOO0000OOOO000O00 ,},'8c6ae')#line:318
        if OO0O0O0OO00OO0O00 ['success']and int (OO0O0O0OO00OO0O00 ['data']['resCode'])==0 :#line:319
            O000O000OO000000O .log .info (f"{OOOO0OO00O000O000}现金:🧧红包兑换成功")#line:320
            O000O000OO000000O .cash_redpacket .append (OOOO0OO00O000O000 )#line:321
        else :#line:322
            O000O000OO000000O .log .info (f"{OOOO0OO00O000O000}现金:🧧红包兑换失败 {OO0O0O0OO00OO0O00}")#line:323
    async def Fission_Draw (OOOO0OOOOOOOOO0O0 ,O0OOOOOO0O00OOO0O ,OO0O0000O0OO0OOO0 ):#line:324
        while True :#line:326
            O0OO0O0OO00O0OOO0 =await OOOO0OOOOOOOOO0O0 .Get_H5st ('inviteFissionDrawPrize',O0OOOOOO0O00OOO0O ,{"linkId":OO0O0000O0OO0OOO0 },'c02c6')#line:329
            if not O0OO0O0OO00O0OOO0 ['success']:#line:331
                if "抽奖次数已用完"in O0OO0O0OO00O0OOO0 ['errMsg']:#line:332
                    OOOO0OOOOOOOOO0O0 .log .debug (f"⚠️抽奖次数已用完")#line:333
                    break #line:334
                elif "本场活动已结束"in O0OO0O0OO00O0OOO0 ['errMsg']:#line:335
                    OOOO0OOOOOOOOO0O0 .log .debug (f"⏰本场活动已结束了,快去重新开始吧")#line:336
                    sys .exit ()#line:337
            try :#line:338
                if int (O0OO0O0OO00O0OOO0 ['data']['rewardType'])in OOOO0OOOOOOOOO0O0 .rewardType :#line:341
                    OOOO0OOOOOOOOO0O0 .log .info (f"获得:{O0OO0O0OO00O0OOO0['data']['prizeValue']}元{OOOO0OOOOOOOOO0O0.rewardType[int(O0OO0O0OO00O0OOO0['data']['rewardType'])]['msg']}")#line:342
                    if int (O0OO0O0OO00O0OOO0 ['data']['rewardType'])==2 :#line:343
                        OOOO0OOOOOOOOO0O0 .redpacket .append (float (O0OO0O0OO00O0OOO0 ['data']['prizeValue']))#line:344
                else :#line:345
                    OOOO0OOOOOOOOO0O0 .log .info (f"获得:{O0OO0O0OO00O0OOO0['data']['prizeValue']}元现金💵")#line:346
                    OOOO0OOOOOOOOO0O0 .cash .append (float (O0OO0O0OO00O0OOO0 ['data']['prizeValue']))#line:347
            except Exception as OOO0O0OOOOOO0O000 :#line:348
                OOOO0OOOOOOOOO0O0 .log .error (f'(未知物品):{O0OO0O0OO00O0OOO0}')#line:349
            await asyncio .sleep (2 )#line:350
        OOOO0OOOOOOOOO0O0 .log .info (f"抽奖结束: 💵现金:{'{:.2f}'.format(sum([float(O0O0000OO00O0OOOO) for O0O0000OO00O0OOOO in OOOO0OOOOOOOOO0O0.cash]))}元, 🧧红包:{'{:.2f}'.format(sum([float(O0O00OO000OOOOOO0) for O0O00OO000OOOOOO0 in OOOO0OOOOOOOOO0O0.redpacket]))}元")#line:351
        OOOO0OOOOOOOOO0O0 .log .info (f"****************开始提现****************")#line:352
        OO00000OOO0O00OOO =0 #line:353
        while True :#line:354
            OO00000OOO0O00OOO =OO00000OOO0O00OOO +1 #line:355
            O0O0OOO0OOO00OOO0 =await OOOO0OOOOOOOOO0O0 .superRedBagList (O0OOOOOO0O00OOO0O ,OO0O0000O0OO0OOO0 ,OO00000OOO0O00OOO )#line:356
            await asyncio .sleep (1 )#line:357
            if not O0O0OOO0OOO00OOO0 :#line:358
                break #line:359
        O0OOOO00OOOO0O000 =('提现结束: ')+(f"💵现金:{'{:.2f}'.format(sum([float(OO00000O00000OOO0) for OO00000O00000OOO0 in OOOO0OOOOOOOOO0O0.successful]))}元, "if OOOO0OOOOOOOOO0O0 .successful else "")+(f"🧧兑换红包:{'{:.2f}'.format(sum([float(OO000O0OOO0OO000O) for OO000O0OOO0OO000O in OOOO0OOOOOOOOO0O0.cash_redpacket]))}元"if OOOO0OOOOOOOOO0O0 .cash_redpacket else "")#line:365
        if not OOOO0OOOOOOOOO0O0 .successful and not OOOO0OOOOOOOOO0O0 .cash_redpacket :#line:366
            O0OOOO00OOOO0O000 ='提现结束: 一毛都没有哦！'#line:367
        OOOO0OOOOOOOOO0O0 .log .info (O0OOOO00OOOO0O000 )#line:368
    async def add_LinkId (OOOOO00OOO00000O0 ):#line:371
        async def OO0OO000000000OOO ():#line:372
            if OOOOO00OOO00000O0 .verify_result !=True :#line:373
                await OOOOO00OOO00000O0 .verify ()#line:374
            if OOOOO00OOO00000O0 .verify_result !=True :#line:375
                OOOOO00OOO00000O0 .log .error ("授权未通过 退出")#line:376
                sys .exit ()#line:377
            OO000O000OO0000O0 ='https://api.ixu.cc/status/inviter.json'#line:378
            async with aiohttp .ClientSession ()as O0000OO00OO0O0000 :#line:379
                async with O0000OO00OO0O0000 .get (OO000O000OO0000O0 ,timeout =5 )as O000OOOO000O00OO0 :#line:380
                    if O000OOOO000O00OO0 .status ==200 :#line:381
                        OO00OOO00O000OO00 =await O000OOOO000O00OO0 .json ()#line:382
                        if OO00OOO00O000OO00 ['stats']!='True':#line:383
                            OOOOO00OOO00000O0 .log .error (f"{OO00OOO00O000OO00['err_text']}")#line:384
                            sys .exit ()#line:385
                        OOOOO00OOO00000O0 .inviter_help =OO00OOO00O000OO00 ['inviter']#line:386
                        if len (OO00OOO00O000OO00 ['text'])>0 :#line:387
                            OOOOO00OOO00000O0 .log .debug (f'那女孩对你说:{OO00OOO00O000OO00["text"]}')#line:388
                        if OOOOO00OOO00000O0 .scode =='ALL'or OOOOO00OOO00000O0 .scode =='all':#line:389
                            for O0OOOOOO0OOO000OO in OO00OOO00O000OO00 ['linkId']:#line:390
                                OOOOO00OOO00000O0 .linkId .append (O0OOOOOO0OOO000OO )#line:391
                                OOOOO00OOO00000O0 .log .info (f'云端获取到linkId:{O0OOOOOO0OOO000OO}')#line:392
                            return True #line:393
                        else :#line:394
                            OOOOO00OOO00000O0 .linkId .append (OO00OOO00O000OO00 ['linkId'][int (OOOOO00OOO00000O0 .scode )-1 ])#line:395
                            OOOOO00OOO00000O0 .log .info (f'云端获取到linkId:{OO00OOO00O000OO00["linkId"][int(OOOOO00OOO00000O0.scode) - 1]}')#line:396
                            return True #line:397
                    else :#line:398
                        OOOOO00OOO00000O0 .log .error ('未获取到linkId 重试')#line:399
        return await OOOOO00OOO00000O0 .retry_with_backoff (OO0OO000000000OOO ,3 ,'linkId')#line:401
    async def task_start (O0O0O00O00O0O0000 ):#line:402
        if O0O0O00O00O0O0000 .verify_result !=True :#line:403
            await O0O0O00O00O0O0000 .verify ()#line:404
        if O0O0O00O00O0O0000 .verify_result !=True :#line:405
            O0O0O00O00O0O0000 .log .error ("授权未通过 退出")#line:406
            sys .exit ()#line:407
        await O0O0O00O00O0O0000 .add_LinkId ()#line:408
        OO000OO00O0O00OO0 =O0O0O00O00O0O0000 .cookie #line:411
        if O0O0O00O00O0O0000 .txj_status :#line:412
            try :#line:413
                O0O00000O0OOO0O00 =await O0O0O00O00O0O0000 .Get_H5st ('inviteFissionHome',OO000OO00O0O00OO0 ,{'linkId':O0O0O00O00O0O0000 .linkId ,"inviter":"",},'af89e')#line:414
                if not O0O00000O0OOO0O00 ['success']and O0O00000O0OOO0O00 ['errMsg']=='未登录':#line:416
                    O0O0O00O00O0O0000 .log .error (f"{O0O00000O0OOO0O00['errMsg']}")#line:417
                    return #line:418
                O00OO00000O0OOO00 =O0O00000O0OOO0O00 ['data']#line:419
                if O00OO00000O0OOO00 ['cashVo']!=None :#line:420
                    O00OOOOOOOOOOOO00 =O00OO00000O0OOO00 ['cashVo']#line:421
                    O0O0O00O00O0O0000 .log .info (f"Name:{O00OOOOOOOOOOOO00['userInfo']['nickName']} 已助理:{O00OO00000O0OOO00['prizeNum']} 提现:{O00OOOOOOOOOOOO00['totalAmount']}元 当前:{O00OOOOOOOOOOOO00['amount']}元 进度{O00OOOOOOOOOOOO00['rate']}% 剩余时间:{O0O0O00O00O0O0000.convert_ms_to_hours_minutes(O00OO00000O0OOO00['countDownTime'])}")#line:423
                    if int (O00OOOOOOOOOOOO00 ['rate'])==100 :#line:424
                        O0O0O00O00O0O0000 .log .info (f"本轮您已提现{O00OOOOOOOOOOOO00['totalAmount']}元了 等{O0O0O00O00O0O0000.convert_ms_to_hours_minutes(O00OO00000O0OOO00['countDownTime'])}后在来吧")#line:426
                        await O0O0O00O00O0O0000 .superRedBagList (OO000OO00O0O00OO0 ,O0O0O00O00O0O0000 .linkId ,1 )#line:427
                        return #line:428
                else :#line:429
                    O0O0O00O00O0O0000 .log .error ('哦和 黑号了哦')#line:430
                while True :#line:432
                    OOO0OOO00OO00OO00 =await O0O0O00O00O0O0000 .inviteFissionReceive (OO000OO00O0O00OO0 ,O0O0O00O00O0O0000 .linkId )#line:433
                    if not OOO0OOO00OO00OO00 :#line:434
                        break #line:435
                    time .sleep (0.3 )#line:436
            except Exception as O0OOOO00OO0OO0000 :#line:437
                O0O0O00O00O0O0000 .log .error ('黑号')#line:438
        else :#line:439
            for OO0000O0O0OOO00OO in O0O0O00O00O0O0000 .linkId :#line:440
                O0O0O00O00O0O0000 .log .info (f'开始执行 LinkId:{OO0000O0O0OOO00OO}')#line:441
                await O0O0O00O00O0O0000 .Fission_Draw (OO000OO00O0O00OO0 ,OO0000O0O0OOO00OO )#line:442
if __name__ =='__main__':#line:445
    pdd =TEN_JD_PDD_DRAW ()#line:446
    loop =asyncio .get_event_loop ()#line:447
    loop .run_until_complete (pdd .task_start ())#line:448
    loop .close ()#line:449
