from numpy import array
from common.lang import LYFactory
from .ast import expressions

class ColorMapLexerFactory(LYFactory):

    # comparison operators
    t_GT = r'\>'
    t_GE = r'\>='
    t_LT = r'\<'
    t_LE = r'\<='
    t_EQ = r'=='
    t_NE = r'(!=)|(\<\>)'

    # logic (only bitwise are relevant) operators
    t_AND = r'&'
    t_OR = r'\|'
    t_XOR = r'\^'
    t_NOT = r'~'

    # math operators (relevant only since they will operate on 0..1 values)
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_BY = r'\*'
    t_QUOTIENT = r'/'
    t_MODULO = r'%'

    # misc operators
    t_PAREN_START = r'\('
    t_PAREN_END = r'\)'
    t_SBRACE_START = r'\['
    t_SBRACE_END = r'\]'
    t_RANGE = r'\.\.'  # e.g. 0.25 .. 0.75
    t_PLUSMIN = r'\+-'  # e.g. 0.5 +- 0.25

    # tokens for sentence delimitation
    t_COLON = r':'  # for slices and directive details
    t_SEMICOLON = r';'  # intended as instruction separator
    t_COMMA = r','  # intended as element separator
    t_DOT = '.'  # intended as reference path separator

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Assignment operators:
    t_ASSIGN = r'='  # only for variables
    t_MUL_ASSIGN = r'\*='  # only for actions
    t_DIV_ASSIGN = r'/='  # only for actions
    t_ADD_ASSIGN = r'\+='  # only for actions
    t_SUB_ASSIGN = r'-='  # only for actions

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    RESERVED_WORDS = {
        # alpha directive and require directive
        # alpha (require|allow|forbid);
        # require STRING as ID;
        'alpha': 'ALPHA',
        'require': 'REQUIRE',
        'allow': 'ALLOW',
        'forbid': 'FORBID',
        'as': 'AS',
        # block delimiters
        'do': 'DO',
        'end': 'END',
        # instructions
        # on [space] pixels having ... do ... end;
        'on': 'ON',
        'pixels': 'PIXELS',
        'having': 'HAVING',
        # [using (space):]
        'using': 'USING',
        # intervals
        'in': 'IN',
    }

    SPACES = {
        'rgb',
        'hsv',
        'xyz',
        'lab',
        'luv',
        'hed',
    }

    CONSTANT_VALUES = {
        # boolean
        'true': ('BOOLEAN', True),
        'false': ('BOOLEAN', False),
        'none': ('NONE', None)
    }

    def t_NUMBER(self, t):
        r'(\d+(\.(\d+)?)?)|(\.\d+)'
        t.value = float(t.value)
        return t

    def t_STRING(self, t):
        r'\x27([\x20-\xff]|\\\x27)*\x27$|\x22([\x20-\xff]|\\\x22)*\x22'
        try:
            t.value = eval(t.value)
            return t
        except SyntaxError:
            print "Illegal string: %s" % t.value[0]

    def t_NAME(self, token):
        r'[a-zA-Z_][a-zA-Z0-9_]*'

        value = token.value.lower()  # And yes! my languages is Case Insensitive.

        # Is a reserved word?
        reserved_word = self.RESERVED_WORDS.get(value)
        if reserved_word:
            token.type = reserved_word
            return token

        # Is a space?
        if value in self.SPACES:
            token.type = 'SPACE'
            return token

        # Is a keyword constant value?
        constant = self.CONSTANT_VALUES.get(value)
        if constant:
            token.type = constant[0]
            token.value = constant[1]
            return token

        # No more keywords recognized. Discard the token.
        print "Illegal constant or keyword: %s" % token.value[0]

    def t_NUMVAR(self, t):
        r"\$[a-zA-Z_][a-zA-Z0-9_]*"
        t.value = t.value[1:]
        return t

    def t_VECVAR(self, t):
        r"\$\$[a-zA-Z_][a-zA-Z0-9_]*"
        t.value = t.value[2:]
        return t

    def _extra_tokens(self):
        return ('SPACE', 'BOOLEAN', 'NONE') + tuple(set(self.RESERVED_WORDS.values()))

    #############################################
    #
    # Parsing rules start here.
    #
    #############################################

    def p_empty(self, p):
        """
        empty :
        """

        p[0] = None

    def p_numeric_inversion(self, p):
        """
        numeric_inversion : MINUS numeric_expression
        """

        p[0] = expressions.Inversion(p[2])

    def p_numeric_factor(self, p):
        """
        numeric_factor : PAREN_START numeric_expression PAREN_END
        """

        p[0] = p[2]

    def p_numeric_division(self, p):
        """
        numeric_division : numeric_term QUOTIENT numeric_factor
        """

        p[0] = expressions.Division(p[1], p[2])

    def p_numeric_multiplication(self, p):
        """
        numeric_multiplication : numeric_term BY numeric_factor
        """

        p[0] = expressions.Multiplication(p[1], p[2])

    def p_numeric_term(self, p):
        """
        numeric_term : numeric_multiplication | numeric_division | numeric_factor
        """

        p[0] = p[1]

    def p_numeric_addition(self, p):
        """
        numeric_addition : numeric_expression MINUS numeric_term
        """

        p[0] = expressions.Subtraction(p[1], p[2])

    def p_numeric_subtraction(self, p):
        """
        numeric_addition : numeric_expression PLUS numeric_term
        """

        p[0] = expressions.Addition(p[1], p[2])

    def p_numeric_expression(self,  p):
        """
        numeric_expression : numeric_addition | numeric_subtraction | numeric_term
                           | NUMBER | NUMVAR | numeric_inversion
        """

        p[0] = p[1]

    def p_vector_term(self, p):
        """
        vector_term : vector_expression
        """

        p[0] = p[1]

    def p_vector_subtraction(self, p):
        """
        vector_addition : vector_expression MINUS vector_term
        """

        if p[1].shape != p[2].shape:
            raise SyntaxError("vectors being subtracted must have the same shape")
        p[0] = expressions.Subtraction(p[1], p[2])

    def p_vector_addition(self, p):
        """
        vector_addition : vector_expression PLUS vector_term
        """

        if p[1].shape != p[2].shape:
            raise SyntaxError("vectors being added must have the same shape")
        p[0] = expressions.Addition(p[1], p[2])

    def p_vector_division(self, p):
        """
        vector_division : vector_expression QUOTIENT numeric_expression
        """

        p[0] = expressions.Division(p[1], p[3])

    def p_vector_multiplication(self, p):
        """
        vector_multiplication : vector_expression BY numeric_expression
                              | numeric_expression BY vector_expression
        """

        p[0] = expressions.Multiplication(p[1], p[3])

    def p_vector_expression(self, p):
        """
        vector_expression : literal_vector | VECVAR
                          | vector_addition | vector_subtraction
                          | vector_multiplication | vector_division
        """

        p[0] = p[1]

    def p_indexed_vector(self, p):
        """
        indexed_vector : vector_expression SBRACE_START numeric_expression SBRACE_END
        """

        p[0] = expressions.VectorIndexation(p[1], p[3])

    def p_numeric_expression_cslist(self, p):
        """
        numeric_expression_cslist : numeric_expression COMMA numeric_expression_cslist
                                  | empty
        """

        if len(p) == 1:
            p[0] = ()
        else:
            p[0] = (p[1],) + p[3]

    def p_literal_vector(self, p):
        """
        literal_vector : SBRACE_START p_numeric_expression_cslist SBRACE_END
        """

        p[0] = array(p[1])

    def p_numeric_var_instruction(self, p):
        """
        numeric_var_instruction : NUMVAR ASSIGN numeric_expression SEMICOLON
        """

        p[0] = expressions.NumberAssignment(p[1], p[3])

    def p_vector_var_instruction(self, p):
        """
        vector_var_instruction : VECVAR ASSIGN vector_expression SEMICOLON
        """

        p[0] = expressions.VectorAssignment(p[1], p[3])

    def p_var_instruction(self, p):
        """
        var_instruction : vector_var_instruction
                        | numeric_var_instruction
        """

        p[0] = p[1]

    def p_var_instructions(self, p):
        """
        var_instructions : var_instruction var_instructions
                         | empty
        """

        if len(p) == 1:
            p[0] = ()
        else:
            p[0] = (p[1],) + p[2]