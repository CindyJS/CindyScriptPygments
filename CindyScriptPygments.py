# -*- coding: utf-8 -*-

import re
import sys
from pygments.lexer import RegexLexer
from pygments.token import Token

if sys.version_info[0] >= 3:
    u = str
else:
    u = unicode

reLetters = u("A-Za-z") # TODO: use Unicode as CindyScript parser does
reName = u(r"(?:#(?:[ \t]*[1-9])?|['L](?:[ \t]*[0-9'L])*)").replace(u("L"), reLetters)
reNumber = u(r"(?:[0-9](?: [0-9])*(?: \\.(?! \\.)(?: [0-9])*)?|\\.(?: [0-9])+)" +
             r"(?: [Ee](?: [+-])?(?: [0-9])+)?").replace(u(" "), u("[ \t]"))

# These must be sorted by decreasing string length, for longest match first
operators = [
    u"~!=",
    u"~<=",
    u"~>=",
    u":=_",
    u"::=",
    u"!=",
    u"++",
    u"--",
    u"->",
    u"..",
    u":=",
    u":>",
    u"<:",
    u"<=",
    u"<>",
    u"==",
    u">=",
    u"~<",
    u"~=",
    u"~>",
    u"~~",
    u"!",
    u"%",
    u"&",
    u"*",
    u"+",
    u"-",
    u".",
    u"/",
    u":",
    u";",
    u"<",
    u"=",
    u">",
    u"^",
    u"_",
    u"|",
    u"\u00ac", # ¬
    u"\u00b0", # °
    u"\u00b7", # ·
    u"\u00d7", # ×
    u"\u00f7", # ÷
    u"\u2062", # invisible times
    u"\u2192", # →
    u"\u2208", # ∈
    u"\u2209", # ∉
    u"\u2212", # −
    u"\u2215", # ∕
    u"\u2216", # ∖
    u"\u221a", # √
    u"\u2227", # ∧
    u"\u2228", # ∨
    u"\u2229", # ∩
    u"\u222a", # ∪
    u"\u2236", # ∶
    u"\u2248", # ≈
    u"\u2249", # ≉
    u"\u225f", # ≟
    u"\u2260", # ≠
    u"\u2264", # ≤
    u"\u2265", # ≥
    u"\u2266", # ≦
    u"\u2267", # ≧
    u"\u22c5", # ⋅
    u"\u2a85", # ⪅
    u"\u2a86", # ⪆
    u"\u2a89", # ⪉
    u"\u2a8a", # ⪊
]

reOps = u"|".join(map(re.escape, operators))

class CindyScriptLexer(RegexLexer):
    name = "CindyScript"
    aliases = ["cindyscript"]
    filenames = [] # since .cs is already taken by C#
    mimetypes = ["text/x-cindyscript"]
    tokens = {
        'root': [
            (u'[ \t\n]+', Token.Text.Whitespace),
            (u'//.*', Token.Comment.Single),
            (u'/\\*', Token.Comment.Multiline, 'mlc'),
            (reNumber, Token.Number),
            (reOps, Token.Operator),
            (u(r'\,|\[|\]|\(|\)|\{|\}'), Token.Punctuation),
            (u'(?:[₊₋][ \t]*)?[₀₁₂₃₄₅₆₇₈₉](?:[ \t]*[₀₁₂₃₄₅₆₇₈₉])*', Token.Number),
            (u'(?:[⁺⁻][ \t]*)?[⁰¹²³⁴⁵⁶⁷⁸⁹](?:[ \t]*[⁰¹²³⁴⁵⁶⁷⁸⁹])*', Token.Number),
            (reName + u'(?=\s*\()', Token.Name.Function),
            (reName, Token.Name.Variable),
            (u'"[^"]*"', Token.String.Double),
        ],
        'mlc': [
            (u'/\\*', Token.Comment.Multiline, '#push'),
            (u'\\*/', Token.Comment.Multiline, '#pop'),
            (u'(?:[^*/]|\\*(?!/)|/(?!\\*))+', Token.Comment.Multiline),
        ],
    }
