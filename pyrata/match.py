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
Resulting objects of a matching process
"""

import logging
from pprint import pprint, pformat
import ply.yacc as yacc

from pyrata.lexer import *
from sympy import Symbol, symbols


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Match(object):
  """ Object which stores the positions of all the groups of a given match delimited by a global start and end."""

  _groups = []          # list of triplet (value, start, end) e.g. [[[{'pos': 'JJ', 'raw': 'fast'}], 0, 1]]
  DEFAULT_GROUP_ID = 0
  (VALUE, START, END) = (0,1,2)

  def __init__(self, **kwargs):
    self._groups = []
    value = ''
    start = -1
    end = -1

    if 'start' in kwargs.keys(): # MANDATORY
      start = kwargs['start']
    if 'end' in kwargs.keys(): # MANDATORY
      end = kwargs['end']
    if 'value' in kwargs.keys(): # MANDATORY
      value = kwargs['value']
    if 'groups' in kwargs.keys(): # MANDATORY
      self._groups = kwargs['groups']  
      #logging.debug ('groups=', self._groups)
      #print ('Debug: Match__init__:(start={}, end={}, value={})'.format(startPosition, endPosition, value))
    else:  
      self._groups.append([value, start, end])
    #if  self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] == '' or self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] == -1 or self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END] == -1:   
    #  raise Exception('pyrata.re - attempt to create a Match object with incomplete informations')
    #print ('Debug: groups=', self.groups)

    self._DFA = []    # list of ordered States 
    if 'DFA' in kwargs.keys(): # MANDATORY
      self._DFA  = kwargs['DFA']

  def __repr__(self):
    #for v, s, e in self.groups
    return ''.join(['<pyrata.re Match object; groups=',str(self._groups),'>']) #span=('+str(self.start())+', '+str(self.end())+'), match="'+str(self.group())+'">'

  def get_group_id(self, *argv):
    if len(argv) > 0:
      group_id = argv[0]
      if group_id > len(self._groups):
        raise IndexError ('In Match - group() function - wrong index required')
    else:
      group_id = Match.DEFAULT_GROUP_ID
    return group_id

  def group(self, *argv):
    ''' 
    Returns the corresponding value of one subgroup of the match. 
    Default is 0. The whole match value.
    '''
    return self._groups[self.get_group_id(*argv)][Match.VALUE]

  def groups (self):
    '''Return a tuple containing all the subgroups of the match, from 0. 
    In python re it is from 1 up to however many groups are in the pattern. '''
    return self._groups
    # if len(self.groups) > 0:
    #   return self.groups[1:len(self.groups)]   
    # else:
    #   return [] 

  def start(self, *argv):
    '''
    Return the indices of the start of the subdata matched by group; 
    group default to zero (meaning the whole matched data).
    '''
    return self._groups[self.get_group_id(*argv)][Match.START]

  def end(self, *argv):
    '''
    Return the indices of the end of the subdata matched by group; 
    group default to zero (meaning the whole matched data).
    '''
    return self._groups[self.get_group_id(*argv)][Match.END]

  def setStart(self, start, *argv):
    '''
    Set the indice of the start of the subdata matched by group; 
    group default to zero (meaning the whole matched data).
    '''
    self._groups[self.get_group_id(*argv)][Match.START] = start

  def setEnd(self, end, *argv):
    '''
    Set the indice of the end of the subdata matched by group; 
    group default to zero (meaning the whole matched data).
    '''
    self._groups[self.get_group_id(*argv)][Match.END] = end

  def DFA(self):
    ''' 
    Returns the corresponding DFA (i.e. a list of states) or [] if not set.
    '''
    return self._DFA

  def str_DFA(self):
    ''' 
    Returns the corresponding DFA as a list of string.
    '''
    str_DFA = []
    for s in self.DFA():
      #print ('Debug: state={}'.format(s))
      #str_DFA.append(str(s))
      str_DFA.append(s.char)  
    return str_DFA   


  def __eq__(self, other):
    if other == None: 
      return False
    if self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] == other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] and self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] == other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] and self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END] == other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END]:
      return True
      return True
    return False  
   
  def __ne__(self, other):
    return not (self == other)
    # if other == None: 
    #   return True   
    # if self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] != other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] or self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] != other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] or self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END] != other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END]:
    #   return True
    # return False  

  def __len__(self):
    #logging.debug  ('groups=', self.groups)
    return len(self._groups) 

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class MatchesList(object):
  """ Object which stores the Match of a given pattern."""

  current = -1
  matcheslist = []    # list of Match

  def __init__(self, **kwargs):
    self.matcheslist = []

  def append(self, match):
    self.matcheslist.append(match)
    #logging.debug ('matcheslist=',self.matcheslist)

  def extend(self, another_matcheslist):
    self.matcheslist.extend(another_matcheslist)  

  def delete(self, index):
    del self.matcheslist[index]


  def group(self, *args):
    if len(self.matcheslist) == 0: 
      return None
    else:  
      if len(args) >0:
        if args[0] <0 and args[0] > len(self.matcheslist):
          raise Exception('Invalid group value out of range')
        return self.matcheslist[args[0]]
    return self.matcheslist[0]

  def DFA(self, *args):
    if len(self.matcheslist) == 0: 
      return None
    else:  
      if len(args) >0:
        if args[0] <0 and args[0] > len(self.matcheslist):
          raise Exception('Invalid group value out of range')
        return self.matcheslist[args[0]].DFA()
    return self.matcheslist[0].DFA()    

  def start(self, *args):
    return self.group(*args).start()

  def end(self, *args):
    return self.group(*args).end()

  def __iter__(self):
    return iter(self.matcheslist)

  def next(self): # Python 3: def __next__(self)
    if self.current > len(self.matcheslist):
      raise StopIteration
    else:
      self.current += 1
    return self.matcheslist[self.current]   

  def __len__(self):
    return len(self.matcheslist)

  # def __repr__(self):
  #   ml = ''
  #   for m in self.matcheslist:
  #     ml = ml + '<pyrata.re Match object; span=({}, {}), match="{}">\n'.format(str(m.start()), str(m.end()), str(m.group()))
  #   return ml

  def __eq__(self, other):
    if other == None: 
      return False       
    matches = 0
    for s, o in zip(self.matcheslist, other.matcheslist):
      if s == o: matches += 1
    if matches == len(self.matcheslist): 
      return True
    return False  

  def __ne__(self, other):
    if other == None: 
      return True       
    matches = 0
    for s, o in zip(self.matcheslist, other.matcheslist):
      if s == o: matches += 1
    if matches == len(self.matcheslist): 
      return False
    return True 

  def __repr__(self):
    return ''.join(['<pyrata.re MatchesList object; matcheslist="',str(self.matcheslist),'">'])


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  MAIN
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__ == '__main__':  
  start = 0
  end = 1
  data =  [{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'Pyrata', 'pos': 'NNP'}]

  print ('Debug: create the Match(start={}, end={}, value={})'.format(start, end, data[start:end]))
  match = Match (start=start, end=end, value=data[start:end])
  print('Debug: match=', match)