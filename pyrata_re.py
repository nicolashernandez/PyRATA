#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PyRATA
#
# Authors: 
#         Nicolas Hernandez <nicolas.hernandez@gmail.com>
# URL: 
#         https://github.com/nicolashernandez/PyRATA/
#
#
# Copyright 2017 Nicolas Hernandez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 
#
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""PyRATA Command Line Demo ()

usage: 

\033[1m$ ./pyrata_re.py -h\033[0m

    informs about all the available parameters

+--------+
| Syntax |
+--------+
'.' matches any single element
'*' matches zero or more of the preceding element
'+' matches one or more of the preceding element
'?' matches zero or 1 of the preceding element
'|' matches the preceding element or following element
'()' groups a sequence of elements into one element
'^' matches the beginning of the data
'$' matches the end of the data
'[]' defines a class of elements with logical connectors '()', '&', '|' and '!' 
'NAME=\042VALUE\042' the element has a feature NAME with the value VALUE
'NAME~\042VALUE\042' the element has a feature NAME whose value matches the regex defined in VALUE
'NAME@\042VALUE\042' the element has a feature NAME whose value belongs in the lexicon named VALUE
'NAME-\042VALUE\042' the element has a feature NAME whose value corresponds to a BIO chunk with VALUE as tag 

"""

import sys

import pyrata.nfa

import ply.yacc as yacc
from pyrata.lexer import *
from pyrata.syntactic_step_parser import *

import ast

import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags


if pyrata.nfa.DEBUG:
    from graph_tool.all import *

import argparse



def main(argv):
    """Entry point
    """

    compiled_nfa = pyrata.nfa.CompiledPattern()
    p = pattern
    s = data
    result = None
    
        # p =  pyrata.nfa_utils.pattern_to_guiguan_nfa_pattern_input(p)

    if NLP: 
      s = [{'raw':word, 'pos':pos, 'stem':nltk.stem.SnowballStemmer('english').stem(word), 'lem':nltk.WordNetLemmatizer().lemmatize(word.lower()), 'sw':(word in nltk.corpus.stopwords.words('english')), 'chunk':chunk} for (word, pos, chunk) in tree2conlltags(ne_chunk(pos_tag(word_tokenize(s))))]
    else:
      s = ast.literal_eval(s) # interprete as a list a list formulated as a string

    nfa = compiled_nfa.compile(p)

    if DEBUG:  
      if not STEP:
        if pdf_file_name:
          nfa.draw(filename = pdf_file_name)
        else:
          nfa.draw()

    try:
            #r = sol.exact_match(p, s)
            
            #r = sol.search(p, s)
            #print('Debug: {}'.format(r.group()))
      if method == 'findall':
        result = compiled_nfa.findall(s, mode = mode)
      elif method == 'finditer':
        result = compiled_nfa.finditer(s, mode = mode)
      elif method == 'extend':
        a = ast.literal_eval(annotation)
        result = compiled_nfa.extend(a,  s, group = [group], iob = iob, mode = mode)  
      else:
        result = compiled_nfa.search(s, mode = mode)
    

    except pyrata.nfa.CompiledPattern.InvalidRegexPattern as e:
            sys.exit('Error: %s' % e)


    print("Pattern:   {}".format(pattern))
    print("Data:      {}".format(data))
    print("Method:    {}".format(method))
    print("Mode:      {}".format(mode))
    print("Group:     {}".format(group))
    print("Annotation:{}".format(annotation))
    print("IOB:       {}".format(iob))
    print("Draw:      {}".format(DEBUG))
    print("pdffile:   {}".format(pdf_file_name))
    print("logger.disabled:   {}".format(logger.disabled))
    print("Result:    {}".format(result))    


if __name__ == '__main__':


  DEBUG = False
  STEP = False
  NLP = False
  
  if len(sys.argv) < 2:
        print('%s: invalid arguments' % sys.argv[0])
        print(__doc__)
        exit()


  # -------------------------------------------------------------------
  parser = argparse.ArgumentParser()
  parser.add_argument("pattern",  help="a pattern")
  parser.add_argument("data",  help="a data (default formulated as a list of dict or user --nlp)")
  parser.add_argument("--draw", help="draw the internal NFA to a pdf file (default is NFA.pdf)", action="store_true")
  parser.add_argument("--pdf_file_name", help="output pdf filename for the draw (--draw must be set) ",  nargs=1)

  parser.add_argument("--step", help="draw the internal NFA at every step to NFA.pdf", action="store_true")
  parser.add_argument("--nlp", help="perform nlp on the sentence (default is to interprete the string as a list of dict)", action="store_true")
  parser.add_argument("--method", help="set the method to perform among search, findall, finditer, extend (default is 'search')", nargs=1, default=['search'])
  parser.add_argument("--annotation", help="extend method requires to specify the annotation extension", nargs=1, default=[])
  parser.add_argument("--group", help="extend method allow to specify the group you want to extend", nargs=1, default=[0])
  parser.add_argument("--iob", help="extend method allow to specify if the annotation to extend will be iob", action="store_true", default = False)
  parser.add_argument("--mode", help="define the pattern matching policy (greedy or reluctant). Default is greedy, ",  nargs=1, default = ['greedy'])
  parser.add_argument("--log", help="log and export into the pyrata_re_py.log file ", action="store_true")

  # method_group = parser.add_mutually_exclusive_group(required=True)
  # method_group.add_argument('-a', nargs=2)
  # method_group.add_argument('-b', nargs=3)
  # method_group.add_argument('-c', nargs=1)


  args = parser.parse_args()

  # ---------------------------------------------------------------------
  logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='pyrata_re_py.log', level=logging.DEBUG)
  # logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='pyrata_re_py.log', level=logging.INFO)
  logger = logging.getLogger()
  logger.disabled = False
  
  # ---------------------------------------------------------------------
  logger.disabled = True
  if args.log:
    logger.disabled = False

  pattern = args.pattern
  data = args.data
  method = args.method[0]
  if len(args.annotation) >0:
    annotation = args.annotation[0]
  else:
    annotation = {}
  group = args.group[0]
  iob = args.iob
  mode = args.mode[0]
  pdf_file_name = None
  if args.pdf_file_name:
    pdf_file_name = args.pdf_file_name[0]


  if args.draw:
    DEBUG = True
  if args.step:
      STEP = True
  if args.nlp:
      NLP = True
  pyrata.nfa.DEBUG = DEBUG
  pyrata.nfa.STEP = STEP
    
  # ---------------------------------------------------------------------

  main(sys.argv)
