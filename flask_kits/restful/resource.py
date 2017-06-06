# -:- coding:utf8 -:-

from flask_login import login_required
from flask_restful import Resource

from flask_kits.decorators import manager_required
from flask_kits.decorators import wx_required


class WxBusinessResource(Resource):
    method_decorators = [wx_required, login_required]


class BusinessResource(Resource):
    method_decorators = [login_required, manager_required]
