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
"""Parse a pattern step"""


import logging
# logging.info() Report events that occur during normal operation of a program (e.g. for status monitoring or fault investigation)
# logging.debug() for very detailed output for diagnostic purposes
# logging.warning() Issue a warning regarding a particular runtime event

#import re 
from re import compile 

from pprint import pprint, pformat
import ply.yacc as yacc
from sympy import *
#import sympy.not as sympy_not
#from FAdo.fa import *
#from FAdo.reex import *

from pyrata.lexer import *



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_current_pattern_step_offsets(p):
  ''' Line Number and Position Tracking'''
  # http://www.dabeaz.com/ply/ply.html#ply_nn33
  left_symbol_start, left_symbol_end = p.lexspan(1)
  if p.lexer.lexpos > len(p.lexer.lexdata):
    previous_lextoken_end = len(p.lexer.lexdata)
  else:
    previous_lextoken_end = p.lexer.lexpos - len(p.lexer.lexTokenEndDict[p.lexer.lexpos].value)
  return left_symbol_start, previous_lextoken_end



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_current_pattern_step(p, start, end):
  ''' surface form of the current parsed step'''
  return p.lexer.lexdata[start:end]



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def log(p, production):
  # Line Number and Position Tracking
  # http://www.dabeaz.com/ply/ply.html#ply_nn33

  step_start, step_end = get_current_pattern_step_offsets(p) 
  step = get_current_pattern_step(p, step_start, step_end)
  logging.info('Production=%s ; step=%s', production, step)
  logging.debug('Whole pattern/lexdata=%s ; len(lexdata)=%s', p.lexer.lexdata, str(len(p.lexer.lexdata)))
  logging.debug('# of lexical tokens in the current production rule=%s', str(len(p)))



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# wi less consumption memory http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to
def depth(l):
    if isinstance(l, list):
        return 1 + max(depth(item) for item in l)
    else:
        return 0



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class SyntacticPatternParser(object):

# p.lexer. variables which are modified in the parsing
#
# group_pattern_offsets_group_list
# pattern_must_match_data_start
# pattern_must_match_data_end
# pattern_steps
#
# see definition in lexer

  precedence = (
    ('left', 'LBRACKET','RBRACKET'),    
    ('left',  'OR'),
    ('left', 'AND'),
    ('left', 'LPAREN','RPAREN'),
    ('right', 'NOT'),
    ('left', 'EQ'),
#  ('right', 'OPTION', 'ANY', 'ATLEASTONE')
  )


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING METHODS
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




# _______________________________________________________________
  def p_step(self,p):
    '''step : single_constraint
            | LBRACKET constraint_class RBRACKET '''  # | NOT atomicconstraint # ajoute WARNING: 2 shift/reduce conflicts
    #log(p, '(step->...)')
    if len(p) == 2:
      p[0] = p[1]

      #log(p, '(step->single_constraint)')
    
    #elif p[1] == '!':
    #  p[0] = not(p[2])
    #  log(p, '(step->NOT step)')
    
    else:
      p[0] = p[2]
      #log(p, '(step->LBRACKET constraint_class RBRACKET)')
      # nfa guiguan
      #last = p.lexer.nfa_guiguan_pattern_input.pop()
      #p.lexer.nfa_guiguan_pattern_input.append('['+last+']')     
    #logging.info ('step sympy expression:{}'.format(p[0]))

    #p.lexer.automata = atom(p[0])
    #print ('Debug: symbolic_step_expression={}'.format(p[0]))
    p.lexer.symbolic_step_expression.append(p[0])

# _______________________________________________________________
  def p_constraint_class(self,p):
    '''constraint_class : constraint_class AND constraint_class_part
            | constraint_class OR constraint_class_part 
            | constraint_class_part ''' 
    
    #log(p, '(constraint_class->...)')  
    if len(p) == 2:
      p[0] = p[1] 
      #log(p, '(constraint_class->constraint_class_part)')
    #
    else:
      if p[2] == '&':
        p[0] = And(p[1], p[3]) 
        #log(p, '(constraint_class->constraint_class AND constraint_class_part)')
        # nfa guiguan
        #p3 = p.lexer.nfa_guiguan_pattern_input.pop()
        #p1 = p.lexer.nfa_guiguan_pattern_input.pop() 
        #p.lexer.nfa_guiguan_pattern_input.append(p1+'&'+p3)     
      else: 
        p[0] = Or(p[1], p[3])
        #log(p, '(constraint_class->constraint_class OR constraint_class_part)')
        # nfa guiguan
        #p3 = p.lexer.nfa_guiguan_pattern_input.pop()
        #p1 = p.lexer.nfa_guiguan_pattern_input.pop() 
        #p.lexer.nfa_guiguan_pattern_input.append(p1+'|'+p3)        
    
    #logging.info ('step sympy expression:{}'.format(p[0]))      

