# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to evaluate the semantic of a given pattern step
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import logging
# logging.info() Report events that occur during normal operation of a program (e.g. for status monitoring or fault investigation)
# logging.debug() for very detailed output for diagnostic purposes
# logging.warning() Issue a warning regarding a particular runtime event

import ply.yacc as yacc
from pyrata.lexer import *

import re


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_current_pattern_step_offsets(p):
  ''' Line Number and Position Tracking'''
  # http://www.dabeaz.com/ply/ply.html#ply_nn33
  left_symbol_start, left_symbol_end = p.lexspan(1)
  if p.lexer.lexpos > len(p.lexer.lexdata):
    previous_lextoken_end = len(p.lexer.lexdata)
  else:
    previous_lextoken_end = p.lexer.lexpos - len(p.lexer.lexTokenEndDict[p.lexer.lexpos].value)
  return left_symbol_start, previous_lextoken_end



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_current_pattern_step(p, start, end):
  ''' surface form of the current parsed step'''
  return p.lexer.lexdata[start:end]



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def log(p, production):
  # Line Number and Position Tracking
  # http://www.dabeaz.com/ply/ply.html#ply_nn33

  step_start, step_end = get_current_pattern_step_offsets(p) 
  step = get_current_pattern_step(p, step_start, step_end)
  logging.info('Production=%s ; step=%s', production, step)
  logging.debug('Whole pattern/lexdata=%s ; len(lexdata)=%s', p.lexer.lexdata, str(len(p.lexer.lexdata)))
  logging.debug('# of lexical tokens in the current production rule=%s', str(len(p)))
#      print ('\t\tProduction={} ; pattern_step=[{}] ; data_token = "{}" ; return="{}"'
#        .format(production, p.lexer.lexdata, p.lexer.data[p.lexer.data_cursor], p[0]))



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class SemanticStepParser(object):

  #self.tokens = self.lex.tokens
  #tokens = ()

  
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
      log(p, '(step->atomicconstraint)')
    
    elif p[1] == '!':
      p[0] = not(p[2])
      log(p, '(step->NOT step)')
    
    else:
      p[0] = p[2]
      log(p, '(step->LBRACKET classconstraint RBRACKET)')

    p.lexer.truth_value = p[0]  


# _______________________________________________________________
  def p_classconstraint(self,p):
    '''classconstraint : classconstraint AND partofclassconstraint
            | classconstraint OR partofclassconstraint 
            | partofclassconstraint '''
    if len(p) == 2:
      p[0] = p[1] 
      log(p, '(classconstraint->partofclassconstraint)')
    #
    else:
      if p[2] == '&':
        p[0] = p[1] and p[3]
        log(p, '(classconstraint->partofclassconstraint AND classconstraint)')

      else: 
        p[0] = p[1] or p[3]
        log(p, '(classconstraint->partofclassconstraint OR classconstraint)')

# _______________________________________________________________
  def p_partofclassconstraint(self,p):
    '''partofclassconstraint : atomicconstraint
                    | LPAREN classconstraint RPAREN  
                    | NOT classconstraint '''
    if p[1] == '(':
      p[0] = p[2]
      log(p, '(partofclassconstraint->LPAREN classconstraint RPAREN)')
    
    elif p[1] == '!':
      p[0] = not(p[2])
      log(p, '(partofclassconstraint->NOT classconstraint)')
    
    else:
      p[0] = p[1]
      log(p, '(partofclassconstraint->atomicconstraint)')

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
      log(p, '(atomicconstraint->NAME=VALUE)') #: ' + attName + ' ' + operator + ' ' + attValue +')')
        
    else:
      p[0] = False
      log(p, '(atomicconstraint->NAME=VALUE)') #: ' + attName + ' ' + operator + ' ' + attValue +')')
        
      logging.warning ('unknown attribute name %s', attName)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING ERROR HANDLING
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def p_error(self,p):
    if not p:
      logging.info('pattern semantically parsed.')
      return

      # http://www.dabeaz.com/ply/ply.html#ply_nn26 6.8.2
      # Read ahead looking for a closing ';'
    logging.warning('semantic parsing error - unexpected token type="{}" with value="{}" at position {}. Search an error before this point.'.format(p.type, p.value, p.lexer.lexpos))

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
  m = Parser(tokens=l.tokens, start='expression')

  # try it out
  print ("Copy the grammar line without 'Grammar: ' (whitespace should not been included); The semi-colon ';' will lead to a parsing error")
  while True:
    try:
      #text2parse
      s = input('cl > ')   # Use raw_input on Python 2
    except EOFError:
      break
    m.parser.parse(s, l.lexer, tracking=True)


