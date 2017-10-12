#!/bin/bash

if [ ! -f pyrata/re.py.save ]
then
  # save .py with logging instruction 
  cp pyrata/re.py pyrata/re.py.save     
  cp pyrata/nfa.py pyrata/nfa.py.save
  cp pyrata/state.py pyrata/state.py.save
  cp pyrata/syntactic_step_parser.py pyrata/syntactic_step_parser.py.save
  cp pyrata/lexer.py  pyrata/lexer.py.save  
  cp pyrata/match.py pyrata/match.py.save   
  # pyrata/nltk.py      
  #pyrata/parsetab.py  
fi

# optimize
cat pyrata/re.py.save  | grep -v logging >  pyrata/re.py    
cat pyrata/nfa.py.save  | grep -v logging > pyrata/nfa.py 
cat pyrata/state.py.save  | grep -v logging > pyrata/state.py 
cat pyrata/syntactic_step_parser.py.save  | grep -v logging > pyrata/syntactic_step_parser.py 
cat pyrata/lexer.py.save  | grep -v logging > pyrata/lexer.py  
cat pyrata/match.py.save | grep -v logging > pyrata/match.py
