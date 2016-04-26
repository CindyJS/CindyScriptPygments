import re
import sys
import unittest

import CindyScriptPygments as C
from pygments.token import Token as T

if sys.version_info[0] >= 3:
    u = str
else:
    u = unicode

class TestRegex(unittest.TestCase):

    def test_reOps(self):
        reOps = re.compile(C.reOps)
        self.assertFalse(reOps.match(u''))
        self.assertTrue(reOps.match(u'+'))
        self.assertFalse(reOps.match(u'('))
        self.assertTrue(reOps.match(u'|'))
        self.assertTrue(reOps.match(u'\u2260'))
        self.assertEqual(3, reOps.match(u'~>=').end(0))


class TestCindyScriptLexer(unittest.TestCase):

    def lex(self, string, expected = None):
        lexer = C.CindyScriptLexer()
        toks = list(lexer.get_tokens(string))
        if expected is not None:
            self.assertEqual(
                len(expected), len(toks),
                ('expected {0} tokens but got {1} tokens: {2} '
                 .format(len(expected), len(toks),
                         ' | '.join(v for t, v in toks))))
            for exp, act in zip(expected, toks):
                if act is None:
                    pass
                elif isinstance(exp, u):
                    self.assertEqual(exp, act[1])
                else:
                    self.assertEqual(exp, act)
        return toks

    def test_string(self):
        self.lex(u'some+"f//o/*o\\"+bar', [
            u'some', u'+',
            (T.String.Double, '"f//o/*o\\"'),
            u'+', u'bar', u'\n'
        ])

    def test_multiLineComment(self):
        self.lex(u'f/*(x)//y+\ng*/(z)', [
            u'f',
            (T.Comment.Multiline, u'/*'),
            (T.Comment.Multiline, u'(x)//y+\ng'),
            (T.Comment.Multiline, u'*/'),
            u'(', u'z', u')', u'\n'
        ])

    def test_nestedMultiLineComment(self):
        self.lex(u'a/*b/*c///*d*//e/**//*/ */*/***/f', [
            u'a',
            (T.Comment.Multiline, u'/*'),
            (T.Comment.Multiline, u'b'),
            (T.Comment.Multiline, u'/*'),
            (T.Comment.Multiline, u'c//'),
            (T.Comment.Multiline, u'/*'),
            (T.Comment.Multiline, u'd'),
            (T.Comment.Multiline, u'*/'),
            (T.Comment.Multiline, u'/e'),
            (T.Comment.Multiline, u'/*'),
            (T.Comment.Multiline, u'*/'),
            (T.Comment.Multiline, u'/*'),
            (T.Comment.Multiline, u'/ '),
            (T.Comment.Multiline, u'*/'),
            (T.Comment.Multiline, u'*/'),
            (T.Comment.Multiline, u'**'),
            (T.Comment.Multiline, u'*/'),
            u'f', u'\n'
        ])
