from flask_kits.restful.entity import EntityBase
from flask_kits.restful.entity import Field
from flask_kits.restful.entity import MoreValidator


class Entity(EntityBase):
    Name = Field('Name', location='json')
    Age = Field("Age", location='json', type=int, validators=[MoreValidator(40)])


class RequestMock(object):
    @staticmethod
    def json():
        return {'Name': 'Benjamin',
                'Age': 32}


if __name__ == '__main__':
    request = RequestMock()
    entity = Entity.parse(request)
    print(entity, entity.Name)
