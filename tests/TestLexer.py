import sys

import CindyScriptPygments as C
from pygments.token import Token as T
from .LexerBase import u, LexerBase

class TestCindyScriptLexer(LexerBase):

    lexerClass = C.CindyScriptLexer

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
