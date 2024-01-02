# -*- coding: utf-8 -*-
"""
File: TEN_JD_PDD_DRAW.py(邀好友赢现金-领现金)
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-领现金');
@author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
@software: PyCharm
@file: TEN_JD_PDD_DRAW.py
"""

from utils.logger import setup_logger
from utils.X_API_EID_TOKEN import *
from utils.User_agent import  generate_random_user_agent
import asyncio, aiohttp, re, os, sys, threading, concurrent.futures, time, json
from utils.jdCookie import get_cookies
import time

try:
    ck = get_cookies()
    if not ck:
        sys.exit()
except:
    sys.exit("未获取到有效COOKIE,退出程序！")


class TEN_JD_PDD_DRAW(object):
    def __init__(self):
        self.log = setup_logger()
        self.ua = generate_random_user_agent()
        self.page = 10
        self.start = time.time()
        self.token = os.environ.get("TEN_TOKEN") if os.environ.get("TEN_TOKEN") else False
        self.scode = os.environ.get("TEN_scode") if os.environ.get("TEN_scode") else 'all'
        self.proxy = os.environ.get("TEN_proxy") if os.environ.get("TEN_proxy") else False
        self.numer_og = os.environ.get("draw_numer") if os.environ.get("draw_numer") else 3
        self.activityUrl = "https://pro.m.jd.com"
        self.cookie = os.environ.get("draw_cookie") if os.environ.get("draw_cookie") else ck[0]
        self.linkId = []
        self.amount = 0
        self.leftAmount = 0
        self.verify_result = False
        self.txj_status = os.environ.get("txj_status") if os.environ.get("txj_status") else False
        self.inviter = ''
        self.power_success = []
        self.power_failure = []
        self.redpacket = []
        self.cash = []
        self.cash_redpacket = []
        self.helpResult = {
            (1, '✅助力成功'),
            (2, '❌活动火爆'),
            (3, '❌没有助力次数'),
            (4, '❌助力次数用尽'),
            (6, '❌已助力')
        }
        self.rewardType = {
            1: {'msg': '优惠券🎫'},
            2: {'msg': '红包🧧'},
            6: {'msg': '惊喜小礼包🎫'},
        }
        self.successful = []

    async def retry_with_backoff(self, coroutine, max_retries, name, backoff_seconds=0):
        for retry_count in range(max_retries):
            retry_failed = False  # 添加一个标志来表示是否已输出异常
            try:
                return await coroutine()
            except asyncio.TimeoutError:
                if not retry_failed:  # 如果尚未输出异常日志
                    self.log.debug(f'第{retry_count + 1}次重试 {name} 请求超时')
                    retry_failed = True  # 标记已输出异常
                await asyncio.sleep(backoff_seconds)
            except Exception as e:
                if not retry_failed:  # 如果尚未输出异常日志
                    self.log.debug(f'第{retry_count + 1}次重试 {name} 出错：{e}')
                    retry_failed = True  # 标记已输出异常
                await asyncio.sleep(backoff_seconds)

            if retry_failed and retry_count == max_retries - 1:
                self.log.error(f'{name} 重试{max_retries}次后仍然发生异常')
                return False, False, False

    async def GET_POST(self, opt, num=1):
        async def GET():
            async with aiohttp.ClientSession() as session:
                if opt['method'] == 'get':
                    async with session.get(**opt['kwargs']) as response:
                        status = response.status
                        result = await response.text()
                else:
                    async with session.post(**opt['kwargs']) as response:
                        status = response.status
                        result = await response.text()
                if status != 200:
                    await asyncio.sleep(3)
                    if num > 3:
                        self.log.warning(f'{status}:状态超出3次')
                        return False, False, False
                    self.log.debug(f'{status}:去重试 第{num}次')
                    return await self.GET_POST(opt, num + 1)
                try:
                    result_json = json.loads(result)
                except:
                    result_json = result
                return status, result, result_json

        return await self.retry_with_backoff(GET, 3, f'GET_POST')

    async def verify(self):
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

    async def Get_H5st(self, functionId, cookie, data, appId):
        if self.verify_result != True:
            await self.verify()
        if self.verify_result != True:
            self.log.error("授权未通过 退出")
            sys.exit()
        opt = {
            'method': '',
            'kwargs': {
                'url': 'https://api.ouklc.com/api/h5st',
                'params': {
                    'functionId': functionId,
                    'body': json.dumps(data),
                    'ua': self.ua,
                    'pin': self.pt_pin(cookie),
                    'appId': appId
                }
            }
        }
        status, res, resp = await self.GET_POST(opt)
        if status != 200:
            return await self.Get_H5st(functionId, cookie, data, appId)
        opt = {
            'method': 'post',
            'kwargs': {
                'url': f'https://api.m.jd.com',
                'headers': {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-cn",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "api.m.jd.com",
                    "Referer": "https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html",
                    "Origin": "https://prodev.m.jd.com",
                    "Cookie": cookie,
                    "User-Agent": self.ua
                },
                # 'proxy': self.proxy,
                'data': resp["body"]
            }
        }
        if self.proxy:
            opt['kwargs'].update({'proxy': self.proxy})
        status, res, resp = await self.GET_POST(opt)
        return resp

    def pt_pin(self, cookie):
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        return pt_pin

    def convert_ms_to_hours_minutes(self, milliseconds):
        seconds = milliseconds // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{hours}小时{minutes}分'

    async def inviteFissionReceive(self, cookie, linkId, page=1):
        if self.verify_result != True:
            await self.verify()
        if self.verify_result != True:
            self.log.error("授权未通过 退出")
            sys.exit()
        ua = generate_random_user_agent()
        data = {
            'linkId': linkId,
        }
        resp = await self.Get_H5st('inviteFissionReceive', cookie, data, 'b8469')
        if resp['success'] == False and resp['errMsg'] == '活动太火爆，请稍候重试':
            msg = f'还差{self.leftAmount / self.amount}次' if self.amount != 0 else '先去助力一次才能计算需要人数'
            self.log.debug(f'没助理了 快去助理吧 {msg}')
            await self.superRedBagList(cookie, linkId, page)
            return False
            # if self.amount != 0:
            #     return await self.inviteFissionBeforeHome(int(self.leftAmount / self.amount))
            # else:
            #     return await self.inviteFissionBeforeHome()

        if resp['success'] and resp['code'] == 0:
            self.amount = float(resp["data"]["receiveList"][0]["amount"])
            self.leftAmount = float(resp["data"]["leftAmount"])
            self.log.info(
                f'领取中:{resp["data"]["totalAmount"]} 当前:{resp["data"]["amount"]} 获得:{resp["data"]["receiveList"][0]["amount"]} 还差:{resp["data"]["leftAmount"]}元/{self.leftAmount / self.amount}次 当前进度:{resp["data"]["rate"]}%')
            if int(resp["data"]["rate"]) == 100:
                self.log.info(f'领取中:{resp["data"]["totalAmount"]} 进度:{resp["data"]["rate"]}% 退出!')
                await self.superRedBagList(cookie, linkId, page)
                return False
        return True

    async def apCashWithDraw(self, linkId, cookie, id, poolBaseId, prizeGroupId, prizeBaseId):
        if self.verify_result != True:
            await self.verify()
        if self.verify_result != True:
            self.log.error("授权未通过 退出")
            sys.exit()
        ua = generate_random_user_agent()
        resp = await self.Get_H5st("apCashWithDraw",
                                   cookie,
                                   {"linkId": linkId,
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
                                    },
                                   '8c6ae'
                                   )
        return resp

    async def inviteFissionBeforeHome(self, num=1):
        found_match = False
        for cookie in ck:
            if len(self.power_success) >= num:
                return await self.inviteFissionReceive(self.cookie, self.linkId)
            resp = await self.Get_H5st("inviteFissionBeforeHome", cookie,
                                       {'linkId': self.linkId, "isJdApp": True, 'inviter': self.inviter},
                                       '02f8d', )
            if int(resp['code']) == 0:
                for code, msg in self.helpResult:
                    if resp['data']['helpResult'] == int(code):
                        found_match = True
                        self.log.info(
                            f"Id:{self.linkId[:4] + '****' + self.linkId[-4:]}|助理:{resp['data']['nickName']}|{resp['data']['helpResult']}|{self.pt_pin(cookie)}|{msg}")
                        if resp['data']['helpResult'] == 1:
                            self.power_success.append(cookie)
                        else:
                            self.power_failure.append(cookie)
                    if not found_match:
                        msg = '❌未知状态 (可能是活动未开启！！！)'
                        self.power_failure.append(cookie)
                        self.log.info(
                            f"Id:{self.linkId[:4] + '****' + self.linkId[-4:]}|助理:{resp['data']['nickName']}|{resp['data']['helpResult']}|{self.pt_pin(cookie)}|{msg}")
            else:
                self.log.info(f"{self.pt_pin(cookie)}{resp['code']} 结果:💔{resp['errMsg']}")

    async def superRedBagList(self, cookie, linkId, page):
        if self.verify_result != True:
            await self.verify()
        if self.verify_result != True:
            self.log.error("授权未通过 退出")
            sys.exit()
        resp = await self.Get_H5st('superRedBagList', cookie,
                                   {"pageNum": page, "pageSize": 200, "linkId": linkId, "business": "fission"},
                                   'f2b1d')
        self.log.info(f"开始提取{page}页, 共{len(resp['data']['items'])}条记录")
        if not resp['data']['hasMore']:
            return False
        for item in resp['data']['items']:
            id, amount, prizeType, state, prizeConfigName, prizeGroupId, poolBaseId, prizeBaseId, startTime = (
                item['id'], item['amount'], item['prizeType'], item['state'],
                item['prizeConfigName'], item['prizeGroupId'], item['poolBaseId'], item['prizeBaseId'],
                item['startTime']
            )
            t = True
            while t:
                if prizeType not in self.rewardType and float(amount) > 1.0:
                    self.log.info(f"{startTime} {amount}元 {'❌未提现' if prizeType == 4 and state != 3 else '✅已提现'}")
                    t = False
                if prizeType == 4 and state != 3 and state != 4:
                    resp = await self.apCashWithDraw(linkId, cookie, id, poolBaseId, prizeGroupId, prizeBaseId)
                    if int(resp['data']['status']) == 310:
                        self.log.info(f"✅{amount}现金💵 提现成功")
                        self.successful.append(amount)
                        await asyncio.sleep(1)
                        t = False
                    elif int(resp['data']['status']) == 50056 or int(resp['data']['status']) == 50001:
                        self.log.warning(f"❌{amount}现金💵 重新发起 提现失败:{resp['data']['message']}")
                        await asyncio.sleep(10)
                    elif '金额超过自然月上限' in resp['data']['message']:
                        self.log.info(f"{amount}现金:{resp['data']['message']}:去兑换红包")
                        t = await self.apRecompenseDrawPrize(linkId, cookie, id, poolBaseId, prizeGroupId, prizeBaseId, amount)
                        await asyncio.sleep(3)
                    else:
                        self.log.error(f"{amount}现金 ❌提现错误:{resp['data']['status']} {resp['data']['message']}")
                        t = False
                else:
                    t = False
        return True





    # 兑换红包
    async def apRecompenseDrawPrize(self, linkId, cookie, id, poolBaseId, prizeGroupId, prizeBaseId, amount):
        resp = await self.Get_H5st('apRecompenseDrawPrize', cookie,
                                   {"linkId": linkId,
                                    "businessSource": "fission",
                                    "drawRecordId": id,
                                    "business": "fission",
                                    "poolId": poolBaseId,
                                    "prizeGroupId": prizeGroupId,
                                    "prizeId": prizeBaseId,
                                    },
                                   '8c6ae')
        if resp['success'] and int(resp['data']['resCode']) == 0:
            self.log.info(f"{amount}现金:🧧红包兑换成功")
            self.cash_redpacket.append(amount)
            return False
        else:
            self.log.info(f"{amount}现金:🧧红包兑换失败 {resp}")
            return True

    async def Fission_Draw(self, cookie, linkId):
        self.log.info(f"****************开始抽奖****************")
        while True:
            resp = await self.Get_H5st('inviteFissionDrawPrize', cookie,
                                       {"linkId": linkId},
                                       'c02c6')

            if not resp['success']:
                if "抽奖次数已用完" in resp['errMsg']:
                    self.log.debug(f"⚠️抽奖次数已用完")
                    break
                elif "本场活动已结束" in resp['errMsg']:
                    self.log.debug(f"⏰本场活动已结束了,快去重新开始吧")
                    sys.exit()
            try:
                if not resp['success']:
                    self.log.warning(f'{resp["errMsg"]}')
                    time.sleep(1)
                    continue
                # print(resp)
                # print(resp['data']['rewardType'])
                if int(resp['data']['rewardType']) in self.rewardType:
                    self.log.info(
                        f"获得:{resp['data']['prizeValue']}元{self.rewardType[int(resp['data']['rewardType'])]['msg']}")
                    if int(resp['data']['rewardType']) == 2:
                        self.redpacket.append(float(resp['data']['prizeValue']))
                else:
                    self.log.info(f"获得:{resp['data']['prizeValue']}元现金💵")
                    self.cash.append(float(resp['data']['prizeValue']))
            except Exception as e:
                self.log.error(f'(未知物品):{resp}')
            await asyncio.sleep(0.3)
        self.log.info(
            f"抽奖结束: 💵现金:{'{:.2f}'.format(sum([float(x) for x in self.cash]))}元, 🧧红包:{'{:.2f}'.format(sum([float(x) for x in self.redpacket]))}元")
        self.log.info(f"****************开始提现****************")
        page = 0
        while True:
            page = page + 1
            super = await self.superRedBagList(cookie, linkId, page)
            await asyncio.sleep(2)
            if page >= self.page:
                break
            if not super:
                break
        # self.log.info(
        #     f"提现结束: 💵现金:{'{:.2f}'.format(sum([float(x) for x in self.successful]))}元, 🧧兑换红包:{'{:.2f}'.format(sum([float(x) for x in self.cash_redpacket]))}元")

        message = ('提现结束: ') + (
            f"💵现金:{'{:.2f}'.format(sum([float(x) for x in self.successful]))}元/") + (
                      f"🧧兑换红包:{'{:.2f}'.format(sum([float(x) for x in self.cash_redpacket]))}元/共计红包:{'{:.2f}'.format(sum([float(x) for x in self.redpacket + self.cash_redpacket]))}")
        if not self.successful and not self.cash_redpacket:
            message = '提现结束: 一毛都没有哦！'
        self.log.info(message)

    async def add_LinkId(self):
        async def Link():
            if self.verify_result != True:
                await self.verify()
            if self.verify_result != True:
                self.log.error("授权未通过 退出")
                sys.exit()
            url = 'https://api.ixu.cc/status/inviter.json'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['stats'] != 'True':
                            self.log.error(f"{data['err_text']}")
                            sys.exit()
                        self.inviter_help = data['inviter']
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

    async def task_start(self):
        if self.verify_result != True:
            await self.verify()
        if self.verify_result != True:
            self.log.error("授权未通过 退出")
            sys.exit()
        await self.add_LinkId()
        # for cookie in ck:
        # time.sleep(1)
        cookie = self.cookie
        if self.txj_status:
            try:
                res = await self.Get_H5st('inviteFissionHome', cookie, {'linkId': self.linkId[0], "inviter": "", },
                                          'eb67b' )
                # if res['errMsg'] == 'errMsg':
                if not res['success'] and res['errMsg'] == '未登录':
                    self.log.error(f"{res['errMsg']}")
                    return
                resp = res['data']
                if resp['cashVo'] != None:
                    cashVo = resp['cashVo']
                    self.log.info(
                        f"Name:{cashVo['userInfo']['nickName']} 已助理:{resp['prizeNum'] + resp['drawPrizeNum']} 提现:{cashVo['totalAmount']}元 当前:{cashVo['amount']}元 进度{cashVo['rate']}% 剩余时间:{self.convert_ms_to_hours_minutes(resp['countDownTime'])}")
                    if int(cashVo['rate']) == 100:
                        self.log.info(
                            f"本轮您已提现{cashVo['totalAmount']}元了 等{self.convert_ms_to_hours_minutes(resp['countDownTime'])}后在来吧")
                        await self.superRedBagList(cookie, self.linkId[0], 1)
                        return
                else:
                    self.log.error('哦和 黑号了哦')

                while True:
                    Receive = await self.inviteFissionReceive(cookie, self.linkId[0])
                    # if not Receive:
                    #     break
                    time.sleep(0.3)
            except Exception as e:
                self.log.error('黑号')
        else:
            for i in self.linkId:
                self.log.info(f'开始执行 LinkId:{i}')
                await self.Fission_Draw(cookie, i)


if __name__ == '__main__':
    pdd = TEN_JD_PDD_DRAW()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pdd.task_start())
    loop.close()
