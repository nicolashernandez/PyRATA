# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to evaluate the semantic of a given pattern step
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import logging
import ply.yacc as yacc
from pyrata.lexer import *

import re

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class SemanticStepParser(object):

  #self.tokens = self.lex.tokens
  #tokens = ()
  verbosity  = 0 # degree of verbosity
  
  precedence = (
    ('left', 'LBRACKET','RBRACKET'),    
    ('left',  'OR'),
    ('left', 'AND'),
    ('left', 'LPAREN','RPAREN'),
    ('right', 'NOT'),
    ('left', 'EQ'),
#  ('right', 'OPTION', 'ANY', 'ATLEASTONE')
  )


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING METHODS
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# _______________________________________________________________
  def p_step(self,p):
    '''step : atomicconstraint
            | NOT step
            | LBRACKET classconstraint RBRACKET ''' 
    if len(p) == 2:
      p[0] = p[1]
      self.log(p, '(step->atomicconstraint)')
    
    elif p[1] == '!':
      p[0] = not(p[2])
      self.log(p, '(step->NOT step)')
    
    else:
      p[0] = p[2]
      self.log(p, '(step->LBRACKET classconstraint RBRACKET)')

    p.lexer.truth_value = p[0]  


# _______________________________________________________________
  def p_classconstraint(self,p):
    '''classconstraint : classconstraint AND partofclassconstraint
            | classconstraint OR partofclassconstraint 
            | partofclassconstraint '''
    if len(p) == 2:
      p[0] = p[1] 
      self.log(p, '(classconstraint->partofclassconstraint)')
    #
    else:
      if p[2] == '&':
        p[0] = p[1] and p[3]
        self.log(p, '(classconstraint->partofclassconstraint AND classconstraint)')

      else: 
        p[0] = p[1] or p[3]
        self.log(p, '(classconstraint->partofclassconstraint OR classconstraint)')

# _______________________________________________________________
  def p_partofclassconstraint(self,p):
    '''partofclassconstraint : atomicconstraint
                    | LPAREN classconstraint RPAREN  
                    | NOT classconstraint '''
    if p[1] == '(':
      p[0] = p[2]
      self.log(p, '(partofclassconstraint->LPAREN classconstraint RPAREN)')
    
    elif p[1] == '!':
      p[0] = not(p[2])
      self.log(p, '(partofclassconstraint->NOT classconstraint)')
    
    else:
      p[0] = p[1]
      self.log(p, '(partofclassconstraint->atomicconstraint)')

# _______________________________________________________________
  def p_atomicconstraint(self,p):
    '''atomicconstraint : NAME EQ VALUE 
                          | NAME MATCH VALUE
                          | NAME IN VALUE'''
    attName = p[1]
    operator = p[2]
    attValue = p[3][1:-1]


    if attName in p.lexer.data[p.lexer.data_cursor]:
      # checking if the given value is equal to the current dict feature of the data
      if operator == '=':
        p[0] = (p.lexer.data[p.lexer.data_cursor][attName] == attValue)
      # checking if the given value, interpreted as regex, matches the current dict feature of the data 
      elif operator == '~':
        p[0] = (re.search(attValue,p.lexer.data[p.lexer.data_cursor][attName]) != None)
        # checking if the current dict feature of the data belongs to a list having the name of the given value
      elif operator == '@':
        # check if the named list is kwown
        if attValue in p.lexer.lexicons:
          p[0] =  (p.lexer.data[p.lexer.data_cursor][attName] in p.lexer.lexicons[attValue])
        else:
          p[0] = False  
      elif operator == '-':
        # TODO 
        logging.warn('operator CHUNK not implemented yet. Manually replace `ch-"NN"` by `(ch="B-NN" ch="I-NN"*)` ')
      # should not enter here, because it would mean that the parser encountered an unknown operator    
      else:
        p[0] = False
      self.log(p, '(atomicconstraint->NAME=VALUE)') #: ' + attName + ' ' + operator + ' ' + attValue +')')
        
    else:
      p[0] = False
      self.log(p, '(atomicconstraint->NAME=VALUE)') #: ' + attName + ' ' + operator + ' ' + attValue +')')
        
      if self.verbosity >0: 
        print ('Warning: unknown attribute name:', attName)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


  def log(self, p, production):
    if self.verbosity >2:
      #print (2*'  ','- - - - - - - - - - - - - - - - - - - - - - - -')
      print ('\t\tProduction={} ; pattern_step=[{}] ; data_token = "{}" ; return="{}"'
        .format(production, p.lexer.lexdata, p.lexer.data[p.lexer.data_cursor], p[0]))




# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING ERROR HANDLING
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def p_error(self,p):
    if not p:
      if self.verbosity >2: 
        print('\t\tInfo: pattern semantically parsed.')
      return

      # http://www.dabeaz.com/ply/ply.html#ply_nn26 6.8.2
      # Read ahead looking for a closing ';'
    if self.verbosity >0: 
      print ('Error: semantic parsing error - unexpected token type="{}" with value="{}" at position {}. Search an error before this point.'.format(p.type, p.value, p.lexer.lexpos))
    while True:
      tok = self.parser.token()             # Get the next token
      if not tok: 
        break
    self.parser.restart()


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  CONSTRUCTOR
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#  def __init__(self, tokens, *argv):
  def __init__(self, **kwargs):
    if 'tokens' in kwargs.keys(): # MANDATORY
      self.tokens = kwargs['tokens']
    kwargs.pop('tokens', None)

    self.verbosity  = 0
    if 'verbosity' in kwargs.keys(): 
      self.verbosity  = kwargs['verbosity']
      kwargs.pop('verbosity', None)

    
    #print ('Debug: len(argv):',len(argv),'; argv:',*argv)
    #if len(argv) > 0:
    #  self.debug = argv[0]
    self.build(**kwargs)

  # Build the parser
  def build(self, **kwargs):
    """ the start attribute is mandatory !
        When calling the method with a start distinct from expression you may get the following message
        WARNING: Symbol 'expression' is unreachable
        Nothing to be aware of
    """


    # start the parser
    start='step'
    if 'start' in kwargs.keys(): # MANDATORY
      start = kwargs['start'] 
    kwargs.pop('start', None)      
    # debugging and logging http://www.dabeaz.com/ply/ply.html#ply_nn44 
    self.parser = yacc.yacc(module=self,  start=start, errorlog=yacc.NullLogger(), **kwargs) #

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  MAIN
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# example use:
if __name__ == '__main__':
  pattern='?lem:"the" +pos:"JJ" [pos:"NN" & (lem:"car" | !lem:"bike" | !(lem:"bike"))] [raw:"is" | raw:"are"]'
  print ('Pattern:', pattern)

  data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'blue', 'lem':'blue', 'pos':'JJ'}]     
  data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
  print ('Data:', data)

  #pattern = 'pos:"NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}]

  # Build the parser and 
  l = Lexer(pattern=pattern, data=data) 
  m = Parser(tokens=l.tokens, verbosity =2, start='expression')

  # try it out
  print ("Copy the grammar line without 'Grammar: ' (whitespace should not been included); The semi-colon ';' will lead to a parsing error")
  while True:
    try:
      #text2parse
      s = input('cl > ')   # Use raw_input on Python 2
    except EOFError:
      break
    m.parser.parse(s, l.lexer, tracking=True)


