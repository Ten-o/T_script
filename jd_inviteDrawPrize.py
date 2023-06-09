"""
File: jd_inviteDrawPrize.py(邀好友赢现金-抽奖)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-抽奖');
"""


import time, requests, sys, re, json, os,uuid, random
import datetime
from urllib.parse import  unquote, unquote_plus
from utils.UTIL import *
from utils.User_agent import *
from utils.X_API_EID_TOKEN import *
try:
    from utils.TEN_UTIL import *
except:
    print('❌ 未检测到依赖 开始安装')
    load_so_file()
    from utils.TEN_UTIL import *


NUMBER_OF = os.environ.get("draw_numer") if os.environ.get("draw_numer") else 3
cookie = os.environ.get("draw_cookie") if os.environ.get("draw_cookie") else sys.exit('❌未获取到draw_cookie变量 程序自动退出')
TEN_TOKEN = os.environ.get("TEN_TOKEN") if os.environ.get("TEN_TOKEN") else sys.exit('❌未获取到TEN_TOKEN变量 程序自动退出')
TEN_scode = os.environ.get("TEN_scode") if os.environ.get("TEN_scode") else 1


activityUrl = "https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html?inviter=HIzs4VDTQOYH_nRbcPIQ7CFCa9577iZwBlQUx0yTITw&channelType=1&femobile=femobile&activityChannel=jdlite"
data_dict = {}


verify = verify(TEN_TOKEN)
print(verify)
if verify != True:
    sys.exit('❌授权未通过 程序自动退出！！！')


stats = stats()
if stats.status_code != False:
    linkId = stats.json()[f'linkId{TEN_scode}']


def base64Encode(string):
    oldBin = ""
    tempStr = []
    result = ""
    base64_list = 'KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/'
    for ch in string:
        oldBin += "{:08}".format(int(str(bin(ord(ch))).replace("0b", "")))
    for i in range(0, len(oldBin), 6):
        tempStr.append("{:<06}".format(oldBin[i:i + 6]))
    for item in tempStr:
        result = result + base64_list[int(item, 2)]
    if len(result) % 4 == 2:
        result += "=="
    elif len(result) % 4 == 3:
        result += "="
    return result

def getTimestamp():
    return int(round(time.time() * 1000))

def userAgent():
    ep = {
        "ciphertype": 5,
        "cipher": {
            "ud": base64Encode(
                ''.join(random.sample('0123456789abcdef0123456789abcdef0123456789abcdef', 40))),
            "sv": "CJSkDy42",
            "iad": base64Encode(str(uuid.uuid1(uuid.getnode())).upper())
            # "iad": base64Encode("c95bcbd6-3cd4-460a-a39d-b85d8e9d59a2".upper())
        },
        "ts": int(time.time()),
        "hdid": "JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=",
        "version": "1.0.3",
        "appname": "com.360buy.jdmobile",
        "ridx": -1
    }
    return f"jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/{quote(json.dumps(ep).replace(' ', ''))};Mozilla/5.0 (iPhone; CPU iPhone OS 12_7_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E126;supportJDSHWK/1"


def printf(cookie, T):
    try:
        pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    except IndexError:
        pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    print(f"{str(datetime.datetime.now())[0:22]}->{pt_pin}->{T}")

