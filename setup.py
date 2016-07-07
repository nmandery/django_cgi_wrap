#!/usr/bin/env python
# encoding: utf8

import codecs
import os
import re
import sys

from setuptools import setup

def read(*names, **kwargs):
    return codecs.open(os.path.join(*names), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='django_cgi_wrap',
    version=find_version("django_cgi_wrap.py"),
    author="Nico Mandery",
    author_email="nico@nmandery.net",
    url="https://github.com/nmandery/django_cgi_wrap",
    py_modules=["django_cgi_wrap"],
    description="Wrapper to integrate CGI scripts into django views.",
    long_description=read("README.rst"),
    license="MIT",
    install_requires=["Django>=1.8"],
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
