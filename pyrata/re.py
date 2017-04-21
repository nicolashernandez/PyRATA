# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import logging
import re

from pyrata.lexer import *
import pyrata.compiled_pattern_re
import pyrata.semantic_pattern_parser

(PREFIX_BEGIN, PREFIX_INSIDE, PREFIX_OTHER) = ('B-', 'I-', 'O-')

   
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def normalize_chunk_operator (pattern, **kwargs):    
  '''
  Here is a trick. The chunk operator does not exist. 
  It is turn into a specific sequence of steps with equal operators.
  Indeed 'ch-"NP"' is rewritten in '(ch="B-NP" ch="I-NP"*)'
  '''
  return re.sub('([a-zA-Z_][a-zA-Z0-9_]*)-\"(([^\\\n]|(\\.))*?)\"', '(\g<1>="B-\g<2>" \g<1>="I-\g<2>"*)', pattern) 

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def compile (pattern, **kwargs):    
  """ 
  Compile a regular expression pattern into a regular expression object, 
  which can be used for matching using match(), search()... methods, described below.
  """
  
  verbosity = 0
  if 'verbosity' in kwargs.keys():
    verbosity = kwargs['verbosity']

  l = pyrata.compiled_pattern_re.parse_syntactic(normalize_chunk_operator(pattern), **kwargs)

  return pyrata.compiled_pattern_re.CompiledPattern(lexer=l, **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def search (pattern, data, **kwargs):
  """ Scan through data looking for the first location where the regular expression pattern produces a match, 
      and return a corresponding match object. 
      Return None if no position in the data matches the pattern."""

  ''' -.- log -.- '''
  verbosity  = 0
  if 'verbosity' in kwargs.keys(): 
    verbosity  = kwargs['verbosity']
  
  lexicons = {}
  if 'lexicons' in kwargs.keys():
    lexicons = kwargs['lexicons']
    kwargs.pop('lexicons', None)

  method = 'search'
  if verbosity >1:
      print ('  ','Method:\t', method) 
      print ('  ','Lexicons:\t', lexicons)       
      print ('  ','Pattern:\t', pattern)
      print ('  ','Data:\t\t', data)  
  ''' -.- /log -.- '''

  # lexicons are passed by parameters via kwargs
  compiledPattern = compile(pattern, lexicons=lexicons, **kwargs)

  return compiledPattern.search(data, **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def findall (pattern, data, **kwargs):
  """ Return all non-overlapping matches of pattern in data, as a list of datas. 
      The data is scanned left-to-right, and matches are returned in the order found. 
      #If one or more groups are present in the pattern, return a list of groups; 
      #this will be a list of tuples if the pattern has more than one group. 
      #Empty matches are included in the result unless they touch the beginning of another match.
  """

  ''' -.- log -.- '''
  verbosity  = 0
  if 'verbosity' in kwargs.keys(): 
    verbosity  = kwargs['verbosity']

  lexicons = {}
  if 'lexicons' in kwargs.keys():
    lexicons = kwargs['lexicons']
    kwargs.pop('lexicons', None)

  method = 'findall' 
  
  if verbosity >1:
    print ('Method:\t', method) 
    print ('Lexicons:\t', lexicons)       
    print ('Pattern:\t', pattern)
    print ('Data:\t\t', data)  
  ''' -.- /log -.- '''
 
  # lexicons are passed by parameters via kwargs
  compiledPattern = compile(pattern, lexicons=lexicons,  **kwargs)

  return compiledPattern.findall(data, **kwargs)



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def finditer (pattern, data, **kwargs):
  """
  Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in data. 
  The data is scanned left-to-right, and matches are returned in the order found. 
  #Empty matches are included in the result unless they touch the beginning of another match.
  """

  ''' -.- log -.- '''
  verbosity  = 0
  if 'verbosity' in kwargs.keys(): 
    verbosity  = kwargs['verbosity']

  lexicons = {}
  if 'lexicons' in kwargs.keys():
    lexicons = kwargs['lexicons']
    kwargs.pop('lexicons', None)

  method = 'finditer'

  if verbosity >1:
    print (1*'  ','Method:\t', method) 
    print (1*'  ','Lexicons:\t', lexicons)       
    print (1*'  ','Pattern:\t', pattern)
    print (1*'  ','Data:\t\t', data)  
  ''' -.- /log -.- '''

  # lexicons are passed by parameters via kwargs
  compiledPattern = compile(pattern, lexicons=lexicons,  **kwargs)

  return compiledPattern.finditer(data, **kwargs)

# 16:15
# 18 et 19 

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def annotate (pattern, annotation, data, group = [0], action = 'sub', iob = False, **kwargs): # group=[0]
  """ 
  Do one of the following process on a copy of the data
  * sub/substitutes a match or a group of a match with a dict or a sequence of dicts (in case of dict we turn it into list of dict to process it the same way)
  * updates (and extends) the features of a match or a group of a match with the features of a dict or a sequence of dicts (of the same size as the group/match
  * extends (i.e. if a feature exists then do not update) the features of a match or a group of a match with the features of a dict or a sequence of dicts (of the same size as the group/match
  * updates|extends the features of a match or a group of a match with IOB values of the features of a dict or a sequence of dicts (of the same size as the group/match or kwargs ?
  Return the data obtained.  If the pattern isn't found, data is returned unchanged.
  """
  prefix = ''

  data_copy = list(data)
  if isinstance(annotation, dict):
    annotation = [annotation]

  iter = finditer(pattern, data) #reversed([finditer(pattern, data)])  
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
                  data_copy = data  
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
                  data_copy = data  
                  break                   
  return data_copy


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def sub (pattern, repl, data, group = [0], **kwargs):
  """
  Return the data obtained by replacing the leftmost non-overlapping occurrences of 
  pattern matches or group of matches in data by the replacement repl. 
  """
  return annotate (pattern, repl, data, group, action = 'sub', iob = False, **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def subn (pattern, repl, data, **kwargs):
  """
  Perform the same operation as sub(), but return a tuple (new_string, number_of_subs_made).
  """
  raise Exception ("Not implemented yet !")

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def update (pattern, repl, data, group = [0], iob = False, **kwargs):
  """
  Return the data after updating (and extending) the features of a match or a group of a match 
  with the features of a dict or a sequence of dicts (of the same size as the group/match). 
  """
  return annotate (pattern, repl, data, group = group, action = 'update', iob = iob, **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def extend (pattern, repl, data, group = [0], iob = False, **kwargs):
  """
  Return the data after updating (and extending) the features of a match or a group of a match 
  with the features of a dict or a sequence of dicts (of the same size as the group/match). 
  """
  return annotate (pattern, repl, data, group = group, action = extend, iob = iob, **kwargs)

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  # TODO
  pattern = 'pos="JJ" pos="NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     

  pyrata.re.search(pattern,data)    