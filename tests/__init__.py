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
        self.assertFalse(reOps.match(u""))
        self.assertTrue(reOps.match(u"+"))
        self.assertFalse(reOps.match(u"("))
        self.assertTrue(reOps.match(u"|"))
        self.assertTrue(reOps.match(u"\u2260"))
        self.assertEqual(3, reOps.match(u"~>=").end(0))


class TestCindyScriptLexer(unittest.TestCase):

    def lex(self, string, expected = None):
        lexer = C.CindyScriptLexer()
        toks = list(lexer.get_tokens(string))
        if expected is not None:
            self.assertEqual(len(expected), len(toks))
            for exp, act in zip(expected, toks):
                if act is None:
                    pass
                elif isinstance(exp, u):
                    self.assertEqual(exp, act[1])
                else:
                    self.assertEqual(exp, act)
        return toks

    def test_string(self):
        self.lex(u'some+"foo\\"+bar', [
            u'some', u'+',
            (T.String.Double, '"foo\\"'),
            u'+', u'bar', u'\n'
        ])
