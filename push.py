import requests
import json

# 时间
from datetime import datetime
import time
import pytz


# 获取云函数执行时的时间
def get_now_date():
    now_date = datetime.fromtimestamp(int(
        time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y年%m月%d日')
    now_time = datetime.fromtimestamp(int(
        time.time()), pytz.timezone('Asia/Shanghai')).strftime('%H:%M:%S')
    return {
        'now_date': now_date,  # 日期
        'now_time': now_time  # 时间
    }


# 企业微信推送
class qiye_wechat():
    def __init__(self, AgentId, Secret, EnterpriseID, Touser):
        # 企业微信消息推送所需参数
        self.AgentId = AgentId
        self.Secret = Secret
        self.EnterpriseID = EnterpriseID
        self.Touser = Touser

        # 企业微信相关API
        self.qiye_push_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
        self.qiye_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'

    # 获取企业微信推送服务的 TOKEN
    def get_access_token(self):
        result = requests.get(url=self.qiye_token_url,
                              params={
                                  'corpid': self.EnterpriseID,
                                  'corpsecret': self.Secret,
                              }).json()
        if result.get('access_token'):
            access_token = result.get('access_token')
        else:
            access_token = None
        return access_token

    # 企业微信推送消息
    # 文本消息
    def push_text_message(self,
                          Title='推送通知',
                          Content='未提供内容',
                          UserName='',
                          Account=''):
        DateTime = get_now_date()  # 获取时间
        Access_Token = self.get_access_token()  # 获取 PUSH_TOKEN
        # 推送消息内容
        message = {
            'touser': self.Touser,
            'msgtype': 'text',
            'agentid': self.AgentId,
            'text': {
                'content': "推送通知\n用户名:{}\n日期:{}\n时间{}\n\n{}".format(UserName,DateTime['now_date'],DateTime['now_time'],Content)
            }
        }
        response = requests.post(url=self.qiye_push_url,
                                 params={'access_token': Access_Token},
                                 data=bytes(json.dumps(message,
                                                       ensure_ascii=False),
                                            encoding='utf-8'))
        result = response.json()
        print(result)
