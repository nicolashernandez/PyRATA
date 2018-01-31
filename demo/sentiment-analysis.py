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
The current work is based on vaderSentiment released under MIT license
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
https://github.com/cjhutto/vaderSentiment/blob/master/vaderSentiment/vaderSentiment.py

 - Analyze typical example cases, including handling of:
  -- negations
  -- punctuation emphasis & punctuation flooding
  -- word-shape as emphasis (capitalization difference)
  -- degree modifiers (intensifiers such as 'very' and dampeners such as 'kind of')
  -- slang words as modifiers such as 'uber' or 'friggin' or 'kinda'
  -- contrastive conjunction 'but' indicating a shift in sentiment; sentiment of later text is dominant
  -- use of contractions as negations
  -- sentiment laden emoticons such as :) and :D
  -- sentiment laden slang words (e.g., 'sux')
  -- sentiment laden initialisms and acronyms (for example: 'lol') 

VADER is smart, handsome, and funny.----------------------------- {'neg': 0.0, 'neu': 0.254, 'pos': 0.746, 'compound': 0.8316}
VADER is not smart, handsome, nor funny.------------------------- {'neg': 0.646, 'neu': 0.354, 'pos': 0.0, 'compound': -0.7424}
VADER is smart, handsome, and funny!----------------------------- {'neg': 0.0, 'neu': 0.248, 'pos': 0.752, 'compound': 0.8439}
VADER is very smart, handsome, and funny.------------------------ {'neg': 0.0, 'neu': 0.299, 'pos': 0.701, 'compound': 0.8545}
VADER is VERY SMART, handsome, and FUNNY.------------------------ {'neg': 0.0, 'neu': 0.246, 'pos': 0.754, 'compound': 0.9227}
VADER is VERY SMART, handsome, and FUNNY!!!---------------------- {'neg': 0.0, 'neu': 0.233, 'pos': 0.767, 'compound': 0.9342}
VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!--------- {'neg': 0.0, 'neu': 0.294, 'pos': 0.706, 'compound': 0.9469}
The book was good.----------------------------------------------- {'neg': 0.0, 'neu': 0.508, 'pos': 0.492, 'compound': 0.4404}
The book was kind of good.--------------------------------------- {'neg': 0.0, 'neu': 0.657, 'pos': 0.343, 'compound': 0.3832}
The plot was good, but the characters are uncompelling and the dialog is not great. {'neg': 0.327, 'neu': 0.579, 'pos': 0.094, 'compound': -0.7042}
At least it isn't a horrible book.------------------------------- {'neg': 0.0, 'neu': 0.637, 'pos': 0.363, 'compound': 0.431}
Make sure you :) or :D today!------------------------------------ {'neg': 0.0, 'neu': 0.294, 'pos': 0.706, 'compound': 0.8633}
Today SUX!------------------------------------------------------- {'neg': 0.779, 'neu': 0.221, 'pos': 0.0, 'compound': -0.5461}
Today only kinda sux! But I'll get by, lol----------------------- {'neg': 0.179, 'neu': 0.569, 'pos': 0.251, 'compound': 0.2228}
----------------------------------------------------
 - About the scoring: 
  -- The 'compound' score is computed by summing the valence scores of each word in the lexicon, adjusted 
     according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). 
     This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence.  
     Calling it a 'normalized, weighted composite score' is accurate.
  -- The 'pos', 'neu', and 'neg' scores are ratios for proportions of text that fall in each category (so these   
     should all add up to be 1... or close to it with float operation).  These are the most useful metrics if 
     you want multidimensional measures of sentiment for a given sentence.

----------------------------------------------------
 - Analyze examples of tricky sentences that cause trouble to other sentiment analysis tools.
  -- special case idioms - e.g., 'never good' vs 'never this good', or 'bad' vs 'bad ass'.
  -- special uses of 'least' as negation versus comparison 

