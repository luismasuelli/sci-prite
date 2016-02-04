from ply.lex import runmain
from lang import LYFactory

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
    t_NOT = r'~'

    # math operators (relevant only since they will operate on 0..1 values)
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_BY = r'\*'
    t_QUOTIENT = r'/'

    # misc operators
    t_PAREN_START = r'\('
    t_PAREN_END = r'\)'
    t_INDEX_START = r'\['
    t_INDEX_END = r'\]'
    t_COLON = r':'  # for slices and directive details
    t_RANGE = r'\.\.'  # e.g. 0.25..0.75
    t_PLUSMIN = r'\+-'  # e.g. 0.5 +- 0.25
    t_COMMA = r','  # intended as element separator

    # tokens for sentence delimitation
    t_SEMICOLON = ';'

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    def t_error(self, t):
        raise self.Error("Illegal character '%s'" % t.value[0])

    RESERVED_WORDS = {
        # alpha directive and require directive
        # alpha (require|allow|forbid);
        # require STRING as ID;
        'alpha': 'ALPHA',
        'require': 'REQUIRE',
        'allow': 'ALLOW',
        'forbid': 'FORBID',
        'as': 'AS',
        # instructions
        # on [space] pixels having ... do ... end;
        'on': 'ON',
        'pixels': 'PIXELS',
        'having': 'HAVING',
        'do': 'DO',
        'end': 'END',
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
            raise self.Error('Invalid string literal: ' + t.value)

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

        # It is a name. No more keywords recognized.
        token.type = 'NAME'
        return token

    def _extra_tokens(self):
        return ('SPACE', 'NAME', 'BOOLEAN', 'NONE') + tuple(set(self.RESERVED_WORDS.values()))


if __name__ == '__main__':
    factory = ColorMapLexerFactory()
    lexer = factory.lexer()
    print factory.tokens
    runmain(lexer, '> < <> != >= <= == [(&|~)],;: 12.5 "a\\"b" .5 rgb hsv hsl luv true false none require as in alpha '
                   'on pixels having do end using forbid require allow')