# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# compare the time performance of pyrata with
# 
# pattern
# http://www.clips.ua.ac.be/pages/pattern-search
# The search() function takes a string (e.g., a word or a sequence of words) and returns a list of non-overlapping matches in the given sentence. 
# The match() function returns the first match, or None.
#
# python.chunk
# spacy
#
# textblob
# http://rwet.decontextualize.com/book/textblob/
#
# to find all patterns of noun phrases Determiner Adjectives Nouns
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import sys
import logging
from timeit import Timer
from nltk.corpus import brown


#import pyrata.re

from pattern.en import parsetree
from pattern.search import search



#import timeit




# --------------------------------------------------------------------
def measure_pattern_search():
  """ pattern 
      JJ|NN* NN*
      DT? JJ|NN?+ NN
      DT? JJ|NN*+ NN*
  """
  global pattern_search_result    #Make measure_me able to modify the value
  #print ('text_tree', text_tree)
  pattern_search_result = search(pattern_string, text_tree)
  #print ('pattern_string:',pattern_string)
  #print ('pattern_search_result',pattern_search_result)






# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run benchmark
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  #
  #logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='benchmark.log', level=logging.INFO)
  #logger = logging.getLogger()
  #logger.disabled = True


  iteration_number = 1
  iteration_number = int(sys.argv[1])

  word_number = int(sys.argv[2])

  argv = sys.argv
  argv.pop(0)
  argv.pop(0)
  argv.pop(0)

  pattern_string = "DT? JJ|NN?+ NN"
  pattern_string = ' '.join(argv)

  #print ('iteration_number',iteration_number)
  #print ('word_number',word_number)
  #print ('pattern_string',pattern_string)


  # Load brown
  # ----------------------------------------
  words = brown.words()[:word_number]
  #len(words)
  #1 161 192
  #print ('join brown words')

  text = ' '.join(words)
  #print ('text',text)
  #len(text)
  # 6 127 073

  # pattern setup
  # ----------------------------------------
  # The parse() function takes a string of text and returns a part-of-speech tagged Unicode string. Sentences in the output are separated by newline characters.
  # A parse tree stores a tagged string as a tree of nested objects that can be traversed to analyze the constituents in the text. The parsetree() function takes the same parameters as parse() and returns a Text object. 
  #logging.info("pattern setup")
  #print ('pattern parsetree')
  text_tree = parsetree(text,
   tokenize = True,         # Split punctuation marks from words?
       tags = True,         # Parse part-of-speech tags? (NN, JJ, ...)
     chunks = False,         # Parse chunks? (NP, VP, PNP, ...)
  relations = False,        # Parse chunk relations? (-SBJ, -OBJ, ...)
    lemmata = False,        # Parse lemmata? (ate => eat)
   encoding = 'utf-8',       # Input string encoding.
     tagset = None)         # Penn Treebank II (default) or UNIVERSAL.
  
  pattern_search_result = []     

  #print ('timer declaration')
  pattern_search_time = Timer(measure_pattern_search)

  #logging.info("pattern timeit")
  #print ('timeit pattern')
  #print (pattern_search_time.timeit(number=iteration_number))
  runtimes = [pattern_search_time.timeit(number=1) for i in range (0, iteration_number)]
  average = sum(runtimes)/len(runtimes)
  print (''.join(['timit: #runs=', str(iteration_number), ' ; average=',str(average),' ; min=', str(min(runtimes))]))

  #print (pattern_search_result)
