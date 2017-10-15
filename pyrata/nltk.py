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
Turn common nltk process to pyrata data structure to perform re precessing
"""

rawFeatureName = 'raw'
posFeatureName = 'pos'
chunkFeatureName = 'chunk'

def list2pyrata (**kwargs):
  """ 
  turn a list into a list of dict 
  e.g. a list of words into a list of dict 
  with a feature to represent the surface form of the word 
  if parameter name is given then the dict feature name will be the one set ; 
  if parameter dictList is given then the list of dict will be extented with the value of the list (named or not) 
  """
 
  alist = []
  if 'list' in kwargs.keys(): # MANDATORY
    alist = kwargs['list']
  #kwargs.pop('list', None)
  name = 'f0'
  if 'name' in kwargs.keys(): 
    name = kwargs['name']

  dictList = []
  if 'dictList' in kwargs.keys():
    dictList = kwargs['dictList']

  if len(dictList) != 0:
    ''' extend a given dictList'''
    if len(dictList) == len(alist):
      for i in range(len(dictList)):
        dictList[i][name] = alist[i]
    else:
      raise Exception('list2pyrata - len of a given dictList should be equal to the len of a list')
  else:  
    for element in alist:
      currentDict = {}
      currentDict[name] = element
      dictList.append(currentDict)
  return dictList

def listList2pyrata (**kwargs):
  """ 
  turn a list of list 'listList' into a list of dict
  with values being the elements of the second list ; 
  the value names are arbitrary choosen. 
  if parameter names is given then the dict feature names will be the ones set (the order matters) ; 
  if parameter dictList is given then the list of dict will be extented with the values of the list (named or not) 
  """

  alistList = []
  if 'listList' in kwargs.keys(): # MANDATORY
    alistList = kwargs['listList']
  
  if len(alistList)==0:
        raise Exception('listList2pyrata - len of listList cannot be empty')

  names = ['f'+str(i) for i in range (len(alistList[0]))] 
  # TODO len of contained list should be also checked (should not be empty and always have the same size)
  if 'names' in kwargs.keys(): # MANDATORY
    names = kwargs['names']
  if len(names)==0:
    raise Exception('listList2pyrata - len of names cannot be empty')

  dictList = []
  if 'dictList' in kwargs.keys(): # MANDATORY
    dictList = kwargs['dictList']

  #print ('Debug: dictList=',dictList,'\n')
  if len(dictList) != 0:
    ''' extend a given dictList'''
    if len(dictList) == len(alistList):
      for j in range(len(alistList)):
        adict = dictList[j]
        alist = alistList[j]
        for i in range(0,len(alist)):
          adict[names[i]]=alist[i]
        dictList[j] = adict
    else:
      raise Exception('listList2pyrata - len of a given dictList should be equal to the len of a listList')
  else:
    ''' create a dictList from scratch '''
    for alist in alistList:  
      adict = {}
      for i in range(0,len(alist)):
        adict[names[i]]=alist[i]
      dictList.append(adict)
  
  return dictList 

def pyrata2conll (dictList, **kwargs):
  """ 
  See 3.1   Reading IOB Format and the CoNLL 2000 Corpus http://www.nltk.org/book/ch07.html
  
  can be used wi
  nltk.chunk.conllstr2tree(text, chunk_types=['NP']).draw()
  """

  if 'raw' in kwargs.keys(): 
    rawFeatureName = kwargs['raw']
  if 'pos' in kwargs.keys(): 
    posFeatureName = kwargs['pos']   
  if 'chunk' in kwargs.keys(): 
    chunkFeatureName = kwargs['chunk']

  text = ''
  for e in dictList:
    text.append(' '.join([e[rawFeatureName], e[posFeatureName], e[chunkFeatureName], '\n']))

  return text


# extend a given dictList 

# merge dictList

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  import nltk
  lemmatizer = nltk.WordNetLemmatizer()
  stemmer = nltk.stem.SnowballStemmer('english')
  stopwords = nltk.corpus.stopwords.words('english')

  sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
  tokens = nltk.word_tokenize(sentence)

  
  print ('sentence:', sentence,'\n')
  print ('nltk tokens:',tokens,'\n')
  print ('pyrata wo name:',list2pyrata(list=tokens),'\n')
  print ('pyrata wi name:',list2pyrata(list=tokens, name='raw'),'\n')

  lowercases = [w.lower() for w in tokens]
  lowercasesdictlist = [{'lc' : w.lower()} for w in tokens]  
  print ('pyrata wi name and dictList wi name:',list2pyrata(list=tokens, name='raw', dictList=lowercasesdictlist),'\n')
  
  pos = nltk.pos_tag(tokens)
  print ('nltk pos:',pos,'\n')
  print ('pyrata wo names:',listList2pyrata(listList=pos),'\n')
  print ('pyrata wi names:',listList2pyrata(listList=pos, names=['raw', 'pos']),'\n')
  
  dictList = list2pyrata(list=tokens)
  print ('pyrata wo names but dictList wo name:',listList2pyrata(listList=pos,dictList=dictList),'\n')
  
  dictList = list2pyrata(list=tokens)
  print ('pyrata wi names and dictList wo name:',listList2pyrata(listList=pos, names=['raw', 'pos'],dictList=dictList),'\n')

  dictList = list2pyrata(list=tokens, name ='raw')
  print ('pyrata wo names but dictList wi name:',listList2pyrata(listList=pos,dictList=dictList),'\n')
  
  dictList = list2pyrata(list=tokens, name ='raw')
  print ('pyrata wi names and dictList wi name:',listList2pyrata(listList=pos, names=['raw', 'pos'],dictList=dictList),'\n')

  pyrata = [{'raw':word, 'pos':pos, 'stem':stemmer.stem(word), 'lem':lemmatizer.lemmatize(word.lower()), 'sw':(word in stopwords)} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
  print ('pyrata in one single line:',pyrata,'\n')
  
    # working with chunks 
    # http://nlpforhackers.io/named-entity-extraction/
  from nltk import word_tokenize, pos_tag, ne_chunk
  
  sentence = "Mark is working at Facebook Corp." 
  from nltk.chunk import conlltags2tree, tree2conlltags
  ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))   
  iob_tagged = tree2conlltags(ne_tree)
  print (iob_tagged)
  """
  [('Mark', 'NNP', 'B-PERSON'), ('is', 'VBZ', 'O'), ('working', 'VBG', 'O'), ('at', 'IN', 'O'), ('Facebook', 'NNP', 'B-ORGANIZATION'), ('Corp', 'NNP', 'I-ORGANIZATION'), ('.', '.', 'O')]
  """   
  ne_tree = conlltags2tree(iob_tagged)
  print (ne_tree)
  """
  (S
  (PERSON Mark/NNP)
  is/VBZ
  working/VBG
  at/IN
  (ORGANIZATION Facebook/NNP Corp/NNP)
  ./.)
  """
  print ('pyrata wi names no dictList from iob_tagged ne chunks:',listList2pyrata(listList=iob_tagged,names=['raw', 'pos', 'chunk']),'\n')
  """
  [{'raw': 'Mark', 'pos': 'NNP', 'chunk': 'B-PERSON'}, {'raw': 'is', 'pos': 'VBZ', 'chunk': 'O'}, {'raw': 'working', 'pos': 'VBG', 'chunk': 'O'}, {'raw': 'at', 'pos': 'IN', 'chunk': 'O'}, {'raw': 'Facebook', 'pos': 'NNP', 'chunk': 'B-ORGANIZATION'}, {'raw': 'Corp', 'pos': 'NNP', 'chunk': 'I-ORGANIZATION'}, {'raw': '.', 'pos': '.', 'chunk': 'O'}] 
  """
  pyrata = [{'raw':raw, 'chunk':chunk} for raw, pos, chunk in iob_tagged]
  print ('pyrata in one single line (from iob_tagged ne chunks):',pyrata,'\n')


  # TODO http://stackoverflow.com/questions/30664677/extract-list-of-persons-and-organizations-using-stanford-ner-tagger-in-nltk
  # https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software

  # http://www.ling.helsinki.fi/kit/2009s/clt231/NLTK/book/ch07-ExtractingInformationFromText.html
  # https://github.com/nltk/nltk.github.com/blob/master/book/pylisting/code_classifier_chunker.py