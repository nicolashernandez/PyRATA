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
part-of-speech (POS) patterns to find and extract NPs

compare the time performance of pyrata with

pattern
http://www.clips.ua.ac.be/pages/pattern-search
The search() function takes a string (e.g., a word or a sequence of words) and returns a list of non-overlapping matches in the given sentence. 
The match() function returns the first match, or None.

python.chunk
http://www.nltk.org/book/ch07.html
http://www.nltk.org/howto/chunk.html
http://www.nltk.org/_modules/nltk/chunk.html

spacy
https://spacy.io/

textblob
http://rwet.decontextualize.com/book/textblob/

re

Reference
=========

Justeson, J., & Katz, S. (1995). Technical terminology: Some linguistic properties and an algorithm for identification in text. Natural Language Engineering, 1(1), 9-27.
https://brenocon.com/JustesonKatz1995.pdf


"""

import logging
from timeit import Timer

import nltk
from nltk.corpus import brown
import nltk.chunk
from nltk.chunk.regexp import *




import pyrata.re as pyrata_re




# time pattern v1
# https://stackoverflow.com/questions/27863832/calling-python-2-script-from-python-3
# ---------------------------------------------------------
import subprocess
def measure_pattern_time_v1(iteration_number, size, pattern):
  """ pattern """
  python2_command = 'python more/measure_pattern_time_v1.py %s %s %s' % (iteration_number, size, pattern)  # launch your python2 script using bash  arg1 arg2
  process = subprocess.Popen(python2_command.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()  # receive output from the python2 script
  return output #.replace('\n','')


# time pattern v2
# https://stackoverflow.com/questions/27863832/calling-python-2-script-from-python-3
# ---------------------------------------------------------
import execnet

def measure_pattern_time_v2(iteration_number, size, pattern):
  gw      = execnet.makegateway("popen//python=python2.7")
  channel = gw.remote_exec("""
from nltk.corpus import brown
words = brown.words()[:%s]
text = ' '.join(words)
from pattern.en import parsetree
text_tree = parsetree(text,
 tokenize = True,         # Split punctuation marks from words?
     tags = True,         # Parse part-of-speech tags? (NN, JJ, ...)
   chunks = False,         # Parse chunks? (NP, VP, PNP, ...)
relations = False,        # Parse chunk relations? (-SBJ, -OBJ, ...)
  lemmata = False,        # Parse lemmata? (ate => eat)
 encoding = 'utf-8',       # Input string encoding.
   tagset = None)         # Penn Treebank II (default) or UNIVERSAL.
from pattern.search import search
def measure_pattern_search():
  global pattern_search_result    #Make measure_me able to modify the value
  pattern_search_result = search("%s", text_tree)
  #print ("clip.pattern len(result)="+str(len(pattern_search_result)))
from timeit import Timer
pattern_search_time = Timer(measure_pattern_search)
#print ('pattern_search_time')
def pattern_search_timeit():
  runtimes = [pattern_search_time.timeit(number=1) for i in range (0, %s)]
  average = sum(runtimes)/len(runtimes)
#  return ''.join(['timit: #runs=', str(%s), ' ; average=', str(average),' ; min=', str(min(runtimes))])
  return [runtimes, average, min(runtimes), len(pattern_search_result)]
