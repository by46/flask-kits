# -:- coding:utf8 -:-


class KitsError(Exception):
    pass


class RestfulError(KitsError):
    pass


class InvalidFormatError(RestfulError):
    def __init__(self):
        super(InvalidFormatError, self).__init__("range must be like: 'id ..;order=id,max=20;'")
