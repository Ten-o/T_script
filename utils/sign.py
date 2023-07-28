""#line:5:'''
import base64 #line:6:import base64
import hashlib #line:7:import hashlib
import time #line:8:import time
import random #line:9:import random
import urllib .parse #line:10:import urllib.parse
import uuid #line:11:import uuid
import json #line:12:import json
import requests #line:13:import requests
ver =False #line:16:ver = False
def verify (OOO0OO00OOO0O00O0 ):#line:18:def verify(token):
    OOO0OOO00O0000O00 ='https://api.ixu.cc/verify'#line:19:url = 'https://api.ixu.cc/verify'
    O0O0OOOOOOO0OO000 =requests .get (url =OOO0OOO00O0000O00 ,data ={'TOKEN':OOO0OO00OOO0O00O0 })#line:20:res = requests.get(url=url, data={'TOKEN': token})
    if O0O0OOOOOOO0OO000 .status_code !=200 :#line:21:if res.status_code != 200:
        return False #line:22:return False
    global ver #line:23:global ver
    ver =True #line:24:ver = True
    return True #line:25:return True
string1 ="KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/"#line:28:string1 = "KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/"
string2 ="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"#line:29:string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
def randomstr (O00O0000OO00O00O0 ):#line:31:def randomstr(num):
    OO0OO0OOO0O00000O =''.join (str (uuid .uuid4 ()).split ('-'))[O00O0000OO00O00O0 :]#line:32:randomstr = ''.join(str(uuid.uuid4()).split('-'))[num:]
    return OO0OO0OOO0O00000O #line:33:return randomstr
def randomstr1 (O00O00OOOOO0O00O0 ):#line:35:def randomstr1(num):
    OO0OO00O00OO0OO0O =""#line:36:randomstr = ""
    for O00O0OO0OOOOOOOOO in range (O00O00OOOOO0O00O0 ):#line:37:for i in range(num):
        OO0OO00O00OO0OO0O =OO0OO00O00OO0OO0O +random .choice ("abcdefghijklmnopqrstuvwxyz0123456789")#line:38:randomstr = randomstr + random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
    return OO0OO00O00OO0OO0O #line:39:return randomstr
def sign_core (O0OOOOOO0OOOO0000 ):#line:41:def sign_core(inarg):
    if ver !=True :#line:42:if ver != True:
        return 900 #line:43:return 900
    OO0O00OOOOOOOOO0O =b'80306f4370b39fd5630ad0529f77adb6'#line:44:key = b'80306f4370b39fd5630ad0529f77adb6'
    O000O000OOOO00O00 =[0x37 ,0x92 ,0x44 ,0x68 ,0xA5 ,0x3D ,0xCC ,0x7F ,0xBB ,0xF ,0xD9 ,0x88 ,0xEE ,0x9A ,0xE9 ,0x5A ]#line:45:mask = [0x37, 0x92, 0x44, 0x68, 0xA5, 0x3D, 0xCC, 0x7F, 0xBB, 0xF, 0xD9, 0x88, 0xEE, 0x9A, 0xE9, 0x5A]
    OOO0O0000OOOOO0OO =[0 for _O0O00OO0000OOO0O0 in range (len (O0OOOOOO0OOOO0000 ))]#line:46:array = [0 for _ in range(len(inarg))]
    for OO0OOOOOOOO00O000 in range (len (O0OOOOOO0OOOO0000 )):#line:47:for i in range(len(inarg)):
        O000OO00OOO0OOO0O =int (O0OOOOOO0OOOO0000 [OO0OOOOOOOO00O000 ])#line:48:r0 = int(inarg[i])
        O0OO000O00OOO0O0O =O000O000OOOO00O00 [OO0OOOOOOOO00O000 &0xf ]#line:49:r2 = mask[i & 0xf]
        O0OOO0OO0O0O0000O =int (OO0O00OOOOOOOOO0O [OO0OOOOOOOO00O000 &7 ])#line:50:r4 = int(key[i & 7])
        O000OO00OOO0OOO0O =O0OO000O00OOO0O0O ^O000OO00OOO0OOO0O #line:51:r0 = r2 ^ r0
        O000OO00OOO0OOO0O =O000OO00OOO0OOO0O ^O0OOO0OO0O0O0000O #line:52:r0 = r0 ^ r4
        O000OO00OOO0OOO0O =O000OO00OOO0OOO0O +O0OO000O00OOO0O0O #line:53:r0 = r0 + r2
        O0OO000O00OOO0O0O =O0OO000O00OOO0O0O ^O000OO00OOO0OOO0O #line:54:r2 = r2 ^ r0
        OOO0OOOOOOOO0O00O =int (OO0O00OOOOOOOOO0O [OO0OOOOOOOO00O000 &7 ])#line:55:r1 = int(key[i & 7])
        O0OO000O00OOO0O0O =O0OO000O00OOO0O0O ^OOO0OOOOOOOO0O00O #line:56:r2 = r2 ^ r1
        OOO0O0000OOOOO0OO [OO0OOOOOOOO00O000 ]=O0OO000O00OOO0O0O &0xff #line:57:array[i] = r2 & 0xff
    return bytes (OOO0O0000OOOOO0OO )#line:58:return bytes(array)
