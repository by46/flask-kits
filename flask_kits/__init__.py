# -:- coding:utf8 -:-
"""

"""

from flask_kits.routing import KitRule

__author__ = 'benjamin.c.yan'
__version__ = '0.0.6'

missing = object()


class Kits(object):
    PREFIX = 'KITS'

    def __init__(self, app=None, **kwargs):
        # from flask import Flask
        # Flask.url_rule_class = KitRule
        self._app = None
        self.app_name = 'recipe'
        self._options = {}
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        self._app = app
        self._options.update(kwargs)
        self.app_name = self.get_parameter('app_name')

        if not hasattr(app, 'extensions'):
            app.extensions = {}

            # jsapi.init_extension(self, app)
            # wxapi.init_extension(self, app)
            # sms.init_extension(self, app)
            # tm.init_extension(self, app)

    def get_parameter(self, name, default=None):
        option = self._options.get(name, missing)
        app = self._app
        if option is missing:
            parameter_name = '{0}_{1}'.format(Kits.PREFIX, name.upper())
            option = app.config.get(parameter_name, default)
        return option
