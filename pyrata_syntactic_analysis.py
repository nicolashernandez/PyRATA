# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to evaluate the semantic of a given pattern step
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ply.yacc as yacc
from pyrata_lexer import *
from pyrata_syntactic_pattern_parser import *


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class CompiledPattern(object):
  lexer = None

  def __init__(self, **kwargs):
    if 'lexer' in kwargs.keys():
      self.lexer = kwargs['lexer']

  def getLexer(self):
    return self.lexer

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