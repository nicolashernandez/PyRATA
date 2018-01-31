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
#
# SET in __main__, the logging level
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import logging
import pyrata.re
import pyrata.match
import pyrata.state

import unittest
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class PyrataReTest(unittest.TestCase):
  """Test cases used for testing methods of the 're' module."""


  # # ----------------------------------------------------------------------
  # def test_findall_pattern_wi_syntax_error_in_it(self):
  #   """Test findall pattern with syntax error in it"""
  #   pattern = '[pos~"NN.*" | pos="JJ"]* blabla pos~"NN.*"'
  #   data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
  #   expected = None
  #   result = pyrata.re.findall(pattern, data)
  #   self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_search_step(self):
    """Test search method with a simple step pattern. The pattern fires at some points."""
    pattern = 'pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'JJ', 'raw': 'fast'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_search_step_only_present_at_the_data_start(self):
    """Test search method with a simple step pattern. The pattern fires at the data start."""
    pattern = 'foo="bar"'
    data = [{'pos': 'PRP', 'raw': 'It', 'foo':'bar'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'PRP', 'raw': 'It', 'foo':'bar'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_search_step_only_present_at_the_data_end(self):
    """Test search method with a simple step pattern. The pattern fires at the data end."""
    pattern = 'foo="bar"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata', 'foo':'bar'}]
    expected = [{'pos': 'NNP', 'raw': 'Pyrata', 'foo':'bar'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)    

  # ----------------------------------------------------------------------
  def test_search_step_absent_from_data(self):
    """Test search method with a simple step pattern. The pattern is not present in the data."""
    pattern = 'foo="bar"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_findall_step(self):
    """Test findall method with a simple step pattern. The pattern fires several times in the data."""
    pattern = 'pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  #def (self):
  # TODO findall with pattern at various position start middle and end

  # ----------------------------------------------------------------------
  def test_findall_step_absent_from_data(self):
    """Test findall method with a simple step pattern. The pattern is not present in the data."""
    pattern = 'foo="bar"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_finditer_step(self):
    """Test finditer method with a simple step pattern. The pattern matches several times the data."""
    pattern = 'pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    matcheslist = pyrata.match.MatchesList()  
    matcheslist.append(pyrata.match.Match (start=2, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}]))
    matcheslist.append(pyrata.match.Match (start=3, end=4, value=[{'pos': 'JJ', 'raw': 'easy'}]))
    matcheslist.append(pyrata.match.Match (start=5, end=6, value=[{'pos': 'JJ', 'raw': 'funny'}]))
    matcheslist.append(pyrata.match.Match (start=8, end=9, value=[{'pos': 'JJ', 'raw': 'regular'}]))
    expected = matcheslist
    result = pyrata.re.finditer(pattern, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_match_step(self):
    """Test match method with a simple step pattern. The pattern is present at the beginning."""
    pattern = 'pos="PRP"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'PRP', 'raw': 'It'}]
    result = pyrata.re.match(pattern, data)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_match_step_not_present_at_the_beginning(self):
    """Test match method with a simple step pattern. The pattern is not present at the beginning."""
    pattern = 'pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.match(pattern, data)
    self.assertEqual(result,expected)


  # ----------------------------------------------------------------------
  def test_match_quantified_wildcard(self):
    """Test match method with a quantified wildcard. The pattern is present at the beginning."""
    pattern = '.*'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.match(pattern, data)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_match_sequence_not_present_at_the_beginning(self):
    """Test match method with a sequence. The pattern is not present at the beginning."""
    pattern = 'pos="JJ" raw="easy"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.match(pattern, data)
    self.assertEqual(result,expected)


  # ----------------------------------------------------------------------
  def test_search_quantified_wildcard_wi_search(self):
    """Test search method with a sequence. The pattern matches the data."""
    pattern = '.*'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)


# --------------------------------------------------------------------------------------
# compiled version of re methods 
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_search_compiled_step(self):
    """Test search method with a compiled step pattern. The pattern fires at some points."""
    pattern = 'pos="JJ"'
    compiled_pattern = pyrata.re.compile(pattern)
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'JJ', 'raw': 'fast'}]
    result = compiled_pattern.search(data)
    self.assertEqual(result.group(),expected)


  # ----------------------------------------------------------------------
  def test_finditer_compiled_step(self):
    """Test finditer method with a compiled step pattern. The pattern matches several times the data."""
    pattern = 'pos="JJ"'
    compiled_pattern = pyrata.re.compile(pattern)
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    matcheslist = pyrata.match.MatchesList()  
    matcheslist.append(pyrata.match.Match (start=2, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}]))
    matcheslist.append(pyrata.match.Match (start=3, end=4, value=[{'pos': 'JJ', 'raw': 'easy'}]))
    matcheslist.append(pyrata.match.Match (start=5, end=6, value=[{'pos': 'JJ', 'raw': 'funny'}]))
    matcheslist.append(pyrata.match.Match (start=8, end=9, value=[{'pos': 'JJ', 'raw': 'regular'}]))
    expected = matcheslist
    result = compiled_pattern.finditer(data)
    self.assertEqual(result, expected)



# --------------------------------------------------------------------------------------
# fullmatch method with various maching conditions i.e. data matching fully/partially (at the beginning/end) or not 
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_fullmatch_quantified_wildcard(self):
    """Test fullmatch method with a sequence. The pattern matches the data."""
    pattern = '.*'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.fullmatch(pattern, data)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_fullmatch_sequence_matching_from_beginning_to_end_the_data(self):
    """Test fullmatch method matching from beginning to end the data."""
    pattern = 'pos="VBZ" raw="easy"'
    data = [ {'pos': 'VBZ', 'raw': 'is'},  {'pos': 'JJ', 'raw': 'easy'}]
    expected = [ {'pos': 'VBZ', 'raw': 'is'},  {'pos': 'JJ', 'raw': 'easy'}]
    result = pyrata.re.fullmatch(pattern, data)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_fullmatch_sequence_matching_only_the_beginning_of_the_data(self):
    """Test fullmatch method matching from beginning to end the data."""
    pattern = 'pos="VBZ" raw="easy"'
    data = [ {'pos': 'VBZ', 'raw': 'is'},  {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}]
    expected = None
    result = pyrata.re.fullmatch(pattern, data)
    self.assertEqual(result,expected)

      # ----------------------------------------------------------------------
  def test_fullmatch_sequence_matching_only_the_end_of_the_data(self):
    """Test fullmatch method matching from beginning to end the data."""
    pattern = 'pos="VBZ" raw="easy"'
    data = [ {'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'},  {'pos': 'JJ', 'raw': 'easy'}]
    expected = None
    result = pyrata.re.fullmatch(pattern, data)
    self.assertEqual(result,expected)



# --------------------------------------------------------------------------------------
# test empty pattern wi all the matching methods 
# --------------------------------------------------------------------------------------


  # ----------------------------------------------------------------------
  def test_search_wi_empty_pattern(self):
    """Test search method with an empty pattern. The data is not empty."""
    pattern = ''
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result,expected)
  # ----------------------------------------------------------------------
  def test_match_wi_empty_pattern(self):
    """Test match method with an empty pattern. The data is not empty."""
    pattern = ''
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.match(pattern, data)
    self.assertEqual(result,expected)
  # ----------------------------------------------------------------------
  def test_fullmatch_wi_empty_pattern(self):
    """Test fullmatch method with an empty pattern. The data is not empty."""
    pattern = ''
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.fullmatch(pattern, data)
    self.assertEqual(result,expected)

  # ----------------------------------------------------------------------
  def test_findall_wi_empty_pattern(self):
    """Test findall method with an empty pattern. The data is not empty."""
    pattern = ''
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result,expected)
  # ----------------------------------------------------------------------
  def test_finditer_wi_empty_pattern(self):
    """Test finditer method with an empty pattern. The data is not empty."""
    pattern = ''
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.finditer(pattern, data)
    self.assertEqual(result,expected)


