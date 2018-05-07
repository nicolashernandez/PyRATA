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

"""
PyRATA Command Line Demo to interface the PyRATA API and plots pretty graphs of NFAs. 
In v0.4 it is an alpha code. It is provided "as is"...
Takes at least two parameters: the pattern to search and the data to process.
By default, it performs English natural language processing (nlp) with NLTK on the input data 
and search the first occurrence of the specified pattern with a greedy pattern matching policy.
No pdf draw. No log export.

  ./pyrata_re.py -h
    informs about all the available parameters and documentation

"""

api_language_documentation = """
language syntax:
  'NAME=\042VALUE\042' the token has a feature NAME with the value VALUE
  'NAME~\042VALUE\042' the token has a feature NAME whose value matches the regex defined in VALUE
  'NAME@\042VALUE\042' the token has a feature NAME whose value belongs in the lexicon named VALUE
  'NAME-\042VALUE\042' the token has a feature NAME whose value corresponds to a BIO chunk with VALUE as tag  

  '[]' defines a class of tokens with logical connectors '()', '&', '|' and '!' 
  
  '*' matches zero or more of the preceding element
  '+' matches one or more of the preceding element
  '?' matches zero or 1 of the preceding element

  '.' matches any single token

  '()' groups a sequence of tokens into one element
  '|' matches the preceding element or following element

  '^' matches the beginning of the data
  '$' matches the end of the data

more:
  https://github.com/nicolashernandez/PyRATA/blob/master/docs/user-guide.rst

"""
# python3 pyrata_re.py 'pos="DT"? pos~"JJ|NN"* pos~"NN.?"+' "" --draw --pdf_file_name my_nfa.pdf && evince my_nfa.pdf

# python3 pyrata_re.py '(pos~"RB.?|VBG"+) (lc@"SENTIMENT" ((lc~"\," .)* lc~"and|or" .)*)' "incredibly horrible, strange and funny" --lexicons "{'SENTIMENT':['horrible', 'funny']}"

import sys

import pyrata.nfa

import ply.yacc as yacc
from pyrata.lexer import *
from pyrata.syntactic_step_parser import *

from pyrata.compiled_pattern import *


import ast

import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags

DRAW = False
DRAW_STEPS = False

#if pyrata.nfa.DRAW:
#   from graph_tool.all import *

import argparse


def main(): #argv):
    """ Perform the specified search request over the input data.
        Optionally plots a graph.
    """
    print ('Debug: data={}'.format(data))

    compiled_nfa = CompiledPattern()
    p = pattern
    s = data
    result = None
    
        # p =  pyrata.nfa_utils.pattern_to_guiguan_nfa_pattern_input(p)


    nfa = compiled_nfa.compile(p, lexicons = lexicons)

    if DRAW:  
      if pdf_file_name:
        nfa.draw(filename = pdf_file_name)
      else:
        nfa.draw()

    try:
            #r = sol.exact_match(p, s)
            
            #r = sol.search(p, s)
            #print('Debug: {}'.format(r.group()))
      if method == 'findall':
        result = compiled_nfa.findall(s, mode = mode, pos = pos, endpos = endpos)
      elif method == 'finditer':
        result = compiled_nfa.finditer(s, mode = mode, pos = pos, endpos = endpos)
      elif method == 'match':
        result = compiled_nfa.match(s, mode = mode, pos = pos, endpos = endpos)
      elif method == 'fullmatch':
        result = compiled_nfa.fullmatch(s, mode = mode, pos = pos, endpos = endpos)
      elif method == 'sub':
        a = ast.literal_eval(annotation)
        result = compiled_nfa.sub(a,  s, group = [group], iob = iob, mode = mode, pos = pos, endpos = endpos)  
      elif method == 'extend':
        a = ast.literal_eval(annotation)
        result = compiled_nfa.extend(a,  s, group = [group], iob = iob, mode = mode, pos = pos, endpos = endpos)  
      else:
        result = compiled_nfa.search(s, mode = mode, pos = pos, endpos = endpos)
    

    except pyrata.nfa.CompiledPattern.InvalidRegexPattern as e:
            sys.exit('Error: %s' % e)


    print("Pattern:   {}".format(pattern))
    print("Data:      {}".format(data))
    print("Lexicons:  {}".format(lexicons))
    print("pos:       {}".format(pos))
    print("endpos:    {}".format(endpos))
    print("Method:    {}".format(method))
    print("Mode:      {}".format(mode))
    print("Group:     {}".format(group))
    print("Annotation:{}".format(annotation))
    print("IOB:       {}".format(iob))
    print("Draw:      {}".format(DRAW))
    print("pdffile:   {}".format(pdf_file_name))
    print("logger.disabled:   {}".format(logger.disabled))
    print("Result:    {}".format(result))    


