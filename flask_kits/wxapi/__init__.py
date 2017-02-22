from flask import Blueprint

wx = Blueprint('wx', __name__)

from . import views

PREFIX = 'wxapi_url_prefix'


def init_extension(kits, app):
    prefix = kits.get_parameter(PREFIX)
    if not prefix:
        prefix = '/{name}/wxapi'.format(name=kits.app_name)
    wx.url_prefix = prefix
    app.register_blueprint(wx)
