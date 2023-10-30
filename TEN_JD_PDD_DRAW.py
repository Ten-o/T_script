"""
File: TEN_JD_PDD.py(邀好友赢现金-抽奖)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-抽奖');
"""
""#line:9
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
    def __init__ (O0O00O00O000OO0O0 ):#line:28
        O0O00O00O000OO0O0 .log =setup_logger ()#line:29
        O0O00O00O000OO0O0 .start =time .time ()#line:30
        O0O00O00O000OO0O0 .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:31
        O0O00O00O000OO0O0 .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:32
        O0O00O00O000OO0O0 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:33
        O0O00O00O000OO0O0 .numer_og =os .environ .get ("draw_numer")if os .environ .get ("draw_numer")else 3 #line:34
        O0O00O00O000OO0O0 .activityUrl ="https://pro.m.jd.com"#line:35
        O0O00O00O000OO0O0 .cookie =os .environ .get ("draw_cookie")if os .environ .get ("draw_cookie")else ck [0 ]#line:36
        O0O00O00O000OO0O0 .linkId =[]#line:37
        O0O00O00O000OO0O0 .amount =0 #line:38
        O0O00O00O000OO0O0 .leftAmount =0 #line:39
        O0O00O00O000OO0O0 .verify_result =False #line:40
        O0O00O00O000OO0O0 .txj_status =False #line:41
        O0O00O00O000OO0O0 .inviter =''#line:42
        O0O00O00O000OO0O0 .power_success =[]#line:43
        O0O00O00O000OO0O0 .power_failure =[]#line:44
        O0O00O00O000OO0O0 .redpacket =[]#line:45
        O0O00O00O000OO0O0 .cash =[]#line:46
        O0O00O00O000OO0O0 .cash_redpacket =[]#line:47
        O0O00O00O000OO0O0 .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:54
        O0O00O00O000OO0O0 .rewardType ={1 :{'msg':'优惠券🎫'},2 :{'msg':'红包🧧'},6 :{'msg':'惊喜小礼包🎫'},}#line:59
        O0O00O00O000OO0O0 .successful =[]#line:60
    async def retry_with_backoff (O0OOO0000000O000O ,OOO00OOO0O000000O ,OO000OO0O0OOOOO0O ,O00O0O0O00OO0OO0O ,backoff_seconds =0 ):#line:62
        for OO0OOOO0000O0O0OO in range (OO000OO0O0OOOOO0O ):#line:63
            O00O0OO0OOO00OOO0 =False #line:64
            try :#line:65
                return await OOO00OOO0O000000O ()#line:66
            except asyncio .TimeoutError :#line:67
                if not O00O0OO0OOO00OOO0 :#line:68
                    O0OOO0000000O000O .log .debug (f'第{OO0OOOO0000O0O0OO + 1}次重试 {O00O0O0O00OO0OO0O} 请求超时')#line:69
                    O00O0OO0OOO00OOO0 =True #line:70
                await asyncio .sleep (backoff_seconds )#line:71
            except Exception as OOO00OO00OO0OOO00 :#line:72
                if not O00O0OO0OOO00OOO0 :#line:73
                    O0OOO0000000O000O .log .debug (f'第{OO0OOOO0000O0O0OO + 1}次重试 {O00O0O0O00OO0OO0O} 出错：{OOO00OO00OO0OOO00}')#line:74
                    O00O0OO0OOO00OOO0 =True #line:75
                await asyncio .sleep (backoff_seconds )#line:76
            if O00O0OO0OOO00OOO0 and OO0OOOO0000O0O0OO ==OO000OO0O0OOOOO0O -1 :#line:78
                O0OOO0000000O000O .log .error (f'{O00O0O0O00OO0OO0O} 重试{OO000OO0O0OOOOO0O}次后仍然发生异常')#line:79
                return False ,False ,False #line:80
    async def GET_POST (OOO0OO00O0O00O000 ,O0O00O00OO000OO0O ,num =1 ):#line:82
        async def OOO00O0OOO0O0O00O ():#line:83
            async with aiohttp .ClientSession ()as O0O00000O000OO000 :#line:84
                if O0O00O00OO000OO0O ['method']=='get':#line:85
                    async with O0O00000O000OO000 .get (**O0O00O00OO000OO0O ['kwargs'])as O0000OOO0OOO0O00O :#line:86
                        OO00OO000OOO0O00O =O0000OOO0OOO0O00O .status #line:87
                        OOO00000O00OO0O0O =await O0000OOO0OOO0O00O .text ()#line:88
                else :#line:89
                    async with O0O00000O000OO000 .post (**O0O00O00OO000OO0O ['kwargs'])as O0000OOO0OOO0O00O :#line:90
                        OO00OO000OOO0O00O =O0000OOO0OOO0O00O .status #line:91
                        OOO00000O00OO0O0O =await O0000OOO0OOO0O00O .text ()#line:92
                if OO00OO000OOO0O00O !=200 :#line:93
                    await asyncio .sleep (3 )#line:94
                    if num >3 :#line:95
                        OOO0OO00O0O00O000 .log .warning (f'{OO00OO000OOO0O00O}:状态超出3次')#line:96
                        return False ,False ,False #line:97
                    OOO0OO00O0O00O000 .log .debug (f'{OO00OO000OOO0O00O}:去重试 第{num}次')#line:98
                    return await OOO0OO00O0O00O000 .GET_POST (O0O00O00OO000OO0O ,num +1 )#line:99
                try :#line:100
                    O0OOO0OOOOOOO0000 =json .loads (OOO00000O00OO0O0O )#line:101
                except :#line:102
                    O0OOO0OOOOOOO0000 =OOO00000O00OO0O0O #line:103
                return OO00OO000OOO0O00O ,OOO00000O00OO0O0O ,O0OOO0OOOOOOO0000 #line:104
        return await OOO0OO00O0O00O000 .retry_with_backoff (OOO00O0OOO0O0O00O ,3 ,f'GET_POST')#line:106
    async def verify (O0O0OO0OOO0OO00OO ):#line:108
        async def OO00O0000OO0OOOO0 ():#line:109
            O0OO0O000OOOOO0O0 ='https://api.ixu.cc/verify'#line:110
            async with aiohttp .ClientSession ()as O0OOO0OOO0OO000O0 :#line:111
                async with O0OOO0OOO0OO000O0 .get (O0OO0O000OOOOO0O0 ,data ={'TOKEN':O0O0OO0OOO0OO00OO .token },timeout =3 )as OO00OO0O0OOO0000O :#line:112
                    OO0O0OOO00O0OO00O =await OO00OO0O0OOO0000O .json ()#line:113
                    if OO00OO0O0OOO0000O .status ==200 :#line:114
                        O0O0OO0OOO0OO00OO .verify_result =True #line:115
                        O0O0OO0OOO0OO00OO .log .info (f'认证通过 UserId：{OO0O0OOO00O0OO00O["user_id"]}')#line:116
                        return OO0O0OOO00O0OO00O #line:117
                    else :#line:118
                        O0O0OO0OOO0OO00OO .log .error (f"授权未通过:{OO0O0OOO00O0OO00O['error']}")#line:119
                        sys .exit ()#line:120
        return await O0O0OO0OOO0OO00OO .retry_with_backoff (OO00O0000OO0OOOO0 ,3 ,'verify')#line:122
    async def Get_H5st (OO00OO0OOOOO00OOO ,OO00OO000OOOOOO0O ,OO0OO000O0000000O ,O00OOO0O0O000OO0O ,OO0O0O000O0OO0OO0 ):#line:124
        if OO00OO0OOOOO00OOO .verify_result !=True :#line:125
            await OO00OO0OOOOO00OOO .verify ()#line:126
        if OO00OO0OOOOO00OOO .verify_result !=True :#line:127
            OO00OO0OOOOO00OOO .log .error ("授权未通过 退出")#line:128
            sys .exit ()#line:129
        OOOO0OO0O0O0OO0OO =generate_random_user_agent ()#line:130
        OOOOOO0O000OOO000 ={'method':'','kwargs':{'url':'https://api.ouklc.com/api/h5st','params':{'functionId':OO00OO000OOOOOO0O ,'body':json .dumps (O00OOO0O0O000OO0O ),'ua':OOOO0OO0O0O0OO0OO ,'pin':OO00OO0OOOOO00OOO .pt_pin (OO0OO000O0000000O ),'appId':OO0O0O000O0OO0OO0 }}}#line:143
        O0OOOOO0000000O00 ,OO00O000OOO0OOO00 ,OOO0OOO000OOOOOOO =await OO00OO0OOOOO00OOO .GET_POST (OOOOOO0O000OOO000 )#line:144
        if O0OOOOO0000000O00 !=200 :#line:146
            return await OO00OO0OOOOO00OOO .Get_H5st (OO00OO000OOOOOO0O ,OO0OO000O0000000O ,O00OOO0O0O000OO0O ,OO0O0O000O0OO0OO0 )#line:147
        OOOOOO0O000OOO000 ={'method':'post','kwargs':{'url':f'https://api.m.jd.com','headers':{"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OO0OO000O0000000O ,"User-Agent":OOOO0OO0O0O0OO0OO },'data':OOO0OOO000OOOOOOO ["body"]}}#line:167
        O0OOOOO0000000O00 ,OO00O000OOO0OOO00 ,OOO0OOO000OOOOOOO =await OO00OO0OOOOO00OOO .GET_POST (OOOOOO0O000OOO000 )#line:168
        return OOO0OOO000OOOOOOO #line:169
    def pt_pin (OO000OOOOOO0OO00O ,OOO00O00O0OOOOOO0 ):#line:171
        try :#line:172
            O000OO0OO0O0OOO0O =re .compile (r'pt_pin=(.*?);').findall (OOO00O00O0OOOOOO0 )[0 ]#line:173
            O000OO0OO0O0OOO0O =unquote_plus (O000OO0OO0O0OOO0O )#line:174
        except IndexError :#line:175
            O000OO0OO0O0OOO0O =re .compile (r'pin=(.*?);').findall (OOO00O00O0OOOOOO0 )[0 ]#line:176
            O000OO0OO0O0OOO0O =unquote_plus (O000OO0OO0O0OOO0O )#line:177
        return O000OO0OO0O0OOO0O #line:178
    def convert_ms_to_hours_minutes (OO0OO0000O0O0OO0O ,O000OO0OO00OO0000 ):#line:180
        OO0O0O000O00O0OO0 =O000OO0OO00OO0000 //1000 #line:181
        O00OO00O000O0OO0O ,OO0O0O000O00O0OO0 =divmod (OO0O0O000O00O0OO0 ,60 )#line:182
        O0OO0O0O0O00000OO ,O00OO00O000O0OO0O =divmod (O00OO00O000O0OO0O ,60 )#line:183
        return f'{O0OO0O0O0O00000OO}小时{O00OO00O000O0OO0O}分'#line:184
    async def inviteFissionReceive (OOOO00OOO0OO0O0OO ,OO000O000OOOO00O0 ,OO0OOO00O00O00000 ,page =1 ):#line:186
        if OOOO00OOO0OO0O0OO .verify_result !=True :#line:187
            await OOOO00OOO0OO0O0OO .verify ()#line:188
        if OOOO00OOO0OO0O0OO .verify_result !=True :#line:189
            OOOO00OOO0OO0O0OO .log .error ("授权未通过 退出")#line:190
            sys .exit ()#line:191
        O0OO00OO00OO00OOO =generate_random_user_agent ()#line:192
        O000OO0OO0O0O0OOO ={'linkId':OO0OOO00O00O00000 ,}#line:195
        O0O00OOOOO000O0O0 =await OOOO00OOO0OO0O0OO .Get_H5st ('inviteFissionReceive',OO000O000OOOO00O0 ,O000OO0OO0O0O0OOO ,'b8469')#line:196
        if O0O00OOOOO000O0O0 ['success']==False and O0O00OOOOO000O0O0 ['errMsg']=='活动太火爆，请稍候重试':#line:197
            O000O00000O000O00 =f'还差{OOOO00OOO0OO0O0OO.leftAmount / OOOO00OOO0OO0O0OO.amount}次'if OOOO00OOO0OO0O0OO .amount !=0 else '先去助力一次才能计算需要人数'#line:198
            OOOO00OOO0OO0O0OO .log .debug (f'没助理了 快去助理吧 {O000O00000O000O00}')#line:199
            await OOOO00OOO0OO0O0OO .superRedBagList (OO000O000OOOO00O0 ,OO0OOO00O00O00000 ,page )#line:200
            return False #line:201
        if O0O00OOOOO000O0O0 ['success']and O0O00OOOOO000O0O0 ['code']==0 :#line:207
            OOOO00OOO0OO0O0OO .amount =float (O0O00OOOOO000O0O0 ["data"]["receiveList"][0 ]["amount"])#line:208
            OOOO00OOO0OO0O0OO .leftAmount =float (O0O00OOOOO000O0O0 ["data"]["leftAmount"])#line:209
            OOOO00OOO0OO0O0OO .log .info (f'领取中:{O0O00OOOOO000O0O0["data"]["totalAmount"]} 当前:{O0O00OOOOO000O0O0["data"]["amount"]} 获得:{O0O00OOOOO000O0O0["data"]["receiveList"][0]["amount"]} 还差:{O0O00OOOOO000O0O0["data"]["leftAmount"]}元/{OOOO00OOO0OO0O0OO.leftAmount / OOOO00OOO0OO0O0OO.amount}次 当前进度:{O0O00OOOOO000O0O0["data"]["rate"]}%')#line:211
            if int (O0O00OOOOO000O0O0 ["data"]["rate"])==100 :#line:212
                OOOO00OOO0OO0O0OO .log .info (f'领取中:{O0O00OOOOO000O0O0["data"]["totalAmount"]} 进度:{O0O00OOOOO000O0O0["data"]["rate"]}% 退出!')#line:213
                await OOOO00OOO0OO0O0OO .superRedBagList (OO000O000OOOO00O0 ,OO0OOO00O00O00000 ,page )#line:214
                return False #line:215
        return True #line:216
    async def apCashWithDraw (OOO00O0OOOOO000OO ,O00000O0OO0000O00 ,O0OO000O0OO0000OO ,O0OOOOOO0O00OOOOO ,O00O00OO0O0OOOO00 ,O0OO0O0OO0OO0OOOO ,O00O0000O000O0OO0 ):#line:218
        if OOO00O0OOOOO000OO .verify_result !=True :#line:219
            await OOO00O0OOOOO000OO .verify ()#line:220
        if OOO00O0OOOOO000OO .verify_result !=True :#line:221
            OOO00O0OOOOO000OO .log .error ("授权未通过 退出")#line:222
            sys .exit ()#line:223
        OO00O0OOO00000O00 =generate_random_user_agent ()#line:224
        O00OOOO0OOO0000OO =await OOO00O0OOOOO000OO .Get_H5st ("apCashWithDraw",O0OO000O0OO0000OO ,{"linkId":O00000O0OO0000O00 ,"businessSource":"NONE","base":{"id":O0OOOOOO0O00OOOOO ,"business":"fission","poolBaseId":O00O00OO0O0OOOO00 ,"prizeGroupId":O0OO0O0OO0OO0OOOO ,"prizeBaseId":O00O0000O000O0OO0 ,"prizeType":4 }},'8c6ae')#line:240
        return O00OOOO0OOO0000OO #line:241
    async def inviteFissionBeforeHome (O0OO000000OOOO000 ,num =1 ):#line:243
        OOO0000O0O00O00O0 =False #line:244
        for O0OOO0OO00O0OOOOO in ck :#line:245
            if len (O0OO000000OOOO000 .power_success )>=num :#line:246
                return await O0OO000000OOOO000 .inviteFissionReceive (O0OO000000OOOO000 .cookie ,O0OO000000OOOO000 .linkId )#line:247
            O00O0OOO0000OOO00 =await O0OO000000OOOO000 .Get_H5st ("inviteFissionBeforeHome",O0OOO0OO00O0OOOOO ,{'linkId':O0OO000000OOOO000 .linkId ,"isJdApp":True ,'inviter':O0OO000000OOOO000 .inviter },'02f8d',)#line:250
            if int (O00O0OOO0000OOO00 ['code'])==0 :#line:251
                for OO00OO0000OOOO0O0 ,OOO00O0O00OO0OO0O in O0OO000000OOOO000 .helpResult :#line:252
                    if O00O0OOO0000OOO00 ['data']['helpResult']==int (OO00OO0000OOOO0O0 ):#line:253
                        OOO0000O0O00O00O0 =True #line:254
                        O0OO000000OOOO000 .log .info (f"Id:{O0OO000000OOOO000.linkId[:4] + '****' + O0OO000000OOOO000.linkId[-4:]}|助理:{O00O0OOO0000OOO00['data']['nickName']}|{O00O0OOO0000OOO00['data']['helpResult']}|{O0OO000000OOOO000.pt_pin(O0OOO0OO00O0OOOOO)}|{OOO00O0O00OO0OO0O}")#line:256
                        if O00O0OOO0000OOO00 ['data']['helpResult']==1 :#line:257
                            O0OO000000OOOO000 .power_success .append (O0OOO0OO00O0OOOOO )#line:258
                        else :#line:259
                            O0OO000000OOOO000 .power_failure .append (O0OOO0OO00O0OOOOO )#line:260
                    if not OOO0000O0O00O00O0 :#line:261
                        OOO00O0O00OO0OO0O ='❌未知状态 (可能是活动未开启！！！)'#line:262
                        O0OO000000OOOO000 .power_failure .append (O0OOO0OO00O0OOOOO )#line:263
                        O0OO000000OOOO000 .log .info (f"Id:{O0OO000000OOOO000.linkId[:4] + '****' + O0OO000000OOOO000.linkId[-4:]}|助理:{O00O0OOO0000OOO00['data']['nickName']}|{O00O0OOO0000OOO00['data']['helpResult']}|{O0OO000000OOOO000.pt_pin(O0OOO0OO00O0OOOOO)}|{OOO00O0O00OO0OO0O}")#line:265
            else :#line:266
                O0OO000000OOOO000 .log .info (f"{O0OO000000OOOO000.pt_pin(O0OOO0OO00O0OOOOO)}{O00O0OOO0000OOO00['code']} 结果:💔{O00O0OOO0000OOO00['errMsg']}")#line:267
    async def superRedBagList (O0O0O0OOOOOOOOO00 ,OOO0000O0O00OOO0O ,OOO0O0000OO0000O0 ,O00O000OOOO000OO0 ):#line:269
        if O0O0O0OOOOOOOOO00 .verify_result !=True :#line:270
            await O0O0O0OOOOOOOOO00 .verify ()#line:271
        if O0O0O0OOOOOOOOO00 .verify_result !=True :#line:272
            O0O0O0OOOOOOOOO00 .log .error ("授权未通过 退出")#line:273
            sys .exit ()#line:274
        OO0O00OO0O0OO00O0 =await O0O0O0OOOOOOOOO00 .Get_H5st ('superRedBagList',OOO0000O0O00OOO0O ,{"pageNum":O00O000OOOO000OO0 ,"pageSize":200 ,"linkId":OOO0O0000OO0000O0 ,"business":"fission"},'f2b1d')#line:277
        O0O0O0OOOOOOOOO00 .log .info (f"开始提取{O00O000OOOO000OO0}页, 共{len(OO0O00OO0O0OO00O0['data']['items'])}条记录")#line:278
        if len (OO0O00OO0O0OO00O0 ['data']['items'])==0 :#line:279
            return False #line:280
        for OO00O0O000O00OO0O in OO0O00OO0O0OO00O0 ['data']['items']:#line:281
            OO0O00000OO0OOO0O ,O0OOO0O000OOO00OO ,OO00OOO000O00O0O0 ,OO000O0O0O00O0000 ,OOO0000O00OOO00O0 ,OOO0O0000OOO00O00 ,OOOO000O00O00OO0O ,O00O0O0O0OO0OOO00 ,O0OOOOO00OO00000O =(OO00O0O000O00OO0O ['id'],OO00O0O000O00OO0O ['amount'],OO00O0O000O00OO0O ['prizeType'],OO00O0O000O00OO0O ['state'],OO00O0O000O00OO0O ['prizeConfigName'],OO00O0O000O00OO0O ['prizeGroupId'],OO00O0O000O00OO0O ['poolBaseId'],OO00O0O000O00OO0O ['prizeBaseId'],OO00O0O000O00OO0O ['startTime'])#line:286
            if float (O0OOO0O000OOO00OO )>1.0 :#line:287
                O0O0O0OOOOOOOOO00 .log .info (f"{O0OOOOO00OO00000O} {O0OOO0O000OOO00OO}元 {'❌未提现' if OO00OOO000O00O0O0 == 4 and OO000O0O0O00O0000 != 3 else '✅已提现'}")#line:288
            if OO00OOO000O00O0O0 ==4 and OO000O0O0O00O0000 !=3 :#line:289
                OO0O00OO0O0OO00O0 =await O0O0O0OOOOOOOOO00 .apCashWithDraw (OOO0O0000OO0000O0 ,OOO0000O0O00OOO0O ,OO0O00000OO0OOO0O ,OOOO000O00O00OO0O ,OOO0O0000OOO00O00 ,O00O0O0O0OO0OOO00 )#line:290
                if int (OO0O00OO0O0OO00O0 ['data']['status'])==310 :#line:292
                    O0O0O0OOOOOOOOO00 .log .info (f"✅{O0OOO0O000OOO00OO}现金💵 提现成功")#line:293
                    O0O0O0OOOOOOOOO00 .successful .append (O0OOO0O000OOO00OO )#line:294
                elif int (OO0O00OO0O0OO00O0 ['data']['status'])==50056 or int (OO0O00OO0O0OO00O0 ['data']['status'])==50001 :#line:295
                    O0O0O0OOOOOOOOO00 .log .warning (f"❌{O0OOO0O000OOO00OO}现金💵 重新发起 提现失败:{OO0O00OO0O0OO00O0['data']['message']}")#line:296
                    time .sleep (3 )#line:297
                    await O0O0O0OOOOOOOOO00 .apCashWithDraw (OOO0O0000OO0000O0 ,OOO0000O0O00OOO0O ,OO0O00000OO0OOO0O ,OOOO000O00O00OO0O ,OOO0O0000OOO00O00 ,O00O0O0O0OO0OOO00 )#line:298
                    if int (OO0O00OO0O0OO00O0 ['data']['status'])==310 :#line:299
                        O0O0O0OOOOOOOOO00 .log .info (f"✅{O0OOO0O000OOO00OO}现金💵 提现成功")#line:300
                        O0O0O0OOOOOOOOO00 .successful .append (O0OOO0O000OOO00OO )#line:301
                    else :#line:302
                        O0O0O0OOOOOOOOO00 .log .error (f"❌{O0OOO0O000OOO00OO}现金💵 提现失败:{OO0O00OO0O0OO00O0['data']['message']}")#line:303
                elif '金额超过自然月上限'in OO0O00OO0O0OO00O0 ['data']['message']:#line:304
                    O0O0O0OOOOOOOOO00 .log .info (f"{O0OOO0O000OOO00OO}现金:{OO0O00OO0O0OO00O0['data']['message']}:去兑换红包")#line:305
                    await O0O0O0OOOOOOOOO00 .apRecompenseDrawPrize (OOO0O0000OO0000O0 ,OOO0000O0O00OOO0O ,OO0O00000OO0OOO0O ,OOOO000O00O00OO0O ,OOO0O0000OOO00O00 ,O00O0O0O0OO0OOO00 ,O0OOO0O000OOO00OO )#line:306
                else :#line:307
                    O0O0O0OOOOOOOOO00 .log .error (f"{O0OOO0O000OOO00OO}现金 ❌提现错误:{OO0O00OO0O0OO00O0['data']['status']} {OO0O00OO0O0OO00O0['data']['message']}")#line:308
            else :#line:310
                continue #line:311
            await asyncio .sleep (0.5 )#line:312
    async def apRecompenseDrawPrize (OOO00OOOOOOO000OO ,O0O0OO0O00O0OOO0O ,OOOOOO0OOOOOOO00O ,O0O0O0O0000000000 ,O0OO000O0O0O00O00 ,O0OO0OOOO0OOOOOO0 ,OOOOOOOO0OO0OOOOO ,OOOO00O0000OO0OO0 ):#line:315
        OO0OOOOO0O000OOOO =await OOO00OOOOOOO000OO .Get_H5st ('apRecompenseDrawPrize',OOOOOO0OOOOOOO00O ,{"linkId":O0O0OO0O00O0OOO0O ,"businessSource":"fission","drawRecordId":O0O0O0O0000000000 ,"business":"fission","poolId":O0OO000O0O0O00O00 ,"prizeGroupId":O0OO0OOOO0OOOOOO0 ,"prizeId":OOOOOOOO0OO0OOOOO ,},'8c6ae')#line:325
        if OO0OOOOO0O000OOOO ['success']and int (OO0OOOOO0O000OOOO ['data']['resCode'])==0 :#line:326
            OOO00OOOOOOO000OO .log .info (f"{OOOO00O0000OO0OO0}现金:🧧红包兑换成功")#line:327
            OOO00OOOOOOO000OO .cash_redpacket .append (OOOO00O0000OO0OO0 )#line:328
        else :#line:329
            OOO00OOOOOOO000OO .log .info (f"{OOOO00O0000OO0OO0}现金:🧧红包兑换失败 {OO0OOOOO0O000OOOO}")#line:330
    async def Fission_Draw (O00O00OOOO0000OOO ,O00OOO0O000OOO00O ,O0O00O0OO0000000O ):#line:332
        O00O00OOOO0000OOO .log .info (f"****************开始抽奖****************")#line:333
        while True :#line:334
            O0O00OOOOOOOO000O =await O00O00OOOO0000OOO .Get_H5st ('inviteFissionDrawPrize',O00OOO0O000OOO00O ,{"linkId":O0O00O0OO0000000O },'c02c6')#line:337
            if not O0O00OOOOOOOO000O ['success']:#line:339
                if "抽奖次数已用完"in O0O00OOOOOOOO000O ['errMsg']:#line:340
                    O00O00OOOO0000OOO .log .debug (f"⚠️抽奖次数已用完")#line:341
                    break #line:342
                elif "本场活动已结束"in O0O00OOOOOOOO000O ['errMsg']:#line:343
                    O00O00OOOO0000OOO .log .debug (f"⏰本场活动已结束了,快去重新开始吧")#line:344
                    sys .exit ()#line:345
            try :#line:346
                if not O0O00OOOOOOOO000O ['success']:#line:347
                    O00O00OOOO0000OOO .log .warning (f'{O0O00OOOOOOOO000O["errMsg"]}')#line:348
                    continue #line:349
                if int (O0O00OOOOOOOO000O ['data']['rewardType'])in O00O00OOOO0000OOO .rewardType :#line:352
                    O00O00OOOO0000OOO .log .info (f"获得:{O0O00OOOOOOOO000O['data']['prizeValue']}元{O00O00OOOO0000OOO.rewardType[int(O0O00OOOOOOOO000O['data']['rewardType'])]['msg']}")#line:354
                    if int (O0O00OOOOOOOO000O ['data']['rewardType'])==2 :#line:355
                        O00O00OOOO0000OOO .redpacket .append (float (O0O00OOOOOOOO000O ['data']['prizeValue']))#line:356
                else :#line:357
                    O00O00OOOO0000OOO .log .info (f"获得:{O0O00OOOOOOOO000O['data']['prizeValue']}元现金💵")#line:358
                    O00O00OOOO0000OOO .cash .append (float (O0O00OOOOOOOO000O ['data']['prizeValue']))#line:359
            except Exception as O0000O0000O00O00O :#line:360
                O00O00OOOO0000OOO .log .error (f'(未知物品):{O0O00OOOOOOOO000O}')#line:361
            await asyncio .sleep (0.3 )#line:362
        O00O00OOOO0000OOO .log .info (f"抽奖结束: 💵现金:{'{:.2f}'.format(sum([float(O00OO0O00O0OOO0OO) for O00OO0O00O0OOO0OO in O00O00OOOO0000OOO.cash]))}元, 🧧红包:{'{:.2f}'.format(sum([float(OOO0O00O00O00O0OO) for OOO0O00O00O00O0OO in O00O00OOOO0000OOO.redpacket]))}元")#line:364
        O00O00OOOO0000OOO .log .info (f"****************开始提现****************")#line:365
        OO00O0OOO00OO000O =0 #line:366
        while True :#line:367
            OO00O0OOO00OO000O =OO00O0OOO00OO000O +1 #line:368
            O00O000O000OO0O00 =await O00O00OOOO0000OOO .superRedBagList (O00OOO0O000OOO00O ,O0O00O0OO0000000O ,OO00O0OOO00OO000O )#line:369
            await asyncio .sleep (1 )#line:370
            if not O00O000O000OO0O00 :#line:371
                break #line:372
        OOO0OOOO0000OOO00 =('提现结束: ')+(f"💵现金:{'{:.2f}'.format(sum([float(O00O00O000O000OO0) for O00O00O000O000OO0 in O00O00OOOO0000OOO.successful]))}元/")+(f"🧧兑换红包:{'{:.2f}'.format(sum([float(O0OOOO000O0O00000) for O0OOOO000O0O00000 in O00O00OOOO0000OOO.cash_redpacket]))}元/共计红包:{'{:.2f}'.format(sum([float(O0OOOOO0OOO0OO00O) for O0OOOOO0OOO0OO00O in O00O00OOOO0000OOO.redpacket + O00O00OOOO0000OOO.cash_redpacket]))}")#line:378
        if not O00O00OOOO0000OOO .successful and not O00O00OOOO0000OOO .cash_redpacket :#line:379
            OOO0OOOO0000OOO00 ='提现结束: 一毛都没有哦！'#line:380
        O00O00OOOO0000OOO .log .info (OOO0OOOO0000OOO00 )#line:381
    async def add_LinkId (OO0000OO0OO0OO0O0 ):#line:383
        async def OOOO00O0000O00O0O ():#line:384
            if OO0000OO0OO0OO0O0 .verify_result !=True :#line:385
                await OO0000OO0OO0OO0O0 .verify ()#line:386
            if OO0000OO0OO0OO0O0 .verify_result !=True :#line:387
                OO0000OO0OO0OO0O0 .log .error ("授权未通过 退出")#line:388
                sys .exit ()#line:389
            O0OOOO0O00000OOOO ='https://api.ixu.cc/status/inviter.json'#line:390
            async with aiohttp .ClientSession ()as O0000O0OOOOO00O00 :#line:391
                async with O0000O0OOOOO00O00 .get (O0OOOO0O00000OOOO ,timeout =5 )as O0OO00OO0OOO000OO :#line:392
                    if O0OO00OO0OOO000OO .status ==200 :#line:393
                        OO00O00O00OO00000 =await O0OO00OO0OOO000OO .json ()#line:394
                        if OO00O00O00OO00000 ['stats']!='True':#line:395
                            OO0000OO0OO0OO0O0 .log .error (f"{OO00O00O00OO00000['err_text']}")#line:396
                            sys .exit ()#line:397
                        OO0000OO0OO0OO0O0 .inviter_help =OO00O00O00OO00000 ['inviter']#line:398
                        if len (OO00O00O00OO00000 ['text'])>0 :#line:399
                            OO0000OO0OO0OO0O0 .log .debug (f'那女孩对你说:{OO00O00O00OO00000["text"]}')#line:400
                        if OO0000OO0OO0OO0O0 .scode =='ALL'or OO0000OO0OO0OO0O0 .scode =='all':#line:401
                            for O0O0O0000OO00OO00 in OO00O00O00OO00000 ['linkId']:#line:402
                                OO0000OO0OO0OO0O0 .linkId .append (O0O0O0000OO00OO00 )#line:403
                                OO0000OO0OO0OO0O0 .log .info (f'云端获取到linkId:{O0O0O0000OO00OO00}')#line:404
                            return True #line:405
                        else :#line:406
                            OO0000OO0OO0OO0O0 .linkId .append (OO00O00O00OO00000 ['linkId'][int (OO0000OO0OO0OO0O0 .scode )-1 ])#line:407
                            OO0000OO0OO0OO0O0 .log .info (f'云端获取到linkId:{OO00O00O00OO00000["linkId"][int(OO0000OO0OO0OO0O0.scode) - 1]}')#line:408
                            return True #line:409
                    else :#line:410
                        OO0000OO0OO0OO0O0 .log .error ('未获取到linkId 重试')#line:411
        return await OO0000OO0OO0OO0O0 .retry_with_backoff (OOOO00O0000O00O0O ,3 ,'linkId')#line:413
    async def task_start (OOO00OOO000O00OOO ):#line:415
        if OOO00OOO000O00OOO .verify_result !=True :#line:416
            await OOO00OOO000O00OOO .verify ()#line:417
        if OOO00OOO000O00OOO .verify_result !=True :#line:418
            OOO00OOO000O00OOO .log .error ("授权未通过 退出")#line:419
            sys .exit ()#line:420
        await OOO00OOO000O00OOO .add_LinkId ()#line:421
        O0OO0OO000000OO0O =OOO00OOO000O00OOO .cookie #line:424
        if OOO00OOO000O00OOO .txj_status :#line:425
            try :#line:426
                O000O0OOO00O0OOO0 =await OOO00OOO000O00OOO .Get_H5st ('inviteFissionHome',O0OO0OO000000OO0O ,{'linkId':OOO00OOO000O00OOO .linkId [0 ],"inviter":"",},'af89e')#line:428
                if not O000O0OOO00O0OOO0 ['success']and O000O0OOO00O0OOO0 ['errMsg']=='未登录':#line:430
                    OOO00OOO000O00OOO .log .error (f"{O000O0OOO00O0OOO0['errMsg']}")#line:431
                    return #line:432
                OOOO00O0O00OO0000 =O000O0OOO00O0OOO0 ['data']#line:433
                if OOOO00O0O00OO0000 ['cashVo']!=None :#line:434
                    O0O0O00O0O0O00000 =OOOO00O0O00OO0000 ['cashVo']#line:435
                    OOO00OOO000O00OOO .log .info (f"Name:{O0O0O00O0O0O00000['userInfo']['nickName']} 已助理:{OOOO00O0O00OO0000['prizeNum']} 提现:{O0O0O00O0O0O00000['totalAmount']}元 当前:{O0O0O00O0O0O00000['amount']}元 进度{O0O0O00O0O0O00000['rate']}% 剩余时间:{OOO00OOO000O00OOO.convert_ms_to_hours_minutes(OOOO00O0O00OO0000['countDownTime'])}")#line:437
                    if int (O0O0O00O0O0O00000 ['rate'])==100 :#line:438
                        OOO00OOO000O00OOO .log .info (f"本轮您已提现{O0O0O00O0O0O00000['totalAmount']}元了 等{OOO00OOO000O00OOO.convert_ms_to_hours_minutes(OOOO00O0O00OO0000['countDownTime'])}后在来吧")#line:440
                        await OOO00OOO000O00OOO .superRedBagList (O0OO0OO000000OO0O ,OOO00OOO000O00OOO .linkId [0 ],1 )#line:441
                        return #line:442
                else :#line:443
                    OOO00OOO000O00OOO .log .error ('哦和 黑号了哦')#line:444
                while True :#line:446
                    O000O00OO00OO00OO =await OOO00OOO000O00OOO .inviteFissionReceive (O0OO0OO000000OO0O ,OOO00OOO000O00OOO .linkId [0 ])#line:447
                    if not O000O00OO00OO00OO :#line:448
                        break #line:449
                    time .sleep (0.3 )#line:450
            except Exception as O0000OO00OOOO00O0 :#line:451
                OOO00OOO000O00OOO .log .error ('黑号')#line:452
        else :#line:453
            for O0O0OOO00O00OOO0O in OOO00OOO000O00OOO .linkId :#line:454
                OOO00OOO000O00OOO .log .info (f'开始执行 LinkId:{O0O0OOO00O00OOO0O}')#line:455
                await OOO00OOO000O00OOO .Fission_Draw (O0OO0OO000000OO0O ,O0O0OOO00O00OOO0O )#line:456
if __name__ =='__main__':#line:459
    pdd =TEN_JD_PDD_DRAW ()#line:460
    loop =asyncio .get_event_loop ()#line:461
    loop .run_until_complete (pdd .task_start ())#line:462
    loop .close ()#line:463
