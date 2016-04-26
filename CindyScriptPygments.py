# -*- coding: utf-8 -*-

import re
import sys
from pygments.lexer import RegexLexer
from pygments.token import Token

if sys.version_info[0] >= 3:
    u = str
    uchr = chr
else:
    u = unicode
    uchr = unichr

def decompressUnicodeRanges(d, s, h):
    utf16 = len("\U00012345") > 1
    j = 0
    res = u"(?:[" if utf16 else u"["
    n = len(s)
    i = 0
    while i < n:
        c = ord(s[i])
        if (c >= 0xd800):
            if utf16:
                res += u"]|" + s[i] + u"["
                j = 0xdc00
            else:
                j = ((c - 0xd800) << 10) + 0x10000
        else:
            fst = j = d[c - 32] + j
            res += uchr(j)
            i += 1
            j += d[ord(s[i]) - 32]
            if j != fst:
                if j != fst + 1:
                    res += u"-"
                res += uchr(j)
        i += 1
    if utf16:
        res += u"]|[" + h + u"][\udc00-\udfff])"
    else:
        n = len(h)
        i = 0
        while i < n:
            c = ord(h[i])
            j = (c - 0xd800) << 10
            res += uchr(j + 0x10000)
            if i + 1 < n and h[i + 1] == u"-":
                i += 2
                c = ord(h[i])
                j = (c - 0xd800) << 10
            res += u"-" + uchr(j + 0x103ff)
            i += 1
        res += u"]"
    return res

# Regular expression matching letters (Unicode 8.0.0 category L)
# customized to match narrow (UTF-16) or wide (UTF-32) build.
# Compressed form taken from CindyJS.  See TestRegex for expansion.
unicodeLetters = decompressUnicodeRanges([
    2, 0, 106, 3, 4, 1, 6, 5, 7, 11, 17, 8, 12, 21, 9, 22, 30, 10, 15, 24, 25,
    16, 13, 42, 46, 14, 18, 19, 29, 37, 27, 28, 35, 26, 32, 36, 40, 43, 47, 53,
    20, 48, 50, 56, 33, 34, 39, 51, 52, 55, 63, 64, 65, 68, 85, 23, 31, 38, 45,
    49, 105, 59, 66, 69, 72, 88, 102, 114, 117, 128, 157, 191, 41, 44, 54, 60,
    67, 70, 71, 73, 74, 75, 76, 80, 81, 82, 83, 84, 86, 87, 89, 93, 94, 98, 99,
    107, 108, 116, 122, 130, 132, 134, 138, 160, 165, 185, 195, 196, 255, 268,
    277, 310, 332, 339, 362, 365, 390, 449, 457, 470, 512, 513, 541, 568, 582,
    619, 673, 726, 768, 820, 921, 991, 1164, 2684, 6581, 8453, 11171, 20949
], (u"T4(4I!)!'!&/ 0 \x96')2$+! !\x83$ %## !(!   ! ; u \x86.\x88 =#!+YoA& 87C"
    u"% } !5%+%) #!*! <0a,!4B1%'!&-'!1!$!33`HsG$!;!+.52'(#%#- & !$#$!*!9%  2%"
    u"H''%#- & % % %B# !H *+   - & % $$!;!5%3!,(#%#- & % $$!X%  5!:! '$  #$% "
    u"! %$%$ $)W!G(   / 2$!> &%C(   / . $$!L! %5%;(   D#!*!* 4'&*$W + !#&]F %"
    u"6&]% !#% !#!(# &   ! !#% # %1!#$ !/#L!S( @?$\x817-!*''#$!$%+ ',6!:= !&!"
    u"#7 \x90 ##& ! ##D ##B ##& ! ##9 K ##^Y2*V#'$\x9d#5 4&p((+, #2*2*2,  5OC"
    u"!'!Uy.D !&_)0J<#$,E'4Q/1Pv!|8:&K<9%)E>@7 )@\x80# #$%1gT\x8e#'#=#'#( ! !"
    u" ! 0#P & !$  &$##'',&  &d!9!*,b!'!#. !$$(! ! ! # 1##&$'!G%\xa58 8 \x84("
    u"#$%6= !&!#Q+!*/1& & & & & & & &t!\x97%E$&%'V(  z #&D${:Aj2\x99\xa6q\xa9"
    u"E\xa4UZ#\x8d$2)%-8*0#_J+#b#M#(S1   # /0O2[R'$! !6>)/A?+8<!*$ .)$ D3  (-"
    u"/$!$[ !$%#$#! !4 #1+ 6'#'#'1& & 7 .)c0\xa86/'I\xa7\x93#\\N&6$&! . , $ !"
    u" % % \x7fM\x92;R#Gh)d$ \x85=4(4,a$'#'#'# \ud800!) 4 : % 9#6@\x82\x94?$I"
    u"IX*5 ((=)<#@'(\ud801!f~N.Of\x8f1-)(\ud802!'#! E %$!#/)/10^: %)-)4nQ(%T!"
    u"5#   AZ?$?C( >?G)-):9*\ud803!`KJ9J\ud804#PriL3>@7M$!6F2#/! !C* 3V& ! # "
    u"9 .+8N(#%#- & % $$!;!6$\ud805eF-% !\x8987#=F-!k7x4\ud806\x87RB!\x95K"
    u"\ud808!\xa2\ud809e\x8a\ud80d!8\ud811!\x9c\ud81a!\x9b+0c<;F*#BH&:\ud81b"
    u"\xa0U,!l,\ud82c!%\ud82f!\"&,$++.\ud835!w m %#!#%## ) ! & S ##( & > # $ "
    u"!$& \x91#3 3 0 3 0 3 0 3 0 3 (\ud83a!\x8b\ud83b\x98# A % !#! . # ! !(!'"
    u"! ! !   % !#! ! ! ! ! % !## & # # ! . 5&  $ 5\ud869!\x9f7\x8c\ud86d!"
    u"\xa1,g\ud86e!<#\xa3\ud873!\x9e\ud87e!\x9a"
), u"\ud80c\ud840-\ud868\ud86a-\ud86c\ud86f-\ud872")

reName = (u(r"(?:#(?:[ \t]*[1-9])?|(?:'|L)(?:[ \t]*(?:[0-9']|L))*)")
          .replace(u("L"), unicodeLetters))
reNumber = u(r"(?:[0-9](?: [0-9])*(?: \.(?! \.)(?: [0-9])*)?|\.(?: [0-9])+)" +
             r"(?: [Ee](?: [+-])?(?: [0-9])+)?").replace(u(" "), u("[ \t]*"))

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
