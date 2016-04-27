#!/usr/bin/env python
from setuptools import setup

def readme():
    with open("README.rst") as f:
        return f.read()

setup(
    name = "CindyScriptPygments",
    version = "0.2.0",
    description = "Pygments plugin for CindyScript",
    long_description = readme(),
    author = "Martin von Gagern",
    author_email = "gagern@ma.tum.de",
    url = "https://github.com/CindyJS/CindyScriptPygments",
    download_url = "https://pypi.python.org/pypi/CindyScriptPygments#downloads",
    license = "Dual license BSD 2-clause or Apache 2",
    py_modules = ["CindyScriptPygments"],
    test_suite = "tests",
    zip_safe = True,
    install_requires = [
        "Pygments",
    ],
    entry_points = {
        "pygments.lexers": [
            "CindyScript = CindyScriptPygments:CindyScriptLexer",
            "CindyJsHtml = CindyScriptPygments:CindyJsHtmlLexer",
        ]
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Text Processing :: Filters",
    ],
)
