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

import logging
from os import path #, getcwd, chdir
import ply.lex as lex


#logger = logging.getLogger(__name__)

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Lexer(object):
  """
  Lexical Analysis: 
  converting a sequence of characters into a sequence of tokens
  Init and build methods.
  """


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Tokens Definitions
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  literals = ['"']

  tokens = (
    'NAME', 
    'VALUE', 
    'EQ', 'MATCH', 'IN',
    'AND', 'OR',
    'LBRACKET','RBRACKET',
    'LPAREN','RPAREN',
    'NOT',
    'OPTION',
    'ATLEASTONE',
    'ANY',
    'BEFORE_FIRST_TOKEN',
    'AFTER_LAST_TOKEN',
    'CHUNK'   
    )
# EOI end of instruction
#    ,'IS',
   # 'QUOTE',
  #  'LPAREN','RPAREN',
# Tokens 

  t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
  #t_VALUE    = r'\"[a-zA-Z_][a-zA-Z0-9_]*\"' # FIXME whatever character except un excaped QUOTE 
  #found at http://wordaligned.org/articles/string-literals-and-regular-expressions
  #TODO: This does not work with the string "bla \" bla"
  #t_STRING_LITERAL = r'"([^"\\]|\\.)*"'
  t_VALUE = r'\"([^\\\n]|(\\.))*?\"'       # accept combination but single constraint value with double quotes
  #t_VALUE = r'\"((\\\")|[^\\\n]|(\\.))*\"' # accept single constraint with backslashed double quote but not logical combination
  #t_VALUE = r'\"([^\\\n]|(\\.))*?[^\\]?\"'  # accept combination and single constraint value with double quotes only if it is the only character...

  t_EQ  = r'='
  t_MATCH  = r'\~'
  t_IN  = r'\@'
  t_CHUNK = r'-'
  #t_QUOTE  = r'"'
  t_AND  = r'&'
  t_OR  = r'\|'
  t_NOT  = r'!' # contrainte sur l'existance de l'attribute name pas sur sa valeur
  t_LBRACKET  = r'\['
  t_RBRACKET  = r'\]'
  t_LPAREN  = r'\('
  t_RPAREN  = r'\)'
  t_OPTION  = r'\?'
  t_ATLEASTONE  = r'\+'
  t_ANY  = r'\*'
  t_BEFORE_FIRST_TOKEN  = r'\^'
  t_AFTER_LAST_TOKEN  = r'\$'
  #t_COLON = r'\:'

