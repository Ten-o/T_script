import asyncio
import time, requests, sys, re
from datetime import datetime
from urllib.parse import unquote_plus
import aiohttp

"""
File: CHECK_COOKIE.py(检测COOKIE-快速)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('检测COOKIE-快速');
"""

#原有CK文件
original_ck = 'cklist.txt'
#存储返回有效ck文件
filename = 'effective_ck.txt'
start = time.time()
#无效ck列表
invalid_ck = []
#有效ck列表
effective_ck = []
def printf(would,cookie, T):
    try:
        pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    except IndexError:
        pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        pt_pin = unquote_plus(pt_pin)
    print(f"{str(datetime.now())[0:22]}->{would}->{pt_pin}->{T}")
    return pt_pin

async def request_interface(cookie):
    url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'
    headers = {
        "Host": "me-api.jd.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        "Accept-Language": "zh-cn",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url,headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data['retcode'] == "1001":
                    msg = f'❌ 验证为无效'
                    invalid_ck.append(cookie)
                elif data['retcode'] == "0":
                    msg = f"✅ 验证为有效"
                    effective_ck.append(cookie)
                else:
                    msg = f"❌ 意外退出"
                return msg

async def handling():
    f = open(original_ck, 'r')
    cklist = f.readlines()
    stack = len(cklist)
    print(f'{original_ck}文件共计COOKIE:{stack}')
    would = 0
    for i in cklist:
        would = would + 1
        cookie = i.replace("\n", "")
        date = await request_interface(cookie)
        printf(f'第{would}个工具人',cookie, f'{date}')
        time.sleep(0.5)
    result = set(effective_ck)
    print(f"✅有效：{result}\n\n\n❌无效：{invalid_ck}\n\n有效COOKIE开始写入{filename}文件\n\n\n✅有效COOKIE:{len(result)}  ❌重复COOKIE：{stack-len(result)-len(invalid_ck)}  ❌无效COOKIE:{len(invalid_ck)}")
    for i in result:
        with open(filename, 'a') as f:
            f.write(f'{i}\n')
    print(f'✅有效COOKIE写入{filename}文件完成   ⏰耗时:{time.time() - start}')

if __name__ == '__main__':
    asyncio.run(handling())