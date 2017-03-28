# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to evaluate the semantic of a given pattern step
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ply.yacc as yacc
from pyrata.lexer import *
from pyrata.semantic_step_parser import *


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
      raise Exception('pyrata.re - attempt to create a Match object with incomplete informations')

  def __repr__(self):
    return '<pyrata.re Match object; span=('+str(self.start())+', '+str(self.end())+'), match="'+str(self.group())+'">'

  def group(self):
    return self.value

  def start(self):
    return self.startPosition

  def end(self):
    return self.endPosition

  def __eq__(self, other):
    if other == None: 
      return False
    if self.value == other.value and self.startPosition == other.startPosition and self.endPosition == other.endPosition:
      return True
    return False  
   
  def __ne__(self, other):
    if other == None: 
      return True   
    if self.value == other.value and self.startPosition == other.startPosition and self.endPosition == other.endPosition:
      return False
    return True  

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class MatchesList(object):

  current = 0
  matcheslist = []

  def __init__(self, **kwargs):
    self.matcheslist = []

  def append(self, match):
    self.matcheslist.append(match)

  def group(self, *args):
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

  def __len__(self):
    return len(self.matcheslist)

  def __repr__(self):
    ml = ''
    for m in self.matcheslist:
      ml = ml + '<pyrata.re Match object; span=('+str(m.start())+', '+str(m.end())+'), match="'+str(m.group())+'">\n'
    return ml

  def __eq__(self, other):
    matches = 0
    for s, o in zip(self.matcheslist, other.matcheslist):
      if s == o: matches += 1
    if matches == len(self.matcheslist): 
      return True
    return False  

  def __ne__(self, other):
    matches = 0
    for s, o in zip(self.matcheslist, other.matcheslist):
      if s == o: matches += 1
    if matches == len(self.matcheslist): 
      return False
    return True 



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def evaluate (lexer, pattern_step, data_token, **kwargs):
  '''
  Return a truth value which is True if the pattern_step recognizes the data_token
  '''
  verbosity = 0
  if 'verbosity' in kwargs.keys():
    verbosity = kwargs['verbosity']
  if verbosity >2:
    print (2*'  ','_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
    print (2*'  ','Info: evaluation...')

  lexer.lexer.data = [data_token]
  lexer.lexer.data_cursor = 0
  lexer.lexer.pattern_cursor = 0
  e = SemanticStepParser(tokens=lexer.tokens, **kwargs)
  e.parser.parse(pattern_step, lexer.lexer) # removed tracking=True
  if verbosity >2: 
    print (2*'  ','_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')

  return lexer.lexer.truth_value 




# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def parse_semantic (compiledPattern, data, **kwargs): 
  '''
  Parse a compiled pattern and depending on the re method return the recognized pattern over the data 
  '''
  verbosity = 0
  if 'verbosity' in kwargs.keys():
    verbosity = kwargs['verbosity']

  if verbosity >1:
    print (1*'  ','________________________________________________')      
    print (1*'  ','Info: semantic parsing...')  

  l = compiledPattern.getLexer()
  pattern_data_start = 0
  data_cursor = 0
  pattern_cursor = 0
  pattern_steps = l.lexer.pattern_steps

  match_on_going = False    # a pattern is being recognized

  group_start_index = []    # the start positions of each recognized group 
  group_end_index = []      # the end positions of each recognized group 

  matcheslist = MatchesList()         # list of matched data

  # # while there is sufficient data to recognize a pattern (! warning some pattern token are ? )
    # len (p.lexer.pattern_steps) minus # ?|*
  while data_cursor < len(data):
    quantifier, step = pattern_steps[pattern_cursor]
    # data_token = data[data_cursor]
    if verbosity >1:
      print (1*'  ','------------------------------------------------')
      print (1*'  ','pattern_cursor="{}" quantifier="{}" pattern_step=[{}] data_cursor="{}" data_token="{}" '
        .format(pattern_cursor, quantifier, step, data_cursor, data[data_cursor]))        

    # step without quantifier
    if quantifier == None:
      if evaluate (l, step, data[data_cursor], **kwargs):
        if verbosity >1: print (1*'  ',"match pattern_step")        
        # first pattern step matched
        if not(match_on_going):
          if verbosity >1: print (1*'  ',"start recognition and store the data_cursor as a start position")
          group_start_index.append(data_cursor)
          match_on_going = True
        pattern_cursor += 1
      else:
        # abort recognition
        if verbosity >1: print (1*'  ',"unmatch pattern_step")
        if match_on_going:
          if verbosity >1: print (1*'  ',"abort recognition")
          group_start_index.pop()
        match_on_going = False
        pattern_data_start = pattern_data_start+1
        pattern_cursor = 0
      data_cursor += 1  

    # optional step
    elif quantifier == '?':
      if evaluate (l, step, data[data_cursor], **kwargs):
        if verbosity >1: print (1*'  ',"match optional pattern_step")
        # first pattern step matched
        if not(match_on_going):
          if verbosity >1: print (1*'  ',"start recognition and store the data_cursor as a start position")
          match_on_going = True
          group_start_index.append(data_cursor)   
        data_cursor += 1  
      else:
        if verbosity >1: print (1*'  ',"unmatch optional pattern_step")
      pattern_cursor += 1 

    elif quantifier == '*':
      any_iter  = 0
      if verbosity >1: print (1*'  ',"evaluate any pattern_step")
      while evaluate (l, step, data[data_cursor], **kwargs):
        if verbosity >1: print (1*'  ','in any pattern_step "{}" iteration, match_on_going="{}", data_cursor="{}", data_token="{}"'
          .format(any_iter, match_on_going, data_cursor, data[data_cursor]))
        if any_iter == 0:
          # first pattern step matched
          if not(match_on_going):
            if verbosity >1: print (1*'  ',"start recognition and store the data_cursor as a start position")
            match_on_going = True
            group_start_index.append(data_cursor)   
        data_cursor += 1 
        any_iter += 1
        # case where a complex pattern has one first part being recognized while the data ends
        if data_cursor >= len(data):
          break

      if verbosity >1: print (1*'  ','after any pattern_step evaluation : "{}" iteration, match_on_going="{}", data_cursor="{}", data_token="{}"'
          .format(any_iter, match_on_going, data_cursor, data[data_cursor] if data_cursor < len(data) else 'no-more'))

      pattern_cursor += 1 

      if any_iter > 0:
        if verbosity >1: print (1*'  ',"some data_token have been recognized")
        # case where *[ab]b
        if pattern_cursor < len(pattern_steps) :
          next_quantifier, next_step = pattern_steps[pattern_cursor]
          if verbosity >1: print (1*'  ','checking the *[ab]b case: any_iter="{}", pattern_cursor="{}", next_step="{}", data_cursor="{}", data[data_cursor-1]="{}"'
            .format(any_iter, pattern_cursor, next_step, data_cursor, data[data_cursor - 1]))
          if any_iter > 0 and evaluate (l, next_step, data[data_cursor - 1], **kwargs):
            if verbosity >1: print (1*'  ','modify the cursor to face the case of *[ab]b')
            data_cursor -= 1

    elif quantifier == '+':
      if verbosity >1: print (1*'  ',"evaluate at_least_one pattern_step")
      any_iter  = 0
      while evaluate (l, step, data[data_cursor], **kwargs):
        if verbosity >1: print (1*'  ','in at_least_one pattern_step "{}" iteration, match_on_going="{}", data_cursor="{}", data_token="{}"'
            .format(any_iter, match_on_going, data_cursor, data[data_cursor]))
        if any_iter == 0:
          # first pattern step matched
          if not(match_on_going):
            if verbosity >1: print (1*'  ',"start recognition and store the data_cursor as a start position")
            match_on_going = True
            group_start_index.append(data_cursor)    
        data_cursor += 1 
        any_iter += 1
        # case where a complex pattern has one first part being recognized while the data ends
        if data_cursor >= len(data):
          break

      if verbosity >1: print (1*'  ','after at_least_one pattern_step evaluation : "{}" iteration, match_on_going="{}", data_cursor="{}", data_token="{}"'
          .format(any_iter, match_on_going, data_cursor, data[data_cursor] if data_cursor < len(data) else 'no-more'))

      if any_iter > 0: 
        pattern_cursor += 1 
        if verbosity >1: print (1*'  ',"some data_token have been recognized")
        # case where +[b]b to recognize bbb
        if any_iter > 1 and pattern_cursor < len(pattern_steps) : 
        # at least 2 iterations are required, since it is '+', we cannot modify the first one
          next_quantifier, next_step = pattern_steps[pattern_cursor]
          if any_iter > 0 and evaluate (l, next_step, data[data_cursor - 1], **kwargs):
            if verbosity >1: print (1*'  ','modify the cursors to face the case of *[ab]b')
            data_cursor -= 1
      else:
        # abort recognition
        if verbosity >1: print (1*'  ',"no data_token has been recognized")
        if match_on_going:
          if verbosity >1: print (1*'  ',"abort recognition")
          group_start_index.pop()
        match_on_going = False
        pattern_data_start = pattern_data_start+1
        pattern_cursor = 0
        data_cursor += 1  

#   # a pattern has been recognized
    #if verbosity >2: 
    #  print (2*'  ','pattern_cursor="{}" quantifier="{}" pattern_step=[{}] len(pattern_steps)="{}" data_cursor="{}" data_token="{}" match_on_going="{}"'.format(pattern_cursor, quantifier, step, len(pattern_steps), data_cursor, data_token, match_on_going))        
    if pattern_cursor >= len(pattern_steps):
      if match_on_going:
        if verbosity >1: print (1*'  ',"recognize a whole pattern ; store the data_cursor as a end position")
        group_end_index.append(data_cursor)
        if verbosity >3: 
          print (3*'  ',"Debug: group_start_index=", group_start_index)
          print (3*'  ',"Debug: group_end_index=", group_end_index) 
        start = group_start_index[len(group_start_index)-1]
        end = group_end_index[len(group_start_index)-1]

        match = Match (start=start, end=end, value=data[start:end])
        matcheslist.append(match)
        if l.lexer.re in ['search', 'match']:  
          break
      else:
        # we are in the case of a pattern made of a single optional step which was not recognized
        # we have to step forward otherwise we fall in an infinite loop
        if verbosity >1: print (1*'  ','case of a pattern made of a single optional step which was not recognized, we move forward data_cursor')
        data_cursor += 1
         
      pattern_data_start = data_cursor
      pattern_cursor = 0
      match_on_going = False
    else: 
      if verbosity >1: print (1*'  ','some pattern recognition may be on going but none full form has been recognized after processing this pattern_step')
        

  return matcheslist