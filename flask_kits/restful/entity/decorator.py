import functools

from flask_kits.restful import post_parameter


def parameter(schema):
    """
    :param EntityBase schema:
    """

    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            entity = schema.parse()
            kwargs['entity'] = entity
            return f(*args, **kwargs)

        # Support swagger document
        if '__swagger_attr' in f.__dict__:
            attr = wrapped.__dict__['__swagger_attr'] = f.__dict__['__swagger_attr']
            params = attr.get('parameters', [])
            params.append(post_parameter(schema))
        return wrapped

    return wrapper
