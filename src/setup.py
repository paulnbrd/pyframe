#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import pyframe

long_description = """
# PyFrame
By paulnbrd.

 A python written pygame utilities, based on classes and simplicity

# Examples
see "examples/" for examples.

# License
See https://github.com/paulnbrd/pyframe/blob/master/LICENSE for the license

"""

setup(

    name='pygame_frame',

    version=pyframe.__version__,

    packages=find_packages(),

    author="PØL1",

    description="A lib to simplify the use of pygame",

    long_description=long_description,

    install_requires=["numpy","pymunk","pygame"],

    url='https://github.com/paulnbrd/PyFrame/',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9"
    ]
)