#t_EOI  = r'\;'

  # Ignored characters
  t_ignore = " \t\\"


  def t_NUMBER(self,t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


  # Define a rule so we can track line numbers
  # http://www.dabeaz.com/ply/ply.html#ply_nn9
  def t_newline(self,t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    #t.lexer.lineno += len(t.value)

  # Compute column. 
  # http://www.dabeaz.com/ply/ply.html#ply_nn9
  #     input is the input text string
  #     token is a token instance
  def find_column(self, input, token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
      last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Constructor
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def __init__(self, **kwargs): 
    
    data = ''
    if 'data' in kwargs.keys():
      data = kwargs['data']
      kwargs.pop('data', None)
    
    re = 'search'
    if 're' in kwargs.keys():
      re = kwargs['re']
      kwargs.pop('re', None)      

    lexicons = {}
    if 'lexicons' in kwargs.keys():
      lexicons = kwargs['lexicons']
      kwargs.pop('lexicons', None)

    if not ('pattern' in kwargs.keys()):
      raise Exception('In',__file__,' pattern argument should be set in the constructor')
    pattern = kwargs['pattern'] 
    kwargs.pop('pattern', None)

    self.build(pattern, **kwargs)
    
    # the whole pattern 
    # self.lexer.lexdata    # (reserved name) 

    # map endposition to lextoken (by getting the len(.value of the element), 
    # you can then get the endposition of the previous element, useful to delimit quantified steps 
    # indeed, p.lexer.lexpos attribute is an integer that contains the current position within the input text.
    # Within token rule functions, this points to the first character after the matched text 
    # and the matched text includes the next lextToken (not only reduced to a single char).
    self.lexTokenEndDict = {} 

    self.lexTokenList = []  # list of LexToken (self.type, self.value, self.lineno, self.lexpos)

    # re method 
    # search: Scan through data looking for the first location where the regular expression pattern produces a match, and return a corresponding match object. 
    # findall: Return all non-overlapping matches of pattern in data, as a list of datas. 
    # finditer: Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in data.
    self.lexer.re = re

    self.lexer.pattern_data_start = 0      # position in the data from where the pattern is applied 

    self.lexer.pattern_cursor = 0          # cursor to follow the parsing progress in the pattern

    self.lexer.pattern_steps = []          # compiled pattern: list of (quantifier=[None, '*', '+', '?'] not=[True, False] group=[True, False], step or group)

    self.lexer.pattern_must_match_data_start = False  # ^ matches the start of data before the first token in a data.
    self.lexer.pattern_must_match_data_end = False    # $ matches the end of data ~after the last token of data.

    self.lexer.data = data                 # data explored by the pattern  

    self.lexer.data_cursor = self.lexer.pattern_data_start     # position in the data that is explored by the current pattern

    self.lexer.lexicons = lexicons     # store dict of lists, a list being used to store a lexicon 
    
    self.lexer.truth_value = False  # parsing result of a given pattern over a certain data 

    self.lexer.group_pattern_offsets_group_list = []   # list of group offsets e.g. [[start_i, end_i], [start_j, end_j], [start_k, end_k]]


    self.lexer.single_constraint_tuple_list = []    # list of single constraints tuples for a given pattern step 
                                                    # temporary structure only used inside the syntactic pattern parser for building pattern_steps
                                                    # used at the semantic evaluation stage
    
    self.lexer.single_constraint_symbol_list = []   # list of single constraints string (variable name) for a given pattern step 
                                                    # temporary structure only used inside the syntactic pattern parser for building pattern_steps
                                                    # used at the semantic evaluation stage

    self.lexer.single_constraint_variable_list = [] # list of variables eachone corresponding to a single constraint of a given pattern step 
                                                    # temporary structure only used inside the syntactic pattern parser for building pattern_steps
                                                    # used at the semantic evaluation stage

    self.lexer.symbolic_step_expression = []        # sympy symbolic expression corresponding to a pattern step ;
                                                    # temporary structure only used inside the syntactic pattern parser for building pattern_steps
                                                    # used at the semantic evaluation stage


                                                         
  def build(self, pattern, **kwargs):
    """
    Create a lexer.
    """
    self.lexer = lex.lex(module=self, errorlog=lex.NullLogger(), **kwargs) #
    self.lexer.input(pattern)
    self.storeLexTokenList()


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  more
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def t_error(self, t):

    #raise Exception('Illegal character "{t}"'.format(t=t.value[0]))
    logging.warning ('Lexer: Illegal character "{}" found at lineno "{}"" and lexpos "{}". We skip the character. It is probably due to unexpected characters which leads to a tokenization error. Search before this position. Current tokenization results in {}'.format(t.value[0], t.lexer.lineno, t.lexpos, t.lexer.lexTokenList))
    t.lexer.skip(1)
    #while True:
    #  tok = self.lexer.token()
    #  if not tok: 
    #    break      # No more input

  def storeLexTokenList(self):
    """ store the the list of the LexToken
    and a map from the end position of a lextoken to the lextoken """

    self.lexer.lexTokenEndDict = {}
    self.lexer.lexTokenList = [] # LexToken (self.type, self.value, self.lineno, self.lexpos)
    while True:
      tok = self.lexer.token()
      #print ('Debug: tok=',tok)
      if not tok: 
        break      # No more input
      #print(tok)
      self.lexer.lexTokenList.append(tok)
      self.lexer.lexTokenEndDict[tok.lexpos+len(tok.value)] = tok
    #print (lexTokenList)  
    # reinit the lexer
    #print ('Debug: self.lexer.lexdata',self.lexer.lexdata)
    self.lexer.input(self.lexer.lexdata)
  
#  def build(self, debug=False, debuglog=None, **kwargs):
    # """Create a lexer."""
    # if debug and debuglog is None:
    #   debuglog = self.logger
    #   self.lexer = ply.lex.lex(
    #     module=self,
    #     debug=debug,
    #     debuglog=debuglog,
    #     **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  example of use
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':
  pattern = 'lem="the" +pos@"positiveLexicon" pos~"NN.?" [lem="be" & !(raw="is" | raw="are")]\n'

  print ("Tokenize the given pattern:", pattern)
  myLexer = Lexer(pattern=pattern, data=[], re='search')
  while True:
    tok = myLexer.lexer.token()
    if not tok: 
      break      # No more input
    print(tok)