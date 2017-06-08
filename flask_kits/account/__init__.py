from functools import partial

from bunch import Bunch

PREFIX_WX = "wx"
PREFIX_MANAGER = "manager"


def wrap_user_id(prefix, user_id):
    return "{prefix}_{id}".format(prefix=prefix, id=user_id)


wrap_user = partial(wrap_user_id, PREFIX_MANAGER)
wrap_wx = partial(wrap_user_id, PREFIX_WX)


def unwrap(identity):
    """
    :param str identity:
    :rtype Bunch
    """
    if not identity:
        return None

    prefix, delimiter, user_id = identity.partition('_')
    if not delimiter:
        return None

    return Bunch(id=int(user_id), is_wx_user=prefix == PREFIX_WX)
