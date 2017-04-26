# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to evaluate the semantic of a given pattern step
# 
# Follows the https://docs.python.org/3/library/re.html#re-objects API
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import logging
from pprint import pformat
import ply.yacc as yacc
import sys # for the function name

from pyrata.lexer import *
from pyrata.syntactic_pattern_parser import *
import pyrata.semantic_pattern_parser

(PREFIX_BEGIN, PREFIX_INSIDE, PREFIX_OTHER) = ('B-', 'I-', 'O-')

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class CompiledPattern(object):
  lexer = None

  def __init__(self, **kwargs):
    if 'lexer' in kwargs.keys():
      self.lexer = kwargs['lexer']

  def getLexer(self):
    return self.lexer


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def re_method(self, data, **kwargs):
    """
    """

    if 'method' in kwargs.keys(): 
      method  = kwargs['method']
    else:
      raise Exception ('Error: in ', sys._getframe().f_code.co_name,': no re method defined')
    kwargs.pop('method', None)

    self.getLexer().lexer.re = method

    #exit() # HERE used to stop the parsing after the syntactic analysis (to see the parser.out or adapt the parser)

    # HERE to shortcut the compilation result and experiment the semantic analysis
    # self.getLexer().lexer.group_pattern_offsets_group_list= [[0, 1]]
    # # self.getLexer().lexer.pattern_steps = [ [None, 'raw="D"'] ]
    # # self.getLexer().lexer.pattern_steps = [ [None, [[[None, 'raw="B"']]]] ]
    # self.getLexer().lexer.pattern_steps = [ [None, [[[None, 'raw="D" '], 
    #                                                   [None, 'raw="E"']]]] ]
    # self.getLexer().lexer.group_pattern_offsets_group_list= [[0, 2]]
    # self.getLexer().lexer.pattern_steps = [ [None, 'raw="D"'], 
    #                                         [None, [[[None, 'raw="E"']]]] ]
   
    logging.info("# Data=%s", pformat(data))
    r = pyrata.semantic_pattern_parser.parse_semantic (self, data, **kwargs)
    return r

  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def search(self, data, **kwargs):
    """
    """

    matcheslist = self.re_method (data, method='search', **kwargs)

    if len(matcheslist) > 0 :
      return matcheslist.group(0)
    return None


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def match(self, data, **kwargs):
    """
    """
    raise Exception ('Not implemented yet')


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def findall(self, data, **kwargs):
    """
    """
    method = 'findall'
    matcheslist = self.re_method (data, method=method, **kwargs)
    matches = []
    if len(matcheslist)>0 :
      for i in range(len(matcheslist)):
        #print ('Debug: len(data):',len(data),'; start:', start,'; end:',end)
        matches.append(matcheslist.group(i).group())
      return matches
    return None



  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def finditer(self, data, **kwargs):
    """
    """

    method = 'finditer'
    matcheslist = self.re_method (data, method=method, **kwargs)

    # build the structure to return
    if len(matcheslist)>0 :
      return matcheslist    
    return None 


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def annotate(self, annotation, data, group = [0], action = 'sub', iob = False, **kwargs):
    """
    """

    prefix = ''

    data_copy = list(data)
    if isinstance(annotation, dict):
      annotation = [annotation]

    iter = self.finditer(data, **kwargs) #reversed([finditer(pattern, data)])  
    if iter != None:
      size = 0
      for m in iter:
        for g in group:
          #print ('Debug: m={} g={} start={} end={}'.format(m, g, m.start(g), m.end(g)))
          if action == 'sub':
  #          data_copy[m.start(g):m.end(g)] = annotation
            data_copy[m.start(g)+size:m.end(g)+size] = annotation
            size +=  len(annotation) - (m.end(g) - m.start(g)) 

          elif action == 'update':
            if len(annotation) == 1:
              for k in annotation[0].keys():
                for r in range (m.start(g), m.end(g)):
                  if iob and r == m.start(g): 
                    prefix = PREFIX_BEGIN
                  elif iob: 
                    prefix = PREFIX_INSIDE
                  data_copy[r][k] = prefix + annotation[0][k]
            else:
              for k in annotation[0].keys():
                for r in range (m.start(g), m.end(g)):
                  if len(annotation) == (m.end(g) - m.start(g)): 
                    if iob and r == m.start(g): 
                      prefix = PREFIX_BEGIN
                    elif iob: 
                      prefix = PREFIX_INSIDE
                    data_copy[r][k] = prefix + annotation[0][k]
                  else: # Verbosity not the same size
                    data_copy = data  
                    break

          elif action == 'extend':
            if len(annotation) == 1:
              for k in annotation[0].keys():
                for r in range (m.start(g), m.end(g)):
                  if k not in data_copy[r]:
                    if iob and r == m.start(g): 
                      prefix = PREFIX_BEGIN
                    elif iob: 
                      prefix = PREFIX_INSIDE
                    data_copy[r][k] = prefix+annotation[0][k]
            else:
              for k in annotation[0].keys():
                for r in range (m.start(g), m.end(g)):
                  if len(annotation) == (m.end(g) - m.start(g)):
                    if k not in data_copy[r]:
                      if iob and r == m.start(g): 
                        prefix = PREFIX_BEGIN
                      elif iob: 
                        prefix = PREFIX_INSIDE
                      data_copy[r][k] = prefix+annotation[0][k]
                  else: # Verbosity not the same size
                    data_copy = data  
                    break       
    return data_copy


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
  def sub (self, repl, data, group = [0], **kwargs):
    """
    Return the data obtained by replacing the leftmost non-overlapping occurrences of 
    pattern matches or group of matches in data by the replacement repl. 
    """
    return self.annotate (repl, data, group, action = 'sub', iob = False, **kwargs)


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
  def subn (self, repl, data, **kwargs):
    """
    Perform the same operation as sub(), but return a tuple (new_string, number_of_subs_made).
    """
    raise Exception ("Not implemented yet !")

  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
  def update (self, repl, data, group = [0], iob = False, **kwargs):
    """
    Return the data after updating (and extending) the features of a match or a group of a match 
    with the features of a dict or a sequence of dicts (of the same size as the group/match). 
    """
    return self.annotate (repl, data, group = group, action = 'update', iob = iob, **kwargs)


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
  def extend (self, repl, data, group = [0], iob = False, **kwargs):
    """
    Return the data after updating (and extending) the features of a match or a group of a match 
    with the features of a dict or a sequence of dicts (of the same size as the group/match). 
    """
    return self.annotate (repl, data, group = group, action = extend, iob = iob, **kwargs)


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def split(self, data, **kwargs):
    """
    """
    raise Exception ('Not implemented yet')


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def __repr__(self):
    return '<pyrata.syntactic_pattern_parser CompiledPattern object; \n\tstarts_wi_data="'+str(self.getLexer().lexer.pattern_must_match_data_start)+      '"\n\tends_wi_data="'+str(self.getLexer().lexer.pattern_must_match_data_end)+      '"\n\tlexicon="'+str(self.getLexer().lexer.lexicons.keys())        +'"\n\tpattern_steps="\n'+  pformat(self.getLexer().lexer.pattern_steps)+      '\n">'


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def parse_syntactic(pattern, lexicons, **kwargs):

  # Build the lexer 
  l = Lexer(pattern=pattern, lexicons=lexicons)

  # Build the syntax parser
  y = SyntacticPatternParser(tokens=l.tokens, **kwargs)

  logging.info ('# ----------------------------------')
  logging.info ('# Pattern=\t%s',pattern)
  logging.info ('# Lexicons=\t%s',lexicons)
  logging.info ('Starting syntax analysis...')

  # we start the compilation to get an internal representation of patterns

  y.parser.parse(pattern, l.lexer, tracking=True)

  return l
