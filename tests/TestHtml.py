import sys

import CindyScriptPygments as C
from pygments.token import Token as T
from .LexerBase import u, LexerBase

class TestCindyJsHtmlLexer(LexerBase):

    lexerClass = C.CindyJsHtmlLexer

    def test_JSandCS(self):
        self.lex('''
<html><body data-foo= "bar"><script type="text/javascript">
if(false)foo();
</script><script id="xy" type="text/x-cindyscript">
if(false,foo())
</script></body></html>''',
        [
            '<', 'html', '>',
            '<', 'body', ' ', 'data-foo', '=', ' ', '"bar"', '>',
            '<', (T.Name.Tag, 'script'), ' ', 'type', '=',
            (T.String, '"text/javascript"'), '>', '', '\n',
            (T.Keyword, 'if'),
            (T.Punctuation, '('),
            (T.Keyword, 'false'),
            (T.Punctuation, ')'),
            (T.Name, 'foo'),
            (T.Punctuation, '('),
            (T.Punctuation, ')'),
            (T.Punctuation, ';'),
            (T.Text, '\n'),
            '<', '/', (T.Name.Tag, 'script'), '>',
            '<', 'script', ' ', 'id', '=', '"xy"',
            ' ', (T.Name.Attribute, 'type'), '=',
            (T.String, '"text/x-cindyscript"'), '>', '\n',
            (T.Name.Function, 'if'),
            (T.Punctuation, '('),
            (T.Name.Variable, 'false'),
            (T.Punctuation, ','),
            (T.Name.Function, 'foo'),
            (T.Punctuation, '('),
            (T.Punctuation, ')'),
            (T.Punctuation, ')'),
            (T.Text, '\n'),
            '<', '/', (T.Name.Tag, 'script'), '>',
            '<', '/', 'body', '>',
            '<', '/', (T.Name.Tag, 'html'), '>',
            '\n',
        ])
