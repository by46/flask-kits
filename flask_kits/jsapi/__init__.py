# -*- coding:utf-8 -*-

import hashlib
import httplib
import time

import requests
from flask import current_app
from flask import render_template_string
from flask import request
from furl import furl
from jinja2 import nodes
from jinja2.ext import Extension
from werkzeug.local import LocalProxy

from flask_kits.utils import nonce_str

JsApi = LocalProxy(lambda: current_app.extensions['kits_jsapi'])


def init_extension(kits, app):
    app_id = app.config['APP_ID']
    server = kits.get_parameter('token_server')
    worker = AccessTokenThread(app_id, server)
    app.extensions['kits_jsapi'] = worker
    app.jinja_env.add_extension(JsApiExtension)


class AccessTokenThread(object):
    def __init__(self, app_id, token_server):
        self.app_id = app_id
        self.token_server = token_server

    @property
    def ticket(self):
        url = "{0}/token/{1}".format(self.token_server, self.app_id)
        response = requests.get(url)
        if response.status_code == httplib.OK:
            return response.json().get('ticket')
        return ""

    @property
    def token(self):
        url = "{0}/token/{1}".format(self.token_server, self.app_id)
        response = requests.get(url)
        if response.status_code == httplib.OK:
            return response.json().get('token')
        return None

    def signature(self, url):
        nonce = nonce_str()
        timestamp = int(time.time())
        ticket = self.ticket
        segments = '&'.join(
            ['jsapi_ticket=' + ticket, 'noncestr=' + nonce, 'timestamp=' + str(timestamp), 'url=' + url])
        sig = hashlib.sha1(segments).hexdigest()
        return dict(ticket=ticket, nonce=nonce, timestamp=timestamp, signature=sig)


TEMPLATE = u"""
<script type="text/javascript">
    wx.config({
        debug: {{ debug }}, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印
        appId: '{{ app_id }}', // 必填，公众号的唯一标识
        timestamp: '{{ config.timestamp }}', // 必填，生成签名的时间戳
        nonceStr: '{{ config.nonce }}', // 必填，生成签名的随机串
        signature: '{{ config.signature }}',// 必填，签名，见附录1
        jsApiList: ["chooseWXPay","onMenuShareTimeline",
        "onMenuShareAppMessage","chooseImage",
        "previewImage","uploadImage","downloadImage"] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
    });
</script>
"""


class JsApiExtension(Extension):
    tags = set(['jsapi'])

    def __init__(self, environment):
        super(JsApiExtension, self).__init__(environment)

    def parse(self, parser):
        line_no = next(parser.stream).lineno

        args = []
        # while True:
        #     arg = parser.parse_expression()
        #     if not arg:
        #         break
        #     args.append(arg)

        # body = parser.parse_statements(['name:endjsapi'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_register', args), [], [], []).set_lineno(line_no)

    def _register(self, caller):
        # TODO(benjamin): process right url
        url = self._make_url()
        config = JsApi.signature(url)
        return render_template_string(TEMPLATE, app_id=current_app.config['APP_ID'], config=config, debug='false')

    @staticmethod
    def _make_url():
        url = furl(request.url)
        domain = furl(current_app.config['APP_DOMAIN'])
        url.port = 80
        url.host = domain.host
        return url.url
