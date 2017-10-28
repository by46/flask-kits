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

from flask_kits.restful import Serializer
from flask_kits.restful.entity import EntityBase
from flask_kits.restful.entity import Field
from flask_kits.restful.entity import MaxLengthValidator
from flask_kits.restful.entity import MinLengthValidator
from flask_kits.restful.entity import MoreValidator
from flask_kits.restful.entity import Response

config = {
    'SQLALCHEMY_DATABASE_URI': "mysql+pymysql://root:root@10.16.76.245:3306/coffee"
}

app = Flask(__name__)
app.config.from_mapping(config)
api = swagger.docs(Api(app), apiVersion="1.0")
db = SQLAlchemy(app)


class Code(EntityBase):
    Code = Field('Code', type=int)


class Address(EntityBase):
    Zip = Field("Zip", type=int)
    Detail = Field('Detail', type=Code)


class Entity(EntityBase):
    Name = Field('Name', location='json')
    Age = Field("Age", location='json', type=int, action='append', validators=[MoreValidator(40)])
    Address = Field("Address", type=Address, action='append')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))


class UserSerializer(Serializer):
    """User"""
    __model__ = User
    __exclude_fields__ = ['password_hash']
    __include_fields__ = {'is_administrator': fields.Boolean}
    __new_entity_fields__ = ['name', ('age', fields.Boolean)]


class UserResponse(Response):
    __model__ = User
    __exclude_fields__ = ['Name']
    Name = fields.String
    Password = fields.String
    ID = fields.Integer


class UserApi(Resource):
    @UserSerializer.list()
    def get(self):
        return User.query

    @UserSerializer.entity_parameter(entity_name='InputUser')
    @UserSerializer.single
    def post(self):
        return User()


api.add_resource(UserApi, '/users')


class User2Api(Resource):
    @Entity.parameter
    @UserSerializer.single
    def post(self, entity):
        print(entity, entity)


api.add_resource(User2Api, '/users2')


class UserEntity(EntityBase):
    Name = Field('Name', validators=[MinLengthValidator(10)])
    LoginID = Field('LoginID', validators=[MinLengthValidator(2), MaxLengthValidator(20)])
    Password = Field("Password", validators=[MinLengthValidator(8), MaxLengthValidator(16)])


class User3Api(Resource):
    @UserEntity.parameter
    @UserResponse.single
    def post(self, entity):
        """新接口测试"""
        print(entity)


api.add_resource(User3Api, '/users3')
if __name__ == '__main__':
    # print(app.url_map)
    app.run()
