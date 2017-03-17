# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from pyrata_parser import *


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Match(object):

  value = ''
  begin = -1
  end = -1

  def __init__(self, **kwargs):
    if 'begin' in kwargs.keys(): # MANDATORY
      self.begin = kwargs['begin']
    if 'end' in kwargs.keys(): # MANDATORY
      self.end = kwargs['end']
    if 'value' in kwargs.keys(): # MANDATORY
      self.value = kwargs['value']
    if  self.value == '' or self.begin == -1 or self.end == -1:   
      raise Exception('pyrata_re - attempt to create a Match object with incomplete informations')



def search (pattern, data, **kwargs):
  """ Scan through data looking for the first location where the regular expression pattern produces a match, 
      and return a corresponding match object. 
      Return None if no position in the data matches the pattern."""
   # Build the parser and  set the re method
  l = Lexer(grammar=pattern, data=data, re='search')

  #debug = False
  #if 'debug' in kwargs.keys():
  #  debug=kwargs['debug']
  m = Parser(tokens=l.tokens, **kwargs)
  

  # we start the parsing
  m.parser.parse(pattern, l.lexer, tracking=True)
  if len(l.lexer.groupstartindex)>0 and len(l.lexer.groupendindex)>0:
    #print ("Debug: l.lexer.expressionresult:", l.lexer.expressionresult)
    #print ("Debug: l.lexer.groupstartindex[0]:", l.lexer.groupstartindex[0])
    #print ("Debug: l.lexer.groupendindex[0]:", l.lexer.groupendindex[0])
    print ("Debug: pyrata_re - len(l.lexer.groupstartindex):", len(l.lexer.groupstartindex), "; l.lexer.groupstartindex=",l.lexer.groupstartindex)
    print ("Debug: pyrata_re - len(l.lexer.groupendindex):", len(l.lexer.groupendindex), "; l.lexer.groupendindex=",l.lexer.groupendindex)
    return data[l.lexer.groupstartindex[0]:l.lexer.groupendindex[0]]
    
  return None

  
def findall (pattern, data, **kwargs):
  """ Return all non-overlapping matches of pattern in data, as a list of datas. 
      The data is scanned left-to-right, and matches are returned in the order found. 
      #If one or more groups are present in the pattern, return a list of groups; 
      #this will be a list of tuples if the pattern has more than one group. 
      #Empty matches are included in the result unless they touch the beginning of another match.
  """
  # list of matched data
  matcheslist = []

  # Build the parser and set the re method
  l = Lexer(grammar=pattern, data=data, re='findall')
  #debug = False
  #if 'debug' in kwargs.keys():
  #  debug=kwargs['debug']
  m = Parser(tokens=l.tokens, **kwargs)

  
  # we start the parsing
  m.parser.parse(pattern, l.lexer, tracking=True)
  
  print ("Debug: pyrata_re - len(l.lexer.groupstartindex):", len(l.lexer.groupstartindex), "; l.lexer.groupstartindex=",l.lexer.groupstartindex)
  print ("Debug: pyrata_re - len(l.lexer.groupendindex):", len(l.lexer.groupendindex), "; l.lexer.groupendindex=",l.lexer.groupendindex)

  if len(l.lexer.groupstartindex)>0 and len(l.lexer.groupendindex)>0:
    for (start, end) in zip(l.lexer.groupstartindex,l.lexer.groupendindex):
      #print ('Debug: len(data):',len(data),'; start:', start,'; end:',end)
      matcheslist.append(data[start:end])
  return matcheslist

def finditer (pattern, data, **kwargs):
  """Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in data. 
  The data is scanned left-to-right, and matches are returned in the order found. 
  #Empty matches are included in the result unless they touch the beginning of another match.
  """
  return None