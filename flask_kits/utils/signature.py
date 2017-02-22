# -*- coding:utf-8 -*-
import hashlib

__author__ = 'benjamin.c.yan'


def sign(params, api_key):
    """
    signature api
    :param params: [(`class`:`str`, `class`:`object`)]
    :return: `class`:`str`
    """
    params = [(key, value) for key, value in params if value]
    params = sorted(params, key=lambda param: param[0])
    temp = u'&'.join([u'{0}={1}'.format(key, value) for key, value in params])
    temp = u'{temp}&key={key}'.format(temp=temp, key=api_key)
    return hashlib.md5(temp.encode('utf8')).hexdigest().upper()


if __name__ == '__main__':
    key1 = sign([('body', u'中文')], '192006250b4c09247ec02edce69f6a2d')
    # assert key1 == '9A0A8659F005D6984697E2CA0A9CF3B7'
    print key1
    key1 = sign([('appid', 'wxd930ea5d5a258f4f'), ('mch_id', '10000100'), ('device_info', '1000'), ('body', 'test'),
                 ('nonce_str', 'ibuaiVcKdpRxkhJA')], '192006250b4c09247ec02edce69f6a2d')
    assert key1 == '9A0A8659F005D6984697E2CA0A9CF3B7'
    print key1

    key1 = sign([('appid', 1)], '192006250b4c09247ec02edce69f6a2d')
    print key1
