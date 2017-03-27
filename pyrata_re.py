# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from pyrata_lexer import *
import pyrata_syntactic_analysis
import pyrata_semantic_analysis


    
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def compile (pattern, **kwargs):    
  """ 
  Compile a regular expression pattern into a regular expression object, 
  which can be used for matching using match(), search()... methods, described below.
  """
  
  verbosity = 0
  if 'verbosity' in kwargs.keys():
    verbosity = kwargs['verbosity']

  l = pyrata_syntactic_analysis.parse_syntactic(pattern, **kwargs)

  return pyrata_syntactic_analysis.CompiledPattern(lexer=l, **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def search (pattern, data, **kwargs):
  """ Scan through data looking for the first location where the regular expression pattern produces a match, 
      and return a corresponding match object. 
      Return None if no position in the data matches the pattern."""

  verbosity  = 0
  if 'verbosity' in kwargs.keys(): 
    verbosity  = kwargs['verbosity']
  
  method = 'search'

  lexicons = {}
  if 'lexicons' in kwargs.keys():
    lexicons = kwargs['lexicons']

  if verbosity >1:
      print (1*'  ','Method:\t', method) 
      print (1*'  ','Lexicons:\t', lexicons)       
      print (1*'  ','Pattern:\t', pattern)
      print (1*'  ','Data:\t\t', data)  

  compiledPattern = compile(pattern, **kwargs)

  compiledPattern.getLexer().lexer.re = method

  kwargs.pop('lexicons', None)
  matcheslist = pyrata_semantic_analysis.parse_semantic (compiledPattern, data, **kwargs)

  if len(matcheslist) > 0 :
    return matcheslist.group(0)
  return None



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def findall (pattern, data, **kwargs):
  """ Return all non-overlapping matches of pattern in data, as a list of datas. 
      The data is scanned left-to-right, and matches are returned in the order found. 
      #If one or more groups are present in the pattern, return a list of groups; 
      #this will be a list of tuples if the pattern has more than one group. 
      #Empty matches are included in the result unless they touch the beginning of another match.
  """
  verbosity  = 0
  if 'verbosity' in kwargs.keys(): 
    verbosity  = kwargs['verbosity']

  lexicons = {}
  if 'lexicons' in kwargs.keys():
    lexicons = kwargs['lexicons']

  
  method = 'findall' 
  
  if verbosity >1:
    print ('Method:\t', method) 
    print ('Lexicons:\t', lexicons)       
    print ('Pattern:\t', pattern)
    print ('Data:\t\t', data)  
 
  compiledPattern = compile(pattern, lexicons=lexicons, verbosity=verbosity)

  compiledPattern.getLexer().lexer.re = method

  kwargs.pop('lexicons', None)
  matcheslist = pyrata_semantic_analysis.parse_semantic (compiledPattern, data, **kwargs)

  # build the structure to return
  matches = []
  if len(matcheslist)>0 :
    for i in range(len(matcheslist)):
      #print ('Debug: len(data):',len(data),'; start:', start,'; end:',end)
      matches.append(matcheslist.group(i).group())
    return matches
  return None

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def finditer (pattern, data, **kwargs):
  """
  Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in data. 
  The data is scanned left-to-right, and matches are returned in the order found. 
  #Empty matches are included in the result unless they touch the beginning of another match.
  """
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

  compiledPattern = compile(pattern, lexicons=lexicons, verbosity=verbosity)

  compiledPattern.getLexer().lexer.re = method

  kwargs.pop('lexicons', None)
  matcheslist = pyrata_semantic_analysis.parse_semantic (compiledPattern, data, **kwargs)

  # build the structure to return
  if len(matcheslist)>0 :
    return matcheslist    
  return None 



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  # TODO
  pattern = 'pos="JJ" pos="NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     

  pyrata_re.search(pattern,data)    