import functools
import inspect
from datetime import datetime
from decimal import Decimal

import flask_restful.fields
from flask_restful import abort
from flask_restful.reqparse import Argument
from flask_restful.reqparse import RequestParser
from flask_restful_swagger import swagger
from six import add_metaclass
from six import iteritems
from six import text_type
from werkzeug.datastructures import MultiDict

from flask_kits.restful import post_parameter

MAPPINGS = {
    int: flask_restful.fields.Integer,
    float: flask_restful.fields.Float,
    text_type: flask_restful.fields.String,
    datetime: flask_restful.fields.DateTime,
    Decimal: flask_restful.fields.String,
    bool: flask_restful.fields.Boolean
}


# optimize this code
def get_field_type(class_type):
    return MAPPINGS.get(class_type)


class EntityDeclarative(type):
    def __new__(cls, class_name, bases, attributes):
        if class_name == 'EntityBase':
            return type.__new__(cls, class_name, bases, attributes)

        parser = RequestParser()
        fields = [(name, field) for name, field in iteritems(attributes) if isinstance(field, Field)]

        field_names = set()
        resource_fields = dict()
        for key, field in fields:
            if inspect.isclass(field.type) and issubclass(field.type, EntityBase):
                resource_fields[key] = flask_restful.fields.Nested(field.type.resource_fields)
                field.type = field.type.parse
                field.location = 'json'
            else:
                resource_fields[key] = get_field_type(field.type)
            parser.add_argument(field)
            field_names.add(key)
            del attributes[key]
        attributes['entity_parser'] = parser
        attributes['entity_fields'] = field_names
        attributes['resource_fields'] = resource_fields

        schema = type.__new__(cls, class_name, bases, attributes)
        # support swagger
        swagger.add_model(schema)
        return schema


# TODO(benjamin): optimize
class WrappedDict(dict):
    def __init__(self, source):
        super(WrappedDict, self).__init__(**source)

    def json(self):
        return MultiDict(self)

    def values(self):
        return None


@add_metaclass(EntityDeclarative)
class EntityBase(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    @classmethod
    def parse(cls, req=None):
        """

        :param req: 
        :rtype: EntityBase
        """
        if isinstance(req, dict):
            req = WrappedDict(req)
        instance = cls()  # type: EntityBase
        args = cls.entity_parser.parse_args(req)
        for field in cls.entity_fields:
            setattr(instance, field, args[field])
        success = instance.validate()
        if isinstance(success, ValueError):
            abort(400, message={'error': text_type(success)})
        return instance

    @classmethod
    def parameter(cls, f):
        """
        :param EntityBase cls:
        :param f:
        """

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            entity = cls.parse()
            kwargs['entity'] = entity
            return f(*args, **kwargs)

        # Support swagger document
        if '__swagger_attr' in f.__dict__:
            attr = wrapped.__dict__['__swagger_attr'] = f.__dict__['__swagger_attr']
            params = attr.get('parameters', [])
            params.append(post_parameter(cls))
        return wrapped

    def validate(self):
        """
        :rtype: (bool|ValueError)
        """
        return True

    def handle_error(self):
        pass


class Field(Argument):
    def __init__(self, name, *args, **kwargs):
        kwargs.setdefault('type', text_type)
        self.validators = set()
        if 'validators' in kwargs:
            self.validators = kwargs.pop('validators')
        super(Field, self).__init__(name, *args, **kwargs)

    def parse(self, request, bundle_errors=False):
        value, found = super(Field, self).parse(request, bundle_errors)
        if not isinstance(value, ValueError) and self.validators:
            for validator in self.validators:
                success = validator(value)
                if isinstance(success, ValueError):
                    found = {self.name: text_type(success)}
                    value = ValueError()
                    break
        return value, found
