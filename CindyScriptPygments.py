# -*- coding: utf-8 -*-
# Copyright 2016  Martin von Gagern
# Dual-licensed under BSD 2-clause and Apache 2 licenses,
# see LICENSE file for details.

import re
import sys
from pygments.lexer import RegexLexer, bygroups, using
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

if sys.version_info[0] >= 3:
    u = str
    uchr = chr
else:
    u = str
    uchr = chr

def decompressUnicodeRanges(d, s, h):
    utf16 = len("\U00012345") > 1
    j = 0
    res = "(?:[" if utf16 else "["
    n = len(s)
    i = 0
    while i < n:
        c = ord(s[i])
        if (c >= 0xe800):
            if utf16:
                res += "]|" + uchr(c - 0x1000) + "["
                j = 0xdc00
            else:
                j = ((c - 0xe800) << 10) + 0x10000
        else:
            fst = j = d[c - 32] + j
            res += uchr(j)
            i += 1
            j += d[ord(s[i]) - 32]
            if j != fst:
                if j != fst + 1:
                    res += "-"
                res += uchr(j)
        i += 1
    if utf16:
        h = ''.join(c if c == '-' else uchr(ord(c) - 0x1000) for c in h)
        res += "]|[" + h + eval(r'u"][\udc00-\udfff])"')
    else:
        n = len(h)
        i = 0
        while i < n:
            c = ord(h[i])
            j = (c - 0xe800) << 10
            res += uchr(j + 0x10000)
            if i + 1 < n and h[i + 1] == "-":
                i += 2
                c = ord(h[i])
                j = (c - 0xe800) << 10
            res += "-" + uchr(j + 0x103ff)
            i += 1
        res += "]"
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
], ("T4(4I!)!'!&/ 0 \x96')2$+! !\x83$ %## !(!   ! ; u \x86.\x88 =#!+YoA& 87C"
    "% } !5%+%) #!*! <0a,!4B1%'!&-'!1!$!33`HsG$!;!+.52'(#%#- & !$#$!*!9%  2%"
    "H''%#- & % % %B# !H *+   - & % $$!;!5%3!,(#%#- & % $$!X%  5!:! '$  #$% "
    "! %$%$ $)W!G(   / 2$!> &%C(   / . $$!L! %5%;(   D#!*!* 4'&*$W + !#&]F %"
    "6&]% !#% !#!(# &   ! !#% # %1!#$ !/#L!S( @?$\x817-!*''#$!$%+ ',6!:= !&!"
    "#7 \x90 ##& ! ##D ##B ##& ! ##9 K ##^Y2*V#'$\x9d#5 4&p((+, #2*2*2,  5OC"
    "!'!Uy.D !&_)0J<#$,E'4Q/1Pv!|8:&K<9%)E>@7 )@\x80# #$%1gT\x8e#'#=#'#( ! !"
    " ! 0#P & !$  &$##'',&  &d!9!*,b!'!#. !$$(! ! ! # 1##&$'!G%\xa58 8 \x84("
    "#$%6= !&!#Q+!*/1& & & & & & & &t!\x97%E$&%'V(  z #&D${:Aj2\x99\xa6q\xa9"
    "E\xa4UZ#\x8d$2)%-8*0#_J+#b#M#(S1   # /0O2[R'$! !6>)/A?+8<!*$ .)$ D3  (-"
    "/$!$[ !$%#$#! !4 #1+ 6'#'#'1& & 7 .)c0\xa86/'I\xa7\x93#\\N&6$&! . , $ !"
    " % % \x7fM\x92;R#Gh)d$ \x85=4(4,a$'#'#'# \ue800!) 4 : % 9#6@\x82\x94?$I"
    "IX*5 ((=)<#@'(\ue801!f~N.Of\x8f1-)(\ue802!'#! E %$!#/)/10^: %)-)4nQ(%T!"
    "5#   AZ?$?C( >?G)-):9*\ue803!`KJ9J\ue804#PriL3>@7M$!6F2#/! !C* 3V& ! # "
    "9 .+8N(#%#- & % $$!;!6$\ue805eF-% !\x8987#=F-!k7x4\ue806\x87RB!\x95K"
    "\ue808!\xa2\ue809e\x8a\ue80d!8\ue811!\x9c\ue81a!\x9b+0c<;F*#BH&:\ue81b"
    "\xa0U,!l,\ue82c!%\ue82f!\"&,$++.\ue835!w m %#!#%## ) ! & S ##( & > # $ "
    "!$& \x91#3 3 0 3 0 3 0 3 0 3 (\ue83a!\x8b\ue83b\x98# A % !#! . # ! !(!'"
    "! ! !   % !#! ! ! ! ! % !## & # # ! . 5&  $ 5\ue869!\x9f7\x8c\ue86d!"
    "\xa1,g\ue86e!<#\xa3\ue873!\x9e\ue87e!\x9a"
), "\ue80c\ue840-\ue868\ue86a-\ue86c\ue86f-\ue872")

