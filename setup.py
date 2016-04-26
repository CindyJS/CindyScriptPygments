#!/usr/bin/env python
from setuptools import setup
setup(
    name = "CindyScriptPygments",
    version = "0.1.0",
    description = "Pygments plugin for CindyScript",
    author = "Martin von Gagern",
    author_email = "gagern@ma.tum.de",
    url = "https://github.com/CindyJS/CindyScriptPygments",
    py_modules = ["CindyScriptPygments"],
    test_suite = "tests",
    entry_points = {
        "pygments.lexers": [
            "CindyScript = CindyScriptPygments:CindyScriptLexer",
        ]
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
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