channel.send(pattern_search_timeit())
  """ % (size, pattern, iteration_number, iteration_number))
  channel.send([])
  return channel.receive()



def measure_time (Function, iteration_number):
  function_time = Timer(Function)
  runtimes = [function_time.timeit(number=1) for i in range (0, iteration_number)]
  average = sum(runtimes)/len(runtimes)
  return runtimes, average, min(runtimes)


def nltk_regex_parser():
  global nltk_regex_parser_result # tree
  nltk_regex_parser_result = regex_parser.parse(pos_tags)
  print (len(nltk_regex_parser_result))

def nltk_regex_chunker_parser():
  global nltk_regex_chunk_parser_result # tree
  nltk_regex_chunk_parser_result = chunk_parser.parse(pos_tags)
  print (len(nltk_regex_chunk_parser_result))


def spacy_rule_based_matcher():
  global spacy_rule_based_matcher_result # tree
  spacy_rule_based_matcher_result = matcher(doc)
  print (len(spacy_rule_based_matcher_result)) 


def measure_pyrata_findall():
  global pyrata_findall_result
  pyrata_findall_result = pyrata_re.findall(pyrata_grammar, dictlist)
  print (len(pyrata_findall_result)) 

def measure_nfa_pyrata_findall():
  global nfa_pyrata_findall_result
  nfa_pyrata_findall_result = pyrata_re.findall(pyrata_grammar, dictlist)
  print (len(nfa_pyrata_findall_result)) 

def time_noun_phrase_recognizers(size, analysers):
  """                            
  """

  print ('Measuring time performance on # {} words over # {} iterations for recognizing Noun Phrases'.format(size, iteration_number))
  print ('analyzer_name,\tpattern_grammar,\taveragetime,\tmintime')

  # # ----------------------------------------------------
  # # pattern 
  # # ----------------------------------------------------
  analyzer_name = 'clips.pattern'
  if analyzer_name in analysers: 

    global grammar 
    # http://www.clips.ua.ac.be/pages/pattern-search
    # | ADJP|ADVP Separator for different options.
    # * JJ* Used as a wildcard character.
    # ? JJ? Used as a suffix, constraint is optional.
    # + RB|JJ+ or JJ?+ or *+  Used as a suffix, constraint can span multiple words.


    # # # v1 
    # # pattern_time = measure_pattern_time_v1(iteration_number, size, grammar)
    # # print ('pattern_time_v1:', pattern_time)
    # # # can also be called by
    # # # python benchmark/measure_pattern_time_v1.py 1 1000 "DT? JJ|NN?+ NN"

    # v2
    pattern_grammar = 'DT? JJ?+ NN+'
    runtimes, averagetime, mintime, len_matches = measure_pattern_time_v2(iteration_number, size, pattern_grammar)
    #print ('{}'.format(len_matches))
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, pattern_grammar, averagetime, mintime, len_matches))

    #pattern_time = measure_pattern_time_v2(iteration_number, size, grammar)
    pattern_grammar = 'DT? JJ|NN?+ NN|NNS'
    runtimes, averagetime, mintime, len_matches = measure_pattern_time_v2(iteration_number, size, pattern_grammar)
    #print ('{}'.format(len_matches))
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, pattern_grammar, averagetime, mintime, len_matches))

    pattern_grammar = 'DT? JJ|NN?+ NN|NNS+'
    runtimes, averagetime, mintime, len_matches = measure_pattern_time_v2(iteration_number, size, pattern_grammar)
    #print ('{}'.format(len_matches))
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, pattern_grammar, averagetime, mintime, len_matches))

    #print ('pattern_time_v2: grammar={} {}'.format(grammar,pattern_time))


  # ----------------------------------------------------
  # data 
  # ----------------------------------------------------
  # brown

  tokens = brown.words()
  #if size != -1:
  tokens = tokens[:size]
  #  size = len(tokens)
  #print ('Info: brown.words size={}'.format(size))
  
  #print ('Info: pos_tag ')
  global pos_tags 
  pos_tags = nltk.pos_tag(tokens)


  # ----------------------------------------------------
  # nltk chunker regexparser
  # ----------------------------------------------------
  analyzer_name = 'nltk_regex_parser'
  if analyzer_name in analysers: 

    global regex_parser 

    nltk_grammar = "NP: {<DT>?<JJ>*<NN>+}"
    nltk_regexparser_result = []
    regex_parser = nltk.RegexpParser(nltk_grammar)
    runtimes, averagetime, mintime = measure_time(nltk_regex_parser, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, nltk_grammar, averagetime, mintime, str(len(nltk_regexparser_result))))


    nltk_regexparser_result = []
    nltk_grammar = "NP: {<DT>?<JJ|NN>*<NN|NNS>}"
    regex_parser = nltk.RegexpParser(nltk_grammar)
    #for subtree in nltk_regexparser_result.subtrees():
    #  if subtree.label() == "NP":
    #    print("NP: "+str(subtree.leaves()))
   
    runtimes, averagetime, mintime = measure_time(nltk_regex_parser, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, nltk_grammar, averagetime, mintime, str(len(nltk_regexparser_result))))


    nltk_grammar = "NP: {<DT>?<JJ|NN>*<NN.*>}"
    nltk_regexparser_result = []
    regex_parser = nltk.RegexpParser(nltk_grammar)
    runtimes, averagetime, mintime = measure_time(nltk_regex_parser, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, nltk_grammar, averagetime, mintime, str(len(nltk_regexparser_result))))


  # ----------------------------------------------------
  # nltk chunker regex_chunker_parser
  # ----------------------------------------------------

  analyzer_name = 'nltk_regex_chunk_parser'
  if analyzer_name in analysers: 

    global chunk_parser 

    nltk_regex_chunk_grammar = "<DT>?<JJ>*<NN>+"
    chunk_rule = ChunkRule(nltk_regex_chunk_grammar, "Noun Phrase")
    chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
    nltk_regex_chunk_parser_result = []
    runtimes, averagetime, mintime = measure_time(nltk_regex_chunker_parser, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, nltk_regex_chunk_grammar, averagetime, mintime, str(len(nltk_regex_chunk_parser_result))))


    nltk_regex_chunk_grammar = "<DT>?<JJ|NN>*<NN|NNS>"
    chunk_rule = ChunkRule(nltk_regex_chunk_grammar, "Noun Phrase")
    chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
    nltk_regex_chunk_parser_result = []
    runtimes, averagetime, mintime = measure_time(nltk_regex_chunker_parser, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, nltk_regex_chunk_grammar, averagetime, mintime, str(len(nltk_regex_chunk_parser_result))))


    nltk_regex_chunk_grammar = "<DT>?<JJ|NN>*<NN.*>"
    chunk_rule = ChunkRule(nltk_regex_chunk_grammar, "Noun Phrase")
    chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
    nltk_regex_chunk_parser_result = []
    runtimes, averagetime, mintime = measure_time(nltk_regex_chunker_parser, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, nltk_regex_chunk_grammar, averagetime, mintime, str(len(nltk_regex_chunk_parser_result))))



  # ----------------------------------------------------
  # spacy v1.x
  # ----------------------------------------------------
  import spacy                           # See "Installing spaCy"
  from spacy.matcher import Matcher
  # https://github.com/explosion/spaCy/blob/master/spacy/attrs.pyx
  # https://github.com/explosion/spaCy/issues/882

  from spacy.attrs import IS_PUNCT, LOWER, POS

  # text = ' '.join(tokens)
  # nlp = spacy.load('en')                 # You are here.
  # global matcher 
  # analyzer_name = 'spaCy'
  
  # spacy_grammar = [{POS: "DET", 'OP':"?"}, {POS: "ADJ", 'OP':"*"}, {POS: "NOUN", 'OP':"+"}]
  # matcher = Matcher(nlp.vocab)
  # matcher.add_pattern("NounPhrase", spacy_grammar)
  # # # matcher.add_pattern("NounPhrase", [{POS: "DET", 'OP':"?"}, {POS: "ADJ", 'OP':"*"}, {POS: "NOUN"}])
  # # #<DT>?<JJ|NN>*<NN|NNS>
  # global doc
  # doc = nlp(text)
  # # matches = matcher(doc)
  # # matches
  # # for ent_id, label, start, end in matches:
  # #   span = doc[start:end]
  # #   # First token is our noun_phrase_0
  # #   np_0 = span[0]
  # #   # Last token is noun_phrase_1
  # #   np_1 = span[-1]
  # #   print("span({})".format(span))
  # spacy_rule_based_matcher_result = []
  # runtimes, averagetime, mintime = measure_time(spacy_rule_based_matcher, iteration_number)
  # print ('{}\t{}\t{}\t{}'.format(analyzer_name, spacy_grammar, averagetime, mintime))


  # ----------------------------------------------------
  # spacy v2.0.
  # https://spacy.io/usage/v2#features-matcher
  # ----------------------------------------------------

  analyzer_name = 'spaCy'
  if analyzer_name in analysers: 
    text = ' '.join(tokens)
    print ("Debug: done - text = ' '.join(tokens) ")

    nlp = spacy.load('en',  disable=['ner', 'parser', 'textcat'])   #  disable=['tagger', 'ner']  'parser', 'ner' or 'textcat'.            # You are here.
    global matcher 

    spacy_grammar = [{POS: "DET", 'OP':"?"}, {POS: "ADJ", 'OP':"*"}, {POS: "NOUN", 'OP':"+"}]
    matcher = Matcher(nlp.vocab)
    matcher.add ("NounPhrase", None, spacy_grammar)
    # # matcher.add_pattern("NounPhrase", [{POS: "DET", 'OP':"?"}, {POS: "ADJ", 'OP':"*"}, {POS: "NOUN"}])
    # #<DT>?<JJ|NN>*<NN|NNS>
    global doc
    doc = nlp(text)
    print ("Debug: done - doc = nlp(text)")

    # matches = matcher(doc)
    # matches
    # for ent_id, label, start, end in matches:
    #   span = doc[start:end]
    #   # First token is our noun_phrase_0
    #   np_0 = span[0]
    #   # Last token is noun_phrase_1
    #   np_1 = span[-1]
    #   print("span({})".format(span))
    spacy_rule_based_matcher_result = []
    runtimes, averagetime, mintime = measure_time(spacy_rule_based_matcher, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, spacy_grammar, averagetime, mintime, str(len(spacy_rule_based_matcher_result))))


  # ----------------------------------------------------
  # pyrata 
  # ----------------------------------------------------
  analyzer_name='pyrata'
  if analyzer_name in analysers: 

    #sentence = 'A great sentence .'
    #dictlist =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
    global dictlist 
    dictlist = [{'raw':w, 'pos':p} for (w, p) in pos_tags]
    global pyrata_grammar

    pyrata_grammar = 'pos="DT"? pos="JJ"* pos="NN"+'
    nfa_pyrata_findall_result = []
    #runtimes, averagetime, mintime = measure_time(measure_pyrata_findall, iteration_number)  
    runtimes, averagetime, mintime = measure_time(measure_nfa_pyrata_findall, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, pyrata_grammar, averagetime, mintime, str(len(nfa_pyrata_findall_result))))

    pyrata_grammar = 'pos="DT"? [pos="NN" | pos="JJ"]* [pos="NN" | pos="NNS"]'
    nfa_pyrata_findall_result = []
     #runtimes, averagetime, mintime = measure_time(measure_pyrata_findall, iteration_number)  
    runtimes, averagetime, mintime = measure_time(measure_nfa_pyrata_findall, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, pyrata_grammar, averagetime, mintime, str(len(nfa_pyrata_findall_result))))


    pyrata_grammar = 'pos="DT"? [pos~"NN|JJ"]* pos~"NN.*"'
    nfa_pyrata_findall_result = []
  # #  runtimes, averagetime, mintime = measure_time(measure_pyrata_findall, iteration_number)  
    runtimes, averagetime, mintime = measure_time(measure_nfa_pyrata_findall, iteration_number)
    print ('{}\t{}\t{}\t{}\t{}'.format(analyzer_name, pyrata_grammar, averagetime, mintime, str(len(nfa_pyrata_findall_result))))




# output pattern v2
# https://stackoverflow.com/questions/27863832/calling-python-2-script-from-python-3
# ---------------------------------------------------------

def write_pattern_v2(iteration_number, size, pattern):
  gw      = execnet.makegateway("popen//python=python2.7")
  channel = gw.remote_exec("""
