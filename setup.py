#!/usr/bin/env python3

# from distutils.core import setup https://stackoverflow.com/questions/9810603/adding-install-requires-to-setup-py-when-making-a-python-package
from setuptools import setup

# https://packaging.python.org/distributing/
setup(name='PyRATA',
  version='0.3.3',
  description='Python Rule-based feAture sTructure Analysis',
  author='Nicolas Hernandez',
  author_email='nicolas.hernandez@gmail.com',
  url='https://github.com/nicolashernandez/PyRATA',
  license='MIT',
  keywords='NLP rule-based text mining',
  install_requires=['ply','sympy'],
  packages=['pyrata'],
)