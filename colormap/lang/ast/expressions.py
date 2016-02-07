from collections import namedtuple
from .core import TreeNode


class VectorAssignment(TreeNode, namedtuple('VectorAssignment', ('variable', 'expression'))):
    pass


class NumberAssignment(TreeNode, namedtuple('NumberAssignment', ('variable', 'expression'))):
    pass


class LiteralVector(TreeNode, namedtuple('LiteralVector', ('elements',))):
    pass


class VectorIndexation(TreeNode, namedtuple('VectorIndexation', ('vector', 'index'))):
    pass


class Multiplication(TreeNode, namedtuple('Multiplication', ('left', 'right'))):
    pass


class Division(TreeNode, namedtuple('Division', ('left', 'right'))):
    pass


class Addition(TreeNode, namedtuple('Addition', ('left', 'right'))):
    pass


class Subtraction(TreeNode, namedtuple('Subtraction', ('left', 'right'))):
    pass


class Inversion(TreeNode, namedtuple('Inversion', ('value',))):
    pass