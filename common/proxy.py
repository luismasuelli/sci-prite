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
               'getitem', 'setitem', 'delitem', 'get', 'set', 'del'}


class Proxy(object):

    def __setattr__(self, key, value):
        if key == '_':
            # This check will stand good for when we assign the proxy var.
            return super(Proxy, self).__setattr__(key, value)
        return setattr(self._, key, value)

    def __getattr__(self, item):
        # This one, for when the attribute is not proxy var nor the proxied object.
        return getattr(self._, item)

    def __delattr__(self, item):
        if item == '_':
            # This function will stand good for when we delete the proxy var.
            return super(Proxy, self).__delattr__(item)
        return delattr(self._, item)

    def __str__(self, *args, **kwargs):
        return self._.__str__(*args, **kwargs)

    def __complex__(self, *args, **kwargs):
        return self._.__complex__(*args, **kwargs)

    def __unicode__(self, *args, **kwargs):
        return self._.__unicode__(*args, **kwargs)

    def __bytes__(self, *args, **kwargs):
        return self._.__bytes__(*args, **kwargs)

    def __int__(self, *args, **kwargs):
        return self._.__int__(*args, **kwargs)

    def __long__(self, *args, **kwargs):
        return self._.__long__(*args, **kwargs)

    def __bool__(self, *args, **kwargs):
        return self._.__bool__(*args, **kwargs)

    def __float__(self, *args, **kwargs):
        return self._.__float__(*args, **kwargs)

    def __nonzero__(self, *args, **kwargs):
        return self._.__nonzero__(*args, **kwargs)

    def __index__(self, *args, **kwargs):
        return self._.__index__(*args, **kwargs)

    def __hash__(self, *args, **kwargs):
        return self._.__hash__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self._.__len__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        return self._.__le__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        return self._.__lt__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return self._.__ge__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        return self._.__gt__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self._.__ne__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        return self._.__eq__(*args, **kwargs)

    def __cmp__(self, *args, **kwargs):
        return self._.__cmp__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._.__call__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self._.__iter__(*args, **kwargs)

    def __missing__(self, *args, **kwargs):
        return self._.__missing__(*args, **kwargs)

    def __reversed__(self, *args, **kwargs):
        return self._.__reversed__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self._.__contains__(*args, **kwargs)

    def __add__(self, *args, **kwargs):
        return self._.__add__(*args, **kwargs)

    def __sub__(self, *args, **kwargs):
        return self._.__sub__(*args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self._.__mul__(*args, **kwargs)

    def __div__(self, *args, **kwargs):
        return self._.__div__(*args, **kwargs)

    def __truediv__(self, *args, **kwargs):
        return self._.__truediv__(*args, **kwargs)

    def __floordiv__(self, *args, **kwargs):
        return self._.__floordiv__(*args, **kwargs)

    def __mod__(self, *args, **kwargs):
        return self._.__mod__(*args, **kwargs)

    def __divmod__(self, *args, **kwargs):
        return self._.__divmod__(*args, **kwargs)

    def __pow__(self, *args, **kwargs):
        return self._.__pow__(*args, **kwargs)

    def __lshift__(self, *args, **kwargs):
        return self._.__lshift__(*args, **kwargs)

    def __rshift__(self, *args, **kwargs):
        return self._.__rshift__(*args, **kwargs)

    def __and__(self, *args, **kwargs):
        return self._.__and__(*args, **kwargs)

    def __or__(self, *args, **kwargs):
        return self._.__or__(*args, **kwargs)

    def __xor__(self, *args, **kwargs):
        return self._.__xor__(*args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        return self._.__iadd__(*args, **kwargs)

    def __isub__(self, *args, **kwargs):
        return self._.__isub__(*args, **kwargs)

    def __imul__(self, *args, **kwargs):
        return self._.__imul__(*args, **kwargs)

    def __idiv__(self, *args, **kwargs):
        return self._.__idiv__(*args, **kwargs)

    def __itruediv__(self, *args, **kwargs):
        return self._.__itruediv__(*args, **kwargs)

    def __ifloordiv__(self, *args, **kwargs):
        return self._.__ifloordiv__(*args, **kwargs)

    def __imod__(self, *args, **kwargs):
        return self._.__imod__(*args, **kwargs)

    def __idivmod__(self, *args, **kwargs):
        return self._.__idivmod__(*args, **kwargs)

    def __ipow__(self, *args, **kwargs):
        return self._.__ipow__(*args, **kwargs)

    def __ilshift__(self, *args, **kwargs):
        return self._.__ilshift__(*args, **kwargs)

    def __irshift__(self, *args, **kwargs):
        return self._.__irshift__(*args, **kwargs)

    def __iand__(self, *args, **kwargs):
        return self._.__iand__(*args, **kwargs)

    def __ior__(self, *args, **kwargs):
        return self._.__ior__(*args, **kwargs)

    def __ixor__(self, *args, **kwargs):
        return self._.__ixor__(*args, **kwargs)

    def __radd__(self, *args, **kwargs):
        return self._.__radd__(*args, **kwargs)

    def __rsub__(self, *args, **kwargs):
        return self._.__rsub__(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return self._.__rmul__(*args, **kwargs)

    def __rdiv__(self, *args, **kwargs):
        return self._.__rdiv__(*args, **kwargs)

    def __rtruediv__(self, *args, **kwargs):
        return self._.__rtruediv__(*args, **kwargs)

    def __rfloordiv__(self, *args, **kwargs):
        return self._.__rfloordiv__(*args, **kwargs)

    def __rmod__(self, *args, **kwargs):
        return self._.__rmod__(*args, **kwargs)

    def __rdivmod__(self, *args, **kwargs):
        return self._.__rdivmod__(*args, **kwargs)

    def __rpow__(self, *args, **kwargs):
        return self._.__rpow__(*args, **kwargs)

    def __rlshift__(self, *args, **kwargs):
        return self._.__rlshift__(*args, **kwargs)

    def __rrshift__(self, *args, **kwargs):
        return self._.__rrshift__(*args, **kwargs)

    def __rand__(self, *args, **kwargs):
        return self._.__rand__(*args, **kwargs)

    def __ror__(self, *args, **kwargs):
        return self._.__ror__(*args, **kwargs)

    def __rxor__(self, *args, **kwargs):
        return self._.__rxor__(*args, **kwargs)

    def __neg__(self, *args, **kwargs):
        return self._.__neg__(*args, **kwargs)

    def __pos__(self, *args, **kwargs):
        return self._.__pos__(*args, **kwargs)

    def __abs__(self, *args, **kwargs):
        return self._.__abs__(*args, **kwargs)

    def __invert__(self, *args, **kwargs):
        return self._.__invert__(*args, **kwargs)

    def __oct__(self, *args, **kwargs):
        return self._.__oct__(*args, **kwargs)

    def __hex__(self, *args, **kwargs):
        return self._.__hex__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self._.__repr__(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        return self._.__enter__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        return self._.__exit__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self._.__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        return self._.__setitem__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self._.__delitem__(*args, **kwargs)

    def __get__(self, *args, **kwargs):
        return self._.__get__(*args, **kwargs)

    def __set__(self, *args, **kwargs):
        return self._.__set__(*args, **kwargs)
