#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: big_winner.py(大赢家-提现)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('大赢家-提现');
"""

import requests, time, re, os, json, random, threading
from urllib.parse import unquote_plus
from datetime import datetime
start = time.time()
ruleId = {
    # '100': {'amount': '100', 'ruleId': '02b48428177a44a4110034497668f808'},
    '20': {'amount': '20', 'ruleId': '7ea791839f7fe3168150396e51e30917'},
    '8': {'amount': '8', 'ruleId': 'da3fc8218d2d1386d3b25242e563acb8'},
    '3': {'amount': '3', 'ruleId': '53515f286c491d66de3e01f64e3810b2'},
}
threads = []
cookie = ['ck']
def get_time():
    time_now = round(time.time() * 1000)
    return time_now
def printf(cookie, T):
    try:
        pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    except IndexError:
        pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    print(f"{str(datetime.now())[0:22]}->{pt_pin}->{T}")



def withdrawal(ruleId,ck):
    for i in ruleId:
        url = f"https://api.m.jd.com/api?functionId=jxPrmtExchange_exchange&appid=cs_h5&body=%7B%22bizCode%22%3A%22makemoneyshop%22%2C%22ruleId%22%3A%22{ruleId[i]['ruleId']}%22%2C%22sceneval%22%3A2%2C%22buid%22%3A325%2C%22appCode%22%3A%22%22%2C%22time%22%3A{get_time()}%2C%22signStr%22%3A%22%22%7D"
        headers = {
            "user-agent":"jdltapp;android;4.8.0;;;appBuild/2384;ef/1;ep/",
            "referer":"https://wqs.jd.com/",
            "cookie": ck
        }
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            printf(ck, f'本次提现{ruleId[i]["amount"]}元 返回结果：{res.json()["msg"]}')
        else:
            printf(ck, f'本次提现{ruleId[i]["amount"]}元 接口：{res.status_code}')




if __name__ == '__main__':
    for index in cookie:
        for i in range(3):
            thead_one = threading.Thread(target=withdrawal, args=(ruleId,index))
            threads.append(thead_one)  # 线程池添加线程
    for t in threads:
        t.start()
        time.sleep(0.08)
    for t in threads:
        t.join()

    print(f'耗时：{time.time()-start}')