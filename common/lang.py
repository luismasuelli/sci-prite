from ply.lex import lex, StringTypes
from ply.yacc import yacc


def _statetoken(s, names):
    parts = s.split('_')
    i = 0
    for i, part in enumerate(parts[1:], 1):
        if part not in names and part != 'ANY':
            break

    if i > 1:
        states = tuple(parts[1:i])
    else:
        states = ('INITIAL',)

    if 'ANY' in states:
        states = tuple(names)

    tokenname = '_'.join(parts[i:])
    return (states, tokenname)


class LYFactory(object):
    """
    Pre-creates the `tokens` attribute for the class.
    """

    class Error(Exception):
        pass

    # This one must be overridden.
    states = ()

    # This one must be overridden.
    literals = ()

    # This one must be overridden.
    t_ignore = ''

    def __init__(self, lexer_args=None, lexer_kwargs=None, parser_args=None, parser_kwargs=None):
        """
        Builds the actual lexer object.
        :return:
        """

        self._lexer_args = lexer_args or ()
        self._lexer_kwargs = lexer_kwargs or {}
        self._parser_args = parser_args or ()
        self._parser_kwargs = parser_kwargs or {}
        self._state_info = None
        self._build_lexer_data()

    @property
    def state_info(self):
        """
        Obtains the states as a dictionary.
        :return:
        """

        if self._state_info is None:
            state_info = {'INITIAL': 'inclusive'}
            if self.states:
                if not isinstance(self.states, (tuple, list, set)):
                    raise TypeError('states must be defined as a tuple, list, or set')
                else:
                    for s in self.states:
                        if not isinstance(s, tuple) or len(s) != 2:
                            raise ValueError("Invalid state specifier %s. Must be a tuple (state, 'exclusive|inclusive')",
                                             repr(s))
                        name, statetype = s
                        if not isinstance(name, StringTypes):
                            raise TypeError('State name %s must be a string', repr(name))
                        if not (statetype == 'inclusive' or statetype == 'exclusive'):
                            raise ValueError("State type for state %s must be 'inclusive' or 'exclusive'", name)
                        if name in state_info:
                            raise ValueError("State '%s' already defined", name)
                        state_info[name] = statetype
            self._state_info = state_info
        return self._state_info

    def _extra_tokens(self):
        """
        Optionally override to specify additional tokens not present
          in parsing rules
        :return:
        """

        return ()

    def _build_lexer_data(self):
        """
        Builds the lexer data. Stuff like `tokens` are built here.
        :return:
        """

        tokens = {'NEWLINE'}
        obj_dict = dir(self)
        symbols = [f for f in obj_dict if f[:2] == 't_']
        for f in symbols:
            states, token_name = _statetoken(f, self.state_info)
            if token_name not in ('error', 'ignore', 'eof'):
                tokens.add(token_name)
        self._tokens = tuple(set(tuple(tokens) + tuple(self._extra_tokens())))

    def t_error(self, token):
        """
        Error processing the token. The default behavior will be to
          ignore the token.
        :param token:
        :return:
        """

        token.lexer.skip(1)

    def t_eof(self, token):
        """
        Processes the 'eof' token. Returns a token if it can continue
          or None if the token should be respected.
        :return:
        """

        return None

    def t_NEWLINE(self, t):
        r"\n+"

        t.lexer.lineno += len(t.value)

    def p_main(self, p):
        "main :"

    def p_error(self, p):
        pass

    @property
    def tokens(self):
        """
        Returns the tokens.
        :return:
        """

        return self._tokens

    def ly(self, input=None, debug=False, tracking=False):
        """
        Creates a lexer, a parser, and starts the party.
        :return:
        """

        if len(self._parser_args) < 5 and 'start' not in self._parser_kwargs:
            self._parser_kwargs['start'] = 'main'
        lexer = lex(object=self, *self._lexer_args, **self._lexer_kwargs)
        parser = yacc(module=self, *self._parser_args, **self._parser_kwargs)
        lexer.parser = parser
        if input is None:
            def _lex_iterate(inp):
                lexer.input(inp)
                return (t for t in lexer)
            return lambda inp: parser.parse(inp, lexer, debug, tracking), _lex_iterate
        else:
            return parser.parse(input, lexer, debug, tracking)
