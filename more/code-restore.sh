#!/bin/bash

if [ -f pyrata/re.py.save ]
then
  # save
  cp pyrata/*.py /tmp

  # restore
  mv pyrata/re.py.save  pyrata/re.py    
  mv pyrata/nfa.py.save  pyrata/nfa.py 
  mv pyrata/state.py.save pyrata/state.py 
  mv pyrata/syntactic_step_parser.py.save  pyrata/syntactic_step_parser.py 
  mv pyrata/lexer.py.save pyrata/lexer.py  
  mv pyrata/match.py.save pyrata/match.py
fi
