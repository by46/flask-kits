from decimal import Decimal

from dateutil.parser import parse

LITERAL = {
    'false': False,
    'true': True,
    '0': False,
    '1': True,
    't': True,
    'f': False}


def compatible_bool(value):
    """it's used to reqparser.RequestParser

    Example:
        >>> from flask_restful import reqparse
        >>> parser = reqparse.RequestParser()
        >>> parser.add_argument('marriaged', type=compatible_bool, help='accept false and true string')
    :param value:
    :return:
    """
    if isinstance(value, basestring):
        json_value = value.lower()
        if json_value in LITERAL:
            return LITERAL.get(json_value)
    return bool(value)


def compatible_datetime(value, name):
    return parse(value)


def compatible_decimal(value):
    try:
        return Decimal(value)
    except Exception:
        return None
