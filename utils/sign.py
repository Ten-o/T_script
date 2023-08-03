""#line:5
import base64 #line:6
import hashlib #line:7
import time #line:8
import random #line:9
import urllib .parse #line:10
import uuid #line:11
import json #line:12
string1 ="KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/"#line:14
string2 ="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"#line:15
def randomstr (O0O0O0OOO0OO0OO00 ):#line:17
    O0OO0000O0OOO0OOO =''.join (str (uuid .uuid4 ()).split ('-'))[O0O0O0OOO0OO0OO00 :]#line:18
    return O0OO0000O0OOO0OOO #line:19
def randomstr1 (OOO0OOO0O00OO0O0O ):#line:21
    OO000OO0OOOOO0OO0 =""#line:22
    for OOO0OO0O00O0OOO0O in range (OOO0OOO0O00OO0O0O ):#line:23
        OO000OO0OOOOO0OO0 =OO000OO0OOOOO0OO0 +random .choice ("abcdefghijklmnopqrstuvwxyz0123456789")#line:24
    return OO000OO0OOOOO0OO0 #line:25
def sign_core (O00O0OOO0OOOOOO0O ):#line:27
    O000OO00OOO000OOO =b'80306f4370b39fd5630ad0529f77adb6'#line:28
    OO0O00O0O0O0OO000 =[0x37 ,0x92 ,0x44 ,0x68 ,0xA5 ,0x3D ,0xCC ,0x7F ,0xBB ,0xF ,0xD9 ,0x88 ,0xEE ,0x9A ,0xE9 ,0x5A ]#line:29
    O0O0O0OOO0O0O00OO =[0 for _O0OOO0000OOOO00O0 in range (len (O00O0OOO0OOOOOO0O ))]#line:30
    for OOOO0OOOOO00OOOOO in range (len (O00O0OOO0OOOOOO0O )):#line:31
        OOOOOO000O00O0O0O =int (O00O0OOO0OOOOOO0O [OOOO0OOOOO00OOOOO ])#line:32
        O000OO000O0O0O00O =OO0O00O0O0O0OO000 [OOOO0OOOOO00OOOOO &0xf ]#line:33
        OO0O0OO0O00000000 =int (O000OO00OOO000OOO [OOOO0OOOOO00OOOOO &7 ])#line:34
        OOOOOO000O00O0O0O =O000OO000O0O0O00O ^OOOOOO000O00O0O0O #line:35
        OOOOOO000O00O0O0O =OOOOOO000O00O0O0O ^OO0O0OO0O00000000 #line:36
        OOOOOO000O00O0O0O =OOOOOO000O00O0O0O +O000OO000O0O0O00O #line:37
        O000OO000O0O0O00O =O000OO000O0O0O00O ^OOOOOO000O00O0O0O #line:38
        O0O0O000OO0OO0000 =int (O000OO00OOO000OOO [OOOO0OOOOO00OOOOO &7 ])#line:39
        O000OO000O0O0O00O =O000OO000O0O0O00O ^O0O0O000OO0OO0000 #line:40
        O0O0O0OOO0O0O00OO [OOOO0OOOOO00OOOOO ]=O000OO000O0O0O00O &0xff #line:41
    return bytes (O0O0O0OOO0O0O00OO )#line:42
def base64Encode (O000000O0O0O000OO ):#line:44
    return base64 .b64encode (O000000O0O0O000OO .encode ("utf-8")).decode ('utf-8').translate (str .maketrans (string1 ,string2 ))#line:45
def base64Decode (O000OOO0O0OO0OO0O ):#line:47
    return base64 .b64decode (O000OOO0O0OO0OO0O .translate (str .maketrans (string1 ,string2 ))).decode ('utf-8')#line:48
def randomeid ():#line:50
    return 'eidAaf8081218as20a2GM%s7FnfQYOecyDYLcd0rfzm3Fy2ePY4UJJOeV0Ub840kG8C7lmIqt3DTlc11fB/s4qsAP8gtPTSoxu'%randomstr1 (20 )#line:52
