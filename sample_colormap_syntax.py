from colormap.lang.syntax import ColorMapLexerFactory

factory = ColorMapLexerFactory(parser_kwargs=dict(
    # start=''
))
parse_func, token_func = factory.ly()
# for t in token_func('> < <> != >= <= == [(&|~)],;: 12.5 "a\\"b" .5 rgb hsv hsl luv true false none require as '
#                     'in alpha on pixels having do end using forbid require allow $aaa $$bbb'):
#     print t
print parse_func('$lorem = 1.45;')