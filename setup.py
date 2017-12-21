#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with codecs.open("README", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="qcloudsms_py",
    version="0.1.1",
    description="qcloudsms python sdk",
    packages=["qcloudsms_py"],
    author="qcloudsms",
    author_email="qcloudsms@gmail.com",
    url="https://gitub.com/qcloudsms/qcloudsms_py",
    license="https://opensource.org/licenses/MIT",
    long_description=long_description,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)
