from functools import partial

from bunch import Bunch
from flask import request
from flask_login import current_user
from flask_menu import MenuEntryMixin
from flask_menu import current_menu
from flask_menu import register_menu


def visible_when(roles):
    """

    :param list[str] roles: 
    :return: 
    """
    if not roles:
        return True

    actual_roles = set(roles)
    expect_roles = set()
    if hasattr(current_user, 'role'):
        expect_roles.add(current_user.role.name)

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            expect_roles.add(role.name)
    return actual_roles & expect_roles


def active_when(menu_item):
    """

    :param MenuEntryMixin menu_item: 
    :return: 
    """
    if request.endpoint == menu_item._endpoint:
        return True

    return False


def config_menu(app, items):
    """
    items contains menu item, like below
    {'name': 'profile', 'text': 'Home', 'roles': ['admin'], 'order': 1}

    :param flask.Flask app:
    :param list[Bunch] items:

    """
    if not items:
        return

    @app.before_first_request
    def before_first_request():
        for item in items:
            name = item.pop('name')
            menu_item = current_menu.submenu(name)  # type: MenuEntryMixin
            item.endpoint = None
            item.visible_when = partial(visible_when, item.get('roles'))
            # kwargs['active_when'] = active_when
            menu_item.register(**item)


def register_menu_ex(app, path, text, **kwargs):
    """
    :param app:
    :param path:
    :param text:
    :param kwargs:

    """
    new_visible_when = partial(visible_when, kwargs.get('roles'))
    kwargs['visible_when'] = new_visible_when
    return register_menu(app, path, text, **kwargs)


register_menu = partial(register_menu, visible_when=visible_when)
