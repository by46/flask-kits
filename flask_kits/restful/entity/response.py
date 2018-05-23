from flask_restful import fields
from flask_restful import marshal_with
from flask_restful_swagger import swagger
from six import add_metaclass
from six import iteritems

from flask_kits.restful import Paginate
from flask_kits.restful import filter_params
from flask_kits.restful.swagger import post_parameter


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
MAPPINGS = {

}
"""
integer
number
string
boolean
"""


class ResponseDeclarative(type):
    def __new__(cls, name, bases, attributes):
        if name == 'Response':
            return type.__new__(cls, name, bases, attributes)

        model = attributes.pop('__model__', None)  # type: User
        exclude_fields = attributes.pop('__exclude_fields__', [])
        class_dict = attributes.copy()
        class_dict['resource_fields'] = resource_fields = {}
        class_dict['exclude_fields'] = exclude_fields
        if model:
            for column in model.__table__.columns:
                if column.name in exclude_fields:
                    continue
                field_type_name = column.type.__visit_name__
                field_type = MAPPING.get(field_type_name)
                if not field_type:
                    field_type = fields.String
                resource_fields[column.name] = field_type
        extra_fields = {}
        for name, field in iteritems(attributes):
            if name.startswith('_'):
                continue

            if isinstance(field, (fields.Raw,)):
                extra_fields[name] = field
            elif isinstance(type(field), type) and issubclass(field, fields.Raw):
                extra_fields[name] = field

        resource_fields.update(extra_fields)
        s = type.__new__(cls, name, bases, class_dict)
        swagger.add_model(s)
        return s


@add_metaclass(ResponseDeclarative)
class Response(object):
    @classmethod
    def operation(cls, f, paginate=True):
        attr = {
            'notes': f.__doc__ or f.__name__,
            'nickname': f.__name__,
            'responseClass': cls,
            'parameters': filter_params() if paginate else []
        }

        return attr

    @classmethod
    def parameter(cls, name=None, description=None, data_type='str', param_type='query', required=False):
        def decorator(func):
            attr = func.__dict__['__swagger_attr']
            params = attr.get('parameters', [])
            if hasattr(data_type, 'resource_fields'):
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
    def authorization_parameter(cls, func):
        decorator = cls.parameter(name='Authorization', data_type='str', param_type='header', required=True)
        return decorator(func)

    @classmethod
    def entity_parameter(cls, entity_name):
        def wrapper(func):
            attr = func.__dict__['__swagger_attr']
            params = attr.get('parameters', [])
            resource_fields = {}
            for field in cls.new_entity_fields:
                if isinstance(field, tuple):
                    name, schema_type = field
                else:
                    name, schema_type = field, cls.resource_fields.get(field)
                resource_fields[name] = schema_type
            attributes = {'resource_fields': resource_fields,
                          '__doc__': 'create new entity'}
            entity_model = type(entity_name, (object,), attributes)
            swagger.add_model(entity_model)
            params.append(post_parameter(entity_model))
            attr['parameters'] = params
            return func

        return wrapper

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