def base64Encode (O00O000O00O00OO0O ):#line:60:def base64Encode(string):
    return base64 .b64encode (O00O000O00O00OO0O .encode ("utf-8")).decode ('utf-8').translate (str .maketrans (string1 ,string2 ))#line:61:return base64.b64encode(string.encode("utf-8")).decode('utf-8').translate(str.maketrans(string1, string2))
def base64Decode (OO000O0000OO00OOO ):#line:63:def base64Decode(string):
    return base64 .b64decode (OO000O0000OO00OOO .translate (str .maketrans (string1 ,string2 ))).decode ('utf-8')#line:64:return base64.b64decode(string.translate(str.maketrans(string1, string2))).decode('utf-8')
def randomeid ():#line:66:def randomeid():
    return 'eidAaf8081218as20a2GM%s7FnfQYOecyDYLcd0rfzm3Fy2ePY4UJJOeV0Ub840kG8C7lmIqt3DTlc11fB/s4qsAP8gtPTSoxu'%randomstr1 (20 )#line:68:20)
def get_ep (OOOO00O0000OO0O00 :str =''):#line:70:def get_ep(jduuid : str=''):
    if ver !=True :#line:71:if ver != True:
        return 900 #line:72:return 900
    if not OOOO00O0000OO0O00 :#line:73:if not jduuid:
        OOOO00O0000OO0O00 =randomstr (16 )#line:74:jduuid = randomstr(16)
    O0O0OOOO000O0OO00 =str (int (time .time ()*1000 ))#line:77:ts = str(int(time.time() * 1000))
    O0OOOO0OO00OO000O =base64Encode (OOOO00O0000OO0O00 )#line:78:bsjduuid = base64Encode(jduuid)
    O0OOOOOO00O0OOOO0 =base64Encode ('%s_%s_%s_%s'%(random .randint (1 ,10000 ),random .randint (1 ,10000 ),random .randint (1 ,10000 ),random .randint (1 ,10000 )))#line:81:random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000)))
    OO0O0O0O00OOOO00O =random .choice (['Mi11Ultra','Mi11','Mi10'])#line:82:d_model = random.choice(['Mi11Ultra', 'Mi11', 'Mi10'])
    OO0O0O0O00OOOO00O =base64Encode (OO0O0O0O00OOOO00O )#line:83:d_model = base64Encode(d_model)
    return '{"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","ts":%s,"ridx":-1,"cipher":{"area":"%s","d_model":"%s","wifiBssid":"dW5hbw93bq==","osVersion":"CJS=","d_brand":"WQvrb21f","screen":"CtS1DIenCNqm","uuid":"%s","aid":"%s","openudid":"%s"},"ciphertype":5,"version":"1.2.0","appname":"com.jingdong.app.mall"}'%(int (O0O0OOOO000O0OO00 )-random .randint (100 ,1000 ),O0OOOOOO00O0OOOO0 ,OO0O0O0O00OOOO00O ,O0OOOO0OO00OO000O ,O0OOOO0OO00OO000O ,O0OOOO0OO00OO000O ),OOOO00O0000OO0O00 ,O0O0OOOO000O0OO00 #line:85:int(ts) - random.randint(100, 1000), area, d_model, bsjduuid, bsjduuid, bsjduuid), jduuid, ts
