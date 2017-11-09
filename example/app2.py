# -:- coding:utf8 -:-
"""
swagger: http://127.0.0.1:5000/api/spec.html
"""
from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from flask_restful import fields
from flask_restful_swagger import swagger
from flask_sqlalchemy import SQLAlchemy

from flask_kits.restful.entity import EntityBase
from flask_kits.restful.entity import Field
from flask_kits.restful.entity import MaxLengthValidator
from flask_kits.restful.entity import MinLengthValidator
from flask_kits.restful.entity import Response

config = {
    'SQLALCHEMY_DATABASE_URI': "mysql+pymysql://root:root@10.16.76.245:3306/coffee"
}

app = Flask(__name__)
app.config.from_mapping(config)
api = swagger.docs(Api(app), apiVersion="1.0")
db = SQLAlchemy(app)


class UserResponse(Response):
    __exclude_fields__ = ['Name']
    Name = fields.String
    Password = fields.String
    ID = fields.Integer


LITERAL = {'false': False, 'true': True}


class UserEntity(EntityBase):
    Name = Field('Name', validators=[MinLengthValidator(10)])
    LoginID = Field('LoginID', validators=[MinLengthValidator(2), MaxLengthValidator(20)])
    Password = Field("Password", validators=[MinLengthValidator(8), MaxLengthValidator(16)])
    Marriage = Field("Marriage", location='header')


class UserApi(Resource):
    @UserEntity.parameter
    @UserResponse.single
    def post(self, entity):
        """新接口测试"""
        print(entity)


api.add_resource(UserApi, '/users')
if __name__ == '__main__':
    # print(app.url_map)
    app.run()
