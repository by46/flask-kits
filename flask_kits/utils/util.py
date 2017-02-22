import time
from decimal import Decimal

__all__ = ['purge_sum_result', 'timestamp', 'get_raw_path']


def purge_sum_result(result, field_name='amount', default=None):
    key = '{0}__sum'.format(field_name)
    if default is None:
        default = Decimal('0')

    return result.get(key) or default


def timestamp():
    return str(int(time.time()))


def get_raw_path(request):
    path = request.path
    if 'QUERY_STRING' in request.META and request.META.get('QUERY_STRING'):
        path += '?' + request.META.get('QUERY_STRING')
    return path
