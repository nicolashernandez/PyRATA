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
Quick and simple phrase extraction with part-of-speech patterns


Justeson, J., & Katz, S. (1995). Technical terminology: Some linguistic properties and an algorithm for identification in text. Natural Language Engineering, 1(1), 9-27.
@article{justeson_katz_1995, title={Technical terminology: some linguistic properties and an algorithm for identification in text}, volume={1}, DOI={10.1017/S1351324900000048}, number={1}, journal={Natural Language Engineering}, publisher={Cambridge University Press}, author={Justeson, John S. and Katz, Slava M.}, year={1995}, pages={9–27}}
https://brenocon.com/JustesonKatz1995.pdf

The proposed algorithm requires satisfaction of two constraints applied to word strings in text. Strings satisfying the constraints are the intended output of the
algorithm. Various parameters that can be used to influence the behavior of the algorithm are introduced in section 3.2.

- Frequency: Candidate strings must have frequency 2 or more in the text. 
- Grammatical structure: Candidate strings are those multi-word noun phrases that are specified by the regular expression 
((A | N)+ | ((A | N)*(N P)?)(A | N)*)N,
where 
A is an ADJECTIVE, but not a determiner.[5]
N is a LEXICAL NOUN (i.e. not a pronoun).
P is a PREPOSITION.

In words, a candidate term is a multi-word noun phrase; and it either is a
string of nouns and/or adjectives, ending in a noun, or it consists of two
such strings, separated by a single preposition. Concerning the exclusion of
determiners from adjectives admitted in candidate strings, see note above.


There are (l + 2).2^(l-3) admissible term patterns of length l. Candidate terms of
length 2 (with two admissible patterns) and length 3 (with five admissible patterns)
are by far the most commonly encountered, and all of the permitted grammatical
sequences are attested in strings of this length. The following examples of each
permitted pattern are taken from articles analyzed in section 4, drawn from three
different domains:
AN: linear function; lexical ambiguity; mobile phase
NN: regression coefficients; word sense; surface area
AAN: Gaussian random variable; lexical conceptual paradigm; aqueous mobile
phase
ANN: cumulative distribution function; lexical ambiguity resolution; accessible
surface area
NAN: mean squared error; domain independent set; silica based packing
NNN: class probability function; text analysis system; gradient elution chromatography
NPN: degrees of freedom; [no example]; energy of adsorption

[5] Determiners include articles, demonstratives, possessive pronouns, and quantifiers. Some common
determiners (after Huddleston 1984:233), occupying three fixed positions relative to one another, are
as follows. Pre-determiners: all, both; half, one-third, three-quarters,...; double, twice, three times; such,
what(exclamative). Determiners proper: the; this, these, that, those; my, our, your; we, us, you; which,
what(relative), what(interrogative); a, another, some, any, no, either, neither; each, enough, much,
more, less; a few(positive), a little(positive). Post-determiners: every; many, several, few(negative),
little(negative); one, two, three...; (a) dozen.


Handler, A., Denny, M. J., Wallach, H., & O’Connor, B. (2016). “Bag of What? Simple Noun Phrase Extraction for Text Analysis”. In Proceedings of the Workshop on Natural Language Processing and Computational Social Science at the 2016 Conference on Empirical Methods in Natural Language Processing

@inproceedings{Handler2016BagOW,
  title={Bag of What? Simple Noun Phrase Extraction for Text Analysis},
  author={Abram Handler and Matthew J. Denny and Hanna Wallach and Brendan O’Connor},
  year={2016},  
  booktitle = {Workshop on Natural Language Processing and Computational Social Science at the 2016 Conference on Empirical Methods in Natural Language Processing}
}
http://slanglab.cs.umass.edu/phrasemachine/
https://brenocon.com/handler2016phrases.pdf
http://brenocon.com/oconnor_textasdata2016.pdf
https://github.com/slanglab/phrasemachine
The simplest grammar that we consider is
(A | N ) ∗ N (P D ∗ (A | N ) ∗ N )∗
defined over a coarse tag set of adjectives, nouns
(both common and proper), prepositions, and deter-
miners. We refer to this grammar as SimpleNP. The
constituents that match this grammar are bare NPs
(with optional PP attachments), N-bars, and names.
We do not include any determiners at the root NP.

