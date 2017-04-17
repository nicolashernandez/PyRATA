# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to evaluate the semantic of a given pattern step
# 
# Follows the https://docs.python.org/3/library/re.html#re-objects API
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ply.yacc as yacc
from pyrata.lexer import *
from pyrata.syntactic_pattern_parser import *
import sys # for the function name
import pyrata.semantic_analysis

def printList(_depth, _list):
  if isinstance(_list[0], list):
    #if not(isinstance(s[1][0], list)):
    #  print (_depth*' ', s[1]) 
    print (_depth*' '+'[')
    for l in _list:
      printList (_depth+1, l)  
    print (_depth*' '+'],', end='')
  else:
    if isinstance(_list[1], list):
      print (_depth*' '+'[{},'.format(_list[0]))
      printList (_depth+6, _list[1])    # [None, which is the maximal string
      print (_depth*' '+'],')
    else:   
      print (_depth*' '+'{}'.format(_list))


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

#    print ('# Syntactic structure parsed:')
#    printList(0, self.getLexer().lexer.pattern_steps)
#    pprint(self.getLexer().lexer.pattern_steps)
    # for s in self.getLexer().lexer.pattern_steps:
    #   if isinstance(s[1], list): 
    #     print ('\t[',s[0])
    #     for g in s[1]:
    #       print ('\t\t{}'.format(g))
    #     print ('\t]')
    #   else: print ('\t{}'.format(s))
#    print ('# group_pattern_offsets_group_list=', self.getLexer().lexer.group_pattern_offsets_group_list)

    # self.getLexer().lexer.group_pattern_offsets_group_list= [[0, 1]]
    # # self.getLexer().lexer.pattern_steps = [ [None, 'raw="D"'] ]
    # # self.getLexer().lexer.pattern_steps = [ [None, [[[None, 'raw="B"']]]] ]
    # self.getLexer().lexer.pattern_steps = [ [None, [[[None, 'raw="D" '], 
    #                                                   [None, 'raw="E"']]]] ]
    # self.getLexer().lexer.group_pattern_offsets_group_list= [[0, 2]]
    # self.getLexer().lexer.pattern_steps = [ [None, 'raw="D"'], 
    #                                         [None, [[[None, 'raw="E"']]]] ]
    #     [
#   [None, 'raw="A" '],
#   [None, [[[None, 'raw="B"']]]],
#   [None, [[
#     [None, [[ 
#       ['*', 'raw="C"'],
#       [None, [[
#         [None, 'raw="C" '], 
#         [None, 'raw="D"']]]],
#       [None, [[
#         [None, 'raw="E"']]]]]]]
#     ]]],  
#   [None, [[
#     [None, 'raw="F"']]]]
# ]


    # self.getLexer().lexer.group_pattern_offsets_group_list= [[0, 1], [0, 1]]
    # self.getLexer().lexer.pattern_steps = [ 
    #   ['+', 
    #       [[[None, 'pos="VB" '], ['?', 'pos="DT"'], ['*', 'pos="JJ"'], [None, 'pos="NN" '], [None, 'pos="."']]]
    #   ] 
    # ]
 
#    self.getLexer().lexer.group_pattern_offsets_group_list= [[0, 7], [1, 2], [2, 6], [2, 6], [3, 5], [5, 6], [6, 7]]

    #exit() # FIXME used to stop the parsing after the syntactic analysis (to see the parser.out or adapt the parser)

    # print ('# Revised syntactic structure parsed:')
    # for s in self.getLexer().lexer.pattern_steps:
    #   if isinstance(s[1], list): 
    #     print ('\t[',s[0])
    #     for g in s[1]:
    #       print ('\t\t{}'.format(g))
    #     print ('\t]')
    #   else: print ('\t{}'.format(s))
    # print ('# group_pattern_offsets_group_list=', self.getLexer().lexer.group_pattern_offsets_group_list)
     
    #print ('Debug: compiledPattern=', self)
    r = pyrata.semantic_analysis.parse_semantic (self, data, **kwargs)
    return r

  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def search(self, data, **kwargs):
    """
    """

    method = 'search'
    matcheslist = self.re_method (data, method=method, **kwargs)

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
  def split(self, data, **kwargs):
    """
    """
    raise Exception ('Not implemented yet')


  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def sub(self, data, **kwargs):
    """
    """
    raise Exception ('Not implemented yet')


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def parse_syntactic(pattern, **kwargs):

  verbosity  = 0
  if 'verbosity' in kwargs.keys(): 
    verbosity  = kwargs['verbosity']

  lexicons = {}
  if 'lexicons' in kwargs.keys():
    lexicons = kwargs['lexicons']
    kwargs.pop('lexicons', None)

     # Build the lexer 
  l = Lexer(pattern=pattern, lexicons=lexicons)

  # Build the syntax parser
  y = SyntacticPatternParser(tokens=l.tokens, **kwargs)

  # we start the compilation to get an internal representation of patterns
  if verbosity >1:
    print (1*'  ','________________________________________________')      
    print (1*'  ','Info: syntax parsing...')
  y.parser.parse(pattern, l.lexer, tracking=True)

  return l
