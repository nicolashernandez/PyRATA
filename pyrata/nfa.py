#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PyRATA
#
# Authors: 
#         Nicolas Hernandez <nicolas.hernandez@gmail.com>
#         Guan Gui 2014-08-10 13:20:03 https://www.guiguan.net/a-beautiful-linear-time-python-regex-matcher-via-nfa
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

"""NFA builder (compilation) and matcher (execution) """

import sys
import logging


import ply.yacc as yacc
from pyrata.lexer import *
from pyrata.syntactic_step_parser import *

from pyrata.nfa import *
#import pyrata.nfa

from pyrata.state import *


import copy

import re

from pyrata.match import *


from pprint import pprint, pformat

DEBUG = False
STEP = False

(PREFIX_BEGIN, PREFIX_INSIDE, PREFIX_OTHER) = ('B-', 'I-', 'O-')



#if DEBUG:
from graph_tool.all import *




# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def normalize_chunk_operator (pattern, **kwargs):    
  '''
  Here is a trick. The chunk operator does not exist. 
  It is turn into a specific sequence of steps with equal operators.
  Indeed 'ch-"NP"' is rewritten in '(ch="B-NP" ch="I-NP"*)'
  FIXME or not: parenthesis imply groups for chunks in the target pattern
  '''
  logging.debug("CompiledPattern - normalize_chunk_operator")
  return re.sub('([a-zA-Z_][a-zA-Z0-9_]*)-\"(([^\\\n]|(\\.))*?)\"', '(\g<1>="B-\g<2>" \g<1>="I-\g<2>"*)', pattern) 


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def pattern_to_guiguan_nfa_pattern_input (pattern):
  """ Return a pattern as a list
      Each special character as an element of list 
  """
  logging.debug("CompiledPattern - pattern_to_guiguan_nfa_pattern_input")

  cur_pos = 0
  guiguan_nfa_pattern_input = []
  last_char_was_special = False
  in_constraint_value = False
  in_class_constraint = False

  while cur_pos < len(pattern):
    c = pattern[cur_pos]
    #print ("Debug: c={} in_class_constraint={} in_constraint_value={}".format(c, in_class_constraint, in_constraint_value))
    if c == '(' and not(in_class_constraint or in_constraint_value):
      guiguan_nfa_pattern_input.append(c)
      last_char_was_special = True
    elif c == ')' and not(in_class_constraint or in_constraint_value):
      guiguan_nfa_pattern_input.append(c)
      last_char_was_special = True
    elif c == '|' and not(in_class_constraint or in_constraint_value):
      #print ('here we append a new element')
      guiguan_nfa_pattern_input.append(c)
      last_char_was_special = True
    elif c == '*' and not(in_constraint_value):
      guiguan_nfa_pattern_input.append(c)
      last_char_was_special = True
    elif c == '+' and not(in_constraint_value):
      guiguan_nfa_pattern_input.append(c)
      last_char_was_special = True
    elif c == '?' and not(in_constraint_value):
      guiguan_nfa_pattern_input.append(c)
      last_char_was_special = True
    elif c == ' ' and not(in_class_constraint or in_constraint_value):
      #guiguan_nfa_pattern_input.append(c) 
      last_char_was_special = True  
    elif c == '$' and not(in_constraint_value):
      guiguan_nfa_pattern_input.append(c)
      last_char_was_special = True
    elif c == '^' and not(in_constraint_value):
      guiguan_nfa_pattern_input.append(c)
      last_char_was_special = True

    else:
      # create a new element
      if last_char_was_special or cur_pos == 0:
        guiguan_nfa_pattern_input.append(c)
      else:
      # merge to the last element
        guiguan_nfa_pattern_input[len(guiguan_nfa_pattern_input)-1] = ''.join([guiguan_nfa_pattern_input[len(guiguan_nfa_pattern_input)-1],c])
      last_char_was_special = False

      # in order not to create an element when a whitespace is encountered inside of a single constraint value

      if c == '"':
        if in_constraint_value:
          # case where " is in a constraint value
          # do not change the constraint value when escaped
          # cur_pos >0 if in_constraint_value so we can test cur_pos-1

          if pattern[cur_pos-1] != '\\': 
            in_constraint_value = False
        else:
          in_constraint_value = True  
      # in order to consider a class constraint as a single element 
      # even if made of several single constraints combined with special character like | pipe or () brackets    
      if c == '[' and not(in_constraint_value):
        in_class_constraint = True
      if c == ']' and not(in_constraint_value):
        in_class_constraint = False  
    cur_pos += 1
  return guiguan_nfa_pattern_input

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def turn_backslashed_double_quote_into_unicode(pattern):
  return pattern.replace('\\"','\u0022')


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def evaluate_single_constraint (data, name, operator, value, lexicons):
  # checking if the given value, interpreted as a string, matches the current dict feature of the data   
  logging.debug("CompiledPattern - evaluate_single_constraint")

  #print ("Debug: CompiledPattern - evaluate_single_constraint")

  if name in data:
    if operator == '=':
      return (data[name] == value)
    # checking if the given value, interpreted as regex, matches the current dict feature of the data 
    elif operator == '~':
      return (re.search(value,data[name]) != None)
  #    return (value.search(data[name]) != None)

    # checking if the current dict feature of the data belongs to a list having the name of the given value
    elif operator == '@':
      # check if the named list is kwown
      if value in lexicons:
        return (data[name] in lexicons[value])
  # the matching operation fails or the attribute name is unknown
  return False   




# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def build_matching_result (an_nfa, s, i, j, matcheslist):
    logging.debug("CompiledPattern - build_matching_result")

    # print ('Debug: build_matching_result ------------------------------------------')

    # print ('Debug: build_matching_result - i={} j={} step_counter={}'.format(i, j, an_nfa.step_counter))
    # print ('Debug: build_matching_result an_nfa.cur_states={}'.format(an_nfa.cur_states))

    # print ('Debug: build_matching_result - contains_matching_state #={} cur_states={}'.format(len(an_nfa.cur_states), an_nfa.cur_states))

    # print ('Debug: build_matching_result - nfa_step_counter={}'.format(an_nfa.step_counter))
    #print ('Debug: build_matching_result - nfa_step_os_is_leaf={}'.format( pformat(an_nfa.step_os_is_leaf)))

    #print ('Debug: build_matching_result - nfa_states_dict={}'.format( an_nfa.states_dict))
    # print ('Debug: build_matching_result - nfa_states_dict={}'.format(pformat( an_nfa.states_dict)))

    # group
    groups_start = dict () # position where the given group starts in the data (first seen)
    groups_end = dict () # position where the given group ends in the data (last seen)
    #groups_start[0] = i
    #groups_end[0] = j +1

    # DFA + group
    DFA = []
    #other_possible_last_state_id = list(an_nfa.step_os_is_leaf[an_nfa.step_counter])[0] #.keys()
    #print ('Debug: build_matching_result - DFA building - At step={}, the other_possible_last_state_id reference is {} '.format(an_nfa.step_counter-1, other_possible_last_state_id))

    #print ('Debug: build_matching_result - nfa_step_os_is_leaf[an_nfa.step_counter-1]={}'.format( pformat(an_nfa.step_os_is_leaf[an_nfa.step_counter-1])))
    #print ('Debug: build_matching_result - list(an_nfa.step_os_is_leaf[an_nfa.step_counter-1])={}'.format( pformat(list(an_nfa.step_os_is_leaf[an_nfa.step_counter-1]))))

    #last_state_id = list(an_nfa.step_os_is_leaf[an_nfa.step_counter-1])[0] #.keys()
    last_state_id = an_nfa.last_state_id
    for l in range(an_nfa.step_counter-1, -1, -1):  # 3rd argument for the reverse order
        #print ('Debug: build_matching_result - DFA building - At step={}, the last_state_id reference is {} '.format(l, last_state_id))
        #if last_state_id != -1: print ('Debug: build_matching_result - DFA building - The corresponding state is={}'.format(an_nfa.states_dict[last_state_id])) # if wildcard then laststateid = -1 and so error 

        # get the state corresponding to an id which is a leaf (second arg of list), value of state_id at a given matching step 
        #print ('Debug: build_matching_result - DFA building - At this step, there are the following back associations={}'.format(an_nfa.step_os_is_leaf[l]))
        if not (last_state_id in an_nfa.step_os_is_leaf[l]):
          #print ('Debug: build_matching_result - DFA building - But none of them from the reference !!!')
          #print ('Debug: build_matching_result - DFA building - In that case we assume to be back to the first root state')
          #print ('Debug: build_matching_result - DFA building - and that there is actually one association at this stage')
          #print ('Debug: build_matching_result - DFA building - and that the corresponding state is #S')
          #print ('Debug: build_matching_result - DFA building - In that case we simply take the present io id')
          # FIXME should to some tests (only one association and char #S)
          last_state_id = list(an_nfa.step_os_is_leaf[l])[0] #.keys()



        #print ('Debug: build_matching_result - DFA building - The one from the reference is={}'.format(an_nfa.step_os_is_leaf[l][last_state_id]))
        
        leaf_id = an_nfa.step_os_is_leaf[l][last_state_id][1]
        is_id = an_nfa.step_os_is_leaf[l][last_state_id][0] if an_nfa.step_os_is_leaf[l][last_state_id][0] != -1 else leaf_id
        #print ('Debug: build_matching_result - DFA building - It said we go in reverse order from(os)={} to(is)={}'.format(last_state_id, is_id))

        #print ('Debug: build_matching_result - DFA building - The corresponding leaf of is_id={} is leaf_id={} '.format(is_id, leaf_id))

        # track of the groups position
        for g in an_nfa.step_os_is_leaf[l][last_state_id][2]:
            if not (g in groups_end):
                groups_end[g] = i+l+1
            groups_start[g] = i+l 

            #print ('Debug: build_matching_result - DFA building - track group={} start={} end={} in i={} j={} l={}'.format(g, groups_start[g], groups_end[g], i, j, l))  

        #
        DFA.insert(0, an_nfa.states_dict[leaf_id])
        last_state_id = is_id
    #print ('Debug: build_matching_result - DFA=\n{}'.format(pformat(DFA)))

    
    current_groups = []
