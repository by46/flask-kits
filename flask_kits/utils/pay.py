import logging
from xml.etree import ElementTree as ET

from .rand import nonce_str
from .signature import sign
from .util import timestamp

SUCCESS = 'success'
FAIL = 'fail'

logger = logging.getLogger('drp.muggle')


def make_h5_pay_sign(app_id, pre_pay_id, api_key):
    params = [('appId', app_id), ('timeStamp', timestamp()), ('nonceStr', nonce_str()),
              ('package', 'prepay_id={0}'.format(pre_pay_id)),
              ('signType', 'MD5')]
    h5_sign = sign(params, api_key)
    params.append(('sign', h5_sign))
    params.append(('pre_pay_id', pre_pay_id))
    return dict(params)


def make_prepay_id(entity, api_key):
    """
    appid, mch_id, body

    :param entity: `class`:`Bunch`
    :param api_key: `class`:`str`
    :return:  `class`:`str`
    """
    nonce = nonce_str()
    params = [('appid', entity.appid),
              ('mch_id', entity.mch_id),
              ('device_info', 'WEB'),
              ('nonce_str', nonce),
              ('body', entity.body),
              ('detail', entity.detail),
              ('out_trade_no', entity.out_trade_no),
              ('total_fee', entity.total_fee),
              ('spbill_create_ip', entity.spbill_create_ip),
              ('time_start', entity.time_start),
              ('time_expire', entity.time_expire),
              ('notify_url', entity.notify_url),
              ('trade_type', 'JSAPI'),
              ('openid', entity.openid)]
    pay_sign = sign(params, api_key)
    params.append(('sign', pay_sign))

    root = ET.Element('xml')

    for key, value in params:
        node = ET.SubElement(root, key)
        if isinstance(value, unicode):
            node.text = value.encode('utf8')
        else:
            node.text = str(value)

    return ET.tostring(root)


def make_company_pay(entity, api_key):
    nonce = nonce_str()
    params = [('mch_appid', entity.get('appid')),
              ('mchid', entity.get('mch_id')),
              ('device_info', 'WEB'),
              ('nonce_str', nonce),
              ('partner_trade_no', entity.get('partner_trade_no')),
              ('openid', entity.get('openid')),
              ('check_name', 'NO_CHECK'),
              ('amount', entity.get('amount')),
              ('desc', 'Cash out'),
              ('spbill_create_ip', entity.get('ip'))]
    pay_sign = sign(params, api_key)
    params.append(('sign', pay_sign))

    root = ET.Element('xml')

    for key, value in params:
        node = ET.SubElement(root, key)
        if isinstance(value, unicode):
            node.text = value.encode('utf8')
        else:
            node.text = str(value)

    return ET.tostring(root)


def parse_prepay_result(content):
    """
    :param content: `class`:`str`
    :return:  (`class`:`bool`, `class`:`str`)
    """
    try:
        root = ET.XML(content)
        params = dict([(e.tag, e.text) for e in root])
        if params['return_code'].lower() == FAIL:
            return False, params['return_msg']
        if params['result_code'].lower() == FAIL:
            return False, params['err_code']
        return True, params['prepay_id']
    except ET.ParseError as e:
        return False, e.message


def parse_company_pay_result(content):
    """
    :param content: `class`:`str`
    :return:  (`class`:`bool`, `class`:`str`)
    """
    try:
        root = ET.XML(content)
        params = dict([(e.tag, e.text) for e in root])
        if params['return_code'].lower() == FAIL:
            return False, params
        if params['result_code'].lower() == FAIL:
            return False, params
        return True, params
    except ET.ParseError as e:
        return False, e.message


def make_response_content(return_code='SUCCESS', return_message="OK"):
    root = ET.Element('xml')
    code = ET.SubElement(root, 'return_code')
    code.text = return_code
    message = ET.SubElement(root, 'return_msg')
    message.text = return_message
    return ET.tostring(root)


def valid_message(params, api_key):
    old_sign = params.pop('sign')
    new_sign = sign(params.items(), api_key)
    return old_sign == new_sign


if __name__ == '__main__':
    from bunch import Bunch

    entity = Bunch(appid='001', mch_id='002', body='body', detail='detail', out_trade_no='out_trade_no',
                   total_fee=10000,
                   spbill_create_ip='127.0.0.1', time_start='20091225091010', time_expire='20091225091010',
                   notify_url='http://www.weixin.qq.com/wxpay/pay.php', openid='1111111111')
    print make_prepay_id(entity, 'api_key')
    xml = """<xml>
       <return_code><![CDATA[SUCCESS]]></return_code>
       <return_msg><![CDATA[OK]]></return_msg>
       <appid><![CDATA[wx2421b1c4370ec43b]]></appid>
       <mch_id><![CDATA[10000100]]></mch_id>
       <nonce_str><![CDATA[IITRi8Iabbblz1Jc]]></nonce_str>
       <sign><![CDATA[7921E432F65EB8ED0CE9755F0E86D72F]]></sign>
       <result_code><![CDATA[SUCCESS]]></result_code>
       <prepay_id><![CDATA[wx201411101639507cbf6ffd8b0779950874]]></prepay_id>
       <trade_type><![CDATA[JSAPI]]></trade_type>
    </xml>"""
    print parse_prepay_result(xml)
