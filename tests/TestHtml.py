import sys

import CindyScriptPygments as C
from pygments.token import Token as T
from .LexerBase import u, LexerBase

class TestCindyJsHtmlLexer(LexerBase):

    lexerClass = C.CindyJsHtmlLexer

    def test_JSandCS(self):
        self.lex(u'''
<html><body data-foo= "bar"><script type="text/javascript">
if(false)foo();
</script><script id="xy" type="text/x-cindyscript">
if(false,foo())
</script></body></html>''',
        [
            u'<', u'html', u'>',
            u'<', u'body', u' ', u'data-foo', u'=', u' ', u'"bar"', u'>',
            u'<', (T.Name.Tag, u'script'), u' ', u'type', u'=',
            (T.String, u'"text/javascript"'), u'>', u'', u'\n',
            (T.Keyword, u'if'),
            (T.Punctuation, u'('),
            (T.Keyword, u'false'),
            (T.Punctuation, u')'),
            (T.Name, u'foo'),
            (T.Punctuation, u'('),
            (T.Punctuation, u')'),
            (T.Punctuation, u';'),
            (T.Text, u'\n'),
            u'<', u'/', (T.Name.Tag, u'script'), u'>',
            u'<', u'script', u' ', u'id', u'=', u'"xy"',
            u' ', (T.Name.Attribute, u'type'), u'=',
            (T.String, u'"text/x-cindyscript"'), u'>', u'\n',
            (T.Name.Function, u'if'),
            (T.Punctuation, u'('),
            (T.Name.Variable, u'false'),
            (T.Punctuation, u','),
            (T.Name.Function, u'foo'),
            (T.Punctuation, u'('),
            (T.Punctuation, u')'),
            (T.Punctuation, u')'),
            (T.Text, u'\n'),
            u'<', u'/', (T.Name.Tag, u'script'), u'>',
            u'<', u'/', u'body', u'>',
            u'<', u'/', (T.Name.Tag, u'html'), u'>',
            u'\n',
        ])
