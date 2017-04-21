# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to evaluate the semantic of a given pattern step
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import logging
from pprint import pprint, pformat
import ply.yacc as yacc

from pyrata.lexer import *
from pyrata.semantic_step_parser import *
import pyrata.compiled_pattern_re


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Match(object):

  _groups = []          # list of triplet (value, start, end) e.g. [[[{'pos': 'JJ', 'raw': 'fast'}], 0, 1]]
  DEFAULT_GROUP_ID = 0
  (VALUE, START, END) = (0,1,2)

  def __init__(self, **kwargs):
    self._groups = []
    value = ''
    start = -1
    end = -1
    if 'start' in kwargs.keys(): # MANDATORY
      start = kwargs['start']
    if 'end' in kwargs.keys(): # MANDATORY
      end = kwargs['end']
    if 'value' in kwargs.keys(): # MANDATORY
      value = kwargs['value']
    if 'groups' in kwargs.keys(): # MANDATORY
      self._groups = kwargs['groups']  
      #logging.debug ('groups=', self._groups)
      #print ('Debug: Match__init__:(start={}, end={}, value={})'.format(startPosition, endPosition, value))
    else:  
      self._groups.append([value, start, end])
    #if  self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] == '' or self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] == -1 or self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END] == -1:   
    #  raise Exception('pyrata.re - attempt to create a Match object with incomplete informations')
    #print ('Debug: groups=', self.groups)

  def __repr__(self):
    #for v, s, e in self.groups
    return '<pyrata.re Match object; groups='+str(self._groups)+'>' #span=('+str(self.start())+', '+str(self.end())+'), match="'+str(self.group())+'">'

  def get_group_id(self, *argv):
    if len(argv) > 0:
      group_id = argv[0]
      if group_id > len(self._groups):
        raise IndexError ('In Match - group() function - wrong index required')
    else:
      group_id = Match.DEFAULT_GROUP_ID
    return group_id

  def group(self, *argv):
    ''' 
    Returns the corresponding value of one subgroup of the match. 
    Default is 0. The whole match value.
    '''
    return self._groups[self.get_group_id(*argv)][Match.VALUE]

  def groups (self):
    '''Return a tuple containing all the subgroups of the match, from 0. 
    In python re it is from 1 up to however many groups are in the pattern. '''
    return self._groups
    # if len(self.groups) > 0:
    #   return self.groups[1:len(self.groups)]   
    # else:
    #   return [] 

  def start(self, *argv):
    '''
    Return the indices of the start of the subdata matched by group; 
    group default to zero (meaning the whole matched data).
    '''
    return self._groups[self.get_group_id(*argv)][Match.START]

  def end(self, *argv):
    '''
    Return the indices of the end of the subdata matched by group; 
    group default to zero (meaning the whole matched data).
    '''
    return self._groups[self.get_group_id(*argv)][Match.END]

  def setStart(self, start, *argv):
    '''
    Set the indice of the start of the subdata matched by group; 
    group default to zero (meaning the whole matched data).
    '''
    self._groups[self.get_group_id(*argv)][Match.START] = start

  def setEnd(self, end, *argv):
    '''
    Set the indice of the end of the subdata matched by group; 
    group default to zero (meaning the whole matched data).
    '''
    self._groups[self.get_group_id(*argv)][Match.END] = end
       

  def __eq__(self, other):
    if other == None: 
      return False
    if self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] == other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] and self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] == other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] and self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END] == other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END]:
      return True
      return True
    return False  
   
  def __ne__(self, other):
    return not (self == other)
    # if other == None: 
    #   return True   
    # if self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] != other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.VALUE] or self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] != other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.START] or self._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END] != other._groups[self.get_group_id(Match.DEFAULT_GROUP_ID)][Match.END]:
    #   return True
    # return False  

  def __len__(self):
    #logging.debug  ('groups=', self.groups)
    return len(self._groups) 

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class MatchesList(object):

  current = -1
  matcheslist = []

  def __init__(self, **kwargs):
    self.matcheslist = []

  def append(self, match):
    self.matcheslist.append(match)
    #logging.debug ('matcheslist=',self.matcheslist)

  def extend(self, another_matcheslist):
    self.matcheslist.extend(another_matcheslist)  

  def delete(self, index):
    del self.matcheslist[index]


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
    return self.group(*args).start()

  def end(self, *args):
    return self.group(*args).end()

  def __iter__(self):
    return iter(self.matcheslist)

  def next(self): # Python 3: def __next__(self)
    if self.current > len(self.matcheslist):
      raise StopIteration
    else:
      self.current += 1
    return self.matcheslist[self.current]   

  def __len__(self):
    return len(self.matcheslist)

  # def __repr__(self):
  #   ml = ''
  #   for m in self.matcheslist:
  #     ml = ml + '<pyrata.re Match object; span=({}, {}), match="{}">\n'.format(str(m.start()), str(m.end()), str(m.group()))
  #   return ml

  def __eq__(self, other):
    if other == None: 
      return False       
    matches = 0
    for s, o in zip(self.matcheslist, other.matcheslist):
      if s == o: matches += 1
    if matches == len(self.matcheslist): 
      return True
    return False  

  def __ne__(self, other):
    if other == None: 
      return True       
    matches = 0
    for s, o in zip(self.matcheslist, other.matcheslist):
      if s == o: matches += 1
    if matches == len(self.matcheslist): 
      return False
    return True 

  def __repr__(self):
    return '<pyrata.re MatchesList object; matcheslist="'+str(self.matcheslist)+'">'


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def evaluate (lexer, pattern_steps, pattern_cursor, data, data_cursor, **kwargs):
  '''
  Return a truth value which is True if the pattern_step recognizes the data_token
  '''

  quantifier, pattern_step = pattern_steps[pattern_cursor]

  verbosity = 0
  if 'verbosity' in kwargs.keys():
    verbosity = kwargs['verbosity']

  data_cursor_extension  = 1
  group_id = 0
  r = None

  if not(isinstance(pattern_step, list)): 
    logging.info ('Evaluation starting... of a pattern step SIMPLE GROUP=%s', pattern_step)

    lexer.lexer.data = [data[data_cursor]]
    lexer.lexer.data_cursor = 0
    lexer.lexer.pattern_cursor = 0
    e = SemanticStepParser(tokens=lexer.tokens, **kwargs)
    e.parser.parse(pattern_step, lexer.lexer) # removed tracking=True

    logging.info ('Evaluation ending... of a pattern step SIMPLE GROUP ; return r={}'.format(r))

  else:
    logging.info ('Evaluation starting... of a pattern step COMPLEX GROUPS=%s',pformat(pattern_steps))

    #print ('Debug: lexer.group_pattern_offsets_group_list=',lexer.lexer.group_pattern_offsets_group_list)
    #local_l = lexer l # defines a new reference
    local_l = Lexer(pattern="", lexicons=lexer.lexer.lexicons)
    #print ('Debug: lexer.group_pattern_offsets_group_list=',lexer.lexer.group_pattern_offsets_group_list)
    #print ('Debug: local_l.group_pattern_offsets_group_list=',local_l.lexer.group_pattern_offsets_group_list)
    

    r = MatchesList()
    # while no match with a group and there is still at least a group to test
    #   add the must start constraint 
    #   then check
    while len(r) == 0 and group_id < len (pattern_step):
      logging.info ('Evaluation starting... of group[{}]={}'.format(group_id, pattern_step[group_id]))

      local_l.lexTokenEndDict = lexer.lexTokenEndDict

      local_l.lexTokenList = lexer.lexTokenList  # list of LexToken (self.type, self.value, self.lineno, self.lexpos)

      local_l.lexer.data = data 
      #local_l.lexer.pattern_data_start = 0      # position in the data from where the pattern is applied 
      #local_l.lexer.pattern_cursor = 0          # cursor to follow the parsing progress in the pattern
      local_l.lexer.pattern_steps = pattern_step[group_id]         # compiled pattern: list of (quantifier=[None, '*', '+', '?'] not=[True, False] group=[True, False], step or group)
      local_l.lexer.pattern_must_match_data_start = True  # ^ matches the start of data before the first token in a data.
      #local_l.lexer.pattern_must_match_data_end = False    # $ matches the end of data ~after the last token of data.
      local_l.lexer.data_cursor = local_l.lexer.pattern_data_start     # position in the data that is explored by the current pattern
      #local_l.lexer.truth_value = False  # parsing result of a given pattern over a certain data 
      #local_l.lexer.quantified_step_index = 0     # syntactic pattern : parser quantified step index 
      #local_l.lexer.quantified_step_start = {}    # syntactic pattern parser : at a given position returns the quantified step index
      #local_l.lexer.quantified_step_end = {}      # syntactic pattern parser : at a given position returns the quantified step index
      #local_l.lexer.last_group_offsets_candidate = []     # last couple of index position of the current group
      local_l.lexer.group_pattern_offsets_group_list = [[0, len(pattern_step[group_id])]]    # list of group offsets e.g. [[start_i, end_i], [start_j, end_j], [start_k, end_k]]
      #local_l.lexer.step_already_counted = 0 # to prevent from duplicate step counting (wo then wi parenthesis) 
      #local_l.lexer.step_group_class = []    # step_group_class list of alternatives
      #print ('Debug: l.lexer.group_pattern_offsets_group_list=',local_l.lexer.group_pattern_offsets_group_list)
      local_cp = pyrata.compiled_pattern_re.CompiledPattern(lexer=local_l, **kwargs)
      #print ('Debug: lexer.group_pattern_offsets_group_list=',lexer.lexer.group_pattern_offsets_group_list)
      #print ('Debug: local_l.group_pattern_offsets_group_list=',local_l.lexer.group_pattern_offsets_group_list)

      r = pyrata.semantic_pattern_parser.parse_semantic (local_cp, data[data_cursor:], **kwargs)
      #print ('Debug: current pattern_steps={} i={} len (list of pattern_steps)={} '.format(local_l.lexer.pattern_steps, i, len (pattern_step)))

      group_id += 1

    if len(r) != 0:
      #len(pattern_step[i])
      # add a group 
      #len(r) FIXME indicate somehow the new data_cursor
      lexer.lexer.truth_value = True
      data_cursor_extension += len(r.group(0).group(0)) -1
      # modify the lexer
      #print ('Debug: lexer.group_pattern_offsets_group_list=',lexer.lexer.group_pattern_offsets_group_list)
      #print ('Debug: local_l.group_pattern_offsets_group_list=',local_l.lexer.group_pattern_offsets_group_list)
      #print ('Debug: r={}'.format(r))
      #print ('Debug: r[0][0]={}'.format(r.group(0).group(0)))
      #print ('Debug: data_cursor_extension=',data_cursor_extension)
      for m in r:
        for g_id in range(len(m._groups)):
          #logging.debug ('Debug: g=',m._groups[g_id])
          m.setStart(m.start(g_id) + data_cursor, g_id)
          m.setEnd(m.end(g_id) + data_cursor, g_id)
          logging.debug ('update m={} from=[{}, {}] to [{}, {}]'.format(m.group(g_id), m.start(g_id), m.end(g_id), m.start(g_id)+ data_cursor, m.end(g_id) + data_cursor))
 #       m.setStart(m.start() + data_cursor)
 #       m.setEnd(m.end() + data_cursor)
        #print ('Debug: after update m={}'.format(m))
    else:
      lexer.lexer.truth_value = False

    logging.info ('Evaluation ending... of a pattern step COMPLEX GROUPS ; return r={}'.format(r))

  return lexer.lexer.truth_value, data_cursor_extension, len(pattern_step[group_id-1]), r 




# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def parse_semantic (compiledPattern, data, **kwargs): 
  '''
  Parse a compiled pattern and depending on the re method return the recognized pattern over the data 
  '''
  verbosity = 0
  if 'verbosity' in kwargs.keys():
    verbosity = kwargs['verbosity']

 

  l = compiledPattern.getLexer()
  pattern_data_start = 0
  data_cursor = 0
  pattern_cursor = 0
  pattern_steps = l.lexer.pattern_steps

  logging.info ('Starting semantic parsing of pattern_steps=%s', pattern_steps) 

  group_pattern_offsets_group_list = l.lexer.group_pattern_offsets_group_list

  match_on_going = False    # a pattern is being recognized

  matcheslist = MatchesList()         # list of matched data
  temporary_matcheslist = MatchesList()         # list of matched data

  pattern_cursor_to_data_cursor = {} 

  # # while there is sufficient data to recognize a pattern (! warning some pattern token are ? )
    # len (p.lexer.pattern_steps) minus # ?|*
  while data_cursor < len(data):
    quantifier, step = pattern_steps[pattern_cursor]

    logging.info ('Exploring data[{}]="{}"  with pattern_steps[{}]="{}" and quantifier="{}"'
        .format(data_cursor, data[data_cursor], pattern_cursor, step, quantifier))        
    initial_data_cursor = data_cursor
    initial_data = data[data_cursor]
    initial_pattern_cursor = pattern_cursor
    initial_step = step 
    initial_quantifier = quantifier

    # step without quantifier
    if quantifier == None:
      logging.info ('Evaluating NONE_QUANTIFIER pattern_step')
      step_evaluation, data_cursor_extension, pattern_cursor_extension, matcheslist_extension = evaluate (l, pattern_steps, pattern_cursor, data, data_cursor, **kwargs)
      if step_evaluation:
        logging.info ('Evaluation result: MATCH ')        
        # first pattern step matched
        if not(match_on_going):
          logging.debug ('start a new recognition')
          match_on_going = True
        if matcheslist_extension != None:
          logging.debug ('extend temporary_matcheslist with=%s',matcheslist_extension)  
          temporary_matcheslist.extend(matcheslist_extension)
          logging.debug ('temporary_matcheslist after extension=%s',temporary_matcheslist)  
        else:
          logging.debug ('no extension since matcheslist_extension=%s',matcheslist_extension)  

        pattern_cursor_to_data_cursor[pattern_cursor] = data_cursor  
        pattern_cursor += 1
      else:
        # abort recognition
        logging.info ('Evaluation result: UNMATCH')
        if match_on_going:
          logging.debug ('abort recognition')
        match_on_going = False
        pattern_data_start = pattern_data_start+1
        pattern_cursor = 0
        pattern_cursor_to_data_cursor = {}
        temporary_matcheslist = MatchesList()
        if l.lexer.pattern_must_match_data_start:
          break

      data_cursor += data_cursor_extension  

    # optional step
    elif quantifier == '?':
      pattern_cursor_to_data_cursor[pattern_cursor] = data_cursor   
      logging.info ('Evaluating OPTION pattern_step')
      step_evaluation, data_cursor_extension, pattern_cursor_extension, matcheslist_extension = evaluate (l, pattern_steps, pattern_cursor, data, data_cursor, **kwargs)
      if step_evaluation:
        logging.info ('Evaluation OPTION result: MATCH ')
        # first pattern step matched
        if not(match_on_going):
          logging.debug ('start a new recognition')
          match_on_going = True
        #pattern_cursor_to_data_cursor[pattern_cursor] = data_cursor
        if matcheslist_extension != None:
          logging.debug ('extension of temporary_matcheslist with=%s',matcheslist_extension)  
          temporary_matcheslist.extend(matcheslist_extension)
          logging.debug ('temporary_matcheslist after extension=%s',temporary_matcheslist)         
        data_cursor += data_cursor_extension  
      else:
        logging.info ('Evaluation OPTION result: UNMATCH')
      pattern_cursor += 1 

    elif quantifier == '*':
      any_iter  = 0
      pattern_cursor_to_data_cursor[pattern_cursor] = data_cursor   
      logging.info ('Evaluating ANY pattern_step')
      step_evaluation = step_evaluation, data_cursor_extension, pattern_cursor_extension, matcheslist_extension = evaluate (l, pattern_steps, pattern_cursor, data, data_cursor, **kwargs)
      while step_evaluation:
        logging.info ('Evaluation result: in any pattern_step "{}" iteration, match_on_going="{}", data_cursor="{}", data_token="{}"'
          .format(any_iter, match_on_going, data_cursor, data[data_cursor]))
        if any_iter == 0:
          # first pattern step matched
          if not(match_on_going):
            logging.debug ('start recognition and store the data_cursor as a start position')
            match_on_going = True
          #pattern_cursor_to_data_cursor[pattern_cursor] = data_cursor
        if matcheslist_extension != None:
          logging.debug ('extension of temporary_matcheslist with=%s',matcheslist_extension)  
          temporary_matcheslist.extend(matcheslist_extension)
          logging.debug ('temporary_matcheslist after extension=%s',temporary_matcheslist)  
        data_cursor += data_cursor_extension 
        any_iter += 1
        # case where a complex pattern has one first part being recognized while the data ends
        if data_cursor >= len(data):
          break

        step_evaluation, data_cursor_extension, pattern_cursor_extension, matcheslist_extension = evaluate (l, pattern_steps, pattern_cursor, data, data_cursor, **kwargs)  

      logging.info ('Evaluation result: after ANY pattern_step evaluation : "{}" iteration, match_on_going="{}", data_cursor="{}", data_token="{}"'
          .format(any_iter, match_on_going, data_cursor, data[data_cursor] if data_cursor < len(data) else 'no-more'))

      pattern_cursor += 1 

      if any_iter > 0:
        logging.info ('Evaluation result: some data_token have been recognized')
        # case where *[ab]b
        if pattern_cursor < len(pattern_steps) :
          next_quantifier, next_step = pattern_steps[pattern_cursor]
          logging.info ('checking the b*b case: any_iter="{}", pattern_cursor="{}", next_step="{}", data_cursor="{}", data[data_cursor-1]="{}"'
            .format(any_iter, pattern_cursor, next_step, data_cursor, data[data_cursor - 1]))
          step_evaluation, next_data_cursor_extension, next_pattern_cursor_extension, next_matcheslist_extension = evaluate (l, pattern_steps, pattern_cursor, data, data_cursor - 1, **kwargs)
          if any_iter > 0 and step_evaluation:
            logging.debug ('modify the cursor to face the case of b*b')
            data_cursor -= data_cursor_extension
            if matcheslist_extension != None:
              for i in len(matcheslist_extension):
                temporary_matcheslist.delete(-1)


    elif quantifier == '+':
      logging.info ('Evaluating AT_LEAST_ONE pattern_step')
      any_iter  = 0
      step_evaluation = step_evaluation, data_cursor_extension, pattern_cursor_extension, matcheslist_extension = evaluate (l, pattern_steps, pattern_cursor, data, data_cursor, **kwargs)
      while step_evaluation:
        logging.info ('Evaluation result: in AT_LEAST_ONE pattern_step "{}" iteration, match_on_going="{}", data_cursor="{}", data_token="{}"'
            .format(any_iter, match_on_going, data_cursor, data[data_cursor]))
        if any_iter == 0:
          # first pattern step matched
          if not(match_on_going):
            logging.debug ('start a new recognition')
            match_on_going = True
          pattern_cursor_to_data_cursor[pattern_cursor] = data_cursor      
        if matcheslist_extension != None:
          logging.debug ('extension of temporary_matcheslist with=%s',matcheslist_extension)  
          temporary_matcheslist.extend(matcheslist_extension)
          logging.debug ('temporary_matcheslist after extension=%s',temporary_matcheslist)  
        data_cursor += data_cursor_extension
        any_iter += 1
        # case where a complex pattern has one first part being recognized while the data ends
        if data_cursor >= len(data):
          break
        step_evaluation, data_cursor_extension, pattern_cursor_extension, matcheslist_extension = evaluate (l, pattern_steps, pattern_cursor, data, data_cursor, **kwargs)

      logging.info ('Evaluation result: after AT_LEAST_ONE pattern_step evaluation : "{}" iteration, match_on_going="{}", data_cursor="{}", data_token="{}"'
          .format(any_iter, match_on_going, data_cursor, data[data_cursor] if data_cursor < len(data) else 'no-more'))

      if any_iter > 0: 
        pattern_cursor += 1 
        logging.info ('Evaluation result: some data_token have been recognized')
        # case where +[b]b to recognize bbb
        if any_iter > 1 and pattern_cursor < len(pattern_steps) : 
        # at least 2 iterations are required, since it is '+', we cannot modify the first one
          next_quantifier, next_step = pattern_steps[pattern_cursor]
          logging.info ('checking the b+b case: any_iter="{}", pattern_cursor="{}", next_step="{}", data_cursor="{}", data[data_cursor-1]="{}"'
            .format(any_iter, pattern_cursor, next_step, data_cursor, data[data_cursor - 1]))          
          step_evaluation, next_data_cursor_extension, next_pattern_cursor_extension, next_matcheslist_extension = evaluate (l, pattern_steps, pattern_cursor, data, data_cursor - 1, **kwargs)
          if any_iter > 0 and step_evaluation:
            logging.debug ('modify the cursors to face the case of ab+b')
            data_cursor -= data_cursor_extension
            if matcheslist_extension != None:
              for i in len(matcheslist_extension):
                temporary_matcheslist.delete(-1)
      else:
        # abort recognition
        logging.info ('Evaluation result: no data_token has been recognized')
        if match_on_going:
          logging.debug  ('abort recognition')
        match_on_going = False
        pattern_data_start = pattern_data_start+1
        pattern_cursor = 0
        data_cursor += 1
        pattern_cursor_to_data_cursor = {}
        temporary_matcheslist = MatchesList()
        if l.lexer.pattern_must_match_data_start:
          break
  

    # a pattern has been recognized
    if pattern_cursor >= len(pattern_steps):
      if match_on_going:
        logging.info ('A pattern has been recognized=%s', pattern_steps) 
        logging.debug ('store the data_cursor as a end position')

        pattern_cursor_to_data_cursor[pattern_cursor] = data_cursor 
        current_groups = []
