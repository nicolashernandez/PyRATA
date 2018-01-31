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

"""RE API to operate the data with a pattern"""

import logging
# logging.info() Report events that occur during normal operation of a program (e.g. for status monitoring or fault investigation)
# logging.debug() for very detailed output for diagnostic purposes
# logging.warning() Issue a warning regarding a particular runtime event

import re

from pyrata.lexer import *
import pyrata.match
from pyrata.compiled_pattern import *
import copy

#from graph_tool.all import *
   

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def compile (pattern, **kwargs):    # lexicons = {}, 
  """ 
  Compile a regular expression pattern into a regular expression object, 
  which can be used for matching using match(), search()... methods, described below.
  """

  logging.info("re - compile")

  # build nfa  
  compiled_nfa = CompiledPattern()

  compiled_nfa.compile(pattern, **kwargs)



  return compiled_nfa





# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def search (pattern, data, lexicons = {},  **kwargs):
  """ Scan through data looking for the first location where the regular expression pattern produces a match, 
      and return a corresponding match object. 
      Return None if no position in the data matches the pattern.
      The optional parameter lexicon FIXME
      The optional parameter pos gives an index in the data where the search is to start; it defaults to 0.
      The optional parameter endpos limits how far the data will be searched; 
      it will be as if the data is endpos characters long, so only the elements from pos to endpos - 1 will be searched for a match. 
      If endpos is less than pos, no match will be found;  
      """

  # build nfa
  compiled_nfa = compile(pattern, lexicons = lexicons, **kwargs) # lexicons = {}
          
  #
  try:
    r = None
    r = compiled_nfa.search(data, **kwargs)  # greedy = True

  #except pyrata.CompiledPattern.CompiledPattern.InvalidRegexPattern as e:
  except CompiledPattern.InvalidRegexPattern as e:
    sys.exit('Error: re - search - %s' % e)
  return r


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def match (pattern, data, lexicons = {},  **kwargs):
  """ If zero or more tokens at the beginning of data match this regular expression, return a corresponding match object. 
      Return None if the data does not match the pattern.
      Zero-length match returns None.
      """

  # build nfa
  compiled_nfa = compile(pattern, lexicons = lexicons, **kwargs) # lexicons = {}
        
  #
  try:
    r = None
    r = compiled_nfa.match(data, **kwargs)  # greedy = True

  #except pyrata.nfa.CompiledPattern.InvalidRegexPattern as e:
  except CompiledPattern.InvalidRegexPattern as e:
    sys.exit('Error: re - match - %s' % e)
  return r

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def fullmatch (pattern, data, lexicons = {},  **kwargs):
  """ If the whole data matches the regular expression pattern, return a corresponding match object. 
      Return None if the data does not match the pattern.
      Zero-length match returns None. """
  # build nfa
  compiled_nfa = compile(pattern, lexicons = lexicons, **kwargs) # lexicons = {}
        
  #
  try:
    r = None
    r = compiled_nfa.fullmatch(data, **kwargs)  # greedy = True

  #except pyrata.nfa.CompiledPattern.InvalidRegexPattern as e:
  except CompiledPattern.InvalidRegexPattern as e:
    sys.exit('Error: re - fullmatch - %s' % e)
  return r


  
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def findall (pattern, data, lexicons = {},  **kwargs):
  """ Return all non-overlapping matches of pattern in data, as a list of datas. 
      The data is scanned left-to-right, and matches are returned in the order found. 
      If one or more groups are present in the pattern, return a list of groups; 
      this will be a list of tuples if the pattern has more than one group. 
      Zero-length match returns None. 
  """

  # build nfa
  compiled_nfa = compile(pattern, lexicons = lexicons, **kwargs) # 

  #
  try:
    r = None
    r = compiled_nfa.findall(data, **kwargs)          # greedy = True
  except CompiledPattern.InvalidRegexPattern as e:
    sys.exit('Error: re - findall - %s' % e)
  return r

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def finditer (pattern, data, lexicons = {},  **kwargs):
  """ Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in data. 
      The data is scanned left-to-right, and matches are returned in the order found. 
      Zero-length match returns None.
  """

  # build nfa
  compiled_nfa = compile(pattern, lexicons = lexicons, **kwargs) # lexicons = {}

  #
  try:
    r = None
    r = compiled_nfa.finditer(data,  **kwargs) # greedy = True
  except CompiledPattern.InvalidRegexPattern as e:
    sys.exit('Error: re - finditer - %s' % e)
  return r


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def annotate (pattern, annotation, data, group = [0], action = 'sub', iob = False, lexicons = {},  **kwargs):  
  """ 
  Do one of the following process on a copy of the data
  * sub/substitutes a match or a group of a match with a dict or a sequence of dicts (in case of dict we turn it into list of dict to process it the same way)
  * updates (and extends) the features of a match or a group of a match with the features of a dict or a sequence of dicts (of the same size as the group/match
  * extends (i.e. if a feature exists then do not update) the features of a match or a group of a match with the features of a dict or a sequence of dicts (of the same size as the group/match
  * updates|extends the features of a match or a group of a match with IOB values of the features of a dict or a sequence of dicts (of the same size as the group/match or kwargs ?
  Return the data obtained.  If the pattern isn't found, data is returned unchanged.
  """

  # lexicons are passed by parameters via kwargs
  compiledPattern = compile(pattern, lexicons = lexicons, **kwargs) # lexicons = {}

  #             
  return compiledPattern.annotate(annotation, data, group, action, iob, **kwargs) # greedy = True


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def sub (pattern, repl, data, group = [0], lexicons = {},  **kwargs):
  """
  Return the data obtained by replacing the leftmost non-overlapping occurrences of 
  pattern matches or group of matches in data by the replacement repl. 
  """
  return annotate (pattern, repl, data, group, action = 'sub', iob = False, lexicons = lexicons, **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def subn (pattern, repl, data,  **kwargs):
  """
  Perform the same operation as sub(), but return a tuple (new_string, number_of_subs_made).
  """
  raise Exception ("Not implemented yet !")

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def update (pattern, repl, data, group = [0], iob = False, lexicons = {},  **kwargs):
  """
  Return the data after updating (and extending) the features of a match or a group of a match 
  with the features of a dict or a sequence of dicts (of the same size as the group/match). 
  """
  return annotate (pattern, repl, data, group = group, action = 'update', iob = iob, lexicons = lexicons, **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def extend (pattern, repl, data, group = [0], iob = False, lexicons = {},  **kwargs):
  """
  Return the data after updating (and extending) the features of a match or a group of a match 
  with the features of a dict or a sequence of dicts (of the same size as the group/match). 
  """
  return annotate (pattern, repl, data, group = group, action = 'extend', iob = iob, lexicons = lexicons, **kwargs)

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  # TODO
  pattern = 'pos="JJ" pos="NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     

  pyrata.re.search(pattern,data)    