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
    'NAME', 'VALUE', 'EQ',
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
  t_EQ  = r'='
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

    # position in the data from where the grammar (set of rules) is applied 
    # lastGrammarStartPositionInData
    # lastFirstExploredTokenPosition
    # lastFirstExploredDataPosition
    self.lexer.lastFirstExploredDataPosition = 0      

    # position in the data that is explored by the current rule
    # currentExploredDataPosition
    self.lexer.currentExploredDataPosition = self.lexer.lastFirstExploredDataPosition 

    # the whole grammar
    # redundant with lexer.lexdata
    self.lexer.grammar = grammar  


    # list of LexToken (self.type, self.value, self.lineno, self.lexpos)
    self.lexTokenList = [] 

    # map endposition to lextoken (by getting the len(.value of the element), 
    # you can then get the endposition of the previous element, useful to delimit quantified steps 
    # indeed, p.lexer.lexpos attribute is an integer that contains the current position within the input text.
    # Within token rule functions, this points to the first character after the matched text 
    # and the matched text includes the next lextToken (not only reduced to a single char).
    self.lexTokenEndDict = {} 


    # the number of global grammar step
    # TODO Fix since step made of class with multiple constraints will be wrongly split
    # len(grammar.split()) 
    self.lexer.grammarsize = None 

    # the grammar part which is in focus when processing a quantifier ; 
    self.lexer.localstep = '' 

    # in the context of local step grammar the step is bare wo quantifier but globally it comes with so 
    # (log use case) 
    # TODO Fix since step made of class with multiple constraints will be wrongly split   
    #grammar.split()[0]
    # patternstep
    self.lexer.patternStep = None

    # cursor to follow the parsing progress in the grammar (log use case) 
    self.lexer.patternStepPosition = 0

    # to exchange information between global and local parser when dealing with quantifiers
    # indicate the local parser that it is a local one
    self.lexer.islocal = 0 

    # as a global one, get the result of the local one
    self.lexer.localresult = False # 

    # store the result after parsing the grammar given a certain data (context)
    self.lexer.expressionresult = False # 

    #self.lexer.is

#  def __init__(self, debug=False):
#    self.tokens = (
#      self.delimiters + self.operators +
#      self.misc + list(set(self.reserved.values())))
#    self.build(debug=debug)


  def t_error(self, t):
    raise Exception('Illegal character "{t}"'.format(t=t.value[0]))


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


  def build(self, grammar, **kwargs):
    """Create a lexer."""
    self.lexer = lex.lex(module=self, **kwargs)
    self.lexer.input(grammar)
    self.storeLexTokenList()


# example use:
if __name__ == '__main__':
  grammar='?lem:"the" +pos:"JJ" [pos:"NN" & (lem:"car" | !lem:"bike" | !(lem:"bike"))] [raw:"is" | raw:"are"] ;\n'
  #grammar='+pos:"JJ" pos:"NN"'
  grammar = 'pos:"DT" +[pos:"JJ" & !pos:"EX"]  pos:"NN"'
  
  # 
  myLexer = Lexer(grammar=grammar, data=[], re='search')
  #myLexer.lexer.input(grammar)

  # 



  print ("tokenize the given grammar:",grammar)
  while True:
    tok = myLexer.lexer.token()
    if not tok: 
      break      # No more input
    print(tok)