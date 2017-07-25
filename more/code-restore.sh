#!/bin/bash

if [ -f pyrata/syntactic_pattern_parser.py.save ]
then
  # save
  cp pyrata/*_pattern_parser.py /tmp

  # restore
  mv pyrata/syntactic_pattern_parser.py.save pyrata/syntactic_pattern_parser.py
  mv pyrata/semantic_pattern_parser.py.save pyrata/semantic_pattern_parser.py
fi