#    for g in (groups_start.keys() | groups_end.keys()):
    for g in (groups_start.keys()):
        current_groups.append([s[groups_start[g]:groups_end[g]], groups_start[g], groups_end[g]])
        # debug group
        #print ('Debug: build_matching_result - create group={} start={} end={}'.format(g, groups_start[g], groups_end[g]))  
    #matcheslist.append(Match(start=groups_start[0], end=groups_end[0], value=s[groups_start[0]:groups_end[0]],groups=current_groups))
    matcheslist.append(Match(groups=current_groups, DFA=DFA))
    return matcheslist


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class CompiledPattern(object):


    def __init__(self):
        logging.debug("CompiledPattern - create CompiledPattern object")
        self.group_counter = 0        # counts the new groups i.e. each openning bracket 
                                 # class variable to make it available in the recursive process
        self.group_depth = 0          # inc/dec the depth depending on the encountered bracket ; inc when opening and dec when closing
                                 # class variable to make it available in the recursive process
        self.already_closed_group_at = dict() # the current nfa building (the continue at the end of each special char case makes decrement more than we wants
                                 # we log the already encountered closing bracket at a position 
                                 # in order to avoid to decrement twice (or more) at a same position.
                                 # class variable to make it available in the recursive process
        self.group_pile = []     # list of the group indice currently open
                                 # at the top there is the indice of the current deepest group
                                 # class variable to make it available in the recursive processs                                 
        self.currently_open_group_counter = 0                        


        self.pattern = None # guiguan pattern (a list of elements and special char)
        self.nfa = None
        self.lexicons = {}

        self.pattern_must_match_data_start = False
        self.pattern_must_match_data_end = False
        #self.lexicon_keys = None




    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def compile(self, p, lexicons = {}, **kwargs):
        """ Compile a regular expression pattern into a regular expression object, 
            which can be used for matching using match(), search()... methods, described below.
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.debug("CompiledPattern - compile")

      #
        self.lexicons = lexicons    

        self.group_pile.append (self.group_counter)

        # build guiguan_nfa_pattern_input
        #self.pattern =  pattern_to_guiguan_nfa_pattern_input(normalize_chunk_operator(turn_backslashed_double_quote_into_unicode(p)))
        self.pattern =  pattern_to_guiguan_nfa_pattern_input(normalize_chunk_operator(p))

        #print ('Debug: guiguan_nfa_pattern_input={}'.format(self.pattern))

        # set if there are pattern start and end constraints on the data 
        if len(self.pattern) > 0:
          if self.pattern[0] == '^':
              self.pattern_must_match_data_start = True
              del self.pattern[0]
          if self.pattern[len(self.pattern)-1] == '$':
              self.pattern_must_match_data_end = True
              del self.pattern[len(self.pattern)-1]

        return self.compile_nfa_pattern()

    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def compile_nfa_pattern(self):
        logging.debug("CompiledPattern - compile_nfa_pattern")

        _, self.nfa = self.__parse_current_pattern_pos(self.pattern, 0)

        #print('COMPILE-----------------\npattern={}\nlast_appended_state={}\nstart_state={}\nmatching_state={}\ncur_states={}'
        #    .format(self.pattern, self.nfa.last_appended_state, self.nfa.start_state, self.nfa.matching_state, self.nfa.cur_states))

        return self.nfa



    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def __parse_current_pattern_pos(self, p, start_pos):
        """Build a NFA for pattern p starting at position pos
        """
        logging.debug("CompiledPattern - __parse_current_pattern_pos")

        global DEBUG

        last_elem = None
        cur_pos = start_pos

#        nfa = self.NFA()
        nfa = NFA()

        while cur_pos < len(p):
            c = p[cur_pos]
            cur_elem = None

            # debug group
            #print ('--------------------------------------------')

            #print ('Debug: __parse_current_pattern_pos - prologue - cur_pos={}, group={}, depth={}, cur_grp={} c={}'
            #        .format(cur_pos, self.group_counter, self.group_depth, self.group_pile[len(self.group_pile)-1], c))
            #if last_elem != None: 
                #print ('Debug: __parse_current_pattern_pos - prologue - last_elem[0]={} id={}'.format(last_elem[0], last_elem[0].id))                                
                #print ('Debug: __parse_current_pattern_pos - prologue - last_elem[1]={} id={}'.format(last_elem[1], last_elem[1].id))                                

            if c == '(':
                # debug group
                #print ('Debug: __parse_current_pattern_pos - ( - open group')                
                self.group_depth +=1
                self.group_counter +=1
                self.group_pile.append (self.group_counter)

                # start a new nfa
                if last_elem:
                    nfa.append_element(last_elem)

                original_debug_flag = DEBUG
                if original_debug_flag:
                    DEBUG = False
                cur_pos, sub_nfa = self.__parse_current_pattern_pos(
                    p, cur_pos + 1)
                if original_debug_flag:
                    DEBUG = True

                #print ('Debug: __parse_current_pattern_pos - ( - sub_nfa.states_dict={}'.format(sub_nfa.states_dict))

                cur_pos += 1

                #print ("char={} symbolic_step_expression={} single_constraint_tuple_list={} single_constraint_variable_list={}"
                #    .format(sub_nfa.char, sub_nfa.symbolic_step_expression,sub_nfa.single_constraint_tuple_list,sub_nfa.single_constraint_variable_list))
                
                sub_nfa.start_state.char = State.EMPTY_STATE
                sub_nfa.matching_state.char = State.EMPTY_STATE
                #.symbolic_step_expression = symbolic_step_expression
                #.single_constraint_tuple_list = single_constraint_tuple_list
                #.single_constraint_variable_list =

                last_elem = sub_nfa.elem()
                #print ('Debug: __parse_current_pattern_pos - ( - continue')                
                continue
            elif c == ')':

                #print ('Debug: __parse_current_pattern_pos - ) - already_closed_group_at={}'.format(self.already_closed_group_at))
                # the condition is a patch because it enters in the if too many times and decrement
                if not cur_pos in self.already_closed_group_at: 

                    self.group_depth -=1 
                    # debug group
                    #print ('Debug: __parse_current_pattern_pos - ) - no group was closed at cur_pos={}'.format(cur_pos) )                                
                    #print ("Debug: __parse_current_pattern_pos - ) - decrement group_depth=", self.group_depth)
                    self.group_pile.pop()

                self.already_closed_group_at[cur_pos] = True
                # debug group
                #print ('Debug: __parse_current_pattern_pos - ) - close group')
                #print ('Debug: __parse_current_pattern_pos - ) - group closed at cur_pos={}'.format(cur_pos) )                                
                #print ('Debug: __parse_current_pattern_pos - ) - already_closed_group_at={}'.format(self.already_closed_group_at))                                
                #print ('Debug: __parse_current_pattern_pos - ) - nfa.states_dict={}'.format(nfa.states_dict))
                #print ('Debug: __parse_current_pattern_pos - ) - break')     
                # return current nfa to parent level             
                break
            elif c == '|':
                # start a new nfa, return while encounters a ')'
                # or end of pattern
                if last_elem:
                    nfa.append_element(last_elem)
                    last_elem = None

                original_debug_flag = DEBUG
                if original_debug_flag:
                    DEBUG = False
                cur_pos, sub_nfa = self.__parse_current_pattern_pos(
                    p, cur_pos + 1)
                if original_debug_flag:
                    DEBUG = True

                nfa.or_nfa(sub_nfa)
                continue
            elif c == '*':
                # Syntax check
                if not last_elem:
                    if cur_pos > start_pos:
                        raise self.InvalidRegexPattern('qualifier %s cannot be put directly after qualifier %s' % (c, p[cur_pos - 1]))
                    else:
                        raise self.InvalidRegexPattern('qualifier %s cannot be used to qualify empty entity' % c)

                #cur_elem = self.State.create_element_star_state(last_elem)
                cur_elem = State.create_element_star_state(last_elem)

                last_elem = None
            elif c == '+':
                # Syntax check
                if not last_elem:
                    if cur_pos > start_pos:
                        raise self.InvalidRegexPattern('qualifier %s cannot be put directly after qualifier %s' % (c, p[cur_pos - 1]))
                    else:
                        raise self.InvalidRegexPattern('qualifier %s cannot be used to qualify empty entity' % c)

                #cur_elem = self.State.create_element_plus_state(last_elem)
                cur_elem = State.create_element_plus_state(last_elem)

                last_elem = None
            elif c == '?':
                # Syntax check
                if not last_elem:
                    if cur_pos > start_pos:
                        raise self.InvalidRegexPattern('qualifier %s cannot be put directly after qualifier %s' % (c, p[cur_pos - 1]))
                    else:
                        raise self.InvalidRegexPattern('qualifier %s cannot be used to qualify empty entity' % c)

                #cur_elem = self.State.create_element_question_mark_state(last_elem)
                cur_elem = State.create_element_question_mark_state(last_elem)
                last_elem = None
            else:

                if last_elem:
                    #print ('Debug: __parse_current_pattern_pos - c - no special character')
                    nfa.append_element(last_elem)
                # Processing a char (i.e. a single pattern step)
                # The process consists in generating a symbolic expression for further evaluation (i.e. at the matching time).
                # It stores in the state whatever it will be required for the step evaluation    
                # in other words: symbolic_step_expression, single_constraint_tuple_list, single_constraint_variable_list
                symbolic_step_expression = single_constraint_tuple_list = single_constraint_variable_list = []
                if c != '.':
                    l = Lexer(pattern=c) 
                    #print ('Debug: SyntacticStepParser of c={}'.format(c))
                    #y = SyntacticPatternParser(tokens=l.tokens, start='step') #,**kwargs
                    y = SyntacticPatternParser(tokens=l.tokens) #,**kwargs

                    logging.debug('CompiledPattern - ply parse the current pattern element')

                    y.parser.parse(c, l.lexer,  tracking=False)
                    # debug group
                    #print ('Debug: c={}, group={}, depth={}, sym_expr={}, single_constr_tuple_list={}, single_constr_var_list={}'
                    #    .format(c, self.group_counter, self.group_depth, l.lexer.symbolic_step_expression, l.lexer.single_constraint_tuple_list, l.lexer.single_constraint_variable_list))
                    #print ('Debug: __parse_current_pattern_pos - c - group_pile={}'.format(self.group_pile))
                    symbolic_step_expression = l.lexer.symbolic_step_expression
                    single_constraint_tuple_list = l.lexer.single_constraint_tuple_list
                    single_constraint_variable_list = l.lexer.single_constraint_variable_list
                last_elem = State.create_char_state(c, symbolic_step_expression, single_constraint_tuple_list, single_constraint_variable_list, list(self.group_pile))
                    # group_pile surrounded of list to make a new list from values (a kind of deep copy)
                    #print ('Debug: __parse_current_pattern_pos - c - last_elem.nfa.id={}'.format(last_elem[0].id))


            if cur_elem:
                nfa.append_element(cur_elem)
            cur_pos += 1

        if last_elem:
            #print ('Debug: __parse_current_pattern_pos - epilogue - in if last_elem:  nfa.states_dict={}'.format(nfa.states_dict))
            nfa.append_element(last_elem)
        #print ('Debug: __parse_current_pattern_pos - epilogue - after if last_elem:  nfa.states_dict={}'.format(nfa.states_dict))
    

        nfa.finalise_nfa()

        return cur_pos, nfa

    class InvalidRegexPattern(Exception):
        pass


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def search (self, s, mode = 'greedy', matchMethod = False, fullmatchMethod = False, pos = 0, endpos = None, **kwargs):
        """ Scan through data looking for the first location where the regular expression pattern produces a match, 
        and return a corresponding match object. 
        Return None if no position in the data matches the pattern."""
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.debug("CompiledPattern - search")

        endpos = len(s) if endpos == None else endpos
        #if pos <0 or endpos < pos or endpos > len(s): return None
        if pos <0: pos = 0
        if endpos > len(s): endpos = len(s)
        if endpos < pos: return None
        
        # while parsing the data we parse and alter the nfa
        # each time the nfa did not match we reinit it by copying it from its original form 
        an_nfa = copy.deepcopy(self.nfa)       

        # in greedy mode, we do not stop the search after the first match
        # so we save the last successful configuration
        last_matched_nfa = None
        last_matched_i = -1
        last_matched_j = -1
        
        #for i in range(0, len(s)):
        #    for j in range(i, len(s)):
        #        print ("Debug: search - i={} j={} s[j]={}".format(i, j, s[j]))
        i = pos
        while i < endpos:           # data exploration  
            j = i      
            
            while j < endpos:       # pattern exploration 

                    if (self.pattern_must_match_data_start or matchMethod or fullmatchMethod) and i != pos:
                        return None
                    
                    c = s[j]
                    #print ('-----------------------------------------------------')
                    #print ("search - nfa.step({}) data_index={} pattern_index={}".format(c, i, j))

                    logging.debug ('-----------------------------------------------------')
                    logging.debug ("search - nfa.step({}) data_index={} pattern_index={}".format(c, i, j))

                    an_nfa.step(c, self.lexicons)
                    
                    if not len(an_nfa.cur_states):
                        # there is no more state to explore
                        #print ("Debug: search - there is no more state to explore")

                        # if there was a backup we compute and create all the stuff with the current nfa
                        if last_matched_nfa != None:
                            #print ("Debug: search - no more state to explore and previously matched nfa so we build_matching_result")


                            # if we are here then it means we did a step too far
                            # the same for i and j
                            an_nfa.step_counter -= 1
                            #print ("Debug: search - i={} j={}".format(i, j))
                            # j -= 1
                            # if j == 0: 
                            #     j = endpos
                            #     i -= 1
                            # FIXME if i == 0 : there will be a bug when doing i-1 ...

                            #print ('Debug: search last_matched_nfa.cur_states={}'.format(last_matched_nfa.cur_states))
                            #
                            matcheslist = build_matching_result (last_matched_nfa, s, last_matched_i, last_matched_j, MatchesList())

                            if len(matcheslist) > 0:

                                if (self.pattern_must_match_data_end  or fullmatchMethod) and j +1 != endpos:
                                    return None

                                return matcheslist.group(0)
                            # i = last_matched_i
                            # j = last_matched_j
                            last_matched_nfa = None
                            last_matched_i = -1
                            last_matched_j = -1    

                        # then we reinit so that next exploration starts after the end of the match
                        an_nfa = copy.deepcopy(self.nfa)

                        break

                    #
                    if an_nfa.contains_matching_state():
                        #print ("Debug: search - the nfa contains_matching_state")

                        if mode == 'greedy':
                            #print ("Debug: search - we are in greedy mode")
                            if len(an_nfa.cur_states) >=2 or an_nfa.have_out_states(): # FIXME =>2 or =>1
                                # at least one nfa path which could be explored
                                #print ("Debug: search - the nfa contains_matching_state but we are in greedy mode so we save the nfa and pursue the exploration")

                                # we backup what do we need for computing and creating all the stuff
                                last_matched_nfa = copy.deepcopy(an_nfa)
                                last_matched_i = i
                                last_matched_j = j
                                j += 1
                                continue # we cut here and pursue the embedding loop at the next iteration
                            #else: 
                               # no more path to explore, so we stop here
                               # we compute and create all the stuff with the current nfa   
                        #else: 
                            # we compute and create all the stuff with the current nfa
                        #print ("Debug: search - the current step ends the nfa (either no greedy or no more out_states) so we build_matching_result")
                        matcheslist = build_matching_result (an_nfa, s, i, j, MatchesList())

                        if len(matcheslist) > 0 :


                            if (self.pattern_must_match_data_end  or fullmatchMethod) and j +1 != endpos:
                                return None
                            # debug group FIXME remove it    
                            #print('SEARCH-----------------\nlast_appended_state={}\nstart_state={}\nmatching_state={}\ncur_states={}'
                            #    .format(an_nfa.last_appended_state, an_nfa.start_state, an_nfa.matching_state, an_nfa.cur_states))
                            #print ("Debug: search - some matcheslist to return ")
                            return matcheslist.group(0)
                    j += 1  
            if last_matched_nfa != None and j == endpos:
                # to prevent from restarting to i+1 when incrementing j in greedy mode; indeed when j = len(s), then i +=1 and j = i 
                # the underlying idea in the greedy mode is that a larger matching nfa may be possible and we try to get it 
                break    

            if self.pattern_must_match_data_start or matchMethod or fullmatchMethod:
                break    
            i += 1       

        # if there was a backup we compute and create all the stuff with the current nfa
        if last_matched_nfa != None:
            #print ("Debug: search - no more data to explore and previously matched nfa so we build_matching_result")

            # if we are here then it means we did a step too far
            # the same for i and j
            an_nfa.step_counter -= 1
            #print ("Debug: search - i={} j={}".format(i, j))

            #
            matcheslist = build_matching_result (last_matched_nfa, s, last_matched_i, last_matched_j, MatchesList())

            if len(matcheslist) > 0:
                #print ('Debug: fullmatchMethod last one j={} len(s)={}'.format(j,len(s)))
                if (self.pattern_must_match_data_end or fullmatchMethod) and j != endpos:
                    return None

                return matcheslist.group(0)
        return None


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def match (self, s, mode = 'greedy', **kwargs):
      """ If zero or more tokens at the beginning of data match this regular expression, return a corresponding match object. 
      Return None if the data does not match the pattern; """
      logging.debug('----------------------------------------------------------------------------------------------------------')
      logging.debug ("match - we call search the get the match")      
      return  self.search (s, mode, matchMethod = True, **kwargs)

    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def fullmatch (self, s, mode = 'greedy', **kwargs):
      """ If zero or more tokens at the beginning of data match this regular expression, return a corresponding match object. 
      Return None if the data does not match the pattern; """
      logging.debug('----------------------------------------------------------------------------------------------------------')
      logging.debug ("match - we call search the get the match")      
      return  self.search (s, mode, fullmatchMethod = True,  **kwargs)


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def finditer (self, s, mode = 'greedy', pos = 0, endpos = None, **kwargs):
        """
          Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in data. 
          The data is scanned left-to-right, and matches are returned in the order found. 
          #Empty matches are included in the result unless they touch the beginning of another match.
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.debug("CompiledPattern - finditer")

        endpos = len(s) if endpos == None else endpos
        if pos <0 or endpos < pos or endpos > len(s): return None
        if pos <0: pos = 0
        if endpos > len(s): endpos = len(s)
        if endpos < pos: return None

        # while parsing the data we parse and alter the nfa
        # each time the nfa did not match we reinit it by copying it from its original form 
        an_nfa = copy.deepcopy(self.nfa)       

        # in greedy mode, we do not stop the search after the first match
        # so we save the last successful configuration
        last_matched_nfa = None
        last_matched_i = -1
        last_matched_j = -1
        j = -1 # to process when data is empty
        #
        matcheslist = MatchesList()

        i = pos
        while i < endpos:           # i position in data   
            j = i      
            while j < endpos:       # j position in the current explored pattern 

                c = s[j]            # c current data token

                logging.debug ('-----------------------------------------------------')
                logging.debug ("finditer - nfa.step({}) data_index={} pattern_index={}".format(c, i, j))
                an_nfa.step(c, self.lexicons)

                if not len(an_nfa.cur_states):
                    logging.debug ('finditer - no more state to explore')

                    # greedy case
                    # if there was a backup we compute and create all the stuff with the current nfa
                    if last_matched_nfa != None:
                        logging.debug ("finditer - but a previously matched nfa so we will build the previously matched nfa")

                        # if we are here then it means we did a step too far
                        # the same for i and j
                        an_nfa.step_counter -= 1

                        # build results and update matchlist
                        if self.pattern_must_match_data_end:
                            logging.debug ("finditer - pattern_must_match_data_end so eventually we will build the result only if we are at the data end")

                            if last_matched_j +1 == endpos:
                                logging.debug ("finditer - we are at the data end, so we consume last_matched_nfa and build the result")
                                matcheslist = build_matching_result (last_matched_nfa, s, last_matched_i, last_matched_j, matcheslist)

                        else:
                            logging.debug ("finditer - we build the result")
                            matcheslist = build_matching_result (last_matched_nfa, s, last_matched_i, last_matched_j, matcheslist)

                        i = last_matched_j 
                        # j = last_matched_j # the next break will make j defined by i
                        last_matched_nfa = None
                        last_matched_i = -1
                        last_matched_j = -1       
 
                    # then we reinit so that next exploration starts after the end of the match
                    logging.debug ("finditer - either a result built from a previous matched nfa or a no successful nfa match ")
                    logging.debug ("finditer - reinit the nfa (last_matched_nfa = None and current_nfa restarts")
                    logging.debug ("finditer - break to start i+1 if unsuccessful or i = last_matched_j if previously matched nfa")

                    an_nfa = copy.deepcopy(self.nfa)

                    break

                if an_nfa.contains_matching_state():
                    logging.debug ("finditer - the nfa contains_matching_state")

                    if mode == 'greedy':
                        logging.debug ('finditer -we are in greedy mode')

                        if len(an_nfa.cur_states) >=2 or an_nfa.have_out_states():
                            # at least one nfa path which could be explored
                            logging.debug ("finditer - the nfa contains_matching_state but we are in greedy mode so we save the nfa")
                            logging.debug ("finditer - and pursue the exploration by directly jumping to the next j")

                            # we backup what do we need for computing and creating all the stuff
                            # and we pursue the pattern exploration
                            last_matched_nfa = copy.deepcopy(an_nfa)
                            last_matched_i = i
                            last_matched_j = j
                            j += 1

                            continue # we cut here and pursue the embedding loop at the next iteration
                        #else: 
                           # no more path to explore, so we stop here
                           # we compute and create all the stuff with the current nfa   
                    #else: 
                        # reluctant mode
                        # we compute and create all the stuff with the current nfa
                    logging.debug ('finditer - the current step ends the nfa (either no greedy or no more out_states) so we build_matching_result we the current nfa')

                    if self.pattern_must_match_data_end:
                        logging.debug ("finditer - pattern_must_match_data_end so eventually we will build the result only if we are at the data end")
                        if j +1 == endpos:
                            logging.debug ("finditer - we are at the data end, so we build the result")
                            matcheslist = build_matching_result (an_nfa, s,  i, j, matcheslist)
                    else:
                        logging.debug ("finditer - we build the result")
                        matcheslist = build_matching_result (an_nfa, s, i, j, matcheslist)

                    logging.debug ("finditer - reinit the nfa")
                    logging.debug ("finditer - if there was a previously saved nfa we reinit it too")
                    logging.debug ("finditer - break to start to i = j (ends of the current matched nfa)")
                    last_matched_nfa = None
                    last_matched_i = -1
                    last_matched_j = -1              
                    i = j
                    an_nfa = copy.deepcopy(self.nfa)
                    
                    break
                #print ("Debug: finditer -about to inc j and maybe i")

                j += 1    
            if last_matched_nfa != None and j == endpos:
                # to prevent from restarting to i+1 when incrementing j in greedy mode; indeed when j = len(s), then i +=1 and j = i 
                # the underlying idea in the greedy mode is that a larger matching nfa may be possible and we try to get it 
                logging.debug ("finditer - actually the next j does not exist (the data ends)")
                logging.debug ("finditer - but a previously matched nfa so we build the previous matched nfa")

                # if we are here then it means we did a step too far
                # the same for i and j
                an_nfa.step_counter -= 1.
                # build results and update matchlist
                matcheslist = build_matching_result (last_matched_nfa, s, last_matched_i, last_matched_j, matcheslist)

                i = last_matched_j 
                # the next break will make j defined by i
                last_matched_nfa = None
                last_matched_i = -1
                last_matched_j = -1       
 
                # then we reinit so that next exploration starts after the end of the match
                logging.debug ("finditer - reinit the nfa")
                logging.debug ("finditer - reinit i = last_matched_j")
                an_nfa = copy.deepcopy(self.nfa)    
            if self.pattern_must_match_data_start:
                logging.debug ("finditer - pattern_must_match_data_start and we were about to starting to explore new pattern at position 1 so we break here data exploration")
                break
            i += 1

        # greedy case
        # if there was a backup we compute and create all the stuff with the current nfa
        if last_matched_nfa != None:
            logging.debug ("finditer - no more data to explore and previously matched nfa so we build_matching_result")

            # if we are here then it means we did a step too far
            # the same for i and j
            an_nfa.step_counter -= 1.
            # build results and update matchlist
            matcheslist = build_matching_result (last_matched_nfa, s, last_matched_i, last_matched_j, matcheslist)
        else:
            # Warning we get here even when len(s) is 0
            last_matched_i = i
            last_matched_j = j



        if len(matcheslist)>0 :
            #matches = []
            #print ('Debug: matcheslist=',matcheslist)
            
            #print ('Debug: re finditer -final -  len(s)={} len(matcheslist)={} i={} j={}'.format(len(s), len(matcheslist), last_matched_i, last_matched_j))

            #if self.pattern_must_match_data_start and last_matched_i != 0:
            #    return None
            if self.pattern_must_match_data_end and last_matched_j +1 != endpos:
                logging.debug ("finditer - matcheslist but pattern_must_match_data_end and last_matched_j+1 does not correspond to the last data position so we return None")
                return None    

            logging.debug ("finditer - we return matcheslist")
            return matcheslist

        logging.debug ("finditer - no matcheslist we return None")

        return None


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def findall(self, s, **kwargs):
        """ Return all non-overlapping matches of pattern in data, as a list of data. 
      The data is scanned left-to-right, and matches are returned in the order found. 
      If one or more groups are present in the pattern, return a list of groups; 
      this will be a list of tuples if the pattern has more than one group. 
      Empty matches are included in the result unless they touch the beginning of another match.
      If the pattern contains start or/and end anchors, the method will work as search 
      and will return only matches at the beginning or end.
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.debug ("findall - we call finditer the get the matchlist")
        matcheslist = self.finditer(s, **kwargs)
        if matcheslist != None:
            matches = []
            for m in range(len(matcheslist)):
                #print ('Debug: lmatcheslist.group(m).group():',matcheslist.group(i).group())
                matches.append(matcheslist.group(m).group())
            return matches
        return None    



    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def annotate(self, annotation, data, group = [0], action = 'sub', iob = False, **kwargs):
        """
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.debug("CompiledPattern - annotate")

        prefix = ''

        #data_copy = list(data)
        data_copy = copy.deepcopy(data)

        if isinstance(annotation, dict):
          annotation = [annotation]

        iter = self.finditer(data, **kwargs) # greedy = True #reversed([finditer(pattern, data)])  
        if iter != None:
          size = 0
          for m in iter:
            for g in group:
              #print ('Debug: m={} g={} start={} end={}'.format(m, g, m.start(g), m.end(g)))
              if action == 'sub':
      #          data_copy[m.start(g):m.end(g)] = annotation
                data_copy[m.start(g)+size:m.end(g)+size] = annotation
                size +=  len(annotation) - (m.end(g) - m.start(g)) 

              elif action == 'update':
                if len(annotation) == 1:
                  for k in annotation[0].keys():
                    for r in range (m.start(g), m.end(g)):
                      if iob and r == m.start(g): 
                        prefix = PREFIX_BEGIN
                      elif iob: 
                        prefix = PREFIX_INSIDE
                      data_copy[r][k] = prefix + annotation[0][k]
                else:
                  for k in annotation[0].keys():
                    for r in range (m.start(g), m.end(g)):
                      if len(annotation) == (m.end(g) - m.start(g)): 
                        if iob and r == m.start(g): 
                          prefix = PREFIX_BEGIN
                        elif iob: 
                          prefix = PREFIX_INSIDE
                        data_copy[r][k] = prefix + annotation[0][k]
                      else: # Verbosity not the same size
                        data_copy = data                                # VIGILENCE data or list(data)
                        break

              elif action == 'extend':
                if len(annotation) == 1:
                  for k in annotation[0].keys():
                    for r in range (m.start(g), m.end(g)):
                      if k not in data_copy[r]:
                        if iob and r == m.start(g): 
                          prefix = PREFIX_BEGIN
                        elif iob: 
                          prefix = PREFIX_INSIDE
                        data_copy[r][k] = prefix+annotation[0][k]
                else:
                  for k in annotation[0].keys():
                    for r in range (m.start(g), m.end(g)):
                      if len(annotation) == (m.end(g) - m.start(g)):
                        if k not in data_copy[r]:
                          if iob and r == m.start(g): 
                            prefix = PREFIX_BEGIN
                          elif iob: 
                            prefix = PREFIX_INSIDE
                          data_copy[r][k] = prefix+annotation[0][k]
                      else: # Verbosity not the same size
                        data_copy = data                            # VIGILENCE data or list(data)
                        break       
        #print ('Debug: annotate - data={}'.format(data))
        #print ('Debug: annotate - data_copy={}'.format(data_copy))

        return data_copy


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
    def sub (self, repl, data, group = [0], **kwargs):
        """
        Return the data obtained by replacing the leftmost non-overlapping occurrences of 
        pattern matches or group of matches in data by the replacement repl. 
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.debug("CompiledPattern - sub")
        return self.annotate (repl, data, group, action = 'sub', iob = False, **kwargs)


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
    def subn (self, repl, data, **kwargs):
        """
        Perform the same operation as sub(), but return a tuple (new_string, number_of_subs_made).
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.warning("CompiledPattern - subn: Not implemented yet !")
        raise Exception ("Not implemented yet !")

    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
    def update (self, repl, data, group = [0], iob = False, **kwargs):
        """
        Return the data after updating (and extending) the features of a match or a group of a match 
        with the features of a dict or a sequence of dicts (of the same size as the group/match). 
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.debug("CompiledPattern - extend")
        return self.annotate (repl, data, group = group, action = 'update', iob = iob, **kwargs)


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
    def extend (self, repl, data, group = [0], iob = False, **kwargs):
        """
        Return the data after updating (and extending) the features of a match or a group of a match 
        with the features of a dict or a sequence of dicts (of the same size as the group/match). 
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.debug("CompiledPattern - extend")
        return self.annotate (repl, data, group = group, action = 'extend', iob = iob, **kwargs)


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def split(self, data, **kwargs):
        """
        """
        logging.debug('----------------------------------------------------------------------------------------------------------')
        logging.warning("CompiledPattern - split: Not implemented yet !")
        raise Exception ('Not implemented yet')


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def __repr__(self):
        return ''.join(['<pyrata.nfa CompiledPattern object; \n\tstarts_wi_data="',str(self.pattern_must_match_data_start),'"\n\tends_wi_data="',str(self.pattern_must_match_data_end),'"\n\tlexicon="',str(self.lexicons.keys()),'"\n\tnfa="\n',str(self.nfa),'\n">'])