Sentiment analysis has never been good.------------------------------ {'neg': 0.325, 'neu': 0.675, 'pos': 0.0, 'compound': -0.3412}
Sentiment analysis has never been this good!------------------------- {'neg': 0.0, 'neu': 0.621, 'pos': 0.379, 'compound': 0.5672}
Most automated sentiment analysis tools are shit.-------------------- {'neg': 0.375, 'neu': 0.625, 'pos': 0.0, 'compound': -0.5574}
With VADER, sentiment analysis is the shit!-------------------------- {'neg': 0.0, 'neu': 0.583, 'pos': 0.417, 'compound': 0.6476}
Other sentiment analysis tools can be quite bad.--------------------- {'neg': 0.351, 'neu': 0.649, 'pos': 0.0, 'compound': -0.5849}
On the other hand, VADER is quite bad ass!--------------------------- {'neg': 0.0, 'neu': 0.414, 'pos': 0.586, 'compound': 0.8172}
Roger Dodger is one of the most compelling variations on this theme.- {'neg': 0.0, 'neu': 0.834, 'pos': 0.166, 'compound': 0.2944}
Roger Dodger is one of the least compelling variations on this theme. {'neg': 0.132, 'neu': 0.868, 'pos': 0.0, 'compound': -0.1695}
Roger Dodger is at least compelling as a variation on the theme.----- {'neg': 0.0, 'neu': 0.84, 'pos': 0.16, 'compound': 0.2263}
----------------------------------------------------

 - VADER works best when analysis is done at the sentence level (but it can work on single words or entire novels).
  -- For example, given the following paragraph text from a hypothetical movie review:
  'It was one of the worst movies I've seen, despite good reviews. Unbelievably bad acting!! Poor direction. VERY poor production. The movie was bad. Very bad movie. VERY BAD movie!'
  -- You could use NLTK to break the paragraph into sentence tokens for VADER, then average the results for the paragraph like this: 

It was one of the worst movies I've seen, despite good reviews.------ -0.7584
Unbelievably bad acting!!-------------------------------------------- -0.6572
Poor direction.------------------------------------------------------ -0.4767
VERY poor production.------------------------------------------------ -0.6281
The movie was bad.--------------------------------------------------- -0.5423
Very bad movie.------------------------------------------------------ -0.5849
VERY BAD movie!------------------------------------------------------ -0.7616
AVERAGE SENTIMENT FOR PARAGRAPH:  -0.6299

polarity_scores
================

- SentiText
- parse the SentiText words and 
  - RULE if the current is a booster BOOSTER_DICT append some valence to sentiments
  - else sentiment_valence: evaluate the sentiment of the current word (and append the value to sentiments)
- RULE _but_check: check for modification in sentiment due to contrastive conjunction 'but'

- RULE score_valence from all the sentiments values

SentiText
----------
- clean tokens (Identify sentiment-relevant string-level properties of input text.)
- RULE allcap_differential (Check whether just some words in the input are ALL CAPS)

sentiment_valence of a given word
-----------------
- RULE if the word has some valence (belongs to some lexicon) and it is the uppercase one among a sentence with cap_diff then add/sub C_INCR to its valence depending on its original valence
- in a range of three prior words 
  - RULE do a scalar_inc_dec i.e. Check if the preceding words increase, decrease, or negate/nullify the valence BOOSTER_DICT ; depending on the distance adjust the valence 
  - RULE _never_check 
  - RULE _idioms_check
- RULE _least_check check for negation case using "least" 


1.Punctuation, namely the exclamation point (!), increases the magnitude of the intensity without modifying the
semantic orientation. For example, “The food here is good!!!” is more intense than “The food here is good.”

2. Capitalization, specifically using ALL-CAPS to emphasize a sentiment-relevant word in the presence of other non-capitalized words, 
increases the magnitude of the sentiment intensity without affecting the semantic orientation. 
For example, “The food here is GREAT!” conveys more intensity than “The food here is great!”

3. Degree modifiers (also called intensifiers, booster words, or degree adverbs) impact sentiment intensity 
by either increasing or decreasing the intensity. 
For example, “The service here is extremely good” is more intense than “The service here is good”, 
whereas “The service here is marginally good” reduces the intensity.

4. The contrastive conjunction “but” signals a shift in sentiment polarity, with the sentiment of the text following the conjunction being dominant. 
“The food here is great, but the service is horrible” has mixed sentiment, with the latter half dictating the overall rating.

5. By examining the tri-gram preceding a sentiment-laden lexical feature, we catch nearly 90% of cases where negation flips the polarity of the text.
A negated sentence would be “The food here isn’t really all that great”.

                                                            relation          level                     intensity_magnitude  modify_semantic_orientation  
Punctuation                                                 in                proposition               increase             no
Capitalization_in_presence_of_other_non-capitalized_words   is                sentiment_relevant_word|booster|negation...   increase             no
Degree modifiers                                            preceding         sentiment_relevant_word   inc/decrease         no
Contrastive_conjunction_but                                 between           pair of propositions      dec prior/inc post   no
Negation                                                    3-gram preceding  sentiment_relevant_word   no                   yes
Contrastive_conjunction_despite                             between           pair of propositions      inc prior/dec post   no

