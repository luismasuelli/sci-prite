from collections import namedtuple


class VectorAssignment(namedtuple('VectorAssignment', ('variable', 'expression'))):
    pass


class NumberAssignment(namedtuple('NumberAssignment', ('variable', 'expression'))):
    pass


class VectorIndexation(namedtuple('VectorIndexation', ('vector', 'index'))):
    pass


class Multiplication(namedtuple('Multiplication', ('left', 'right'))):
    pass


class Division(namedtuple('Division', ('left', 'right'))):
    pass


class Addition(namedtuple('Addition', ('left', 'right'))):
    pass


class Subtraction(namedtuple('Subtraction', ('left', 'right'))):
    pass


class Inversion(namedtuple('Inversion', ('value',))):
    pass