class NFA(object):


    def __init__(self):
        logging.debug("NFA - create object")
        self.last_appended_state = State.create_start_state()[1]

        if DEBUG:
            self.states = set([self.last_appended_state])
            self.g = Graph()
            self.gf = self.g.new_vertex_property('bool')
            self.vp = {}
            start_v = self.g.add_vertex()
            self.vp[start_v] = self.last_appended_state
            self.vp[self.last_appended_state] = start_v
            self.gf[start_v] = True
            self.pos = None

        self.start_state = self.last_appended_state
        self.matching_state = None
        self.cur_states = set()


        self.step_counter = 0   # at each step a matching state

        self.step_os_is_leaf = dict() # at each step counter a dict of out_state id refering to 
                                    # one in_state [0], a leaf state [1], a pile_group [2] 
                                    # A leaf state is the normal state result of the substitution when the in_state is not normal
                                    # If the in_state is normal, the leaf state corresponds to the in_state
                                    # back sequence of the leaves informs about the current DFA

        self.states_dict = dict()   # each state referenced by its id

        self.last_state_id = -1     # state id of the last state matching #M   

    #if DEBUG:
    def draw(self, filename = "NFA.pdf"):
        self.g.set_vertex_filter(self.gf)
        v_text = self.g.new_vertex_property('string')
        vertex_fill_color = self.g.new_vertex_property('vector<float>')
        active_vertex_fill_color = [1.0000, 0.5216, 0.1216, 1]
        normal_vertex_fill_color = [0.0157, 0.6667, 0.9686, 1]
        vertex_color = self.g.new_vertex_property('vector<float>')
        active_vertex_color = [0.9843, 0.5882, 0.3098, 1]
        normal_vertex_color = [0.1294, 0.7216, 0.9961, 1]
        for v in self.g.vertices():
            v_text[v] = State.get_state_description(
                self.vp[v])
            vertex_fill_color[v] = active_vertex_fill_color if STEP and self.vp[
                v] in self.cur_states else normal_vertex_fill_color
            vertex_color[v] = active_vertex_color if STEP and self.vp[
                v] in self.cur_states else normal_vertex_color
        if self.pos:
            pos = self.pos
        else:
            pos = sfdp_layout(self.g)
        #output_size = 225 + 25 * self.g.num_vertices()
        output_size = 225 + 25 * self.g.num_vertices()
        output_size = (output_size, output_size)
        graph_draw(self.g, pos=pos, nodesfirst=True,
                   vertex_text=v_text,
                   vertex_font_size=6, #12
                   vertex_pen_width=1, #3
                   vertex_color=vertex_color,
                   vertex_fill_color=vertex_fill_color,
                   vertex_text_color=[1, 1, 1, 1],
                   edge_pen_width=1,
                   edge_marker_size=8, # 8
                  # edge_marker='circle',
                   edge_color=[0.6157, 0.6353, 0.6431, 1],
                   output_size=output_size,
                   output=filename)
        # the following allows further deep_copy
        del self.g
        del self.gf
        del self.vp
        del self.states
        del self.pos
        

    def elem(self):
        if self.matching_state:
            #print ('Debug: elem - self.matching_state.states_dict={}'.format(self.states_dict))                                
            return self.start_state, self.matching_state
        else:
            #print ('Debug: elem - self.last_appended_state.states_dict={}'.format(self.last_appended_state.states_dict))
            return self.start_state, self.last_appended_state

    def reset(self):
        self.cur_states = set([self.start_state])

    def have_out_states(self):
        for cs in self.cur_states:
            if len(cs.out_states) != 0: 
                return True
            return False


    def contains_matching_state(self):
        if self.matching_state in self.cur_states:
            return True
        for cs in self.cur_states:
            if self.__contains_matching_state(cs):
                return True
        return False

    def __contains_matching_state(self, state):
        if state == self.matching_state:
            return True
        else:
            if not state.is_normal():
                for os in state.out_states:
                    if self.__contains_matching_state(os):
                        return True
            return False

    def step(self, char, lexicons):
        logging.debug('NFA - step - step_counter={}'.format(self.step_counter))
        # consume char then add next states
        states_remove = set()
        states_add = set()

        for cs in self.cur_states:
            # print ('Debug: step \t\t\tid(cs)={}\tcs=\t{}'.format(cs.id, cs.char, cs)) 
            states_remove.add(cs)
            states_add.update(self.__step_special_state(char, None, cs, lexicons))
        # print ('Debug: step - cs=\t\t\t\t{} \nDebug: step minus states_remove=\t{} \nDebug: step plus states_add=\t\t{}'
        #     .format(self.cur_states, states_remove, states_add))    
        self.cur_states.difference_update(states_remove)
        self.cur_states.update(states_add)
        self.step_counter += 1
        # print ('Debug: step - new cs=\t\t\t{}'.format(self.cur_states))    


    def __step_special_state(self, char, previous_state, state, lexicons):
        states_add = set()
        logging.debug('NFA - __step_special_state - id(cs)={}\tstate={}'.format(state.id, state)) 

        if state.is_normal():

            # print ('Debug: __step_special_state - state is_normal, we evaluate it.') 

            # char evaluation
            # state.char is the current pattern element
            # char       is the current data element

            substitution_list = []
            step_evaluation = state.char == char
            if not (state.single_constraint_tuple_list == None) and state.char != '.':
                # evaluate each single constraint on the current data token
                single_constraint_evaluation_list = [evaluate_single_constraint(char, single_constraint_dict['name'], single_constraint_dict['operator'], single_constraint_dict['value'], lexicons) for single_constraint_dict in state.single_constraint_tuple_list]
                var_list = state.single_constraint_variable_list
                substitution_list = list(zip (var_list, single_constraint_evaluation_list))
                step_evaluation = state.symbolic_step_expression[0].subs(substitution_list)


            #if state.char == '.' or state.char == char:
            if state.char == '.' or step_evaluation:  
                #print ('Debug: __step_special_state - current char={} matches the state'.format(state.char))
                                  
                ps_id = -1 if previous_state == None  else previous_state.id                  
                
                # store the back reference to the in_state
                # the structure step_os_is_leaf will be used to build the actual matching DFA among the NFA
                for os in state.out_states:
                    #print ('Debug: __step_special_state - id(is)={}, since id(cs)={} matches, we will explore next step id(os)={} char(os)={}'
                    #  .format(ps_id, state.id, os.id, os.char))  

                    if self.step_counter in  self.step_os_is_leaf:
                        if os.id in self.step_os_is_leaf[self.step_counter]:
                            #print ('Debug: __step_special_state - WARNING - id(os)={} already present in self.step_os_is_leaf[{}]={}'.format(os.id, self.step_counter,self.step_os_is_leaf[self.step_counter]))
                            # exit()
                            self.step_os_is_leaf[self.step_counter][os.id].extend([ps_id, state.id, state.group_pile])
                        else:
                            self.step_os_is_leaf[self.step_counter][os.id] = []
                            self.step_os_is_leaf[self.step_counter][os.id].extend([ps_id, state.id, state.group_pile])
                    else:
                        self.step_os_is_leaf[self.step_counter] = dict()
                        self.step_os_is_leaf[self.step_counter][os.id] = []
                        self.step_os_is_leaf[self.step_counter][os.id].extend([ps_id, state.id, state.group_pile])
                    #print ('Debug: __step_special_state - at step={} we store the following association from id(os)={} to id(is)={} (with leaf/sub={})'
                    #  .format(self.step_counter, os.id, ps_id, state.id))
                    #print ('Debug: __step_special_state - so after extension={})'.format(self.step_os_is_leaf[self.step_counter]))


                    # patch
                    # I did not success to find when in building the NFA some state were lost 
                    # (not added in states_dict ; so I did not find where to add my storing code...)
                    # pattern=['raw="is"', '(', 'pos="JJ"', ')', 'pos="JJ"']
                    # But actually the state was not lost since it is mentioned in the run
                    # So I store it on fly now...
                    if not (os.id in self.states_dict):
                        # print('Debug: __step_special_state - id(cs)={} is absent from states_dict. Should have be added during NFA build ! We store now.'.format(state.id)) 
                        self.states_dict[os.id] = os
                    # else:
                    #   print ('Debug: __step_special_state - state.id={} already present registered_state={} and state={}'.format(os.id, self.states_dict[os.id], os))        
                    #   if os != self.states_dict[os.id]:
                    #     print ('Warning: __step_special_state - state.id={} already present but with a different registered state registered_state={} and state={}'.format(os.id, self.states_dict[os.id], os))        

                    if os.char == "#M":
                      #print ('Debug: __step_special_state - last_state_id={})'.format(os.id))
                      self.last_state_id = os.id
                # patch
                # I did not success to find when in building the NFA some state were lost 
                # (not added in states_dict ; so I did not find where to add my storing code...)
                # pattern=['raw="is"', '(', 'pos="JJ"', ')', 'pos="JJ"']
                # But actually the state was not lost since it is mentioned in the run
                # So I store it on fly now...
                if not (state.id in self.states_dict):
                    # print('Debug: __step_special_state - id(cs)={} is absent from states_dict. Should have be added during NFA build ! We store now.'.format(state.id)) 
                    self.states_dict[state.id] = state
                # else:
                #     print ('Debug: __step_special_state - state.id={} already present registered_state={} and state={}'
                #       .format(state.id, self.states_dict[state.id], state))        
   
                #     if state != self.states_dict[state.id]:
                #         print ('Warning: __step_special_state - state.id={} already present but with a different registered state registered_state={} and state={}'
                #           .format(state.id, self.states_dict[state.id], state))        

                #                 
                states_add.update(state.out_states)

                # print ('Debug: __step_special_state - state.group_pile={}'.format(state.group_pile))

            # else: print ('Debug: __step_special_state - current char did not match the state')
        else:
            for os in state.out_states:
                # print ('Debug: __step_special_state - state id(cs)={} is not_normal so we process instead id(os)={}'.format(state.id,os.id))  
                # patch
                # I did not success to find when in building the NFA some state were lost 
                # (not added in states_dict ; so I did not find where to add my storing code...)
                # pattern=['raw="is"', '(', 'pos="JJ"', ')', 'pos="JJ"']
                # But actually the state was not lost since it is mentioned in the run
                # So I store it on fly now...
                if not (state.id in self.states_dict):
                    # print('Debug: __step_special_state - id(cs)={} is absent from states_dict. Should have be added during NFA build ! We store now.'.format(state.id)) 
                    self.states_dict[state.id] = state
                # else:
                #     print ('Debug: __step_special_state - state.id={} already present registered_state={} and state={}'
                #       .format(state.id, self.states_dict[state.id], state))  
                #     if state != self.states_dict[state.id]:
                #       print ('Warning: __step_special_state - state.id={} already present but with a different registered state registered_state={} and state={}'
                #         .format(state.id, self.states_dict[state.id], state))        

                states_add.update(self.__step_special_state(char, state, os, lexicons))
        return states_add

    def append_element(self, elem):

        self.last_appended_state = self.append_B_to_A(
            (None, self.last_appended_state), elem)

        # store each state in a structure indexed by state ids
        #print ('Debug: append_element - states_dict={}'.format(self.states_dict))
        #print ('Debug: append_element - add in states_dict id()={}'.format(self.last_appended_state.id))  
        self.states_dict[self.last_appended_state.id] = self.last_appended_state

    def append_B_to_A(self, elem_A, elem_B):
        if DEBUG:
            merge_callback = self.__check_and_clear_in_states(elem_B[0])
        else:
            merge_callback = None

        _, last_appended_state = State.append_B_to_A(
            elem_A, elem_B, merge_callback=merge_callback)

        if DEBUG:
            self.__add_debug_info_from(elem_A[1])

        return last_appended_state

