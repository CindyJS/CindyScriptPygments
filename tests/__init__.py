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

    def shouldMatch(self, string, length = None):
        string = u(string)
        m = self.re.match(string)
        self.assertTrue(m, 'should match ' + repr(string))
        if length is None:
            length = len(string)
        self.assertEqual(length, m.end(0))

    def shouldNotMatch(self, string):
        string = u(string)
        m = self.re.match(string)
        self.assertFalse(m, 'should not match ' + repr(string))

    def test_reOps(self):
        self.re = re.compile(C.reOps)
        self.shouldNotMatch(u'')
        self.shouldMatch(u'+')
        self.shouldNotMatch(u'(')
        self.shouldMatch(u'|')
        self.shouldMatch(u';')
        self.shouldMatch(u'\u2260')
        self.shouldMatch(u'~>=')

    def test_reNumber(self):
        self.re = re.compile(C.reNumber)
        self.shouldMatch(u'1.2')
        self.shouldMatch(u'1..2', 1)
        self.shouldMatch(u'1  . . 2', 1)
        self.shouldMatch(u'1  . * 2', 4)
        self.shouldMatch(u'1  .   2')
        self.shouldMatch(u'. 3')
        self.shouldMatch(u'.  1  e  +  2')
        self.shouldMatch(u'3  .  e  4')


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

    def test_singleDot(self):
        self.lex(u'1.*2', [
            (T.Number, u'1.'),
            (T.Operator, u'*'),
            (T.Number, u'2'),
            u'\n'
        ])

    def test_doubleDot(self):
        self.lex(u'1..2', [
            (T.Number, u'1'),
            (T.Operator, u'..'),
            (T.Number, u'2'),
            u'\n'
        ])
