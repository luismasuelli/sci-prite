from common.lang import LYFactory

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
    t_SATURATE_START = r'\(\|'
    t_SATURATE_END = r'\|\)'
    t_RANGE = r'\.\.'  # e.g. 0.25..0.75
    t_PLUSMIN = r'\+-'  # e.g. 0.5 +- 0.25
    t_COMMA = r','  # intended as element separator

    # tokens for sentence delimitation
    t_COLON = r':'  # for slices and directive details
    t_SEMICOLON = r';'

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
        print "Illegal constant or keyword: %s" % t.value[0]

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


if __name__ == '__main__':
    factory = ColorMapLexerFactory(parser_kwargs=dict(
        # start=''
    ))
    parse_func, token_func = factory.ly()
    for t in token_func('> < <> != >= <= == [(&|~)],;: 12.5 "a\\"b" .5 rgb hsv hsl luv true false none require as '
                        'in alpha on pixels having do end using forbid require allow $aaa $$bbb'):
        print t