#if DEBUG:
    def __check_and_clear_in_states(self, state):
        if state in self.states:
            self.states.remove(state)
            v_state = self.vp.pop(state)
            self.vp.pop(v_state)
            self.g.clear_vertex(v_state)
            self.gf[v_state] = False

    def __add_debug_info_from(self, state):
        """Add necessary debug information from given state. Normally
        the given state should have already existed in current NFA. If
        it is not the case, the given state must have newly created to
        be preceding any other states. Then, the given state's debug
        information will be added as well.
        """
        if DEBUG:
            if state not in self.states:
                # state has no in_states
                new_v = self.g.add_vertex()
                self.vp[new_v] = state
                self.vp[state] = new_v
                self.gf[new_v] = True
                self.states.add(state)
            for ins in state.in_states:
                v_state = self.vp[state]
                if ins in self.states:
                    v_ins = self.vp[ins]
                    if not self.g.edge(v_ins, v_state):
                        self.g.add_edge(v_ins, v_state)
            cur_states = set([state])
            while len(cur_states) > 0:
                # needs to check and add the rest states
                next_states = set()
                for cs in cur_states:
                    for os in cs.out_states:
                        if os in self.states:
                            v_cs = self.vp[cs]
                            v_os = self.vp[os]
                            if not self.g.edge(v_cs, v_os):
                                self.g.add_edge(
                                    v_cs, v_os)
                        else:
                            new_v = self.g.add_vertex()
                            self.vp[new_v] = os
                            self.vp[os] = new_v
                            self.gf[new_v] = True
                            self.g.add_edge(self.vp[cs], new_v)
                            self.states.add(os)
                            next_states.add(os)
                cur_states = next_states

    def or_nfa(self, nfa):
        """Or NFA B to A (putting NFA B in parallel with NFA A)
            
        Connecting heads
        ================
        [A] and [B] are the start states of NFA A and B respectively.
        
                   +------ in_A ----
                   |
                   v
            [?]-->[A]---- out_A --->
             |
             +--->[B]---- out_B --->
                   ^
                   |
                   +------ in_B ----
        
        [B] can merge with [A] if after the merge, in_B cannot reach out_A
        and in_A cannot reach out_B, i.e. there is no going back 
        possibilities from either states after [B] to states after [A] or 
        states after [A] to states after [B].
        """
        A = self.start_state
        B = nfa.start_state
        if len(A.in_states) > 0 and len(B.in_states) > 0:
            # add [?] as the new start state and connect [?] to both [A]
            # and [B]
            A.char = State.EMPTY_STATE
            B.char = State.EMPTY_STATE
            new_start_elem = State.create_char_state('T', None, None, None, [])
            self.append_B_to_A(new_start_elem, self.elem())
            self.append_B_to_A(new_start_elem, nfa.elem())
            new_start_elem[1].char = State.START_STATE
            self.start_state = new_start_elem[1]
        elif len(A.in_states) > 0:
            # turn [B] to the new start state and append [A] to [B]
            A.char = State.EMPTY_STATE
            self.append_B_to_A((None, B), self.elem())
            self.start_state = B
        else:
            # append [B] to [A] or merge [B] into [A]
            B.char = State.EMPTY_STATE
            self.append_B_to_A((None, A), nfa.elem())
        """
        Connecting tails
        ================
        [A] is the tail state of NFA A.
        [B] is the matching states of NFA B.

                 <----- out_A ----+
                                  |
                 ------ in_A --->[A]--->[?]
                                         ^
                                         |
                 ------ in_B --->[B]-----+
                                  |
                 <----- out_B ----+

        [B] can merge with [A] if after the merge, in_B cannot reach out_A
        and in_A cannot reach out_B, i.e. there is no going back 
        possibilities from either states before [B] to states before [A] or
        states before [A] to states before [B].
        """
        A = self.last_appended_state
        B = nfa.matching_state
        if (len(A.out_states) > 0 or A.is_normal()) and len(B.out_states) > 0:
            # add [?] as the new matching state and connect both [A] and
            # [b] to [?]
            B.char = State.EMPTY_STATE
            new_empty_elem = State.create_char_state('T', None, None, None, [])
            self.last_appended_state = self.append_B_to_A(
                (None, A), new_empty_elem)
            self.append_B_to_A((None, B), new_empty_elem)
            new_empty_elem[1].char = State.EMPTY_STATE
        elif len(A.out_states) > 0 or A.is_normal():
            # append [B] to [A]
            B.char = State.EMPTY_STATE
            self.last_appended_state = self.append_B_to_A(
                (None, A), (B, B))
        else:
            # append [A] to [B] or merge [A] into [B]
            B.char = State.EMPTY_STATE
            self.last_appended_state = self.append_B_to_A(
                (None, B), (A, A))

        # store each state in a structure indexed by state ids
        self.states_dict[self.last_appended_state.id] = self.last_appended_state    

    def finalise_nfa(self):
        if not self.last_appended_state:
            raise CompiledPattern.NFAHasAlreadyBeenFinalisedError

        new_matching_elem = State.create_matching_state()
        self.matching_state = self.append_B_to_A(
            (None, self.last_appended_state), new_matching_elem)

        # store each state in a structure indexed by state ids
        #print ('Debug: finalise_nfa - states_dict={}'.format(self.states_dict))
        #print ('Debug: finalise_nfa - add in states_dict id()={}'.format(self.matching_state.id))  
        self.states_dict[self.matching_state.id] = self.matching_state

        self.cur_states = set([self.start_state])
        self.last_appended_state = None

        if DEBUG:
            self.pos = sfdp_layout(self.g)

    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def __repr__(self):

  
        states_dict_values_set = set(self.states_dict.values())
        states_dict_values_set.add(str(self.start_state))

        return ''.join(['<pyrata.nfa NFA object; \n\tstates="',str(states_dict_values_set),'">'])


class NFAHasAlreadyBeenFinalisedError(Exception):
    pass



#if __name__ == '__main__':
#