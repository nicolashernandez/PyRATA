# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to compile pattern to recognize
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import logging
# logging.info() Report events that occur during normal operation of a program (e.g. for status monitoring or fault investigation)
# logging.debug() for very detailed output for diagnostic purposes
# logging.warning() Issue a warning regarding a particular runtime event

#import re 
from re import compile 

from pprint import pprint, pformat
import ply.yacc as yacc
from sympy import *

from pyrata.lexer import *



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



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# wi less consumption memory http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to
def depth(l):
    if isinstance(l, list):
        return 1 + max(depth(item) for item in l)
    else:
        return 0



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class SyntacticPatternParser(object):

# p.lexer. variables which are modified in the parsing
#
# group_pattern_offsets_group_list
# pattern_must_match_data_start
# pattern_must_match_data_end
# pattern_steps
#
# see definition in lexer

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
  def p_expression(self, p):
    '''expression : 
       expression : quantified_step_group_list
       expression : BEFORE_FIRST_TOKEN quantified_step_group_list
       expression : quantified_step_group_list AFTER_LAST_TOKEN
       expression : BEFORE_FIRST_TOKEN quantified_step_group_list AFTER_LAST_TOKEN'''
    
    log(p, '(expression->...)')

    # add the step range from 0 to the last pattern step as the initial group 0
    p.lexer.group_pattern_offsets_group_list.append([0, len(p.lexer.pattern_steps)])  

    #
    p[0] = p[1]
    if len(p) == 3:
      if p[1] == '^':
        p[0] = p[2]
        p.lexer.pattern_must_match_data_start = True
      else:
        p[0] = p[1]        
        p.lexer.pattern_must_match_data_end = True
    elif len(p) == 4:
      p[0] = p[2]          
      p.lexer.pattern_must_match_data_start = True
      p.lexer.pattern_must_match_data_end = True   
    logging.info('\treturn p[0]={}'.format(p[0]))

    logging.info ('# ----------------------------------')
    logging.info ('# Syntactic structure parsed tree (pattern_steps): %s',pformat(p.lexer.pattern_steps))
    logging.info ('# Must start the data=\t%s',p.lexer.pattern_must_match_data_start)
    logging.info ('# Must end the data=\t%s',p.lexer.pattern_must_match_data_end)
    logging.info ('# Group_pattern_offsets_group_list=%s',p.lexer.group_pattern_offsets_group_list)
    logging.info ('# ----------------------------------')
  

# _______________________________________________________________
  def p_quantified_step_group_list(self, p): 
    ''' quantified_step_group_list : quantified_step_group 
                                   | quantified_step_group_list quantified_step_group  '''
    if len(p) == 2:
      p[0] = p[1]
      log(p, '(quantified_step_group_list->quantified_step_group)')
    elif len(p) == 3:
      log(p, '(quantified_step_group_list->quantified_step_group_list quantified_step_group)')
      logging.debug ('p[1] =%s',pformat(p[1]))
      logging.debug ('p[2] =%s',pformat(p[2]))

      if not(isinstance (p[1][0], list)):      # 2nd part of a steps sequence 
        logging.debug ('2nd part of a steps sequence ')
        p[0] = [p[1], p[2]]
      else:                                    # 3rd and more parts of a steps sequence
        logging.debug ('3rd and more parts of a steps sequence')
        p[1].append(p[2])
        p[0] = p[1]

    logging.info('\treturn p[0]={}'.format(p[0]))

# _______________________________________________________________
  def p_quantified_step_group(self, p):
    ''' quantified_step_group : step_group
            | step_group OPTION
            | step_group ATLEASTONE 
            | step_group ANY 
            ''' 

    if len(p) == 2:
      log(p, '(quantified_step_group->step_group)')
    elif len(p) == 3:
      log(p, '(quantified_step_group->step_group QUANTIFIER)')

    # store the step
    # quantifier=[None, '*', '+', '?'] not=[True, False] group=[True, False] p[1]
    if len(p) == 2:
      p[0] = [None, p[1]]
    elif p[2] == '*':
      p[0] = ['*', p[1]]
    elif p[2] == '+':
      p[0] = ['+', p[1]]
    elif p[2] == '?':  
      p[0] = ['?', p[1]]
    else:
      True
      logging.warning ('syntactic_pattern_parser - p_quantified_step_group - should not be here p[2]=%s',p[2])

    # extend the patten step structures with for each elementary step its list of variables, its list of variable names, and the symbolic expression,
    if not isinstance (p[1], list): 
    # we are dealing with a step 
      p[0].append(p.lexer.single_constraint_variable_list)
      p[0].append(p.lexer.single_constraint_tuple_list)
      p[0].append(p.lexer.single_constraint_symbol_list) 
      p[0].append(p.lexer.symbolic_step_expression[0])
      p.lexer.single_constraint_symbol_list = []    
      p.lexer.single_constraint_tuple_list = []
      p.lexer.single_constraint_variable_list = []   
      p.lexer.symbolic_step_expression = []
    
