""#line:7
import requests ,re ,random ,json ,sys ,os ,time ,threading ,concurrent .futures #line:9
from utils .sign import *#line:10
from fake_useragent import UserAgent #line:12
from jdCookie import get_cookies #line:13
from datetime import datetime ,timedelta #line:14
class Daily :#line:15
    def __init__ (O0O0OOO0OOO0OO0OO ):#line:16
        O0O0OOO0OOO0OO0OO .ua =UserAgent ()#line:17
        O0O0OOO0OOO0OO0OO .proxy =os .environ .get ("TEN_proxy")if os .environ .get ("TEN_proxy")else False #line:18
        O0O0OOO0OOO0OO0OO .proxies ={'http':f'{O0O0OOO0OOO0OO0OO.proxy}','https':f'{O0O0OOO0OOO0OO0OO.proxy}',}#line:22
        O0O0OOO0OOO0OO0OO .token =os .environ .get ("TEN_TOKEN")if os .environ .get ("TEN_TOKEN")else sys .exit ('❌TOKEN未设置')#line:23
        O0O0OOO0OOO0OO0OO .activiturl =os .environ .get ("jd_loreal_Daily")if os .environ .get ("jd_loreal_Daily")else sys .exit ('❌未获取到jd_loreal_Daily变量 程序自动退出')#line:24
        O0O0OOO0OOO0OO0OO .activityId =re .findall ('activityId=(\d+)',O0O0OOO0OOO0OO0OO .activiturl )[0 ]#line:25
        O0O0OOO0OOO0OO0OO .time_list =["10:00","20:00"]#line:26
        O0O0OOO0OOO0OO0OO .token_activities ={}#line:27
        O0O0OOO0OOO0OO0OO .start =''#line:28
        O0O0OOO0OOO0OO0OO .pause =False #line:29
        O0O0OOO0OOO0OO0OO .verify =False #line:30
    def verif (O00O0000OO0OO0O0O ):#line:32
        try :#line:33
            O00O0000OO0OO0O0O .verify =verify (O00O0000OO0OO0O0O .token )#line:34
            if O00O0000OO0OO0O0O .verify !=True :#line:35
                sys .exit ('❌授权未通过 程序自动退出！！！')#line:36
            return O00O0000OO0OO0O0O .verify #line:37
        except Exception as OO00O0OO0O00OOOOO :#line:38
            print (f'验证授权失败： {OO00O0OO0O00OOOOO}')#line:39
    def save_json_data (O00OOOOO00OO00000 ,OO000000O0000OO0O ,OO00000O0OOO0OOO0 ):#line:40
        with open (OO00000O0OOO0OOO0 ,'w',encoding ='utf-8')as OO0O000000OO0OO0O :#line:42
            json .dump (OO000000O0000OO0O ,OO0O000000OO0OO0O ,ensure_ascii =False ,indent =4 )#line:43
    def load_json_data (OOO0O0OOO0O000O00 ,O000O000OOOO000O0 ):#line:45
        with open (O000O000OOOO000O0 ,'r',encoding ='utf-8')as OO000OO000OO0OOOO :#line:47
            O000O00OO0OOO0000 =json .load (OO000OO000OO0OOOO )#line:48
        return O000O00OO0OOO0000 #line:49
    def data_timeout (O0OO0000OOO0OO000 ,O0000OO00OOOO0O0O ):#line:50
        OO00O0O0000000O0O =datetime .fromtimestamp (O0000OO00OOOO0O0O /1000 )#line:51
        OO0O0O0O0OOO0O00O =OO00O0O0000000O0O .strftime ("%Y-%m-%d %H:%M:%S")#line:52
        return OO0O0O0O0OOO0O00O #line:53
    def post_Token (OOOOO00O00O000O0O ,OOO000O00OOO0OO0O ):#line:54
        OO0000OO00O0OO0OO ='https://api.m.jd.com/client.action'#line:55
        O0OO000O0O00000OO ={'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':OOOOO00O00O000O0O .ua .safari ,'Cookie':OOO000O00OOO0OO0O ,'Host':'api.m.jd.com','Referer':'https://lzkjdz-isv.isvjcloud.com/wxAssemblePage/activity/?activityId=67dfd244aacb438893a73a03785a48c7&sid=&un_area=17_1413_1418_7610','Accept-Language':'zh-Hans-CN;q=1 en-CN;q=0.9','Accept':'*/*'}#line:66
        O000000OO0000OO00 =get_sign ('isvObfuscator',{"url":'https://lzkjdz-isv.isvjcloud.com',"id":""})#line:68
        if OOOOO00O00O000O0O .proxy !=False :#line:69
            O0000OOOO00O000O0 =requests .post (url =OO0000OO00O0OO0OO ,headers =O0OO000O0O00000OO ,data =O000000OO0000OO00 ['convertUrl'],proxies =OOOOO00O00O000O0O .proxies )#line:70
        else :#line:71
            O0000OOOO00O000O0 =requests .post (url =OO0000OO00O0OO0OO ,headers =O0OO000O0O00000OO ,data =O000000OO0000OO00 ['convertUrl'],)#line:72
        print (O0000OOOO00O000O0 .status_code )#line:73
        if O0000OOOO00O000O0 .status_code !=200 :#line:74
            sys .exit (f'❌ 获取Token失败:{O0000OOOO00O000O0.status_code}, 程序将自动退出！！')#line:75
        if 'token'in O0000OOOO00O000O0 .json ():#line:76
            OOOOO00O00O000O0O .token =O0000OOOO00O000O0 .json ()['token']#line:77
        else :#line:78
            print (O0000OOOO00O000O0 .json ())#line:79
    def get_Token (OO00OO00OO0OO0OOO ,O0O00O0O00000OOO0 ,OO0OO0O0OOO00OO00 ,OO00OO00OO00O000O ,O0OOO000O0O0O00OO ):#line:81
        if OO00OO00OO0OO0OOO .verify !=True :#line:82
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:83
        OO00OOOO0O0O000OO ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/user-info/login'#line:84
        OO0O0O0000OOO00O0 ={"status":"0","activityId":O0O00O0O00000OOO0 ,"source":"01","tokenPin":OO00OO00OO0OO0OOO .token ,"shareUserId":""}#line:85
        O000O00O00OOO0OOO ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/json;charset=UTF-8','Origin':f'https://lzkj-isv.isvjcloud.com','User-Agent':OO00OO00OO0OO0OOO .ua .safari ,'Connection':'keep-alive','Referer':OO0OO0O0OOO00OO00 ,}#line:96
        if OO00OO00OO0OO0OOO .proxy !=False :#line:97
            OOO00OOOOO0O0O0O0 =requests .post (url =OO00OOOO0O0O000OO ,headers =O000O00O00OOO0OOO ,data =json .dumps (OO0O0O0000OOO00O0 ),proxies =OO00OO00OO0OO0OOO .proxies )#line:98
        else :#line:99
            OOO00OOOOO0O0O0O0 =requests .post (url =OO00OOOO0O0O000OO ,headers =O000O00O00OOO0OOO ,data =json .dumps (OO0O0O0000OOO00O0 ))#line:100
        if OOO00OOOOO0O0O0O0 .status_code !=200 :#line:101
            sys .exit (f'❌ 登录失败:{OOO00OOOOO0O0O0O0.status_code}, 程序将自动退出！！')#line:102
        OOOOO0O00O00OOO0O ={"start_time":O0OOO000O0O0O00OO ,"activityId":O0O00O0O00000OOO0 ,"prizeInfoId":OO00OO00OO00O000O ,"token":OOO00OOOOO0O0O0O0 .json ()['data']['token'],"url":OO0OO0O0OOO00OO00 ,}#line:109
        OO00OO00OO0OO0OOO .token_activities [O0O00O0O00000OOO0 ]=OOOOO0O00O00OOO0O #line:110
        return 200 ,OOO00OOOOO0O0O0O0 .json ()['data']['token'],OOO00OOOOO0O0O0O0 .json ()['data']['userPin']#line:111
    def post_activity (OOO0OOO0O000000O0 ,O00O0OOO0000OO0O0 ,O00OOOO00OO00O000 ,OOOO0OOOOOO000O00 ):#line:113
        if OOO0OOO0O000000O0 .verify !=True :#line:114
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:115
        O00OO0OO00O0O00O0 ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/dailyGrabs/activity'#line:116
        OO0O000O00OO000O0 ={"accept":"application/json, text/plain, */*","accept-language":"zh-CN,zh;q=0.9,en;q=0.8","content-type":"application/json;charset=UTF-8","sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-origin","token":O00O0OOO0000OO0O0 ,"Referer":O00OOOO00OO00O000 ,"Referrer-Policy":"strict-origin-when-cross-origin",}#line:127
        if OOO0OOO0O000000O0 .proxy !=False :#line:128
            OOOO0OO0000OOOOOO =requests .post (url =O00OO0OO00O0O00O0 ,headers =OO0O000O00OO000O0 ,data ={},proxies =OOO0OOO0O000000O0 .proxies )#line:129
        else :#line:130
            OOOO0OO0000OOOOOO =requests .post (url =O00OO0OO00O0O00O0 ,headers =OO0O000O00OO000O0 ,data ={})#line:131
        if OOOO0OO0000OOOOOO .status_code ==200 :#line:132
            OOOO0OO0000OOOOOO =OOOO0OO0000OOOOOO .json ()['data']#line:133
            OO00O0O0OOO0O000O =OOO0OOO0O000000O0 .data_timeout (OOOO0OO0000OOOOOO ['activityStartTime'])#line:134
            OO0O0OO0OO0OO0000 =OOO0OOO0O000000O0 .data_timeout (OOOO0OO0000OOOOOO ['activityEndTime'])#line:135
            OOO0OOO0O000000O0 .start =OOO0OOO0O000000O0 .data_timeout (OOOO0OO0000OOOOOO ['lotteryTime'])#line:136
            print ('-'*15 ,'记录缓存','-'*16 )#line:137
            print (f'开抢时间: {OOO0OOO0O000000O0.start} \n抢购详细: {OOOO0OO0000OOOOOO["prizeName"]}  抢购数量: {OOOO0OO0000OOOOOO["hours"]}个  已抢成功：{OOOO0OO0000OOOOOO["userCount"]}个\n活动时间: {OO00O0O0OOO0O000O} - {OO0O0OO0OO0OO0000}')#line:138
            print ("-"*40 )#line:139
            O0OOO00000OO0OOO0 =OOO0OOO0O000000O0 .load_json_data ('activity_info.json')#line:141
            O00O0O0O000OO0OO0 ={"id":OOOO0OOOOOO000O00 ,"prizeInfoId":OOOO0OO0000OOOOOO ['prizeInfoId'],"start":datetime .strptime (OOO0OOO0O000000O0 .start ,'%Y-%m-%d %H:%M:%S').strftime ('%H:%M:%S'),"prizeName":OOOO0OO0000OOOOOO ['prizeName'],"hours":OOOO0OO0000OOOOOO ['hours'],"userCount":OOOO0OO0000OOOOOO ['userCount'],"StartTime":OO00O0O0OOO0O000O ,"EndTime":OO0O0OO0OO0OO0000 ,"activiturl":O00OOOO00OO00O000 }#line:152
            O0OOO00000OO0OOO0 [OOO0OOO0O000000O0 .activityId ]=O00O0O0O000OO0OO0 #line:153
            OOO0OOO0O000000O0 .save_json_data (O0OOO00000OO0OOO0 ,'activity_info.json')#line:155
            return OOOO0OO0000OOOOOO #line:156
    def get_dayReceive (OO0OOO0OOOOOO0000 ,OOOO00O0OO0O00OOO ,OOO00O0OO0OO000O0 ,O0OOOO0OO000OO0O0 ):#line:158
        if OO0OOO0OOOOOO0000 .verify !=True :#line:159
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:160
        OOOOOO0OO00O0OOO0 ='https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas/api/task/dailyGrabs/dayReceive'#line:162
        OO00000OO000OO0O0 ={'Host':'lzkj-isv.isvjcloud.com','Accept':'application/json, text/plain, */*','Accept-Language':'zh-CN,zh-Hans;q=0.9','Accept-Encoding':'gzip, deflate, br','token':OOO00O0OO0OO000O0 ,'Content-Type':'application/json;charset=UTF-8','Origin':'https://lzkj-isv.isvjcloud.com','User-Agent':OO0OOO0OOOOOO0000 .ua .safari ,'Connection':'keep-alive','Referer':O0OOOO0OO000OO0O0 ,}#line:174
        O0O0000OO0OO0OOOO ={'prizeInfoId':OOOO00O0OO0O00OOO }#line:177
        if OO0OOO0OOOOOO0000 .proxy !=False :#line:178
            O0OOOO00OOO0OO0OO =requests .post (url =OOOOOO0OO00O0OOO0 ,headers =OO00000OO000OO0O0 ,data =json .dumps (O0O0000OO0OO0OOOO ),proxies =OO0OOO0OOOOOO0000 .proxies )#line:179
        else :#line:180
            O0OOOO00OOO0OO0OO =requests .post (url =OOOOOO0OO00O0OOO0 ,headers =OO00000OO000OO0O0 ,data =json .dumps (O0O0000OO0OO0OOOO ))#line:181
        if O0OOOO00OOO0OO0OO .status_code ==200 :#line:182
            O0O0000OO0OO0OOOO =O0OOOO00OOO0OO0OO .json ()#line:184
            if 'resp_msg'in O0O0000OO0OO0OOOO and O0O0000OO0OO0OOOO ['resp_msg']:#line:185
                print (datetime .now (),f'PZID:{OOOO00O0OO0O00OOO}',f'❌领取失败:{O0O0000OO0OO0OOOO["resp_msg"]}')#line:186
            elif 'data'in O0O0000OO0OO0OOOO and 'result'in O0O0000OO0OO0OOOO ['data']and O0O0000OO0OO0OOOO ['data']['result']:#line:187
                try :#line:189
                    print (datetime .now (),f'PZID:{OOOO00O0OO0O00OOO}',f"✔️领取成功:{O0O0000OO0OO0OOOO['data']['prizeName']}")#line:190
                except Exception as O0OO0OO0000O000O0 :#line:191
                    print (datetime .now (),f'PZID:{OOOO00O0OO0O00OOO}',O0OOOO00OOO0OO0OO .json ())#line:192
                    print (O0OO0OO0000O000O0 )#line:193
            else :#line:195
                print (datetime .now (),f'PZID:{OOOO00O0OO0O00OOO}','💭新鲜空气')#line:196
        else :#line:198
            print (datetime .now (),f'PZID:{OOOO00O0OO0O00OOO}',f"dayReceive：{O0OOOO00OOO0OO0OO.status_code}")#line:199
    def cache_Daily (OOO0OOOO0O0000O00 ):#line:201
        if OOO0OOOO0O0000O00 .verify !=True :#line:202
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:203
        OOO0OOOO0O0000O00 .token_activities ={}#line:204
        with open ('activity_info.json',encoding ="utf-8")as O000OOOOO0O00O0OO :#line:205
            OO0000OOOOOO00O0O =json .load (O000OOOOO0O00O0OO )#line:206
        OOO0OOOO0O0000O00 .post_Token (get_cookies ()[0 ])#line:207
        time .sleep (1 )#line:208
        OO0OO00000OO0O00O =datetime .now ().date ()#line:209
        for OO000O0000OO0O00O in OO0000OOOOOO00O0O :#line:210
            OO0OOOO0000OO000O =datetime .strptime (OO0000OOOOOO00O0O [OO000O0000OO0O00O ]['EndTime'],'%Y-%m-%d %H:%M:%S')#line:211
            if datetime .now ()>OO0OOOO0000OO000O :#line:212
                continue #line:213
            OOOO0OO0OO0OO0OO0 =datetime .strptime (OO0000OOOOOO00O0O [OO000O0000OO0O00O ]['start'],"%H:%M:%S").time ()#line:214
            if datetime .now ()<datetime .combine (OO0OO00000OO0O00O ,OOOO0OO0OO0OO0OO0 ):#line:215
                OO0O0OO0OOO0000OO =datetime .combine (OO0OO00000OO0O00O ,OOOO0OO0OO0OO0OO0 )-datetime .now ()#line:216
                O0OO00OOOOO0OOOO0 =OO0O0OO0OOO0000OO .total_seconds ()//60 #line:217
                if O0OO00OOOOO0OOOO0 <=5 :#line:218
                    OOO0OOOO0O0000O00 .get_Token (OO0000OOOOOO00O0O [OO000O0000OO0O00O ]['id'],OO0000OOOOOO00O0O [OO000O0000OO0O00O ]['activiturl'],OO0000OOOOOO00O0O [OO000O0000OO0O00O ]['prizeInfoId'],datetime .combine (OO0OO00000OO0O00O ,OOOO0OO0OO0OO0OO0 ))#line:220
        print (f"读取缓存文件成功 有{len(OOO0OOOO0O0000O00.token_activities)}个任务")#line:221
        O0OOOO00OOO00OO0O =False #line:222
        for OO000O0000OO0O00O in OOO0OOOO0O0000O00 .token_activities :#line:223
            O00OOO00O0OOOO0O0 =OOO0OOOO0O0000O00 .token_activities [OO000O0000OO0O00O ]['start_time']#line:224
            O0O0O0000OOO0000O =datetime .now ()#line:225
            if O0O0O0000OOO0000O <O00OOO00O0OOOO0O0 and not O0OOOO00OOO00OO0O :#line:226
                OO0O0OO0OOO0000OO =O00OOO00O0OOOO0O0 -O0O0O0000OOO0000O #line:227
                O0OO00OOOOO0OOOO0 =OO0O0OO0OOO0000OO .total_seconds ()//60 #line:228
                if O0OO00OOOOO0OOOO0 <=5 :#line:229
                    OOO0O0OO000O00O00 =O0O0O0000OOO0000O .strftime ("%Y-%m-%d %H:%M:%S")#line:230
                    OOO00OOO0O00OOOO0 =(O00OOO00O0OOOO0O0 -O0O0O0000OOO0000O ).total_seconds ()-0.3 #line:231
                    print (f"当前时间:{OOO0O0OO000O00O00} 需等待: {OOO00OOO0O00OOOO0}秒")#line:232
                    print ('-'*40 )#line:233
                    time .sleep (OOO00OOO0O00OOOO0 )#line:234
                    O0OOOO00OOO00OO0O =True #line:235
                else :#line:236
                    print (f"活动开始时间是{O00OOO00O0OOOO0O0}哦！！！")#line:237
        print ('-'*15 ,'倒计时结束','-'*15 )#line:238
        """ 线程并发 """#line:242
        OO00O000OOOO0O00O =time .time ()#line:243
        for OO00O00OOOO0O00OO in range (1 ,20 ):#line:244
            OOOO00O00O0O0OOO0 =[]#line:245
            for OO000O0000OO0O00O in OOO0OOOO0O0000O00 .token_activities :#line:246
                O0O0OOO00000OO00O =threading .Thread (target =OOO0OOOO0O0000O00 .get_dayReceive ,args =(OOO0OOOO0O0000O00 .token_activities [OO000O0000OO0O00O ]["prizeInfoId"],OOO0OOOO0O0000O00 .token_activities [OO000O0000OO0O00O ]["token"],OOO0OOOO0O0000O00 .token_activities [OO000O0000OO0O00O ]["url"]))#line:249
                OOOO00O00O0O0OOO0 .append (O0O0OOO00000OO00O )#line:250
            for OO0O000OOOO0OOOOO in OOOO00O00O0O0OOO0 :#line:251
                OO0O000OOOO0OOOOO .start ()#line:252
            for OO0O000OOOO0OOOOO in OOOO00O00O0O0OOO0 :#line:253
                OO0O000OOOO0OOOOO .join ()#line:254
        print (f'耗时：{time.time() - OO00O000OOOO0O00O}')#line:255
    def main (OOOOO00OO0OOOO0O0 ):#line:258
        OOOOO00OO0OOOO0O0 .verif ()#line:259
        if OOOOO00OO0OOOO0O0 .verify !=True :#line:260
            sys .exit ('❌授权未通过 程序自动退出！！！')#line:261
        O0OO0O0OO0O0O00OO =datetime .now ().time ()#line:262
        OO0O00OOOO00OOO00 =False #line:263
        for OO00OOOOO0OO0OOO0 in OOOOO00OO0OOOO0O0 .time_list :#line:264
            O0000O000O0000000 =datetime .strptime (OO00OOOOO0OO0OOO0 ,"%H:%M").time ()#line:265
            O0O0000O0O00OOOO0 =datetime .combine (datetime .now ().date (),O0000O000O0000000 )-datetime .combine (datetime .now ().date (),O0OO0O0OO0O0O00OO )#line:267
            OOOOO0O00OO000O00 =abs (O0O0000O0O00OOOO0 .total_seconds ())//60 #line:268
            if OOOOO0O00OO000O00 <=5 :#line:269
                print ('-'*40 )#line:270
                print (f"当前时间接近于 {OO00OOOOO0OO0OOO0} 开始读取缓存文件")#line:271
                OOOOO00OO0OOOO0O0 .cache_Daily ()#line:272
                OO0O00OOOO00OOO00 =True #line:273
            else :#line:274
                if not OO0O00OOOO00OOO00 :#line:275
                    OOOOO00OO0OOOO0O0 .post_Token (get_cookies ()[0 ])#line:276
                    time .sleep (1 )#line:277
                    OO00OO0OO0O00OOO0 =OOOOO00OO0OOOO0O0 .get_Token (OOOOO00OO0OOOO0O0 .activityId ,OOOOO00OO0OOOO0O0 .activiturl ,0 ,0 )[1 ]#line:278
                    OOOOO00OO0OOOO0O0 .post_activity (OO00OO0OO0O00OOO0 ,OOOOO00OO0OOOO0O0 .activiturl ,OOOOO00OO0OOOO0O0 .activityId )#line:279
                    OO0O00OOOO00OOO00 =True #line:280
s =Daily ()#line:282
s .main ()#line:283
