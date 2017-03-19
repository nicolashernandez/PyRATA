# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import logging
from os import path #, getcwd, chdir
import ply.lex as lex


#logger = logging.getLogger(__name__)

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Lexer(object):
  """
  Lexical Analysis: 
  converting a sequence of characters into a sequence of tokens
  Init and build methods.
  """


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Tokens Definitions
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  literals = ['"']

  tokens = (
    'NAME', 
    'VALUE', 
    'EQ', 'MATCH', 'IN',
    'AND', 'OR',
    'LBRACKET','RBRACKET',
    'LPAREN','RPAREN',
    'NOT',
    'OPTION',
    'ATLEASTONE',
    'ANY'
    )
# EOI end of instruction
#    ,'IS',
   # 'QUOTE',
  #  'LPAREN','RPAREN',
# Tokens

  t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
  #t_VALUE    = r'\"[a-zA-Z_][a-zA-Z0-9_]*\"' # FIXME whatever character except un excaped QUOTE 
  #found at http://wordaligned.org/articles/string-literals-and-regular-expressions
  #TODO: This does not work with the string "bla \" bla"
  #t_STRING_LITERAL = r'"([^"\\]|\\.)*"'
  t_VALUE = r'\"([^\\\n]|(\\.))*?\"'

  t_EQ  = r'='
  t_MATCH  = r'\~'
  t_IN  = r'\@'
  #t_QUOTE  = r'"'
  t_AND  = r'&'
  t_OR  = r'\|'
  t_NOT  = r'!' # contrainte sur l'existance de l'attribute name pas sur sa valeur
  t_LBRACKET  = r'\['
  t_RBRACKET  = r'\]'
  t_LPAREN  = r'\('
  t_RPAREN  = r'\)'
  t_OPTION  = r'\?'
  t_ATLEASTONE  = r'\+'
  t_ANY  = r'\*'
