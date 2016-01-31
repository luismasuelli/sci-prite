import six


PROXY_MAGIC = {'str', 'complex', 'unicode', 'bytes', 'int', 'long', 'bool', 'float', 'nonzero', 'index', 'hash', 'len',
               'le', 'lt', 'ge', 'gt', 'ne', 'eq', 'cmp', 'call', 'iter', 'missing', 'reversed', 'contains',
               'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'divmod', 'pow', 'lshift', 'rshift',
               'and', 'or', 'xor',
               'iadd', 'isub', 'imul', 'idiv', 'itruediv', 'ifloordiv', 'imod', 'idivmod', 'ipow', 'ilshift', 'irshift',
               'iand', 'ior', 'ixor',
               'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rdivmod', 'rpow', 'rlshift', 'rrshift',
               'rand', 'ror', 'rxor',
               'neg', 'pos', 'abs', 'invert',
               'oct', 'hex', 'repr',
               'enter', 'exit',
               'getattr', 'setattr', 'getattribute', 'delattr', 'getitem', 'setitem', 'delitem', 'get', 'set', 'del'}


class OperatorProxyMeta(object):
    """
    For the operator magic methods, this metaclass will create a method when needed and non-existent.
    """

    def __getattribute__(self, item):
        """
        Same as always for non-magic methods.

        For magic methods
        :param item:
        :return:
        """

        proxy_var = self.proxy_var

        if not hasattr(self, item):
            if item[:2] == '__' and item[-2:] == '__':
                name = item[2:-2]
                if name in PROXY_MAGIC:
                    # We must implement a magic method by proxying.
                    def method(self, *args, **kwargs):
                        return getattr(getattr(self, proxy_var), item)(*args, **kwargs)
                    setattr(self, item, method)
        return super(OperatorProxyMeta, self).__getattribute__(item)


class Proxy(six.with_metaclass(OperatorProxyMeta)):
    pass