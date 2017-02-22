# -:- coding:utf8 -:-
import json

from flask import current_app
from werkzeug.local import LocalProxy

from top import api
from top import appinfo

#
# url = 'gw.api.taobao.com'
# port = 80
# app_key = '23555395'
# secret_key = '2425c701b7df62bba83ff7b83af43b1a'
# req = api.AlibabaAliqinFcSmsNumSendRequest(url, port)
# req.set_app_info(appinfo(app_key, secret_key))
#
# req.extend = ""
# req.sms_type = "normal"
# req.sms_free_sign_name = "极度体验"
# req.sms_param = json.dumps({'name': '晏长寿', 'code': '223456'})
# req.rec_num = "18708140165"
# req.sms_template_code = "SMS_33335093"
# try:
#     resp = req.getResponse()
#     print (resp)
# except Exception, e:
#     print (e)
#
# import time
#
# time.sleep(10)
# req.sms_param = json.dumps({'name': '晏长寿', 'code': '223457'})
# try:
#     resp = req.getResponse()
#     print (resp)
# except Exception, e:
#     print (e)

DEFAULT_URL = 'gw.api.taobao.com'
DEFAULT_PORT = 80

SMS = LocalProxy(lambda: current_app.extensions['kits_sms'])


class SMSSender(object):
    def __init__(self, app_key, secret_key, url=DEFAULT_URL, port=DEFAULT_PORT):
        self.app_key = app_key
        self.secret_key = secret_key
        self.url = url
        self.port = port

    def send(self, template_code, sign_name, receive_num, param):
        req = api.AlibabaAliqinFcSmsNumSendRequest(self.url, self.port)
        req.set_app_info(appinfo(self.app_key, self.secret_key))

        if not isinstance(param, basestring):
            try:
                param = json.dumps(param)
            except Exception as e:
                current_app.logger.exception(e)
                return False

        req.extend = ""
        req.sms_type = "normal"
        req.sms_free_sign_name = sign_name
        req.sms_param = param
        req.rec_num = receive_num
        req.sms_template_code = template_code
        try:
            response = req.getResponse()
            return True
        except Exception as e:
            current_app.logger.exception(e)
            return False


def init_extension(kits, app):
    url = kits.get_parameter('SMS_URL', default=DEFAULT_URL)
    port = kits.get_parameter('SMS_PORT', default=DEFAULT_PORT)
    app_key = kits.get_parameter("SMS_APP_KEY")
    secret_key = kits.get_parameter('SMS_SECRET_KEY')
    req = api.AlibabaAliqinFcSmsNumSendRequest(url, port)
    req.set_app_info(appinfo(app_key, secret_key))
    app.extensions['kits_sms'] = SMSSender(app_key, secret_key, url, port)


if __name__ == '__main__':
    sender = SMSSender('app_key', 'sms_secret_key')
    sender.send()
