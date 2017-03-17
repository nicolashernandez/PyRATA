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
  startPosition = -1
  endPosition = -1

  def __init__(self, **kwargs):
    if 'start' in kwargs.keys(): # MANDATORY
      self.startPosition = kwargs['start']
    if 'end' in kwargs.keys(): # MANDATORY
      self.endPosition = kwargs['end']
    if 'value' in kwargs.keys(): # MANDATORY
      self.value = kwargs['value']
    if  self.value == '' or self.startPosition == -1 or self.endPosition == -1:   
      raise Exception('pyrata_re - attempt to create a Match object with incomplete informations')

  def __repr__(self):
    return '<pyrata_re Match object; span=('+str(self.start())+', '+str(self.end())+'), match="'+str(self.group())+'">'

  def group(self):
    return self.value

  def start(self):
    return self.startPosition

  def end(self):
    return self.endPosition    

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class MatchesList(object):

  current = 0
  matcheslist = []

  def __init__(self, **kwargs):
    self.matcheslist = []

  def append(self, match):
    self.matcheslist.append(match)

  def group(self,*args):
    if len(self.matcheslist) == 0: 
      return None
    else:  
      if len(args) >0:
        if args[0] <0 and args[0] > len(self.matcheslist):
          raise Exception('Invalid group value out of range')
        return self.matcheslist[args[0]]
    return self.matcheslist[0]

  def start(self, *args):
    return self.group(args).start()

  def end(self):
    return self.group(args).end()

  def __iter__(self):
    return iter(self.matcheslist)

  def next(self): # Python 3: def __next__(self)
    if self.current > len(self.matcheslist):
      raise StopIteration
    else:
      self.current += 1
    return self.matcheslist[self.current - 1]   
    

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

  #print ("Debug: pyrata_re - len(l.lexer.groupstartindex):", len(l.lexer.groupstartindex), "; l.lexer.groupstartindex=",l.lexer.groupstartindex)
  #print ("Debug: pyrata_re - len(l.lexer.groupendindex):", len(l.lexer.groupendindex), "; l.lexer.groupendindex=",l.lexer.groupendindex)

  if len(l.lexer.groupstartindex)>0 and len(l.lexer.groupendindex)>0:
    #print ("Debug: l.lexer.expressionresult:", l.lexer.expressionresult)
    #print ("Debug: l.lexer.groupstartindex[0]:", l.lexer.groupstartindex[0])
    #print ("Debug: l.lexer.groupendindex[0]:", l.lexer.groupendindex[0])
    start = l.lexer.groupstartindex[0]
    end = l.lexer.groupendindex[0]
    match = Match (start=start, end=end, value=data[start:end])
    return match
    
  return None



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
  m = Parser(tokens=l.tokens, **kwargs)
  
  # start the parsing
  m.parser.parse(pattern, l.lexer, tracking=True)
  
  #  print ("Debug: pyrata_re - len(l.lexer.groupstartindex):", len(l.lexer.groupstartindex), "; l.lexer.groupstartindex=",l.lexer.groupstartindex)
  #  print ("Debug: pyrata_re - len(l.lexer.groupendindex):", len(l.lexer.groupendindex), "; l.lexer.groupendindex=",l.lexer.groupendindex)

  # build the structure to return
  if len(l.lexer.groupstartindex)>0 and len(l.lexer.groupendindex)>0:
    for (start, end) in zip(l.lexer.groupstartindex,l.lexer.groupendindex):
      #print ('Debug: len(data):',len(data),'; start:', start,'; end:',end)
      matcheslist.append(data[start:end])
    return matcheslist  
  return None

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
def finditer (pattern, data, **kwargs):
  """
  Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in data. 
  The data is scanned left-to-right, and matches are returned in the order found. 
  #Empty matches are included in the result unless they touch the beginning of another match.
  """
  # list of matched data
  matcheslist = MatchesList()

  # Build the parser and set the re method
  l = Lexer(grammar=pattern, data=data, re='findall')
  m = Parser(tokens=l.tokens, **kwargs)
  
  # start the parsing
  m.parser.parse(pattern, l.lexer, tracking=True)
  
  #  print ("Debug: pyrata_re - len(l.lexer.groupstartindex):", len(l.lexer.groupstartindex), "; l.lexer.groupstartindex=",l.lexer.groupstartindex)
  #  print ("Debug: pyrata_re - len(l.lexer.groupendindex):", len(l.lexer.groupendindex), "; l.lexer.groupendindex=",l.lexer.groupendindex)

  # build the structure to return
  if len(l.lexer.groupstartindex)>0 and len(l.lexer.groupendindex)>0:
    for (start, end) in zip(l.lexer.groupstartindex,l.lexer.groupendindex):
      #print ('Debug: len(data):',len(data),'; start:', start,'; end:',end)
      match = Match (start=start, end=end, value=data[start:end])
      matcheslist.append(match)
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