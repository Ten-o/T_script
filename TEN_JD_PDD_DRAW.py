""#line:9
from utils .logger import setup_logger #line:11
from utils .X_API_EID_TOKEN import *#line:12
from utils .User_agent import RandomUA ,generate_random_user_agent #line:13
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
    def __init__ (OO00O0OOOO0O0OO00 ):#line:28
        OO00O0OOOO0O0OO00 .log =setup_logger ()#line:29
        OO00O0OOOO0O0OO00 .ua =generate_random_user_agent ()#line:30
        OO00O0OOOO0O0OO00 .page =10 #line:31
        OO00O0OOOO0O0OO00 .start =time .time ()#line:32
        OO00O0OOOO0O0OO00 .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else False #line:33
        OO00O0OOOO0O0OO00 .scode =os .environ .get ("TEN_scode")if os .environ .get ("TEN_scode")else 'all'#line:34
        OO00O0OOOO0O0OO00 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:35
        OO00O0OOOO0O0OO00 .numer_og =os .environ .get ("draw_numer")if os .environ .get ("draw_numer")else 3 #line:36
        OO00O0OOOO0O0OO00 .activityUrl ="https://pro.m.jd.com"#line:37
        OO00O0OOOO0O0OO00 .cookie =os .environ .get ("draw_cookie")if os .environ .get ("draw_cookie")else ck [0 ]#line:38
        OO00O0OOOO0O0OO00 .linkId =[]#line:39
        OO00O0OOOO0O0OO00 .amount =0 #line:40
        OO00O0OOOO0O0OO00 .leftAmount =0 #line:41
        OO00O0OOOO0O0OO00 .verify_result =False #line:42
        OO00O0OOOO0O0OO00 .txj_status =os .environ .get ("txj_status")if os .environ .get ("txj_status")else False #line:43
        OO00O0OOOO0O0OO00 .inviter =''#line:44
        OO00O0OOOO0O0OO00 .power_success =[]#line:45
        OO00O0OOOO0O0OO00 .power_failure =[]#line:46
        OO00O0OOOO0O0OO00 .redpacket =[]#line:47
        OO00O0OOOO0O0OO00 .cash =[]#line:48
        OO00O0OOOO0O0OO00 .cash_redpacket =[]#line:49
        OO00O0OOOO0O0OO00 .helpResult ={(1 ,'✅助力成功'),(2 ,'❌活动火爆'),(3 ,'❌没有助力次数'),(4 ,'❌助力次数用尽'),(6 ,'❌已助力')}#line:56
        OO00O0OOOO0O0OO00 .rewardType ={1 :{'msg':'优惠券🎫'},2 :{'msg':'红包🧧'},6 :{'msg':'惊喜小礼包🎫'},}#line:61
        OO00O0OOOO0O0OO00 .successful =[]#line:62
    async def retry_with_backoff (O0000O0OOO000O000 ,OO000OOO0000O0O0O ,OOOO0000OOO0000O0 ,OO00OO0OO0000OOOO ,backoff_seconds =0 ):#line:64
        for OO0O000O0OOOO0OO0 in range (OOOO0000OOO0000O0 ):#line:65
            O00O0OOOO0OOOOOOO =False #line:66
            try :#line:67
                return await OO000OOO0000O0O0O ()#line:68
            except asyncio .TimeoutError :#line:69
                if not O00O0OOOO0OOOOOOO :#line:70
                    O0000O0OOO000O000 .log .debug (f'第{OO0O000O0OOOO0OO0 + 1}次重试 {OO00OO0OO0000OOOO} 请求超时')#line:71
                    O00O0OOOO0OOOOOOO =True #line:72
                await asyncio .sleep (backoff_seconds )#line:73
            except Exception as O0O0O0OO0000O000O :#line:74
                if not O00O0OOOO0OOOOOOO :#line:75
                    O0000O0OOO000O000 .log .debug (f'第{OO0O000O0OOOO0OO0 + 1}次重试 {OO00OO0OO0000OOOO} 出错：{O0O0O0OO0000O000O}')#line:76
                    O00O0OOOO0OOOOOOO =True #line:77
                await asyncio .sleep (backoff_seconds )#line:78
            if O00O0OOOO0OOOOOOO and OO0O000O0OOOO0OO0 ==OOOO0000OOO0000O0 -1 :#line:80
                O0000O0OOO000O000 .log .error (f'{OO00OO0OO0000OOOO} 重试{OOOO0000OOO0000O0}次后仍然发生异常')#line:81
                return False ,False ,False #line:82
    async def GET_POST (O0OOOO00O000O0O0O ,O0000O0O0OO0O00OO ,num =1 ):#line:84
        async def O0O00O00O000OOOOO ():#line:85
            async with aiohttp .ClientSession ()as OO00OOO000O00OOO0 :#line:86
                if O0000O0O0OO0O00OO ['method']=='get':#line:87
                    async with OO00OOO000O00OOO0 .get (**O0000O0O0OO0O00OO ['kwargs'])as OOO00O0OOO000OOOO :#line:88
                        O00OO000000O000OO =OOO00O0OOO000OOOO .status #line:89
                        O0O0OO000OOO0O0OO =await OOO00O0OOO000OOOO .text ()#line:90
                else :#line:91
                    async with OO00OOO000O00OOO0 .post (**O0000O0O0OO0O00OO ['kwargs'])as OOO00O0OOO000OOOO :#line:92
                        O00OO000000O000OO =OOO00O0OOO000OOOO .status #line:93
                        O0O0OO000OOO0O0OO =await OOO00O0OOO000OOOO .text ()#line:94
                if O00OO000000O000OO !=200 :#line:95
                    await asyncio .sleep (3 )#line:96
                    if num >3 :#line:97
                        O0OOOO00O000O0O0O .log .warning (f'{O00OO000000O000OO}:状态超出3次')#line:98
                        return False ,False ,False #line:99
                    O0OOOO00O000O0O0O .log .debug (f'{O00OO000000O000OO}:去重试 第{num}次')#line:100
                    return await O0OOOO00O000O0O0O .GET_POST (O0000O0O0OO0O00OO ,num +1 )#line:101
                try :#line:102
                    O0O0OOOOO0O00000O =json .loads (O0O0OO000OOO0O0OO )#line:103
                except :#line:104
                    O0O0OOOOO0O00000O =O0O0OO000OOO0O0OO #line:105
                return O00OO000000O000OO ,O0O0OO000OOO0O0OO ,O0O0OOOOO0O00000O #line:106
        return await O0OOOO00O000O0O0O .retry_with_backoff (O0O00O00O000OOOOO ,3 ,f'GET_POST')#line:108
    async def verify (O00OOOOO0OOOO0O0O ):#line:110
        async def O000O0O00O000000O ():#line:111
            O0O0000OO00O0OOO0 ='https://api.ixu.cc/verify'#line:112
            async with aiohttp .ClientSession ()as OOOO00OO0O0OO000O :#line:113
                async with OOOO00OO0O0OO000O .get (O0O0000OO00O0OOO0 ,data ={'TOKEN':O00OOOOO0OOOO0O0O .token },timeout =3 )as OOOOOO00OO000O000 :#line:114
                    O0O0O00O0O000OOO0 =await OOOOOO00OO000O000 .json ()#line:115
                    if OOOOOO00OO000O000 .status ==200 :#line:116
                        O00OOOOO0OOOO0O0O .verify_result =True #line:117
                        O00OOOOO0OOOO0O0O .log .info (f'认证通过 UserId：{O0O0O00O0O000OOO0["user_id"]}')#line:118
                        return O0O0O00O0O000OOO0 #line:119
                    else :#line:120
                        O00OOOOO0OOOO0O0O .log .error (f"授权未通过:{O0O0O00O0O000OOO0['error']}")#line:121
                        sys .exit ()#line:122
        return await O00OOOOO0OOOO0O0O .retry_with_backoff (O000O0O00O000000O ,3 ,'verify')#line:124
    async def Get_H5st (O0O00O0O0O0OO00OO ,O00O00O0OO00O0OO0 ,OO0OO00O00OOO0OOO ,OO0OOO000OOO0O00O ,O000OOOO00OOOO000 ):#line:126
        if O0O00O0O0O0OO00OO .verify_result !=True :#line:127
            await O0O00O0O0O0OO00OO .verify ()#line:128
        if O0O00O0O0O0OO00OO .verify_result !=True :#line:129
            O0O00O0O0O0OO00OO .log .error ("授权未通过 退出")#line:130
            sys .exit ()#line:131
        OO0O000OOOOOOOO00 ={'method':'','kwargs':{'url':'https://api.ouklc.com/api/h5st','params':{'functionId':O00O00O0OO00O0OO0 ,'body':json .dumps (OO0OOO000OOO0O00O ),'ua':O0O00O0O0O0OO00OO .ua ,'pin':O0O00O0O0O0OO00OO .pt_pin (OO0OO00O00OOO0OOO ),'appId':O000OOOO00OOOO000 }}}#line:144
        OOO0000OO00OOO0OO ,O000O0OOO0OO0000O ,OOOOO000OO0OO0OOO =await O0O00O0O0O0OO00OO .GET_POST (OO0O000OOOOOOOO00 )#line:145
        if OOO0000OO00OOO0OO !=200 :#line:146
            return await O0O00O0O0O0OO00OO .Get_H5st (O00O00O0OO00O0OO0 ,OO0OO00O00OOO0OOO ,OO0OOO000OOO0O00O ,O000OOOO00OOOO000 )#line:147
        OO0O000OOOOOOOO00 ={'method':'post','kwargs':{'url':f'https://api.m.jd.com','headers':{"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"zh-cn","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"api.m.jd.com","Referer":"https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html","Origin":"https://prodev.m.jd.com","Cookie":OO0OO00O00OOO0OOO ,"User-Agent":O0O00O0O0O0OO00OO .ua },'data':OOOOO000OO0OO0OOO ["body"]}}#line:167
        if O0O00O0O0O0OO00OO .proxy :#line:168
            OO0O000OOOOOOOO00 ['kwargs'].update ({'proxy':O0O00O0O0O0OO00OO .proxy })#line:169
        OOO0000OO00OOO0OO ,O000O0OOO0OO0000O ,OOOOO000OO0OO0OOO =await O0O00O0O0O0OO00OO .GET_POST (OO0O000OOOOOOOO00 )#line:170
        return OOOOO000OO0OO0OOO #line:171
    def pt_pin (O0OO00O00O0O00O0O ,O0000O000O0O0OO0O ):#line:173
        try :#line:174
            OOOO0OOO0OO0O0000 =re .compile (r'pt_pin=(.*?);').findall (O0000O000O0O0OO0O )[0 ]#line:175
            OOOO0OOO0OO0O0000 =unquote_plus (OOOO0OOO0OO0O0000 )#line:176
        except IndexError :#line:177
            OOOO0OOO0OO0O0000 =re .compile (r'pin=(.*?);').findall (O0000O000O0O0OO0O )[0 ]#line:178
            OOOO0OOO0OO0O0000 =unquote_plus (OOOO0OOO0OO0O0000 )#line:179
        return OOOO0OOO0OO0O0000 #line:180
    def convert_ms_to_hours_minutes (O00O000O0OOOOO0OO ,O0O0OO0O00OOOOOOO ):#line:182
        OOOO0OOO0O0000O00 =O0O0OO0O00OOOOOOO //1000 #line:183
        OOO00OO00OO0000O0 ,OOOO0OOO0O0000O00 =divmod (OOOO0OOO0O0000O00 ,60 )#line:184
        OOO0OO0OO00000OO0 ,OOO00OO00OO0000O0 =divmod (OOO00OO00OO0000O0 ,60 )#line:185
        return f'{OOO0OO0OO00000OO0}小时{OOO00OO00OO0000O0}分'#line:186
    async def inviteFissionReceive (O000000O00OO0OO0O ,OOOO0OO00O0O00OO0 ,OOOOOO0OOOO0OOO0O ,page =1 ):#line:188
        if O000000O00OO0OO0O .verify_result !=True :#line:189
            await O000000O00OO0OO0O .verify ()#line:190
        if O000000O00OO0OO0O .verify_result !=True :#line:191
            O000000O00OO0OO0O .log .error ("授权未通过 退出")#line:192
            sys .exit ()#line:193
        O00O00000OO0OO0O0 =generate_random_user_agent ()#line:194
        OOO00O0000OO000OO ={'linkId':OOOOOO0OOOO0OOO0O ,}#line:197
        O0O00000O0OO0OO0O =await O000000O00OO0OO0O .Get_H5st ('inviteFissionReceive',OOOO0OO00O0O00OO0 ,OOO00O0000OO000OO ,'b8469')#line:198
        if O0O00000O0OO0OO0O ['success']==False and O0O00000O0OO0OO0O ['errMsg']=='活动太火爆，请稍候重试':#line:199
            O00000O0000O00OOO =f'还差{O000000O00OO0OO0O.leftAmount / O000000O00OO0OO0O.amount}次'if O000000O00OO0OO0O .amount !=0 else '先去助力一次才能计算需要人数'#line:200
            O000000O00OO0OO0O .log .debug (f'没助理了 快去助理吧 {O00000O0000O00OOO}')#line:201
            await O000000O00OO0OO0O .superRedBagList (OOOO0OO00O0O00OO0 ,OOOOOO0OOOO0OOO0O ,page )#line:202
            return False #line:203
        if O0O00000O0OO0OO0O ['success']and O0O00000O0OO0OO0O ['code']==0 :#line:209
            O000000O00OO0OO0O .amount =float (O0O00000O0OO0OO0O ["data"]["receiveList"][0 ]["amount"])#line:210
            O000000O00OO0OO0O .leftAmount =float (O0O00000O0OO0OO0O ["data"]["leftAmount"])#line:211
            O000000O00OO0OO0O .log .info (f'领取中:{O0O00000O0OO0OO0O["data"]["totalAmount"]} 当前:{O0O00000O0OO0OO0O["data"]["amount"]} 获得:{O0O00000O0OO0OO0O["data"]["receiveList"][0]["amount"]} 还差:{O0O00000O0OO0OO0O["data"]["leftAmount"]}元/{O000000O00OO0OO0O.leftAmount / O000000O00OO0OO0O.amount}次 当前进度:{O0O00000O0OO0OO0O["data"]["rate"]}%')#line:213
            if int (O0O00000O0OO0OO0O ["data"]["rate"])==100 :#line:214
                O000000O00OO0OO0O .log .info (f'领取中:{O0O00000O0OO0OO0O["data"]["totalAmount"]} 进度:{O0O00000O0OO0OO0O["data"]["rate"]}% 退出!')#line:215
                await O000000O00OO0OO0O .superRedBagList (OOOO0OO00O0O00OO0 ,OOOOOO0OOOO0OOO0O ,page )#line:216
                return False #line:217
        return True #line:218
    async def apCashWithDraw (O00O0O00O0000000O ,OO0OO00OOOO0O0O0O ,O000000OOOOO0O000 ,OOO0O0OOOO0O00O00 ,OO0OO0OO00OO0OOOO ,O0O0OO0OO0O00O0OO ,O0O00O00O00O0OO0O ):#line:220
        if O00O0O00O0000000O .verify_result !=True :#line:221
            await O00O0O00O0000000O .verify ()#line:222
        if O00O0O00O0000000O .verify_result !=True :#line:223
            O00O0O00O0000000O .log .error ("授权未通过 退出")#line:224
            sys .exit ()#line:225
        O0OOOOOO00OO0O000 =generate_random_user_agent ()#line:226
        OO0O0O00O00O0OOOO =await O00O0O00O0000000O .Get_H5st ("apCashWithDraw",O000000OOOOO0O000 ,{"linkId":OO0OO00OOOO0O0O0O ,"businessSource":"NONE","base":{"id":OOO0O0OOOO0O00O00 ,"business":"fission","poolBaseId":OO0OO0OO00OO0OOOO ,"prizeGroupId":O0O0OO0OO0O00O0OO ,"prizeBaseId":O0O00O00O00O0OO0O ,"prizeType":4 }},'8c6ae')#line:242
        return OO0O0O00O00O0OOOO #line:243
    async def inviteFissionBeforeHome (O0O00O00000O0OOOO ,num =1 ):#line:245
        O00000O00OO0OO0O0 =False #line:246
        for OOOO00O0000O0OO00 in ck :#line:247
            if len (O0O00O00000O0OOOO .power_success )>=num :#line:248
                return await O0O00O00000O0OOOO .inviteFissionReceive (O0O00O00000O0OOOO .cookie ,O0O00O00000O0OOOO .linkId )#line:249
            OO0O0O0O0O00O0O00 =await O0O00O00000O0OOOO .Get_H5st ("inviteFissionBeforeHome",OOOO00O0000O0OO00 ,{'linkId':O0O00O00000O0OOOO .linkId ,"isJdApp":True ,'inviter':O0O00O00000O0OOOO .inviter },'02f8d',)#line:252
            if int (OO0O0O0O0O00O0O00 ['code'])==0 :#line:253
                for O0OO0OO0OOOO0O000 ,O0O00O0O0OO0OOO0O in O0O00O00000O0OOOO .helpResult :#line:254
                    if OO0O0O0O0O00O0O00 ['data']['helpResult']==int (O0OO0OO0OOOO0O000 ):#line:255
                        O00000O00OO0OO0O0 =True #line:256
                        O0O00O00000O0OOOO .log .info (f"Id:{O0O00O00000O0OOOO.linkId[:4] + '****' + O0O00O00000O0OOOO.linkId[-4:]}|助理:{OO0O0O0O0O00O0O00['data']['nickName']}|{OO0O0O0O0O00O0O00['data']['helpResult']}|{O0O00O00000O0OOOO.pt_pin(OOOO00O0000O0OO00)}|{O0O00O0O0OO0OOO0O}")#line:258
                        if OO0O0O0O0O00O0O00 ['data']['helpResult']==1 :#line:259
                            O0O00O00000O0OOOO .power_success .append (OOOO00O0000O0OO00 )#line:260
                        else :#line:261
                            O0O00O00000O0OOOO .power_failure .append (OOOO00O0000O0OO00 )#line:262
                    if not O00000O00OO0OO0O0 :#line:263
                        O0O00O0O0OO0OOO0O ='❌未知状态 (可能是活动未开启！！！)'#line:264
                        O0O00O00000O0OOOO .power_failure .append (OOOO00O0000O0OO00 )#line:265
                        O0O00O00000O0OOOO .log .info (f"Id:{O0O00O00000O0OOOO.linkId[:4] + '****' + O0O00O00000O0OOOO.linkId[-4:]}|助理:{OO0O0O0O0O00O0O00['data']['nickName']}|{OO0O0O0O0O00O0O00['data']['helpResult']}|{O0O00O00000O0OOOO.pt_pin(OOOO00O0000O0OO00)}|{O0O00O0O0OO0OOO0O}")#line:267
            else :#line:268
                O0O00O00000O0OOOO .log .info (f"{O0O00O00000O0OOOO.pt_pin(OOOO00O0000O0OO00)}{OO0O0O0O0O00O0O00['code']} 结果:💔{OO0O0O0O0O00O0O00['errMsg']}")#line:269
    async def superRedBagList (OO0OO0O0OO00O0O0O ,OOO0OO0O000OOOO00 ,O0O00OO0O000OO000 ,OO0OO0O0OO0OOO0OO ):#line:271
        if OO0OO0O0OO00O0O0O .verify_result !=True :#line:272
            await OO0OO0O0OO00O0O0O .verify ()#line:273
        if OO0OO0O0OO00O0O0O .verify_result !=True :#line:274
            OO0OO0O0OO00O0O0O .log .error ("授权未通过 退出")#line:275
            sys .exit ()#line:276
        OO0OOO00OOOOOOOOO =await OO0OO0O0OO00O0O0O .Get_H5st ('superRedBagList',OOO0OO0O000OOOO00 ,{"pageNum":OO0OO0O0OO0OOO0OO ,"pageSize":200 ,"linkId":O0O00OO0O000OO000 ,"business":"fission"},'f2b1d')#line:279
        OO0OO0O0OO00O0O0O .log .info (f"开始提取{OO0OO0O0OO0OOO0OO}页, 共{len(OO0OOO00OOOOOOOOO['data']['items'])}条记录")#line:280
        if not OO0OOO00OOOOOOOOO ['data']['hasMore']:#line:281
            return False #line:282
        for OO0O0OOO0OO00O00O in OO0OOO00OOOOOOOOO ['data']['items']:#line:283
            OOOOO0OO0000O0OOO ,OO0000OO00O0O000O ,OOO000OO0OOO00OO0 ,O000O0OOOOOOO00OO ,OO0OO00000O000OO0 ,OO0OOOO00O0O0O00O ,O0O0O0OOOOO0O0000 ,OOOO0O00O0000O00O ,OO000O0OO0000OO0O =(OO0O0OOO0OO00O00O ['id'],OO0O0OOO0OO00O00O ['amount'],OO0O0OOO0OO00O00O ['prizeType'],OO0O0OOO0OO00O00O ['state'],OO0O0OOO0OO00O00O ['prizeConfigName'],OO0O0OOO0OO00O00O ['prizeGroupId'],OO0O0OOO0OO00O00O ['poolBaseId'],OO0O0OOO0OO00O00O ['prizeBaseId'],OO0O0OOO0OO00O00O ['startTime'])#line:288
            OOOO00O00O00O00OO =True #line:289
            while OOOO00O00O00O00OO :#line:290
                if OOO000OO0OOO00OO0 not in OO0OO0O0OO00O0O0O .rewardType and float (OO0000OO00O0O000O )>1.0 :#line:291
                    OO0OO0O0OO00O0O0O .log .info (f"{OO000O0OO0000OO0O} {OO0000OO00O0O000O}元 {'❌未提现' if OOO000OO0OOO00OO0 == 4 and O000O0OOOOOOO00OO != 3 else '✅已提现'}")#line:292
                    OOOO00O00O00O00OO =False #line:293
                if OOO000OO0OOO00OO0 ==4 and O000O0OOOOOOO00OO !=3 and O000O0OOOOOOO00OO !=4 :#line:294
                    OO0OOO00OOOOOOOOO =await OO0OO0O0OO00O0O0O .apCashWithDraw (O0O00OO0O000OO000 ,OOO0OO0O000OOOO00 ,OOOOO0OO0000O0OOO ,O0O0O0OOOOO0O0000 ,OO0OOOO00O0O0O00O ,OOOO0O00O0000O00O )#line:295
                    if int (OO0OOO00OOOOOOOOO ['data']['status'])==310 :#line:296
                        OO0OO0O0OO00O0O0O .log .info (f"✅{OO0000OO00O0O000O}现金💵 提现成功")#line:297
                        OO0OO0O0OO00O0O0O .successful .append (OO0000OO00O0O000O )#line:298
                        await asyncio .sleep (1 )#line:299
                        OOOO00O00O00O00OO =False #line:300
                    elif int (OO0OOO00OOOOOOOOO ['data']['status'])==50056 or int (OO0OOO00OOOOOOOOO ['data']['status'])==50001 :#line:301
                        OO0OO0O0OO00O0O0O .log .warning (f"❌{OO0000OO00O0O000O}现金💵 重新发起 提现失败:{OO0OOO00OOOOOOOOO['data']['message']}")#line:302
                        await asyncio .sleep (3 )#line:303
                    elif '金额超过自然月上限'in OO0OOO00OOOOOOOOO ['data']['message']:#line:304
                        OO0OO0O0OO00O0O0O .log .info (f"{OO0000OO00O0O000O}现金:{OO0OOO00OOOOOOOOO['data']['message']}:去兑换红包")#line:305
                        OOOO00O00O00O00OO =await OO0OO0O0OO00O0O0O .apRecompenseDrawPrize (O0O00OO0O000OO000 ,OOO0OO0O000OOOO00 ,OOOOO0OO0000O0OOO ,O0O0O0OOOOO0O0000 ,OO0OOOO00O0O0O00O ,OOOO0O00O0000O00O ,OO0000OO00O0O000O )#line:306
                        time .sleep (3 )#line:307
                    else :#line:308
                        OO0OO0O0OO00O0O0O .log .error (f"{OO0000OO00O0O000O}现金 ❌提现错误:{OO0OOO00OOOOOOOOO['data']['status']} {OO0OOO00OOOOOOOOO['data']['message']}")#line:309
                        print (OOO000OO0OOO00OO0 ,O000O0OOOOOOO00OO )#line:310
                        OOOO00O00O00O00OO =False #line:311
                else :#line:312
                    OOOO00O00O00O00OO =False #line:313
        return True #line:314
    async def apRecompenseDrawPrize (O0O0OO0OO00OOOO00 ,OOOO0000000O0O0O0 ,OO0000O00OOOO000O ,O0O0O0O0000000000 ,OOOOOO00O0000000O ,O0OOOOO0OO0OOOOO0 ,OO0O000O0OO0O0000 ,O0O0OOOO0O00000OO ):#line:321
        O0000O00O000000OO =await O0O0OO0OO00OOOO00 .Get_H5st ('apRecompenseDrawPrize',OO0000O00OOOO000O ,{"linkId":OOOO0000000O0O0O0 ,"businessSource":"fission","drawRecordId":O0O0O0O0000000000 ,"business":"fission","poolId":OOOOOO00O0000000O ,"prizeGroupId":O0OOOOO0OO0OOOOO0 ,"prizeId":OO0O000O0OO0O0000 ,},'8c6ae')#line:331
        if O0000O00O000000OO ['success']and int (O0000O00O000000OO ['data']['resCode'])==0 :#line:332
            O0O0OO0OO00OOOO00 .log .info (f"{O0O0OOOO0O00000OO}现金:🧧红包兑换成功")#line:333
            O0O0OO0OO00OOOO00 .cash_redpacket .append (O0O0OOOO0O00000OO )#line:334
            return False #line:335
        else :#line:336
            O0O0OO0OO00OOOO00 .log .info (f"{O0O0OOOO0O00000OO}现金:🧧红包兑换失败 {O0000O00O000000OO}")#line:337
            return True #line:338
    async def Fission_Draw (OO0OO0OOO00O0000O ,OOO00O0OO000O00OO ,OOO0OO0OOO00OOO0O ):#line:340
        OO0OO0OOO00O0000O .log .info (f"****************开始抽奖****************")#line:341
        while True :#line:342
            O0OOOOOO0OOOO00OO =await OO0OO0OOO00O0000O .Get_H5st ('inviteFissionDrawPrize',OOO00O0OO000O00OO ,{"linkId":OOO0OO0OOO00OOO0O },'c02c6')#line:345
            if not O0OOOOOO0OOOO00OO ['success']:#line:347
                if "抽奖次数已用完"in O0OOOOOO0OOOO00OO ['errMsg']:#line:348
                    OO0OO0OOO00O0000O .log .debug (f"⚠️抽奖次数已用完")#line:349
                    break #line:350
                elif "本场活动已结束"in O0OOOOOO0OOOO00OO ['errMsg']:#line:351
                    OO0OO0OOO00O0000O .log .debug (f"⏰本场活动已结束了,快去重新开始吧")#line:352
                    sys .exit ()#line:353
            try :#line:354
                if not O0OOOOOO0OOOO00OO ['success']:#line:355
                    OO0OO0OOO00O0000O .log .warning (f'{O0OOOOOO0OOOO00OO["errMsg"]}')#line:356
                    time .sleep (1 )#line:357
                    continue #line:358
                if int (O0OOOOOO0OOOO00OO ['data']['rewardType'])in OO0OO0OOO00O0000O .rewardType :#line:361
                    OO0OO0OOO00O0000O .log .info (f"获得:{O0OOOOOO0OOOO00OO['data']['prizeValue']}元{OO0OO0OOO00O0000O.rewardType[int(O0OOOOOO0OOOO00OO['data']['rewardType'])]['msg']}")#line:363
                    if int (O0OOOOOO0OOOO00OO ['data']['rewardType'])==2 :#line:364
                        OO0OO0OOO00O0000O .redpacket .append (float (O0OOOOOO0OOOO00OO ['data']['prizeValue']))#line:365
                else :#line:366
                    print (O0OOOOOO0OOOO00OO ['data']['rewardType'])#line:367
                    OO0OO0OOO00O0000O .log .info (f"获得:{O0OOOOOO0OOOO00OO['data']['prizeValue']}元现金💵")#line:368
                    OO0OO0OOO00O0000O .cash .append (float (O0OOOOOO0OOOO00OO ['data']['prizeValue']))#line:369
            except Exception as O00OOOOOOO00OO0OO :#line:370
                OO0OO0OOO00O0000O .log .error (f'(未知物品):{O0OOOOOO0OOOO00OO}')#line:371
            await asyncio .sleep (0.3 )#line:372
        OO0OO0OOO00O0000O .log .info (f"抽奖结束: 💵现金:{'{:.2f}'.format(sum([float(O0OO0OOOO000OOOOO) for O0OO0OOOO000OOOOO in OO0OO0OOO00O0000O.cash]))}元, 🧧红包:{'{:.2f}'.format(sum([float(OO0OOOOO000OOOOOO) for OO0OOOOO000OOOOOO in OO0OO0OOO00O0000O.redpacket]))}元")#line:374
        OO0OO0OOO00O0000O .log .info (f"****************开始提现****************")#line:375
        OO0O0OOOO0OO0O000 =0 #line:376
        while True :#line:377
            OO0O0OOOO0OO0O000 =OO0O0OOOO0OO0O000 +1 #line:378
            OO0OO0OO00OOOOOO0 =await OO0OO0OOO00O0000O .superRedBagList (OOO00O0OO000O00OO ,OOO0OO0OOO00OOO0O ,OO0O0OOOO0OO0O000 )#line:379
            await asyncio .sleep (2 )#line:380
            if OO0O0OOOO0OO0O000 >=OO0OO0OOO00O0000O .page :#line:381
                break #line:382
            if not OO0OO0OO00OOOOOO0 :#line:383
                break #line:384
        OOOO0O00O0O0OOO00 =('提现结束: ')+(f"💵现金:{'{:.2f}'.format(sum([float(O0O0O000O0OOO0O0O) for O0O0O000O0OOO0O0O in OO0OO0OOO00O0000O.successful]))}元/")+(f"🧧兑换红包:{'{:.2f}'.format(sum([float(O0O0000O0O00OOO0O) for O0O0000O0O00OOO0O in OO0OO0OOO00O0000O.cash_redpacket]))}元/共计红包:{'{:.2f}'.format(sum([float(O00O00OO00O0O0000) for O00O00OO00O0O0000 in OO0OO0OOO00O0000O.redpacket + OO0OO0OOO00O0000O.cash_redpacket]))}")#line:390
        if not OO0OO0OOO00O0000O .successful and not OO0OO0OOO00O0000O .cash_redpacket :#line:391
            OOOO0O00O0O0OOO00 ='提现结束: 一毛都没有哦！'#line:392
        OO0OO0OOO00O0000O .log .info (OOOO0O00O0O0OOO00 )#line:393
    async def add_LinkId (OO00OOO0OOOO00O00 ):#line:395
        async def OOOO0OOO00O0000O0 ():#line:396
            if OO00OOO0OOOO00O00 .verify_result !=True :#line:397
                await OO00OOO0OOOO00O00 .verify ()#line:398
            if OO00OOO0OOOO00O00 .verify_result !=True :#line:399
                OO00OOO0OOOO00O00 .log .error ("授权未通过 退出")#line:400
                sys .exit ()#line:401
            OOO000O0O00O0000O ='https://api.ixu.cc/status/inviter.json'#line:402
            async with aiohttp .ClientSession ()as OO0OOO0O0O0OOOOO0 :#line:403
                async with OO0OOO0O0O0OOOOO0 .get (OOO000O0O00O0000O ,timeout =5 )as OOO0O0OOOOO000000 :#line:404
                    if OOO0O0OOOOO000000 .status ==200 :#line:405
                        OO00O0OOOO00OO0O0 =await OOO0O0OOOOO000000 .json ()#line:406
                        if OO00O0OOOO00OO0O0 ['stats']!='True':#line:407
                            OO00OOO0OOOO00O00 .log .error (f"{OO00O0OOOO00OO0O0['err_text']}")#line:408
                            sys .exit ()#line:409
                        OO00OOO0OOOO00O00 .inviter_help =OO00O0OOOO00OO0O0 ['inviter']#line:410
                        if len (OO00O0OOOO00OO0O0 ['text'])>0 :#line:411
                            OO00OOO0OOOO00O00 .log .debug (f'那女孩对你说:{OO00O0OOOO00OO0O0["text"]}')#line:412
                        if OO00OOO0OOOO00O00 .scode =='ALL'or OO00OOO0OOOO00O00 .scode =='all':#line:413
                            for OO0O0O00O0OOOOO00 in OO00O0OOOO00OO0O0 ['linkId']:#line:414
                                OO00OOO0OOOO00O00 .linkId .append (OO0O0O00O0OOOOO00 )#line:415
                                OO00OOO0OOOO00O00 .log .info (f'云端获取到linkId:{OO0O0O00O0OOOOO00}')#line:416
                            return True #line:417
                        else :#line:418
                            OO00OOO0OOOO00O00 .linkId .append (OO00O0OOOO00OO0O0 ['linkId'][int (OO00OOO0OOOO00O00 .scode )-1 ])#line:419
                            OO00OOO0OOOO00O00 .log .info (f'云端获取到linkId:{OO00O0OOOO00OO0O0["linkId"][int(OO00OOO0OOOO00O00.scode) - 1]}')#line:420
                            return True #line:421
                    else :#line:422
                        OO00OOO0OOOO00O00 .log .error ('未获取到linkId 重试')#line:423
        return await OO00OOO0OOOO00O00 .retry_with_backoff (OOOO0OOO00O0000O0 ,3 ,'linkId')#line:425
    async def task_start (O0O0OOO0OO00000OO ):#line:427
        if O0O0OOO0OO00000OO .verify_result !=True :#line:428
            await O0O0OOO0OO00000OO .verify ()#line:429
        if O0O0OOO0OO00000OO .verify_result !=True :#line:430
            O0O0OOO0OO00000OO .log .error ("授权未通过 退出")#line:431
            sys .exit ()#line:432
        await O0O0OOO0OO00000OO .add_LinkId ()#line:433
        O0OOO00OOOO0OO000 =O0O0OOO0OO00000OO .cookie #line:436
        if O0O0OOO0OO00000OO .txj_status :#line:437
            try :#line:438
                O000000OOO00OO000 =await O0O0OOO0OO00000OO .Get_H5st ('inviteFissionHome',O0OOO00OOOO0OO000 ,{'linkId':O0O0OOO0OO00000OO .linkId [0 ],"inviter":"",},'eb67b')#line:440
                if not O000000OOO00OO000 ['success']and O000000OOO00OO000 ['errMsg']=='未登录':#line:442
                    O0O0OOO0OO00000OO .log .error (f"{O000000OOO00OO000['errMsg']}")#line:443
                    return #line:444
                OO0000OOOOO0000O0 =O000000OOO00OO000 ['data']#line:445
                if OO0000OOOOO0000O0 ['cashVo']!=None :#line:446
                    OO000O00OOO0OOO00 =OO0000OOOOO0000O0 ['cashVo']#line:447
                    O0O0OOO0OO00000OO .log .info (f"Name:{OO000O00OOO0OOO00['userInfo']['nickName']} 已助理:{OO0000OOOOO0000O0['prizeNum'] + OO0000OOOOO0000O0['drawPrizeNum']} 提现:{OO000O00OOO0OOO00['totalAmount']}元 当前:{OO000O00OOO0OOO00['amount']}元 进度{OO000O00OOO0OOO00['rate']}% 剩余时间:{O0O0OOO0OO00000OO.convert_ms_to_hours_minutes(OO0000OOOOO0000O0['countDownTime'])}")#line:449
                    if int (OO000O00OOO0OOO00 ['rate'])==100 :#line:450
                        O0O0OOO0OO00000OO .log .info (f"本轮您已提现{OO000O00OOO0OOO00['totalAmount']}元了 等{O0O0OOO0OO00000OO.convert_ms_to_hours_minutes(OO0000OOOOO0000O0['countDownTime'])}后在来吧")#line:452
                        await O0O0OOO0OO00000OO .superRedBagList (O0OOO00OOOO0OO000 ,O0O0OOO0OO00000OO .linkId [0 ],1 )#line:453
                        return #line:454
                else :#line:455
                    O0O0OOO0OO00000OO .log .error ('哦和 黑号了哦')#line:456
                while True :#line:458
                    OOO0OOO0000000OO0 =await O0O0OOO0OO00000OO .inviteFissionReceive (O0OOO00OOOO0OO000 ,O0O0OOO0OO00000OO .linkId [0 ])#line:459
                    time .sleep (0.3 )#line:462
            except Exception as O0OO000OO000OO0O0 :#line:463
                O0O0OOO0OO00000OO .log .error ('黑号')#line:464
        else :#line:465
            for O000OO000O00O0O00 in O0O0OOO0OO00000OO .linkId :#line:466
                O0O0OOO0OO00000OO .log .info (f'开始执行 LinkId:{O000OO000O00O0O00}')#line:467
                await O0O0OOO0OO00000OO .Fission_Draw (O0OOO00OOOO0OO000 ,O000OO000O00O0O00 )#line:468
if __name__ =='__main__':#line:471
    pdd =TEN_JD_PDD_DRAW ()#line:472
    loop =asyncio .get_event_loop ()#line:473
    loop .run_until_complete (pdd .task_start ())#line:474
    loop .close ()#line:475
