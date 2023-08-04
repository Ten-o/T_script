""#line:5
import base64 #line:6
import hashlib #line:7
import time #line:8
import random #line:9
import urllib .parse #line:10
import uuid #line:11
import json #line:12
import requests #line:13
ver =False #line:16
def verify (O0O0O0O000O0O0O0O ):#line:18
    O0OOOO0O00OOOOOO0 ='https://api.ixu.cc/verify'#line:19
    O0OO00O000OO0O000 =requests .get (url =O0OOOO0O00OOOOOO0 ,data ={'TOKEN':O0O0O0O000O0O0O0O })#line:20
    if O0OO00O000OO0O000 .status_code !=200 :#line:21
        return False #line:22
    global ver #line:23
    ver =True #line:24
    return True #line:25
string1 ="KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/"#line:28
string2 ="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"#line:29
def randomstr (OOO00O0000O0O0O0O ):#line:31
    O000O000O0O0OOOO0 =''.join (str (uuid .uuid4 ()).split ('-'))[OOO00O0000O0O0O0O :]#line:32
    return O000O000O0O0OOOO0 #line:33
def randomstr1 (OO0OOOO000O0OO00O ):#line:35
    OO000O0O0O000O0OO =""#line:36
    for OO0OOO0OO0O00O0OO in range (OO0OOOO000O0OO00O ):#line:37
        OO000O0O0O000O0OO =OO000O0O0O000O0OO +random .choice ("abcdefghijklmnopqrstuvwxyz0123456789")#line:38
    return OO000O0O0O000O0OO #line:39
def sign_core (O000O00OOO0OOOO00 ):#line:41
    if ver !=True :#line:42
        return 900 #line:43
    OOO000OOOO00OO000 =b'80306f4370b39fd5630ad0529f77adb6'#line:44
    O0O00O0O00OO0OOOO =[0x37 ,0x92 ,0x44 ,0x68 ,0xA5 ,0x3D ,0xCC ,0x7F ,0xBB ,0xF ,0xD9 ,0x88 ,0xEE ,0x9A ,0xE9 ,0x5A ]#line:45
    OOO0OO0OO0000O0OO =[0 for _OO00O0O00O000O0OO in range (len (O000O00OOO0OOOO00 ))]#line:46
    for O00000O00000OO000 in range (len (O000O00OOO0OOOO00 )):#line:47
        OO000000OOOOO000O =int (O000O00OOO0OOOO00 [O00000O00000OO000 ])#line:48
        O00O000O0OO000OOO =O0O00O0O00OO0OOOO [O00000O00000OO000 &0xf ]#line:49
        O0O0OOO00OO0O0OOO =int (OOO000OOOO00OO000 [O00000O00000OO000 &7 ])#line:50
        OO000000OOOOO000O =O00O000O0OO000OOO ^OO000000OOOOO000O #line:51
        OO000000OOOOO000O =OO000000OOOOO000O ^O0O0OOO00OO0O0OOO #line:52
        OO000000OOOOO000O =OO000000OOOOO000O +O00O000O0OO000OOO #line:53
        O00O000O0OO000OOO =O00O000O0OO000OOO ^OO000000OOOOO000O #line:54
        OOOOO000O0000O00O =int (OOO000OOOO00OO000 [O00000O00000OO000 &7 ])#line:55
        O00O000O0OO000OOO =O00O000O0OO000OOO ^OOOOO000O0000O00O #line:56
        OOO0OO0OO0000O0OO [O00000O00000OO000 ]=O00O000O0OO000OOO &0xff #line:57
    return bytes (OOO0OO0OO0000O0OO )#line:58
def base64Encode (OOOOOO0OOO0O0OO0O ):#line:60
    return base64 .b64encode (OOOOOO0OOO0O0OO0O .encode ("utf-8")).decode ('utf-8').translate (str .maketrans (string1 ,string2 ))#line:61
def base64Decode (OO0OO00OOOOO0O0O0 ):#line:63
    return base64 .b64decode (OO0OO00OOOOO0O0O0 .translate (str .maketrans (string1 ,string2 ))).decode ('utf-8')#line:64
def randomeid ():#line:66
    return 'eidAaf8081218as20a2GM%s7FnfQYOecyDYLcd0rfzm3Fy2ePY4UJJOeV0Ub840kG8C7lmIqt3DTlc11fB/s4qsAP8gtPTSoxu'%randomstr1 (20 )#line:68