if __name__ == '__main__':
  """
    parsing the arguments
  """
  # -------------------------------------------------------------------
  # https://docs.python.org/3/library/argparse.html
  # default description
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
    description= __doc__, 
    epilog=api_language_documentation) # epilog= description
  

  # wo -- we are in presence of positional arguments
  parser.add_argument("pattern",  help="a pattern")
  parser.add_argument("data",  help="data string or path to a data file. Use --path to mean a path. By default the data is assumed to be English text and so nlp processed with NLTK. Use --pyrata_data to consider it as a list of dicts.")
  #parser.add_argument('data', help="data string or path to a data file. Use --path to mean a path. By default the data is assumed to be English text and so nlp processed with NLTK. Use --pyrata_data to consider it as a list of dicts.", nargs='?', type=argparse.FileType('r'), default=sys.stdin)

  # wi -- we are in presence of optional arguments
  parser.add_argument("--path", help="force the interpretation of the data argument as a file path", action="store_true")

  parser.add_argument("--draw", help="draw the internal NFA to a pdf file. Default is 'NFA.pdf'. Requires graph_tool.", action="store_true")
  parser.add_argument("--pdf_file_name", help="output pdf filename for the draw (--draw must be set) ",  nargs=1)
  parser.add_argument("--draw_steps", help="draw draw the internal NFA at every steps to a pdf file. Default is 'NFA.pdf'. Requires graph_tool. It is best to run this option and observe the result with a PDF viewer that can detect file change and reload the changed file.", action="store_true")

  parser.add_argument("--pyrata_data", help="interpret the string data as a list of dict", action="store_true")
  parser.add_argument("--method", help="search/edit method to perform among 'search', 'findall', 'match', 'fullmatch', 'finditer', 'sub', 'extend' (default is 'search')", nargs=1, default=['search'])
  parser.add_argument("--annotation", help="'extend' method requires to specify the annotation extension", nargs=1, default=[])
  parser.add_argument("--group", help="'extend' method allows to specify the group you want to extend", nargs=1, default=[0])
  parser.add_argument("--iob", help="'extend' method allows to specify if the annotation to extend will be iob", action="store_true", default = False)
  parser.add_argument("--mode", help="define the pattern matching policy (greedy or reluctant). Default is greedy, ",  nargs=1, default = ['greedy'])
  parser.add_argument("--log", help="log and export into the pyrata_re_py.log file ", action="store_true")
  parser.add_argument("--pos", help="index in the data where the search is to start; it defaults to 0. ", nargs=1, type=int, default=[])
  parser.add_argument("--endpos", help="endpos limits how far the data will be searched ", nargs=1, type=int, default=[])
  parser.add_argument("--lexicons", help="lexicons expressed as a dict of list, each key being a lexicon name", nargs=1, default=[])


  # method_group = parser.add_mutually_exclusive_group(required=True)
  # method_group.add_argument('-a', nargs=2)
  # method_group.add_argument('-b', nargs=3)
  # method_group.add_argument('-c', nargs=1)

  args = parser.parse_args()
  


  #  if len(sys.argv) < 2:
  #      print('%s: invalid arguments' % sys.argv[0])
  #      print(__doc__)
  #      #parser = argparse.ArgumentParser(description='A foo that bars')
  #      #parser.print_help()
  #      exit()


  # ---------------------------------------------------------------------
  logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='pyrata_re_py.log', level=logging.DEBUG)
  # logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='pyrata_re_py.log', level=logging.INFO)
  logger = logging.getLogger()

  # ---------------------------------------------------------------------
  logger.disabled = True
  if args.log:
    logger.disabled = False

  # ---------------------------------------------------------------------
  pattern = args.pattern
  data = args.data

  # ---------------------------------------------------------------------
  if args.pyrata_data:
    data = ast.literal_eval(data) # interprete as a list a list formulated as a string
  else:
    data = [{'raw':word, 'lc':word.lower(), 'pos':pos, 'stem':nltk.stem.SnowballStemmer('english').stem(word), 'lem':nltk.WordNetLemmatizer().lemmatize(word.lower()), 'sw':(word in nltk.corpus.stopwords.words('english')), 'chunk':chunk} for (word, pos, chunk) in tree2conlltags(ne_chunk(pos_tag(word_tokenize(data))))]
 
  # ---------------------------------------------------------------------
  if len(args.lexicons) >0:
    lexicons = ast.literal_eval(args.lexicons[0]) # interprete as a dict a list formulated as a string
  else:
    lexicons = []

  # ---------------------------------------------------------------------
  # interpret data as a data path
  if args.path:
    #infile=open(data)
    #lines=infile.readlines()
    #f = open(fname, encoding="utf-8")
    #text = open(data).read().decode("utf-8",'replace')
  # close the connection
    #infile.close()
    with open(data) as f: # no need to close the connection
      data = f.read()


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

  pos = 0
  endpos = len(data) 
  if len(args.pos) >0:
    pos = args.pos[0]
  if len(args.endpos) >0:
    endpos = args.endpos[0]

  if args.draw:
    DRAW = True
  if args.draw_steps:
    DRAW_STEPS = True

  # TODO
  if DRAW_STEPS:
    print ("Error: '--draw_steps' parameters not implemented yet.")
    parser.print_help()
    exit()  

  pyrata.nfa.DEBUG = DRAW
  pyrata.nfa.STEP = DRAW_STEPS


# ---------------------------------------------------------------------
"""
Loading the dependency
"""
if DRAW or DRAW_STEPS:
  from graph_tool.all import *

# ---------------------------------------------------------------------
if __name__ == '__main__':
  """
    performing the job
  """

  main() # (sys.argv) # FIXME sys ?
