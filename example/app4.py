class Model(object):
    """model class

    hello world
    >>> i =1
    >>> print(i)
    """

    def get(self, x, y=12):
        # hello world
        print('get')


if __name__ == '__main__':
    import inspect

    print(inspect.getdoc(Model))
    print(inspect.getcomments(Model))
    print(inspect.getcomments(Model.get))
    print(inspect.getfile(Model))
    print(inspect.getmodule(Model))
