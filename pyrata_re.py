# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from pyrata_parser import *

def search (pattern, data, **kwargs):
  """ Scan through data looking for the first location where the regular expression pattern produces a match, 
      and return a corresponding match object. 
      Return None if no position in the data matches the pattern."""
   # Build the parser and 
  l = Lexer(grammar=pattern, data=data)
  #debug = False
  #if 'debug' in kwargs.keys():
  #  debug=kwargs['debug']
  m = Parser(tokens=l.tokens, **kwargs)
  
  m.parser.parse(pattern, l.lexer, tracking=True)
  if len(l.lexer.groupstartindex)>0 and len(l.lexer.groupendindex)>0:
    #print ("Debug: l.lexer.expressionresult:", l.lexer.expressionresult)
    #print ("Debug: l.lexer.groupstartindex[0]:", l.lexer.groupstartindex[0])
    #print ("Debug: l.lexer.groupendindex[0]:", l.lexer.groupendindex[0])
    return data[l.lexer.groupstartindex[0]:l.lexer.groupendindex[0]]
    
  return None