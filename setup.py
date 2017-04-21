#!/usr/bin/env python

from distutils.core import setup

# https://packaging.python.org/distributing/
setup(name='PyRATA',
  version='0.3.2',
  description='Python Rule-based feAture sTructure Analysis',
  author='Nicolas Hernandez',
  author_email='nicolas.hernandez@gmail.com',
  url='https://github.com/nicolashernandez/PyRATA',
  license='MIT',
  keywords='NLP rule-based text mining',
  install_requires=['ply'],
  packages=['pyrata'],
)