#t_EOI  = r'\;'

  # Ignored characters
  t_ignore = " \t"


  def t_NUMBER(self,t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


  # Define a rule so we can track line numbers
  # http://www.dabeaz.com/ply/ply.html#ply_nn9
  def t_newline(self,t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    #t.lexer.lineno += len(t.value)

  # Compute column. 
  # http://www.dabeaz.com/ply/ply.html#ply_nn9
  #     input is the input text string
  #     token is a token instance
  def find_column(self, input, token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
      last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Constructor
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def __init__(self, **kwargs): # pattern, data, re):
    
    data = ''
    if 'data' in kwargs.keys():
      data = kwargs['data']
      kwargs.pop('data', None)
    
    re = 'search'
    if 're' in kwargs.keys():
      re = kwargs['re']
      kwargs.pop('re', None)      

    lexicons = {}
    if 'lexicons' in kwargs.keys():
      lexicons = kwargs['lexicons']
      kwargs.pop('lexicons', None)

    self.verbosity  = 0      
    if 'verbosity' in kwargs.keys(): 
      self.verbosity  = kwargs['verbosity']
      kwargs.pop('verbosity', None)

    if not ('pattern' in kwargs.keys()):
      raise Exception('In',__file__,' pattern argument should be set in the constructor')
    pattern = kwargs['pattern'] 
    kwargs.pop('pattern', None)

    #print ("Debug: kwargs=", kwargs) 
    self.build(pattern, **kwargs)
    

    # store dict of lists, a list being used to store a lexicon 
    self.lexer.lexicons = lexicons
    

    # data structure (list of dicts) explored by the pattern  
    self.lexer.data = data

    # re method 
    # search: Scan through data looking for the first location where the regular expression pattern produces a match, and return a corresponding match object. 
    # findall: Return all non-overlapping matches of pattern in data, as a list of datas. 
    # finditer: Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in data.
    self.lexer.re = re

    # list of start/end index of each recognized group 
    # TODO how to handle multiple rules in a single grammar... each rule should have an identifier... and its own groupindex
    self.lexer.groupstartindex = [] # (the first one is the whole match)  
    self.lexer.groupendindex = []  # (the last one is the whole match)  

    # variable used to distinguish the first step (and consequently the start position of the pattern) from the others
    self.lexer.matchongoing = False

    # position in the data from where the pattern is applied 
    self.lexer.lastFirstExploredDataPosition = 0      

    # position in the data that is explored by the current rule
    self.lexer.currentExploredDataPosition = self.lexer.lastFirstExploredDataPosition 

    # the whole pattern
    # self.lexer.lexdata
  

    # list of LexToken (self.type, self.value, self.lineno, self.lexpos)
    self.lexTokenList = [] 

    # map endposition to lextoken (by getting the len(.value of the element), 
    # you can then get the endposition of the previous element, useful to delimit quantified steps 
    # indeed, p.lexer.lexpos attribute is an integer that contains the current position within the input text.
    # Within token rule functions, this points to the first character after the matched text 
    # and the matched text includes the next lextToken (not only reduced to a single char).
    self.lexTokenEndDict = {} 



    # the pattern part which is in focus when processing a quantifier ; 
    self.lexer.localstep = '' 

    # in the context of local step pattern the step is bare wo quantifier but globally it comes with so 
    # (log use case) 
    self.lexer.patternStep = None

    # cursor to follow the parsing progress in the pattern (log use case) 
    self.lexer.patternStepPosition = 0

    # to exchange information between global and local parser when dealing with quantifiers
    # indicate the local parser that it is a local one
    self.lexer.islocal = 0 

    # as a global one, get the result of the local one
    self.lexer.localresult = False # 

    # store the result after parsing the pattern given a certain data (context)
    self.lexer.expressionresult = False # 


#  def __init__(self, debug=False):
#    self.tokens = (
#      self.delimiters + self.operators +
#      self.misc + list(set(self.reserved.values())))
#    self.build(debug=debug)



  def build(self, pattern, **kwargs):
    """
    Create a lexer.
    """
    self.lexer = lex.lex(module=self, errorlog=lex.NullLogger(), **kwargs) #
    self.lexer.input(pattern)
    self.storeLexTokenList()


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  more
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def t_error(self, t):

    #raise Exception('Illegal character "{t}"'.format(t=t.value[0]))
    if self.verbosity>0:
      print ('Lexer: Illegal character "{}" found at lineno "{}"" and lexpos "{}". We skip the character. It is probably due to unexpected characters which leads to a tokenization error. Search before this position. Current tokenization results in {}'.format(t.value[0], t.lexer.lineno, t.lexpos, t.lexer.lexTokenList))
    t.lexer.skip(1)
    #while True:
    #  tok = self.lexer.token()
    #  if not tok: 
    #    break      # No more input

  def storeLexTokenList(self):
    """ store the the list of the LexToken
    and a map from the end position of a lextoken to the lextoken """

    self.lexer.lexTokenEndDict = {}
    self.lexer.lexTokenList = [] # LexToken (self.type, self.value, self.lineno, self.lexpos)
    while True:
      tok = self.lexer.token()
      if not tok: 
        break      # No more input
      #print(tok)
      self.lexer.lexTokenList.append(tok)
      self.lexer.lexTokenEndDict[tok.lexpos+len(tok.value)] = tok
    #print (lexTokenList)  
    # reinit the lexer
    self.lexer.input(self.lexer.lexdata)
  
#  def build(self, debug=False, debuglog=None, **kwargs):
    # """Create a lexer."""
    # if debug and debuglog is None:
    #   debuglog = self.logger
    #   self.lexer = ply.lex.lex(
    #     module=self,
    #     debug=debug,
    #     debuglog=debuglog,
    #     **kwargs)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  example of use
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':
  pattern = 'lem="the" +pos@"positiveLexicon" pos~"NN.?" [lem="be" & !(raw="is" | raw="are")]\n'

  print ("Tokenize the given pattern:", pattern)
  myLexer = Lexer(pattern=pattern, data=[], re='search', verbosity=1)
  while True:
    tok = myLexer.lexer.token()
    if not tok: 
      break      # No more input
    print(tok)