#    logging.info ('\tpattern_steps={} append pattern_steps = {}'.format(p.lexer.pattern_steps, p[0]))

    logging.info ('\tappend pattern_steps = {}'.format(p[0]))       
    p.lexer.pattern_steps.append(p[0])

    logging.info ('\treturn p[0]={}'.format(p[0]))
 

# _______________________________________________________________
  def p_step_group(self,p):
    '''step_group : step
                  | LPAREN step_group_class RPAREN'''
#                   | NOT step_group
    # get the start and the end of the part of the pattern recognized by the current rule 
    step_start, step_end = get_current_pattern_step_offsets(p) 

    p[0] = get_current_pattern_step(p, step_start, step_end)

    #logging.info ('DEBUG p[0]:{}'.format(p[0]))

    if len(p) == 2: 
      log(p, '(step_group->step)')
      logging.info ('step sympy expression:{}'.format(p[1]))

 
 #   elif len(p) == 3: 
 #     log(p, '(step_group->NOT step_group)') 

    elif len(p) == 4:
      log(p, '(step_group->LPAREN step_group_class RPAREN)')
      logging.debug ('depth={} ; p[2] = {} ; len(p[2]) = {}; len(p[2][0]) = {}; '.format(depth(p[2]), p[2],len(p[2]), len(p[2][0])))
      p[0] = [p[2]]

      if isinstance (p[2][0][0], list): 
        logging.debug ('dealing with alternatives') 
        p[0] = p[2]
      else:
        True
        logging.debug ('not dealing with alternatives p[1][0][0]=%s', p[2][0][0])

    logging.info('\treturn p[0]={}'.format(p[0]))

# _______________________________________________________________
  def p_step_group_class(self,p):
    '''step_group_class : quantified_step_group_list
                        | step_group_class OR quantified_step_group_list'''

    if len(p) == 2:
      log(p, '(step_group_class->quantified_step_group_list)')

      if not(isinstance (p[1][0], list)):
        p[0]=[p[1]]
      else:
        p[0]=p[1]

      logging.debug ('len(p[0])={}'.format(p[0]))
      logging.info ('\tpop pattern_steps=%s',p.lexer.pattern_steps[len(p.lexer.pattern_steps)-len(p[0]):len(p.lexer.pattern_steps)])
      del (p.lexer.pattern_steps[len(p.lexer.pattern_steps)-len(p[0]):len(p.lexer.pattern_steps)])

    else:
      log(p, '(step_group_class->step_group_class OR quantified_step_group_list)') 
      logging.debug ('p[1] = {} ; len(p[0]) = {}'.format(p[1],len(p[1])))
      logging.debug ('p[3] = {} ; len(p[3]) = {}'.format(p[3],len(p[3])))

      if not(isinstance (p[1][0][0], list)):  # 2nd part of an alternative
        logging.debug ('2nd part of an alternative')
        if not(isinstance (p[3][0], list)) or len(p[3]) == 1:                      # 2nd part has only one step
          logging.debug ('2nd part has only one step')
          p[0] = [p[1], [p[3]]]                     
        else:                                   # 2nd part is a sequence of several steps
          logging.debug ('2nd part is a sequence of several steps')
          p[0] = [p[1], p[3]] 
      else:                                   # 3rd and more parts of an alternative
        logging.debug ('3rd and more parts of an alternative')
        p[1].append(p[3])                     
        p[0] = p[1]
      logging.info ('\tpop pattern_steps=%s',p.lexer.pattern_steps[len(p.lexer.pattern_steps)-len(p[3]):len(p.lexer.pattern_steps)])
      del (p.lexer.pattern_steps[len(p.lexer.pattern_steps)-len(p[3]):len(p.lexer.pattern_steps)])

    logging.info('\treturn p[0]={}'.format(p[0]))
 

# _______________________________________________________________
  def p_step(self,p):
    '''step : single_constraint
            | LBRACKET constraint_class RBRACKET '''  # | NOT atomicconstraint # ajoute WARNING: 2 shift/reduce conflicts
    #log(p, '(step->...)')
    if len(p) == 2:
      p[0] = p[1]
      log(p, '(step->single_constraint)')
    
    #elif p[1] == '!':
    #  p[0] = not(p[2])
    #  log(p, '(step->NOT step)')
    
    else:
      p[0] = p[2]
      log(p, '(step->LBRACKET constraint_class RBRACKET)')
    logging.info ('step sympy expression:{}'.format(p[0]))


    p.lexer.symbolic_step_expression.append(p[0])

