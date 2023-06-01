"""
File: jd_inviteDrawPrize.py(邀好友赢现金-抽奖)
Author: 𝓣𝓮𝓷 𝓸'𝓬𝓵𝓸𝓬𝓴
cron: 1 1 1 1 1 1
new Env('邀好友赢现金-抽奖');
"""
import sys,  os
from urllib.parse import  unquote
from utils.UTIL import *
try:
    from utils.TEN_UTIL import *
except:
    print('❌ 未检测到依赖 开始安装')
    load_so_file()

NUMBER_OF = os.environ.get("draw_numer") if os.environ.get("draw_numer") else 3
cookie = os.environ.get("draw_cookie") if os.environ.get("draw_cookie") else sys.exit('❌未获取到draw_cookie变量 程序自动退出')
TEN_TOKEN = os.environ.get("TEN_TOKEN") if os.environ.get("TEN_TOKEN") else sys.exit('❌未获取到TEN_TOKEN变量 程序自动退出')
TEN_scode = os.environ.get("TEN_scode") if os.environ.get("TEN_scode") else 1


activityUrl = "https://jump.ixu.cc/?url=https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html?inviter=HIzs4VDTQOYH_nRbcPIQ7CFCa9577iZwBlQUx0yTITw&channelType=1&femobile=femobile&activityChannel=jdlite"
data_dict = {}



verify = verify(TEN_TOKEN)
if verify != True:
    sys.exit('❌授权未通过 程序自动退出！！！')


stats = stats()
if stats.status_code != False:
    linkId = stats.json()[f'linkId{TEN_scode}']



def inviteFissionDrawPrize(cookie):
    url = "https://api.m.jd.com/"
    data = 'functionId=inviteFissionDrawPrize&body={{"linkId":"{linkId}"}}&t=1684891089602&appid=activities_platform&client=ios&clientVersion=4.2.0&h5st=20230524091809610;3661921034167168;c02c6;tk02web331cb341lMngzeDMrMysyAV-ygRzQmWiviZOtObeBJ8fdwuKsp_70EWTjJVKF4ME4EoSn_rBAwZkgL167NT5S;37520995a8ab73b2c8d5425c82095f0ba6055625bba7af32ecb258de5b80fdef;3.1;1684891089610;7414c4e56278580a133b60b72a30beb2764d2e61c66a5620e8e838e06644d1bf734f45e55381a9c227bd506a8ea6832d223716652cee6d293327f55f82b9ae6d67c5afac84eff2a44960858e1981c32bb8c0c4222649ec402519fe414d7ee8e944b69d78e5b8c76501b39210d7a831271f9b4dada85ae203278969712f23301ed140e58007758665bdd87d535c5a57e70059e89db5a8ffb285845b1107266a7af8c44b88edfb338419251c24fa6726bb'.format(linkId=linkId)

    headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'jdltapp;iPhone;4.2.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;hasOCPay/0;appBuild/1217;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22CJGzCwS1ZQCmDzYmYzrsYJU5Y2Y1ZWGmDWZrZtO2YzHuCzHuYwC5Cq%3D%3D%22%2C%22sv%22%3A%22CJYkDM4n%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1684891082%2C%22hdid%22%3A%22M1j35qhispl99TdfCvaiQodeZDjJzRZ5%5C%2F8PEE1%5C%2Fv0I4%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.jd.jdmobilelite%22%2C%22ridx%22%3A1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;',
            'Cookie': cookie,
            'Host': 'api.m.jd.com',
            'Referer': activityUrl,
            'Origin': 'https://prodev.m.jd.com',
            'Accept-Language': 'zh-Hans-CN;q=1 en-CN;q=0.9',
            'Accept': '*/*'
    }
    response = requests.request("POST", url, headers=headers, data=data)
    if response.status_code == 200:
        res = response.json()
        if res['data']:
            return response.status_code, res['data']['prizeValue'], res['data']['rewardType']
        else:
            return response.status_code, response.text

