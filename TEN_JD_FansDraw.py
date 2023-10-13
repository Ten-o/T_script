# -*- coding: utf-8 -*-
"""
File: TEN_JD_PDD.py(宠粉抽奖)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('宠粉抽奖');
"""

import asyncio ,aiohttp ,re ,os ,sys ,threading ,concurrent .futures ,time ,json ,datetime #line:8
from utils .jdCookie import get_cookies #line:9
from utils .logger import setup_logger #line:10
from fake_useragent import UserAgent #line:11
try :#line:13
    ck =get_cookies ()#line:14
    if not ck :#line:15
        sys .exit ()#line:16
except :#line:17
    print ("未获取到有效COOKIE,退出程序！")#line:18
    sys .exit ()#line:19
class TEN_JD_FansDraw :#line:22
    def __init__ (O00OOOO00OO0OO0O0 ):#line:23
        O00OOOO00OO0OO0O0 .ua =UserAgent ()#line:24
        O00OOOO00OO0OO0O0 .semaphore =asyncio .Semaphore (int (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 20 ))#line:25
        O00OOOO00OO0OO0O0 .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:26
        O00OOOO00OO0OO0O0 .log =setup_logger ()#line:27
        O00OOOO00OO0OO0O0 .headers ={'Content-Type':'application/x-www-form-urlencoded','Connection':'keep-alive','Accept':'*/*','Referer':'https://service.vapp.jd.com/3CCA5269C1CA14CA76B9955243C60F78/1/page-frame.html','Host':'api.m.jd.com','Accept-Encoding':'gzip, deflate, br','Accept-Language':'zh-CN,zh-Hans;q=0.9'}#line:36
    async def retry_with_backoff (O0O0O0000O0O00OO0 ,OOOOO0OOOO00OO0OO ,OOO00O00O0O0O0OO0 ,OOO00OOOO0OOO000O ,backoff_seconds =1 ):#line:38
        for OO0OO0OOO0OOOOOO0 in range (OOO00O00O0O0O0OO0 ):#line:39
            try :#line:40
                return await OOOOO0OOOO00OO0OO ()#line:41
            except asyncio .TimeoutError :#line:42
                O0O0O0000O0O00OO0 .log .debug (f'第{OO0OO0OOO0OOOOOO0 + 1}次重试  {OOO00OOOO0OOO000O} 请求超时')#line:43
                await asyncio .sleep (backoff_seconds )#line:44
            except Exception as O0O0OOOOO0OO0O00O :#line:45
                O0O0O0000O0O00OO0 .log .debug (f'第{OO0OO0OOO0OOOOOO0 + 1}次重试 {OOO00OOOO0OOO000O}出错：{O0O0OOOOO0OO0O00O}')#line:46
                await asyncio .sleep (backoff_seconds )#line:47
                if OO0OO0OOO0OOOOOO0 ==OOO00O00O0O0O0OO0 :#line:48
                    O0O0O0000O0O00OO0 .log .error (f'{OOO00OOOO0OOO000O}重试{OOO00O00O0O0O0OO0}次后仍然发生异常')#line:49
                    return #line:50
    async def GET_POST (OOO0O0OO00000OOOO ,O0O0OO000O00O00O0 ):#line:52
        async def O0000000O0O0OO000 ():#line:53
            async with aiohttp .ClientSession ()as O00000O00OO00O00O :#line:54
                if O0O0OO000O00O00O0 ['method']=='get':#line:55
                    async with O00000O00OO00O00O .get (**O0O0OO000O00O00O0 ['kwargs'])as OO0O00OOO0O0O0000 :#line:56
                        O0OOOOOOOOO0OO0OO =OO0O00OOO0O0O0000 .status #line:57
                        OOO0OOOO00OO0O00O =await OO0O00OOO0O0O0000 .text ()#line:58
                else :#line:59
                    async with O00000O00OO00O00O .post (**O0O0OO000O00O00O0 ['kwargs'])as OO0O00OOO0O0O0000 :#line:60
                        O0OOOOOOOOO0OO0OO =OO0O00OOO0O0O0000 .status #line:61
                        OOO0OOOO00OO0O00O =await OO0O00OOO0O0O0000 .text ()#line:62
                if O0OOOOOOOOO0OO0OO !=200 :#line:63
                    OOO0O0OO00000OOOO .log .debug (f'{O0OOOOOOOOO0OO0OO}:去重试')#line:64
                    return await OOO0O0OO00000OOOO .GET_POST (O0O0OO000O00O00O0 )#line:65
                try :#line:66
                    O000O0O0O0OO0OO0O =json .loads (OOO0OOOO00OO0O00O )#line:67
                except :#line:68
                    O000O0O0O0OO0OO0O =OOO0OOOO00OO0O00O #line:69
                return O0OOOOOOOOO0OO0OO ,OOO0OOOO00OO0O00O ,O000O0O0O0OO0OO0O #line:70
        return await OOO0O0OO00000OOOO .retry_with_backoff (O0000000O0O0OO000 ,3 ,f'GET_POST')#line:72
    async def Api_Jd_Com (O000OO00OO0OO0O0O ,O0O000O00O00O0OO0 ,OO000OO0OO0OO0O0O ):#line:74
        O000OO00OO0OO0O0O .headers ['User-Agent']=O000OO00OO0OO0O0O .ua .safari #line:75
        O000OO00OO0OO0O0O .headers ['Cookie']=O0O000O00O00O0OO0 #line:76
        OOOO0OOOO00O0OO0O ={'method':'post','kwargs':{'url':'https://api.m.jd.com/client.action','headers':O000OO00OO0OO0O0O .headers ,'data':OO000OO0OO0OO0O0O }}#line:84
        if O000OO00OO0OO0O0O .proxy :#line:85
            OOOO0OOOO00O0OO0O ['kwargs'].update ({'proxy':O000OO00OO0OO0O0O .proxy })#line:86
        OO0O0O0O0O0000O00 ,O000OO000OO000OO0 ,OOO0OOO0OOOOOO00O =await O000OO00OO0OO0O0O .GET_POST (OOOO0OOOO00O0OO0O )#line:87
        return OO0O0O0O0O0000O00 ,O000OO000OO000OO0 ,OOO0OOO0OOOOOO00O #line:88
    async def MainInfo (OOOO0O0O0O0O00OO0 ,O0OOO00000OO0O000 ,O000OO0OOOO00OOOO ):#line:90
        OO0OO0OO0OOOO0000 ='functionId=jm_marketing_maininfo&body=%7B%22shopId%22%3A%2212765935%22%2C%22venderId%22%3A%2213577546%22%2C%22projectId%22%3A358620%7D&t=1697155128683&eid=eidIde5c812183sbwkZEkK6%2FTCezMUyGy3rdu8JGRgfcBCAt40UcQi3vl8KucZUDXY9IDHh3YGNPj%2BnDWMIUs19jQaju%2FLkzCeIe030URPX5cdlBMNhF&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=70492ed7d2e0f3c29baa49e8f4a45a3812d922a3'#line:91
        OOO000O0O0OO0OO0O ,O0OO0O0000OOOOOOO ,O0O0O0OO000OOOOOO =await OOOO0O0O0O0O00OO0 .Api_Jd_Com (O000OO0OOOO00OOOO ,OO0OO0OO0OOOO0000 )#line:92
        if OOO000O0O0OO0OO0O !=200 :#line:93
            OOOO0O0O0O0O00OO0 .log .error ("请手动确认活动")#line:94
        try :#line:95
            OOO0OOOOO0O0OOOO0 =O0O0O0OO000OOOOOO ['data']['project']['viewTaskVOS']#line:96
        except Exception as O0O000OO0O0O0O0O0 :#line:97
            return #line:98
        O00O0OO0O0O000O00 =datetime .datetime .now ().timestamp ()#line:101
        if O00O0OO0O0O000O00 >1698249599000 /1000 :#line:102
            OOOO0O0O0O0O00OO0 .log .error ("活动已结束")#line:103
            return #line:104
        OOOO0O0O0O0O00OO0 .log .info (f"第{O0OOO00000OO0O000}个号 去关注店铺")#line:105
        OO0OO0OO0OOOO0000 ='functionId=followShop&body=%7B%22shopId%22%3A%2212765935%22%2C%22follow%22%3Atrue%2C%22type%22%3A0%2C%22sourceRpc%22%3A%22shop_app_myfollows_shop%22%2C%22refer%22%3A%22https%3A%2F%2Fwq.jd.com%2Fpages%2Findex%2Findex%22%7D&t=1697113701851&eid=eidIde5c812183sbwkZEkK6%2FTCezMUyGy3rdu8JGRgfcBCAt40UcQi3vl8KucZUDXY9IDHh3YGNPj%2BnDWMIUs19jQaju%2FLkzCeIe030URPX5cdlBMNhF&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=70492ed7d2e0f3c29baa49e8f4a45a3812d922a3'#line:106
        OOO000O0O0OO0OO0O ,O0OO0O0000OOOOOOO ,O0O0O0OO000OOOOOO =await OOOO0O0O0O0O00OO0 .Api_Jd_Com (O000OO0OOOO00OOOO ,OO0OO0OO0OOOO0000 )#line:107
        for OO0OOOOOO0O0O00OO in OOO0OOOOO0O0OOOO0 :#line:108
            if OO0OOOOOO0O0O00OO ['type']in [2 ,4 ]and OO0OOOOOO0O0O00OO ['finishCount']==0 :#line:109
                OO0OO0OO0OOOO0000 =f'functionId=jm_task_process&body=%7B%22shopId%22%3A%2212765935%22%2C%22venderId%22%3A%2213577546%22%2C%22projectId%22%3A358620%2C%22taskId%22%3A{OO0OOOOOO0O0O00OO["id"]}%2C%22token%22%3A%22{OO0OOOOOO0O0O00OO["token"]}%22%2C%22opType%22%3A2%2C%22referSource%22%3A10084096558196%7D&t=1697113686255&eid=eidIde5c812183sbwkZEkK6%2FTCezMUyGy3rdu8JGRgfcBCAt40UcQi3vl8KucZUDXY9IDHh3YGNPj%2BnDWMIUs19jQaju%2FLkzCeIe030URPX5cdlBMNhF&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=70492ed7d2e0f3c29baa49e8f4a45a3812d922a3'#line:110
                OOO000O0O0OO0OO0O ,O0OO0O0000OOOOOOO ,O0O0O0OO000OOOOOO =await OOOO0O0O0O0O00OO0 .Api_Jd_Com (O000OO0OOOO00OOOO ,OO0OO0OO0OOOO0000 )#line:111
                if isinstance (O0O0O0OO000OOOOOO ,dict )and O0O0O0OO000OOOOOO .get ('success')and isinstance (O0OO0O0000OOOOOOO ,dict )and int (O0OO0O0000OOOOOOO .get ('code'))==810 :#line:112
                    OOOO0O0O0O0O00OO0 .log .info ('加购成功')#line:113
                OO0OO0OO0OOOO0000 =f'functionId=jm_task_process&body=%7B%22shopId%22%3A%2212765935%22%2C%22venderId%22%3A%2213577546%22%2C%22projectId%22%3A%22358620%22%2C%22taskId%22%3A{OO0OOOOOO0O0O00OO["id"]}%2C%22token%22%3A%22{OO0OOOOOO0O0O00OO["token"]}%22%2C%22opType%22%3A1%7D&t=1697184247624&eid=eidIa5c68120d7sfY99PKHwxTOyB1RlGTgCZBGPfUKTz5feUoC%2FDD%2FjdN%2BC0r%2FtF%2Bh%2F6lGZVL8mAQ8uwgybpEbZ4oL7RkLBJv4tF%2FWjF%2FTw3Nn%2FRR3dh&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=d3cbfc4ea3604057234b4257433ef5bc586d1f2c'#line:114
                OOO000O0O0OO0OO0O ,O0OO0O0000OOOOOOO ,O0O0O0OO000OOOOOO =await OOOO0O0O0O0O00OO0 .Api_Jd_Com (O000OO0OOOO00OOOO ,OO0OO0OO0OOOO0000 )#line:115
        O0OOO0OOO00OOOO0O =[O00OO000OO0OOO0OO ['token']for O00OO000OO0OOO0OO in OOO0OOOOO0O0OOOO0 if "抽奖"in O00OO000OO0OOO0OO ['name']][0 ]#line:116
        O0000O0O0000OO00O =[O0O000OOO0OOOOO0O ['id']for O0O000OOO0OOOOO0O in OOO0OOOOO0O0OOOO0 if "抽奖"in O0O000OOO0OOOOO0O ['name']][0 ]#line:117
        while True :#line:118
                OO0OO0OO0OOOO0000 =f'functionId=jm_task_process&body=%7B%22shopId%22%3A%2212765935%22%2C%22venderId%22%3A%2213577546%22%2C%22projectId%22%3A358620%2C%22taskId%22%3A{O0000O0O0000OO00O}%2C%22token%22%3A%22{O0OOO0OOO00OOOO0O}%22%2C%22opType%22%3A2%2C%22referSource%22%3A10084096558196%7D&t=1697113686255&eid=eidIde5c812183sbwkZEkK6%2FTCezMUyGy3rdu8JGRgfcBCAt40UcQi3vl8KucZUDXY9IDHh3YGNPj%2BnDWMIUs19jQaju%2FLkzCeIe030URPX5cdlBMNhF&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=70492ed7d2e0f3c29baa49e8f4a45a3812d922a3'#line:120
                OOO000O0O0OO0OO0O ,O0OO0O0000OOOOOOO ,O0O0O0OO000OOOOOO =await OOOO0O0O0O0O00OO0 .Api_Jd_Com (O000OO0OOOO00OOOO ,OO0OO0OO0OOOO0000 )#line:121
                if not O0O0O0OO000OOOOOO ['success']and O0O0O0OO000OOOOOO ['code']==300 :#line:123
                    break #line:124
                if O0O0O0OO000OOOOOO .get ('msg')is not None and "宠粉币数量不足"in O0O0O0OO000OOOOOO ['msg']:#line:125
                    OOOO0O0O0O0O00OO0 .log .debug (f"第{O0OOO00000OO0O000}个号 {O0O0O0OO000OOOOOO['msg']}")#line:126
                    break #line:127
                OO0OO00O00OO0O0OO =O0O0O0OO000OOOOOO ['data']['awardVO']#line:129
                if OO0OO00O00OO0O0OO is None :#line:130
                    OOOO0O0O0O0O00OO0 .log .info (f"第{O0OOO00000OO0O000}个号 剩余{O0O0O0OO000OOOOOO['data']['fansCoin']}次: {O0O0O0OO000OOOOOO['data']['pin']}:空气")#line:131
                    continue #line:132
                OOOOOOO000OO00000 =OO0OO00O00OO0O0OO ['discount']+OO0OO00O00OO0O0OO ['name']#line:133
                OOOO0O0O0O0O00OO0 .log .info (f"第{O0OOO00000OO0O000}个号 剩余{O0O0O0OO000OOOOOO['data']['fansCoin']}次: {O0O0O0OO000OOOOOO['data']['pin']}:{OOOOOOO000OO00000}")#line:134
                if OO0OO00O00OO0O0OO ['type']==1 :#line:135
                    break #line:136
    async def start (O00000O0O0O000000 ,):#line:138
        O0OO00000000OOOO0 =[]#line:139
        if O00000O0O0O000000 .proxy :#line:141
            O00000O0O0O000000 .log .info (f'[并发执行 线程:{O00000O0O0O000000.semaphore._value}]')#line:142
            async def OOOOO0O00O0O0O0O0 (OO000OO000000O0O0 ,OOO0O000O0OOOOO0O ):#line:143
                async with O00000O0O0O000000 .semaphore :#line:144
                    O0OOOO00O0O000O00 =asyncio .create_task (O00000O0O0O000000 .MainInfo (OO000OO000000O0O0 ,OOO0O000O0OOOOO0O ))#line:145
                    return await O0OOOO00O0O000O00 #line:146
            for OO0O0O0OOOOOO00OO ,OO0OOO000OO0OOOOO in enumerate (ck ,1 ):#line:148
                OO0O000OOO0O0O00O =asyncio .create_task (OOOOO0O00O0O0O0O0 (OO0O0O0OOOOOO00OO ,OO0OOO000OO0OOOOO ))#line:149
                O0OO00000000OOOO0 .append (OO0O000OOO0O0O00O )#line:150
            await asyncio .gather (*O0OO00000000OOOO0 )#line:152
        else :#line:153
            O00000O0O0O000000 .log .info (f'[非并发执行]')#line:154
            for OO0O0O0OOOOOO00OO ,OO0OOO000OO0OOOOO in enumerate (ck ,1 ):#line:155
                await O00000O0O0O000000 .MainInfo (OO0O0O0OOOOOO00OO ,OO0OOO000OO0OOOOO )#line:156
if __name__ =='__main__':#line:161
    FD =TEN_JD_FansDraw ()#line:162
    loop =asyncio .get_event_loop ()#line:163
    loop .run_until_complete (FD .start ())#line:164
    loop .close ()#line:165
