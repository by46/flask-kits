import inspect

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
        exclude_fields = attributes.pop('__exclude_fields__', [])
        include_fields = attributes.pop('__include_fields__', {})
        new_entity_fields = attributes.pop('__new_entity_fields__', [])
        class_dict = attributes.copy()
        class_dict['resource_fields'] = resource_fields = {}
        class_dict['exclude_fields'] = exclude_fields
        class_dict['include_fields'] = include_fields
        class_dict['new_entity_fields'] = new_entity_fields
        if model:
            for column in model.__table__.columns:
                if column.name in exclude_fields:
                    continue
                field_type_name = column.type.__visit_name__
                field_type = MAPPING.get(field_type_name)
                if not field_type:
                    field_type = fields.String
                resource_fields[column.name] = field_type

            if include_fields:
                resource_fields.update(include_fields)
        s = type.__new__(cls, name, bases, class_dict)
        swagger.add_model(s)
        return s


@add_metaclass(SerializerMetaclass)
class Serializer(object):
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
            # TODO(benjamin): check data_type type
            # if inspect.isclass(data_type) and issubclass(data_type, cls):
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
            wrapper = Paginate(cls.default_serializer(), item_builder=item_builder)
            wrapper = wrapper(func)
            wrapper.__dict__['__swagger_attr'] = cls.operation(func)
            return wrapper

        return decorator

    @classmethod
    def single(cls, func):
        wrapper = marshal_with(cls.default_serializer())(func)
        wrapper.__dict__['__swagger_attr'] = cls.operation(func, paginate=False)
        return wrapper

    @classmethod
    def default_serializer(cls):
        return cls.resource_fields

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__
