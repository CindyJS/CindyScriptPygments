# CindyScriptPygments

[![PyPi version badge](https://img.shields.io/pypi/v/CindyScriptPygments.svg)](https://pypi.python.org/pypi/CindyScriptPygments/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/CindyScriptPygments.svg)

[Pygments][Pygments] plugin for the [CindyScript][CindyScript] language
used by [Cinderella][Cinderella] and [CindyJS][CindyJS].
It can be used to nicely format CindyScript as HTML or in other formats.

## Installation

In theory, all you need to do is install `Pygments` and this package here:

```sh
pip install Pygments
pip install CindyScriptPygments
```

This will install the latest release of each of these packages.
(Some future version of the package will likely mention `Pygments` as a dependency.)
If you don’t want to install the package system-wide, `pip` offers alternatives
like the `--user` flag for a per-user installation.
See `pip install --help` for details.
In that case, you may have to perform additional steps in order to ensure
that the `pygmentize` command line utility is available on the `PATH`.

## Usage

This plugin registers a Pygments lexer for a language named `CindyScript`,
associated with the MIME type `text/x-cindyscript`.
You can use it from the command line like this:

```sh
pygmentize -l cindyscript sourcecode.cs
```

The file extension `*.cs` is not associated with the plugin,
since that’s already taken by C# a.k.a. `csharp`.

To generate specific file formats, use commands like these:

```sh
pygmentize -f html -O full -l cindyscript -o sourcecode.html sourcecode.cs
pygmentize -f tex -O full -l cindyscript -o sourcecode.tex sourcecode.cs
pygmentize -f svg -O full -l cindyscript -o sourcecode.svg sourcecode.cs
```

There exist several packages which make use of Pygments for syntax highlighting.
Notable examples include the [`minted`](http://ctan.org/pkg/minted) package for LaTeX
or the [`pygmentize-bundled`](https://www.npmjs.com/package/pygmentize-bundled) package for Node.js.

## Compatibility

The package aims to be compatible with both Python 2.7 and Python 3.
It won't support Python 3.0 through 3.2 out of the box, since it relies on Unicode literals
as introduced by [PEP 414](https://www.python.org/dev/peps/pep-0414/) for Python 3.3.
The 2to3 fixer might be able to make the code work with those versions of Python.

It also doesn't support Jython since it makes use of isolated surrogates
for some internal data structures, which Jython doesn't support.

Contrary to the current implementation of Pygments’ built-in parsers,
this package supports unicode symbols outside the basic multilingual plane
even on narrow (UTF-16) builds of Python 2.7.

[Pygments]: http://pygments.org/
[CindyScript]: http://doc.cinderella.de/tiki-index.php?page=CindyScript
[Cinderella]: http://www.cinderella.de/
[CindyJS]: https://github.com/CindyJS/CindyJS
