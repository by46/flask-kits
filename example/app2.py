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
from werkzeug.datastructures import FileStorage

from flask_kits.restful import compatible_bool
from flask_kits.restful.entity import EntityBase
from flask_kits.restful.entity import Field
from flask_kits.restful.entity import LOC_ARGS
from flask_kits.restful.entity import LOC_FILES
from flask_kits.restful.entity import LOC_HEADERS
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
    Marriage = Field("Marriage", type=compatible_bool, location=LOC_HEADERS)


class UserFormEntity(EntityBase):
    Name = Field("Name", location=LOC_HEADERS)
    Sex = Field("Sex", location=LOC_ARGS)
    Attachment = Field("Attachment", type=FileStorage, location=LOC_FILES)


class UserApi(Resource):
    @UserEntity.parameter
    @UserResponse.single
    def post(self, entity):
        """新接口测试"""
        print(entity)

    @UserFormEntity.parameter
    @UserResponse.single
    def put(self, entity):
        """multi form"""
        print(entity)


api.add_resource(UserApi, '/users')
if __name__ == '__main__':
    # print(app.url_map)
    app.run()
