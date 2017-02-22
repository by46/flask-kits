# -*- coding:utf-8 -*-
import logging
from datetime import datetime

import requests


class TemplateMessage(object):
    logger = logging.getLogger('drp.muggle')
    _session = requests.session()

    @staticmethod
    def make_timestamp(today=None):
        if today is None:
            today = datetime.now()
        return u"{0}年{1}月{2}日 {3:02}:{4:02}:{5:02}".format(today.year, today.month, today.day, today.hour,
                                                           today.minute, today.second)

    @staticmethod
    def build_retrieve_template_id_url(access_token):
        return 'https://api.weixin.qq.com/cgi-bin/template/api_add_template?access_token={0}'.format(access_token)

    @staticmethod
    def build_send_message_url(access_token):
        return 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}'.format(access_token)

    @staticmethod
    def send_message(message_id, open_id, **kwargs):
        from flask_kits import JsApi as  access
        access_token = access.token

        try:
            url = TemplateMessage.build_send_message_url(access_token)
            pay_load = {
                "touser": open_id,
                "template_id": message_id,
                "url": "{0}/drp/h5/ordinary_member".format(settings.APP_DOMAIN),
                'data': {key: dict(value=value) for key, value in kwargs.iteritems()}}
            response = TemplateMessage._session.post(url, json=pay_load, verify=False)
            result = response.json()
            if result['errcode']:
                TemplateMessage.logger.error(u'send template message failure, error code: %s, error message: %s',
                                             result['errcode'], result['errmsg'])
                return False
            return True
        except Exception, e:
            TemplateMessage.logger.exception(e)
            return False

    @staticmethod
    def send_pay_message(open_id, follower_nick_name, item_name, price):

        kwargs = dict(first=u"你的下级已购买一件商品",
                      keyword1=follower_nick_name,
                      keyword2=item_name,
                      keyword3=u"{0} 元".format(price),
                      keyword4=TemplateMessage.make_timestamp(),
                      remark=u"购买成功后你将获得返利")
        return TemplateMessage.send_message(settings.TPL_PAY, open_id, **kwargs)

    @staticmethod
    def send_new_follow_message(open_id, follower_nick_name):
        kwargs = dict(first=u"你新增了一个下级会员",
                      keyword1=follower_nick_name,
                      keyword2=TemplateMessage.make_timestamp(),
                      remark=u"")
        return TemplateMessage.send_message(settings.TPL_NEW_FOLLOW, open_id, **kwargs)

    @staticmethod
    def send_bonus_message(open_id, item_name, total_bonus, voucher, order_cost, available_date):
        kwargs = dict(first=u"你有下级会员购买成功，给你的返利已到账",
                      keyword1=item_name,
                      keyword2=str(total_bonus),
                      keyword3=str(order_cost),
                      keyword4=TemplateMessage.make_timestamp(available_date),
                      remark=u"其中有{0}元是代金券".format(voucher))
        return TemplateMessage.send_message(settings.TPL_BONUS, open_id, **kwargs)


if __name__ == '__main__':
    TemplateMessage.send_pay_message('o7unIwPw8iiTSvQpQe6QcMRtJapA', follower_nick_name="Neo",
                                     item_name="Demo product", price=12.19)
