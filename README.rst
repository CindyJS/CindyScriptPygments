CindyScriptPygments
===================

|PyPi version badge| |Supported Python versions|

.. |PyPi version badge| image:: https://img.shields.io/pypi/v/CindyScriptPygments.svg
   :target: https://pypi.python.org/pypi/CindyScriptPygments/
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/CindyScriptPygments.svg

Pygments_ plugin for the CindyScript_ language
used by Cinderella_ and CindyJS_.
It can be used to nicely format CindyScript as HTML or in other formats.

Installation
------------

In theory, all you need to do is install ``Pygments`` and this package here:

.. code:: sh

    pip install CindyScriptPygments

This will install the latest release of each of these packages.
If you don’t want to install the package system-wide, ``pip`` offers alternatives
like the ``--user`` flag for a per-user installation.
See ``pip install --help`` for details.
In that case, you may have to perform additional steps in order to ensure
that the ``pygmentize`` command line utility is available on the ``PATH``,
at least if the ``Pygments`` dependency isn’t already installed globally.

Usage
-----

This plugin registers a Pygments lexer for a language named ``CindyScript``,
associated with the MIME type ``text/x-cindyscript``.
You can use it from the command line like this:

.. code:: sh

    pygmentize -l cindyscript sourcecode.cs

To generate specific file formats, use commands like these:

.. code:: sh

    pygmentize -f html -O full -l cindyscript -o sourcecode.html sourcecode.cs
    pygmentize -f tex -O full -l cindyscript -o sourcecode.tex sourcecode.cs
    pygmentize -f svg -O full -l cindyscript -o sourcecode.svg sourcecode.cs

The file extension ``*.cs`` is not associated with the plugin,
since that’s already taken by C# a.k.a. ``csharp``.
Most often, CindyScript code is not contained in a file of its own,
but instead embedded into a ``*.cdy`` file for Cinderella,
or a HTML page for CindyJS.
For the latter case, you can format the whole document using

.. code:: sh

    pygmentize -l CindyJS-HTML sourcecode.html

This runs the HTML highlighter on the document,
which in turn delegates to the JavaScript and CSS highlighters.
But script blocks with the attribute ``type="text/x-cindyscript"``
are handled by the CindyScript lexer.

There exist several packages which make use of Pygments for syntax highlighting.
Notable examples include the `minted <http://ctan.org/pkg/minted>`_ package for LaTeX
or the `pygmentize-bundled <https://www.npmjs.com/package/pygmentize-bundled>`_ package for Node.js.

Compatibility
-------------

The package aims to be compatible with both Python 2.7 and Python 3.
It won’t support Python 3.0 through 3.2 out of the box, since it relies on Unicode literals
as introduced by `PEP 414`_ for Python 3.3.
The 2to3 fixer might be able to make the code work with those versions of Python.

Contrary to the current implementation of Pygments’ built-in parsers,
this package supports unicode symbols outside the basic multilingual plane
even on narrow (UTF-16) builds of Python 2.7.

.. _PEP 414: https://www.python.org/dev/peps/pep-0414/

.. _Pygments: http://pygments.org/
.. _CindyScript: http://doc.cinderella.de/tiki-index.php?page=CindyScript
.. _Cinderella: http://www.cinderella.de/
.. _CindyJS: https://github.com/CindyJS/CindyJS
