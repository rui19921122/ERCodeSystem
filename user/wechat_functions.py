from django.conf import settings
import requests

from custom_exceptions import WechatUserCodeError


def get_user_open_id(code):
    """
    通过微信小程序端生成的code结合小程序app密钥与微信服务器端进行通信，以获取用户的open id
    :param code: 微信小程序端发送来的code
    :return: 用户的open id 以及session_key
    """
    wechat_http_api_url = "https://api.weixin.qq.com/sns/jscode2session"
    APP_ID = settings.WECHAT_APP_ID
    APP_SECRET = settings.WECHAT_APP_SECRET_KEY
    response = requests.get(wechat_http_api_url,
                            params={
                                "appid": APP_ID,
                                "secret": APP_SECRET,
                                "js_code": code,
                                "grant_type": "authorization_code"
                            })
    if response.status_code == 200:
        data = response.json()
        if "errcode" in data:
            if data.get('errcode') == 40029:
                raise WechatUserCodeError()
            else:
                raise BaseException(data)
        open_id = data.get('openid')
        session_key = data.get('session_key')
        return open_id, session_key