reName = (u(r"(?:#(?:[ \t]*[1-9])?|(?:'|L)(?:[ \t]*(?:[0-9']|L))*)")
          .replace(u("L"), unicodeLetters))
reNumber = u(r"(?:[0-9](?: [0-9])*(?: \.(?! \.)(?: [0-9])*)?|\.(?: [0-9])+)" +
             r"(?: [Ee](?: [+-])?(?: [0-9])+)?").replace(u(" "), u("[ \t]*"))

# These must be sorted by decreasing string length, for longest match first
operators = [
    "~!=",
    "~<=",
    "~>=",
    ":=_",
    "::=",
    "!=",
    "++",
    "--",
    "->",
    "..",
    ":=",
    ":>",
    "<:",
    "<=",
    "<>",
    "==",
    ">=",
    "~<",
    "~=",
    "~>",
    "~~",
    "!",
    "%",
    "&",
    "*",
    "+",
    "-",
    ".",
    "/",
    ":",
    ";",
    "<",
    "=",
    ">",
    "^",
    "_",
    "|",
    "\u00ac", # ¬
    "\u00b0", # °
    "\u00b7", # ·
    "\u00d7", # ×
    "\u00f7", # ÷
    "\u2062", # invisible times
    "\u2192", # →
    "\u2208", # ∈
    "\u2209", # ∉
    "\u2212", # −
    "\u2215", # ∕
    "\u2216", # ∖
    "\u221a", # √
    "\u2227", # ∧
    "\u2228", # ∨
    "\u2229", # ∩
    "\u222a", # ∪
    "\u2236", # ∶
    "\u2248", # ≈
    "\u2249", # ≉
    "\u225f", # ≟
    "\u2260", # ≠
    "\u2264", # ≤
    "\u2265", # ≥
    "\u2266", # ≦
    "\u2267", # ≧
    "\u22c5", # ⋅
    "\u2a85", # ⪅
    "\u2a86", # ⪆
    "\u2a89", # ⪉
    "\u2a8a", # ⪊
]

reOps = "|".join(map(re.escape, operators))

class CindyScriptLexer(RegexLexer):
    name = "CindyScript"
    aliases = ["cindyscript"]
    filenames = [] # since .cs is already taken by C#
    mimetypes = ["text/x-cindyscript"]
    tokens = {
        'root': [
            ('[ \t\n]+', Token.Text.Whitespace),
            ('//.*', Token.Comment.Single),
            ('/\\*', Token.Comment.Multiline, 'mlc'),
            (reNumber, Token.Number),
            (reOps, Token.Operator),
            (u(r'\,|\[|\]|\(|\)|\{|\}'), Token.Punctuation),
            ('(?:[₊₋][ \t]*)?[₀₁₂₃₄₅₆₇₈₉](?:[ \t]*[₀₁₂₃₄₅₆₇₈₉])*', Token.Number),
            ('(?:[⁺⁻][ \t]*)?[⁰¹²³⁴⁵⁶⁷⁸⁹](?:[ \t]*[⁰¹²³⁴⁵⁶⁷⁸⁹])*', Token.Number),
            (reName + '(?=\s*\()', Token.Name.Function),
            (reName, Token.Name.Variable),
            ('"[^"]*"', Token.String.Double),
        ],
        'mlc': [
            ('/\\*', Token.Comment.Multiline, '#push'),
            ('\\*/', Token.Comment.Multiline, '#pop'),
            ('(?:[^*/]|\\*(?!/)|/(?!\\*))+', Token.Comment.Multiline),
        ],
    }


HtmlLexer = type(get_lexer_by_name('html'))


class CindyJsHtmlLexer(RegexLexer):
    name = "CindyJS-HTML"
    aliases = ["cindyjs-html", "cindyjshtml", "cindyjs_html"]
    filenames = [] # since .html is already taken
    flags = re.DOTALL
    tokens = {
        'root': [
            ('(.*<\\s*script[^>]*\\s'
             'type\\s*=\\s*["\']text/x-cindyscript[^a-z][^>]*>)'
             '(.*?)'
             '(<\\s*/\\s*script\\s*>)',
             bygroups(using(HtmlLexer),
                      using(CindyScriptLexer),
                      using(HtmlLexer))
            ),
            ('.+', using(HtmlLexer))
        ]
    }