def get_sign (O0OO0000000OOOOO0 ,OOO00OOO0OOO0OO00 ,OO0OOO0O0O00OOO0O :str ="android",O0O00OO0000O0O000 :str ='11.2.8',O000O0O0OOOOOOO0O :str ='')->dict :#line:87:def get_sign(functionId, body, client : str="android", clientVersion : str='11.2.8',jduuid : str='') -> dict:
    if ver !=True :#line:88:if ver != True:
        return 900 #line:89:return 900
    if isinstance (OOO00OOO0OOO0OO00 ,dict ):#line:90:if isinstance(body,dict):#判断body数据类型是否为dict 是就转化为json
        O0O0OO0O0OOO00000 =OOO00OOO0OOO0OO00 #line:91:d=body
        OOO00OOO0OOO0OO00 =json .dumps (OOO00OOO0OOO0OO00 )#line:92:body=json.dumps(body)
    else :#line:93:else:
        O0O0OO0O0OOO00000 =json .loads (OOO00OOO0OOO0OO00 )#line:94:d=json.loads(body)
    if "eid"in O0O0OO0O0OOO00000 :#line:96:if "eid" in d:
        OOO0O0OOOO0O00OO0 =O0O0OO0O0OOO00000 ["eid"]#line:97:eid=d["eid"]
    else :#line:98:else:
        OOO0O0OOOO0O00OO0 =randomeid ()#line:99:eid=randomeid()
    OO0OOOO00O000OO0O ,O0000O0OO00OOO0O0 ,OOO00000OO00O0O00 =get_ep (O000O0O0OOOOOOO0O )#line:101:ep, suid, st = get_ep(jduuid)
    OO0O0O0O000O0OO00 =random .choice (["102","111","120"])#line:103:sv = random.choice(["102", "111", "120"])
    O0000O000O0000000 ="functionId=%s&body=%s&uuid=%s&client=%s&clientVersion=%s&st=%s&sv=%s"%(O0OO0000000OOOOO0 ,OOO00OOO0OOO0OO00 ,O0000O0OO00OOO0O0 ,OO0OOO0O0O00OOO0O ,O0O00OO0000O0O000 ,OOO00000OO00O0O00 ,OO0O0O0O000O0OO00 )#line:106:functionId, body, suid, client, clientVersion, st, sv)
    O00OO0OOO00OO0OO0 =sign_core (str .encode (O0000O000O0000000 ))#line:108:back_bytes = sign_core(str.encode(all_arg))
    O0OO0OOO0O0OO0O00 =hashlib .md5 (base64 .b64encode (O00OO0OOO00OO0OO0 )).hexdigest ()#line:109:sign = hashlib.md5(base64.b64encode(back_bytes)).hexdigest()
    O0OO0O0O0O00OO00O ={"functionId":O0OO0000000OOOOO0 ,"body":OOO00OOO0OOO0OO00 ,"clientVersion":O0O00OO0000O0O000 ,"client":OO0OOO0O0O00OOO0O ,"uuid":O0000O0OO00OOO0O0 ,"eid":OOO0O0OOOO0O00OO0 ,"ep":OO0OOOO00O000OO0O ,"st":OOO00000OO00O0O00 ,"sign":O0OO0OOO0O0OO0O00 ,"sv":OO0O0O0O000O0OO00 }#line:111:data={"functionId":functionId,"body":body,"clientVersion":clientVersion,"client":client,"uuid":suid,"eid":eid,"ep":ep,"st":st,"sign":sign,"sv":sv}
    O0OO0O0O0O00OO00O ["convertUrl"]='functionId=%s&body=%s&clientVersion=%s&client=%s&sdkVersion=31&lang=zh_CN&harmonyOs=0&networkType=wifi&oaid=%s&eid=%s&ef=1&ep=%s&st=%s&sign=%s&sv=%s'%(O0OO0000000OOOOO0 ,OOO00OOO0OOO0OO00 ,O0O00OO0000O0O000 ,OO0OOO0O0O00OOO0O ,O0000O0OO00OOO0O0 ,OOO0O0OOOO0O00OO0 ,urllib .parse .quote (OO0OOOO00O000OO0O ),OOO00000OO00O0O00 ,O0OO0OOO0O0OO0O00 ,OO0O0O0O000O0OO00 )#line:113:functionId,body, clientVersion, client, suid, eid, urllib.parse.quote(ep), st, sign, sv)
    O0OO0O0O0O00OO00O ["url"]='https://api.m.jd.com?%s'%(O0OO0O0O0O00OO00O ["convertUrl"])#line:114:data["url"]='https://api.m.jd.com?%s' % (data["convertUrl"])
    return O0OO0O0O0O00OO00O 