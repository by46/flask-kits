# -:- coding:utf8 -:-


class KitsError(Exception):
    pass


class RestfulError(KitsError):
    pass


class InvalidFormatError(RestfulError):
    def __init__(self):
        super(InvalidFormatError, self).__init__("range must be like: 'id ..;order=asc,max=20;'")