from nltk.corpus import brown
size = %s
words = brown.words()[:size]
text = ' '.join(words)
from pattern.en import parsetree
text_tree = parsetree(text,
 tokenize = True,         # Split punctuation marks from words?
     tags = True,         # Parse part-of-speech tags? (NN, JJ, ...)
   chunks = False,         # Parse chunks? (NP, VP, PNP, ...)
relations = False,        # Parse chunk relations? (-SBJ, -OBJ, ...)
  lemmata = False,        # Parse lemmata? (ate => eat)
 encoding = 'utf-8',       # Input string encoding.
   tagset = None)         # Penn Treebank II (default) or UNIVERSAL.
def backslash(string):
  for ch in [' ','?', '+', '*', '.', '[', ']', '~' , '{', '}', '|', '"', "'", ',', ':', '<', '>']:
    if ch in string:
      string=string.replace(ch,'_')
  return string  
from pattern.search import search
pattern = "%s"
pattern_search_result = search(pattern, text_tree)
measure_pattern_search()
filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(pattern_search_result))+'_'+backslash(pattern)
thefile = open(filename, 'w')
for item in pattern_search_result:
  print>>thefile, item
channel.send([filename, size, len(pattern_search_result)])
  """ % (size, pattern, iteration_number, iteration_number))
  channel.send([])
  return channel.receive()  

def output_noun_phrase_recognizers(size):
  """                            
  """

  print ('Measuring time performance on # {} words over # {} iterations for recognizing Noun Phrases'.format(size, iteration_number))
  print ('analyzer_name,\tpattern_grammar,\taveragetime,\tmintime')

  # # ----------------------------------------------------
  # # pattern 
  # # ----------------------------------------------------
  analyzer_name = 'clips.pattern'
  global grammar 
  # http://www.clips.ua.ac.be/pages/pattern-search
  # | ADJP|ADVP Separator for different options.
  # * JJ* Used as a wildcard character.
  # ? JJ? Used as a suffix, constraint is optional.
  # + RB|JJ+ or JJ?+ or *+  Used as a suffix, constraint can span multiple words.


  # # # v1 
  # # pattern_time = measure_pattern_time_v1(iteration_number, size, grammar)
  # # print ('pattern_time_v1:', pattern_time)
  # # # can also be called by
  # # # python benchmark/measure_pattern_time_v1.py 1 1000 "DT? JJ|NN?+ NN"

  # v2
  pattern_grammar = 'DT? JJ?+ NN+'
  filename, data_size, result_size = write_pattern_v2(iteration_number, size, pattern_grammar)
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, pattern_grammar, result_size, filename))

  #pattern_time = measure_pattern_time_v2(iteration_number, size, grammar)
  pattern_grammar = 'DT? JJ|NN?+ NN|NNS'
  filename, data_size, result_size = write_pattern_v2(iteration_number, size, pattern_grammar)
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, pattern_grammar, result_size, filename))

  pattern_grammar = 'DT? JJ|NN?+ NN|NNS+'
  filename, data_size, result_size  = write_pattern_v2(iteration_number, size, pattern_grammar)
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, pattern_grammar, result_size, filename))

  #print ('pattern_time_v2: grammar={} {}'.format(grammar,pattern_time))


  # ----------------------------------------------------
  # data 
  # ----------------------------------------------------
  # brown

  tokens = brown.words()
  #if size != -1:
  tokens = tokens[:size]
  #  size = len(tokens)
  #print ('Info: brown.words size={}'.format(size))
  
  #print ('Info: pos_tag ')
  global pos_tags 
  pos_tags = nltk.pos_tag(tokens)


  # ----------------------------------------------------
  # nltk chunker regexparser
  # ----------------------------------------------------
  analyzer_name = 'nltk_regex_parser'
  global regex_parser 

  grammar = "NP: {<DT>?<JJ>*<NN>+}"
  result = []
  regex_parser = nltk.RegexpParser(grammar)
  result = regex_parser.parse(pos_tags)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  result_list = []
  for subtree in result.subtrees():
    if subtree.label() == "NP":
      result_list.append(str(subtree.leaves()))
  thefile = open(filename, 'w')
  thefile.write("\n".join(result_list))
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result_list), filename))



  grammar = "NP: {<DT>?<JJ|NN>*<NN|NNS>}"
  result = []
  regex_parser = nltk.RegexpParser(grammar)
  result = regex_parser.parse(pos_tags)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  result_list = []
  for subtree in result.subtrees():
    if subtree.label() == "NP":
      result_list.append(str(subtree.leaves()))
  thefile = open(filename, 'w')
  thefile.write("\n".join(result_list))
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result_list), filename))


  grammar = "NP: {<DT>?<JJ|NN>*<NN.*>}"
  result = []
  regex_parser = nltk.RegexpParser(grammar)
  result = regex_parser.parse(pos_tags)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  result_list = []
  for subtree in result.subtrees():
    if subtree.label() == "NP":
      result_list.append(str(subtree.leaves()))
  thefile = open(filename, 'w')
  thefile.write("\n".join(result_list))
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result_list), filename))


  # ----------------------------------------------------
  # nltk chunker regex_chunker_parser
  # ----------------------------------------------------

  analyzer_name = 'nltk_regex_chunk_parser'
  global chunk_parser 

  grammar = "<DT>?<JJ>*<NN>+"
  chunk_rule = ChunkRule(grammar, "Noun Phrase")
  chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
  result = []
  result = chunk_parser.parse(pos_tags)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  result_list = []
  for subtree in result.subtrees():
    if subtree.label() == "NP":
      result_list.append(str(subtree.leaves()))
  thefile = open(filename, 'w')
  thefile.write("\n".join(result_list))
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result_list), filename))

  grammar = "<DT>?<JJ|NN>*<NN|NNS>"
  chunk_rule = ChunkRule(grammar, "Noun Phrase")
  chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
  result = []
  result = chunk_parser.parse(pos_tags)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  result_list = []
  for subtree in result.subtrees():
    if subtree.label() == "NP":
      result_list.append(str(subtree.leaves()))
  thefile = open(filename, 'w')
  thefile.write("\n".join(result_list))
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result_list), filename))



  grammar = "<DT>?<JJ|NN>*<NN.*>"
  chunk_rule = ChunkRule(grammar, "Noun Phrase")
  chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
  result = []
  result = chunk_parser.parse(pos_tags)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  result_list = []
  for subtree in result.subtrees():
    if subtree.label() == "NP":
      result_list.append(str(subtree.leaves()))
  thefile = open(filename, 'w')
  thefile.write("\n".join(result_list))
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result_list), filename))




  # ----------------------------------------------------
  # spacy v1.x
  # ----------------------------------------------------
  import spacy                           # See "Installing spaCy"
  from spacy.matcher import Matcher
  # https://github.com/explosion/spaCy/blob/master/spacy/attrs.pyx
  # https://github.com/explosion/spaCy/issues/882

  from spacy.attrs import IS_PUNCT, LOWER, POS


  # ----------------------------------------------------
  # spacy v2.0.
  # https://spacy.io/usage/v2#features-matcher
  # ----------------------------------------------------
# https://spacy.io/api/matcher
# from spacy.matcher import Matcher
# matcher = Matcher(nlp.vocab)
# pattern = [{'LOWER': "hello"}, {'LOWER': "world"}]
# matcher.add("HelloWorld", None, pattern)
# doc = nlp(u'hello world!')
# matches = matcher(doc)


  text = ' '.join(tokens)
  print ("Debug: done - text = ' '.join(tokens) ")

  nlp = spacy.load('en',  disable=['ner', 'parser', 'textcat'])   #  disable=['tagger', 'ner']  'parser', 'ner' or 'textcat'.            # You are here.
  global matcher 
  analyzer_name = 'spaCy'
  
  grammar = [{POS: "DET", 'OP':"?"}, {POS: "ADJ", 'OP':"*"}, {POS: "NOUN", 'OP':"+"}]


  matcher = Matcher(nlp.vocab)
  matcher.add ("NounPhrase", None, grammar)
  # # matcher.add_pattern("NounPhrase", [{POS: "DET", 'OP':"?"}, {POS: "ADJ", 'OP':"*"}, {POS: "NOUN"}])
  # #<DT>?<JJ|NN>*<NN|NNS>
  global doc
  doc = nlp(text)
  print ('Debug: done - spacy doc = nlp(text) ')
  # matches = matcher(doc)
  # matches
  # for ent_id, label, start, end in matches:
  #   span = doc[start:end]
  #   # First token is our noun_phrase_0
  #   np_0 = span[0]
  #   # Last token is noun_phrase_1
  #   np_1 = span[-1]
  #   print("span({})".format(span))
  result = []
  result = matcher(doc)
  result_list = []
  for ent_id, start, end in result:
    span = doc[start:end]
    # First token is our noun_phrase_0
    np_0 = span[0]
    # Last token is noun_phrase_1
    np_1 = span[-1]
    #result_list.append([span.text, str(start), str(end)])
    result_list.append(span.text)

  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+str(backslash(grammar))
  thefile = open(filename, 'w')
  #thefile.write("\n".join([' '.join(r) for r in result_list]))
  thefile.write("\n".join(result_list))
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, str(grammar), len(result_list), filename))

  # ----------------------------------------------------
  # pyrata 
  # ----------------------------------------------------
  analyzer_name='pyrata'

  #sentence = 'A great sentence .'
  #dictlist =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
  global dictlist 
  dictlist = [{'raw':w, 'pos':p} for (w, p) in pos_tags]
  global pyrata_grammar

  grammar = 'pos="DT"? pos="JJ"* pos="NN"+'
  result = []
  result = pyrata_re.findall(pyrata_grammar, dictlist)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  thefile = open(filename, 'w')
  for item in result:
    print>>thefile, item
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result), filename))



  grammar = 'pos="DT"? [pos="NN" | pos="JJ"]* [pos="NN" | pos="NNS"]'
  result = []
  result = pyrata_re.findall(pyrata_grammar, dictlist)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  thefile = open(filename, 'w')
  for item in result:
    print>>thefile, item
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result), filename))

  grammar = 'pos="DT"? [pos~"NN|JJ"]* pos~"NN.*"'
  result = []
  result = pyrata_re.findall(pyrata_grammar, dictlist)
  filename = '/tmp/benchmark_'+analyzer_name+'_'+str(size)+"_"+str(len(result))+'_'+backslash(grammar)
  thefile = open(filename, 'w')
  for item in result:
    print>>thefile, item
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, len(result), filename))


def nltk_parse_clause(sentence):
  """
  Natural Language Toolkit: code_cascaded_chunker
  http://www.nltk.org/book/ch07.html#code-cascaded-chunker
  """
  grammar = r"""
  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP>}               # Chunk prepositions followed by NP
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
  CLAUSE: {<NP><VP>}           # Chunk NP, VP
  """
  cp = nltk.RegexpParser(grammar)
  #sentence = [("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"),  ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
  parsed_sentence = cp.parse(sentence)
  #print('parsed_sentence=', parsed_sentence)

def nltk_parse_clause_in_the_whole_text():
  for s in brown_pos_tag_sents:
    nltk_parse_clause(s)

def pyrata_recognize_clause_in_short(sentence_dict_list):
  # http://www.nltk.org/book/ch07.html # Building Nested Structure with Cascaded Chunkers
#    sentence = [("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"),
#      ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
#   sentence = [("John", "NNP"), ("thinks", "VBZ"), ("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"), ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
#   data = [{'raw':w, 'pos':p} for (w, p) in sentence]
#   print ('Debug:', data)

  # NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN :      can   
  # extend pattern='pos~"DT|JJ|NN.*"+' annotation={'ch1':'NP'} iob = True 
  action = 'extend'
  group = [0]
  iob = True
  pattern = 'pos~"DT|JJ|NN.*"+'
  annotation = {'ch1':'NP'}
  result_NP = pyrata_re.annotate (pattern, annotation, sentence_dict_list, group, action, iob)
  #print ('Debug: ch1 NP=',result_NP)

  #PP: {<IN><NP>}               # Chunk prepositions followed by NP :  may   
  #extend pattern='pos="IN" ch1-"NP"' annotation={'ch2':'PP'} iob = True 
  #       pattern='pos="IN" (ch1="B-NP" ch1="I-NP"*)"
  pattern = 'pos="IN" (ch1="B-NP" ch1="I-NP"*)'
  annotation = {'ch2':'PP'}
  result_PP = pyrata_re.annotate (pattern, annotation, result_NP, group, action, iob)
  #rint ('Debug: ch2 PP=',result_PP)

  # VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments :    might 
  # extend pattern='pos~"VB.*" (ch1-"NP"|ch2-"PP"|ch3-"CLAUSE")+$' annotation={'ch4':'VP'} iob = True
   #       pattern='pos~"VB.*" (ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$'
  pattern = 'pos~"VB.*" (ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$' 
  annotation = {'ch4':'VP'}
  result_VP = pyrata_re.annotate (pattern, annotation, result_PP, group, action, iob)
  #print ('Debug: ch4 VP=',result_VP)


  # CLAUSE: {<NP><VP>}           # Chunk NP, VP                         might 
  #extend pattern='ch1-"NP" ch4-"VP"' annotation={'ch3':'CLAUSE'} iob = True
  #        pattern='(ch1="B-NP" ch1="B-NP"*) (ch4="B-VP" ch4="I-VP"*)'
  pattern = '(ch1="B-NP" ch1="I-NP"*) (ch4="B-VP" ch4="I-VP"*)'
  annotation = {'ch3':'CLAUSE'}
  result_CLAUSE = pyrata_re.annotate (pattern, annotation, result_VP, group, action, iob)
  #print ('Debug: ch3 CLAUSE=',result_CLAUSE)

  # loop 2
  pattern = 'pos~"VB.*" (ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$' # it is not an OR all inclusive it is the first presented which match ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|
  annotation = {'ch5':'VP'}
  result_VP = pyrata_re.annotate (pattern, annotation, result_PP, group, action, iob)
  #print ('Debug: ch5 (loop 2) VP=',result_VP)

  pattern = '(ch1="B-NP" ch1="I-NP"*) (ch5="B-VP" ch5="I-VP"*)'
  annotation = {'ch6':'CLAUSE'}
  result_CLAUSE = pyrata_re.annotate (pattern, annotation, result_VP, group, action, iob)
  #print ('Debug: ch6 (loop 2) CLAUSE=',result_CLAUSE)    

def pyrata_recognize_clause(sentence_dict_list):
  # http://www.nltk.org/book/ch07.html # Building Nested Structure with Cascaded Chunkers
#    sentence = [("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"),
#      ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
#   sentence = [("John", "NNP"), ("thinks", "VBZ"), ("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"), ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
#   data = [{'raw':w, 'pos':p} for (w, p) in sentence]
#   print ('Debug:', data)

  # NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN :      can   
  # extend pattern='pos~"DT|JJ|NN.*"+' annotation={'ch1':'NP'} iob = True 
  action = 'extend'
  group = [0]
  iob = True
  pattern = 'pos~"DT|JJ|NN.*"+'
  annotation = {'ch1':'NP'}
  result_NP = pyrata_re.annotate (pattern, annotation, sentence_dict_list, group, action, iob)
  #print ('Debug: ch1 NP=',result_NP)

  #PP: {<IN><NP>}               # Chunk prepositions followed by NP :  may   
  #extend pattern='pos="IN" ch1-"NP"' annotation={'ch2':'PP'} iob = True 
  #       pattern='pos="IN" (ch1="B-NP" ch1="I-NP"*)"
  pattern = 'pos="IN" (ch1="B-NP" ch1="I-NP"*)'
  annotation = {'ch2':'PP'}
  result_PP = pyrata_re.annotate (pattern, annotation, result_NP, group, action, iob)
  #rint ('Debug: ch2 PP=',result_PP)

  # VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments :    might 
  # extend pattern='pos~"VB.*" (ch1-"NP"|ch2-"PP"|ch3-"CLAUSE")+$' annotation={'ch4':'VP'} iob = True
   #       pattern='pos~"VB.*" (ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$'
  pattern = 'pos~"VB.*" (ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$' 
  annotation = {'ch4':'VP'}
  result_VP = pyrata_re.annotate (pattern, annotation, result_PP, group, action, iob)
  #print ('Debug: ch4 VP=',result_VP)


  # CLAUSE: {<NP><VP>}           # Chunk NP, VP                         might 
  #extend pattern='ch1-"NP" ch4-"VP"' annotation={'ch3':'CLAUSE'} iob = True
  #        pattern='(ch1="B-NP" ch1="B-NP"*) (ch4="B-VP" ch4="I-VP"*)'
  pattern = '(ch1="B-NP" ch1="I-NP"*) (ch4="B-VP" ch4="I-VP"*)'
  annotation = {'ch3':'CLAUSE'}
  result_CLAUSE = pyrata_re.annotate (pattern, annotation, result_VP, group, action, iob)
  #print ('Debug: ch3 CLAUSE=',result_CLAUSE)

  # loop 2
  pattern = 'pos~"VB.*" (ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$' # it is not an OR all inclusive it is the first presented which match ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|
  annotation = {'ch5':'VP'}
  result_VP = pyrata_re.annotate (pattern, annotation, result_PP, group, action, iob)
  #print ('Debug: ch5 (loop 2) VP=',result_VP)

  pattern = '(ch1="B-NP" ch1="I-NP"*) (ch5="B-VP" ch5="I-VP"*)'
  annotation = {'ch6':'CLAUSE'}
  result_CLAUSE = pyrata_re.annotate (pattern, annotation, result_VP, group, action, iob)
  #print ('Debug: ch6 (loop 2) CLAUSE=',result_CLAUSE)

  # Debug: [{'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'raw': 'the', 'pos': 'DT'}, {'raw': 'cat', 'pos': 'NN'}, {'raw': 'sit', 'pos': 'VB'}, {'raw': 'on', 'pos': 'IN'}, {'raw': 'the', 'pos': 'DT'}, {'raw': 'mat', 'pos': 'NN'}]
  # Debug: ch1 NP= [{'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN'}, {'raw': 'sit', 'pos': 'VB'}, {'raw': 'on', 'pos': 'IN'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'mat', 'pos': 'NN'}]
  # Debug: ch2 PP= [{'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN'}, {'raw': 'sit', 'pos': 'VB'}, {'raw': 'on', 'pos': 'IN', 'ch2': 'B-PP'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT', 'ch2': 'I-PP'}, {'ch1': 'I-NP', 'raw': 'mat', 'pos': 'NN', 'ch2': 'I-PP'}]
  # Debug: ch4 VP= [{'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN'}, {'ch4': 'B-VP', 'raw': 'sit', 'pos': 'VB'}, {'ch4': 'I-VP', 'raw': 'on', 'pos': 'IN', 'ch2': 'B-PP'}, {'ch4': 'I-VP', 'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT', 'ch2': 'I-PP'}, {'ch4': 'I-VP', 'ch1': 'I-NP', 'raw': 'mat', 'pos': 'NN', 'ch2': 'I-PP'}]
  # [{'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, 
  # {'raw': 'saw', 'pos': 'VBD'}, 
  # {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN'}, 
  # {'ch4': 'B-VP', 'raw': 'sit', 'pos': 'VB'}, 
  # {'ch4': 'I-VP', 'raw': 'on', 'pos': 'IN', 'ch2': 'B-PP'}, 
  # {'ch4': 'I-VP', 'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT', 'ch2': 'I-PP'}, 
  # {'ch4': 'I-VP', 'ch1': 'I-NP', 'raw': 'mat', 'pos': 'NN', 'ch2': 'I-PP'}]

  # Debug: ch3 CLAUSE= [{'pos': 'NN', 'raw': 'Mary', 'ch1': 'B-NP'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'raw': 'the', 'ch1': 'B-NP', 'ch3': 'B-CLAUSE'}, {'pos': 'NN', 'raw': 'cat', 'ch1': 'I-NP', 'ch3': 'I-CLAUSE'}, {'pos': 'VB', 'raw': 'sit', 'ch4': 'B-VP', 'ch3': 'I-CLAUSE'}, {'pos': 'IN', 'raw': 'on', 'ch2': 'B-PP', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP'}, {'ch2': 'I-PP', 'ch4': 'I-VP', 'ch3': 'I-CLAUSE', 'pos': 'DT', 'raw': 'the', 'ch1': 'B-NP'}, {'ch2': 'I-PP', 'ch4': 'I-VP', 'ch3': 'I-CLAUSE', 'pos': 'NN', 'raw': 'mat', 'ch1': 'I-NP'}]
  # (S
  #   (NP Mary/NN)
  #   saw/VBD
  #   (CLAUSE
  #     (NP the/DT cat/NN)
  #     (VP sit/VB (PP on/IN (NP the/DT mat/NN)))))

  # [{'pos': 'NN', 'raw': 'Mary', 'ch1': 'B-NP'}, 
  # {'pos': 'VBD', 'raw': 'saw'}, 
  # {'pos': 'DT', 'raw': 'the', 'ch1': 'B-NP', 'ch3': 'B-CLAUSE'}, 
  # {'pos': 'NN', 'raw': 'cat', 'ch1': 'I-NP', 'ch3': 'I-CLAUSE'}, 
  # {'pos': 'VB', 'raw': 'sit', 'ch4': 'B-VP', 'ch3': 'I-CLAUSE'}, 
  # {'pos': 'IN', 'raw': 'on', 'ch2': 'B-PP', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP'},
  # {'ch2': 'I-PP', 'ch4': 'I-VP', 'ch3': 'I-CLAUSE', 'pos': 'DT', 'raw': 'the', 'ch1': 'B-NP'}, 
  # {'ch2': 'I-PP', 'ch4': 'I-VP', 'ch3': 'I-CLAUSE', 'pos': 'NN', 'raw': 'mat', 'ch1': 'I-NP'}]

  #Debug: ch4 (loop 2) VP= [{'raw': 'Mary', 'ch1': 'B-NP', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch3': 'B-CLAUSE', 'raw': 'the', 'ch1': 'B-NP', 'pos': 'DT'}, {'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch1': 'I-NP', 'pos': 'NN'}, {'ch3': 'I-CLAUSE', 'raw': 'sit', 'ch4': 'B-VP', 'pos': 'VB'}, {'ch3': 'I-CLAUSE', 'raw': 'on', 'ch4': 'I-VP', 'ch2': 'B-PP', 'pos': 'IN'}, {'ch3': 'I-CLAUSE', 'raw': 'the', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'DT', 'ch1': 'B-NP'}, {'ch3': 'I-CLAUSE', 'raw': 'mat', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'NN', 'ch1': 'I-NP'}]
  #Debug: ch3 (loop 2) CLAUSE= [{'raw': 'Mary', 'ch1': 'B-NP', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch3': 'B-CLAUSE', 'raw': 'the', 'ch1': 'B-NP', 'pos': 'DT'}, {'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch1': 'I-NP', 'pos': 'NN'}, {'ch3': 'I-CLAUSE', 'raw': 'sit', 'ch4': 'B-VP', 'pos': 'VB'}, {'ch3': 'I-CLAUSE', 'raw': 'on', 'ch4': 'I-VP', 'ch2': 'B-PP', 'pos': 'IN'}, {'ch3': 'I-CLAUSE', 'raw': 'the', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'DT', 'ch1': 'B-NP'}, {'ch3': 'I-CLAUSE', 'raw': 'mat', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'NN', 'ch1': 'I-NP'}]

  # [{'raw': 'Mary', 'ch1': 'B-NP', 'pos': 'NN'}, 
  # {'raw': 'saw', 'pos': 'VBD'}, 
  # {'ch3': 'B-CLAUSE', 'raw': 'the', 'ch1': 'B-NP', 'pos': 'DT'}, 
  # {'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch1': 'I-NP', 'pos': 'NN'}, 
  # {'ch3': 'I-CLAUSE', 'raw': 'sit', 'ch4': 'B-VP', 'pos': 'VB'}, 
  # {'ch3': 'I-CLAUSE', 'raw': 'on', 'ch4': 'I-VP', 'ch2': 'B-PP', 'pos': 'IN'}, 
  # {'ch3': 'I-CLAUSE', 'raw': 'the', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'DT', 'ch1': 'B-NP'}, 
  # {'ch3': 'I-CLAUSE', 'raw': 'mat', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'NN', 'ch1': 'I-NP'}]

  # sentence 2
  #Debug: [{'pos': 'NNP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'raw': 'the'}, {'pos': 'NN', 'raw': 'cat'}, {'pos': 'VB', 'raw': 'sit'}, {'pos': 'IN', 'raw': 'on'}, {'pos': 'DT', 'raw': 'the'}, {'pos': 'NN', 'raw': 'mat'}]
  #Debug: ch1 NP= [{'pos': 'NNP', 'ch1': 'B-NP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'ch1': 'B-NP', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'cat'}, {'pos': 'VB', 'raw': 'sit'}, {'pos': 'IN', 'raw': 'on'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'mat'}]
  #Debug: ch2 PP= [{'pos': 'NNP', 'ch1': 'B-NP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'ch1': 'B-NP', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'cat'}, {'pos': 'VB', 'raw': 'sit'}, {'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on'}, {'pos': 'DT', 'ch1': 'B-NP', 'ch2': 'I-PP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'ch2': 'I-PP', 'raw': 'mat'}]
  #Debug: ch4 VP= [{'pos': 'NNP', 'ch1': 'B-NP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'ch1': 'B-NP', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'cat'}, {'pos': 'VB', 'raw': 'sit', 'ch4': 'B-VP'}, {'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on', 'ch4': 'I-VP'}, {'pos': 'DT', 'ch1': 'B-NP', 'ch2': 'I-PP', 'raw': 'the', 'ch4': 'I-VP'}, {'pos': 'NN', 'ch1': 'I-NP', 'ch2': 'I-PP', 'raw': 'mat', 'ch4': 'I-VP'}]
  #Debug: ch3 CLAUSE= [{'pos': 'NNP', 'ch1': 'B-NP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'ch1': 'B-NP', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the', 'ch3': 'B-CLAUSE'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'cat', 'ch3': 'I-CLAUSE'}, {'pos': 'VB', 'raw': 'sit', 'ch3': 'I-CLAUSE', 'ch4': 'B-VP'}, {'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP'}, {'ch1': 'B-NP', 'ch2': 'I-PP', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP', 'pos': 'DT', 'raw': 'the'}, {'ch1': 'I-NP', 'ch2': 'I-PP', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP', 'pos': 'NN', 'raw': 'mat'}]
  #Debug: ch5 (loop 2) VP= [{'ch1': 'B-NP', 'raw': 'John', 'pos': 'NNP'}, {'raw': 'thinks', 'pos': 'VBZ'}, {'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT', 'ch3': 'B-CLAUSE'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN', 'ch3': 'I-CLAUSE'}, {'ch4': 'B-VP', 'raw': 'sit', 'ch5': 'B-VP', 'pos': 'VB', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch1': 'B-NP', 'pos': 'DT', 'ch2': 'I-PP', 'raw': 'the', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch1': 'I-NP', 'pos': 'NN', 'ch2': 'I-PP', 'raw': 'mat', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}]
  #Debug: ch6 (loop 2) CLAUSE= [{'ch1': 'B-NP', 'raw': 'John', 'pos': 'NNP'}, {'raw': 'thinks', 'pos': 'VBZ'}, {'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'ch6': 'B-CLAUSE', 'pos': 'DT', 'ch3': 'B-CLAUSE'}, {'ch1': 'I-NP', 'raw': 'cat', 'ch6': 'I-CLAUSE', 'pos': 'NN', 'ch3': 'I-CLAUSE'}, {'ch4': 'B-VP', 'pos': 'VB', 'ch6': 'I-CLAUSE', 'raw': 'sit', 'ch5': 'B-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch6': 'I-CLAUSE', 'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch1': 'B-NP', 'ch6': 'I-CLAUSE', 'pos': 'DT', 'ch2': 'I-PP', 'raw': 'the', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch1': 'I-NP', 'ch6': 'I-CLAUSE', 'pos': 'NN', 'ch2': 'I-PP', 'raw': 'mat', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}]
  #Debug: ch5 (loop 2) VP= [{'ch1': 'B-NP', 'pos': 'NNP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'ch1': 'B-NP', 'pos': 'NN', 'raw': 'Mary'}, {'ch5': 'B-VP', 'pos': 'VBD', 'raw': 'saw'}, {'ch1': 'B-NP', 'ch3': 'B-CLAUSE', 'pos': 'DT', 'raw': 'the', 'ch5': 'I-VP'}, {'ch1': 'I-NP', 'ch3': 'I-CLAUSE', 'pos': 'NN', 'raw': 'cat', 'ch5': 'I-VP'}, {'ch3': 'I-CLAUSE', 'pos': 'VB', 'raw': 'sit', 'ch4': 'B-VP', 'ch5': 'I-VP'}, {'ch2': 'B-PP', 'pos': 'IN', 'raw': 'on', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch1': 'B-NP', 'ch2': 'I-PP', 'pos': 'DT', 'raw': 'the', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch1': 'I-NP', 'ch2': 'I-PP', 'pos': 'NN', 'raw': 'mat', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}]
  #Debug: ch6 (loop 2) CLAUSE= [{'ch1': 'B-NP', 'pos': 'NNP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'ch1': 'B-NP', 'pos': 'NN', 'raw': 'Mary', 'ch6': 'B-CLAUSE'}, {'ch5': 'B-VP', 'pos': 'VBD', 'raw': 'saw', 'ch6': 'I-CLAUSE'}, {'ch1': 'B-NP', 'ch5': 'I-VP', 'pos': 'DT', 'ch3': 'B-CLAUSE', 'raw': 'the', 'ch6': 'I-CLAUSE'}, {'ch1': 'I-NP', 'ch5': 'I-VP', 'pos': 'NN', 'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch6': 'I-CLAUSE'}, {'ch5': 'I-VP', 'pos': 'VB', 'ch3': 'I-CLAUSE', 'ch4': 'B-VP', 'raw': 'sit', 'ch6': 'I-CLAUSE'}, {'ch2': 'B-PP', 'pos': 'IN', 'raw': 'on', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}, {'ch1': 'B-NP', 'ch2': 'I-PP', 'pos': 'DT', 'raw': 'the', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}, {'ch1': 'I-NP', 'ch2': 'I-PP', 'pos': 'NN', 'raw': 'mat', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}]


  # (S
  #   (NP John/NNP)
  #   thinks/VBZ
  #   (CLAUSE
  #     (NP Mary/NN)
  #     (VP
  #       saw/VBD
  #       (CLAUSE
  #         (NP the/DT cat/NN)
  #         (VP sit/VB (PP on/IN (NP the/DT mat/NN)))))))

  # [{'ch1': 'B-NP', 'pos': 'NNP', 'raw': 'John'}, 
  # {'pos': 'VBZ', 'raw': 'thinks'}, 
  # {'ch1': 'B-NP', 'pos': 'NN', 'raw': 'Mary', 'ch6': 'B-CLAUSE'}, 
  # {'ch5': 'B-VP', 'pos': 'VBD', 'raw': 'saw', 'ch6': 'I-CLAUSE'}, 
  # {'ch1': 'B-NP', 'ch5': 'I-VP', 'pos': 'DT', 'ch3': 'B-CLAUSE', 'raw': 'the', 'ch6': 'I-CLAUSE'}, 
  # {'ch1': 'I-NP', 'ch5': 'I-VP', 'pos': 'NN', 'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch6': 'I-CLAUSE'}, 
  # {'ch5': 'I-VP', 'pos': 'VB', 'ch3': 'I-CLAUSE', 'ch4': 'B-VP', 'raw': 'sit', 'ch6': 'I-CLAUSE'}, 
  # {'ch2': 'B-PP', 'pos': 'IN', 'raw': 'on', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}, 
  # {'ch1': 'B-NP', 'ch2': 'I-PP', 'pos': 'DT', 'raw': 'the', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}, 
  # {'ch1': 'I-NP', 'ch2': 'I-PP', 'pos': 'NN', 'raw': 'mat', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}]





def pyrata_recognize_clause_in_the_whole_text():
  for s in sentences_dict_list_list:
    pyrata_recognize_clause(s)


def test_clause():

  """                            
  """

  print ('Measuring time performance on # {} sentences over # {} iterations for recognizing Clause'.format(size, iteration_number))

  from nltk.corpus import brown
  brown_sents = brown.sents()[:size]
  import nltk
  global brown_pos_tag_sents
  brown_pos_tag_sents = [nltk.pos_tag(sentence) for sentence in brown_sents] 
  #print (brown_pos_tag_sents[0])


  # ----------------------------------------------------
  # nltk_parser 
  # ----------------------------------------------------
  analyzer_name='nltk_parser'
  

  times, averagetime, mintime = measure_time(nltk_parse_clause_in_the_whole_text, iteration_number)
  grammar = "clause"
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, averagetime, mintime))


  # ----------------------------------------------------
  # pyrata 
  # ----------------------------------------------------
  analyzer_name='pyrata'

  global sentences_dict_list_list
  sentences_dict_list_list = []

  for s in brown_pos_tag_sents:
    sentences_dict_list_list.append([{'raw':w, 'pos':p} for (w, p) in s])
  # data -> sentences_dict_list_list
  #data = data[0]
  # flatten a list of list i.e. sentences of words becomes a text of words 
  # data = [val for sublist in data for val in sublist]
  #print (data[:10])
  #print ('len(data):', len(data))

  times, averagetime, mintime = measure_time(pyrata_recognize_clause_in_the_whole_text, iteration_number)
  grammar = "clause"
  print ('{}\t{}\t{}\t{}'.format(analyzer_name, grammar, averagetime, mintime))



def backslash(string):
  for ch in [' ','?', '+', '*', '.', '[', ']', '~' , '{', '}', '|', '"', "'", ',', ':', '<', '>']:
    if ch in string:
      #string=string.replace(ch,"\\"+ch)
      string=string.replace(ch,'_')
  return string    


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run benchmark
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

#
  logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='benchmark.log', level=logging.INFO)
  logger = logging.getLogger()
  logger.disabled = True

  # SET
  iteration_number = 1 #0
  
  # 
  #sizes = [10000*i for i in range (2, iteration_number)]
  analysers =  ['clips.pattern', 'nltk_regex_parser', 'nltk_regex_chunk_parser', 'spaCy', 'pyrata']
  analysers =  ['clips.pattern', 'nltk_regex_chunk_parser', 'pyrata']

  # 1161192 # # brown corpus 1 161 192 words ; can also be interpreted as number of sentences
  sizes = [10000, 50000, 100000, 200000, 300000, 500000, 750000, 1000000]

  for size in sizes:
    print(size) 
    time_noun_phrase_recognizers(size, analysers)
    #output_noun_phrase_recognizers(size)


# SET
  #size = 1 # 1161192 # # brown corpus 1 161 192 words ; can also be interpreted as number of sentences
  #iteration_number = 1
  #test_clause()