# _______________________________________________________________
  def p_constraint_class(self,p):
    '''constraint_class : constraint_class AND constraint_class_part
            | constraint_class OR constraint_class_part 
            | constraint_class_part ''' 
    
    #log(p, '(constraint_class->...)')  
    if len(p) == 2:
      p[0] = p[1] 
      log(p, '(constraint_class->constraint_class_part)')
    #
    else:
      if p[2] == '&':
        p[0] = And(p[1], p[3]) 
        log(p, '(constraint_class->constraint_class AND constraint_class_part)')

      else: 
        p[0] = Or(p[1], p[3])
        log(p, '(constraint_class->constraint_class OR constraint_class_part)')
    
    logging.info ('step sympy expression:{}'.format(p[0]))      

# _______________________________________________________________
  def p_constraint_class_part(self,p):
    '''constraint_class_part : single_constraint
                    | LPAREN constraint_class RPAREN  
                    | NOT constraint_class '''
    
    #log(p, '(constraint_class_part->...)')  

    if p[1] == '(':
      p[0] = p[2]
      log(p, '(constraint_class_part->LPAREN constraint_class RPAREN)')
    
    elif p[1] == '!':
      p[0] = Not(p[2])
      log(p, '(constraint_class_part->NOT constraint_class)')
    
    else:
      p[0] = p[1]
      log(p, '(constraint_class_part->single_constraint)')

    logging.info ('step sympy expression:{}'.format(p[0]))

# _______________________________________________________________
  def p_single_constraint(self,p):
    '''single_constraint : NAME EQ VALUE 
                          | NAME MATCH VALUE
                          | NAME IN VALUE'''
    
    log(p, '(single_constraint->...)')  
    #attName = p[1]
    #operator = p[2]
    #attValue = p[3][1:-1]

    # add to the temporary list of single constraint string
    single_constraint_string = ''.join([p[1],p[2],p[3]])
    p.lexer.single_constraint_symbol_list.append(single_constraint_string)

    # add single contraint tuple to lists in the lexer 
    c = {}
    c['name'] = p[1]
    c['operator'] = p[2]
    c['value'] = p[3][1:-1]
    if c['operator'] == '~': 
      #c['value'] = re.compile(c['value'])
      c['value'] = compile(c['value'])
    p.lexer.single_constraint_tuple_list.append(c)

    # build a variable and a name
    indice = str(len(p.lexer.single_constraint_tuple_list)-1)
    var = {} 
    var[indice] =  symbols(single_constraint_string.replace(' ','\\ '))
    p[0] = var[indice]
    p.lexer.single_constraint_variable_list.append(var[indice])


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING ERROR HANDLING
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def p_error(self,p):
    if not p:
       
      logging.info("Pattern syntaxically parsed.")
      return

    # http://www.dabeaz.com/ply/ply.html#ply_nn26 6.8.2
     # Read ahead looking for a closing ';'

    logging.warning('syntactic parsing error - unexpected token type="{}" with value="{}" at position {}. Search an error before this point.'.format(p.type, p.value, p.lexer.lexpos))
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

    # keep track of 

    # start the parser
    start='expression'
    if 'start' in kwargs.keys(): # MANDATORY
      start = kwargs['start'] 
    kwargs.pop('start', None)      
    # debugging and logging http://www.dabeaz.com/ply/ply.html#ply_nn44 
    self.parser = yacc.yacc(module=self, start=start, errorlog=yacc.NullLogger(), **kwargs) #

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  MAIN
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# example use:
if __name__ == '__main__':
  pattern='?lem="the" ( pos="JJ"* [pos="NN" & (lem="car" | !lem="bike" | !(lem="bike"))] ) [raw="is" | raw="are"]'
  print ('Pattern:', pattern)

  #data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'blue', 'lem':'blue', 'pos':'JJ'}]     
  #data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
  
  #pattern = 'pos:"NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}]
  print ('Data:', data)

  # Build the parser and 
  l = Lexer(pattern=pattern, data=data) 
  m = SyntacticPatternParser(tokens=l.tokens, start='expression')

  # try it out
  # print ("Copy the grammar line without 'Grammar: ' (whitespace should not been included); The semi-colon ';' will lead to a parsing error")
  # while True:
  #   try:
  #     #text2parse
  #     s = input('cl > ')   # Use raw_input on Python 2
  #   except EOFError:
  #     break
  #   m.parser.parse(s, l.lexer, tracking=True)


