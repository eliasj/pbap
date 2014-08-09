#! /usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pbap import __version__, __author__, __email__, __url__

setup(
    name="pbap",
    description="""A package implenting the
        Phonebook Access Profile (PBAP) protocol.""",
    author=__author__,
    author_email=__email__,
    url=__url__,
    version=__version__,
    install_requires=['lightblue'],
    license="GPL",
    packages=['pbap']
)
