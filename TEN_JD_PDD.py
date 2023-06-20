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


try:
    cks = get_cookies()
    if not cks:
        sys.exit()
except:
    print("未获取到有效COOKIE,退出程序！")
    sys.exit()

class JD_PDD():
    def __init__(self):
        self.start = time.time()
        self.token = os.environ.get("TEN_TOKEN") if os.environ.get("TEN_TOKEN") else sys.exit('未获取到你的TEN_TOKEN')
        self.inviter = os.environ.get("TEN_inviter") if os.environ.get("TEN_inviter") else False
        self.scode = os.environ.get("TEN_scode") if os.environ.get("TEN_scode") else 1
        self.proxy = os.environ.get("TEN_proxy") if os.environ.get("TEN_proxy") else False
        self.threadsNum = int(os.environ.get("TEN_threadsNum") if os.environ.get("TEN_threadsNum") else 50)
        self.power_success = []
        self.power_failure = []
        self.not_log = []
        self.exit_event = threading.Event()
        self.coookie = cks[0]
        self.helpResult = {
            (1, '✅助力成功'),
            (2, '❌活动火爆'),
            (3, '❌没有助力次数'),
            (4, '❌助力次数用尽'),
            (6, '❌已助力')
        }
    def ver_code(self):
        try:
            self.verify = verify(self.token)
            if self.verify != True:
                sys.exit('❌授权未通过 程序自动退出！！！')
        except Exception as e:
            print(f'验证授权失败： {e}')
        try:
            self.stats = stats()
            if self.stats.status_code != False:
                self.linkId = self.stats.json()[f'linkId{self.scode}']
        except Exception as e:
            print(f'从云端获取inviter失败： {e}')
    def convert_ms_to_hours_minutes(self,milliseconds):
        seconds = milliseconds // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{hours}:{minutes}'

    def list_of_groups(self, init_list, children_list_len):
        list_of_groups = zip(*(iter(init_list),) * children_list_len)
        end_list = [list(i) for i in list_of_groups]
        count = len(init_list) % children_list_len
        end_list.append(init_list[-count:]) if count != 0 else end_list
        return end_list

    def H5API(self, functionId, body, cookie, appId):
        if self.verify != True:
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

        url = 'https://ten.ouklc.com/h5st'
        params = {
            'functionId': functionId,
            'body': json.dumps(body),
            'ua': ua,
            'pin': pt_pin,
            'appId': appId
        }
        try:
            response = requests.get(url, params=params, timeout=5)


        except Exception as e:
            if isinstance(e, requests.exceptions.Timeout):
                print(f"h5st 获取超时：{e}")
            else:
                print(f'h5st 获取失败：{e}')
            return False
        try:
            if response.status_code == 200:
                uuid = getUUID("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")
                body = response.json()['body'] + "&x-api-eid-token=" + x_api_eid_token(ua, cookie) + f"&uuid={uuid}&"
                body += "&build=1217&screen=390*844&networkType=3g&d_brand=iPhone&d_model=iPhone14,5&lang=zh_CN&osVersion=16.4.1&partner=-1&cthr=1"
                url = "https://api.m.jd.com"
                if self.proxy == False:
                    response = requests.post(url, headers=headers, data=body)
                else:
                    proxies = {
                        'http': f'{self.proxy}',
                        'https': f'{self.proxy}',
                    }
                    response = requests.post(url, headers=headers, data=body, proxies=proxies, timeout=5)

                return response
        except Exception as e:
            if isinstance(e, requests.exceptions.Timeout):
                # 处理超时异常
                print(f"助理超时：{e}")
            else:
                print(f'助理失败：{e}')
            return False
    def Result(self,inviter, cookie):
        try:
            if self.verify != True:
                sys.exit('❌授权未通过 程序自动退出！！！')
            response = self.H5API("inviteFissionBeforeHome", {'linkId': self.linkId, "isJdApp": True, 'inviter': inviter}, cookie,'02f8d')
            if int(response.status_code) != int(200):
                print(f'inviteFissionBeforeHome 接口：{response.status_code}')
                self.exit_event.set()
                return
            if int(response.json()['code']) == 0:
                for code, msg in self.helpResult:
                    if response.json()['data']['helpResult'] == int(code):
                        found_match = True
                        printf(cookie,
                               f"{response.status_code}  助力 →→ {response.json()['data']['nickName']} {response.json()['data']['helpResult']} {msg}")
                        if response.json()['data']['helpResult'] == 1:
                            self.power_success.append(cookie)
                        else:
                            self.power_failure.append(cookie)

                if not found_match:
                    msg = '❌未知状态 (可能是活动未开启！！！)'
                    self.power_failure.append(cookie)
                    printf(cookie,
                           f"{response.status_code}  助力 →→ {response.json()['data']['nickName']} {response.json()['data']['helpResult']} {msg}")

            else:
                printf(cookie, f"{response.json()['code']} →→ 💔{response.json()['errMsg']}")
                self.not_log.append(cookie)
        except Exception as e:
            msg = ''


    def main(self):
        self.ver_code()
        if self.verify != True:
            sys.exit('❌授权未通过 程序自动退出！！！')
        response = self.H5API("inviteFissionBeforeHome",
                         {'linkId': self.linkId, "isJdApp": True, 'inviter': self.stats.json()['inviter']}, self.coookie, '02f8d')
        if response.json()['data']['helpResult'] == 1:
            printf(self.coookie, '✅助力作者成功 谢谢你 你是个好人！！！')
        else:
            printf(self.coookie, '❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')
        if self.inviter == False:
            response = self.H5API('inviteFissionHome', {'linkId': self.linkId, "inviter": "", }, self.coookie, 'af89e').json()
            printf(self.coookie,
                   f'⏰剩余时间:{self.convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力:{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【助力码】:{response["data"]["inviter"]}')
            inviter = response["data"]["inviter"]
        else:
            inviter = self.inviter
        new_cks = self.list_of_groups(cks[1:len(cks)], self.threadsNum)
        for i, cookies in enumerate(new_cks, 1):
            print(f"\n##############并发第{i}组ck##############")
            threads = []
            print(f"****************提取{len(cookies) if cookies else 0}个COOKIE****************")
            for index, cookie in enumerate(cookies, 1):
                if self.exit_event.is_set():
                    # Event被设置，停止启动后续线程
                    sys.exit('403 程序自动退出！！！')
                thead_one = threading.Thread(target=self.Result, args=(inviter, cookie))
                threads.append(thead_one)  # 线程池添加线程
            for t in threads:
                t.start()
                if self.proxy == False:
                    time.sleep(2)
                    if self.exit_event.is_set():
                        sys.exit('403 程序自动退出！！！')
            for t in threads:
                t.join()
        print(
            f'\n\n\n##############清点人数##############\n  ✅助力成功:{len(self.power_success)}人 ❌助力失败:{len(self.power_failure)}人 💔未登录CK{len(self.not_log)}人 \n  ⏰耗时:{time.time() - self.start}')

if __name__ == '__main__':
    self = JD_PDD()
    self.main()
