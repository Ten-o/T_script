#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: TEN_JD_PDD.py(邀好友赢现金-助理)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-助理');
"""


from utils.logger import setup_logger
from utils.X_API_EID_TOKEN import *
from utils.User_agent import *
import asyncio, aiohttp, re, os, sys, threading, concurrent.futures, time, json
from utils.jdCookie import get_cookies

try:
    ck = get_cookies()
    if not ck:
        sys.exit()
except:
    print("未获取到有效COOKIE,退出程序！")
    sys.exit()


class TEN_JD_PDD:
    def __init__(self):
        self.log = setup_logger()
        self.start = time.time()
        self.token = os.environ.get("TEN_TOKEN") if os.environ.get(
            "TEN_TOKEN") else False
        self.inviter = os.environ.get("TEN_inviter") if os.environ.get("TEN_inviter") else False
        self.scode = os.environ.get("TEN_scode") if os.environ.get("TEN_scode") else '0'
        self.proxy = os.environ.get("TEN_proxy") if os.environ.get("TEN_proxy") else False
        self.semaphore = asyncio.Semaphore(int(os.environ.get("TEN_threadsNum") if os.environ.get("TEN_threadsNum") else 50))
        self.power_success = []
        self.power_failure = []
        self.not_log = []
        self.exit_event = threading.Event()
        self.coookie = ck[0]
        self.helpResult = {
            (1, '✅助力成功'),
            (2, '❌活动火爆'),
            (3, '❌没有助力次数'),
            (4, '❌助力次数用尽'),
            (6, '❌已助力')
        }
        self.verify_result = False
        self.linkId = []
        self.inviter_help = ''
        self.version = '1.3.6'
        self.exit_condition = int(os.environ.get("TEN_EXIT") if os.environ.get("TEN_EXIT") else 99999)
        self.lock = threading.Lock()

    def pt_pin(self, cookie):
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        return pt_pin


    # def fetch_proxies_from_api(self, num):
    #     try:
    #         response = requests.get(self.proxy, timeout=5)
    #         proxies = response.text.splitlines()
    #         self.log.debug(f'获取到代理IP：{len(proxies)}个')
    #         with self.lock:
    #             self.proxy = proxies
    #     except Exception as e:
    #         self.log.error(f'无法获取代理列表: {str(e)}')


    def convert_ms_to_hours_minutes(self, milliseconds):
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

    async def retry_with_backoff(self, coroutine, max_retries, name, backoff_seconds=0):
        for retry_count in range(max_retries):
            retry_failed = False  # 添加一个标志来表示是否已输出异常
            try:
                return await coroutine()
            except asyncio.TimeoutError:
                if not retry_failed:  # 如果尚未输出异常日志
                    self.log.warning(f'第{retry_count + 1}次重试 {name} 请求超时')
                    retry_failed = True  # 标记已输出异常
                await asyncio.sleep(backoff_seconds)
            except Exception as e:
                if not retry_failed:  # 如果尚未输出异常日志
                    self.log.warning(f'第{retry_count + 1}次重试 {name} 出错：{e}')
                    retry_failed = True  # 标记已输出异常
                await asyncio.sleep(backoff_seconds)

            if retry_failed and retry_count == max_retries - 1:
                self.log.error(f'{name} 重试{max_retries}次后仍然发生异常')
                return False, False, False


    async def verify(self):
        self.verify_result = True
        async def verify_internal():
            url = 'https://api.ixu.cc/verify'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, data={'TOKEN': self.token}, timeout=3) as response:
                    data = await response.json()
                    if response.status == 200:
                        self.verify_result = True
                        self.log.info(f'认证通过 UserId：{data["user_id"]}')
                        return data  # 成功后返回数据并退出函数
                    else:
                        self.log.error(f"授权未通过:{data['error']}")
                        sys.exit()

        return await self.retry_with_backoff(verify_internal, 3, 'verify')

    def parse_version(self, version_str):
        return list(map(int, version_str.split('.')))

    def is_major_update(self, current_version, new_version):
        if current_version[1] != new_version[1]:
            return True
        elif current_version[0] != new_version[0]:
            return True
        else:
            return False

    def is_force_update(self, current_version, new_version):
        if self.is_major_update(current_version, new_version):
            return True
        elif new_version[2] - current_version[2] >= 3:
            return True
        elif new_version[2] < current_version[2]:
            return True
        else:
            return False

    async def LinkId(self):
        async def Link():
            if self.verify_result != True:
                await self.verify()
            if self.verify_result != True:
                self.log.error("授权未通过 退出")
                sys.exit()
            url = 'https://api.ixu.cc/status/inviter.json'
            async with aiohttp.ClientSession() as session:
                async with session.get(url,  timeout=3) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['stats'] != 'True':
                            self.log.error(f"{data['err_text']}")
                            sys.exit()
                        self.inviter_help = data['inviter']
                        if self.is_force_update(self.parse_version(self.version), self.parse_version(data["version"])):
                            self.log.error(
                                f'强制更新 云端版本:{data["version"]},当前版本:{self.version} {data["upload_text"]}')
                            sys.exit()
                        else:
                            self.log.debug(f'云端版本:{data["version"]},当前版本:{self.version}')
                        if len(data['text']) > 0:
                            self.log.debug(f'那女孩对你说:{data["text"]}')
                        if self.scode == 'ALL' or self.scode == 'all':
                            for i in data['linkId']:
                                self.linkId.append(i)
                                self.log.info(f'云端获取到linkId:{i}')
                            return True
                        else:
                            self.linkId.append(data['linkId'][int(self.scode) - 1])
                            self.log.info(f'云端获取到linkId:{data["linkId"][int(self.scode) - 1]}')
                            return True
                    else:
                        self.log.error('未获取到linkId 重试')

        return await self.retry_with_backoff(Link, 3, 'linkId')

    async def Get_H5st(self, functionId, body, ua, appId, cookie):
        async def H5st():
            if self.verify_result != True:
                self.log.error("授权未通过 退出")
                sys.exit()
            url = 'https://api.ouklc.com/api/h5st4'
            opt = {
                "functionId": functionId,
                'appId': appId,  # h5st里面的appId
                "appid": "activities_platform",
                "clientVersion": "4.2.0",
                "client": "ios",
                'body': body,
                "version": '4.1',
                "ua": ua
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=opt, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['body']
                    else:
                        return await self.retry_with_backoff(H5st, 3, 'H5st')

        return await self.retry_with_backoff(H5st, 3, 'H5st')

    async def Get_H5_Api(self, functionId, data, cookie, appId):
        async def H5_Api(data):
            if self.verify_result != True:
                self.log.error("授权未通过 退出")
                sys.exit()
            ua = generate_random_user_agent()
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-cn",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "api.m.jd.com",
                "Referer": "https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html",
                "Origin": "https://prodev.m.jd.com",
                "Cookie": cookie,
                "User-Agent": ua
            }
            uuid = getUUID("xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx")
            data = await self.Get_H5st(functionId, data, ua, appId, cookie)
            # body = str(data) + "&x-api-eid-token=" + x_api_eid_token(ua, cookie) + f"&uuid={uuid}&"
            url = "https://api.m.jd.com"
            async with aiohttp.ClientSession() as session:
                if self.proxy == False:
                    async with session.post(url, headers=headers, data=data, timeout=5) as response:
                        if response.status == 200:
                            return await response.json()

                        else:
                            self.log.error(f'重试 请求结果：{response.status}')
                else:
                    async with session.post(url, headers=headers, data=data, timeout=5, proxy=self.proxy) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            self.log.error(f'重试 请求结果：{response.status}')
                            await self.Get_H5_Api(functionId, data, cookie, appId)

        return await self.retry_with_backoff(lambda: H5_Api(data), 3, 'H5st_Api')

    async def Result(self, index, inviter, cookie):
        if self.exit_condition and len(self.power_success) >= self.exit_condition:
            sys.exit(f'已助理:{len(self.power_success)}')

        async def Result_test():
            found_match = False
            if self.verify_result != True:
                self.log.error("授权未通过 退出")
                sys.exit()
            for linkId in self.linkId:
                response = await self.Get_H5_Api("inviteFissionhelp",
                                                 {'linkId': linkId, "isJdApp": True, 'inviter': inviter}, cookie,
                                                 'c5389')
                if int(response['code']) == 0:
                    for code, msg in self.helpResult:
                        if response['data']['helpResult'] == int(code):
                            found_match = True
                            self.log.info(
                                f"Id:{linkId[:4] + '****' + linkId[-4:]}|助理:{response['data']['nickName']}|{response['data']['helpResult']}|第{index}次|{self.pt_pin(cookie)}|{msg}")
                            if response['data']['helpResult'] == 1:
                                self.power_success.append(cookie)
                            else:
                                self.power_failure.append(cookie)
                    if not found_match:
                        msg = '❌未知状态 (可能是活动未开启！！！)'
                        self.power_failure.append(cookie)
                        self.log.info(
                            f"Id:{linkId[:4] + '****' + linkId[-4:]}|助理:{response['data']['nickName']}|{response['data']['helpResult']}|第{index}次|{self.pt_pin(cookie)}|{msg}")
                else:
                    self.log.info(f"{self.pt_pin(cookie)}{response['code']} 结果:💔{response['errMsg']}")
                    self.not_log.append(cookie)

        return await self.retry_with_backoff(Result_test, 3, 'Result')

    async def main(self):
        await self.verify()
        await self.LinkId()
        if self.verify_result != True:
            await self.verify()
        if self.verify_result != True:
            self.log.error("授权未通过 退出")
            sys.exit()
        for i in self.linkId:
            response = await self.Get_H5_Api("inviteFissionhelp",
                                             {'linkId': i, "isJdApp": True, 'inviter': self.inviter_help},
                                             self.coookie, 'c5389')
            if response['success'] == False and response['code'] == 1000:
                self.log.info(f"{response['errMsg']}")
                sys.exit()
            if response['data']['helpResult'] == 1:
                self.log.info(f'{self.pt_pin(self.coookie)} ✅助力作者成功 谢谢你 你是个好人！！！')
            else:
                self.log.info(f'{self.pt_pin(self.coookie)} ❌助理作者失败 下次记得把助理留给我 呜呜呜！！！')

        if self.inviter == False:
            for i in self.linkId:
                response = await self.Get_H5_Api('inviteFissionHome', {'linkId': i, "inviter": "", }, self.coookie,
                                                 'eb67b')
                self.log.info(
                    f'{self.pt_pin(self.coookie)} ⏰剩余时间:{self.convert_ms_to_hours_minutes(response["data"]["countDownTime"])} 🎉已获取助力:{response["data"]["prizeNum"] + response["data"]["drawPrizeNum"]}次 ✅【LinkId】:{i}')
                self.inviter = response["data"]["inviter"]
            self.log.info(f'{self.pt_pin(self.coookie)} ✅助理码: {self.inviter}')

        if self.proxy != False:
            self.log.info(f"##############开始并发[线程数:{self.semaphore._value}]##############")
            tasks = []

            # for index, cookie in enumerate(ck, 1):
            #     async with self.semaphore:
            #         task = asyncio.create_task(self.Result(self.inviter, cookie))
            #         tasks.append(task)
            #
            # await asyncio.gather(*tasks)
            async def worker(index, cookie):
                async with self.semaphore:
                    task = asyncio.create_task(self.Result(index, self.inviter, cookie))
                    if self.exit_condition and len(self.power_success) >= self.exit_condition:
                        sys.exit(f'已助理:{len(self.power_success)}')
                    return await task

            async def main():
                tasks = []
                for index, cookie in enumerate(ck, 1):
                    if self.exit_condition and len(self.power_success) >= self.exit_condition:
                        sys.exit(f'已助理:{len(self.power_success)}')
                    task = asyncio.create_task(worker(index, cookie))
                    tasks.append(task)
                await asyncio.gather(*tasks)

            await main()
            # for index, cookie in enumerate(ck, 1):
            #     task = asyncio.create_task(worker(index, cookie))
            #     tasks.append(task)
            # await asyncio.gather(*tasks)

        else:
            self.log.info(f"##############开始任务##############")
            for index, cookie in enumerate(ck, 1):
                await self.Result(index, self.inviter, cookie)
                if self.exit_condition and len(self.power_success) >= self.exit_condition:
                    sys.exit(f'已助理:{len(self.power_success)}')
                await asyncio.sleep(0.5)

        self.log.info(f"##############清点人数##############")
        self.log.info(
            f"✅助力成功:{len(self.power_success)}人 ❌助力失败:{len(self.power_failure)}人 💔未登录CK{len(self.not_log)}人")
        self.log.info(f" ⏰耗时:{time.time() - self.start}")


if __name__ == '__main__':
    pdd = TEN_JD_PDD()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pdd.main())
    loop.close()
