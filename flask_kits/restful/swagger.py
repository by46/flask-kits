def post_parameter(model_class):
    return {
        'name': 'entity',
        'description': model_class.__doc__,
        'required': True,
        'dataType': model_class.__name__,
        'paramType': 'body'
    }
