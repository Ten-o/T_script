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
from utils.UTIL import *
try:
    from utils.TEN_UTIL import *
except:
    print('❌ 未检测到依赖 开始安装')
    load_so_file()
    from utils.TEN_UTIL import *


start = time.time()


#scode  定义 1为特价 2为京东
TEN_TOKEN = os.environ.get("TEN_TOKEN") if os.environ.get("TEN_TOKEN") else sys.exit('❌未获取到TEN_TOKEN变量 程序自动退出')
TEN_inviter = os.environ.get("TEN_inviter") if os.environ.get("TEN_inviter") else False
TEN_scode = os.environ.get("TEN_scode") if os.environ.get("TEN_scode") else 1





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



def main():
    response = H5API('POST', "inviteFissionBeforeHome", {'linkId': linkId, "isJdApp": True, 'inviter': stats.json()['inviter']}, cks[0],'02f8d')
    if response[1]['data']['helpResult'] == 1:
        printf(cks[0], '✅助力作者成功 谢谢你 你是个好人！！！')
    else:
        printf(cks[0],'❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')
        time.sleep(2)

    if TEN_inviter == False:
        response = H5API('POST','inviteFissionHome', {'linkId': linkId, "inviter": "", }, cks[0], 'af89e')
        if response == 900:
            sys.exit('❌授权未通过 程序自动退出！！！')
        printf(cks[0],
               f'⏰剩余时间:{convert_ms_to_hours_minutes(response[1]["data"]["countDownTime"])} 🎉已获取助力:{response[1]["data"]["prizeNum"] + response[1]["data"]["drawPrizeNum"]}次 ✅【助力码】:{response[1]["data"]["inviter"]}')
        inviter = response[1]["data"]["inviter"]
        time.sleep(3)
    else:
        inviter = TEN_inviter
    print(f"****************开始助理****************")
    for i, cookie in enumerate(cks[1:], 1):
        response = H5API('POST',"inviteFissionBeforeHome", {'linkId': linkId, "isJdApp": True, 'inviter': inviter}, cookie, '02f8d')
        if response[0] == 900:
            sys.exit('❌授权未通过 程序自动退出！！！')
        res = response[1]
        if int(res['code']) == int(0):
            if res['data']['helpResult'] == 1:
                msg = '✅助力成功'
                power_success.append(cookie)
            elif res['data']['helpResult'] == 6:
                msg = '❌已助力'
                power_failure.append(cookie)
            elif res['data']['helpResult'] == 3:
                msg = '❌没有助力次数'
                power_failure.append(cookie)
            elif res['data']['helpResult'] == 4:
                msg = '❌助力次数用尽'
                power_failure.append(cookie)
            elif res['data']['helpResult'] == 2:
                msg = '❌活动火爆'
                power_failure.append(cookie)
                time.sleep(10)
            else:
                msg = '❌未知状态'
                power_failure.append(cookie)
            printf(cookie, f" 200  →→ 第{i}位 →→ 去助力 →→ {res['data']['nickName']} {msg}")
        else:
            printf(cookie, f" {res['code']} →→ 第{i}位 →→  💔{res['errMsg']}")
            not_log.append(cookie)
            time.sleep(5)
    print(
        f'\n\n##############清点人数##############\n  ✅助力成功:{len(power_success)}人 ❌助力失败:{len(power_failure)}人 💔未登录COOOKIE{len(not_log)}\n  ⏰耗时:{time.time() - start}')

if __name__ == '__main__':
    main()