from flask_restful import fields


class ISODateTime(fields.DateTime):
    def __init__(self):
        super(ISODateTime, self).__init__(dt_format="iso8601")

    def format(self, value):
        return super(ISODateTime, self).format(value) + "Z"


class RFC822DateTime(fields.DateTime):
    def __init__(self):
        super(RFC822DateTime, self).__init__(dt_format="rfc822")