FullNP extends SimpleNP by adding coordination
of pairs of words with the same tag (e.g., (VB
CC VB) in (cease and desist) order); coordination
of noun phrases; parenthetical post-modifiers (e.g.,
401(k), which is a 4-gram because of common NLP
tokenization conventions); numeric modifiers and
nominals; and support for 
* the Penn Treebank tag set,
https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

* the coarse universal tag set (Petrov et al., 2011), 

* and Gimpel et al. (2011)’s Twitter-specific coarse tag set.
We provide the complete definition in the appendix.


The following foma grammar defines the rewrite phrase transducer P :
# POS tag categories. "Coarse" refer to the Petrov Univeral tag set.
# We directly use PTB tags, but for Twitter, we assume they’ve been
# preprocessed to coarse tags.
# CD is intentionally under both Adj and Noun.
define Adj1 [JJ | JJR | JJS | CD | CoarseADJ];
define Det1 [DT | CoarseDET];
define Prep1 [IN | TO | CoarseADP];
define Adv1 [RB | RBR | RBS | CoarseADV];
# Note that Twitter and coarse tags subsume some of this under VERB.
define VerbMod1 [Adv1 | RP | MD | CoarsePRT];
# PTB FW goes to CoarseX, but we’re excluding CoarseX since for Gimpel et al.’s
# Twitter tags, that’s usually non-constituent-participating things like URLs.
define Noun [NN | NNS | NNP | NNPS | FW | CD | CoarseNOUN | CoarseNUM];
define Verb [VB | VBD | VBG | VBN | VBP | VBZ | CoarseVERB];
define AnyPOS [O | Adj1|Det1|Prep1|Adv1|VerbMod1|Noun|Verb | CoarseDOT|CoarseADJ|CoarseADP|CoarseADV|CoarseCONJ|CoarseDET| CoarseNOUN|CoarseNUM|CoarsePRON|CoarsePRT|CoarseVERB|CoarseX ]
define Lparen ["-LRB-" | "-LSB-" | "-LCB-"]; # Twitter doesnt have this.
define Rparen ["-RRB-" | "-RSB-" | "-RCB-"];
# Ideally, auxiliary verbs would be VerbMod, but PTB gives them VB* tags.
# single-word coordinations
define Adj Adj1 [CC Adj1]*;
define Det Det1 [CC Det1]*;
define Adv Adv1 [CC Adv1]*;
define Prep Prep1 [CC Prep1]*;
define VerbMod VerbMod1 [CC VerbMod1]*;
# NP (and thus BaseNP) have to be able to stand on their own. They are not
# allowed to start with a determiner, since it’s usually extraneous for our
# purposes. But when we want an NP right of something, we need to allow
# optional determiners since they’re in between.
define BaseNP [Adj|Noun]* Noun;
define PP Prep+ [Det|Adj]* BaseNP;
define ParenP Lparen AnyPOSˆ{1,50} Rparen;
define NP1 BaseNP [PP | ParenP]*;
define NP NP1 [CC [Det|Adj]* NP1]*;
regex NP -> START ... END;
write att compiled_fsts/NP.attfoma
"""

import logging
from timeit import Timer
from pprint import pprint, pformat

import nltk
from nltk.corpus import brown



import pyrata.re as pyrata_re




# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def JK_simpleNP_Penn(data):
  """
  Justeson and Katz (1995): Patterns restricted to Content bigrams and trigrams
  i.e. Extended NP JK retricted to length 2 and 3  

AN: linear function; lexical ambiguity; mobile phase
NN: regression coefficients; word sense; surface area
AAN: Gaussian random variable; lexical conceptual paradigm; aqueous mobile
phase
ANN: cumulative distribution function; lexical ambiguity resolution; accessible
surface area
NAN: mean squared error; domain independent set; silica based packing
NNN: class probability function; text analysis system; gradient elution chromatography
NPN: degrees of freedom; [no example]; energy of adsorption
where 

