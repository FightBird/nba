from django.conf import settings
from urllib.parse import urlencode, parse_qs

import json
import requests



class OAuthWb(object):
    """
    QQ认证辅助工具类
    """

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = state   # 用于保存登录成功后的跳转页面路径

    def get_qq_url(self):
        # QQ登录url参数组建
        data_dict = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state
        }

        # 构建url
        qq_url = 'https://api.weibo.com/oauth2/authorize?' + 'client_id=' + self.client_id +'&redirect_uri=' + self.redirect_uri +'&state'+self.state

        return qq_url

    # 获取access_token值
    def get_access_token(self, code):
        url = 'https://api.weibo.com/oauth2/access_token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri

        }
        try:
            response = requests.post(url=url,data=data)
            # access_token=FE04************************CCE2&expires_in=7776000&refresh_token=88E4************************BE14
            data = response.text

            # 转化为字典
            data_dict =json.loads(data)
            print(data_dict)
        except:
            raise Exception('微博请求失败')

        # 提取access_token
        access_token = data_dict.get('access_token', None)

        if not access_token:
            raise Exception('access_token获取失败')

        return access_token

        # # 构建参数数据
        # data_dict = {
        #     'grant_type': 'authorization_code',
        #     'client_id': self.client_id,
        #     'client_secret': self.client_secret,
        #     'redirect_uri': self.redirect_uri,
        #     'code': code
        # }
        #
        # # 构建url
        # access_url = 'https://api.weibo.com/oauth2/access_token'
        # # 发送请求
        # try:
        #     response = requests.get(access_url,data_dict)
        #
        #     # 提取数据
        #     # access_token=FE04************************CCE2&expires_in=7776000&refresh_token=88E4************************BE14
        #     data = response.text
        #
        #     # 转化为字典
        #     data = parse_qs(data)
        # except:
        #     raise Exception('微博请求失败')
        #
        # # 提取access_token
        # access_token = data.get('access_token', None)
        #
        # if not access_token:
        #     raise Exception('access_token获取失败')
        #
        # return access_token[0]

