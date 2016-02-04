from collections import namedtuple
from colormap.expressions import IN

_binary = ('left', 'right')
_unary = ('expression',)

class Evaluable(object):

    def evaluate(self):
        raise NotImplementedError

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

#########
#
# Unary operators
#
#########

# -X
class NegatedExpression(Evaluable, namedtuple('NegatedExpression', _unary)):

    def evaluate(self):
        return -self.expression.evaluate()

# ~X
class InvertedExpression(Evaluable, namedtuple('InvertedExpression', _unary)):

    def evaluate(self):
        return ~self.expression.evaluate()