It is not true that,
I do not think that he
"It was one of the worst movies I've seen, despite good reviews."
Despite these vague categories, one should not 
claim unequivocally that hostility between recognizable 
classes cannot be legitimately observed. Outside of New 
York, however, there were very few instances of openly 
expressed class antagonism.
http://examples.yourdictionary.com/examples-of-double-negatives.html Negatives Using Prefixes or words
"""

import nltk
import math
import pyrata.re as pyrata_re

from inspect import getsourcefile
from os.path import abspath, join, dirname

##Constants##

# (empirically derived mean sentiment intensity rating increase for booster words)
# B Booster
B_INCR = 0.293
B_DECR = -0.293

# (empirically derived mean sentiment intensity rating increase for using
# ALLCAPs to emphasize a word)
# C Capitalization
C_INCR = 0.733

# N Negative
N_SCALAR = -0.74


# for removing punctuation
#REGEX_REMOVE_PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

PUNC_LIST = [".", "!", "?", ",", ";", ":", "-", "'", "\"",
             "!!", "!!!", "??", "???", "?!?", "!?!", "?!?!", "!?!?"]
NEGATE = \
["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
 "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
 "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
 "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
 "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
 "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
 "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
 "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite", "n't", "at least"]



# check for special case idioms using a sentiment-laden keyword known to VADER
SPECIAL_CASE_IDIOMS = {"the shit": 3, "the bomb": 3, "bad ass": 1.5, "yeah right": -2,
                       "cut the mustard": 2, "kiss of death": -1.5, "hand to mouth": -2}



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def normalize(score, alpha=15):
  """
  Normalize the score to be between -1 and 1 using an alpha that
  approximates the max expected value
  """
  norm_score = score/math.sqrt((score*score) + alpha)
  if norm_score < -1.0: 
      return -1.0
  elif norm_score > 1.0:
      return 1.0
  else:
      return norm_score  

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def scalar_inc_dec(booster_raw_word, booster_word_scalar, valence, is_cap_diff):
    """
    Check if the preceding words increase, decrease, or negate/nullify the
    valence
    booster_word is lower
    """
    if valence < 0:
      booster_word_scalar *= -1
    #check if booster/dampener word is in ALLCAPS (while others aren't)
    if booster_raw_word.isupper() and is_cap_diff:
      if valence > 0:
         booster_word_scalar += C_INCR
      else: booster_word_scalar -= C_INCR
    return booster_word_scalar      

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def score_valence(sentiments):
  if sentiments:
    sum_s = float(sum(sentiments))

    compound = normalize(sum_s)
    # discriminate between positive, negative and neutral sentiment scores
    pos_sum, neg_sum, neu_count = _separate_sentiment_scores(sentiments)


    total = pos_sum + math.fabs(neg_sum) + neu_count
    pos = math.fabs(pos_sum / total)
    neg = math.fabs(neg_sum / total)
    neu = math.fabs(neu_count / total)

  else:
    compound = 0.0
    pos = 0.0
    neg = 0.0
    neu = 0.0

  sentiment_dict = \
      {"neg" : round(neg, 3),
       "neu" : round(neu, 3),
       "pos" : round(pos, 3),
       "compound" : round(compound, 4)}

  return sentiment_dict

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def _separate_sentiment_scores(sentiments):
  """ want separate positive versus negative sentiment scores"""
  pos_sum = 0.0
  neg_sum = 0.0
  neu_count = 0
  for sentiment_score in sentiments:
      if sentiment_score > 0:
          pos_sum += (float(sentiment_score) +1) # compensates for neutral words that are counted as 1
      if sentiment_score < 0:
          neg_sum += (float(sentiment_score) -1) # when used with math.fabs(), compensates for neutrals
      if sentiment_score == 0:
          neu_count += 1
  return pos_sum, neg_sum, neu_count


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def make_scored_lexicon_dict(read_data):
  """
  Convert lexicon file to a dictionary
  """
  lex_dict = dict()
  for line in read_data.split('\n'):
      if not(line.startswith('#')):
        (word, measure) = line.strip().split('\t')[0:2]
        lex_dict[word] = float(measure)
  return lex_dict


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def check_whether_just_some_words_in_the_input_are_ALL_CAPS(pyrata_tokens):
  """
  Check whether just some words (at least two characters) in the input are ALL CAPS
  """
  is_cap_diff = False
  if pyrata_re.search ('raw~"^[A-Z][A-Z]+$"', pyrata_tokens) and pyrata_re.search ('raw~"^[^A-Z][^A-Z]+$"', pyrata_tokens) :
    is_cap_diff = True
  return is_cap_diff

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class SentimentAnalyzer ():
  """
  Identify sentiment-relevant string-level properties of input text.
  """

  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def __init__(self):
    """
      load sentiment lexicon
      load booster lexicon
    """
    #
    _this_module_file_path_ = abspath(getsourcefile(lambda:0))

    sentiment_lexicon_filepath = "vader_sentiment_lexicon.txt"
    sentiment_lexicon_filepath = join(dirname(_this_module_file_path_), sentiment_lexicon_filepath)

    with open(sentiment_lexicon_filepath, encoding='utf-8') as f:
        read_data = f.read()
    self.sentiment_scored_lexicon = make_scored_lexicon_dict(read_data) # sentiment_word valency_score

    # booster/dampener 'intensifiers' or 'degree adverbs'
    # http://en.wiktionary.org/wiki/Category:English_degree_adverbs
    booster_lexicon_filepath = "vader_booster_lexicon.txt"
    booster_lexicon_filepath = join(dirname(_this_module_file_path_), booster_lexicon_filepath)

    with open(booster_lexicon_filepath, encoding='utf-8') as f:
        read_data = f.read()
    self.booster_scored_lexicon = make_scored_lexicon_dict(read_data) # sentiment_word valency_score

    #
    self.lexicons = dict()       # list of sentiment words and booster words referenced by a unique key
    self.lexicons['SENTIMENT'] = self.sentiment_scored_lexicon.keys()
    self.lexicons['BOOSTER'] = self.booster_scored_lexicon.keys()
    self.lexicons['NEGATE'] = NEGATE

    # pre 'compile pattern'
    #self.cp_negate = pyrata_re.compile('(lc@"NEGATE"|lc="at" lc="least"|lc~"n\'t")')
    #self.cp_never_so = pyrata_re.compile('lc="never" .? lc~"so|this"')
    #self.cp_booster = pyrata_re.compile('lc@"BOOSTER"')
    #self.cp_sentiment_chunk = pyrata_re.compile('([!lc@"SENTIMENT"]*) (lc@"SENTIMENT")')

  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def polarity_scores(self, pyrata_tokens):
    """ Return a float for sentiment strength based on the input tokenized text.
        Positive values are positive valence, negative value are negative
        valence. """
    
    # valence for each word
    sentiments = []

    # propositions (i.e. sub sentence)
    propositions = []

    # 
    is_cap_diff = check_whether_just_some_words_in_the_input_are_ALL_CAPS(pyrata_tokens)
    #print("{:-<15} {}".format("is_cap_diff", str(is_cap_diff)))

#     # 
#     but_groups = pyrata_re.search('([!lc="but"]*) lc="but" ([!lc="but"]*)', pyrata_tokens, lexicons=self.lexicons)
#     if but_groups != None: 
#       #print ('Debug: {}'.format(but_groups.group()))
#       for g in but_groups.groups()[1:]:
#         #print ('Debug: {}'.format(g[0]))
#         propositions.append(g[0])
#     else:
#       propositions.append(pyrata_tokens)

#     for i, p in enumerate(propositions):
#       #booster_star_wildcard_optional_sentiment = pyrata_re.findall('lc@"BOOSTER"* .? lc@"SENTIMENT"', pyrata_tokens, lexicons=self.lexicons)
#       #print ('Debug: {}'.format(booster_star_wildcard_optional_sentiment))
#       #booster_sentiment = pyrata_re.findall('(lc@"BOOSTER") (lc@"SENTIMENT")', pyrata_tokens, lexicons=self.lexicons)
#       #booster_not_booster_sentiment = pyrata_re.findall('(lc@"BOOSTER") [!lc@"BOOSTER"] (lc@"SENTIMENT")', pyrata_tokens, lexicons=self.lexicons)
# #       booster_option_sentiment = pyrata_re.finditer('(lc@"BOOSTER"?) (lc@"SENTIMENT")', pyrata_tokens, lexicons=self.lexicons)

# #       valence = 0
# #       for e in booster_option_sentiment:
# #         if len(e.groups()[1:]) == 2:
# #           booster = e.group(1)
# #           sentiment = e.group(2)
# #         else:
# #           sentiment = e.group(1)
# # #        print ('e(1)={} e(2)'.format())  
    # idea process sentiment chunks led by a sentiment head but how to handle negation declared in prior chunks
    # kinds of chunks
      # - negated
      # - but
      # - despite
      # - + booster
      # - + never so good 
    #no_sentiment_star_sentiment = self.cp_sentiment_chunk.finditer(pyrata_tokens, lexicons=self.lexicons)
    no_sentiment_star_sentiment = pyrata_re.finditer('([!lc@"SENTIMENT"]*) (lc@"SENTIMENT")', pyrata_tokens, lexicons=self.lexicons)
    # pre 'compile pattern'



    if no_sentiment_star_sentiment != None:
      for sentiment_chunk in no_sentiment_star_sentiment:
        #print ('e={}'.format(e))
        context = []
        if len(sentiment_chunk.groups()[1:]) == 2:
          context = sentiment_chunk.group(1)
          sentiment = sentiment_chunk.group(2)
        else:
          sentiment = sentiment_chunk.group(1)
        #print ('Debug: sentiment={}'.format(sentiment))
        #print ('Debug: sentiment[lc]={}'.format(sentiment[0]['lc']))
        valence = self.sentiment_scored_lexicon[sentiment[0]['lc']]
        #print ('Debug: sentiment={} valence={}'.format(sentiment[0]['lc'], valence))

        #print ('Debug: context={} tokens={}'.format(context, ' '.join([e['raw'] for e in pyrata_tokens])))

        # Check if the preceding words increase, decrease, or negate/nullify the valence
        #booster_in_context = self.cp_booster.finditer(context, lexicons=self.lexicons)
        booster_in_context = pyrata_re.finditer('lc@"BOOSTER"', context, lexicons=self.lexicons)

        if booster_in_context != None:
          #print ('booster_in_context={}'.format(booster_in_context))
          # FIXME distance from the sentiment word is not actually handled
          #print ('len(booster_in_context)={}'.format(len(booster_in_context)))
          distance_factor = 1 - len(booster_in_context) *0.05
          for booster in booster_in_context: # [0][::-1]: # browse in reverse order 
            #print ('booster={}'.format(booster.group(0)[0]))

            booster_scalar = scalar_inc_dec(booster.group(0)[0]['raw'], self.booster_scored_lexicon[booster.group(0)[0]['lc']], valence, is_cap_diff)
            # the more distant the less the factor is important and 
            distance_factor += 0.05
            valence = valence + booster_scalar * distance_factor

        # Determine if input contains negation words, n't or "at least"
        # FIXME reduce the context size?
        # FIXME handle double negatives?
        # FIXME distance from the sentiment word is not actually handled
        # TODO is_cap_diff like in scalar_inc_dec
        negative_scalar = 0.0
        #negative_in_context = pyrata_re.search('(lc@"NEGATE"|lc="at" lc="least"|lc~"n\'t")', context, lexicons=self.lexicons)
  #      negative_in_context = pyrata_re.search('(lc@"NEGATE"|lc="at" lc="least"|lc~"n\'t")', context, lexicons=self.lexicons)

#        negative_in_context = self.cp_negate.search(context, lexicons=self.lexicons)
        negative_in_context = pyrata_re.search('(lc@"NEGATE"|lc="at" lc="least"|lc~"n\'t")', context, lexicons=self.lexicons)
        if negative_in_context != None:
          #print ('negative_in_context={}'.format(negative_in_context))
          negative_scalar = N_SCALAR
        else:
          negative_in_context = pyrata_re.search('lc="never" .? lc~"so|this"', context, lexicons=self.lexicons)
          if negative_in_context != None:
            #print ('negative_in_context={}'.format(negative_in_context))
            negative_scalar = 1.5 # 1.25
        if negative_scalar != 0.0:    
          if negative_in_context.group(0)[0]['raw'].isupper() and is_cap_diff:
            if valence > 0:
              negative_scalar -= C_INCR
            else: negative_scalar += C_INCR
          valence = valence*negative_scalar


        #    
        sentiments.append(valence)
      else:
        print ('Debug: finditer return None')
        exit()

    #
    # #for word in pyrata_tokens:
    # for index in range (0, len(pyrata_tokens)):  
    #   word = pyrata_tokens[index]

    #   # Check if the preceding words increase, decrease, or negate/nullify the valence
    #   if (pyrata_re.match('raw@"BOOSTER"', pyrata_tokens, pos=index-1)):
    #     scalar = 0.0
    #     word_lower = word.lower()
    #     if word_lower in BOOSTER_DICT:
    #       scalar = BOOSTER_DICT[word_lower]
    #       if valence < 0:
    #           scalar *= -1
    #       #check if booster/dampener word is in ALLCAPS (while others aren't)
    #       if word.isupper() and is_cap_diff:
    #           if valence > 0:
    #               scalar += C_INCR
    #           else: scalar -= C_INCR
      
    #   sentiments.append(self.sentiment_valence(word['raw']))

    # # compute and add emphasis from punctuation in text
    # punct_emph_amplifier = self._punctuation_emphasis(sum_s, text)
    # if sum_s > 0:
    #     sum_s += punct_emph_amplifier
    # elif  sum_s < 0:
    #     sum_s -= punct_emph_amplifier

    # if pos_sum > math.fabs(neg_sum):
    #     pos_sum += (punct_emph_amplifier)
    # elif pos_sum < math.fabs(neg_sum):
    #     neg_sum -= (punct_emph_amplifier)

    #return normalize(float(sum(sentiments)))
    return score_valence(sentiments)

  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def label_polarity(self, pyrata_tokens):
    """ Label pos/neg/neu {'neu': 0.0, 'neg': 0.0, 'compound': 0.2263, 'pos': 1.0} """     

    vs = self.polarity_scores(pyrata_tokens)
    if vs['neg'] > vs['pos']: return 'neg'
    return 'pos' # for neu and pos

  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def booster_extraction (self, pyrata_tokens):
    """ Vader booster are ADV and +ing forms 
      extract such a lexicon on a training corpus based on the presence of 
      a vader sentiment lexicon in a near right context 
      
      as candidates we consider
      RB  Adverb
      RBR Adverb, comparative
      RBS Adverb, superlative 
      VBG Verb, gerund or present participl
    """     
    extracted_booster_expressions = pyrata_re.finditer('(pos~"RB.?|VBG"+) (lc@"SENTIMENT" ((lc~"\," .)* lc~"and|or" .)*)', pyrata_tokens, lexicons=self.lexicons)
    print ('-------------------------------------------------')
    for extracted_boosters in extracted_booster_expressions:
      #print ('Debug: pyrata_tokens={}'.format(pyrata_tokens))
      print ('---------------')
      #print ('Debug: len()={} extracted_boosters={}'.format(len(extracted_boosters.groups()), extracted_boosters))
      booster_candidate = extracted_boosters.group(1)
      vader_sentiment = extracted_boosters.group(2)

      context_size = 4
      f = extracted_boosters.start() -context_size if extracted_boosters.start()-context_size >=0 else 0
      t = extracted_boosters.start() +context_size+1 if extracted_boosters.start()+context_size+1 <len(pyrata_tokens) else len(pyrata_tokens)
      
      negate_expression = pyrata_re.search('lc@"NEGATE"', pyrata_tokens, lexicons=self.lexicons, pos=f, endpos=extracted_boosters.start(2))

      print ('Debug: f={} t={} context={} '.format(f, t, [tok['raw'] for tok in pyrata_tokens[f:t]]))

      if negate_expression != None: print ('Debug: negate is present={}'.format(negate_expression))

      if len(booster_candidate)>1:
        print ('Debug: multi word candidate={} with sentiment={}'.format([tok['raw'] for tok in booster_candidate], [tok['raw'] for tok in vader_sentiment]))

      else:
        #print ('Debug: booster_candidate={}'.format(booster_candidate))        
        #print ('Debug: booster_candidate[lc]={}'.format(booster_candidate[0]['lc']))
        if booster_candidate[0]['lc'] in  self.lexicons['BOOSTER']:
          print ('Debug: in vaderBooster candidate={} with sentiment={}'.format(booster_candidate[0]['raw'], [tok['raw'] for tok in vader_sentiment]))
        else:
          print ('Debug: new candidate={} with sentiment={}'.format(booster_candidate[0]['raw'], [tok['raw'] for tok in vader_sentiment]))



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_vader_sentences():


  sentences = ["VADER is smart , handsome , and funny .",      # positive sentence example
            "VADER is not smart , handsome , nor funny .",   # negation sentence example
            "VADER is smart , handsome , and funny !",       # punctuation emphasis handled correctly (sentiment intensity adjusted)
            "VADER is very smart , handsome , and funny .",  # booster words handled correctly (sentiment intensity adjusted)
            "VADER is VERY SMART , handsome , and FUNNY .",  # emphasis for ALLCAPS handled
            "VADER is VERY SMART , handsome , and FUNNY ! ! !",# combination of signals - VADER appropriately adjusts intensity
            "VADER is VERY SMART , uber handsome , and FRIGGIN FUNNY ! ! !",# booster words & punctuation make this close to ceiling for score
            "The book was good .",         # positive sentence
            "The book was kind of good .", # qualified positive sentence is handled correctly (intensity adjusted)
            "The plot was good , but the characters are uncompelling and the dialog is not great .", # mixed negation sentence
            "The plot was good , but the characters are uncompelling and the dialog is not great , but I enjoyed it anyway .", # two "but' mixed negation sentence
            "At least it isn't a horrible book .", # negated negative sentence with contraction
            "Make sure you :) or :D today !",     # emoticons handled
            "Today SUX !",    #  negative slang with capitalization emphasis
            "Today only kinda sux ! But I 'll get by , lol", # mixed sentiment example with slang and constrastive conjunction "but"
            "Sentiment analysis has never been good .",
                        "Sentiment analysis has never been this good !",
                        "Most automated sentiment analysis tools are shit .",
                        "With VADER , sentiment analysis is the shit !",
                        "Other sentiment analysis tools can be quite bad .",
                        "On the other hand , VADER is quite bad ass !",
                        "Roger Dodger is one of the most compelling variations on this theme .",
                        "Roger Dodger is one of the least compelling variations on this theme .",
                        "Roger Dodger is at least compelling as a variation on the theme ."]
  # for s in sentences:
  #   print (nltk.word_tokenize(s))
  # ['VADER', 'is', 'smart', ',', 'handsome', ',', 'and', 'funny', '.']
  # ['VADER', 'is', 'not', 'smart', ',', 'handsome', ',', 'nor', 'funny', '.']
  # ['VADER', 'is', 'smart', ',', 'handsome', ',', 'and', 'funny', '!']
  # ['VADER', 'is', 'very', 'smart', ',', 'handsome', ',', 'and', 'funny', '.']
  # ['VADER', 'is', 'VERY', 'SMART', ',', 'handsome', ',', 'and', 'FUNNY', '.']
  # ['VADER', 'is', 'VERY', 'SMART', ',', 'handsome', ',', 'and', 'FUNNY', '!', '!', '!']
  # ['VADER', 'is', 'VERY', 'SMART', ',', 'uber', 'handsome', ',', 'and', 'FRIGGIN', 'FUNNY', '!', '!', '!']
  # ['The', 'book', 'was', 'good', '.']
  # ['The', 'book', 'was', 'kind', 'of', 'good', '.']
  # ['The', 'plot', 'was', 'good', ',', 'but', 'the', 'characters', 'are', 'uncompelling', 'and', 'the', 'dialog', 'is', 'not', 'great', '.']
  # ['At', 'least', 'it', 'is', "n't", 'a', 'horrible', 'book', '.']
  # ['Make', 'sure', 'you', ':', ')', 'or', ':', 'D', 'today', '!']
  # ['Today', 'SUX', '!']
  # ['Today', 'only', 'kinda', 'sux', '!', 'But', 'I', "'ll", 'get', 'by', ',', 'lol']


    # tricky_sentences = ["Sentiment analysis has never been good.",
    #                     "Sentiment analysis has never been this good!",
    #                     "Most automated sentiment analysis tools are shit.",
    #                     "With VADER, sentiment analysis is the shit!",
    #                     "Other sentiment analysis tools can be quite bad.",
    #                     "On the other hand, VADER is quite bad ass!",
    #                     "Roger Dodger is one of the most compelling variations on this theme.",
    #                     "Roger Dodger is one of the least compelling variations on this theme.",
    #                     "Roger Dodger is at least compelling as a variation on the theme."

  sa = SentimentAnalyzer()       

  for sentence in sentences:

    # nlp
    tokens = sentence.split()
    tokens_pos = nltk.pos_tag(tokens)
    pyrata_tokens = [{'raw':w, 'pos':p, 'lc':w.lower()} for (w, p) in tokens_pos]

    # sentiment analysis
    vs = sa.polarity_scores(pyrata_tokens)
    print("{:-<65} {}".format(sentence, str(vs)))

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_movie_reviews():
  """ http://www.cs.cornell.edu/people/pabo/movie-review-data/
      http://www.nltk.org/book/ch06.html


      https://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/
