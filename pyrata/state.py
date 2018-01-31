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

""" Description of the NFA elementary object namely as the state"""
import logging

class State(object):
    START_STATE = '#S'
    MATCHING_STATE = '#M'
    EMPTY_STATE = '#E'
    
    class_counter = 0      # make each State object have a unique id

    @classmethod
    def get_state_description(cls, state):
        if state.char == cls.START_STATE:
            return '({}) START'.format(state.id)
        elif state.char == cls.MATCHING_STATE:
            return '({}) MATCHING'.format(state.id)
        elif state.char == cls.EMPTY_STATE:
            return '({}) EMPTY'.format(state.id)
        else:
            return '({}) {}'.format(state.id,state.char)


    def __init__(self, char, in_states, out_states, symbolic_step_expression, single_constraint_tuple_list, single_constraint_variable_list, group_pile):
        self.char = char
        self.in_states = in_states
        self.out_states = out_states
        self.symbolic_step_expression = symbolic_step_expression
        self.single_constraint_tuple_list = single_constraint_tuple_list
        self.single_constraint_variable_list = single_constraint_variable_list
        self.group_pile = group_pile            # list of group id currently open at this point
        self.id = State.class_counter           # unique id for this State
        State.class_counter += 1
        logging.debug('State - create object - char={} id={} self={}'.format(char, self.id, self))
        # print ('Debug: State type(self.char)={}'.format(self.char))
        # print ('Debug: State type(self.in_states)={}'.format(self.in_states))
        # print ('Debug: State type(self.symbolic_step_expression)={}'.format(self.symbolic_step_expression))
        # print ('Debug: State type(self.single_constraint_tuple_list)={}'.format(self.single_constraint_tuple_list))
        # print ('Debug: State type(self.single_constraint_variable_list)={}'.format(self.single_constraint_variable_list))
        # print ('Debug: State type(self.group_pile)={}'.format(self.group_pile))
        # print ('Debug: State type(self.id)={}'.format(self.id))
 


    def is_start(self):
        return self.char == self.START_STATE

    def is_matching(self):
        return self.char == self.MATCHING_STATE

    def is_empty(self):
        return self.char == self.EMPTY_STATE

    def is_normal(self):
        return (not self.is_start() and
                not self.is_matching() and
                not self.is_empty())

    @classmethod
    def create_start_state(cls):
        new_state = cls(cls.START_STATE, set(), set(), None, None, None, [])
        return new_state, new_state

    @classmethod
    def create_matching_state(cls):
        new_state = cls(cls.MATCHING_STATE, set(), set(), None, None, None, [])
        return new_state, new_state

    @classmethod
    def create_empty_state(cls):
        new_state = cls(cls.EMPTY_STATE, set(), set(), None, None, None, [])
        return new_state, new_state

    @classmethod
    def create_char_state(cls, char, symbolic_step_expression, single_constraint_tuple_list, single_constraint_variable_list, group_pile):

        new_state = cls(char, set(), set(), symbolic_step_expression, single_constraint_tuple_list, single_constraint_variable_list, group_pile)
        return new_state, new_state

    @classmethod
    def append_B_to_A(cls, elem_A, elem_B, merge_callback=None):
        """Append element B to A and return the last state of the combined
        element 
        
        [A] and [B] are the end and start state of element A and B
        respectively
        
                                  +------ in_B ----
             <-- out_A --+        |
                         |        v
             -- in_A -->[A]----->[B]----- out_B -->
        
        
        [A] can merge with [B] if either [A] or [B] is empty and
        after the merge, in_B cannot reach out_A, i.e. there is no
        going back possibilities from states after [B] to states
        before [A]. If [A] is start state, don't merge.
        """
        A = elem_A[1]
        B = elem_B[0]
        last_state = elem_B[1]
        if not ((A.is_start() and (
                B.is_normal() or B.is_matching())) or (
                A.is_normal() and (
                B.is_matching() or B.is_normal()))) and (
                (len(A.out_states) == 0 and not A.is_normal()) or (len(B.in_states) == 0 and not B.is_normal())):
            if A.is_empty():
                A.char = B.char
                A.symbolic_step_expression = B.symbolic_step_expression
                A.single_constraint_tuple_list = B.single_constraint_tuple_list
                A.single_constraint_variable_list = B.single_constraint_variable_list 
                A.group_pile = B.group_pile
                A.id = B.id                     
            A.out_states.discard(B)
            B.in_states.discard(A)

            A.out_states.update(B.out_states)

            for ous in B.out_states:
                ous.in_states.discard(B)
                ous.in_states.add(A)

            A.in_states.update(B.in_states)

            for ins in B.in_states:
                ins.out_states.discard(B)
                ins.out_states.add(A)

            if elem_B[0] == elem_B[1]:
                last_state = A

            if merge_callback:
                merge_callback()
        else:
            A.out_states.add(B)
            B.in_states.add(A)

        return elem_A[0], last_state

    @classmethod
    def create_element_star_state(cls, elem):
        facade_elem = cls.create_start_state()
        final_elem = cls.append_B_to_A(facade_elem, elem)
        facade_elem[1].char = cls.MATCHING_STATE
        final_elem = cls.append_B_to_A(final_elem, facade_elem)
        final_elem[1].char = cls.EMPTY_STATE
        return final_elem[1], final_elem[1]

    @classmethod
    def create_element_plus_state(cls, elem):
        if len(elem[0].out_states) == 1:
            os = elem[0].out_states.pop()
            tmp_elem = cls.append_B_to_A((elem[0], elem[0]), (os, os))
            if tmp_elem[1] != elem[0]:
                elem[0].out_states.add(os)

        if len(elem[1].in_states) == 1:
            ins = elem[1].in_states.pop()
            tmp_elem = cls.append_B_to_A((ins, ins), (elem[1], elem[1]))
            if tmp_elem[1] == elem[1]:
                elem[1].in_states.add(ins)
            else:
                elem = (elem[0], tmp_elem[1])

        elem[1].out_states.add(elem[0])
        elem[0].in_states.add(elem[1])

        return elem

    @classmethod
    def create_element_question_mark_state(cls, elem):
        new_start_elem = cls.create_start_state()
        new_end_elem = cls.create_matching_state()
        final_elem = cls.append_B_to_A(new_start_elem, elem)
        final_elem = cls.append_B_to_A(final_elem, new_end_elem)
        final_elem = cls.append_B_to_A(
            (final_elem[0], final_elem[0]), (final_elem[1], final_elem[1]))
        final_elem[0].char = cls.EMPTY_STATE
        final_elem[1].char = cls.EMPTY_STATE
        return final_elem

    def __str__(self):
        return 'IN[%s]->CHAR(%s)->OUT[%s]' % (','.join([s.char for s in self.in_states]), self.char, ','.join([s.char for s in self.out_states]))

    def __repr__(self):
        return "'%s'" % self