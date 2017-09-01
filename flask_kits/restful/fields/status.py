from flask_restful import fields


class YNStatusFields(fields.Raw):
    def format(self, value):
        return value.lower() == 'y'
