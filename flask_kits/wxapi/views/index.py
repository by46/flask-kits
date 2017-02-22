# -*- coding:utf-8 -*-
import hashlib
from xml.etree import ElementTree as ET

from flask import Response
from flask import current_app as app
from flask import request

from flask_kits.utils import make_response_content
from flask_kits.utils import valid_message
from flask_kits.wxapi import wx


@wx.route('/heath_check', methods=['GET', 'POST'])
def heath_check():
    if request.method.lower() == 'get':
        return validate()
    else:
        return receive_message()


@wx.route('/consume_event', methods=["POST"])
def consumer_event():
    content = request.body
    app.logger.error(content)
    headers = {'Content-Type': 'application/xml'}
    try:
        root = ET.XML(content)
        params = dict([(e.tag, e.text) for e in root])
        if params['return_code'].lower() == 'fail':
            # TODO(benjamin): process business logical
            return Response(make_response_content(), headers=headers)

        if not valid_message(params, app.config['APP_API_KEY']):
            response = make_response_content('FAIL', 'Sign fail')
            return Response(response, headers=headers)

        trade_no = params.get('out_trade_no')
        # TODO(benjamin): process business logical when pay success

    except ET.ParseError as e:
        app.logger.error('Parse Content error %s', e)
    except Exception as e:
        app.logger.error('Process notified message error: %e', e)
        app.logger.exception(e)

    response = make_response_content()
    return Response(response, headers={'Content-Type': 'application/xml'})


def validate():
    signature = request.args.get("signature")
    nonce = request.args.get("nonce")
    timestamp = request.args.get("timestamp")
    if signature is None or nonce is None or timestamp is None:
        return Response("Invalid Signature")
    if not validate_signature(signature, app.config['APP_TOKEN'], nonce, timestamp):
        return Response("Invalid Signature", headers={'Content-Type': 'text/plain'})

    nonce_str = request.args.get('echostr')
    if nonce_str:
        return Response(nonce_str, headers={'Content-Type': 'text/plain'})

    return Response("Invalid encrypt type", headers={'Content-Type': 'text/plain'})


def validate_signature(signature, token, nonce, timestamp):
    tmp = ''.join(sorted([token, nonce, timestamp]))
    return hashlib.sha1(tmp).hexdigest() == signature


def receive_message():
    content = request.data
    app.logger.error(content)
    headers = {'Content-Type': 'application/xml'}
    try:
        root = ET.XML(content)
        params = dict([(e.tag, e.text) for e in root])
        if params['MsgType'].lower() == 'event' and params['Event'] == 'subscribe':
            return Response(make_content(params), headers=headers)
            # TODO(benjamin): process business logical
            # return Response(make_response_content(), headers=headers)



    except ET.ParseError as e:
        app.logger.error('Parse Content error %s', e)
    except Exception as e:
        app.logger.error('Process notified message error: %e', e)
        app.logger.exception(e)
    return Response(status=200)

def make_content(recvmsg):
    textTpl = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>"""
    message = u"""每一个探索极致自然的灵魂，都不会错过雪山体验

欢迎关注极度体验，让专注高海拔登山十多年的我们，带你踏足雪山之巅

岗什卡雪山和乞力马扎罗登山活动正在招募队员中
如需咨询登山及合作事宜，请联系微信（电话）：18787100402
联系人：晓晓"""
    echostr = textTpl % (recvmsg['FromUserName'], recvmsg['ToUserName'], recvmsg['CreateTime'], message)
    app.logger.error(echostr)
    return echostr