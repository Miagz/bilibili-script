import requests
import json
import time
import random,push,sys
# import urllib3
# urllib3.disable_warnings()
proxies={'http': 'http://127.0.0.1:8080' , 'https': 'http://127.0.0.1:8080'}
header={
    "Sec-Ch-Ua": """" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96" """
    ,"Accept": "application/json, text/plain, */*"
    ,"Content-Type": "application/x-www-form-urlencoded"
    ,"Sec-Ch-Ua-Mobile": "?0"
    ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
    ,"Sec-Ch-Ua-Platform": """"Windows" """
    ,"Origin": "https://www.bilibili.com"
    ,"Sec-Fetch-Site": "same-site"
    ,"Sec-Fetch-Mode": "cors"
    ,"Sec-Fetch-Dest": "empty"
    ,"Referer": "https://www.bilibili.com/"
    ,"Accept-Encoding": "gzip, deflate"
    ,"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
}
class bilibili_run():
    def __init__(self):
        self.cookies="i-wanna-go-back=1; _uuid=68559AB1-43E4-59E9-F1086-10C23D94D8C10652836infoc; buvid3=882C6909-2AB1-4AF0-BB88-C489261A758F167629infoc; b_nut=1638064553; buvid_fp=882C6909-2AB1-4AF0-BB88-C489261A758F167629infoc; fingerprint=5cfe383d09b03a96f002efbab47ab55e; buvid_fp_plain=882C6909-2AB1-4AF0-BB88-C489261A758F167629infoc; SESSDATA=a6dc55c7,1653616580,e992a*b1; bili_jct=43a9f34e646cdc2a2576af5b1b32af0f; DedeUserID=360947223; DedeUserID__ckMd5=ba34cf7628e3b068; sid=4fukbi76; video_page_version=v_old_home; blackside_state=1; rpdid=|(J|Y||uRuR|0J'uYJ)|YR~k); b_ut=6; CURRENT_FNVAL=2000; bp_video_offset_360947223=603430844825025107"
        self.cookie = self.extract_cookies(self.cookies)
    def extract_cookies(self,cookies):
        global csrf
        cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
        csrf = cookies['bili_jct']
        return cookies
    def getCoin(self):
        url = "http://account.bilibili.com/site/getCoin"
        r = requests.get(url,headers=header, cookies=self.cookie, verify=False).text
        j = json.loads(r)
        money = j['data']['money']
        return money
    def getActiveInfo(self):
        url = "http://api.bilibili.com/x/web-interface/index/top/rcmd?fresh_type=3&version=1&ps=14"
        r = requests.get(url,headers=header, cookies=self.cookie, verify=False).text
        j = json.loads(r)
        return j
    def Task(self):
        j = self.getActiveInfo()
        data = j['data']
        coin_count = 0
        for i in range(0, len(data["item"])):
            bvid = data["item"][i]['bvid']
            aid  = data["item"][i]['id']
            print(str(bvid)+' ---- '+ str(aid))
            if coin_count < 5:
                coin_code = self.tocoin(aid)
                if coin_code == -99:
                    return
            time.sleep(3)
            self.toview(bvid)
            time.sleep(3)
            self.shareVideo(bvid)
            if coin_code == 1:
                coin_count = coin_count+1
            if coin_count == 5:
                break
            print('----------------------')
    def toview(self,bvid):
        playedTime = random.randint(10, 100)
        url = "http://api.bilibili.com/x/click-interface/web/heartbeat"
        data = {
            'bvid': bvid,
            'played_time': playedTime,
            'csrf': csrf
        }
        r = requests.post(url,headers=header, data=data, cookies=self.cookie, verify=False).text
        j = json.loads(r)
        code = j['code']
        if code == 0:
            print('观看视频成功!')
        else:
            print('观看视频失败!')
    def shareVideo(self,bvid):
        url = "http://api.bilibili.com/x/web-interface/share/add"
        data = {
            'bvid': bvid,
            'csrf': csrf
        }
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
        }
        r = requests.post(url, data=data, cookies=self.cookie, headers=header, verify=False).text
        j = json.loads(r)
        code = j['code']
        if code == 0:
            print('分享成功!')
        else:
            print('分享失败!')
    def tocoin(self,aid):
        coinNum = self.getCoin()
        if coinNum == 0:
            self.qiye_push_msg("停止执行！ 硬币不够！",self.name)
            return -99
        url = "http://api.bilibili.com/x/web-interface/coin/add"
        data = {
            'aid': aid,
            'multiply': 1,
            'select_like': 1,
            "cross_domain":"true",
            'csrf': csrf
        }
        r = requests.post(url,data=data,headers=header, cookies=self.cookie, verify=False).text
        j = json.loads(r)
        code = j['code']
        print("code="+str(code))
        if code == 0:
            print(str(aid)+' 投币成功 !')
            return 1
        else:
            print(str(aid)+' 投币失败!')
            return 0
    def getInfo(self):
        global uid
        url = "http://api.bilibili.com/x/space/myinfo"
        r = requests.get(url,headers=header, cookies=self.cookie, verify=False).text
        j = json.loads(r)
        uid = j['data']['mid']
        self.name = j['data']['name']
        level = j['data']['level']
        current_exp = j['data']['level_exp']['current_exp']
        next_exp = j['data']['level_exp']['next_exp']
        sub_exp = int(next_exp)-int(current_exp)
        days = int(int(sub_exp)/65)
        coin = self.getCoin()
        msg ="今日运行完成! 目前等级为{}级 目前经验{} 离升级还差{}经验 大概需要{}天 剩余硬币:{}".format(str(level),str(current_exp),str(sub_exp),str(days),str(coin))
        return msg

    def check_cookie(self):
        url = "http://api.bilibili.com/x/space/myinfo"
        r = requests.get(url,headers=header, cookies=self.cookie, verify=False).text
        j = json.loads(r)
        if j["code"]!=0:
            self.qiye_push_msg("Bilibili Session失效,请立即修改Session！")
            sys.exit()

    def qiye_push_msg(self,content, username='Miagz'):
        # 企业微信推送
        AgentId = ""
        Secret = ""
        EnterpriseID = ""
        Touser = "@all"
        p = push.qiye_wechat(AgentId, Secret, EnterpriseID, Touser)
        p.push_text_message('BiliBili', content, username)
    def run(self):
        self.check_cookie()
        self.Task()
        self.qiye_push_msg(self.getInfo(), self.name)
def main():
    bilibili_run().run()

main()