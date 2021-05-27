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

"""

control cpu time and memory usage of a simple pyrata use case: part-of-speech (POS) patterns to find and extract NPs


"""

import logging
from timeit import Timer

import nltk
from nltk.corpus import brown
import nltk.chunk
from nltk.chunk.regexp import *


import pyrata.re as pyrata_re


def toPyRATAFormat(pos_tags):
  return [{'raw':w, 'pos':p} for (w, p) in pos_tags]

def test_noun_phrase(dictlist):
  """                            
  """

  #print ('Measuring time performance on # {} words over # {} iterations for recognizing Noun Phrases'.format(size, iteration_number))
  #print ('analyzer_name,\tpattern_grammar,\taveragetime,\tmintime')

  # ----------------------------------------------------
  # pyrata 
  # ----------------------------------------------------
  #analyzer_name='pyrata'

  #sentence = 'A great sentence .'
  #dictlist =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
  #global dictlist 

  #global pyrata_grammar

  pyrata_grammar = 'pos="DT"? pos="JJ"* pos="NN"+'
  pyrata_grammar = 'pos="DT"? [pos="NN" | pos="JJ"]* [pos="NN" | pos="NNS"]+'
  pyrata_grammar = 'pos="DT"? [pos~"NN|JJ"]* pos~"NN.*"+'
  #nfa_pyrata_findall_result = []
  #nfa_pyrata_findall_result = 
  return pyrata_re.findall(pyrata_grammar, dictlist)
#  print ('{}\t{}\t{}\t{}'.format(analyzer_name, pyrata_grammar, averagetime, mintime))





# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Control time memory usage
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

#
#  logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='system-performance.log', level=logging.INFO)
#  logger = logging.getLogger()
#  logger.disabled = True

  # ----------------------------------------------------
  # data 
  # ----------------------------------------------------
  # brown

  size = 1000 # 1161192 # # brown corpus 1 161 192 words ; can also be interpreted as number of sentences

  print ('Info: Start...')
  print ('Info: get {} brown.words'.format(size))
  tokens = brown.words()
  tokens = tokens[:size]

  print ('Info: annotate pos_tag ({} tokens)'.format(len(tokens)))
  print('Info: annotate pos_tag ({} unique tokens)'.format(len(set(tokens))))

  pos_tags = nltk.pos_tag(tokens)

  print ('Info: convert to pyrata format ')
  dictlist = toPyRATAFormat(pos_tags)

  print ('Info: control pyrata cpu time and memory usage')
  test_noun_phrase(dictlist)

  print ('Info: end.')
