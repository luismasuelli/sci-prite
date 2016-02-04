from collections import namedtuple
from colormap.expressions import IN, sat01

_primitive = ('value',)
_binary = ('left', 'right')
_unary = ('expression',)

class Evaluable(object):

    def evaluate(self):
        raise NotImplementedError

####################################################
####################################################
#
# Data Types (these operations have top precedence).
#
####################################################
####################################################

# Some types are truly primitive:
#   Number
#   Boolean
#   None
#   String
#
# While others not:
#   Interval
#   Slice
#   Vector (either boolean or numeric; just a tuple)
#   IndexVector (like a vector but capable of holding slices and numbers, mixed fashion)
#   Indexing/Masking
#   Saturation

class Primitive(Evaluable, namedtuple('Primitive', _primitive)):

    def evaluate(self):
        return self.expression

class Interval(Evaluable, namedtuple('Interval', ('min', 'max', 'strict_min', 'strict_max'))):

    def evaluate(self):
        return IN(self.min, self.max, self.strict_min, self.strict_max)

class Slice(Evaluable, namedtuple('Slice', ('start', 'stop', 'step'))):

    def evaluate(self):
        return slice(self.start, self.stop, self.step)

class Vector(Evaluable, namedtuple('Vector', ('elements',))):

    def evaluate(self):
        return tuple(self.elements)

class IndexVector(Evaluable, namedtuple('IndexVector', ('elements',))):

    def evaluate(self):
        return tuple(self.elements)

class Indexed(Evaluable, namedtuple('Indexed', ('master', 'index'))):

    def evaluate(self):
        return self.master.__getitem__(self.index)

class Saturated(Evaluable, namedtuple('Saturated', ('value',))):

    def evaluate(self):
        return sat01(self.value)

######################################
######################################
#
# Operators (these apply precedences).
#
######################################
######################################

#########################
#
# Binary logic operations
#
#########################

class XorExpression(Evaluable, namedtuple('XorExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() ^ self.right.evaluate()

class OrExpression(Evaluable, namedtuple('OrExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() | self.right.evaluate()

class AndExpression(Evaluable, namedtuple('AndExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() & self.right.evaluate()

#########
#
# Comparisons (same precedence) and membership.
#
#########

class LtExpression(Evaluable, namedtuple('LtExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() < self.right.evaluate()

class LeExpression(Evaluable, namedtuple('LeExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() <= self.right.evaluate()

class GtExpression(Evaluable, namedtuple('GtExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() > self.right.evaluate()

class GeExpression(Evaluable, namedtuple('GeExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() >= self.right.evaluate()

class EqExpression(Evaluable, namedtuple('EqExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() == self.right.evaluate()

class NeExpression(Evaluable, namedtuple('NeExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() != self.right.evaluate()

class InExpression(Evaluable, namedtuple('InExpression', _binary)):

    def evaluate(self):
        return self.right.evaluate().contains(self.left.evaluate())

#########
#
# Math operations.
#
#########

# Add and Sub have same precedence

class AddExpression(Evaluable, namedtuple('AddExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()

class SubExpression(Evaluable, namedtuple('SubExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()

# Mul, Div, and Mod have same precedence

class MulExpression(Evaluable, namedtuple('MulExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()

class DivExpression(Evaluable, namedtuple('DivExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()

class ModExpression(Evaluable, namedtuple('ModExpression', _binary)):

    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()

##################################################################
#
# Unary operators (With same precedence as relevant `data types`).
#
##################################################################

# -X
class NegatedExpression(Evaluable, namedtuple('NegatedExpression', _unary)):

    def evaluate(self):
        return -self.expression.evaluate()

# ~X
class InvertedExpression(Evaluable, namedtuple('InvertedExpression', _unary)):

    def evaluate(self):
        return ~self.expression.evaluate()