def getUUID(x="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", t=0):
    if isinstance(x, int):
        x = "x" * x
    uuid = re.sub("[xy]", lambda x: str(int((16 * random.random()) // 1) if x.group() == "x" else ((3 & int(x.group(), 16)) | 8)), x)
    return uuid

def H5API(functionId, body, cookie, appId):
    # ua = userAgent()
    # ua = random.choice(USER_AGENTS)
    # ua = 'jdltapp;iPhone;4.2.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1217;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22CJGzCwS1ZQCmDzYmYzrsYJU5Y2Y1ZWGmDWZrZtO2YzHuCzHuYwC5Cq%3D%3D%22%2C%22sv%22%3A%22CJYkDM4n%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1685502010%2C%22hdid%22%3A%22M1j35qhispl99TdfCvaiQodeZDjJzRZ5%5C%2F8PEE1%5C%2Fv0I4%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.jd.jdmobilelite%22%2C%22ridx%22%3A1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;'

    ua = generate_random_user_agent()
    try:
        pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    except IndexError:
        pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-cn",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "api.m.jd.com",
        "Referer": "https://prodev.m.jd.com/",
        "Origin": "https://prodev.m.jd.com",
        "Cookie": cookie,
        "User-Agent": ua
    }

    urla = 'https://ten.ouklc.com/h5st'
    params = {
        'functionId': functionId,
        'body': json.dumps(body),
        'ua': ua,
        'pin': pt_pin,
        'appId': appId
    }
    response = requests.get(urla, params=params)
    if response.status_code == 200:
        result = response.json()
        body = result['body']
        url = "https://api.m.jd.com"
        response = requests.post(url, headers=headers, data=body)
        return response

def inviteFissionDrawPrize(cookie):
    url = "https://api.m.jd.com/"
    # data = 'functionId=inviteFissionDrawPrize&body={{"linkId":"{linkId}"}}&t=1684891089602&appid=activities_platform&client=ios&clientVersion=4.2.0&h5st=20230524091809610;3661921034167168;c02c6;tk02web331cb341lMngzeDMrMysyAV-ygRzQmWiviZOtObeBJ8fdwuKsp_70EWTjJVKF4ME4EoSn_rBAwZkgL167NT5S;37520995a8ab73b2c8d5425c82095f0ba6055625bba7af32ecb258de5b80fdef;3.1;1684891089610;7414c4e56278580a133b60b72a30beb2764d2e61c66a5620e8e838e06644d1bf734f45e55381a9c227bd506a8ea6832d223716652cee6d293327f55f82b9ae6d67c5afac84eff2a44960858e1981c32bb8c0c4222649ec402519fe414d7ee8e944b69d78e5b8c76501b39210d7a831271f9b4dada85ae203278969712f23301ed140e58007758665bdd87d535c5a57e70059e89db5a8ffb285845b1107266a7af8c44b88edfb338419251c24fa6726bb'.format(linkId=linkId)
    # print(data)
    # headers = {
    #         'Connection': 'keep-alive',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #         'User-Agent': 'jdltapp;iPhone;4.2.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1217;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22CJGzCwS1ZQCmDzYmYzrsYJU5Y2Y1ZWGmDWZrZtO2YzHuCzHuYwC5Cq%3D%3D%22%2C%22sv%22%3A%22CJYkDM4n%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1684891082%2C%22hdid%22%3A%22M1j35qhispl99TdfCvaiQodeZDjJzRZ5%5C%2F8PEE1%5C%2Fv0I4%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.jd.jdmobilelite%22%2C%22ridx%22%3A1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;',
    #         'Cookie': cookie,
    #         'Host': 'api.m.jd.com',
    #         'Referer': activityUrl,
    #         'Origin': 'https://prodev.m.jd.com',
    #         'Accept-Language': 'zh-Hans-CN;q=1 en-CN;q=0.9',
    #         'Accept': '*/*'
    # }
    # response = requests.request("POST", url, headers=headers, data=data)
    response = H5API("inviteFissionDrawPrize", {"linkId": linkId, "lbs": "null"}, cookie,
                     'c02c6')
    if response.status_code == 200:
        res = response.json()
        if res['data']:
            return response.status_code, res['data']['prizeValue'], res['data']['rewardType']
        else:
            return response.status_code, response.text

def superRedBagList(cookie, pageNum):
    response = H5API("superRedBagList", {"linkId": linkId, "pageNum": pageNum, "pageSize": 100, "business": "fission"}, cookie,
                     'f2b1d')
    if response.status_code != 200:
        print(f'❌ 获取提现列表接口：{response.status_code }')
        sys.exit()
    res = response.json()
    if res['data']:
        return res['data']
    else:
        printf(cookie, f"{response.status_code} {res}")
        return response.text

def apCashWithDraw(cookie, id, poolBaseId, prizeGroupId, prizeBaseId):
    try:
        response = H5API("apCashWithDraw", {"linkId": linkId,
                "businessSource": "NONE",
                "base":
                    {
                        "id": id,
                        "business": "fission",
                        "poolBaseId": poolBaseId,
                        "prizeGroupId": prizeGroupId,
                        "prizeBaseId": prizeBaseId,
                        "prizeType": 4
                    }
                }, cookie, '8c6ae')
        if response.status_code == 200:
            res = response.json()
            print(res)
            if res['data']:
                return res['data']
            else:
                printf(cookie, f"{response.status_code} {res}")
        else:
            print(f'{response.status_code}')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    cash = []
    successful = []
    total = 0
    i = 0
    redpacket = []
    MEASURE_WATER = []
    while True:
        info = inviteFissionDrawPrize(cookie)
        if "抽奖次数已用完" in info[1]:
            printf(cookie, f"{info[0]} ⚠️抽奖次数已用完")
            break
        elif "本场活动已结束" in info[1]:
            printf(cookie, f"{info[0]} ⏰本场活动已结束了,快去重新开始吧")
            sys.exit()
        if info:
            total += 1
            if info[2] == 1:
                printf(cookie, f"{info[0]} 🎫获得{info[1]}优惠券")
                MEASURE_WATER.append(info[1])
            elif info[2] == 2:
                printf(cookie, f"{info[0]} 🧧获得{info[1]}红包")
                redpacket.append(info[1])
                MEASURE_WATER.append(info[1])
            else:
                printf(cookie, f"{info[0]} 💵获得{info[1]}现金")
                cash.append(info[1])
        if len(MEASURE_WATER) >= int(NUMBER_OF):
            if len(cash) < 1:
                sys.exit(f'❌未抽中现金 可能没水 已自动退出！！！')

    total_amount = '{:.2f}'.format(sum([float(x) for x in cash]))
    print(f"****************抽奖结束,共抽奖{total}次,💵获得:{total_amount}元现金,🧧获得:{'{:.2f}'.format(sum([float(x) for x in redpacket]))}元红包,开始提现****************")
    wamst = True
    while wamst:
        print(f"\n****************开始获取第{i + 1}页奖励列表****************\n")
        info = superRedBagList(cookie, i)
        i += 1
        items = info['items']
        if not items:
            break
        for item in items:
            id = item['id']
            amount = item['amount']
            prizeType = item['prizeType']
            state = item['state']
            prizeConfigName = item['prizeConfigName']
            prizeGroupId = item['prizeGroupId']
            poolBaseId = item['poolBaseId']
            prizeBaseId = item['prizeBaseId']
            date_obj = datetime.datetime.strptime(item['startTime'], "%Y-%m-%d %H:%M:%S")
            delta = datetime.datetime.now() - date_obj
            # if delta >= datetime.timedelta(hours=24):
            #     print('24小时内的提现记录已检测完毕')
            #     wamst = False
            #     break
            if int(i) >= 100:
                wamst = False
                break

            if prizeType == 4 and state != 3:
                cashInfo = apCashWithDraw(cookie, id, poolBaseId, prizeGroupId, prizeBaseId)
                if int(cashInfo['status'])== 310:
                    printf(cookie, f"✅{amount}现金 提现成功")
                    successful.append(amount)
                    time.sleep(3)
                elif int(cashInfo['status']) == 50056 or int(cashInfo['status']) == 50001:
                    printf(cookie, f"{amount}现金 📔记录缓存:{cashInfo['status']} {cashInfo['message']}")
                    data = {
                        'cookie': cookie,
                        'numbers': (id, poolBaseId, prizeGroupId, prizeBaseId)}
                    data_dict[id] = data
                    time.sleep(3)
                else:
                    printf(cookie, f"{amount}现金 ❌提现错误:{cashInfo['status']} {cashInfo['message']}")
            else:
                continue
        time.sleep(10)
    print(f"\n****************提现结束,成功提现{'{:.2f}'.format(sum([float(x) for x in successful]))}元****************\n")
    if len(data_dict) != 0:
        print(f"****************有{len(data_dict)}笔未成功提现, 重新发起提现****************")
        for i in data_dict:
            cashInfo = apCashWithDraw(data_dict[i]['cookie'], data_dict[i]['numbers'][0], data_dict[i]['numbers'][1], data_dict[i]['numbers'][2], data_dict[i]['numbers'][3])
            if int(cashInfo['status']) == 310:
                printf(cookie, f"✅{cashInfo['record']['amount']}现金 提现成功")
                successful.append(cashInfo['record']['amount'])
                time.sleep(3)
            else:
                printf(cookie, f"❌提现错误:{cashInfo['status']} {cashInfo['message']}")

            time.sleep(6)
    print(f"\n****************提现结束,开始清点****************\n  🎁共抽奖{total}次  🧧获得:{'{:.2f}'.format(sum([float(x) for x in redpacket]))}元红包\n  💵获得{total_amount}元现金 ✅成功提现:{'{:.2f}'.format(sum([float(x) for x in successful]))}元")
