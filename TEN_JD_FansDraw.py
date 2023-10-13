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
    def __init__ (O00OO00OO0O000O0O ):#line:23
        O00OO00OO0O000O0O .ua =UserAgent ()#line:24
        O00OO00OO0O000O0O .semaphore =asyncio .Semaphore (int (os .environ .get ("TEN_threadsNum")if os .environ .get ("TEN_threadsNum")else 20 ))#line:25
        O00OO00OO0O000O0O .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:26
        O00OO00OO0O000O0O .log =setup_logger ()#line:27
        O00OO00OO0O000O0O .headers ={'Content-Type':'application/x-www-form-urlencoded','Connection':'keep-alive','Accept':'*/*','Referer':'https://service.vapp.jd.com/3CCA5269C1CA14CA76B9955243C60F78/1/page-frame.html','Host':'api.m.jd.com','Accept-Encoding':'gzip, deflate, br','Accept-Language':'zh-CN,zh-Hans;q=0.9'}#line:36
    async def retry_with_backoff (OOOO00O00OO0OOOOO ,OOOO00OOOOO0O0000 ,OOOOOOOOOO0OO0O00 ,O0O0OO0O0O0OOO000 ,backoff_seconds =1 ):#line:38
        for OO00000OO000OO0OO in range (OOOOOOOOOO0OO0O00 ):#line:39
            try :#line:40
                return await OOOO00OOOOO0O0000 ()#line:41
            except asyncio .TimeoutError :#line:42
                OOOO00O00OO0OOOOO .log .debug (f'第{OO00000OO000OO0OO + 1}次重试  {O0O0OO0O0O0OOO000} 请求超时')#line:43
                await asyncio .sleep (backoff_seconds )#line:44
            except Exception as O00O00O0OO0O0000O :#line:45
                OOOO00O00OO0OOOOO .log .debug (f'第{OO00000OO000OO0OO + 1}次重试 {O0O0OO0O0O0OOO000}出错：{O00O00O0OO0O0000O}')#line:46
                await asyncio .sleep (backoff_seconds )#line:47
                if OO00000OO000OO0OO ==OOOOOOOOOO0OO0O00 :#line:48
                    OOOO00O00OO0OOOOO .log .error (f'{O0O0OO0O0O0OOO000}重试{OOOOOOOOOO0OO0O00}次后仍然发生异常')#line:49
                    return #line:50
    async def GET_POST (O00OO0O00OOO00O0O ,O000OO0OOO000O000 ):#line:52
        async def OO0OOO00OO0O0O0O0 ():#line:53
            async with aiohttp .ClientSession ()as O0OO0OO0OOO00000O :#line:54
                if O000OO0OOO000O000 ['method']=='get':#line:55
                    async with O0OO0OO0OOO00000O .get (**O000OO0OOO000O000 ['kwargs'])as OOO000OOO0000O0OO :#line:56
                        OO000O0O00000O0OO =OOO000OOO0000O0OO .status #line:57
                        OO0O0O0OO0OO0OO00 =await OOO000OOO0000O0OO .text ()#line:58
                else :#line:59
                    async with O0OO0OO0OOO00000O .post (**O000OO0OOO000O000 ['kwargs'])as OOO000OOO0000O0OO :#line:60
                        OO000O0O00000O0OO =OOO000OOO0000O0OO .status #line:61
                        OO0O0O0OO0OO0OO00 =await OOO000OOO0000O0OO .text ()#line:62
                if OO000O0O00000O0OO !=200 :#line:63
                    O00OO0O00OOO00O0O .log .debug (f'{OO000O0O00000O0OO}:去重试')#line:64
                    return await O00OO0O00OOO00O0O .GET_POST (O000OO0OOO000O000 )#line:65
                try :#line:66
                    O0O00O0O000000OOO =json .loads (OO0O0O0OO0OO0OO00 )#line:67
                except :#line:68
                    O0O00O0O000000OOO =OO0O0O0OO0OO0OO00 #line:69
                return OO000O0O00000O0OO ,OO0O0O0OO0OO0OO00 ,O0O00O0O000000OOO #line:70
        return await O00OO0O00OOO00O0O .retry_with_backoff (OO0OOO00OO0O0O0O0 ,3 ,f'GET_POST')#line:72
    async def Api_Jd_Com (O000OO000OO0O0OO0 ,O0OO0O000O00O000O ,O0OO0OO0O0000O0OO ):#line:74
        O000OO000OO0O0OO0 .headers ['User-Agent']=O000OO000OO0O0OO0 .ua .safari #line:75
        O000OO000OO0O0OO0 .headers ['Cookie']=O0OO0O000O00O000O #line:76
        O00O00O00O0O0OO00 ={'method':'post','kwargs':{'url':'https://api.m.jd.com/client.action','headers':O000OO000OO0O0OO0 .headers ,'data':O0OO0OO0O0000O0OO }}#line:84
        if O000OO000OO0O0OO0 .proxy :#line:85
            O00O00O00O0O0OO00 ['kwargs'].update ({'proxy':O000OO000OO0O0OO0 .proxy })#line:86
        O00O00OO0OOOO000O ,O0O0O000O00O00000 ,O00000O0OOOOOO00O =await O000OO000OO0O0OO0 .GET_POST (O00O00O00O0O0OO00 )#line:87
        return O00O00OO0OOOO000O ,O0O0O000O00O00000 ,O00000O0OOOOOO00O #line:88
    async def MainInfo (OO00OO0000O0000OO ,O0O0OOO0000O000OO ,O000O00O000OOO0O0 ):#line:90
        OO0O0OOOOO00O0O0O ='functionId=jm_marketing_maininfo&body=%7B%22shopId%22%3A%2212765935%22%2C%22venderId%22%3A%2213577546%22%2C%22projectId%22%3A358620%7D&t=1697155128683&eid=eidIde5c812183sbwkZEkK6%2FTCezMUyGy3rdu8JGRgfcBCAt40UcQi3vl8KucZUDXY9IDHh3YGNPj%2BnDWMIUs19jQaju%2FLkzCeIe030URPX5cdlBMNhF&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=70492ed7d2e0f3c29baa49e8f4a45a3812d922a3'#line:91
        OO00O0000000OO00O ,OOO00O00O00OOO000 ,OO0000O000000OO0O =await OO00OO0000O0000OO .Api_Jd_Com (O000O00O000OOO0O0 ,OO0O0OOOOO00O0O0O )#line:92
        if OO00O0000000OO00O !=200 :#line:93
            OO00OO0000O0000OO .log .error ("请手动确认活动")#line:94
        try :#line:95
            O0O000OO00OO00O0O =OO0000O000000OO0O ['data']['project']['viewTaskVOS']#line:96
        except Exception as OO00O000OOOO0OOOO :#line:97
            return #line:98
        OO00OO000O0O00OOO =datetime .datetime .now ().timestamp ()#line:101
        if OO00OO000O0O00OOO >1698249599000 /1000 :#line:102
            OO00OO0000O0000OO .log .error ("活动已结束")#line:103
            return #line:104
        OO00OO0000O0000OO .log .info (f"第{O0O0OOO0000O000OO}个号 去关注店铺")#line:105
        OO0O0OOOOO00O0O0O ='functionId=followShop&body=%7B%22shopId%22%3A%2212765935%22%2C%22follow%22%3Atrue%2C%22type%22%3A0%2C%22sourceRpc%22%3A%22shop_app_myfollows_shop%22%2C%22refer%22%3A%22https%3A%2F%2Fwq.jd.com%2Fpages%2Findex%2Findex%22%7D&t=1697113701851&eid=eidIde5c812183sbwkZEkK6%2FTCezMUyGy3rdu8JGRgfcBCAt40UcQi3vl8KucZUDXY9IDHh3YGNPj%2BnDWMIUs19jQaju%2FLkzCeIe030URPX5cdlBMNhF&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=70492ed7d2e0f3c29baa49e8f4a45a3812d922a3'#line:106
        OO00O0000000OO00O ,OOO00O00O00OOO000 ,OO0000O000000OO0O =await OO00OO0000O0000OO .Api_Jd_Com (O000O00O000OOO0O0 ,OO0O0OOOOO00O0O0O )#line:107
        for O0O0OOO0000000O00 in O0O000OO00OO00O0O :#line:108
            if O0O0OOO0000000O00 ['type']in [2 ,4 ]and O0O0OOO0000000O00 ['finishCount']==0 :#line:109
                OO0O0OOOOO00O0O0O =f'functionId=jm_task_process&body=%7B%22shopId%22%3A%2212765935%22%2C%22venderId%22%3A%2213577546%22%2C%22projectId%22%3A358620%2C%22taskId%22%3A{O0O0OOO0000000O00["id"]}%2C%22token%22%3A%22{O0O0OOO0000000O00["token"]}%22%2C%22opType%22%3A2%2C%22referSource%22%3A10084096558196%7D&t=1697113686255&eid=eidIde5c812183sbwkZEkK6%2FTCezMUyGy3rdu8JGRgfcBCAt40UcQi3vl8KucZUDXY9IDHh3YGNPj%2BnDWMIUs19jQaju%2FLkzCeIe030URPX5cdlBMNhF&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=70492ed7d2e0f3c29baa49e8f4a45a3812d922a3'#line:110
                OO00O0000000OO00O ,OOO00O00O00OOO000 ,OO0000O000000OO0O =await OO00OO0000O0000OO .Api_Jd_Com (O000O00O000OOO0O0 ,OO0O0OOOOO00O0O0O )#line:111
                if isinstance (OO0000O000000OO0O ,dict )and OO0000O000000OO0O .get ('success')and isinstance (OOO00O00O00OOO000 ,dict )and int (OOO00O00O00OOO000 .get ('code'))==810 :#line:112
                    OO00OO0000O0000OO .log .info ('加购成功')#line:113
                OO0O0OOOOO00O0O0O =f'functionId=jm_task_process&body=%7B%22shopId%22%3A%2212765935%22%2C%22venderId%22%3A%2213577546%22%2C%22projectId%22%3A%22358620%22%2C%22taskId%22%3A{O0O0OOO0000000O00["id"]}%2C%22token%22%3A%22{O0O0OOO0000000O00["token"]}%22%2C%22opType%22%3A1%7D&t=1697184247624&eid=eidIa5c68120d7sfY99PKHwxTOyB1RlGTgCZBGPfUKTz5feUoC%2FDD%2FjdN%2BC0r%2FtF%2Bh%2F6lGZVL8mAQ8uwgybpEbZ4oL7RkLBJv4tF%2FWjF%2FTw3Nn%2FRR3dh&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=d3cbfc4ea3604057234b4257433ef5bc586d1f2c'#line:114
                OO00O0000000OO00O ,OOO00O00O00OOO000 ,OO0000O000000OO0O =await OO00OO0000O0000OO .Api_Jd_Com (O000O00O000OOO0O0 ,OO0O0OOOOO00O0O0O )#line:115
        OO0OO00OO00O0O0O0 =[OOOOO00O00OO00OO0 ['token']for OOOOO00O00OO00OO0 in O0O000OO00OO00O0O if "抽奖"in OOOOO00O00OO00OO0 ['name']][0 ]#line:116
        OOO0000OO00000000 =[O000O0O0OO00OOO00 ['id']for O000O0O0OO00OOO00 in O0O000OO00OO00O0O if "抽奖"in O000O0O0OO00OOO00 ['name']][0 ]#line:117
        while True :#line:118
                OO0O0OOOOO00O0O0O =f'functionId=jm_task_process&body=%7B%22shopId%22%3A%2212765935%22%2C%22venderId%22%3A%2213577546%22%2C%22projectId%22%3A358620%2C%22taskId%22%3A{OOO0000OO00000000}%2C%22token%22%3A%22{OO0OO00OO00O0O0O0}%22%2C%22opType%22%3A2%2C%22referSource%22%3A10084096558196%7D&t=1697113686255&eid=eidIde5c812183sbwkZEkK6%2FTCezMUyGy3rdu8JGRgfcBCAt40UcQi3vl8KucZUDXY9IDHh3YGNPj%2BnDWMIUs19jQaju%2FLkzCeIe030URPX5cdlBMNhF&appid=shop_view&clientVersion=10.0.0&client=wh5&uuid=70492ed7d2e0f3c29baa49e8f4a45a3812d922a3'#line:120
                OO00O0000000OO00O ,OOO00O00O00OOO000 ,OO0000O000000OO0O =await OO00OO0000O0000OO .Api_Jd_Com (O000O00O000OOO0O0 ,OO0O0OOOOO00O0O0O )#line:121
                if not OO0000O000000OO0O ['success']and OO0000O000000OO0O ['code']==300 :#line:123
                    break #line:124
                if OO0000O000000OO0O .get ('msg')is not None and "宠粉币数量不足"in OO0000O000000OO0O ['msg']:#line:125
                    OO00OO0000O0000OO .log .debug (f"第{O0O0OOO0000O000OO}个号 {OO0000O000000OO0O['msg']}")#line:126
                    break #line:127
                O00O00OOOOOOO0000 =OO0000O000000OO0O ['data']['awardVO']#line:129
                if O00O00OOOOOOO0000 is None :#line:130
                    OO00OO0000O0000OO .log .info (f"第{O0O0OOO0000O000OO}个号 剩余{OO0000O000000OO0O['data']['fansCoin']}次: {OO0000O000000OO0O['data']['pin']}:空气")#line:131
                    continue #line:132
                OO000O00O0OO00OOO =O00O00OOOOOOO0000 ['discount']+O00O00OOOOOOO0000 ['name']#line:133
                OO00OO0000O0000OO .log .info (f"第{O0O0OOO0000O000OO}个号 剩余{OO0000O000000OO0O['data']['fansCoin']}次: {OO0000O000000OO0O['data']['pin']}:{OO000O00O0OO00OOO}")#line:134
                if O00O00OOOOOOO0000 ['type']==1 :#line:135
                    break #line:136
    async def start (O00O0O0000OOOOO0O ,):#line:138
        O0O00OO0O0O0000O0 =[]#line:139
        if not O00O0O0000OOOOO0O .proxy :#line:141
            async def OOO0OOO00OO00OO0O (O0OO0O000O0OOOO00 ,OO00OO0OO0OOO000O ):#line:142
                async with O00O0O0000OOOOO0O .semaphore :#line:143
                    OO00O00OOO000O0OO =asyncio .create_task (O00O0O0000OOOOO0O .MainInfo (O0OO0O000O0OOOO00 ,OO00OO0OO0OOO000O ))#line:144
                    return await OO00O00OOO000O0OO #line:145
            for O00O0OOO00OOO000O ,OOO00O0OO0OO000OO in enumerate (ck ,1 ):#line:147
                O0O00OO0OO00O0OO0 =asyncio .create_task (OOO0OOO00OO00OO0O (O00O0OOO00OOO000O ,OOO00O0OO0OO000OO ))#line:148
                O0O00OO0O0O0000O0 .append (O0O00OO0OO00O0OO0 )#line:149
            await asyncio .gather (*O0O00OO0O0O0000O0 )#line:151
        else :#line:152
            for O00O0OOO00OOO000O ,OOO00O0OO0OO000OO in enumerate (ck ,1 ):#line:153
                await O00O0O0000OOOOO0O .MainInfo (O00O0OOO00OOO000O ,OOO00O0OO0OO000OO )#line:154
if __name__ =='__main__':#line:158
    FD =TEN_JD_FansDraw ()#line:159
    loop =asyncio .get_event_loop ()#line:160
    loop .run_until_complete (FD .start ())#line:161
    loop .close ()#line:162
