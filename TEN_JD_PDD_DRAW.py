"""
File: TEN_JD_PDD.py(邀好友赢现金-抽奖)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-抽奖');
"""
""#line:9
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
    def __init__ (OO0O0OOO0OO0OOO00 ):#line:28
        OO0O0OOO0OO0OOO00 .log =setup_logger ()#line:29
        OO0O0OOO0OO0OOO00 .start =time .time ()#line:30
        OO0O0OOO0OO0OOO00 .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:31
        OO0O0OOO0OO0OOO00 .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 2 #line:32
        OO0O0OOO0OO0OOO00 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:33
        OO0O0OOO0OO0OOO00 .numer_og =os .environ .get ("draw_numer")if os .environ .get ("draw_numer")else 3 #line:34
        OO0O0OOO0OO0OOO00 .activityUrl ="https://pro.m.jd.com"#line:35
        OO0O0OOO0OO0OOO00 .cookie =os .environ .get ("draw_cookie")if os .environ .get ("draw_cookie")else ck [0 ]#line:36
        OO0O0OOO0OO0OOO00 .linkId =[]#line:37
        OO0O0OOO0OO0OOO00 .amount =0 #line:38
        OO0O0OOO0OO0OOO00 .leftAmount =0 #line:39
        OO0O0OOO0OO0OOO00 .verify_result =False #line:40
        OO0O0OOO0OO0OOO00 .txj_status =os .environ .get ("txj_status")if os .environ .get ("txj_status")else (OO0O0OOO0OO0OOO00 .scode ==3 )#line:41
        OO0O0OOO0OO0OOO00 .inviter =''#line:42
        OO0O0OOO0OO0OOO00 .power_success =[]#line:43
        OO0O0OOO0OO0OOO00 .power_failure =[]#line:44
        OO0O0OOO0OO0OOO00 .redpacket =[]#line:45
        OO0O0OOO0OO0OOO00 .cash =[]#line:46
        OO0O0OOO0OO0OOO00 .cash_redpacket =[]#line:47
        OO0O0OOO0OO0OOO00 .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:54
        OO0O0OOO0OO0OOO00 .rewardType ={1 :{'msg':'优惠券🎫'},2 :{'msg':'红包🧧'},6 :{'msg':'惊喜小礼包🎫'},}#line:59
        OO0O0OOO0OO0OOO00 .successful =[]#line:60
    async def retry_with_backoff (O000OOOO0OOOO0OOO ,O00O0OO0O0OO00000 ,O0OO0OOO0000000O0 ,OO0000OO00OO0O00O ,backoff_seconds =0 ):#line:62
        for O0OOOOOO000000O00 in range (O0OO0OOO0000000O0 ):#line:63
            OO0OO000O00O0000O =False #line:64
            try :#line:65
                return await O00O0OO0O0OO00000 ()#line:66
            except asyncio .TimeoutError :#line:67
                if not OO0OO000O00O0000O :#line:68
                    O000OOOO0OOOO0OOO .log .debug (f'第{O0OOOOOO000000O00 + 1}次重试 {OO0000OO00OO0O00O} 请求超时')#line:69
                    OO0OO000O00O0000O =True #line:70
                await asyncio .sleep (backoff_seconds )#line:71
            except Exception as O00OO0O000OO0OO0O :#line:72
                if not OO0OO000O00O0000O :#line:73
                    O000OOOO0OOOO0OOO .log .debug (f'第{O0OOOOOO000000O00 + 1}次重试 {OO0000OO00OO0O00O} 出错：{O00OO0O000OO0OO0O}')#line:74
                    OO0OO000O00O0000O =True #line:75
                await asyncio .sleep (backoff_seconds )#line:76
            if OO0OO000O00O0000O and O0OOOOOO000000O00 ==O0OO0OOO0000000O0 -1 :#line:78
                O000OOOO0OOOO0OOO .log .error (f'{OO0000OO00OO0O00O} 重试{O0OO0OOO0000000O0}次后仍然发生异常')#line:79
                return False ,False ,False #line:80
    async def GET_POST (O0OO0O0000O0OO00O ,OO000O0O0O000O0O0 ,num =1 ):#line:82
        async def O00OO00O0O00OO00O ():#line:83
            async with aiohttp .ClientSession ()as O000O0000OOOOO0OO :#line:84
                if OO000O0O0O000O0O0 ['method']=='get':#line:85
                    async with O000O0000OOOOO0OO .get (**OO000O0O0O000O0O0 ['kwargs'])as OOOO000OOOOOOO000 :#line:86
                        O0OOO0OO0OO0O0O0O =OOOO000OOOOOOO000 .status #line:87
                        OOO0O0O000OO0O0OO =await OOOO000OOOOOOO000 .text ()#line:88
                else :#line:89
                    async with O000O0000OOOOO0OO .post (**OO000O0O0O000O0O0 ['kwargs'])as OOOO000OOOOOOO000 :#line:90
                        O0OOO0OO0OO0O0O0O =OOOO000OOOOOOO000 .status #line:91
                        OOO0O0O000OO0O0OO =await OOOO000OOOOOOO000 .text ()#line:92
                if O0OOO0OO0OO0O0O0O !=200 :#line:93
                    await asyncio .sleep (3 )#line:94
                    if num >3 :#line:95
                        O0OO0O0000O0OO00O .log .warning (f'{O0OOO0OO0OO0O0O0O}:状态超出3次')#line:96
                        return False ,False ,False #line:97
                    O0OO0O0000O0OO00O .log .debug (f'{O0OOO0OO0OO0O0O0O}:去重试 第{num}次')#line:98
                    return await O0OO0O0000O0OO00O .GET_POST (OO000O0O0O000O0O0 ,num +1 )#line:99
                try :#line:100
                    OO0000O0O0O00OOO0 =json .loads (OOO0O0O000OO0O0OO )#line:101
                except :#line:102
                    OO0000O0O0O00OOO0 =OOO0O0O000OO0O0OO #line:103
                return O0OOO0OO0OO0O0O0O ,OOO0O0O000OO0O0OO ,OO0000O0O0O00OOO0 #line:104
        return await O0OO0O0000O0OO00O .retry_with_backoff (O00OO00O0O00OO00O ,3 ,f'GET_POST')#line:106
    async def verify (OOOO00000O000O00O ):#line:108
        async def OOO0O0OOOO000000O ():#line:109
            O0OO0OO0O000OOO00 ='https://api.ixu.cc/verify'#line:110
            async with aiohttp .ClientSession ()as OO0000O000OO0O000 :#line:111
                async with OO0000O000OO0O000 .get (O0OO0OO0O000OOO00 ,data ={'TOKEN':OOOO00000O000O00O .token },timeout =3 )as O00000O00000OOOOO :#line:112
                    O0000OOOO00000OO0 =await O00000O00000OOOOO .json ()#line:113
                    if O00000O00000OOOOO .status ==200 :#line:114
                        OOOO00000O000O00O .verify_result =True #line:115
                        OOOO00000O000O00O .log .info (f'认证通过 UserId：{O0000OOOO00000OO0["user_id"]}')#line:116
                        return O0000OOOO00000OO0 #line:117
                    else :#line:118
                        OOOO00000O000O00O .log .error (f"授权未通过:{O0000OOOO00000OO0['error']}")#line:119
                        sys .exit ()#line:120
        return await OOOO00000O000O00O .retry_with_backoff (OOO0O0OOOO000000O ,3 ,'verify')#line:122
    async def Get_H5st (O0000OO0O0OOO0OO0 ,O0O0O0O0OO0OOOOO0 ,OO0OO000OOOOOOOOO ,O000000OO0000O0O0 ,OO0O00OO0O0OO0OOO ):#line:124
        if O0000OO0O0OOO0OO0 .verify_result !=True :#line:125
            await O0000OO0O0OOO0OO0 .verify ()#line:126
        if O0000OO0O0OOO0OO0 .verify_result !=True :#line:127
            O0000OO0O0OOO0OO0 .log .error ("授权未通过 退出")#line:128
            sys .exit ()#line:129
        O0O0O0O000OOO0000 =generate_random_user_agent ()#line:130
        O0OO0O0OOOO00O0OO ={'method':'','kwargs':{'url':'https://api.ouklc.com/api/h5st','params':{'functionId':O0O0O0O0OO0OOOOO0 ,'body':json .dumps (O000000OO0000O0O0 ),'ua':O0O0O0O000OOO0000 ,'pin':O0000OO0O0OOO0OO0 .pt_pin (OO0OO000OOOOOOOOO ),'appId':OO0O00OO0O0OO0OOO }}}#line:143
        OO0OO0OO000O0OOOO ,OO0OOOOO0O0OO0OO0 ,OO0O0OOO0OOOOOO00 =await O0000OO0O0OOO0OO0 .GET_POST (O0OO0O0OOOO00O0OO )#line:144
        if OO0OO0OO000O0OOOO !=200 :#line:146
            return await O0000OO0O0OOO0OO0 .Get_H5st (O0O0O0O0OO0OOOOO0 ,OO0OO000OOOOOOOOO ,O000000OO0000O0O0 ,OO0O00OO0O0OO0OOO )#line:147
        O0OO0O0OOOO00O0OO ={'method':'post','kwargs':{'url':f'https://api.m.jd.com','headers':{"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OO0OO000OOOOOOOOO ,"User-Agent":O0O0O0O000OOO0000 },'data':OO0O0OOO0OOOOOO00 ["body"]}}#line:167
        OO0OO0OO000O0OOOO ,OO0OOOOO0O0OO0OO0 ,OO0O0OOO0OOOOOO00 =await O0000OO0O0OOO0OO0 .GET_POST (O0OO0O0OOOO00O0OO )#line:168
        return OO0O0OOO0OOOOOO00 #line:169
    def pt_pin (O00O000O00OO0O0OO ,O0O0O000000O0000O ):#line:171
        try :#line:172
            OOO000OOOO0O00O00 =re .compile (r'pt_pin=(.*?);').findall (O0O0O000000O0000O )[0 ]#line:173
            OOO000OOOO0O00O00 =unquote_plus (OOO000OOOO0O00O00 )#line:174
        except IndexError :#line:175
            OOO000OOOO0O00O00 =re .compile (r'pin=(.*?);').findall (O0O0O000000O0000O )[0 ]#line:176
            OOO000OOOO0O00O00 =unquote_plus (OOO000OOOO0O00O00 )#line:177
        return OOO000OOOO0O00O00 #line:178
    def convert_ms_to_hours_minutes (OO0O0OOO00000O0OO ,O000OOOOOOOO000OO ):#line:180
        O0O000O0O0OO0O000 =O000OOOOOOOO000OO //1000 #line:181
        O00O0OO0OOOO00OO0 ,O0O000O0O0OO0O000 =divmod (O0O000O0O0OO0O000 ,60 )#line:182
        OO0OOO0000O00O0OO ,O00O0OO0OOOO00OO0 =divmod (O00O0OO0OOOO00OO0 ,60 )#line:183
        return f'{OO0OOO0000O00O0OO}小时{O00O0OO0OOOO00OO0}分'#line:184
    async def inviteFissionReceive (O00OOOO0O0OOO00O0 ,O00OOO00O0OO000OO ,OO0OO0OOOO0OO00OO ,page =1 ):#line:186
        if O00OOOO0O0OOO00O0 .verify_result !=True :#line:187
            await O00OOOO0O0OOO00O0 .verify ()#line:188
        if O00OOOO0O0OOO00O0 .verify_result !=True :#line:189
            O00OOOO0O0OOO00O0 .log .error ("授权未通过 退出")#line:190
            sys .exit ()#line:191
        O0O00OOOOOOO0OOO0 =generate_random_user_agent ()#line:192
        O0OOOOOOOO00O0O00 ={'linkId':OO0OO0OOOO0OO00OO ,}#line:195
        O00OO000OOOOOOO0O =await O00OOOO0O0OOO00O0 .Get_H5st ('inviteFissionReceive',O00OOO00O0OO000OO ,O0OOOOOOOO00O0O00 ,'b8469')#line:196
        if O00OO000OOOOOOO0O ['success']==False and O00OO000OOOOOOO0O ['errMsg']=='活动太火爆，请稍候重试':#line:197
            OOO0000OO0OOOO0OO =f'还差{O00OOOO0O0OOO00O0.leftAmount / O00OOOO0O0OOO00O0.amount}次'if O00OOOO0O0OOO00O0 .amount !=0 else '先去助力一次才能计算需要人数'#line:198
            O00OOOO0O0OOO00O0 .log .debug (f'没助理了 快去助理吧 {OOO0000OO0OOOO0OO}')#line:199
            await O00OOOO0O0OOO00O0 .superRedBagList (O00OOO00O0OO000OO ,OO0OO0OOOO0OO00OO ,page )#line:200
            return False #line:201
        if O00OO000OOOOOOO0O ['success']and O00OO000OOOOOOO0O ['code']==0 :#line:207
            O00OOOO0O0OOO00O0 .amount =float (O00OO000OOOOOOO0O ["data"]["receiveList"][0 ]["amount"])#line:208
            O00OOOO0O0OOO00O0 .leftAmount =float (O00OO000OOOOOOO0O ["data"]["leftAmount"])#line:209
            O00OOOO0O0OOO00O0 .log .info (f'领取中:{O00OO000OOOOOOO0O["data"]["totalAmount"]} 当前:{O00OO000OOOOOOO0O["data"]["amount"]} 获得:{O00OO000OOOOOOO0O["data"]["receiveList"][0]["amount"]} 还差:{O00OO000OOOOOOO0O["data"]["leftAmount"]}元/{O00OOOO0O0OOO00O0.leftAmount / O00OOOO0O0OOO00O0.amount}次 当前进度:{O00OO000OOOOOOO0O["data"]["rate"]}%')#line:211
            if int (O00OO000OOOOOOO0O ["data"]["rate"])==100 :#line:212
                O00OOOO0O0OOO00O0 .log .info (f'领取中:{O00OO000OOOOOOO0O["data"]["totalAmount"]} 进度:{O00OO000OOOOOOO0O["data"]["rate"]}% 退出!')#line:213
                await O00OOOO0O0OOO00O0 .superRedBagList (O00OOO00O0OO000OO ,OO0OO0OOOO0OO00OO ,page )#line:214
                return False #line:215
        return True #line:216
    async def apCashWithDraw (O00O00000OOO0000O ,OO000O000OO00OOOO ,OOOOOOOOOO0OO00O0 ,OO00O0OOO00OO00OO ,OO0O000O0OO0O00O0 ,O0OOO00O0O0OOO000 ,OO0OO0OO00OO0OOOO ):#line:218
        if O00O00000OOO0000O .verify_result !=True :#line:219
            await O00O00000OOO0000O .verify ()#line:220
        if O00O00000OOO0000O .verify_result !=True :#line:221
            O00O00000OOO0000O .log .error ("授权未通过 退出")#line:222
            sys .exit ()#line:223
        OOO0OO00OO0O000O0 =generate_random_user_agent ()#line:224
        O0OOOO00O00OO00O0 =await O00O00000OOO0000O .Get_H5st ("apCashWithDraw",OOOOOOOOOO0OO00O0 ,{"linkId":OO000O000OO00OOOO ,"businessSource":"NONE","base":{"id":OO00O0OOO00OO00OO ,"business":"fission","poolBaseId":OO0O000O0OO0O00O0 ,"prizeGroupId":O0OOO00O0O0OOO000 ,"prizeBaseId":OO0OO0OO00OO0OOOO ,"prizeType":4 }},'8c6ae')#line:240
        return O0OOOO00O00OO00O0 #line:241
    async def inviteFissionBeforeHome (OOO0O000O00O00O00 ,num =1 ):#line:243
        O0O0000OO00OO0O00 =False #line:244
        for O00O0O000OOOO0OO0 in ck :#line:245
            if len (OOO0O000O00O00O00 .power_success )>=num :#line:246
                return await OOO0O000O00O00O00 .inviteFissionReceive (OOO0O000O00O00O00 .cookie ,OOO0O000O00O00O00 .linkId )#line:247
            OO00000OO0OO0OO00 =await OOO0O000O00O00O00 .Get_H5st ("inviteFissionBeforeHome",O00O0O000OOOO0OO0 ,{'linkId':OOO0O000O00O00O00 .linkId ,"isJdApp":True ,'inviter':OOO0O000O00O00O00 .inviter },'02f8d',)#line:250
            if int (OO00000OO0OO0OO00 ['code'])==0 :#line:251
                for OOOOOOOOOOOOOOO00 ,O000OO00OOOOOO000 in OOO0O000O00O00O00 .helpResult :#line:252
                    if OO00000OO0OO0OO00 ['data']['helpResult']==int (OOOOOOOOOOOOOOO00 ):#line:253
                        O0O0000OO00OO0O00 =True #line:254
                        OOO0O000O00O00O00 .log .info (f"Id:{OOO0O000O00O00O00.linkId[:4] + '****' + OOO0O000O00O00O00.linkId[-4:]}|助理:{OO00000OO0OO0OO00['data']['nickName']}|{OO00000OO0OO0OO00['data']['helpResult']}|{OOO0O000O00O00O00.pt_pin(O00O0O000OOOO0OO0)}|{O000OO00OOOOOO000}")#line:256
                        if OO00000OO0OO0OO00 ['data']['helpResult']==1 :#line:257
                            OOO0O000O00O00O00 .power_success .append (O00O0O000OOOO0OO0 )#line:258
                        else :#line:259
                            OOO0O000O00O00O00 .power_failure .append (O00O0O000OOOO0OO0 )#line:260
                    if not O0O0000OO00OO0O00 :#line:261
                        O000OO00OOOOOO000 ='❌未知状态 (可能是活动未开启！！！)'#line:262
                        OOO0O000O00O00O00 .power_failure .append (O00O0O000OOOO0OO0 )#line:263
                        OOO0O000O00O00O00 .log .info (f"Id:{OOO0O000O00O00O00.linkId[:4] + '****' + OOO0O000O00O00O00.linkId[-4:]}|助理:{OO00000OO0OO0OO00['data']['nickName']}|{OO00000OO0OO0OO00['data']['helpResult']}|{OOO0O000O00O00O00.pt_pin(O00O0O000OOOO0OO0)}|{O000OO00OOOOOO000}")#line:265
            else :#line:266
                OOO0O000O00O00O00 .log .info (f"{OOO0O000O00O00O00.pt_pin(O00O0O000OOOO0OO0)}{OO00000OO0OO0OO00['code']} 结果:💔{OO00000OO0OO0OO00['errMsg']}")#line:267
    async def superRedBagList (O00O00OO0OOO00O0O ,OO0O0O0OOOO00O00O ,O00O00OO0OOOOOO0O ,OOO0000O00O0OO00O ):#line:269
        if O00O00OO0OOO00O0O .verify_result !=True :#line:270
            await O00O00OO0OOO00O0O .verify ()#line:271
        if O00O00OO0OOO00O0O .verify_result !=True :#line:272
            O00O00OO0OOO00O0O .log .error ("授权未通过 退出")#line:273
            sys .exit ()#line:274
        O0O0OO0OO0O00000O =await O00O00OO0OOO00O0O .Get_H5st ('superRedBagList',OO0O0O0OOOO00O00O ,{"pageNum":OOO0000O00O0OO00O ,"pageSize":200 ,"linkId":O00O00OO0OOOOOO0O ,"business":"fission"},'f2b1d')#line:277
        O00O00OO0OOO00O0O .log .info (f"开始提取{OOO0000O00O0OO00O}页, 共{len(O0O0OO0OO0O00000O['data']['items'])}条记录")#line:278
        if len (O0O0OO0OO0O00000O ['data']['items'])==0 :#line:279
            return False #line:280
        for OOO00OO00O00O0O00 in O0O0OO0OO0O00000O ['data']['items']:#line:281
            OO0O00O0O00O0O0O0 ,OO0OO0000OOOO0OO0 ,O0OO0O0O000OOO000 ,OOO000OOOO000O000 ,O0O00OO000O00O0O0 ,O0OO000OOOOO0OO0O ,O0OO0OOO0O0O0O0O0 ,O00OO00OO00OO00O0 ,O0O0O00000O0O0000 =(OOO00OO00O00O0O00 ['id'],OOO00OO00O00O0O00 ['amount'],OOO00OO00O00O0O00 ['prizeType'],OOO00OO00O00O0O00 ['state'],OOO00OO00O00O0O00 ['prizeConfigName'],OOO00OO00O00O0O00 ['prizeGroupId'],OOO00OO00O00O0O00 ['poolBaseId'],OOO00OO00O00O0O00 ['prizeBaseId'],OOO00OO00O00O0O00 ['startTime'])#line:286
            if float (OO0OO0000OOOO0OO0 )>1.0 :#line:287
                O00O00OO0OOO00O0O .log .info (f"{O0O0O00000O0O0000} {OO0OO0000OOOO0OO0}元 {'❌未提现' if O0OO0O0O000OOO000 == 4 and OOO000OOOO000O000 != 3 else '✅已提现'}")#line:288
            if O0OO0O0O000OOO000 ==4 and OOO000OOOO000O000 !=3 :#line:289
                O0O0OO0OO0O00000O =await O00O00OO0OOO00O0O .apCashWithDraw (O00O00OO0OOOOOO0O ,OO0O0O0OOOO00O00O ,OO0O00O0O00O0O0O0 ,O0OO0OOO0O0O0O0O0 ,O0OO000OOOOO0OO0O ,O00OO00OO00OO00O0 )#line:290
                if int (O0O0OO0OO0O00000O ['data']['status'])==310 :#line:292
                    O00O00OO0OOO00O0O .log .info (f"✅{OO0OO0000OOOO0OO0}现金💵 提现成功")#line:293
                    O00O00OO0OOO00O0O .successful .append (OO0OO0000OOOO0OO0 )#line:294
                elif int (O0O0OO0OO0O00000O ['data']['status'])==50056 or int (O0O0OO0OO0O00000O ['data']['status'])==50001 :#line:295
                    O00O00OO0OOO00O0O .log .warning (f"❌{OO0OO0000OOOO0OO0}现金💵 重新发起 提现失败:{O0O0OO0OO0O00000O['data']['message']}")#line:296
                    time .sleep (3 )#line:297
                    await O00O00OO0OOO00O0O .apCashWithDraw (O00O00OO0OOOOOO0O ,OO0O0O0OOOO00O00O ,OO0O00O0O00O0O0O0 ,O0OO0OOO0O0O0O0O0 ,O0OO000OOOOO0OO0O ,O00OO00OO00OO00O0 )#line:298
                    if int (O0O0OO0OO0O00000O ['data']['status'])==310 :#line:299
                        O00O00OO0OOO00O0O .log .info (f"✅{OO0OO0000OOOO0OO0}现金💵 提现成功")#line:300
                        O00O00OO0OOO00O0O .successful .append (OO0OO0000OOOO0OO0 )#line:301
                    else :#line:302
                        O00O00OO0OOO00O0O .log .error (f"❌{OO0OO0000OOOO0OO0}现金💵 提现失败:{O0O0OO0OO0O00000O['data']['message']}")#line:303
                elif '金额超过自然月上限'in O0O0OO0OO0O00000O ['data']['message']:#line:304
                    O00O00OO0OOO00O0O .log .info (f"{OO0OO0000OOOO0OO0}现金:{O0O0OO0OO0O00000O['data']['message']}:去兑换红包")#line:305
                    await O00O00OO0OOO00O0O .apRecompenseDrawPrize (O00O00OO0OOOOOO0O ,OO0O0O0OOOO00O00O ,OO0O00O0O00O0O0O0 ,O0OO0OOO0O0O0O0O0 ,O0OO000OOOOO0OO0O ,O00OO00OO00OO00O0 ,OO0OO0000OOOO0OO0 )#line:306
                else :#line:307
                    O00O00OO0OOO00O0O .log .error (f"{OO0OO0000OOOO0OO0}现金 ❌提现错误:{O0O0OO0OO0O00000O['data']['status']} {O0O0OO0OO0O00000O['data']['message']}")#line:308
            else :#line:310
                continue #line:311
            await asyncio .sleep (0.5 )#line:312
    async def apRecompenseDrawPrize (O0O00OOO000OOO0O0 ,OO000OOO0O00O00OO ,O0OO0OO0OOOOOOO00 ,O0O0O0OOOOOO00OOO ,O00OO00O0O00O000O ,OOOOO000000000O0O ,O00000O000OOO0O00 ,O0O0O0000OO0OOO0O ):#line:315
        O00OOOO00O0OO000O =await O0O00OOO000OOO0O0 .Get_H5st ('apRecompenseDrawPrize',O0OO0OO0OOOOOOO00 ,{"linkId":OO000OOO0O00O00OO ,"businessSource":"fission","drawRecordId":O0O0O0OOOOOO00OOO ,"business":"fission","poolId":O00OO00O0O00O000O ,"prizeGroupId":OOOOO000000000O0O ,"prizeId":O00000O000OOO0O00 ,},'8c6ae')#line:325
        if O00OOOO00O0OO000O ['success']and int (O00OOOO00O0OO000O ['data']['resCode'])==0 :#line:326
            O0O00OOO000OOO0O0 .log .info (f"{O0O0O0000OO0OOO0O}现金:🧧红包兑换成功")#line:327
            O0O00OOO000OOO0O0 .cash_redpacket .append (O0O0O0000OO0OOO0O )#line:328
        else :#line:329
            O0O00OOO000OOO0O0 .log .info (f"{O0O0O0000OO0OOO0O}现金:🧧红包兑换失败 {O00OOOO00O0OO000O}")#line:330
    async def Fission_Draw (O0O0O000O0OO00O0O ,OO0O0OO0O0OO000OO ,O00OO0000OOOOO00O ):#line:332
        O0O0O000O0OO00O0O .log .info (f"****************开始抽奖****************")#line:333
        while True :#line:334
            OOO0O00OOOO0000O0 =await O0O0O000O0OO00O0O .Get_H5st ('inviteFissionDrawPrize',OO0O0OO0O0OO000OO ,{"linkId":O00OO0000OOOOO00O },'c02c6')#line:337
            if not OOO0O00OOOO0000O0 ['success']:#line:339
                if "抽奖次数已用完"in OOO0O00OOOO0000O0 ['errMsg']:#line:340
                    O0O0O000O0OO00O0O .log .debug (f"⚠️抽奖次数已用完")#line:341
                    break #line:342
                elif "本场活动已结束"in OOO0O00OOOO0000O0 ['errMsg']:#line:343
                    O0O0O000O0OO00O0O .log .debug (f"⏰本场活动已结束了,快去重新开始吧")#line:344
                    sys .exit ()#line:345
            try :#line:346
                if not OOO0O00OOOO0000O0 ['success']:#line:347
                    O0O0O000O0OO00O0O .log .warning (f'{OOO0O00OOOO0000O0["errMsg"]}')#line:348
                    continue #line:349
                if int (OOO0O00OOOO0000O0 ['data']['rewardType'])in O0O0O000O0OO00O0O .rewardType :#line:352
                    O0O0O000O0OO00O0O .log .info (f"获得:{OOO0O00OOOO0000O0['data']['prizeValue']}元{O0O0O000O0OO00O0O.rewardType[int(OOO0O00OOOO0000O0['data']['rewardType'])]['msg']}")#line:354
                    if int (OOO0O00OOOO0000O0 ['data']['rewardType'])==2 :#line:355
                        O0O0O000O0OO00O0O .redpacket .append (float (OOO0O00OOOO0000O0 ['data']['prizeValue']))#line:356
                else :#line:357
                    O0O0O000O0OO00O0O .log .info (f"获得:{OOO0O00OOOO0000O0['data']['prizeValue']}元现金💵")#line:358
                    O0O0O000O0OO00O0O .cash .append (float (OOO0O00OOOO0000O0 ['data']['prizeValue']))#line:359
            except Exception as OOO00O0000O0OOOO0 :#line:360
                O0O0O000O0OO00O0O .log .error (f'(未知物品):{OOO0O00OOOO0000O0}')#line:361
            await asyncio .sleep (0.3 )#line:362
        O0O0O000O0OO00O0O .log .info (f"抽奖结束: 💵现金:{'{:.2f}'.format(sum([float(O00O0O00OO00000OO) for O00O0O00OO00000OO in O0O0O000O0OO00O0O.cash]))}元, 🧧红包:{'{:.2f}'.format(sum([float(OO0OOO00OO0OO000O) for OO0OOO00OO0OO000O in O0O0O000O0OO00O0O.redpacket]))}元")#line:364
        O0O0O000O0OO00O0O .log .info (f"****************开始提现****************")#line:365
        O0O00OO00O0O0OO0O =0 #line:366
        while True :#line:367
            O0O00OO00O0O0OO0O =O0O00OO00O0O0OO0O +1 #line:368
            O0OOOO00O00O00OOO =await O0O0O000O0OO00O0O .superRedBagList (OO0O0OO0O0OO000OO ,O00OO0000OOOOO00O ,O0O00OO00O0O0OO0O )#line:369
            await asyncio .sleep (1 )#line:370
            if not O0OOOO00O00O00OOO :#line:371
                break #line:372
        OOO0O00OOO0O0OO00 =('提现结束: ')+(f"💵现金:{'{:.2f}'.format(sum([float(OOO00O00OO0O0000O) for OOO00O00OO0O0000O in O0O0O000O0OO00O0O.successful]))}元/")+(f"🧧兑换红包:{'{:.2f}'.format(sum([float(OO0OOOO00OOOOO00O) for OO0OOOO00OOOOO00O in O0O0O000O0OO00O0O.cash_redpacket]))}元/共计红包:{'{:.2f}'.format(sum([float(OOOOOO00000OO0000) for OOOOOO00000OO0000 in O0O0O000O0OO00O0O.redpacket + O0O0O000O0OO00O0O.cash_redpacket]))}")#line:378
        if not O0O0O000O0OO00O0O .successful and not O0O0O000O0OO00O0O .cash_redpacket :#line:379
            OOO0O00OOO0O0OO00 ='提现结束: 一毛都没有哦！'#line:380
        O0O0O000O0OO00O0O .log .info (OOO0O00OOO0O0OO00 )#line:381
    async def add_LinkId (O0O00O0OOOOOO0O0O ):#line:383
        async def OOOOO0O0OOOO00000 ():#line:384
            if O0O00O0OOOOOO0O0O .verify_result !=True :#line:385
                await O0O00O0OOOOOO0O0O .verify ()#line:386
            if O0O00O0OOOOOO0O0O .verify_result !=True :#line:387
                O0O00O0OOOOOO0O0O .log .error ("授权未通过 退出")#line:388
                sys .exit ()#line:389
            O000O0O0OOOO0OOO0 ='https://api.ixu.cc/status/inviter.json'#line:390
            async with aiohttp .ClientSession ()as OO0O0000OOO0OO0OO :#line:391
                async with OO0O0000OOO0OO0OO .get (O000O0O0OOOO0OOO0 ,timeout =5 )as OO0O00000O0O0O000 :#line:392
                    if OO0O00000O0O0O000 .status ==200 :#line:393
                        O0OOO000OO00O000O =await OO0O00000O0O0O000 .json ()#line:394
                        if O0OOO000OO00O000O ['stats']!='True':#line:395
                            O0O00O0OOOOOO0O0O .log .error (f"{O0OOO000OO00O000O['err_text']}")#line:396
                            sys .exit ()#line:397
                        O0O00O0OOOOOO0O0O .inviter_help =O0OOO000OO00O000O ['inviter']#line:398
                        if len (O0OOO000OO00O000O ['text'])>0 :#line:399
                            O0O00O0OOOOOO0O0O .log .debug (f'那女孩对你说:{O0OOO000OO00O000O["text"]}')#line:400
                        if O0O00O0OOOOOO0O0O .scode =='ALL'or O0O00O0OOOOOO0O0O .scode =='all':#line:401
                            for OO0O00OO00OO0OOOO in O0OOO000OO00O000O ['linkId']:#line:402
                                O0O00O0OOOOOO0O0O .linkId .append (OO0O00OO00OO0OOOO )#line:403
                                O0O00O0OOOOOO0O0O .log .info (f'云端获取到linkId:{OO0O00OO00OO0OOOO}')#line:404
                            return True #line:405
                        else :#line:406
                            O0O00O0OOOOOO0O0O .linkId .append (O0OOO000OO00O000O ['linkId'][int (O0O00O0OOOOOO0O0O .scode )-1 ])#line:407
                            O0O00O0OOOOOO0O0O .log .info (f'云端获取到linkId:{O0OOO000OO00O000O["linkId"][int(O0O00O0OOOOOO0O0O.scode) - 1]}')#line:408
                            return True #line:409
                    else :#line:410
                        O0O00O0OOOOOO0O0O .log .error ('未获取到linkId 重试')#line:411
        return await O0O00O0OOOOOO0O0O .retry_with_backoff (OOOOO0O0OOOO00000 ,3 ,'linkId')#line:413
    async def task_start (O00000OO000O0O0O0 ):#line:415
        if O00000OO000O0O0O0 .verify_result !=True :#line:416
            await O00000OO000O0O0O0 .verify ()#line:417
        if O00000OO000O0O0O0 .verify_result !=True :#line:418
            O00000OO000O0O0O0 .log .error ("授权未通过 退出")#line:419
            sys .exit ()#line:420
        await O00000OO000O0O0O0 .add_LinkId ()#line:421
        OO00O0OOO0000OOOO =O00000OO000O0O0O0 .cookie #line:424
        if O00000OO000O0O0O0 .txj_status :#line:425
            try :#line:426
                OO00O0OO000O0O000 =await O00000OO000O0O0O0 .Get_H5st ('inviteFissionHome',OO00O0OOO0000OOOO ,{'linkId':O00000OO000O0O0O0 .linkId [0 ],"inviter":"",},'eb67b'if O00000OO000O0O0O0 .linkId [0 ]in 'EcuVpjGGfccY3Ic_1ni83w'else 'af89e')#line:428
                if not OO00O0OO000O0O000 ['success']and OO00O0OO000O0O000 ['errMsg']=='未登录':#line:430
                    O00000OO000O0O0O0 .log .error (f"{OO00O0OO000O0O000['errMsg']}")#line:431
                    return #line:432
                O0OO0000O00O000O0 =OO00O0OO000O0O000 ['data']#line:433
                if O0OO0000O00O000O0 ['cashVo']!=None :#line:434
                    O0O0000O0OOOOOO00 =O0OO0000O00O000O0 ['cashVo']#line:435
                    O00000OO000O0O0O0 .log .info (f"Name:{O0O0000O0OOOOOO00['userInfo']['nickName']} 已助理:{O0OO0000O00O000O0['prizeNum']} 提现:{O0O0000O0OOOOOO00['totalAmount']}元 当前:{O0O0000O0OOOOOO00['amount']}元 进度{O0O0000O0OOOOOO00['rate']}% 剩余时间:{O00000OO000O0O0O0.convert_ms_to_hours_minutes(O0OO0000O00O000O0['countDownTime'])}")#line:437
                    if int (O0O0000O0OOOOOO00 ['rate'])==100 :#line:438
                        O00000OO000O0O0O0 .log .info (f"本轮您已提现{O0O0000O0OOOOOO00['totalAmount']}元了 等{O00000OO000O0O0O0.convert_ms_to_hours_minutes(O0OO0000O00O000O0['countDownTime'])}后在来吧")#line:440
                        await O00000OO000O0O0O0 .superRedBagList (OO00O0OOO0000OOOO ,O00000OO000O0O0O0 .linkId [0 ],1 )#line:441
                        return #line:442
                else :#line:443
                    O00000OO000O0O0O0 .log .error ('哦和 黑号了哦')#line:444
                while True :#line:446
                    OO0000O0OOOOOO0OO =await O00000OO000O0O0O0 .inviteFissionReceive (OO00O0OOO0000OOOO ,O00000OO000O0O0O0 .linkId [0 ])#line:447
                    if not OO0000O0OOOOOO0OO :#line:448
                        break #line:449
                    time .sleep (0.3 )#line:450
            except Exception as OOOO0OOOOO0OOO0O0 :#line:451
                O00000OO000O0O0O0 .log .error ('黑号')#line:452
        else :#line:453
            for OOO0000OO0O0O0O0O in O00000OO000O0O0O0 .linkId :#line:454
                O00000OO000O0O0O0 .log .info (f'开始执行 LinkId:{OOO0000OO0O0O0O0O}')#line:455
                await O00000OO000O0O0O0 .Fission_Draw (OO00O0OOO0000OOOO ,OOO0000OO0O0O0O0O )#line:456
if __name__ =='__main__':#line:459
    pdd =TEN_JD_PDD_DRAW ()#line:460
    loop =asyncio .get_event_loop ()#line:461
    loop .run_until_complete (pdd .task_start ())#line:462
    loop .close ()#line:463
