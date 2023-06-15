#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_invite_H5_31.py(邀好友赢现金-助理)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-助理');
"""
import sys
from jdCookie import *
from utils.UTIL import *
from utils.X_API_EID_TOKEN import *
from utils.User_agent import generate_random_user_agent
try:
    from utils.TEN_UTIL import *
except:
    print('❌ 未检测到依赖 开始安装')
    load_so_file()
    from utils.TEN_UTIL import *



start = time.time()



#scode  定义 1为特价 2为京东
TEN_TOKEN = os.environ.get("TEN_TOKEN") if os.environ.get("TEN_TOKEN") else sys.exit('未获取到你的TEN_TOKEN')
TEN_inviter = os.environ.get("TEN_inviter") if os.environ.get("TEN_inviter") else False
TEN_scode = os.environ.get("TEN_scode") if os.environ.get("TEN_scode") else 1
proxy = os.environ.get("Ten_proxy") if os.environ.get("Ten_proxy") else False


threadsNum = 50
exit_event = threading.Event()

try:
    getCk = get_cookies()
    cks = getCk
    if not cks:
        sys.exit()
except:
    print("未获取到有效COOKIE,退出程序！")
    sys.exit()

verify = verify(TEN_TOKEN)
print(verify)
if verify != True:
    sys.exit('❌授权未通过 程序自动退出！！！')


stats = stats()
if stats.status_code != False:
    linkId = stats.json()[f'linkId{TEN_scode}']


power_success = []
power_failure = []
not_log = []


def convert_ms_to_hours_minutes(milliseconds):
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}:{minutes}'


def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list
def H5API(functionId, body, cookie, appId):
    if verify != True:
        sys.exit('❌授权未通过 程序自动退出！！！')
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
        uuid="5616237366134353-4383338333661383"
        uuid = getUUID("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")
        body = result['body'] + "&x-api-eid-token="+x_api_eid_token(ua, cookie) + f"&uuid={uuid}&"
        body += "&build=1217&screen=390*844&networkType=3g&d_brand=iPhone&d_model=iPhone14,5&lang=zh_CN&osVersion=16.4.1&partner=-1&cthr=1"
        url = "https://api.m.jd.com"
        if proxy == False:
            response = requests.post(url, headers=headers, data=body)
        else:
            response = requests.post(url, headers=headers, data=body, proxies=proxy)

        return response


def Result(inviter,cookie):
    response = H5API("inviteFissionBeforeHome", {'linkId':linkId, "isJdApp":True, 'inviter':inviter}, cookie, '02f8d')
    if int(response.status_code) != int(200):
        print(f'inviteFissionBeforeHome 接口：{response.status_code}')
        exit_event.set()
        return
    if int(response.json()['code']) == 0:
        if response.json()['data']['helpResult'] == 1:
            msg = '✅助力成功'
            power_success.append(cookie)
        elif response.json()['data']['helpResult'] == 6:
            msg = '❌已助力'
            power_failure.append(cookie)
        elif response.json()['data']['helpResult'] == 3:
            msg = '❌没有助力次数'
            power_failure.append(cookie)
        elif response.json()['data']['helpResult'] == 4:
            msg = '❌助力次数用尽'
            power_failure.append(cookie)
        elif response.json()['data']['helpResult'] == 2:
            msg = '❌活动火爆'
            power_failure.append(cookie)
        else:
            msg = '❌未知状态'
            power_failure.append(cookie)
        printf(cookie,
               f"{response.status_code}  助力 →→ {response.json()['data']['nickName']} {msg}")
    else:
        printf(cookie, f"{response.json()['code']} →→ 💔{response.json()['errMsg']}")
        not_log.append(cookie)




def main():
    if verify != True:
        sys.exit('❌授权未通过 程序自动退出！！！')
    cookie = cks[0]
    response = H5API("inviteFissionBeforeHome", {'linkId': linkId, "isJdApp": True, 'inviter': stats.json()['inviter']}, cookie,'02f8d')
    if response.json()['data']['helpResult'] == 1:
        printf(cks[0], '✅助力作者成功 谢谢你 你是个好人！！！')
    else:
        printf(cks[0],'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')
        time.sleep(2)
    if TEN_inviter == False:
        response = H5API('inviteFissionHome', {'linkId': linkId, "inviter": "", }, cookie, 'af89e').json()
        printf(cookie,
               f'⏰剩余时间:{convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力:{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【助力码】:{response["data"]["inviter"]}')
        inviter = response["data"]["inviter"]
    else:
        inviter = TEN_inviter
    time.sleep(1)
    new_cks = list_of_groups(cks[1:len(cks)], threadsNum)
    for i, cookies in enumerate(new_cks, 1):
        print(f"\n##############并发第{i}组ck##############")
        threads = []
        print(f"****************提取{len(cookies) if cookies else 0}个COOKIE****************")
        for index, cookie in enumerate(cookies, 1):
            if exit_event.is_set():
                # Event被设置，停止启动后续线程
                sys.exit('403 程序自动退出！！！')
            thead_one = threading.Thread(target=Result, args=(inviter, cookie))
            threads.append(thead_one)  # 线程池添加线程
        for t in threads:
            t.start()
            if proxy == False:
                time.sleep(2)
                if exit_event.is_set():
                    sys.exit('403 程序自动退出！！！')
        for t in threads:
            t.join()
    print(
        f'\n\n\n##############清点人数##############\n  ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录CK{len(not_log)}人 \n  ⏰耗时:{time.time() - start}')


if __name__ == '__main__':
    main()