def superRedBagList(cookie, pageNum):
    body = "{%22linkId%22:%22Wvzc_VpNTlSkiQdHT8r7QA%22,%22pageNum%22:" + str(pageNum) + ",%22pageSize%22:10,%22business%22:%22fission%22}"
    body_str = unquote(
        '{%22linkId%22:%22Wvzc_VpNTlSkiQdHT8r7QA%22,%22pageNum%22:0,%22pageSize%22:10,%22business%22:%22fission%22}')
    body = json.loads(body_str)
    body['linkId'] = linkId
    body['pageNum'] = pageNum
    body = json.dumps(body)

    url = f"https://api.m.jd.com/?functionId=superRedBagList&body={body}&t=1680175108168&appid=activities_platform&client=ios&clientVersion=4.9.0&h5st=20230330191828169%3B5964585891728540%3Bf2b1d%3Btk02wc3a91c5a18nt2xka8eQHyXXWp61qlfYzVh7QiJwS83CsnYmvHZ0zVWyl5%2BXeyd02pJYGBOTj425fSkJOveE47py%3B09b111659c94110f8dedb8946c0f0c710e294d46fd9f7f88b6e11ab8d83a9b6c%3B3.1%3B1680175108169%3B7414c4e56278580a133b60b72a30beb2764d2e61c66a5620e8e838e06644d1bf435af310f448d006ddca390b55816edb3095af37a52b23094abc1d07a641003dd8161839dc9345ad0509b37448f3568e8931b2a66b59424fce91105921020c34ac036a040671281527a6b391a17ae3c9050baecf9e89343eb3032d1c77ebf7e4&cthr=1&uuid=7d86572aa70a501372d1e01cf2212d68dfda01ac&build=1283&screen=390*844&networkType=3g&d_brand=iPhone&d_model=iPhone13,2&lang=zh_CN&osVersion=16.1&partner=&eid=eidIe2348121bas7muRXboOGSZSt8bC%2F1GjazprkWOa1Bg%2FyAiv5t%2FfA%2BTd96yOxdnQ0CHVZ3w0sm7qAZxAEIqH17hENZao3bWVVnx1x2J0RB6SHjApm"
    headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/0;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22D2G4DtU3CwPrDzLrDJKnCzcyZNPvCNPtZtSyCJTuDtruZwHrCNPrYm%3D%3D%22%2C%22sv%22%3A%22CJYkCG%3D%3D%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1680174624%2C%22hdid%22%3A%22T5f08Jsy8xEp7Aoi7Lcw9mOJ3mEKQVO%2BmnaqJGSmYUQ%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.jd.jdmobilelite%22%2C%22ridx%22%3A1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;',
            'Cookie': cookie,
            'Host': 'api.m.jd.com',
            'Referer': activityUrl,
            'Origin': 'https://prodev.m.jd.com',
            'Accept-Language': 'zh-Hans-CN;q=1 en-CN;q=0.9',
            'Accept': '*/*'
    }
    response = requests.request("GET", url, headers=headers)
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
    url = "https://api.m.jd.com/"
    body = {"linkId": f"{linkId}",
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
            }
    data = f'functionId=apCashWithDraw&body={body}&t=1680573210922&appid=activities_platform&client=ios&clientVersion=4.9.0&h5st=20230404095330926%3B6981837197624937%3B8c6ae%3Btk02w91ec1bc218ncb4I9tI0ekCxJE9hRZRrw0WZKS0sgSwFfy6ko2ALTHqQk7xeE720V3gUNA7gYEZHmHc4swptp%2FxC%3B8b6968fa86fc8d900bed837e81d27e2b393d9074baf29376bcf7776d4b1b348a%3B3.1%3B1680573210926%3B7414c4e56278580a133b60b72a30beb2764d2e61c66a5620e8e838e06644d1bf435af310f448d006ddca390b55816edb3095af37a52b23094abc1d07a641003dd8161839dc9345ad0509b37448f3568e8931b2a66b59424fce91105921020c345db7ba64b005adbc37e0f2bcd130e3fcebf2dc359596c08a314013cae0da6c9c&cthr=1&uuid=7d86572aa70a501372d1e01cf2212d68dfda01ac&build=1283&screen=390*844&networkType=3g&d_brand=iPhone&d_model=iPhone13,2&lang=zh_CN&osVersion=16.1&partner=&eid=eidIe2348121bas7muRXboOGSZSt8bC%2F1GjazprkWOa1Bg%2FyAiv5t%2FfA%2BTd96yOxdnQ0CHVZ3w0sm7qAZxAEIqH17hENZao3bWVVnx1x2J0RB6SHjApm'
    headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'jdltapp;iPhone;4.9.0;;;M/5.0;hasUPPay/0;pushNoticeIsOpen/0;lang/zh_CN;hasOCPay/0;appBuild/1283;supportBestPay/0;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22D2G4DtU3CwPrDzLrDJKnCzcyZNPvCNPtZtSyCJTuDtruZwHrCNPrYm%3D%3D%22%2C%22sv%22%3A%22CJYkCG%3D%3D%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1680573193%2C%22hdid%22%3A%22T5f08Jsy8xEp7Aoi7Lcw9mOJ3mEKQVO%2BmnaqJGSmYUQ%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.jd.jdmobilelite%22%2C%22ridx%22%3A1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;',
            'Cookie': cookie,
            'Host': 'api.m.jd.com',
            'Referer': activityUrl,
            'Origin': 'https://prodev.m.jd.com',
            'Accept-Language': 'zh-Hans-CN;q=1 en-CN;q=0.9',
            'Accept': '*/*'
    }
    response = requests.request("POST", url, headers=headers, data=data)
    if response.status_code == 200:
        res = response.json()
        print(res)
        if res['data']:
            return res['data']
        else:
            printf(cookie, f"{response.status_code} {res}")
    else:
        print(f'{response.status_code}')

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
        time.sleep(1)
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
