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
    def __init__ (O0O00O0OO0O000000 ):#line:28
        O0O00O0OO0O000000 .log =setup_logger ()#line:29
        O0O00O0OO0O000000 .ua =generate_random_user_agent ()#line:30
        O0O00O0OO0O000000 .page =10 #line:31
        O0O00O0OO0O000000 .start =time .time ()#line:32
        O0O00O0OO0O000000 .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:33
        O0O00O0OO0O000000 .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:34
        O0O00O0OO0O000000 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:35
        O0O00O0OO0O000000 .numer_og =os .environ .get ("draw_numer")if os .environ .get ("draw_numer")else 3 #line:36
        O0O00O0OO0O000000 .activityUrl ="https://pro.m.jd.com"#line:37
        O0O00O0OO0O000000 .cookie =os .environ .get ("draw_cookie")if os .environ .get ("draw_cookie")else ck [0 ]#line:38
        O0O00O0OO0O000000 .linkId =[]#line:39
        O0O00O0OO0O000000 .amount =0 #line:40
        O0O00O0OO0O000000 .leftAmount =0 #line:41
        O0O00O0OO0O000000 .verify_result =False #line:42
        O0O00O0OO0O000000 .txj_status =os .environ .get ("txj_status")if os .environ .get ("txj_status")else False #line:43
        O0O00O0OO0O000000 .inviter =''#line:44
        O0O00O0OO0O000000 .power_success =[]#line:45
        O0O00O0OO0O000000 .power_failure =[]#line:46
        O0O00O0OO0O000000 .redpacket =[]#line:47
        O0O00O0OO0O000000 .cash =[]#line:48
        O0O00O0OO0O000000 .cash_redpacket =[]#line:49
        O0O00O0OO0O000000 .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:56
        O0O00O0OO0O000000 .rewardType ={1 :{'msg':'优惠券🎫'},2 :{'msg':'红包🧧'},6 :{'msg':'惊喜小礼包🎫'},}#line:61
        O0O00O0OO0O000000 .successful =[]#line:62
    async def retry_with_backoff (OOOOO0O0000O0000O ,OOO0O0OO00OOOO00O ,OO00OOOOOO00OO0OO ,OO000OO0O0OOO0O00 ,backoff_seconds =0 ):#line:64
        for OO00O0O0OO00O0OOO in range (OO00OOOOOO00OO0OO ):#line:65
            O00O0O0000000O000 =False #line:66
            try :#line:67
                return await OOO0O0OO00OOOO00O ()#line:68
            except asyncio .TimeoutError :#line:69
                if not O00O0O0000000O000 :#line:70
                    OOOOO0O0000O0000O .log .debug (f'第{OO00O0O0OO00O0OOO + 1}次重试 {OO000OO0O0OOO0O00} 请求超时')#line:71
                    O00O0O0000000O000 =True #line:72
                await asyncio .sleep (backoff_seconds )#line:73
            except Exception as OOO00O0OO000OO0OO :#line:74
                if not O00O0O0000000O000 :#line:75
                    OOOOO0O0000O0000O .log .debug (f'第{OO00O0O0OO00O0OOO + 1}次重试 {OO000OO0O0OOO0O00} 出错：{OOO00O0OO000OO0OO}')#line:76
                    O00O0O0000000O000 =True #line:77
                await asyncio .sleep (backoff_seconds )#line:78
            if O00O0O0000000O000 and OO00O0O0OO00O0OOO ==OO00OOOOOO00OO0OO -1 :#line:80
                OOOOO0O0000O0000O .log .error (f'{OO000OO0O0OOO0O00} 重试{OO00OOOOOO00OO0OO}次后仍然发生异常')#line:81
                return False ,False ,False #line:82
    async def GET_POST (OOO0OO0OOO0OOOOOO ,OO0000OOO000O000O ,num =1 ):#line:84
        async def OOO0O0OO0O0O0OO0O ():#line:85
            async with aiohttp .ClientSession ()as O0OOOOO0OO0OO0OOO :#line:86
                if OO0000OOO000O000O ['method']=='get':#line:87
                    async with O0OOOOO0OO0OO0OOO .get (**OO0000OOO000O000O ['kwargs'])as OO00OOO0000OOO00O :#line:88
                        O0O00OOO000O0O0OO =OO00OOO0000OOO00O .status #line:89
                        OO00OOO0OOO00O0O0 =await OO00OOO0000OOO00O .text ()#line:90
                else :#line:91
                    async with O0OOOOO0OO0OO0OOO .post (**OO0000OOO000O000O ['kwargs'])as OO00OOO0000OOO00O :#line:92
                        O0O00OOO000O0O0OO =OO00OOO0000OOO00O .status #line:93
                        OO00OOO0OOO00O0O0 =await OO00OOO0000OOO00O .text ()#line:94
                if O0O00OOO000O0O0OO !=200 :#line:95
                    await asyncio .sleep (3 )#line:96
                    if num >3 :#line:97
                        OOO0OO0OOO0OOOOOO .log .warning (f'{O0O00OOO000O0O0OO}:状态超出3次')#line:98
                        return False ,False ,False #line:99
                    OOO0OO0OOO0OOOOOO .log .debug (f'{O0O00OOO000O0O0OO}:去重试 第{num}次')#line:100
                    return await OOO0OO0OOO0OOOOOO .GET_POST (OO0000OOO000O000O ,num +1 )#line:101
                try :#line:102
                    OOOO00OO0O00O0OOO =json .loads (OO00OOO0OOO00O0O0 )#line:103
                except :#line:104
                    OOOO00OO0O00O0OOO =OO00OOO0OOO00O0O0 #line:105
                return O0O00OOO000O0O0OO ,OO00OOO0OOO00O0O0 ,OOOO00OO0O00O0OOO #line:106
        return await OOO0OO0OOO0OOOOOO .retry_with_backoff (OOO0O0OO0O0O0OO0O ,3 ,f'GET_POST')#line:108
    async def verify (OO00O000O00O0000O ):#line:110
        async def OOOOOOOO00O00000O ():#line:111
            OO0OOOO000O0OO0OO ='https://api.ixu.cc/verify'#line:112
            async with aiohttp .ClientSession ()as OO0O0O0000OOO0O00 :#line:113
                async with OO0O0O0000OOO0O00 .get (OO0OOOO000O0OO0OO ,data ={'TOKEN':OO00O000O00O0000O .token },timeout =3 )as OO0000OOOOOO000O0 :#line:114
                    OOO000000OO000O00 =await OO0000OOOOOO000O0 .json ()#line:115
                    if OO0000OOOOOO000O0 .status ==200 :#line:116
                        OO00O000O00O0000O .verify_result =True #line:117
                        OO00O000O00O0000O .log .info (f'认证通过 UserId：{OOO000000OO000O00["user_id"]}')#line:118
                        return OOO000000OO000O00 #line:119
                    else :#line:120
                        OO00O000O00O0000O .log .error (f"授权未通过:{OOO000000OO000O00['error']}")#line:121
                        sys .exit ()#line:122
        return await OO00O000O00O0000O .retry_with_backoff (OOOOOOOO00O00000O ,3 ,'verify')#line:124
    async def Get_H5st (O000O0O000O0OOOO0 ,O0O000O0OOO0O0O00 ,OOO000OOOO00OO0OO ,OO0OOOO00O0O0O00O ,O0OOO0O0OOO000O00 ):#line:126
        if O000O0O000O0OOOO0 .verify_result !=True :#line:127
            await O000O0O000O0OOOO0 .verify ()#line:128
        if O000O0O000O0OOOO0 .verify_result !=True :#line:129
            O000O0O000O0OOOO0 .log .error ("授权未通过 退出")#line:130
            sys .exit ()#line:131
        OO000OOO0OO0OO0OO ={'method':'','kwargs':{'url':'https://api.ouklc.com/api/h5st','params':{'functionId':O0O000O0OOO0O0O00 ,'body':json .dumps (OO0OOOO00O0O0O00O ),'ua':O000O0O000O0OOOO0 .ua ,'pin':O000O0O000O0OOOO0 .pt_pin (OOO000OOOO00OO0OO ),'appId':O0OOO0O0OOO000O00 }}}#line:144
        OOO0OOOO0O0O0OO00 ,O0O00OOOO0000O0OO ,OO0000OOOO0OOO0OO =await O000O0O000O0OOOO0 .GET_POST (OO000OOO0OO0OO0OO )#line:145
        if OOO0OOOO0O0O0OO00 !=200 :#line:146
            return await O000O0O000O0OOOO0 .Get_H5st (O0O000O0OOO0O0O00 ,OOO000OOOO00OO0OO ,OO0OOOO00O0O0O00O ,O0OOO0O0OOO000O00 )#line:147
        OO000OOO0OO0OO0OO ={'method':'post','kwargs':{'url':f'https://api.m.jd.com','headers':{"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OOO000OOOO00OO0OO ,"User-Agent":O000O0O000O0OOOO0 .ua },'data':OO0000OOOO0OOO0OO ["body"]}}#line:167
        if O000O0O000O0OOOO0 .proxy :#line:168
            OO000OOO0OO0OO0OO ['kwargs'].update ({'proxy':O000O0O000O0OOOO0 .proxy })#line:169
        OOO0OOOO0O0O0OO00 ,O0O00OOOO0000O0OO ,OO0000OOOO0OOO0OO =await O000O0O000O0OOOO0 .GET_POST (OO000OOO0OO0OO0OO )#line:170
        return OO0000OOOO0OOO0OO #line:171
    def pt_pin (OO0O00OOOOOO0000O ,OOOOOOO0O0O000O00 ):#line:173
        try :#line:174
            OO0OO0OO0OO000O00 =re .compile (r'pt_pin=(.*?);').findall (OOOOOOO0O0O000O00 )[0 ]#line:175
            OO0OO0OO0OO000O00 =unquote_plus (OO0OO0OO0OO000O00 )#line:176
        except IndexError :#line:177
            OO0OO0OO0OO000O00 =re .compile (r'pin=(.*?);').findall (OOOOOOO0O0O000O00 )[0 ]#line:178
            OO0OO0OO0OO000O00 =unquote_plus (OO0OO0OO0OO000O00 )#line:179
        return OO0OO0OO0OO000O00 #line:180
    def convert_ms_to_hours_minutes (O0O0O000O00000O00 ,OOOO0O0OOO0OO0000 ):#line:182
        OO0OO000O00O000O0 =OOOO0O0OOO0OO0000 //1000 #line:183
        OOOO00O0OO000OO00 ,OO0OO000O00O000O0 =divmod (OO0OO000O00O000O0 ,60 )#line:184
        OOO00O0O00OO0O000 ,OOOO00O0OO000OO00 =divmod (OOOO00O0OO000OO00 ,60 )#line:185
        return f'{OOO00O0O00OO0O000}小时{OOOO00O0OO000OO00}分'#line:186
    async def inviteFissionReceive (O0OOOO00O00OO0OOO ,OO0OO0O0OO00OO000 ,OO00O00O00OO0O000 ,page =1 ):#line:188
        if O0OOOO00O00OO0OOO .verify_result !=True :#line:189
            await O0OOOO00O00OO0OOO .verify ()#line:190
        if O0OOOO00O00OO0OOO .verify_result !=True :#line:191
            O0OOOO00O00OO0OOO .log .error ("授权未通过 退出")#line:192
            sys .exit ()#line:193
        OO00O0O00OOOO0OO0 =generate_random_user_agent ()#line:194
        O00O0OOO000000OO0 ={'linkId':OO00O00O00OO0O000 ,}#line:197
        OO0O0OO00O000OO00 =await O0OOOO00O00OO0OOO .Get_H5st ('inviteFissionReceive',OO0OO0O0OO00OO000 ,O00O0OOO000000OO0 ,'b8469')#line:198
        if OO0O0OO00O000OO00 ['success']==False and OO0O0OO00O000OO00 ['errMsg']=='活动太火爆，请稍候重试':#line:199
            O0OO0O000OO00OO0O =f'还差{O0OOOO00O00OO0OOO.leftAmount / O0OOOO00O00OO0OOO.amount}次'if O0OOOO00O00OO0OOO .amount !=0 else '先去助力一次才能计算需要人数'#line:200
            O0OOOO00O00OO0OOO .log .debug (f'没助理了 快去助理吧 {O0OO0O000OO00OO0O}')#line:201
            await O0OOOO00O00OO0OOO .superRedBagList (OO0OO0O0OO00OO000 ,OO00O00O00OO0O000 ,page )#line:202
            return False #line:203
        if OO0O0OO00O000OO00 ['success']and OO0O0OO00O000OO00 ['code']==0 :#line:209
            O0OOOO00O00OO0OOO .amount =float (OO0O0OO00O000OO00 ["data"]["receiveList"][0 ]["amount"])#line:210
            O0OOOO00O00OO0OOO .leftAmount =float (OO0O0OO00O000OO00 ["data"]["leftAmount"])#line:211
            O0OOOO00O00OO0OOO .log .info (f'领取中:{OO0O0OO00O000OO00["data"]["totalAmount"]} 当前:{OO0O0OO00O000OO00["data"]["amount"]} 获得:{OO0O0OO00O000OO00["data"]["receiveList"][0]["amount"]} 还差:{OO0O0OO00O000OO00["data"]["leftAmount"]}元/{O0OOOO00O00OO0OOO.leftAmount / O0OOOO00O00OO0OOO.amount}次 当前进度:{OO0O0OO00O000OO00["data"]["rate"]}%')#line:213
            if int (OO0O0OO00O000OO00 ["data"]["rate"])==100 :#line:214
                O0OOOO00O00OO0OOO .log .info (f'领取中:{OO0O0OO00O000OO00["data"]["totalAmount"]} 进度:{OO0O0OO00O000OO00["data"]["rate"]}% 退出!')#line:215
                await O0OOOO00O00OO0OOO .superRedBagList (OO0OO0O0OO00OO000 ,OO00O00O00OO0O000 ,page )#line:216
                return False #line:217
        return True #line:218
    async def apCashWithDraw (O000O000O0O0O00O0 ,OOOO0OOO0OO0O00OO ,OO0OO00O00O0OO0OO ,OOOO0OO000OO00O0O ,OO0OOOO000O000OO0 ,OO000OOOOO0O0O00O ,O00000OOOOOOOOOO0 ):#line:220
        if O000O000O0O0O00O0 .verify_result !=True :#line:221
            await O000O000O0O0O00O0 .verify ()#line:222
        if O000O000O0O0O00O0 .verify_result !=True :#line:223
            O000O000O0O0O00O0 .log .error ("授权未通过 退出")#line:224
            sys .exit ()#line:225
        OOO00000000OO0O00 =generate_random_user_agent ()#line:226
        O000OO00000OO000O =await O000O000O0O0O00O0 .Get_H5st ("apCashWithDraw",OO0OO00O00O0OO0OO ,{"linkId":OOOO0OOO0OO0O00OO ,"businessSource":"NONE","base":{"id":OOOO0OO000OO00O0O ,"business":"fission","poolBaseId":OO0OOOO000O000OO0 ,"prizeGroupId":OO000OOOOO0O0O00O ,"prizeBaseId":O00000OOOOOOOOOO0 ,"prizeType":4 }},'8c6ae')#line:242
        return O000OO00000OO000O #line:243
    async def inviteFissionBeforeHome (OOO0O0OOO0O0O00OO ,num =1 ):#line:245
        OOO0000000O00OO00 =False #line:246
        for O000OOOOOO000OO00 in ck :#line:247
            if len (OOO0O0OOO0O0O00OO .power_success )>=num :#line:248
                return await OOO0O0OOO0O0O00OO .inviteFissionReceive (OOO0O0OOO0O0O00OO .cookie ,OOO0O0OOO0O0O00OO .linkId )#line:249
            O00O0O00OOOOOOOO0 =await OOO0O0OOO0O0O00OO .Get_H5st ("inviteFissionBeforeHome",O000OOOOOO000OO00 ,{'linkId':OOO0O0OOO0O0O00OO .linkId ,"isJdApp":True ,'inviter':OOO0O0OOO0O0O00OO .inviter },'02f8d',)#line:252
            if int (O00O0O00OOOOOOOO0 ['code'])==0 :#line:253
                for OO0OO0OOO0O000OOO ,OO0OOO00OOOO0000O in OOO0O0OOO0O0O00OO .helpResult :#line:254
                    if O00O0O00OOOOOOOO0 ['data']['helpResult']==int (OO0OO0OOO0O000OOO ):#line:255
                        OOO0000000O00OO00 =True #line:256
                        OOO0O0OOO0O0O00OO .log .info (f"Id:{OOO0O0OOO0O0O00OO.linkId[:4] + '****' + OOO0O0OOO0O0O00OO.linkId[-4:]}|助理:{O00O0O00OOOOOOOO0['data']['nickName']}|{O00O0O00OOOOOOOO0['data']['helpResult']}|{OOO0O0OOO0O0O00OO.pt_pin(O000OOOOOO000OO00)}|{OO0OOO00OOOO0000O}")#line:258
                        if O00O0O00OOOOOOOO0 ['data']['helpResult']==1 :#line:259
                            OOO0O0OOO0O0O00OO .power_success .append (O000OOOOOO000OO00 )#line:260
                        else :#line:261
                            OOO0O0OOO0O0O00OO .power_failure .append (O000OOOOOO000OO00 )#line:262
                    if not OOO0000000O00OO00 :#line:263
                        OO0OOO00OOOO0000O ='❌未知状态 (可能是活动未开启！！！)'#line:264
                        OOO0O0OOO0O0O00OO .power_failure .append (O000OOOOOO000OO00 )#line:265
                        OOO0O0OOO0O0O00OO .log .info (f"Id:{OOO0O0OOO0O0O00OO.linkId[:4] + '****' + OOO0O0OOO0O0O00OO.linkId[-4:]}|助理:{O00O0O00OOOOOOOO0['data']['nickName']}|{O00O0O00OOOOOOOO0['data']['helpResult']}|{OOO0O0OOO0O0O00OO.pt_pin(O000OOOOOO000OO00)}|{OO0OOO00OOOO0000O}")#line:267
            else :#line:268
                OOO0O0OOO0O0O00OO .log .info (f"{OOO0O0OOO0O0O00OO.pt_pin(O000OOOOOO000OO00)}{O00O0O00OOOOOOOO0['code']} 结果:💔{O00O0O00OOOOOOOO0['errMsg']}")#line:269
    async def superRedBagList (O0O0O000OO0OOO0O0 ,OOOOO0OO0OOO0OOO0 ,OOO0OO00OOOOO00OO ,O00O0OO0OO0OO00O0 ):#line:271
        if O0O0O000OO0OOO0O0 .verify_result !=True :#line:272
            await O0O0O000OO0OOO0O0 .verify ()#line:273
        if O0O0O000OO0OOO0O0 .verify_result !=True :#line:274
            O0O0O000OO0OOO0O0 .log .error ("授权未通过 退出")#line:275
            sys .exit ()#line:276
        O00OO00OO0OO00O00 =await O0O0O000OO0OOO0O0 .Get_H5st ('superRedBagList',OOOOO0OO0OOO0OOO0 ,{"pageNum":O00O0OO0OO0OO00O0 ,"pageSize":200 ,"linkId":OOO0OO00OOOOO00OO ,"business":"fission"},'f2b1d')#line:279
        O0O0O000OO0OOO0O0 .log .info (f"开始提取{O00O0OO0OO0OO00O0}页, 共{len(O00OO00OO0OO00O00['data']['items'])}条记录")#line:280
        if not O00OO00OO0OO00O00 ['data']['hasMore']:#line:281
            return False #line:282
        for O00000OOOO00O0OO0 in O00OO00OO0OO00O00 ['data']['items']:#line:283
            OOO0OO00OOOO00OOO ,O00O00OO0000OO000 ,OOO00OO0OO0O000O0 ,O00OOOOO000OO0O00 ,O00OO00000O00OOOO ,OOO0O0OOOO00O0OO0 ,OO0O0OOOOO0O0O0O0 ,O0OO0OOOO0OOO000O ,O000OO0O00O000000 =(O00000OOOO00O0OO0 ['id'],O00000OOOO00O0OO0 ['amount'],O00000OOOO00O0OO0 ['prizeType'],O00000OOOO00O0OO0 ['state'],O00000OOOO00O0OO0 ['prizeConfigName'],O00000OOOO00O0OO0 ['prizeGroupId'],O00000OOOO00O0OO0 ['poolBaseId'],O00000OOOO00O0OO0 ['prizeBaseId'],O00000OOOO00O0OO0 ['startTime'])#line:288
            OOO0O0000O0O0O000 =True #line:289
            while OOO0O0000O0O0O000 :#line:290
                if OOO00OO0OO0O000O0 not in O0O0O000OO0OOO0O0 .rewardType and float (O00O00OO0000OO000 )>1.0 :#line:291
                    O0O0O000OO0OOO0O0 .log .info (f"{O000OO0O00O000000} {O00O00OO0000OO000}元 {'❌未提现' if OOO00OO0OO0O000O0 == 4 and O00OOOOO000OO0O00 != 3 else '✅已提现'}")#line:292
                    OOO0O0000O0O0O000 =False #line:293
                if OOO00OO0OO0O000O0 ==4 and O00OOOOO000OO0O00 !=3 and O00OOOOO000OO0O00 !=4 :#line:294
                    O00OO00OO0OO00O00 =await O0O0O000OO0OOO0O0 .apCashWithDraw (OOO0OO00OOOOO00OO ,OOOOO0OO0OOO0OOO0 ,OOO0OO00OOOO00OOO ,OO0O0OOOOO0O0O0O0 ,OOO0O0OOOO00O0OO0 ,O0OO0OOOO0OOO000O )#line:295
                    if int (O00OO00OO0OO00O00 ['data']['status'])==310 :#line:296
                        O0O0O000OO0OOO0O0 .log .info (f"✅{O00O00OO0000OO000}现金💵 提现成功")#line:297
                        O0O0O000OO0OOO0O0 .successful .append (O00O00OO0000OO000 )#line:298
                        await asyncio .sleep (1 )#line:299
                        OOO0O0000O0O0O000 =False #line:300
                    elif int (O00OO00OO0OO00O00 ['data']['status'])==50056 or int (O00OO00OO0OO00O00 ['data']['status'])==50001 :#line:301
                        O0O0O000OO0OOO0O0 .log .warning (f"❌{O00O00OO0000OO000}现金💵 重新发起 提现失败:{O00OO00OO0OO00O00['data']['message']}")#line:302
                        await asyncio .sleep (3 )#line:303
                    elif '金额超过自然月上限'in O00OO00OO0OO00O00 ['data']['message']:#line:304
                        O0O0O000OO0OOO0O0 .log .info (f"{O00O00OO0000OO000}现金:{O00OO00OO0OO00O00['data']['message']}:去兑换红包")#line:305
                        OOO0O0000O0O0O000 =await O0O0O000OO0OOO0O0 .apRecompenseDrawPrize (OOO0OO00OOOOO00OO ,OOOOO0OO0OOO0OOO0 ,OOO0OO00OOOO00OOO ,OO0O0OOOOO0O0O0O0 ,OOO0O0OOOO00O0OO0 ,O0OO0OOOO0OOO000O ,O00O00OO0000OO000 )#line:306
                        await asyncio .sleep (3 )#line:307
                    else :#line:308
                        O0O0O000OO0OOO0O0 .log .error (f"{O00O00OO0000OO000}现金 ❌提现错误:{O00OO00OO0OO00O00['data']['status']} {O00OO00OO0OO00O00['data']['message']}")#line:309
                        print (OOO00OO0OO0O000O0 ,O00OOOOO000OO0O00 )#line:310
                        OOO0O0000O0O0O000 =False #line:311
                else :#line:312
                    OOO0O0000O0O0O000 =False #line:313
        return True #line:314
    async def apRecompenseDrawPrize (O0OO0O000O00000O0 ,OO0O0O0O000O0OOO0 ,OOOOO0O0OO0O00000 ,OOOOO00OO0OO0000O ,OO00O0OOOOO0OO000 ,O0OO00O000O0OOOOO ,O0OOO0OO000O00O0O ,OOO00OOOO00O00OO0 ):#line:321
        O00OO000OOO00OOOO =await O0OO0O000O00000O0 .Get_H5st ('apRecompenseDrawPrize',OOOOO0O0OO0O00000 ,{"linkId":OO0O0O0O000O0OOO0 ,"businessSource":"fission","drawRecordId":OOOOO00OO0OO0000O ,"business":"fission","poolId":OO00O0OOOOO0OO000 ,"prizeGroupId":O0OO00O000O0OOOOO ,"prizeId":O0OOO0OO000O00O0O ,},'8c6ae')#line:331
        if O00OO000OOO00OOOO ['success']and int (O00OO000OOO00OOOO ['data']['resCode'])==0 :#line:332
            O0OO0O000O00000O0 .log .info (f"{OOO00OOOO00O00OO0}现金:🧧红包兑换成功")#line:333
            O0OO0O000O00000O0 .cash_redpacket .append (OOO00OOOO00O00OO0 )#line:334
            return False #line:335
        else :#line:336
            O0OO0O000O00000O0 .log .info (f"{OOO00OOOO00O00OO0}现金:🧧红包兑换失败 {O00OO000OOO00OOOO}")#line:337
            return True #line:338
    async def Fission_Draw (O0OO0O00000OOO00O ,O00O0O0O0O000O0O0 ,OO0OOO0O0OOOOO000 ):#line:340
        O0OO0O00000OOO00O .log .info (f"****************开始抽奖****************")#line:341
        while True :#line:342
            OOOOOO00OO00000O0 =await O0OO0O00000OOO00O .Get_H5st ('inviteFissionDrawPrize',O00O0O0O0O000O0O0 ,{"linkId":OO0OOO0O0OOOOO000 },'c02c6')#line:345
            if not OOOOOO00OO00000O0 ['success']:#line:347
                if "抽奖次数已用完"in OOOOOO00OO00000O0 ['errMsg']:#line:348
                    O0OO0O00000OOO00O .log .debug (f"⚠️抽奖次数已用完")#line:349
                    break #line:350
                elif "本场活动已结束"in OOOOOO00OO00000O0 ['errMsg']:#line:351
                    O0OO0O00000OOO00O .log .debug (f"⏰本场活动已结束了,快去重新开始吧")#line:352
                    sys .exit ()#line:353
            try :#line:354
                if not OOOOOO00OO00000O0 ['success']:#line:355
                    O0OO0O00000OOO00O .log .warning (f'{OOOOOO00OO00000O0["errMsg"]}')#line:356
                    time .sleep (1 )#line:357
                    continue #line:358
                if int (OOOOOO00OO00000O0 ['data']['rewardType'])in O0OO0O00000OOO00O .rewardType :#line:361
                    O0OO0O00000OOO00O .log .info (f"获得:{OOOOOO00OO00000O0['data']['prizeValue']}元{O0OO0O00000OOO00O.rewardType[int(OOOOOO00OO00000O0['data']['rewardType'])]['msg']}")#line:363
                    if int (OOOOOO00OO00000O0 ['data']['rewardType'])==2 :#line:364
                        O0OO0O00000OOO00O .redpacket .append (float (OOOOOO00OO00000O0 ['data']['prizeValue']))#line:365
                else :#line:366
                    print (OOOOOO00OO00000O0 ['data']['rewardType'])#line:367
                    O0OO0O00000OOO00O .log .info (f"获得:{OOOOOO00OO00000O0['data']['prizeValue']}元现金💵")#line:368
                    O0OO0O00000OOO00O .cash .append (float (OOOOOO00OO00000O0 ['data']['prizeValue']))#line:369
            except Exception as OO0O0000O0OOO0O00 :#line:370
                O0OO0O00000OOO00O .log .error (f'(未知物品):{OOOOOO00OO00000O0}')#line:371
            await asyncio .sleep (0.3 )#line:372
        O0OO0O00000OOO00O .log .info (f"抽奖结束: 💵现金:{'{:.2f}'.format(sum([float(OOOO00OOOOO0OOO00) for OOOO00OOOOO0OOO00 in O0OO0O00000OOO00O.cash]))}元, 🧧红包:{'{:.2f}'.format(sum([float(OOOO0O00OOOO0O0O0) for OOOO0O00OOOO0O0O0 in O0OO0O00000OOO00O.redpacket]))}元")#line:374
        O0OO0O00000OOO00O .log .info (f"****************开始提现****************")#line:375
        O0OO0000O0OO000O0 =0 #line:376
        while True :#line:377
            O0OO0000O0OO000O0 =O0OO0000O0OO000O0 +1 #line:378
            OO0OO0000OOOOOO00 =await O0OO0O00000OOO00O .superRedBagList (O00O0O0O0O000O0O0 ,OO0OOO0O0OOOOO000 ,O0OO0000O0OO000O0 )#line:379
            await asyncio .sleep (2 )#line:380
            if O0OO0000O0OO000O0 >=O0OO0O00000OOO00O .page :#line:381
                break #line:382
            if not OO0OO0000OOOOOO00 :#line:383
                break #line:384
        O0O0O00O0O0000O0O =('提现结束: ')+(f"💵现金:{'{:.2f}'.format(sum([float(O000OOOO00OOO0000) for O000OOOO00OOO0000 in O0OO0O00000OOO00O.successful]))}元/")+(f"🧧兑换红包:{'{:.2f}'.format(sum([float(O0OOO0O000O000000) for O0OOO0O000O000000 in O0OO0O00000OOO00O.cash_redpacket]))}元/共计红包:{'{:.2f}'.format(sum([float(OOOOOOO0O0OOO0000) for OOOOOOO0O0OOO0000 in O0OO0O00000OOO00O.redpacket + O0OO0O00000OOO00O.cash_redpacket]))}")#line:390
        if not O0OO0O00000OOO00O .successful and not O0OO0O00000OOO00O .cash_redpacket :#line:391
            O0O0O00O0O0000O0O ='提现结束: 一毛都没有哦！'#line:392
        O0OO0O00000OOO00O .log .info (O0O0O00O0O0000O0O )#line:393
    async def add_LinkId (O0O00O000OOOO00OO ):#line:395
        async def OOO000OO000O0OO0O ():#line:396
            if O0O00O000OOOO00OO .verify_result !=True :#line:397
                await O0O00O000OOOO00OO .verify ()#line:398
            if O0O00O000OOOO00OO .verify_result !=True :#line:399
                O0O00O000OOOO00OO .log .error ("授权未通过 退出")#line:400
                sys .exit ()#line:401
            O0OOOOOOOO0000O00 ='https://api.ixu.cc/status/inviter.json'#line:402
            async with aiohttp .ClientSession ()as O0OOOOO0OOOOO00O0 :#line:403
                async with O0OOOOO0OOOOO00O0 .get (O0OOOOOOOO0000O00 ,timeout =5 )as O0O0O0O000OOO00OO :#line:404
                    if O0O0O0O000OOO00OO .status ==200 :#line:405
                        OO000OOO0000OO0OO =await O0O0O0O000OOO00OO .json ()#line:406
                        if OO000OOO0000OO0OO ['stats']!='True':#line:407
                            O0O00O000OOOO00OO .log .error (f"{OO000OOO0000OO0OO['err_text']}")#line:408
                            sys .exit ()#line:409
                        O0O00O000OOOO00OO .inviter_help =OO000OOO0000OO0OO ['inviter']#line:410
                        if len (OO000OOO0000OO0OO ['text'])>0 :#line:411
                            O0O00O000OOOO00OO .log .debug (f'那女孩对你说:{OO000OOO0000OO0OO["text"]}')#line:412
                        if O0O00O000OOOO00OO .scode =='ALL'or O0O00O000OOOO00OO .scode =='all':#line:413
                            for OO0O00O0O00OOO000 in OO000OOO0000OO0OO ['linkId']:#line:414
                                O0O00O000OOOO00OO .linkId .append (OO0O00O0O00OOO000 )#line:415
                                O0O00O000OOOO00OO .log .info (f'云端获取到linkId:{OO0O00O0O00OOO000}')#line:416
                            return True #line:417
                        else :#line:418
                            O0O00O000OOOO00OO .linkId .append (OO000OOO0000OO0OO ['linkId'][int (O0O00O000OOOO00OO .scode )-1 ])#line:419
                            O0O00O000OOOO00OO .log .info (f'云端获取到linkId:{OO000OOO0000OO0OO["linkId"][int(O0O00O000OOOO00OO.scode) - 1]}')#line:420
                            return True #line:421
                    else :#line:422
                        O0O00O000OOOO00OO .log .error ('未获取到linkId 重试')#line:423
        return await O0O00O000OOOO00OO .retry_with_backoff (OOO000OO000O0OO0O ,3 ,'linkId')#line:425
    async def task_start (O0O00O0000O00O00O ):#line:427
        if O0O00O0000O00O00O .verify_result !=True :#line:428
            await O0O00O0000O00O00O .verify ()#line:429
        if O0O00O0000O00O00O .verify_result !=True :#line:430
            O0O00O0000O00O00O .log .error ("授权未通过 退出")#line:431
            sys .exit ()#line:432
        await O0O00O0000O00O00O .add_LinkId ()#line:433
        OOO0OOOOO0OOOO000 =O0O00O0000O00O00O .cookie #line:436
        if O0O00O0000O00O00O .txj_status :#line:437
            try :#line:438
                O0O00O0000OOOO0OO =await O0O00O0000O00O00O .Get_H5st ('inviteFissionHome',OOO0OOOOO0OOOO000 ,{'linkId':O0O00O0000O00O00O .linkId [0 ],"inviter":"",},'eb67b')#line:440
                if not O0O00O0000OOOO0OO ['success']and O0O00O0000OOOO0OO ['errMsg']=='未登录':#line:442
                    O0O00O0000O00O00O .log .error (f"{O0O00O0000OOOO0OO['errMsg']}")#line:443
                    return #line:444
                O0O0OO0OOO0O0OO0O =O0O00O0000OOOO0OO ['data']#line:445
                if O0O0OO0OOO0O0OO0O ['cashVo']!=None :#line:446
                    O00OOOOO0OO00OOO0 =O0O0OO0OOO0O0OO0O ['cashVo']#line:447
                    O0O00O0000O00O00O .log .info (f"Name:{O00OOOOO0OO00OOO0['userInfo']['nickName']} 已助理:{O0O0OO0OOO0O0OO0O['prizeNum'] + O0O0OO0OOO0O0OO0O['drawPrizeNum']} 提现:{O00OOOOO0OO00OOO0['totalAmount']}元 当前:{O00OOOOO0OO00OOO0['amount']}元 进度{O00OOOOO0OO00OOO0['rate']}% 剩余时间:{O0O00O0000O00O00O.convert_ms_to_hours_minutes(O0O0OO0OOO0O0OO0O['countDownTime'])}")#line:449
                    if int (O00OOOOO0OO00OOO0 ['rate'])==100 :#line:450
                        O0O00O0000O00O00O .log .info (f"本轮您已提现{O00OOOOO0OO00OOO0['totalAmount']}元了 等{O0O00O0000O00O00O.convert_ms_to_hours_minutes(O0O0OO0OOO0O0OO0O['countDownTime'])}后在来吧")#line:452
                        await O0O00O0000O00O00O .superRedBagList (OOO0OOOOO0OOOO000 ,O0O00O0000O00O00O .linkId [0 ],1 )#line:453
                        return #line:454
                else :#line:455
                    O0O00O0000O00O00O .log .error ('哦和 黑号了哦')#line:456
                while True :#line:458
                    OO0O00OOOOO00O000 =await O0O00O0000O00O00O .inviteFissionReceive (OOO0OOOOO0OOOO000 ,O0O00O0000O00O00O .linkId [0 ])#line:459
                    time .sleep (0.3 )#line:462
            except Exception as O0000O0O00O0OOO00 :#line:463
                O0O00O0000O00O00O .log .error ('黑号')#line:464
        else :#line:465
            for OO00O0O000000O0OO in O0O00O0000O00O00O .linkId :#line:466
                O0O00O0000O00O00O .log .info (f'开始执行 LinkId:{OO00O0O000000O0OO}')#line:467
                await O0O00O0000O00O00O .Fission_Draw (OOO0OOOOO0OOOO000 ,OO00O0O000000O0OO )#line:468
if __name__ =='__main__':#line:471
    pdd =TEN_JD_PDD_DRAW ()#line:472
    loop =asyncio .get_event_loop ()#line:473
    loop .run_until_complete (pdd .task_start ())#line:474
    loop .close ()#line:475
