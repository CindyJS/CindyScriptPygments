import sys
import unittest

if sys.version_info[0] >= 3:
    u = str
else:
    u = unicode

class LexerBase(unittest.TestCase):

    def lex(self, string, expected = None):
        lexer = self.lexerClass()
        toks = list(lexer.get_tokens(string))
        if expected is not None:
            if len(expected) != len(toks):
                print()
                print(' | '.join(v for t, v in toks))
            for exp, act in zip(expected, toks):
                if act is None:
                    pass
                elif isinstance(exp, u):
                    self.assertEqual(exp, act[1])
                else:
                    self.assertEqual(exp[1], act[1])
                    self.assertTrue(
                        act[0] in exp[0],
                        '{2} should be in {0} but is in {1}'
                        .format(exp[0], act[0], repr(act[1])))
            self.assertEqual(len(expected), len(toks))
        return toks

__all__ = [
    'u',
    'LexerBase',
]
