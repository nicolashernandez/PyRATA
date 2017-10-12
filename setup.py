#!/usr/bin/env python3

# from distutils.core import setup https://stackoverflow.com/questions/9810603/adding-install-requires-to-setup-py-when-making-a-python-package
from setuptools import setup

# https://packaging.python.org/distributing/
setup(name='PyRATA',
  version='0.4.1',
  description='Python Rule-based feAture sTructure Analysis',
  author='Nicolas Hernandez',
  author_email='nicolas.hernandez@gmail.com',
  url='https://github.com/nicolashernandez/PyRATA',
  license='Apache 2.0',
  keywords='NLP rule-based text mining machine learning natural language processing',
  install_requires=['ply','sympy'],
  packages=['pyrata'],
)