from flask_restful import fields
from flask_restful import marshal_with
from flask_restful_swagger import swagger
from six import add_metaclass

from flask_kits.restful import Paginate
from flask_kits.restful import filter_params
from .swagger import post_parameter


class LocalDateTime(fields.DateTime):
    def format(self, value):
        result = super(LocalDateTime, self).format(value)
        return result.replace('T', ' ')


MAPPING = {
    'integer': fields.Integer,
    'boolean': fields.Boolean,
    'date': LocalDateTime(dt_format='iso8601'),
    'datetime': LocalDateTime(dt_format='iso8601')
}


class SerializerMetaclass(type):
    def __new__(cls, name, bases, attributes):
        if name == 'Serializer':
            return type.__new__(cls, name, bases, attributes)

        model = attributes.pop('__model__', None)  # type: User
        class_dict = attributes.copy()
        class_dict['resource_fields'] = resource_fields = {}
        if model:
            for column in model.__table__.columns:
                field_type_name = column.type.__visit_name__
                field_type = MAPPING.get(field_type_name)
                if not field_type:
                    field_type = fields.String
                resource_fields[column.name] = field_type
        s = type.__new__(cls, name, bases, class_dict)
        swagger.add_model(s)
        return s


@add_metaclass(SerializerMetaclass)
class Serializer(object):
    @classmethod
    def operation(cls, f, paginate=True):
        attr = {
            'notes': f.__doc__,
            'nickname': f.__name__,
            'responseClass': cls,
            'parameters': filter_params() if paginate else []
        }

        return attr

    @classmethod
    def parameter(cls, name, description=None, data_type='str', param_type='query', required=False):
        def decorator(func):
            attr = func.__dict__['__swagger_attr']
            params = attr.get('parameters', [])
            # TODO(benjamin): check data_type type
            if type(data_type).__name__ == 'type' and issubclass(data_type, cls):
                params.append(post_parameter(data_type))
            else:
                params.append({
                    "name": name,
                    "description": description or name,
                    "required": required,
                    "dataType": str(data_type),
                    "paramType": param_type
                })
            attr['parameters'] = params
            return func

        return decorator

    @classmethod
    def list(cls, item_builder=None):
        def decorator(func):
            wrapper = Paginate(cls.resource_fields, item_builder=item_builder)
            wrapper = wrapper(func)
            wrapper.__dict__['__swagger_attr'] = cls.operation(func)
            return wrapper

        return decorator

    @classmethod
    def single(cls, func):
        wrapper = marshal_with(cls.resource_fields)(func)
        wrapper.__dict__['__swagger_attr'] = cls.operation(func, paginate=False)
        return wrapper

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__
