#!/bin/bash


if [ ! -f pyrata/syntactic_pattern_parser.py.save ]
then
  # save
  cp pyrata/syntactic_pattern_parser.py pyrata/syntactic_pattern_parser.py.save
  cp pyrata/semantic_pattern_parser.py pyrata/semantic_pattern_parser.py.save
fi

# optimize
cat pyrata/syntactic_pattern_parser.py.save | grep -v logging > pyrata/syntactic_pattern_parser.py
cat pyrata/semantic_pattern_parser.py.save | grep -v logging > pyrata/semantic_pattern_parser.py