#        logging.debug ('data_cursor=', data_cursor)
#        logging.debug ('pattern_cursor=', pattern_cursor)
        for s, e in group_pattern_offsets_group_list:
#          logging.debug ('group_pattern_offsets_group_list=', group_pattern_offsets_group_list)
#          logging.debug ('pattern_cursor_to_data_cursor=', pattern_cursor_to_data_cursor)
#          logging.debug ('pattern_cursor_to_data_cursor[{}]={} pattern_cursor_to_data_cursor[{}]={}'.format(
#            s, pattern_cursor_to_data_cursor[s], e, pattern_cursor_to_data_cursor[e]))  
          logging.debug ('append from group_pattern_offsets_group_list to current_groups: value={} start={} end={}'.format(
            data[pattern_cursor_to_data_cursor[s]:pattern_cursor_to_data_cursor[e]],  pattern_cursor_to_data_cursor[s], pattern_cursor_to_data_cursor[e]))            
          current_groups.append([data[pattern_cursor_to_data_cursor[s]:pattern_cursor_to_data_cursor[e]], pattern_cursor_to_data_cursor[s], pattern_cursor_to_data_cursor[e]])

        # FIXME Here we have to iterate over the group of the current Match
        if temporary_matcheslist != None:
          #logging.debug  ('temporary_matcheslist=', temporary_matcheslist)
          for _m in temporary_matcheslist:
            #logging.debug  ('m=', _m)

            if _m != None:
              for g in _m._groups:
                logging.debug ('append from temporary_matcheslist to current_groups: value={} start={} end={}'
                  .format(g[Match.VALUE], g[Match.START], g[Match.END])) 
                current_groups.append([g[Match.VALUE], g[Match.START], g[Match.END]])

        if not(l.lexer.pattern_must_match_data_end) or (l.lexer.pattern_must_match_data_end and data_cursor == len(data)):
          logging.info ('create the Match corresponding to current_groups=%s',current_groups)
          logging.debug ('matcheslist before appending=',matcheslist)
 
          matcheslist.append(Match(groups=current_groups))
          logging.info ('append to matcheslist') #=',matcheslist)
        
        # stop parsing after the first match or if findall but only possible match since the pattern_must_match_data_start !
        if l.lexer.re in ['search', 'match'] or l.lexer.pattern_must_match_data_start:
          logging.info('stop exploration since match and ((the re method is search or match) or pattern_must_match_data_start)')  
          break
      else:
        # we are in the case of a pattern made of a single optional step which was not recognized
        # we have to step forward otherwise we fall in an infinite loop
        logging.info ('Case of a pattern made of a single optional step which was not recognized, we move forward data_cursor')
        data_cursor += 1
         
      pattern_data_start = data_cursor
      pattern_cursor = 0
      match_on_going = False
      if l.lexer.pattern_must_match_data_start:
        break
    else: 
      logging.info ('Exploration of data[{}]="{}" with pattern_steps[{}]="{}" and quantifier="{}" does not lead to the recognition of a whole pattern (a recognition may be ongoing)'
        .format(initial_data_cursor, initial_data, initial_pattern_cursor, initial_step, initial_quantifier))   

  logging.info('Ending semantic parsing with returning matcheslist=%s',matcheslist)  
  return matcheslist


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  MAIN
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__ == '__main__':  
  start = 0
  end = 1
  data =  [{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'Pyrata', 'pos': 'NNP'}]

  print ('Debug: create the Match(start={}, end={}, value={})'.format(start, end, data[start:end]))
  match = Match (start=start, end=end, value=data[start:end])
  print('Debug: match=', match)