from functools import wraps

from flask import abort
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from furl import furl


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(401)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required()(f)


def common_required(validate_permission):
    """
    common required decorator, used to simple permission validate
    :param validate_permission: `class`:`func`
    :return:
    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not validate_permission(current_user):
                abort(401)
            return func(*args, **kwargs)

        return decorated_function

    return decorator


def wx_required(func):
    """
    require wx login
    :param func:
    :return:
    """
    return common_required(lambda user: user.is_wx_user)(func)


def manager_required(func):
    """
    require portal login
    :param func:
    :return:
    """
    return common_required(lambda user: user.is_manager_user)(func)


def h5_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_wx_user:
            location = url_for('h5.router')
            url = furl(location)
            end_point = request.endpoint
            view = end_point.split('.')[-1]
            redirect_url = furl(request.full_path)
            redirect_url.path = view
            url.query.params['redirect_uri'] = redirect_url.url
            return redirect(url.url)
        return func(*args, **kwargs)

    return decorated_function


def portal_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_manager_user:
            location = url_for('auth.login')
            return redirect(location)
        return func(*args, **kwargs)

    return decorated_function
