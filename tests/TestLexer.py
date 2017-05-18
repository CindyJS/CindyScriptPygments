import sys

import CindyScriptPygments as C
from pygments.token import Token as T
from .LexerBase import u, LexerBase

class TestCindyScriptLexer(LexerBase):

    lexerClass = C.CindyScriptLexer

    def test_string(self):
        self.lex('some+"f//o/*o\\"+bar', [
            'some', '+',
            (T.String.Double, '"f//o/*o\\"'),
            '+', 'bar', '\n'
        ])

    def test_multiLineComment(self):
        self.lex('f/*(x)//y+\ng*/(z)', [
            'f',
            (T.Comment.Multiline, '/*'),
            (T.Comment.Multiline, '(x)//y+\ng'),
            (T.Comment.Multiline, '*/'),
            '(', 'z', ')', '\n'
        ])

    def test_nestedMultiLineComment(self):
        self.lex('a/*b/*c///*d*//e/**//*/ */*/***/f', [
            'a',
            (T.Comment.Multiline, '/*'),
            (T.Comment.Multiline, 'b'),
            (T.Comment.Multiline, '/*'),
            (T.Comment.Multiline, 'c//'),
            (T.Comment.Multiline, '/*'),
            (T.Comment.Multiline, 'd'),
            (T.Comment.Multiline, '*/'),
            (T.Comment.Multiline, '/e'),
            (T.Comment.Multiline, '/*'),
            (T.Comment.Multiline, '*/'),
            (T.Comment.Multiline, '/*'),
            (T.Comment.Multiline, '/ '),
            (T.Comment.Multiline, '*/'),
            (T.Comment.Multiline, '*/'),
            (T.Comment.Multiline, '**'),
            (T.Comment.Multiline, '*/'),
            'f', '\n'
        ])

    def test_singleDot(self):
        self.lex('1.*2', [
            (T.Number, '1.'),
            (T.Operator, '*'),
            (T.Number, '2'),
            '\n'
        ])

    def test_doubleDot(self):
        self.lex('1..2', [
            (T.Number, '1'),
            (T.Operator, '..'),
            (T.Number, '2'),
            '\n'
        ])
