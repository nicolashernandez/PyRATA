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

"""NFA object """

import sys
import logging

from pyrata.state import *

import re

#if DEBUG:
#  from graph_tool.all import *

try:
    from graph_tool.all import *
except ImportError:
    DEBUG=False
else: 
    DEBUG = True
#DEBUG = False
#STEP = False




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
class NFA(object):


    def __init__(self):
        logging.debug("NFA - create object")
        self.last_appended_state = State.create_start_state()[1]
        #print ('Debug: type(self.last_appended_state)={}'.format(type(self.last_appended_state)))
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

    if DEBUG:
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
            #print ('Debug: step \t\t\tid(cs)={}\tcs=\t{}'.format(cs.id, cs.char, cs)) 
            states_remove.add(cs)
            states_add.update(self.__step_special_state(char, None, cs, lexicons))
        # print ('Debug: step - cs=\t\t\t\t{} \nDebug: step minus states_remove=\t{} \nDebug: step plus states_add=\t\t{}'
        #     .format(self.cur_states, states_remove, states_add))    
        self.cur_states.difference_update(states_remove)
        self.cur_states.update(states_add)
        self.step_counter += 1
        # print ('Debug: step - new cs=\t\t\t{}'.format(self.cur_states))    

    # @profile
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
                # print ('Debug: state.single_constraint_tuple_list {}'.format(state.single_constraint_tuple_list))
                # print ('Debug: single_constraint_evaluation_list {}'.format(single_constraint_evaluation_list))
                # print ('Debug: state.single_constraint_variable_list {}'.format(state.single_constraint_variable_list))
                # print ('Debug: substitution_list {}'.format(substitution_list))
                # print ('Debug: state.symbolic_step_expression[0] {}'.format(state.symbolic_step_expression[0]))
                
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

    if DEBUG:
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


    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def __deepcopy__(self, memodict={}):
        copy_object = NFA()
        #copy_object.value = self.value
        copy_object.last_appended_state = self.last_appended_state
        # #print ('Debug: type(self.last_appended_state)={}'.format(type(self.last_appended_state)))
        # if DEBUG:
        #     self.states = set([self.last_appended_state])
        #     self.g = Graph()
        #     self.gf = self.g.new_vertex_property('bool')
        #     self.vp = {}
        #     start_v = self.g.add_vertex()
        #     self.vp[start_v] = self.last_appended_state
        #     self.vp[self.last_appended_state] = start_v
        #     self.gf[start_v] = True
        #     self.pos = None

        copy_object.start_state = self.start_state 
        copy_object.matching_state = self.matching_state # = None
        copy_object.cur_states = self.cur_states.copy() # = set()


        copy_object.step_counter = self.step_counter # = 0   # at each step a matching state

        copy_object.step_os_is_leaf = self.step_os_is_leaf.copy() # = dict() # at each step counter a dict of out_state id refering to 
                                    # one in_state [0], a leaf state [1], a pile_group [2] 
                                    # A leaf state is the normal state result of the substitution when the in_state is not normal
                                    # If the in_state is normal, the leaf state corresponds to the in_state
                                    # back sequence of the leaves informs about the current DFA

        copy_object.states_dict = self.states_dict.copy() # = dict()   # each state referenced by its id

        copy_object.last_state_id = self.last_state_id 
        return copy_object

class NFAHasAlreadyBeenFinalisedError(Exception):
    pass



#if __name__ == '__main__':
#