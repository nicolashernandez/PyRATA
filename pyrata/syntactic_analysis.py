# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to evaluate the semantic of a given pattern step
# 
# Follows the https://docs.python.org/3/library/re.html#re-objects API
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ply.yacc as yacc
from pyrata.lexer import *
from pyrata.syntactic_pattern_parser import *
import sys # for the function name
import pyrata.semantic_analysis


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class CompiledPattern(object):
  lexer = None

  def __init__(self, **kwargs):
    if 'lexer' in kwargs.keys():
      self.lexer = kwargs['lexer']

  def getLexer(self):
    return self.lexer


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def re_method(self, data, **kwargs):
    """
    """

    if 'method' in kwargs.keys(): 
      method  = kwargs['method']
    else:
      raise Exception ('Error: in ', sys._getframe().f_code.co_name,': no re method defined')
    kwargs.pop('method', None)

    self.getLexer().lexer.re = method

    #exit() # FIXME used to stop the parsing after the syntactic analysis (to see the parser.out or adapt the parser)
    #print ('Debug: compiledPattern=', self)
    r = pyrata.semantic_analysis.parse_semantic (self, data, **kwargs)
    return r

  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def search(self, data, **kwargs):
    """
    """

    method = 'search'
    matcheslist = self.re_method (data, method=method, **kwargs)

    if len(matcheslist) > 0 :
      return matcheslist.group(0)
    return None




  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def match(self, data, **kwargs):
    """
    """
    raise Exception ('Not implemented yet')


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def findall(self, data, **kwargs):
    """
    """
    method = 'findall'
    matcheslist = self.re_method (data, method=method, **kwargs)
    matches = []
    if len(matcheslist)>0 :
      for i in range(len(matcheslist)):
        #print ('Debug: len(data):',len(data),'; start:', start,'; end:',end)
        matches.append(matcheslist.group(i).group())
      return matches
    return None



  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def finditer(self, data, **kwargs):
    """
    """

    method = 'finditer'
    matcheslist = self.re_method (data, method=method, **kwargs)

    # build the structure to return
    if len(matcheslist)>0 :
      return matcheslist    
    return None 


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def split(self, data, **kwargs):
    """
    """
    raise Exception ('Not implemented yet')


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def sub(self, data, **kwargs):
    """
    """
    raise Exception ('Not implemented yet')


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def parse_syntactic(pattern, **kwargs):

  verbosity  = 0
  if 'verbosity' in kwargs.keys(): 
    verbosity  = kwargs['verbosity']

  lexicons = {}
  if 'lexicons' in kwargs.keys():
    lexicons = kwargs['lexicons']
    kwargs.pop('lexicons', None)

     # Build the lexer 
  l = Lexer(pattern=pattern, lexicons=lexicons)

  # Build the syntax parser
  y = SyntacticPatternParser(tokens=l.tokens, **kwargs)

  # we start the compilation to get an internal representation of patterns
  if verbosity >1:
    print (1*'  ','________________________________________________')      
    print (1*'  ','Info: syntax parsing...')
  y.parser.parse(pattern, l.lexer, tracking=True)

  return l
