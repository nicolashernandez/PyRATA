# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from pyrata.lexer import *
import pyrata.syntactic_analysis
import pyrata.semantic_analysis


    
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def compile (pattern, **kwargs):    
  """ 
  Compile a regular expression pattern into a regular expression object, 
  which can be used for matching using match(), search()... methods, described below.
  """
  
  verbosity = 0
  if 'verbosity' in kwargs.keys():
    verbosity = kwargs['verbosity']

  l = pyrata.syntactic_analysis.parse_syntactic(pattern, **kwargs)

  return pyrata.syntactic_analysis.CompiledPattern(lexer=l, **kwargs)


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
      print (1*'  ','Method:\t', method) 
      print (1*'  ','Lexicons:\t', lexicons)       
      print (1*'  ','Pattern:\t', pattern)
      print (1*'  ','Data:\t\t', data)  
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
 

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  # TODO
  pattern = 'pos="JJ" pos="NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     

  pyrata.re.search(pattern,data)    