def get_ep (jduuid :str =''):#line:70
    if ver !=True :#line:71
        return 900 #line:72
    if not jduuid :#line:73
        jduuid =randomstr (16 )#line:74
    OO0000OOO0O00O00O =str (int (time .time ()*1000 ))#line:77
    OOOOOO00OO00OOO00 =base64Encode (jduuid )#line:78
    O0O00000O0000OOO0 =base64Encode ('%s_%s_%s_%s'%(random .randint (1 ,10000 ),random .randint (1 ,10000 ),random .randint (1 ,10000 ),random .randint (1 ,10000 )))#line:81
    OO00OOO0O000O0000 =random .choice (['Mi11Ultra','Mi11','Mi10'])#line:82
    OO00OOO0O000O0000 =base64Encode (OO00OOO0O000O0000 )#line:83
    return '{"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","ts":%s,"ridx":-1,"cipher":{"area":"%s","d_model":"%s","wifiBssid":"dW5hbw93bq==","osVersion":"CJS=","d_brand":"WQvrb21f","screen":"CtS1DIenCNqm","uuid":"%s","aid":"%s","openudid":"%s"},"ciphertype":5,"version":"1.2.0","appname":"com.jingdong.app.mall"}'%(int (OO0000OOO0O00O00O )-random .randint (100 ,1000 ),O0O00000O0000OOO0 ,OO00OOO0O000O0000 ,OOOOOO00OO00OOO00 ,OOOOOO00OO00OOO00 ,OOOOOO00OO00OOO00 ),jduuid ,OO0000OOO0O00O00O #line:85
def get_sign (O00000OO0OOOO0O0O ,OO0O000OOO0OOOOO0 ,client :str ="android",clientVersion :str ='11.2.8',jduuid :str ='')->dict :#line:87
    if ver !=True :#line:88
        return 900 #line:89
    if isinstance (OO0O000OOO0OOOOO0 ,dict ):#line:90
        OOO0O000OOOOOOO00 =OO0O000OOO0OOOOO0 #line:91
        OO0O000OOO0OOOOO0 =json .dumps (OO0O000OOO0OOOOO0 )#line:92
    else :#line:93
        OOO0O000OOOOOOO00 =json .loads (OO0O000OOO0OOOOO0 )#line:94
    if "eid"in OOO0O000OOOOOOO00 :#line:96
        O0O00000O0OO00000 =OOO0O000OOOOOOO00 ["eid"]#line:97
    else :#line:98
        O0O00000O0OO00000 =randomeid ()#line:99
    OO0O0OOO0O00000OO ,OO0000O0OOO0O0O0O ,OO0O0O00OOOO00OO0 =get_ep (jduuid )#line:101
    O00O0000O0OO00OO0 =random .choice (["102","111","120"])#line:103
    OO00OOO0000OOO0O0 ="functionId=%s&body=%s&uuid=%s&client=%s&clientVersion=%s&st=%s&sv=%s"%(O00000OO0OOOO0O0O ,OO0O000OOO0OOOOO0 ,OO0000O0OOO0O0O0O ,client ,clientVersion ,OO0O0O00OOOO00OO0 ,O00O0000O0OO00OO0 )#line:106
    O0000OO0O0O0OO0OO =sign_core (str .encode (OO00OOO0000OOO0O0 ))#line:108
    O00O0OO0OOOOO0OO0 =hashlib .md5 (base64 .b64encode (O0000OO0O0O0OO0OO )).hexdigest ()#line:109
    O000O0OOOOO0000OO ={"functionId":O00000OO0OOOO0O0O ,"body":OO0O000OOO0OOOOO0 ,"clientVersion":clientVersion ,"client":client ,"uuid":OO0000O0OOO0O0O0O ,"eid":O0O00000O0OO00000 ,"ep":OO0O0OOO0O00000OO ,"st":OO0O0O00OOOO00OO0 ,"sign":O00O0OO0OOOOO0OO0 ,"sv":O00O0000O0OO00OO0 }#line:111
    O000O0OOOOO0000OO ["convertUrl"]='functionId=%s&body=%s&clientVersion=%s&client=%s&sdkVersion=31&lang=zh_CN&harmonyOs=0&networkType=wifi&oaid=%s&eid=%s&ef=1&ep=%s&st=%s&sign=%s&sv=%s'%(O00000OO0OOOO0O0O ,OO0O000OOO0OOOOO0 ,clientVersion ,client ,OO0000O0OOO0O0O0O ,O0O00000O0OO00000 ,urllib .parse .quote (OO0O0OOO0O00000OO ),OO0O0O00OOOO00OO0 ,O00O0OO0OOOOO0OO0 ,O00O0000O0OO00OO0 )#line:113
    O000O0OOOOO0000OO ["url"]='https://api.m.jd.com?%s'%(O000O0OOOOO0000OO ["convertUrl"])#line:114
    return O000O0OOOOO0000OO