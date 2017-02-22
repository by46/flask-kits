from flask_restful import fields
from flask_restful_swagger import swagger
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql import sqltypes


class Meta(type):
    MODEL_NAME = '__model_class__'
    IGNORE_FIELDS = '__ignore_fields__'
    EXTRA_FIELDS = '__extra_fields__'

    def __new__(cls, name, bases, attributes):
        model = attributes.get(Meta.MODEL_NAME)
        resource_fields = {}
        if model:
            ignore_fields = attributes.get(Meta.IGNORE_FIELDS, [])
            raw_fields = [x for x in model.__dict__ if x not in ignore_fields and not x.startswith('_')]
            for field in raw_fields:
                value = getattr(model, field)
                if isinstance(value, InstrumentedAttribute):
                    field_type = value.comparator.type
                    if isinstance(field_type, (sqltypes.String, sqltypes.Text)):
                        resource_fields[field] = fields.String
                    elif isinstance(field_type, sqltypes.Integer):
                        resource_fields[field] = fields.Integer
                    elif isinstance(field_type, sqltypes.Boolean):
                        resource_fields[field] = fields.Boolean
                    elif isinstance(field_type, sqltypes.DateTime):
                        resource_fields[field] = fields.DateTime(dt_format='iso8601')
                    elif isinstance(field_type, sqltypes.DECIMAL):
                        resource_fields[field] = fields.MyDecimal
                    else:
                        resource_fields[field] = fields.String

        # add extra fields
        extra_fields = attributes.get(Meta.EXTRA_FIELDS, {})
        if isinstance(extra_fields, dict):
            resource_fields.update(extra_fields)
        attributes['resource_fields'] = resource_fields
        meta = type.__new__(cls, name, bases, attributes)
        swagger.add_model(meta)
        return meta
