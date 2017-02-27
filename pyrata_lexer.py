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


class Lexer(object):
  """Init and build methods."""



  literals = [ '"']

  tokens = (
    'NAME', 'VALUE', 'IS',
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
  t_VALUE    = r'\"[a-zA-Z_][a-zA-Z0-9_]*\"' # FIXME whatever character except un excaped QUOTE 
  t_IS  = r':'
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


  def t_newline(self,t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

  
  def __init__(self, **kwargs): # grammar, data, re):
    # grammar is at least a pattern definition

    # print (kwargs)
    data = ''
    if 'data' in kwargs.keys():
      data = kwargs['data']
    re = 'search'
    if 're' in kwargs.keys():
      re = kwargs['re']      
    if not ('grammar' in kwargs.keys()):
      raise Exception('In',__file__,' grammar argument should be set in the constructor')
    grammar= kwargs['grammar']     

    self.build(grammar)

    # data structure (list of dicts) explored by the grammar  
    self.lexer.data = data

    # re method 
    # search: stop at first match, return the matched structure or None otherwise
    # findall: find all the matches, return a list of objects embedding the recognized structure and the positions in the data
    self.lexer.re = re

    # list of start/end index of each recognized group 
    # TODO how to handle multiple rules in a single grammar... each rule should have an identifier... and its own groupindex
    self.lexer.groupstartindex = [] # (the first one is the whole match)  
    self.lexer.groupendindex = []  # (the last one is the whole match)  

    # variable used to distinguish the first step (and consequently the start position of the pattern) from the others
    self.lexer.matchongoing = False

    # position in the data from where the grammar (set of rules) is applied 
    # lastGrammarStartPositionInData
    # lastFirstExploredTokenPosition
    # lastFirstExploredDataPosition
    self.lexer.lastFirstExploredDataPosition = 0      

    # position in the data that is explored by the current rule
    # currentExploredDataPosition
    self.lexer.currentExploredDataPosition = self.lexer.lastFirstExploredDataPosition 

    # the whole grammar
    self.lexer.grammar = grammar  

    # the number of global grammar step
    self.lexer.grammarsize = len(grammar.split())

    # the grammar part which is in focus when processing a quantifier ; 
    self.lexer.grammarstep = '' 

    # in the context of local step grammar the step is bare wo quantifier but globally it comes with so 
    self.lexer.globalgrammarstep = grammar.split()[0]

    # position in the grammar which is currently in focus during the parsing
    self.lexer.globalgrammarstepPosition = 0

    # to exchange information between global and local parser when dealing with quantifiers
    # indicate the local parser that it is a local one
    self.lexer.islocal = 0 

    # as a global one, get the result of the local one
    self.lexer.localresult = False # 

    # store the result after parsing the grammar given a certain data (context)
    self.lexer.expressionresult = False # 

#  def __init__(self, debug=False):
#    self.tokens = (
#      self.delimiters + self.operators +
#      self.misc + list(set(self.reserved.values())))
#    self.build(debug=debug)


  def t_error(self, t):
    raise Exception('Illegal character "{t}"'.format(t=t.value[0]))

#  def build(self, debug=False, debuglog=None, **kwargs):
    # """Create a lexer."""
    # if debug and debuglog is None:
    #   debuglog = self.logger
    #   self.lexer = ply.lex.lex(
    #     module=self,
    #     debug=debug,
    #     debuglog=debuglog,
    #     **kwargs)


  def build(self, grammar, **kwargs):
    """Create a lexer."""
    self.lexer = lex.lex(module=self, **kwargs)
    self.lexer.input(grammar)


# example use:
if __name__ == '__main__':
  grammar='?lem:"the" +pos:"JJ" [pos:"NN" & (lem:"car" | !lem:"bike" | !(lem:"bike"))] [raw:"is" | raw:"are"] ;\n'
  #grammar='+pos:"JJ" pos:"NN"'

  myLexer = Lexer(grammar=grammar, data=[], re='search')
  #myLexer.lexer.input(grammar)

  print ("tokenize the given grammar:",grammar)
  while True:
    tok = myLexer.lexer.token()
    if not tok: 
      break      # No more input
    print(tok)