# _______________________________________________________________
  def p_constraint_class_part(self,p):
    '''constraint_class_part : single_constraint
                    | LPAREN constraint_class RPAREN  
                    | NOT constraint_class '''
    
    #log(p, '(constraint_class_part->...)')  

    if p[1] == '(':
      p[0] = p[2]
      #log(p, '(constraint_class_part->LPAREN constraint_class RPAREN)')
      # nfa guiguan
      #last = p.lexer.nfa_guiguan_pattern_input.pop() 
      #p.lexer.nfa_guiguan_pattern_input.append('('+last+')')
    elif p[1] == '!':
      p[0] = Not(p[2])
      #log(p, '(constraint_class_part->NOT constraint_class)')
      # nfa guiguan
      #last = p.lexer.nfa_guiguan_pattern_input.pop() 
      #p.lexer.nfa_guiguan_pattern_input.append('!'+last)
    else:
      p[0] = p[1]
      #log(p, '(constraint_class_part->single_constraint)')

    #logging.info ('step sympy expression:{}'.format(p[0]))

# _______________________________________________________________
  def p_single_constraint(self,p):
    '''single_constraint : NAME EQ VALUE 
                          | NAME MATCH VALUE
                          | NAME IN VALUE'''
    
    #log(p, '(single_constraint->...)')  
    #attName = p[1]
    #operator = p[2]
    #attValue = p[3][1:-1]

    # add to the temporary list of single constraint string
    single_constraint_string = ''.join([p[1],p[2],p[3]])
    p.lexer.single_constraint_symbol_list.append(single_constraint_string)
    # print ('Debug: single_constraint_string='.format(single_constraint_string))
    # print ('Debug: p[1]='.format(p[1]))
    # print ('Debug: p[2]='.format(p[2]))
    # print ('Debug: p[3]='.format(p[3]))


    # add single contraint tuple to lists in the lexer 
    c = {}
    c['name'] = p[1]
    c['operator'] = p[2]
    c['value'] = p[3][1:-1]
    # print ('Debug: single_constraint value={}'.format(c['value']))
    # deep_copy cannot copy re so we move the re evaluate at runtime...
    #if c['operator'] == '~': 
      #c['value'] = re.compile(c['value'])
    #  c['value'] = compile(c['value'])
    p.lexer.single_constraint_tuple_list.append(c)

    # build a variable and a name
    indice = str(len(p.lexer.single_constraint_tuple_list)-1)
    var = {} 
    var[indice] =  symbols(single_constraint_string.replace(' ','\\ ').replace(':','\\:'))
    p[0] = var[indice]
    #print ('Debug: c='.format(c))
    #print ('Debug: single_constraint_string='.format(single_constraint_string))
    #print ('Debug: var[indice]='.format(var[indice]))
    p.lexer.single_constraint_variable_list.append(var[indice])

    # nfa guiguan
    #p.lexer.nfa_guiguan_pattern_input.append(single_constraint_string)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING ERROR HANDLING
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def p_error(self,p):
    if not p:
       
      logging.info("Info - syntactic step parser - parsed.")
      return

    # http://www.dabeaz.com/ply/ply.html#ply_nn26 6.8.2
     # Read ahead looking for a closing ';'

    logging.warning('Warning - syntactic step parser - unexpected token type="{}" with value="{}" at position {}. Search an error before this point.'.format(p.type, p.value, p.lexer.lexpos))
    while True:
      tok = self.parser.token()             # Get the next token
      if not tok: 
        break
    self.parser.restart()


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  CONSTRUCTOR
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#  def __init__(self, tokens, *argv):
  def __init__(self, **kwargs):
    if 'tokens' in kwargs.keys(): # MANDATORY
      self.tokens = kwargs['tokens']
    kwargs.pop('tokens', None)

    # debugging and logging http://www.dabeaz.com/ply/ply.html#ply_nn44 
    #self.parser = yacc.yacc(module=self, start='step', errorlog=yacc.NullLogger(), debug = True, debugfile='debug_file', **kwargs) 
    self.parser = yacc.yacc(module=self, start='step', errorlog=yacc.NullLogger(), debug = False, **kwargs) 

    # https://github.com/dabeaz/ply/blob/master/ply/yacc.py
    # debug yaccdebug   = True        # Debugging mode.  If set, yacc generates a
                               # a 'parser.out' file in the current directory

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  MAIN
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# example use:
if __name__ == '__main__':
  pattern='?lem="the" ( pos="JJ"* [pos="NN" & (lem="car" | !lem="bike" | !(lem="bike"))] ) [raw="is" | raw="are"]'
  print ('Pattern:', pattern)

  #data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'blue', 'lem':'blue', 'pos':'JJ'}]     
  #data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
  
  #pattern = 'pos:"NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}]
  print ('Data:', data)

  # Build the parser and 
  l = Lexer(pattern=pattern, data=data) 
  m = SyntacticPatternParser(tokens=l.tokens, start='expression')

  # try it out
  # print ("Copy the grammar line without 'Grammar: ' (whitespace should not been included); The semi-colon ';' will lead to a parsing error")
  # while True:
  #   try:
  #     #text2parse
  #     s = input('cl > ')   # Use raw_input on Python 2
  #   except EOFError:
  #     break
  #   m.parser.parse(s, l.lexer, tracking=True)