def get_ep (jduuid :str =''):#line:54
    if not jduuid :#line:55
        jduuid =randomstr (16 )#line:56
    OOOO0000OOO0OO000 =str (int (time .time ()*1000 ))#line:59
    O0OO0OO0OOO0O00OO =base64Encode (jduuid )#line:60
    OO0O0O0O0OOOO000O =base64Encode ('%s_%s_%s_%s'%(random .randint (1 ,10000 ),random .randint (1 ,10000 ),random .randint (1 ,10000 ),random .randint (1 ,10000 )))#line:63
    OO00OOOO000O00OOO =random .choice (['Mi11Ultra','Mi11','Mi10'])#line:64
    OO00OOOO000O00OOO =base64Encode (OO00OOOO000O00OOO )#line:65
    return '{"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","ts":%s,"ridx":-1,"cipher":{"area":"%s","d_model":"%s","wifiBssid":"dW5hbw93bq==","osVersion":"CJS=","d_brand":"WQvrb21f","screen":"CtS1DIenCNqm","uuid":"%s","aid":"%s","openudid":"%s"},"ciphertype":5,"version":"1.2.0","appname":"com.jingdong.app.mall"}'%(int (OOOO0000OOO0OO000 )-random .randint (100 ,1000 ),OO0O0O0O0OOOO000O ,OO00OOOO000O00OOO ,O0OO0OO0OOO0O00OO ,O0OO0OO0OOO0O00OO ,O0OO0OO0OOO0O00OO ),jduuid ,OOOO0000OOO0OO000 #line:67
def get_sign (O00OO000O0O0OOOO0 ,O000000O00O0OO00O ,client :str ="android",clientVersion :str ='11.2.8',jduuid :str ='')->dict :#line:69
    if isinstance (O000000O00O0OO00O ,dict ):#line:70
        OOO0000OOO0OOOO0O =O000000O00O0OO00O #line:71
        O000000O00O0OO00O =json .dumps (O000000O00O0OO00O )#line:72
    else :#line:73
        OOO0000OOO0OOOO0O =json .loads (O000000O00O0OO00O )#line:74
    if "eid"in OOO0000OOO0OOOO0O :#line:76
        O0O00O00OO0OOO000 =OOO0000OOO0OOOO0O ["eid"]#line:77
    else :#line:78
        O0O00O00OO0OOO000 =randomeid ()#line:79
    O0O0O0O00000O0000 ,O0O00000000O0O0O0 ,O0OOO0O00OOO00O0O =get_ep (jduuid )#line:81
    O0OO0O00O00OO0O00 =random .choice (["102","111","120"])#line:83
    O00O0O0O0OO00OOOO ="functionId=%s&body=%s&uuid=%s&client=%s&clientVersion=%s&st=%s&sv=%s"%(O00OO000O0O0OOOO0 ,O000000O00O0OO00O ,O0O00000000O0O0O0 ,client ,clientVersion ,O0OOO0O00OOO00O0O ,O0OO0O00O00OO0O00 )#line:86
    OOOO00O0O00O0O00O =sign_core (str .encode (O00O0O0O0OO00OOOO ))#line:88
    O0000OO0O0OOO0O0O =hashlib .md5 (base64 .b64encode (OOOO00O0O00O0O00O )).hexdigest ()#line:89
    O0OOO0OO000OOOO00 ={}#line:91
    O0OOO0OO000OOOO00 ["data"]={"functionId":O00OO000O0O0OOOO0 ,"body":O000000O00O0OO00O ,"clientVersion":clientVersion ,"client":client ,"uuid":O0O00000000O0O0O0 ,"eid":O0O00O00OO0OOO000 ,"ep":O0O0O0O00000O0000 ,"st":O0OOO0O00OOO00O0O ,"sign":O0000OO0O0OOO0O0O ,"sv":O0OO0O00O00OO0O00 }#line:92
    O0OOO0OO000OOOO00 ["convertUrl"]='functionId=%s&body=%s&clientVersion=%s&client=%s&sdkVersion=31&lang=zh_CN&harmonyOs=0&networkType=wifi&oaid=%s&eid=%s&ef=1&ep=%s&st=%s&sign=%s&sv=%s'%(O00OO000O0O0OOOO0 ,O000000O00O0OO00O ,clientVersion ,client ,O0O00000000O0O0O0 ,O0O00O00OO0OOO000 ,urllib .parse .quote (O0O0O0O00000O0000 ),O0OOO0O00OOO00O0O ,O0000OO0O0OOO0O0O ,O0OO0O00O00OO0O00 )#line:94
    O0OOO0OO000OOOO00 ["url"]='https://api.m.jd.com?%s'%(O0OOO0OO000OOOO00 ["convertUrl"])#line:95
    return O0OOO0OO000OOOO00