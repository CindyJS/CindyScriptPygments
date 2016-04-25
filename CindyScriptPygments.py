# -*- coding: utf-8 -*-

from pygments.lexer import RegexLexer
from pygments.token import Token

reLetters = u"A-Za-z" # TODO: use Unicode as CindyScript parser does
reName = ur"(?:#(?:[ \t]*[1-9])?|['L](?:[ \t]*[0-9'L])*)".replace(u"L", reLetters)
reNumber = (ur"(?:[0-9](?: [0-9])*(?: \\.(?! \\.)(?: [0-9])*)?|\\.(?: [0-9])+)" +
            ur"(?: [Ee](?: [+-])?(?: [0-9])+)?").replace(u" ", ur"[ \t]")
reOps = ur"\~\<\=|\~\!\=|\~\>\=|\:\=\_|\:\:\=|\<\=|\>\=|\~\=|\~\<|\~\>|\.\.|\=\=|\<\:|\+\+|\-\-|\~\~|\:\>|\:\=|\!\=|\<\>|\-\>|°|≟|\_|\^|≠|\<|\>|√|≤|≦|\*|≥|≧|\.|≈|⁢|≉|⋅|⪉|·|⪊|×|⪅|\/|⪆|∈|∉|\&|∧|\%|∨|÷|∕|∪|∶|∖|\+|∩|\-|\=|−|\!|¬|\;|\:|→|\|"

class CindyScriptLexer(RegexLexer):
    name = "CindyScript"
    aliases = ["cindyscript"]
    filenames = [] # since .cs is already taken by C#
    tokens = {
        'root': [
            (ur'[ \t\n]+', Token.Text.Whitespace),
            (ur'//.*', Token.Comment.Single),
            (ur'(?s)/\*.*?\*/', Token.Comment.Multiline), # TODO: Nested comments
            (reNumber, Token.Number),
            (reOps, Token.Operator),
            (ur'\,|\[|\]|\(|\)|\{|\}', Token.Punctuation),
            (ur'(?:[₊₋][ \t]*)?[₀₁₂₃₄₅₆₇₈₉](?:[ \t]*[₀₁₂₃₄₅₆₇₈₉])*', Token.Number),
            (ur'(?:[⁺⁻][ \t]*)?[⁰¹²³⁴⁵⁶⁷⁸⁹](?:[ \t]*[⁰¹²³⁴⁵⁶⁷⁸⁹])*', Token.Number),
            (reName + ur'(?=\s*\()', Token.Name.Function),
            (reName, Token.Name.Variable),
            (ur'"[^"]*"', Token.String.Double),
        ]
    }