A is an ADJECTIVE, but not a determiner.[5]
N is a LEXICAL NOUN (i.e. not a pronoun).
P is a PREPOSITION.

 # Penn Treebank tag set
  7.  JJ  Adjective
8.  JJR Adjective, comparative
9.  JJS Adjective, superlative
12. NN  Noun, singular or mass
13. NNS Noun, plural
14. NNP Proper noun, singular
15. NNPS  Proper noun, plural
6.  IN  Preposition or subordinating conjunction


    """
  patterns = set(['pos="JJ" pos="NN"', 
    'pos="NN" pos="NN"', 
    'pos="JJ" pos="JJ" pos="NN"', 
    'pos="JJ" pos="NN" pos="NN"', 
    'pos="NN" pos="JJ" pos="NN"', 
    'pos="NN" pos="NN" pos="NN"', 
    'pos="NN" pos="IN" pos="NN"'])

  noun_phrases = []
  for p in patterns:
    noun_phrases.extend(pyrata_re.findall(p, data))
  return noun_phrases  


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def JK_extendedNP_Penn(data):
  """ 
( (A|N)+ |  ((A | N)*(N P)?) (A | N)* ) N
where 
A is an ADJECTIVE, but not a determiner.
N is a LEXICAL NOUN (i.e. not a pronoun).
P is a PREPOSITION.
Of lengh 2 or more

# do not generate the right NFA...
python3 pyrata_re.py '((pos="JJ"|pos="NN")+ | ((pos="JJ"|pos="NN")* (pos="NN" pos="IN")? (pos="JJ"|pos="NN")*) pos="NN" ' "[{'name':'value'}]" --draw

# generate the right one ; I ve just switch the two alternative parts
python3 pyrata_re.py '(  ((pos="JJ"|pos="NN")* (pos="NN" pos="IN")? (pos="JJ"|pos="NN")* | (pos="JJ"|pos="NN")+) pos="NN" ' "[{'name':'value'}]" --draw
"""
  pattern = '((pos="JJ"|pos="NN")+ | (((pos="JJ"|pos="NN")* (pos="NN" pos="IN")? (pos="JJ"|pos="NN")*)) pos="NN"'
  return pyrata_re.findall(pattern, data)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def Handel_simpleNP_Penn(data):
  """ 
(A | N )∗ N (P D∗ (A | N )∗ N)∗
where 
A is an ADJECTIVE, but not a determiner.
N is a LEXICAL NOUN (i.e. not a pronoun).
P is a PREPOSITION.
Of lengh 2 or more

# do not generate the right NFA...
python3 pyrata_re.py '((pos="JJ"|pos="NN")+ | ((pos="JJ"|pos="NN")* (pos="NN" pos="IN")? (pos="JJ"|pos="NN")*) pos="NN" ' "[{'name':'value'}]" --draw

# generate the right one ; I ve just switch the two alternative parts
python3 pyrata_re.py '(  ((pos="JJ"|pos="NN")* (pos="NN" pos="IN")? (pos="JJ"|pos="NN")* | (pos="JJ"|pos="NN")+) pos="NN" ' "[{'name':'value'}]" --draw
"""
  pattern = '(pos="JJ"|pos="NN")* pos="NN" (pos="IN" pos="DT"* (pos="JJ"|pos="NN")* pos="NN")*'
  return pyrata_re.findall(pattern, data)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def Handel_FullNP_multi_tag_set(data):
  """ 
