from flask import Flask
from flask_restful import Api
from flask_restful import fields
from flask_restful_swagger import swagger
from flask_restful_swagger.swagger import model
from flask_restful_swagger.swagger import operation

from flask_restful import Resource

app = Flask(__name__)
restful_api = Api(app)
restful_api = swagger.docs(api=restful_api)  # type: Api


@model
class Version(object):
    resource_fields = {
        'ID': fields.Integer
    }


@restful_api.resource('/version')
class VersionResource(Resource):
    @operation(notes="hello",
               responseClass=Version.__class__)
    def get(self): pass


def class_decorator(func):
    return func


def func_decorator(func):
    return func


@class_decorator
class Demo(object):
    @func_decorator
    def get(self):
        pass


if __name__ == '__main__':
    app.run()
