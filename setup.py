#! /usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pbap import __version__

setup(
    name="pbap",
    description="""A package implenting the
        Phonebook Access Profile (PBAP) protocol.""",
    author="Elias Johansson",
    author_email="eliasj@student.chalmers.se",
    url="https://github.com/eliasj/pbap",
    version=__version__,
    install_requires=['lightblue'],
    license="GPL",
    packages=['pbap']
)