# --------------------------------------------------------------------------------------
# test all sort of elements
# --------------------------------------------------------------------------------------



  # ----------------------------------------------------------------------
  def test_search_class_step(self):
    """Test search method with a class step pattern. The class is present present in the data."""
    pattern = '[pos="VBZ"]'
    #data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    #expected = [ {'raw':'are', 'lem':'be', 'pos':'VB'}]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, 
      {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, 
      {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, 
      {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'VBZ', 'raw': 'is'}]   
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)    

  # ----------------------------------------------------------------------
  def test_search_complex_class_step_(self):
    """Test search method with a complex class step pattern. The class is present present in the data."""
    pattern = '[(pos="VB" | pos="VBZ") & !raw="is"]'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, 
      {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, 
      {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, 
      {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'VB', 'raw': 'write'}]   
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)    


  # ----------------------------------------------------------------------
  def test_findall_regex_step(self):
    """Test findall method with a regex step pattern. The pattern is present in the data."""

    pattern = 'pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'NNP', 'raw': 'Pyrata'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_findall_lexicon_step(self):
    """Test findall method with a step pattern declaring a lexicon constraint. The pattern is present in the data."""
    lexicons = {'positiveLexicon':['easy', 'funny']}
    pattern = 'raw@"positiveLexicon"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}]]
    result = pyrata.re.findall(pattern, data, lexicons=lexicons)
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_findall_undefined_lexicon_step(self):
    """Test findall method with a step pattern declaring a lexicon constraint but no lexicons. The pattern is present in the data."""
    pattern = 'raw@"positiveLexicon"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_findall_multiple_lexicon_step(self):
    """Test findall method with a step pattern declaring multiple lexicon constraints with multiple lexicons. The pattern is present in the data."""
    lexicons = {'positiveLexicon':['easy', 'funny'], 'negativeLexicon':['fast', 'regular']}
    pattern = '[raw@"positiveLexicon" | raw@"negativeLexicon"]'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'fast'}], [ {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}],[ {'pos': 'JJ', 'raw': 'regular'}]]
    result = pyrata.re.findall(pattern, data, lexicons=lexicons)
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_findall_wildcard_step(self):
    """Test findall method with a step pattern declaring a lexicon constraint but no lexicons. The pattern is present in the data."""
    pattern = '.'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'PRP', 'raw': 'It'}], [{'pos': 'VBZ', 'raw': 'is'}], [{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'CC', 'raw': 'and'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'TO', 'raw': 'to'}], [{'pos': 'VB', 'raw': 'write'}], [{'pos': 'JJ', 'raw': 'regular'}], [{'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'IN', 'raw': 'with'}],[{'pos': 'NNP', 'raw': 'Pyrata'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_search_optional_step(self):
    """Test search method with an optional step pattern. The pattern is present in the data."""
    # echo 1 | perl -ne '$s = "abcbdb"; if ($s =~ /b?/) {print "matched>$1<\n";} else {print "unmatched\n"}'
    # echo 1 | perl -ne '$s = "abcbdb"; if ($s =~ /e?/) {print "matched>$1<\n";} else {print "unmatched\n"}'
    # both return matche but wo any character
    pattern = 'pos="JJ"?'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'raw': 'fast', 'pos': 'JJ'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected) 

  # ----------------------------------------------------------------------
  def test_findall_optional_step(self):
    """Test findall method with an optional step pattern. The pattern is present in the data."""
    # echo 1 | perl -ne '$s = "abcbdb"; if ($s =~ /b?/) {print "matched>$1<\n";} else {print "unmatched\n"}'
    # echo 1 | perl -ne '$s = "abcbdb"; if ($s =~ /e?/) {print "matched>$1<\n";} else {print "unmatched\n"}'
    # both return matche but wo any character
    pattern = 'pos="JJ"?'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_findall_sequence(self):
    """Test findall method with a step sequence pattern. The pattern is present in the data."""
    pattern = 'pos="JJ" pos="NNS"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_findall_sequence_wi_wildcard(self):
    """Test findall method with a step sequence pattern. The pattern is present in the data."""
    pattern = '. pos="NNS"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected) 



# --------------------------------------------------------------------------------------
# test pos/endpos  
# --------------------------------------------------------------------------------------


  # ----------------------------------------------------------------------
  def test_match_step_pos_present(self):
    """Test match method at a given pos."""
    pattern = 'raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [ {'pos': 'VBZ', 'raw': 'is'}]
    result = pyrata.re.match(pattern, data, pos = 1)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_match_step_pos_and_endpos_present(self):
    """Test match method at a given pos and endpos."""
    pattern = 'raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [ {'pos': 'VBZ', 'raw': 'is'}]
    result = pyrata.re.match(pattern, data, pos = 1, endpos=2)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_search_step_pos_present(self):
    """Test search method at a given pos."""
    pattern = 'raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [ {'pos': 'VBZ', 'raw': 'is'}]
    result = pyrata.re.search(pattern, data, pos = 1)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_search_step_pos_and_endpos_present(self):
    """Test search method at a given pos and endpos."""
    pattern = 'raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [ {'pos': 'VBZ', 'raw': 'is'}]
    result = pyrata.re.search(pattern, data, pos = 1, endpos=2)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_findall_step_pos_present(self):
    """Test findall method at a given pos."""
    pattern = 'raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'VBZ', 'raw': 'is'}]]
    result = pyrata.re.findall(pattern, data, pos = 1)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_findall_step_pos_and_endpos_present(self):
    """Test findall method at a given pos and endpos."""
    pattern = 'raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'VBZ', 'raw': 'is'}]]
    result = pyrata.re.findall(pattern, data, pos = 1, endpos=2)
    self.assertEqual(result,expected)



  # ----------------------------------------------------------------------
  def test_search_step_endpos_present(self):
    """Test search method that ends at endpos. Data is present"""
    pattern = 'raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [ {'pos': 'JJ', 'raw': 'fast'}]
    result = pyrata.re.search(pattern, data,  endpos=3)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_search_step_endpos_not_present(self):
    """Test search method that ends at endpos. Data is not present"""
    pattern = 'raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data,  endpos=1)
    self.assertEqual(result,expected)



  # ----------------------------------------------------------------------
  def test_match_step_endpos_present(self):
    """Test search method that ends at endpos. Data is present"""
    pattern = 'raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data,  endpos=2)
    self.assertEqual(result,expected)

  # ----------------------------------------------------------------------
  def test_match_step_endpos_not_present(self):
    """Test search method that ends at endpos. Data is not present"""
    pattern = 'raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data,  endpos=1)
    self.assertEqual(result,expected)

  # ----------------------------------------------------------------------
  def test_match_step_endpos_gt_len_data_present(self):
    """Test search method that ends at endpos gt than len data. Data is present"""
    pattern = 'raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'JJ', 'raw': 'fast'}]
    result = pyrata.re.search(pattern, data,  endpos=100)
    self.assertEqual(result.group(),expected)





  # ----------------------------------------------------------------------
  def test_search_step_negative_pos(self):
    """Test search method at a negative pos."""
    pattern = 'raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'VBZ', 'raw': 'is'}]
    result = pyrata.re.search(pattern, data, pos = -20)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_search_step_pos_gt_endpos(self):
    """Test search method at a pos greater than a endpos."""
    pattern = 'raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data, pos = 1, endpos = 0)
    self.assertEqual(result,expected)



# --------------------------------------------------------------------------------------
# aa in caaaab greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_aa_in_caaaad(self):
    """Test greedy search aa_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = 'pos="JJ" pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_aa_in_caaaad(self):
    """Test reluctant search aa_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = 'pos="JJ" pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_aa_in_caaaad(self):
    """Test greedy findall aa_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = 'pos="JJ" pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_aa_in_caaaad(self):
    """Test reluctant findall aa_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = 'pos="JJ" pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_aa_in_caaaad(self):
    """Test greedy finditer aa_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = 'pos="JJ" pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'} ]))
    expected.append(pyrata.match.Match (start=3, end=5, value=[{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_aa_in_caaaad(self):
    """Test reluctant finditer aa_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = 'pos="JJ" pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'} ]))
    expected.append(pyrata.match.Match (start=3, end=5, value=[{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   



# --------------------------------------------------------------------------------------
# dot_a_in_caaaab greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_dot_a_in_caaaad(self):
    """Test greedy search dot_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  '. pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = '. pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=0, end=2, value=[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_dot_a_in_caaaad(self):
    """Test reluctant search dot_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  '. pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = '. pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=0, end=2, value=[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_dot_a_in_caaaad(self):
    """Test greedy findall dot_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  '. pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = '. pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_dot_a_in_caaaad(self):
    """Test reluctant findall dot_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  '. pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = '. pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_dot_a_in_caaaad(self):
    """Test greedy finditer dot_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  '. pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = '. pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=0, end=2, value=[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}]))
    expected.append(pyrata.match.Match (start=2, end=4, value=[{'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_dot_a_in_caaaad(self):
    """Test reluctant finditer dot_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  '. pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = '. pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=0, end=2, value=[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}]))
    expected.append(pyrata.match.Match (start=2, end=4, value=[{'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   


# --------------------------------------------------------------------------------------
# a_star_a_in_caaaad greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_a_star_a_in_caaaad(self):
    """Test greedy search wi a_star_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"* pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = 'pos="JJ"* pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=5, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_a_star_a_in_caaaad(self):
    """Test reluctant search wi a_star_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"* pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = 'pos="JJ"* pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=2, value=[{'pos': 'JJ', 'raw': 'fast'}])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_a_star_a_in_caaaad(self):
    """Test greedy findall wi a_star_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"* pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = 'pos="JJ"* pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_a_star_a_in_caaaad(self):
    """Test reluctant findall wi a_star_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"* pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = 'pos="JJ"* pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_a_star_a_in_caaaad(self):
    """Test greedy finditer wi a_star_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"* pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = 'pos="JJ"* pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=5, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_a_star_a_in_caaaad(self):
    """Test reluctant finditer wi a_star_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"* pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = 'pos="JJ"* pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=2, value=[ {'pos': 'JJ', 'raw': 'fast'} ]))
    expected.append(pyrata.match.Match (start=2, end=3, value=[ {'pos': 'JJ', 'raw': 'easy'} ]))
    expected.append(pyrata.match.Match (start=3, end=4, value=[ {'pos': 'JJ', 'raw': 'funny'} ]))
    expected.append(pyrata.match.Match (start=4, end=5, value=[ {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   



# --------------------------------------------------------------------------------------
# a_option_a_in_caaaad greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_a_option_a_in_caaaad(self):
    """Test greedy search wi a_option_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"? pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = 'pos="JJ"? pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_a_option_a_in_caaaad(self):
    """Test reluctant search wi a_option_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"? pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = 'pos="JJ"? pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=2, value=[{'pos': 'JJ', 'raw': 'fast'}])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_a_option_a_in_caaaad(self):
    """Test greedy findall wi a_option_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"? pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = 'pos="JJ"? pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_a_option_a_in_caaaad(self):
    """Test reluctant findall wi a_option_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"? pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = 'pos="JJ"? pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_a_option_a_in_caaaad(self):
    """Test greedy finditer wi a_option_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"? pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = 'pos="JJ"? pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}]))
    expected.append(pyrata.match.Match (start=3, end=5, value=[{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_a_option_a_in_caaaad(self):
    """Test reluctant finditer wi a_option_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"? pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = 'pos="JJ"? pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=2, value=[ {'pos': 'JJ', 'raw': 'fast'} ]))
    expected.append(pyrata.match.Match (start=2, end=3, value=[ {'pos': 'JJ', 'raw': 'easy'} ]))
    expected.append(pyrata.match.Match (start=3, end=4, value=[ {'pos': 'JJ', 'raw': 'funny'} ]))
    expected.append(pyrata.match.Match (start=4, end=5, value=[ {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   


# --------------------------------------------------------------------------------------
# a_plus_a_in_caaaad greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_a_plus_a_in_caaaad(self):
    """Test greedy search wi  a_plus_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"+ pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = 'pos="JJ"+ pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=5, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_a_plus_a_in_caaaad(self):
    """Test reluctant search wi a_plus_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"+ pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = 'pos="JJ"+ pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_a_plus_a_in_caaaad(self):
    """Test greedy findall wi a_plus_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"+ pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = 'pos="JJ"+ pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_a_plus_a_in_caaaad(self):
    """Test reluctant findall wi a_plus_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"+ pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = 'pos="JJ"+ pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_a_plus_a_in_caaaad(self):
    """Test greedy finditer wi a_plus_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"+ pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = 'pos="JJ"+ pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=5, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_a_plus_a_in_caaaad(self):
    """Test reluctant finditer wi a_plus_a_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ"+ pos="JJ"' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = 'pos="JJ"+ pos="JJ"'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=3, value=[ {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}]))
    expected.append(pyrata.match.Match (start=3, end=5, value=[ {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   




# --------------------------------------------------------------------------------------
# a_dot_in_caaaab greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_a_dot_in_caaaab(self):
    """Test greedy search a_dot_in_caaaab. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" .' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = 'pos="JJ" .'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'},  {'pos': 'JJ', 'raw': 'easy'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_a_dot_in_caaaab(self):
    """Test reluctant search a_dot_in_caaaab. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" .' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = 'pos="JJ" .'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'},  {'pos': 'JJ', 'raw': 'easy'} ])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_a_dot_in_caaaab(self):
    """Test greedy findall a_dot_in_caaaab. The pattern is present in the data."""
    # python3 pyrata_re.py 'pos="JJ" .' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = 'pos="JJ" .'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_a_dot_in_caaaab(self):
    """Test reluctant findall a_dot_in_caaaab. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" .' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = 'pos="JJ" .'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_a_dot_in_caaaab(self):
    """Test greedy finditer a_dot_in_caaaab. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" .' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = 'pos="JJ" .'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}]))
    expected.append(pyrata.match.Match (start=3, end=5, value=[{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_a_dot_in_caaaab(self):
    """Test reluctant finditer a_dot_in_caaaab. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" .' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = 'pos="JJ" .'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}]))
    expected.append(pyrata.match.Match (start=3, end=5, value=[{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   


# --------------------------------------------------------------------------------------
# a_a_star_in_caaaad greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_a_a_star_in_caaaad(self):
    """Test greedy search wi a_a_star_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"*' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = 'pos="JJ" pos="JJ"*'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=5, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_a_a_star_in_caaaad(self):
    """Test reluctant search wi a_a_star_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"*' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = 'pos="JJ" pos="JJ"*'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=2, value=[{'pos': 'JJ', 'raw': 'fast'}])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_a_a_star_in_caaaad(self):
    """Test greedy findall wi a_a_star_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"*' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = 'pos="JJ" pos="JJ"*'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_a_a_star_in_caaaad(self):
    """Test reluctant findall wi a_a_star_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"*' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = 'pos="JJ" pos="JJ"*'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_a_a_star_in_caaaad(self):
    """Test greedy finditer wi a_a_star_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"*' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = 'pos="JJ" pos="JJ"*'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=5, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_a_a_star_in_caaaad(self):
    """Test reluctant finditer wi a_a_star_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"*' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = 'pos="JJ" pos="JJ"*'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=2, value=[ {'pos': 'JJ', 'raw': 'fast'} ]))
    expected.append(pyrata.match.Match (start=2, end=3, value=[ {'pos': 'JJ', 'raw': 'easy'} ]))
    expected.append(pyrata.match.Match (start=3, end=4, value=[ {'pos': 'JJ', 'raw': 'funny'} ]))
    expected.append(pyrata.match.Match (start=4, end=5, value=[ {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   


# --------------------------------------------------------------------------------------
# a_a_option_in_caaaad greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_a_a_option_in_caaaad(self):
    """Test greedy search wi a_a_option_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"?' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = 'pos="JJ" pos="JJ"?'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_a_a_option_in_caaaad(self):
    """Test reluctant search wi a_a_option_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"?' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = 'pos="JJ" pos="JJ"?'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=2, value=[{'pos': 'JJ', 'raw': 'fast'}])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_a_a_option_in_caaaad(self):
    """Test greedy findall wi a_a_option_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"?' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = 'pos="JJ" pos="JJ"?'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_a_a_option_in_caaaad(self):
    """Test reluctant findall wi a_a_option_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"?' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = 'pos="JJ" pos="JJ"?'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_a_a_option_in_caaaad(self):
    """Test greedy finditer wi a_a_option_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"?' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = 'pos="JJ" pos="JJ"?'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}]))
    expected.append(pyrata.match.Match (start=3, end=5, value=[{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_a_a_option_in_caaaad(self):
    """Test reluctant finditer wi a_a_option_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"?' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = 'pos="JJ" pos="JJ"?'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=2, value=[ {'pos': 'JJ', 'raw': 'fast'} ]))
    expected.append(pyrata.match.Match (start=2, end=3, value=[ {'pos': 'JJ', 'raw': 'easy'} ]))
    expected.append(pyrata.match.Match (start=3, end=4, value=[ {'pos': 'JJ', 'raw': 'funny'} ]))
    expected.append(pyrata.match.Match (start=4, end=5, value=[ {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   



# --------------------------------------------------------------------------------------
# a_a_plus_in_caaaad greedy/reluctant search/findall/finditer (i.e. any_quantifier at_the_beginning)  
# --------------------------------------------------------------------------------------

  # ----------------------------------------------------------------------
  def test_greedy_search_a_a_plus_in_caaaad(self):
    """Test greedy search wi  a_a_plus_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"+' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}]" --method search --mode greedy
    pattern = 'pos="JJ" pos="JJ"+'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=5, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ])
    result = pyrata.re.search(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_search_a_a_plus_in_caaaad(self):
    """Test reluctant search wi a_a_plus_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"+' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method search --mode reluctant
    pattern = 'pos="JJ" pos="JJ"+'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  pyrata.match.Match (start=1, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}])
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_findall_a_a_plus_in_caaaad(self):
    """Test greedy findall wi a_a_plus_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"+' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method findall --mode greedy
    pattern = 'pos="JJ" pos="JJ"+'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_findall_a_a_plus_in_caaaad(self):
    """Test reluctant findall wi a_a_plus_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"+' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method findall --mode reluctant
    pattern = 'pos="JJ" pos="JJ"+'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected =  [[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    #print ('\ntest_reluctant_findall_wi_any_quantifier_at_the_beginning={}'.format(result))
    self.assertEqual(result, expected)    

  # ----------------------------------------------------------------------
  def test_greedy_finditer_a_a_plus_in_caaaad(self):
    """Test greedy finditer wi a_a_plus_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"+' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'},{'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode greedy
    pattern = 'pos="JJ" pos="JJ"+'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=5, value=[{'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'greedy')
    self.assertEqual(result, expected) 

   # ----------------------------------------------------------------------
  def test_reluctant_finditer_a_a_plus_in_caaaad(self):
    """Test reluctant finditer wi a_a_plus_in_caaaad. The pattern is present in the data."""
    # python3 pyrata_re.py  'pos="JJ" pos="JJ"+' "[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]" --method finditer --mode reluctant
    pattern = 'pos="JJ" pos="JJ"+'
    data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'},  {'pos': 'TO', 'raw': 'to'}]
    expected = pyrata.match.MatchesList()  
    expected.append(pyrata.match.Match (start=1, end=3, value=[ {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}]))
    expected.append(pyrata.match.Match (start=3, end=5, value=[ {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'} ]))
    result = pyrata.re.finditer(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)   






  # ----------------------------------------------------------------------
  def test_greedy_findall_sequence_wi_optional_step_at_the_beginning(self):
    """Test findall method with a step sequence pattern; one element at the beginning being optional. The pattern is present in the data."""
    pattern = 'pos="JJ"? pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_reluctant_findall_sequence_wi_optional_step_at_the_beginning(self):
    """Test findall method in reluctant mode with a step sequence pattern; one element at the beginning being optional. The pattern is present in the data."""
    pattern = 'pos="JJ"? pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]
    result = pyrata.re.findall(pattern, data, mode='reluctant')
    self.assertEqual(result, expected)     

  # ----------------------------------------------------------------------
  def test_greedy_findall_sequence_wi_any_step_at_the_beginning(self):
    """Test findall method in greedy mode with sequences with any step at the beginning of the pattern . The pattern is present in the data."""
    pattern = 'pos="JJ"* pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected) 


  # ----------------------------------------------------------------------
  def test_reluctant_findall_sequence_wi_any_step_at_the_beginning(self):
    """Test findall method in reluctant mode on sequences with any step at the beginning of the pattern. The pattern is present in the data."""
    pattern = 'pos="JJ"* pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_greedy_findall_sequence_wi_at_least_one_step_at_the_beginning(self):
    """Test findall method in greedy mode on sequence with  at least one step sequence at the beginning of the pattern. The pattern is present in the data."""
    pattern = 'pos="JJ"+ pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  


  # ----------------------------------------------------------------------
  def test_DFA_from_greedy_finditer_sequence_wi_any_step_at_the_beginning(self):
    """Test findall method in greedy mode with sequences with any step at the beginning of the pattern . The pattern is present in the data."""
    pattern = 'pos="JJ"* pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    
    # expected = [['IN[#S]->CHAR(pos="JJ")->OUT[#S]', 'IN[#S]->CHAR(pos~"NN.*")->OUT[#M]'], 
    #             ['IN[#S]->CHAR(pos~"NN.*")->OUT[#M]'], 
    #             ['IN[#S]->CHAR(pos~"NN.*")->OUT[#M]']]
    expected = [['pos="JJ"', 'pos~"NN.*"'],  ['pos~"NN.*"']] 
    #def __init__(self, char, in_states, out_states, symbolic_step_expression, single_constraint_tuple_list, single_constraint_variable_list, group_pile):
    # start_state = State.create_start_state()
    # matching_state = State.create_matching_state()
    # in_states = Set()
    # in_states.add(start_state)
    # out_states.add(start_state)
    # State('pos="JJ"', in_states, out_states, [], [], [], [])

    result = []
#    i = 0    
    for m in pyrata.re.finditer(pattern, data):
      # print ('Debug: DFA={} type={}'.format(m, type(m)))
      # print ('Debug: DFA={}'.format(m.DFA()))
 #     result.append(m.DFA())
      result.append(m.str_DFA())
#      print ('Debug: DFA={} type={} str={}'.format(m.DFA(), type(m.DFA()[0]), m.str_DFA()))
#      self.assertEqual(m.DFA(), expected[i])  # m.DFA() return state so expected should also be made of states 
#      self.assertEqual(m.str_DFA(), expected[i]) 
#      i += 1
#    print ('test_DFA_from_greedy_finditer_sequence_wi_any_step_at_the_beginning expected={}'.format(expected))  
#    print ('test_DFA_from_greedy_finditer_sequence_wi_any_step_at_the_beginning result  ={}'.format(result))  
    self.assertEqual(result, expected) 

  # ----------------------------------------------------------------------
  def test_findall_any_step_step_nbar_in_data(self):
    """Test findall method in greedy mode on sequence with optional class step  at the beginning of the pattern. The pattern is present in the data."""
    # https://gist.github.com/alexbowe/879414
    # echo 0 | perl -ne '$s = "abccd"; if ($s =~ /([bc]c)/) {print "$1\n"}'
    # bc
    pattern = '[pos~"NN.*" | pos="JJ"]* pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]

    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  
  


  # ----------------------------------------------------------------------
  def test_findall_at_least_one_step_step_nbar_in_data(self):
    """Test findall method in greedy mode on sequence with at least one class step  at the beginning of the pattern. The pattern is present in the data."""
    # https://gist.github.com/alexbowe/879414
    # echo 0 | perl -ne '$s = "abccd"; if ($s =~ /([bc]c)/) {print "$1\n"}'
    # bc
    pattern = '[pos~"NN.*" | pos="JJ"]+ pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    #data = [ {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_sequence_partially_matched_in_data_ending(self):
    """Test findall method in greedy mode on sequence pattern partially present in the data."""
    pattern = 'pos="NNS" pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_optional_step_step_partially_matched_in_data_ending(self):
    """Test findall method in greedy mode on sequence pattern partially present in the data with optional step at the beginning of the pattern."""
    pattern = 'pos="NNS"? pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_any_step_step_partially_matched_in_data_ending(self):
    """Test findall method in greedy mode on sequence pattern partially present in the data with any step at the beginning of the pattern."""
    pattern = 'pos="NNS"? pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_at_least_one_step_step_partially_matched_in_data_ending(self):
    """Test findall method in greedy mode on sequence pattern partially present in the data with at least one step at the beginning of the pattern."""
    pattern = 'pos="NNS"+ pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  


  # ----------------------------------------------------------------------
  def test_findall_step_at_least_one_not_step_step_in_data(self):
    """Test findall method in greedy mode on sequence with at least one class step in the middle of the pattern. The pattern is present in the data."""
    pattern = 'pos="VB" [!pos="NNS"]+ pos="NNS"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_step_present_optional_step_step_in_data(self):
    """Test findall method in greedy mode on sequence with optional step in the middle of the pattern. The pattern is present in the data."""
    pattern = 'pos="VB" pos="JJ"? pos="NNS"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_step_absent_optional_step_step_in_data(self):
    """Test findall method in greedy mode on sequence with at least one class step in the middle of the pattern. The option is absent from the data."""
    pattern = 'pos="IN" pos="JJ"? pos="NNP"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  


  # ----------------------------------------------------------------------
  def test_greedy_findall_sequence_wi_optional_step_at_the_end(self):
    """Test findall method in greedy mode on sequence with optional step at the end of the pattern. The pattern is present in the data."""
    #echo 0 |  perl -ne '$s="abbbcb"; if ($s =~/(bc?)/) {print "$1\n"}' gives b
    pattern = 'pos="JJ" pos~"NN.*"?'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    # naive approach
    expected = [[{'raw': 'fast', 'pos': 'JJ'}], [{'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_reluctant_findall_sequence_wi_optional_step_at_the_end(self):
    """Test findall method in reluctant mode on sequence with optional step at the end of the pattern. The pattern is present in the data."""
    #echo 0 |  perl -ne '$s="abbbcb"; if ($s =~/(bc?)/) {print "$1\n"}' gives b
    pattern = 'pos="JJ" pos~"NN.*"?'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    # reluctant
    expected = [[{'raw': 'fast', 'pos': 'JJ'}], [{'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)  




  # ----------------------------------------------------------------------
  def test_greedy_findall_sequence_wi_any_step_at_the_end(self):
    """Test findall method in greedy mode on sequence with any step at the end of the pattern. The pattern is present in the data."""
    pattern = 'pos="JJ" pos~"NN.*"*'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_reluctant_findall_sequence_wi_any_step_at_the_end(self):
    """Test findall method in reluctant mode on sequence with any step at the end of the pattern. The pattern is present in the data."""
    pattern = 'pos="JJ" pos~"NN.*"*'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'raw': 'fast', 'pos': 'JJ'}], [{'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')

    self.assertEqual(result, expected)  


  # ----------------------------------------------------------------------
  def test_greedy_findall_sequence_wi_two_optinal_steps_in_the_middle(self):
    """Test findall method in greedy mode on sequence with two optional steps in the middle of the pattern. The pattern is present in the data."""
    #echo 0 |  perl -ne '$s="abbbcb"; if ($s =~/(bc?)/) {print "$1\n"}' gives b
    pattern = 'pos="VBZ" pos="JJ"? pos="JJ"? pos="CC"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_reluctant_findall_sequence_wi_two_optinal_steps_in_the_middle(self):
    """Test findall method in reluctant mode on sequence with two optional steps in the middle of the pattern. The pattern is present in the data."""
    #echo 0 |  perl -ne '$s="abbbcb"; if ($s =~/(bc?)/) {print "$1\n"}' gives b
    pattern = 'pos="VBZ" pos="JJ"? pos="JJ"? pos="CC"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}]]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_sequence_wi_step_preceded_by_its_complement(self):
    """Test findall method on sequence with any class step which is the complement to the next one. The pattern is present in the data."""
    # https://gist.github.com/alexbowe/879414
    pattern = 'pos~"VB." [!raw="to"]* raw="to"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}]]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  




  # ----------------------------------------------------------------------
  def test_search_wi_start_anchor(self):
    """Test search method with start anchor. The pattern is present in the data."""
    # ^ matches the start of data before the first token in a data.
    # $ matches the end of data ~after the last token of data.
    # test_pattern_starting_with_the_first_token_of_data_present_as_expected_in_data
    # test_pattern_ending_with_the_last_token_of_data_present_as_expected_in_data
    # test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_present_as_expected_in_data   
    # test_pattern_starting_with_the_first_token_of_data_not_present_as_expected_in_data
    # test_pattern_ending_with_the_last_token_of_data_not_present_as_expected_in_data
    # test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_not_present_as_expected_in_data  
    pattern = '^raw="It" raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    #data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}]
    expected = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)  

  # ----------------------------------------------------------------------
  def test_search_wi_end_anchor(self):
    """Test search method with end anchor. The pattern is present in the data."""
    pattern = 'raw="with" raw="Pyrata"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)  

  # ----------------------------------------------------------------------
  def test_search_wi_start_and_end_anchors(self):
    """Test search method with both start and end anchors. The pattern is present in the data."""
    pattern = '^raw="with" raw="Pyrata"$'
    data = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)  




  # ----------------------------------------------------------------------
  def test_findall_wi_start_anchor(self):
    """Test findall method with start anchor. The pattern is present in the data."""
    pattern = '^raw="It" raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'},{'pos': 'CC', 'raw': 'and'}, {'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'easy'},  {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    #data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}]
    expected = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result[0],expected)  

  # ----------------------------------------------------------------------
  def test_findall_wi_end_anchor(self):
    """Test findall method with end anchor. The pattern is present in the data."""
    pattern = 'raw="with" raw="Pyrata"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'funny'},  {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'},{'pos': 'CC', 'raw': 'and'}, {'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'easy'},  {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result[0],expected)   

  # ----------------------------------------------------------------------
  def test_findall_wi_start_and_end_anchors(self):
    """Test findall method with both start and end anchors. The pattern is present in the data."""
    pattern = '^raw="with" raw="Pyrata"$'
    data = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result[0],expected)  


  # ----------------------------------------------------------------------
  def test_reluctant_findall_wi_start_anchor(self):
    """Test reluctant findall method with start anchor. The pattern is present in the data."""
    pattern = '^raw="It" raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'},{'pos': 'CC', 'raw': 'and'}, {'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'easy'},  {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    #data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}]
    expected = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    self.assertEqual(result[0],expected)  

  # ----------------------------------------------------------------------
  def test_reluctant_findall_wi_end_anchor(self):
    """Test reluctant findall method with end anchor. The pattern is present in the data."""
    pattern = 'raw="with" raw="Pyrata"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'funny'},  {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'},{'pos': 'CC', 'raw': 'and'}, {'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'easy'},  {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    self.assertEqual(result[0],expected)   

  # ----------------------------------------------------------------------
  def test_reluctant_findall_wi_start_and_end_anchors(self):
    """Test reluctant findall method with both start and end anchors. The pattern is present in the data."""
    pattern = '^raw="with" raw="Pyrata"$'
    data = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.findall(pattern, data, mode = 'reluctant')
    self.assertEqual(result[0],expected)  



  # ----------------------------------------------------------------------
  def test_search_wi_start_anchor_but_absent(self):
    """Test search method with start anchor. The pattern is not present in the data."""
    pattern = '^raw="is" raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_search_wi_end_anchor_but_absent(self):
    """Test search method with end anchor. The pattern is not present in the data."""
    pattern = 'raw="is" raw="fast"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_search_wi_start_and_end_anchors_but_absent(self):
    """Test search method with start and end anchors. The pattern is not present in the data."""
    pattern = '^raw="is" raw="fast"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result, expected)  




  # ----------------------------------------------------------------------
  def test_findall_wi_start_anchor_but_absent(self):
    """Test findall method with start anchor. The pattern is not present in the data."""
    pattern = '^raw="is" raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_wi_end_anchor_but_absent(self):
    """Test findall method with end anchor. The pattern is not present in the data."""
    pattern = 'raw="is" raw="fast"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  

  # ----------------------------------------------------------------------
  def test_findall_wi_start_and_end_anchors_but_absent(self):
    """Test findall method with start and end anchors. The pattern is not present in the data."""
    pattern = '^raw="is" raw="fast"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    result = pyrata.re.findall(pattern, data)
    self.assertEqual(result, expected)  





  # ----------------------------------------------------------------------
  def test_search_no_group_marked(self):
    """Test search method with no group. The pattern is present in the data."""
    #pattern = '(raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")'

    #pattern = 'raw="It" (raw="is" |fa="ke") (( pos="JJ"* (pos="JJ" raw="and"|fa="ke") (pos="JJ"|fa="ke") |fa="ke")|fa="ke") (raw="to"|fa="ke")'
    #pattern = 'raw="It" (raw="is"|fa="ke") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )|fa="ke") (raw="to"|fa="ke")'
    #pattern = 'raw="It" (raw="is"|fa="ke") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to"|fa="ke")'
    #pattern = 'raw="A" (raw="B") (( raw="C"* (raw="C" raw="D") (raw="E") )) (raw="F")'
    
    pattern = 'raw="is"'                     # [None, 'raw="is"']
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}], 1, 2]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected)  

  # ----------------------------------------------------------------------
  def test_search_group_zero_marked(self):
    """Test search method with zero group marked. The pattern is present in the data."""
    pattern = '(raw="is")'                   # [None, [[[None, 'raw="is"']]]]
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}], 1, 2], [[{'pos': 'VBZ', 'raw': 'is'}], 1, 2]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected)  

  # ----------------------------------------------------------------------
  def test_search_nested_group_zero_marked(self):
    """Test search method with nested zero group marked. The pattern is present in the data."""
    pattern = '(((raw="is")))'               # [None, [[[None, [[[None, [[[None, 'raw="is"']]]]]]]]]]   
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}], 1, 2], [[{'pos': 'VBZ', 'raw': 'is'}], 1, 2], [[{'pos': 'VBZ', 'raw': 'is'}], 1, 2], [[{'pos': 'VBZ', 'raw': 'is'}], 1, 2]] # [[[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'is', 'pos': 'VBZ'}], 0, 1], [[{'raw': 'is', 'pos': 'VBZ'}], 0, 1]] 
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected)  

  # ----------------------------------------------------------------------
  def test_search_step_group_inside_a_sequence(self):
    """Test search method with a group inside the sequence. The pattern is present in the data."""
    #pattern = 'raw="is" pos="JJ" pos="JJ"'   # [[None, 'raw="is" '], [None, 'pos="JJ" '], [None, 'pos="JJ"']]
    #expected = [[[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], 1, 4]]
    pattern = 'raw="is" (pos="JJ") pos="JJ"' # [[None, 'raw="is" '], [None, [[[None, 'pos="JJ"']]]], [None, 'pos="NN"']]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], 1, 4], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected)  

  # ----------------------------------------------------------------------
  def test_search_multiple_step_group_some_nested(self):
    """Test search method with multiple step groups; some nested. The pattern is present in the data."""
    pattern = 'raw="is" (pos="JJ") ((pos="JJ"))' # 
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], 1, 4], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3], [[{'raw': 'easy', 'pos': 'JJ'}], 3, 4], [[{'raw': 'easy', 'pos': 'JJ'}], 3, 4] ]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected)  
    





  # ----------------------------------------------------------------------
  def test_search_sequence_as_group_zero(self):
    """Test search method with a sequence as group. The pattern is present in the data."""
    pattern = '(raw="is" pos="JJ")'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}], 1, 3], [[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}], 1, 3]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 



  # ----------------------------------------------------------------------
  def test_search_sequence_of_individual_step_groups(self):
    """Test search method with two distinct step groups. The pattern is present in the data."""
    pattern = '(raw="is") (pos="JJ")'        # [[None, [[[None, 'raw="is"']]]], [None, [[[None, 'pos="JJ"']]]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 

  # ----------------------------------------------------------------------
  def test_search_sequence_as_zero_group_wi_nested_step_group (self):
    """Test search method with a sequence as zero group and a nested step group. The pattern is present in the data."""
    pattern = '(raw="is" (pos="JJ"))'        # [None, [[[None, 'raw="is" '], [None, [[[None, 'pos="JJ"']]]]]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 

    

  # ----------------------------------------------------------------------
  def test_search_step_alternative_as_group_zero(self):
    """Test search method with a step alternative as group zero. The pattern is present in the data."""
    pattern = '(raw="is"|pos="JJ")'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}], 1, 2], [[{'pos': 'VBZ', 'raw': 'is'}], 1, 2]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 
# FIXME check the result ! 

  # ----------------------------------------------------------------------
  def test_greedy_search_of_step_sequences_alternative_of_same_length_wi_a_common_starting_subpart (self):
    """Test greedy search method of sequences alternatives of same length wi a common starting subpart. The pattern is present in the data."""
    pattern = '(raw="is" pos="NN"|raw="is" pos="JJ")'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 

  # ----------------------------------------------------------------------
  def test_greedy_search_of_step_sequences_alternative_of_various_length_wi_a_common_starting_subpart (self):
    """Test greedy search method of sequences alternatives of various length wi a common starting subpart. The pattern is present in the data."""
    pattern = '(raw="is" pos="JJ"|raw="is" )'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 

  # ----------------------------------------------------------------------
  def test_reluctant_search_of_step_sequences_alternative_of_various_length_wi_a_common_starting_subpart (self):
    """Test reluctant search method of sequences alternatives of various length wi a common starting subpart. The pattern is present in the data."""
    pattern = '(raw="is" pos="JJ"|raw="is" )'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data, mode = 'reluctant')
    self.assertEqual(result.groups(),expected) 

  # ----------------------------------------------------------------------
  def test_greedy_search_of_step_sequences_alternative_of_various_length_wo_a_common_starting_subpart (self):
    """Test greedy search method of sequences alternatives of various length wo a common starting subpart. The pattern is present in the data."""
    pattern = '(pos="JJ" pos="JJ"|raw="is" )'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2]]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 



  # ----------------------------------------------------------------------
  def test_greedy_search_of_multiple_step_sequences_alternative_of_same_length_wi_a_common_starting_subpart (self):
    """Test greedy search method of multiple sequences alternatives of same length wi a common starting subpart. The pattern is present in the data."""
    pattern = '(raw="is" pos="NN"|raw="is" pos="NN"|raw="is" pos="JJ")'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3]]

    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 

    

  # ----------------------------------------------------------------------
  def test_search_multiple_optionnaly_nested_quantified_step_or_sequence_group_1 (self):
    """Test greedy search method on multiple quantified step and sequence groups; some being nested. The pattern is present in the data."""
    pattern = 'raw="It" (raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")'
    expected = [[[{'pos': 'PRP', 'raw': 'It'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}], 0, 7], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], [[{'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}], 3, 5], [[{'raw': 'funny', 'pos': 'JJ'}], 5, 6], [[{'raw': 'to', 'pos': 'TO'}], 6, 7]]
    #self.getLexer().lexer.group_pattern_offsets_group_list= [[0, 7], [1, 2], [2, 6], [2, 6], [3, 5], [5, 6], [6, 7]]

    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 


  # ----------------------------------------------------------------------
  def test_search_multiple_optionnaly_nested_quantified_step_or_sequence_group_2 (self):
    """Test greedy search method on multiple quantified step and sequence groups; some being nested (v2). The pattern is present in the data."""
    pattern = 'raw="It" (raw="is") (( (pos="JJ"* pos="JJ") raw="and" (pos="JJ") )) (raw="to")'
    expected = [[[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}], 0, 7], 
      [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], 
      [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], 
      [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], 
      [[{'raw': 'fast', 'pos': 'JJ'}, {'pos': 'JJ', 'raw': 'easy'}], 2, 4], 
      [[{'raw': 'funny', 'pos': 'JJ'}], 5, 6], 
      [[{'raw': 'to', 'pos': 'TO'}], 6, 7]]
 
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.groups(),expected) 
    

  # ----------------------------------------------------------------------
  def test_annotate_default_action_sub_default_group_default_iob(self):
    """Test annotate method on optional step with default args namely sub action, zero group and iob False. The pattern is present in the data."""
    pattern = 'pos~"NN.?"'
    annotation = {'raw':'smurf', 'pos':'NN' },
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [{'pos': 'IN', 'raw': 'Over'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'smurf'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'smurf'}, {'pos': ',', 'raw': ','}, {'pos': 'NN', 'raw': 'smurf'}, {'pos': 'NN', 'raw': 'smurf'}, {'pos': 'VBD', 'raw': 'told'}, {'pos': 'PRP$', 'raw': 'his'}, {'pos': 'NN', 'raw': 'smurf'}]
    result = pyrata.re.annotate(pattern, annotation, data)
    self.assertEqual(result, expected)


    gold = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT', 'chunk':'B-NP'}, 
      {'raw':'cup', 'pos':'NN', 'chunk':'I-NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'B-NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'B-NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'I-NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'B-NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'I-NP'} ]


  # ----------------------------------------------------------------------
  def test_annotate_default_action_sub_default_group_default_iob_absent_from_data(self):
    """Test annotate method on step with default args namely sub action, zero group and iob False. The pattern is non present in the data."""
    pattern = 'pos="JJ"'    
    annotation = {'raw':'smurf', 'pos':'NN' }
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'}, 
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, {'raw':'story', 'pos':'NN'} ]
    result = pyrata.re.annotate(pattern, annotation, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_annotate_default_action_sub_default_group_default_iob_annotation_empty_in_data(self):
    """Test annotate method on  step with default args namely sub action, zero group and iob False. The annotation is empty. The pattern is present in the data."""
    pattern = 'pos~"NN.?"'
    annotation = []
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'of', 'pos':'IN'},
      {'raw':',', 'pos':','},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}]
    result = pyrata.re.annotate(pattern, annotation, data)
    self.assertEqual(result, expected)


  # ----------------------------------------------------------------------
  def test_annotate_default_action_sub_default_group_default_iob_annotation_dict_pattern_sequence_to_annotation_step_in_data(self):
    """Test annotate method on sequence with default args namely sub action, zero group and iob False. The annotation is a sequence. The pattern is present in the data."""
    pattern = 'pos~"(DT|PRP\$)" pos~"NN.?"'
    annotation = {'raw':'smurf', 'pos':'NN' }
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, {'raw':'story', 'pos':'NN'} ]
    expected = [{'raw': 'Over', 'pos': 'IN'}, 
      {'raw': 'smurf', 'pos': 'NN'}, 
      {'raw': 'of', 'pos': 'IN'}, 
      {'raw': 'coffee', 'pos': 'NN'}, 
      {'raw': ',', 'pos': ','}, 
      {'raw': 'Mr.', 'pos': 'NNP'}, {'raw': 'Stone', 'pos': 'NNP'}, 
      {'raw': 'told', 'pos': 'VBD'}, 
      {'raw': 'smurf', 'pos': 'NN'}]
    result = pyrata.re.annotate(pattern, annotation, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_annotate_default_action_sub_group_one_default_iob_annotation_dict_pattern_in_data (self):
    """Test annotate method on sequence with default args namely sub action, and iob False. The annotation is a sequence. The group is one. The pattern is present in the data."""
    pattern = 'pos~"(DT|PRP\$)" (pos~"NN.?")'
    group = [1]
    annotation = {'raw':'smurf', 'pos':'NN' }
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [{'raw': 'Over', 'pos': 'IN'}, {'raw': 'a', 'pos': 'DT'}, {'raw': 'smurf', 'pos': 'NN'}, {'raw': 'of', 'pos': 'IN'}, {'raw': 'coffee', 'pos': 'NN'}, {'raw': ',', 'pos': ','}, {'raw': 'Mr.', 'pos': 'NNP'}, {'raw': 'Stone', 'pos': 'NNP'}, {'raw': 'told', 'pos': 'VBD'}, {'raw': 'his', 'pos': 'PRP$'}, {'raw': 'smurf', 'pos': 'NN'}]
    result = pyrata.re.annotate(pattern, annotation, data, group = group)
    self.assertEqual(result, expected)


  # ----------------------------------------------------------------------
  def test__sub_group_one_default_iob_annotation_dict_pattern_in_data (self):
    """Test sub method on sequence with default args namely sub action, and iob False. The annotation is a sequence. The group is one. The pattern is present in the data."""
    pattern = 'pos~"(DT|PRP\$)" (pos~"NN.?")'
    group = [1]
    annotation = {'raw':'smurf', 'pos':'NN' }
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [{'raw': 'Over', 'pos': 'IN'}, {'raw': 'a', 'pos': 'DT'}, {'raw': 'smurf', 'pos': 'NN'}, {'raw': 'of', 'pos': 'IN'}, {'raw': 'coffee', 'pos': 'NN'}, {'raw': ',', 'pos': ','}, {'raw': 'Mr.', 'pos': 'NNP'}, {'raw': 'Stone', 'pos': 'NNP'}, {'raw': 'told', 'pos': 'VBD'}, {'raw': 'his', 'pos': 'PRP$'}, {'raw': 'smurf', 'pos': 'NN'}]
    result = pyrata.re.sub(pattern, annotation, data, group = group)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_update_default_group_default_iob_annotation_dict_pattern_in_data(self):
    """Test update method on sequence with optional first step and default args namely sub action, and iob False. The annotation is a sequence. The pattern is present in the data."""
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    annotation = {'raw':'smurf', 'pos':'NN', 'chunk':'NP'}
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [{'pos': 'IN', 'raw': 'Over'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'pos': 'IN', 'raw': 'of'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'pos': ',', 'raw': ','}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'pos': 'VBD', 'raw': 'told'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}]
    result = pyrata.re.update(pattern, annotation, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_extend_wi_default_group_default_iob_pattern_sequence_on_sequence_wi_optional_first_step(self):
    """Test extend method on sequence with optional first step and default args namely group and iob False. The annotation is a sequence. The pattern is present in the data."""

    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    annotation = {'raw':'smurf', 'pos':'NN', 'chunk':'NP'}
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' , 'chunk':'NP'}, 
      {'raw':'cup', 'pos':'NN' , 'chunk':'NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'NP'} ]
    result = pyrata.re.extend(pattern, annotation, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_extend_default_group_default_iob_annotation_sequence_of_dict_for_single_token_match_in_data(self):
    """Test extend method on sequence with optional first step and default args namely group and iob False. The annotation is one step. The pattern is present in the data."""

    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    annotation = {'chunk':'NP'}
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' , 'chunk':'NP'}, 
      {'raw':'cup', 'pos':'NN' , 'chunk':'NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'NP'} ]
    result = pyrata.re.extend(pattern, annotation, data)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_extend_default_group_true_iob_wi_step_pattern_but_sequence_annotation(self):
    """Test extend method on step wi iob true and a sequence as annotation. The pattern is present in the data."""
    pattern = 'pos~"NN.?"'
    annotation = [{'raw':'smurf1'}, {'raw':'smurf2'} ]
    iob = True
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    result = pyrata.re.extend(pattern, annotation, data, iob = iob)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_greedy_extend_default_group_iob_true_wi_sequence_pattern_and_step_annotation(self):
    """Test greedy extend method on step on zero group and iob True with a step as annotation. The pattern is present in the data."""
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    annotation = {'chunk':'NP'}
    iob = True
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]

    # naive approach
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' , 'chunk':'B-NP'}, 
      {'raw':'cup', 'pos':'NN' , 'chunk':'I-NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'B-NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'B-NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'I-NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'B-NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'I-NP'} ]

    result = pyrata.re.extend(pattern, annotation, data, iob = iob)
    self.assertEqual(result, expected)


  # ----------------------------------------------------------------------
  def test_reluctant_extend_default_group_iob_true_wi_sequence_pattern_and_step_annotation(self):
    """Test reluctant extend method on step on zero group and iob True with a step as annotation. The pattern is present in the data."""
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    annotation = {'chunk':'NP'}
    iob = True
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' , 'chunk':'B-NP'}, 
      {'raw':'cup', 'pos':'NN' , 'chunk':'I-NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'B-NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'B-NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'B-NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'B-NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'I-NP'} ]      

    result = pyrata.re.extend(pattern, annotation, data, iob = iob, mode = 'reluctant')
    self.assertEqual(result, expected)



  # ----------------------------------------------------------------------
  def test_greedy_annotate_nfa_fire_on_shortest_match(self):
    """Test greedy extend method on step on sequence wi optional steps and iob true with a step as annotation. The pattern is present in the data."""

    pattern = 'pos="DT"? pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'

    annotation = {'chunk':'NP'}
    iob = True

    data = [ {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'} ]
    # longest 
    expected = [ {'raw':'Mr.', 'pos':'NNP', 'chunk':'B-NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'I-NP'}]

 
    result = pyrata.re.extend(pattern, annotation, data, iob = iob)
    self.assertEqual(result, expected)

  # ----------------------------------------------------------------------
  def test_reluctant_annotate_nfa_fire_on_shortest_match(self):
    """Test reluctant extend method on step on sequence wi optional steps and iob true with a step as annotation. The pattern is present in the data."""
    pattern = 'pos="DT"? pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'

    annotation = {'chunk':'NP'}
    iob = True

    data = [  {'raw':'Mr.', 'pos':'NNP'}, #{'raw':'The', 'pos':'DT'}, 
      {'raw':'Stone', 'pos':'NNP'} ]


    # shortest  
    expected = [ {'raw':'Mr.', 'pos':'NNP', 'chunk':'B-NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'B-NP'}]
 
    result = pyrata.re.extend(pattern, annotation, data, iob = iob, mode = 'reluctant')
    self.assertEqual(result, expected)



  # ----------------------------------------------------------------------
  def test_search_sequence_wi_alternative_groups_of_sequence_of_various_length(self):
    """Test search method of a sequence made of groups wi alternatives of various size. The pattern is present in the data."""

    pattern = '(raw="a" raw="cup" raw="of" raw="coffee")'
    pattern = '(raw="a" raw="cup" raw="of" raw="coffee" | raw="a" raw="tea" )' # Error: syntactic parsing error - unexpected token type="NAME" with value="raw" at position 54. Search an error before this point.
    pattern = '((raw="a" raw="cup" raw="of" raw="coffee") | (raw="a" raw="tea" ))'

    pattern = '((raw="of" raw="coffee") | (raw="of" raw="tea" ))'
    pattern = '(raw="of" raw="coffee" | raw="of" raw="tea" )'

    pattern = '(raw="a" raw="the")'  # [None, [[[None, 'raw="a" '], [None, 'raw="the"']]]]
    group_id = 0

    pattern = '(raw="a"|raw="the")'  # [None, [ [[None, 'raw="a" ']], [[None, 'raw="the"']] ]]
    expected =  [[{'pos': 'DT', 'raw': 'a'}], 1, 2]

    #pattern = '(raw="a" raw="cup"|raw="the")'  # [None, [ [[None, 'raw="a" ']], [[None, 'raw="the"']] ]]
    #pattern = '(raw="the"|raw="a" raw="cup" raw="of")'  # [None, [ [[None, 'raw="a" ']], [[None, 'raw="the"']] ]]


    pattern = '(pos="IN") (raw="a" raw="tea" | raw="a" raw="cup" raw="of" raw="coffee" | raw="an" raw="orange" raw="juice" ) [!pos=";"]'
    group_id = 2
    expected = [[{'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'cup'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'coffee'}], 1, 5]
    #self.test(description, method, lexicons, pattern, data, expected)  
    #pattern = '((raw="a" raw="cup" raw="of" raw="coffee")*| (raw="a" raw="tea" ))+'
    #pattern = '(raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")'
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]

    result = pyrata.re.search(pattern, data)
    self.assertEqual(result._groups[group_id], expected)

   # ----------------------------------------------------------------------
  def test_group_search_sequence_wi_alternative_groups_of_sequence_of_various_length_and_quantifiers(self):
    """Test search method of a sequence made of groups wi alternatives of various lengths and various quantifiers. The pattern is present in the data."""

    pattern = '(pos="IN") (raw="a" raw="tea" | raw="a" raw="cup" raw="of"? raw="coffee" | raw="an" raw="orange"* raw="juice" )+ [!pos=";"]'

    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [[{'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'cup'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'coffee'}], 1, 5]


    result = pyrata.re.search(pattern, data)
    # print ('\ttest_search_sequence_wi_alternative_groups_of_sequence_of_various_length_and_quantifiers={}'.format(result))
    # print ('\tresult.group(2)={}'.format(result.group(2)))
    # print ('\tresult.groups[2]={}'.format(result.groups()[2]))
    # print ('\texpected={}'.format(expected))
    self.assertEqual(result.group(2), expected[0])
    #self.assertEqual(result.groups()[2], expected)

   # ----------------------------------------------------------------------
  def test_groups_search_sequence_wi_alternative_groups_of_sequence_of_various_length_and_quantifiers(self):
    """Test search method of a sequence made of groups wi alternatives of various lengths and various quantifiers. The pattern is present in the data."""

    pattern = '(pos="IN") (raw="a" raw="tea" | raw="a" raw="cup" raw="of"? raw="coffee" | raw="an" raw="orange"* raw="juice" )+ [!pos=";"]'

    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [[{'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'cup'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'coffee'}], 1, 5]


    result = pyrata.re.search(pattern, data)
    # print ('\ttest_search_sequence_wi_alternative_groups_of_sequence_of_various_length_and_quantifiers={}'.format(result))
    # print ('\tresult.group(2)={}'.format(result.group(2)))
    # print ('\tresult.groups[2]={}'.format(result.groups()[2]))
    # print ('\texpected={}'.format(expected))
    #self.assertEqual(result.group(2), expected)
    self.assertEqual(result.groups()[2], expected)



  # ----------------------------------------------------------------------
  def test_search_quantified_zero_group_wi_nested_quantified_steps(self):
    """Test search method of a sequence group made of steps wi quantifiers; the whole group wi a quantifier. The pattern is present in the data."""
    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 

    pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")+' 

    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(0), expected)
    



  # ----------------------------------------------------------------------
  def test_search_zero_group_made_of_alternatives_wi_nested_quantified_steps(self):
    """Test search method of sequence alternatives made of steps wi quantifiers; the whole group wi a quantifier. The pattern is present in the data."""
  
    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 

    pattern = '(pos="VB" [!pos="NN"]* raw="Life" pos="."| pos="VB" [!pos="NN"]* raw="job" pos="."|pos="VB" [!pos="NN"]* raw="career" pos="."|pos="VB" [!pos="NN"]* raw="family" pos="."|pos="VB" [!pos="NN"]* raw="television" pos=".")+' # Debug: p[0]=[[[None, 'pos="VB" '], ['?', 'pos="DT"'], ['*', 'pos="JJ"'], [None, 'pos="NN" '], [None, 'pos="."']], [[None, 'pos="FAKE"']]]

    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}
      ,   {'raw':'foo', 'pos':'bar'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(0), expected)
    


  # ----------------------------------------------------------------------
  def test_eq_operator_on_Matches(self):
    """Test eq operator on Matches"""

    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]

    pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")+' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']
    quantified_group = pyrata.re.search(pattern, data )
    pattern = '(pos="VB" [!pos="NN"]* raw="Life" pos="."| pos="VB" [!pos="NN"]* raw="job" pos="."|pos="VB" [!pos="NN"]* raw="career" pos="."|pos="VB" [!pos="NN"]* raw="family" pos="."|pos="VB" [!pos="NN"]* raw="television" pos=".")+'
    quantified_alternatives = pyrata.re.search(pattern, data)
    
    success = False
    if quantified_group == quantified_alternatives:
      success = True
    self.assertTrue(success)
  


  # ----------------------------------------------------------------------
  def test_ne_operator_on_Matches(self):
    """Test ne operator on Matches"""

    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")+' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']
    quantified_group = pyrata.re.search(pattern, data )
    pattern = '(pos="VB" [!pos="NN"]* raw="Life" pos="."| pos="VB" [!pos="NN"]* raw="job" pos="."|pos="VB" [!pos="NN"]* raw="career" pos="."|pos="VB" [!pos="NN"]* raw="family" pos="."|pos="VB" [!pos="NN"]* raw="television" pos=".")+'
    quantified_alternatives = pyrata.re.search(pattern, data)
    
    success = True
    if quantified_group != quantified_alternatives:
      success = False
    self.assertTrue(success)

    

  # ----------------------------------------------------------------------
  def test_len_on_Matches_ie_len_groups(self):
    """Test test_len_on_Matches_ie_len_groups"""

    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")+' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']
    quantified_group = pyrata.re.search(pattern, data )
    pattern = '(pos="VB" [!pos="NN"]* raw="Life" pos="."| pos="VB" [!pos="NN"]* raw="job" pos="."|pos="VB" [!pos="NN"]* raw="career" pos="."|pos="VB" [!pos="NN"]* raw="family" pos="."|pos="VB" [!pos="NN"]* raw="television" pos=".")+'
    quantified_alternatives = pyrata.re.search(pattern, data)
    
    success = False
    #print ('Debug: do_test - len(quantified_group)={} len (quantified_alternatives)={}'.format(len(quantified_group), len (quantified_alternatives)))
    if len(quantified_group) == 2 and len(quantified_group) == len (quantified_alternatives):
      success = True
    self.assertTrue(success)


     
  # ----------------------------------------------------------------------
  def test_eq_on_MatchesList(self):
    """Test test_eq_on_MatchesList"""

    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    pattern = 'pos="VB" pos="DT"? pos="JJ"* pos="NN" pos="."' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']
    aMatchesList = pyrata.re.finditer(pattern, data)
    anotherMatchesList = pyrata.re.finditer(pattern, data)
    result = aMatchesList
    expected = anotherMatchesList
    success = False
    if aMatchesList == anotherMatchesList:
      success = True
    self.assertTrue(success)

     
   # ----------------------------------------------------------------------
  def test_ne_on_MatchesList(self):
    """Test test_ne_on_MatchesList"""

    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    pattern = 'pos="VB" pos="DT"? pos="JJ"* pos="NN" pos="."' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']
    aMatchesList = pyrata.re.finditer(pattern, data)
    anotherMatchesList = pyrata.re.finditer(pattern, data)
    result = aMatchesList
    expected = anotherMatchesList
    success = False
    if not(aMatchesList != anotherMatchesList):
      success = True
    self.assertTrue(success)


     

     
  # ----------------------------------------------------------------------
  def test_len_on_MatchesList(self):
    """Test test_len_on_MatchesList"""

    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    pattern = 'pos="VB" pos="DT"? pos="JJ"* pos="NN" pos="."' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']
    aMatchesList = pyrata.re.finditer(pattern, data)
    success = False
    if len(aMatchesList) == 5:
      success = True
    self.assertTrue(success)


  # ----------------------------------------------------------------------
  def test_search_step_in_empty_data_wo_lexicon(self):
    """Test search method in empty data."""
    pattern = 'pos="JJ"'
    data = []
    expected =None
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result,expected)

  # ----------------------------------------------------------------------
  def test_finditer_step_in_empty_data_wo_lexicon(self):
    """Test finditer method in empty data."""
    pattern = 'pos="JJ"'
    data = []
    expected =None
    result = pyrata.re.finditer(pattern, data)
    self.assertEqual(result,expected)

  # ----------------------------------------------------------------------
  def test_search_step_in_empty_data_wi_lexicon(self):
    """Test search method in empty data with a lexicon."""
    pattern = 'pos="JJ"'
    data = []
    expected =None
    result = pyrata.re.search(pattern, data, lexicons = {'mylexicon':['a', 'b']})
    self.assertEqual(result,expected)

  # ----------------------------------------------------------------------
  def test_finditer_step_in_empty_data_wi_lexicon(self):
    """Test finditer method in empty data with a lexicon."""
    pattern = 'pos="JJ"'
    data = []
    expected =None
    result = pyrata.re.finditer(pattern, data, lexicons = {'mylexicon':['a', 'b']})
    self.assertEqual(result,expected)


  # ----------------------------------------------------------------------
  def test_search_apostrophe_in_constraint_value(self):
    """Test search apostrophe in constraint value. The pattern fires at some points."""
    pattern = 'raw~"n\'t"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'MD', 'raw': 'can\'t'}]
    expected = [{'pos': 'MD', 'raw': 'can\'t'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected)

  # ----------------------------------------------------------------------
  def test_search_wi_an_empty_constraint_value(self):
    """Test search wi empty constraint value. The pattern fires at some points."""
    # python3 pyrata_re.py 'raw~"\""' "[{'raw':'\"'}]"
    pattern = 'raw=""'
    data = [{'raw': ''}]
    expected = [{'raw': ''}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(),expected) 


# --------------------------------------------------------------------------------------
# double quotes
# --------------------------------------------------------------------------------------


  # # ----------------------------------------------------------------------
  # def test_search_sequence_wi_backslashed_double_quotation_mark_in_constraint_value_wo_backslached_mark_in_data(self):
  #   """Test search backslached double quotation mark  in constraint value _wo_backslached_mark_in_data. The pattern fires at some points."""
  #   # python3 pyrata_re.py 'raw~"\""' "[{'raw':'\"'}]"
  #   pattern = 'raw="\"" next="value"'
  #   data = [{'raw': '"'}]
  #   expected = [{'raw': '"'}]
  #   result = pyrata.re.search(pattern, data)
  #   self.assertEqual(result.group(),expected) 

  # # ----------------------------------------------------------------------
  # def test_search_backslashed_double_quotation_mark_in_constraint_value_wo_backslached_mark_in_data(self):
  #   """Test search backslached double quotation mark  in constraint value _wo_backslached_mark_in_data. The pattern fires at some points."""
  #   # python3 pyrata_re.py 'raw~"\""' "[{'raw':'\"'}]"
  #   pattern = 'raw="\""'
  #   data = [{'raw': '"'}]
  #   expected = [{'raw': '"'}]
  #   result = pyrata.re.search(pattern, data)
  #   self.assertEqual(result.group(),expected) 

  # # ----------------------------------------------------------------------
  # def test_search_backslashed_double_quotation_mark_something_in_constraint_value_wo_backslached_mark_in_data(self):
  #   """Test search backslached double quotation mark  in constraint value _wo_backslached_mark_in_data. The pattern fires at some points."""
  #   # python3 pyrata_re.py 'raw~"\""' "[{'raw':'\"'}]"
  #   pattern = 'raw="\"something"'
  #   data = [{'raw': '"something'}]
  #   expected = [{'raw': '"something'}]
  #   result = pyrata.re.search(pattern, data)
  #   self.assertEqual(result.group(),expected) 

  # # ----------------------------------------------------------------------
  # def test_search_something_backslashed_double_quotation_mark_in_constraint_value_wo_backslached_mark_in_data(self):
  #   """Test search backslached double quotation mark  in constraint value _wo_backslached_mark_in_data. The pattern fires at some points."""
  #   # python3 pyrata_re.py 'raw~"\""' "[{'raw':'\"'}]"
  #   pattern = 'raw="something\""'
  #   data = [{'raw': 'something"'}]
  #   expected = [{'raw': 'something"'}]
  #   result = pyrata.re.search(pattern, data)
  #   self.assertEqual(result.group(),expected) 

  # # ----------------------------------------------------------------------
  # def test_search_backslashed_double_quotation_mark_something_backslashed_double_quotation_mark_in_constraint_value_wo_backslached_mark_in_data(self):
  #   """Test search backslached double quotation mark  in constraint value _wo_backslached_mark_in_data. The pattern fires at some points."""
  #   # python3 pyrata_re.py 'raw~"\""' "[{'raw':'\"'}]"
  #   pattern = 'raw="\"something\""'
  #   data = [{'raw': '"something"'}]
  #   expected = [{'raw': '"something"'}]
  #   result = pyrata.re.search(pattern, data)
  #   self.assertEqual(result.group(),expected) 




  # ----------------------------------------------------------------------
  def test_finditer_2_element_pattern_1st_e_quantified_matching_2_consecutive_tok_wi_same_constraint_2nd_e_matching_2nd_tok_wi_distinct_constraint(self):
    """Test finditer pattern made of two elements, the first one being quantified 
    and matching two consecutive data tokens with the same constraint
    and the latter matching only the second data token thanks to another constraint. """    
    lexicons = {'LEX':['B']}    
    pattern = '(a~"A|B"+) (b@"LEX")'
    data = [{'c':'C'}, {'a':'A'}, {'a':'A', 'b':'B'}, {'d':'D'}]
    expected = [ {'a':'A', 'b':'B'}]
    result = pyrata.re.finditer(pattern, data, lexicons = lexicons)
    for e in result:
      self.assertEqual(e.group(2),expected) 

  # ----------------------------------------------------------------------
  def test_finditer_2_element_pattern_1st_e_quantified_matching_2_consecutive_tok_wi_same_constraint_2nd_e_matching_2nd_tok_wi_same_constraint_key(self):
    """Test finditer pattern made of two elements, the first one being quantified 
    and matching two consecutive data tokens with the same constraint
    and the latter matching only the second data token thanks to constraint having the same key as the first one. """ 
    lexicons = {'LEX':['B']}    
    pattern = '(a~"A|B"+) (a@"LEX")'
    data = [{'c':'C'}, {'a':'A'}, {'a':'B'}, {'d':'D'}]
    expected = [{'a':'B'}]
    result = pyrata.re.finditer(pattern, data, lexicons = lexicons)
    for e in result:
      self.assertEqual(e.group(2),expected) 

  # ----------------------------------------------------------------------
  def test_search_2_element_pattern_1st_e_quantified_matching_2_consecutive_tok_wi_same_constraint_2nd_e_matching_2nd_tok_wi_distinct_constraint_key_and_lexicon(self):
    """Test search pattern made of two elements, the first one being quantified matching two consecutive data tokens 
    and the latter matching only the second data token.  The pattern is present in the data."""
    lexicons = {'LEX':['B']}    
    pattern = '(a~"A|B"+) (b@"LEX")'
    data = [{'c':'C'}, {'a':'A'}, {'a':'A', 'b':'B'}, {'d':'D'}]
    expected = [ {'a':'A', 'b':'B'}]
    result = pyrata.re.search(pattern, data, lexicons = lexicons)
    self.assertEqual(result.group(2),expected) 


  # ----------------------------------------------------------------------
  def test_search_2_element_pattern_1st_e_quantified_matching_2_consecutive_tok_wi_same_constraint_2nd_e_matching_2nd_tok_wi_distinct_constraint_key_and_equal(self):
    """Test search pattern made of two elements, the first one being quantified matching two consecutive data tokens 
    and the latter matching only the second data token.  """
    pattern = '(a~"A|B"+) (b="B")'
    data = [{'c':'C'}, {'a':'A'}, {'a':'A', 'b':'B'}, {'d':'D'}]
    expected = [ {'a':'A', 'b':'B'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(2),expected) 

  # ----------------------------------------------------------------------
  def test_search_2_element_pattern_1st_e_matching_1st_tok_2nd_e_matching_2nd_tok(self):
    """Test search pattern made of two elements, the first one no quantified matching the first data token 
    and the latter matching only the second data token. """
    pattern = '(a~"A|B") (b="B")'
    data = [{'c':'C'}, {'a':'A'}, {'a':'A', 'b':'B'}, {'d':'D'}]
    expected = [ {'a':'A', 'b':'B'}]
    result = pyrata.re.search(pattern, data)
    self.assertEqual(result.group(2),expected) 

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='do_tests_py.log', level=logging.DEBUG)
  # logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='do_tests_py.log', level=logging.INFO)
  logger = logging.getLogger()

  # SET HERE True or False
  logger.disabled = True

  unittest.main()
  