https://streamhacker.com/2010/05/24/text-classification-sentiment-analysis-stopwords-collocations/
      https://streamhacker.com/2010/06/16/text-classification-sentiment-analysis-eliminate-low-information-features/


evaluating single word features
accuracy: 0.728
pos precision: 0.651595744681
pos recall: 0.98
neg precision: 0.959677419355
neg recall: 0.476


evaluating best word features
accuracy: 0.93
pos precision: 0.890909090909
pos recall: 0.98
neg precision: 0.977777777778
neg recall: 0.88


Signficant Bigrams
evaluating best words + bigram chi_sq word features
accuracy: 0.92
pos precision: 0.913385826772
pos recall: 0.928
neg precision: 0.926829268293
neg recall: 0.912


NaiveBayesClassifier
train on 1900 instances, test on 100 instances
pos precision: 0.7435897435897436
pos recall: 0.5370370370370371
pos F-measure: 0.6236559139784946
neg precision: 0.5901639344262295
neg recall: 0.782608695652174
neg F-measure: 0.6728971962616822

Rules-based SentimentAnalyzer
pos precision:0.6031746031746031
pos recall:0.7037037037037037
pos F-measure:0.6495726495726496
neg precision:0.5675675675675675
neg recall:0.45652173913043476
neg F-measure:0.5060240963855421


      """

  from nltk.corpus import movie_reviews
  from nltk.metrics import precision, recall, f_measure
  from nltk.classify import NaiveBayesClassifier
  import random  
  import collections

  # data
  documents = [(list(movie_reviews.words(fileid)), category)
    for category in movie_reviews.categories()
    for fileid in movie_reviews.fileids(category)]
  
  #random.shuffle(documents)
  
  # SET this line is only present for some debug reason. Remove it when the development is done.
  documents = documents[:200]

  train_docs = documents[100:]
  test_docs = documents[:100]


  # negids = movie_reviews.fileids('neg')
  # posids = movie_reviews.fileids('pos')

  # negfeats = [(featx(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
  # posfeats = [(featx(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

  # negcutoff = len(negfeats)*3/4
  # poscutoff = len(posfeats)*3/4

  # trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
  # testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
 
 

  # Machine Learning approach
  do_ML = False                             # SET  
  refsets = collections.defaultdict(set)

  if do_ML:
    print ('NaiveBayesClassifier')

    # preprocessing 
    print ('+ preprocessing')  
    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    word_features = list(all_words)[:2000] 

    def document_features(document): 
      document_words = set(document) 
      features = {}
      for word in word_features:
          features['contains({})'.format(word)] = (word in document_words)
      return features

    train_featuresets = [(document_features(d), c) for (d,c) in train_docs]
    test_featuresets = [(document_features(d), c) for (d,c) in test_docs]

    # training
    print ('+ train on %d instances' % (len(train_featuresets)))
    classifier = nltk.NaiveBayesClassifier.train(train_featuresets)


    # testing
    print ('+ test on %d instances' % ( len(test_featuresets)))
    classifier_hypsets = collections.defaultdict(set)
    
    for i, (feats, label) in enumerate(test_featuresets):
      refsets[label].add(i)
      classifier_hyp = classifier.classify(feats)
      classifier_hypsets[classifier_hyp].add(i)
   
    print ('pos precision:', precision(refsets['pos'], classifier_hypsets['pos']))
    print ('pos recall:', recall(refsets['pos'], classifier_hypsets['pos']))
    print ('pos F-measure:', f_measure(refsets['pos'], classifier_hypsets['pos']))
    print ('neg precision:', precision(refsets['neg'], classifier_hypsets['neg']))
    print ('neg recall:', recall(refsets['neg'], classifier_hypsets['neg']))
    print ('neg F-measure:', f_measure(refsets['neg'], classifier_hypsets['neg']))


  # 
  print ('Rules-based SentimentAnalyzer')
  sa = SentimentAnalyzer()       

  # preprocessing 
  print ('+ preprocessing')  

  def pyrata_structure_as_features (doc):
    tokens_pos = nltk.pos_tag(doc)
    pyrata_tokens = [{'raw':w, 'pos':p, 'lc':w.lower()} for (w, p) in tokens_pos]
    return pyrata_tokens

  train_featuresets = [(pyrata_structure_as_features(d), c) for (d,c) in train_docs]
  test_featuresets = [(pyrata_structure_as_features(d), c) for (d,c) in test_docs]

  #
  print ('+ train on %d instances' % (len(train_featuresets)))
  for i, (doc, label) in enumerate(train_featuresets):
    print ('Debug: label={}'.format(label))
    sa.booster_extraction(doc)

  # testing
  print ('+ test on %d instances' % (len(test_featuresets)))  
  rules_based_hypsets = collections.defaultdict(set)

  for i, (doc, label) in enumerate(test_featuresets):
    #print ('Debug: doc={}'.format(doc))

    rules_based_hyp = sa.label_polarity(doc)
    rules_based_hypsets[rules_based_hyp].add(i)
 
  print ('pos precision:{:10}'.format(precision(refsets['pos'], rules_based_hypsets['pos'])))
  print ('pos recall:{:10}'.format(recall(refsets['pos'], rules_based_hypsets['pos'])))
  print ('pos F-measure:{:10}'.format(f_measure(refsets['pos'], rules_based_hypsets['pos'])))
  print ('neg precision:{:10}'.format(precision(refsets['neg'], rules_based_hypsets['neg'])))
  print ('neg recall:{:10}'.format(recall(refsets['neg'], rules_based_hypsets['neg'])))
  print ('neg F-measure:{:10}'.format(f_measure(refsets['neg'], rules_based_hypsets['neg'])))



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  #test_vader_sentences()
  test_movie_reviews()