# POS tag categories. "Coarse" refer to the Petrov Univeral tag set.
# We directly use PTB tags, but for Twitter, we assume they’ve been
# preprocessed to coarse tags.
# CD is intentionally under both Adj and Noun.
define Adj1 [JJ | JJR | JJS | CD | CoarseADJ];
define Det1 [DT | CoarseDET];
define Prep1 [IN | TO | CoarseADP];
define Adv1 [RB | RBR | RBS | CoarseADV];
# Note that Twitter and coarse tags subsume some of this under VERB.
define VerbMod1 [Adv1 | RP | MD | CoarsePRT];
# PTB FW goes to CoarseX, but we’re excluding CoarseX since for Gimpel et al.’s
# Twitter tags, that’s usually non-constituent-participating things like URLs.
define Noun [NN | NNS | NNP | NNPS | FW | CD | CoarseNOUN | CoarseNUM];
define Verb [VB | VBD | VBG | VBN | VBP | VBZ | CoarseVERB];
define AnyPOS [O | Adj1|Det1|Prep1|Adv1|VerbMod1|Noun|Verb | CoarseDOT|CoarseADJ|CoarseADP|CoarseADV|CoarseCONJ|CoarseDET| CoarseNOUN|CoarseNUM|CoarsePRON|CoarsePRT|CoarseVERB|CoarseX ]
define Lparen ["-LRB-" | "-LSB-" | "-LCB-"]; # Twitter doesnt have this.
define Rparen ["-RRB-" | "-RSB-" | "-RCB-"];
# Ideally, auxiliary verbs would be VerbMod, but PTB gives them VB* tags.
# single-word coordinations
define Adj Adj1 [CC Adj1]*;
define Det Det1 [CC Det1]*;
define Adv Adv1 [CC Adv1]*;
define Prep Prep1 [CC Prep1]*;
define VerbMod VerbMod1 [CC VerbMod1]*;
# NP (and thus BaseNP) have to be able to stand on their own. They are not
# allowed to start with a determiner, since it’s usually extraneous for our
# purposes. But when we want an NP right of something, we need to allow
# optional determiners since they’re in between.
define BaseNP [Adj|Noun]* Noun;
define PP Prep+ [Det|Adj]* BaseNP;
define ParenP Lparen AnyPOSˆ{1,50} Rparen;
define NP1 BaseNP [PP | ParenP]*;
define NP NP1 [CC [Det|Adj]* NP1]*;
regex NP -> START ... END;"""

  data = pyrata_re.update('pos~"JJ|JJR|JJS|CD|CoarseADJ"', {'pos':"Adj1"}, data)
  data = pyrata_re.update('pos~"DT|CoarseDET"', {'pos':"Det1"}, data)
  data = pyrata_re.update('pos~"IN|TO|CoarseADP"', {'pos':"Prep1"}, data)
  data = pyrata_re.update('pos~"RB|RBR|RBS|CoarseADV"', {'pos':"Adv1"}, data)
  data = pyrata_re.update('pos~"Adv1|RP|MD|CoarsePRT"', {'pos':"VerbMod1"}, data)
  data = pyrata_re.update('pos~"NN|NNS|NNP|NNPS|FW|CD|CoarseNOUN|CoarseNUM"', {'pos':"Noun"}, data)
  data = pyrata_re.update('pos~"VB|VBD|VBG|VBN|VBP|VBZ|CoarseVERB"', {'pos':"Verb"}, data)
  #data = pyrata_re.update('pos~"O|Adj1|Det1|Prep1|Adv1|VerbMod1|Noun|Verb|CoarseDOT|CoarseADJ|CoarseADP|CoarseADV|CoarseCONJ|CoarseDET|CoarseNOUN|CoarseNUM|CoarsePRON|CoarsePRT|CoarseVERB|CoarseX"', {'pos':"AnyPOS"}, data)
  data = pyrata_re.update('pos~"-LRB-|-LSB-|-LCB-"', {'pos':"Lparen"}, data)
  data = pyrata_re.update('pos~"-RRB-|-RSB-|-RCB-"', {'pos':"Rparen"}, data)

# for each transducer level inc the chk argument
  data = pyrata_re.extend('pos="Adj1" (pos="CC" pos="Adj1")*', {'chk1':"Adj"}, data, iob = True)
  data = pyrata_re.extend('pos="Det1" (pos="CC" pos="Det1")*', {'chk1':"Det"}, data, iob = True)
  data = pyrata_re.extend('pos="Adv1" (pos="CC" pos="Adv1")*', {'chk1':"Adv"}, data, iob = True)
  data = pyrata_re.extend('pos="Prep1" (pos="CC" pos="Prep1")*', {'chk1':"Prep"}, data, iob = True)
  data = pyrata_re.extend('pos="VerbMod1" (pos="CC" pos="VerbMod1")*', {'chk1':"VerbMod"}, data, iob = True)


  data = pyrata_re.extend('(chk1-"Adj" | pos="Noun")*', {'chk2':"BaseNP"}, data, iob = True)

  data = pyrata_re.extend('chk1-"Prep" (chk1-"Det" | chk1-"Adj")* chk2-"BaseNP"', {'chk3':"PP"}, data, iob = True)

  data = pyrata_re.extend('pos="Lparen" .+ pos="Rparen"', {'chk4':"ParenP"}, data, iob = True)

  data = pyrata_re.extend('chk2-"BaseNP" (chk3-"PP" | chk4-"ParenP")*', {'chk5':"NP1"}, data, iob = True)

  data = pyrata_re.extend('chk5-"NP1" (pos="CC" (chk1-"Det" | chk1-"Adj")* chk5-"NP1")*', {'chk6':"NP"}, data, iob = True)

  return pyrata_re.findall('chk6-"NP"' , data)





# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def brown_data():
  """return the text_length first tokens of the brown corpus tagged in pyrata format"""
  tokens = brown.words()
  tokens = tokens[:text_length]

  pos_tags = nltk.pos_tag(tokens)

  return [{'raw':w, 'pos':p} for (w, p) in pos_tags]


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_JK_simpleNP_Penn_brown():
  # should occur twice 
  np_counter = set()
  for np in JK_simpleNP_Penn(brown_data()):
    #print ('{}'.format(np))
    # stringify in raw_pos list 
    np = ' '.join([''.join([e['raw'], '_', e['pos']]) for e in np])
    if np in np_counter:
      print ('{}'.format(np))
    np_counter.add(np)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_JK_extendedNP_Penn_brown():
  # should occur twice 
  np_counter = set()
  for np in JK_extendedNP_Penn(brown_data()):
    #print ('{}'.format(np))
    if len(np) >=2:
      # stringify in raw_pos list 
      np = ' '.join([''.join([e['raw'], '_', e['pos']]) for e in np])
      if np in np_counter:
        print ('{}'.format(np))
      np_counter.add(np)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_Handel_simpleNP_Penn_brown():
  # should occur twice 
  np_counter = set()
  for np in Handel_simpleNP_Penn(brown_data()):
    #print ('{}'.format(np))
    if len(np) >=2:
      # stringify in raw_pos list 
      np = ' '.join([''.join([e['raw'], '_', e['pos']]) for e in np])
      if np in np_counter:
        print ('{}'.format(np))
      np_counter.add(np)



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_Handel_FullNP_multi_tag_set_brown():
  #print (pformat(Handel_FullNP_multi_tag_set(brown_data())))
  # should occur twice 
  np_counter = set()
  for np in Handel_FullNP_multi_tag_set(brown_data()):
    #print ('{}'.format(np))
    if len(np) >=2:
      # stringify in raw_pos list 
      np = ' '.join([''.join([e['raw'], '_', e['pos']]) for e in np])
      if np in np_counter:
        print ('{}'.format(np))
      np_counter.add(np)

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_Handel_FullNP_multi_tag_set_brown_wo_filter():
  for np in Handel_FullNP_multi_tag_set(brown_data()):
    if len(np) >=2:    
      np = ' '.join([''.join([e['raw'], '_', e['pos']]) for e in np])
      print ('{}'.format(np))
    


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run benchmark
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  global text_length
  text_length = 10000


  #test_JK_simpleNP_Penn_brown()
  #test_JK_extendedNP_Penn_brown()
  test_Handel_simpleNP_Penn_brown()
  #test_Handel_FullNP_multi_tag_set_brown()
  #test_Handel_FullNP_multi_tag_set_brown_wo_filter()