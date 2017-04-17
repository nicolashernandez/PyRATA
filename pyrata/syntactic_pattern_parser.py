# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to compile pattern to recognize
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ply.yacc as yacc
from pyrata.lexer import *

import re

from pprint import pprint

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_current_pattern_step_offsets(p):
  ''' Line Number and Position Tracking'''
  # http://www.dabeaz.com/ply/ply.html#ply_nn33
  left_symbol_start, left_symbol_end = p.lexspan(1)
  #if self.verbosity >3: 
  #  print ('\t\tget_current_pattern_step_offsets: p.lexer.lexpos=',p.lexer.lexpos,'; isInLexTokenEndDict=',(p.lexer.lexpos in p.lexer.lexTokenEndDict))
  if p.lexer.lexpos > len(p.lexer.lexdata):
    previous_lextoken_end = len(p.lexer.lexdata)
  else:
    previous_lextoken_end = p.lexer.lexpos - len(p.lexer.lexTokenEndDict[p.lexer.lexpos].value)
  #print ('Debug: lexdata from {} to {}'.format(left_symbol_start, previous_lextoken_end))
  return left_symbol_start, previous_lextoken_end



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_current_pattern_step(p, start, end):
  ''' surface form of the current parsed step'''
  return p.lexer.lexdata[start:end]

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
# wi less consumption memory http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to
def depth(l):
    if isinstance(l, list):
        return 1 + max(depth(item) for item in l)
    else:
        return 0



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# verbosity  (0 None 1 global 2 verbose) 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class SyntacticPatternParser(object):

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
  def p_expression(self, p):
    '''expression : 
       expression : quantified_step_group_list
       expression : BEFORE_FIRST_TOKEN quantified_step_group_list
       expression : quantified_step_group_list AFTER_LAST_TOKEN
       expression : BEFORE_FIRST_TOKEN quantified_step_group_list AFTER_LAST_TOKEN'''
    
    if self.verbosity >1:
      self.log(p, '(expression->...)')

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
    print('\treturn p[0]={}'.format(p[0]))

    #
    if self.verbosity >1: 
      print ('# ----------------------------------')
      #print ('# Syntactic structure parsed raw:',p.lexer.pattern_steps)
      print ('# Syntactic structure parsed tree:')
      pprint(p.lexer.pattern_steps)
      # for s in p.lexer.pattern_steps:
      #   if isinstance(s[1], list): 
      #     print ('\t[',s[0])
      #     for g in s[1]:
      #       print ('\t\t{}'.format(g))
      #     print ('\t]')
      #   else: print ('\t{}'.format(s))

      print ('# Must start the data=\t',p.lexer.pattern_must_match_data_start)
      print ('# Must end the data=\t',p.lexer.pattern_must_match_data_end)

      print ('# Group_pattern_offsets_group_list=',p.lexer.group_pattern_offsets_group_list)


    # reorder the groups to simulate the perl group order 
    ordered_list = []
    list_to_order = p.lexer.group_pattern_offsets_group_list
    while len(list_to_order) != 0:
      min_a = len(p.lexer.pattern_steps)
      max_b = 0
      for i, (m, n) in enumerate(list_to_order):
        if (m <= min_a):
          min_a = m
      for i, (m, n) in enumerate(list_to_order) :
        if m == min_a and n >= max_b:
          max_b = n 
          i_to_del = i

      ordered_list.append(list_to_order[i_to_del])
      list_to_order.pop(i_to_del)
    p.lexer.group_pattern_offsets_group_list =  ordered_list

    if self.verbosity >1:
      print ('# Ordered group_pattern_offsets_group_list=',p.lexer.group_pattern_offsets_group_list)
      for i, (a, b) in enumerate(p.lexer.group_pattern_offsets_group_list):
        print ('\tgroup {} = {}'.format(i, p.lexer.pattern_steps[a:b]))
      print ('# ----------------------------------')
  

# _______________________________________________________________
  def p_quantified_step_group_list(self, p): 
    ''' quantified_step_group_list : quantified_step_group 
                                   | quantified_step_group_list quantified_step_group  '''
    if len(p) == 2:
      p[0] = p[1]
      if self.verbosity >1:
        self.log(p, '(quantified_step_group_list->quantified_step_group)')
    elif len(p) == 3:
      if self.verbosity >1:
        self.log(p, '(quantified_step_group_list->quantified_step_group_list quantified_step_group)')
      #print ('Debug: p[1] =', p[1])
      #print ('Debug: p[2] =', p[2])
 #     print ('Debug: p.lexer.buffer=', p.lexer.buffer)
      #print ('Debug: p[0] = [p[1], p[2]]')
      #p[0] = p.lexer.buffer.append(p[2])  
      if not(isinstance (p[1][0], list)):      # 2nd part of a steps sequence 
        print ('Debug: 2nd part of a steps sequence ')
        p[0] = [p[1], p[2]]
      else:                                    # 3rd and more parts of a steps sequence
        print ('Debug: 3rd and more parts of a steps sequence')
        p[1].append(p[2])
        p[0] = p[1]

      #print ('Debug: p[0]=', p[0])
      p.lexer.buffer = None

    # get the start and the end of the part of the pattern recognized by the current rule 
    step_start, step_end = get_current_pattern_step_offsets(p)

    # store the last couple of quantified step position which delimits a group candidate
    #print ('   Debug: p_quantified_step_group_list - lexdata from {} to {}'.format(step_start, step_end))    
    if step_start in p.lexer.quantified_step_start: # and step_end in p.lexer.quantified_step_end:
      #p.lexer.last_group_offsets_candidate = [p.lexer.quantified_step_start[step_start],p.lexer.quantified_step_end[step_end]]    
      p.lexer.last_group_offsets_candidate = [p.lexer.quantified_step_start[step_start],p.lexer.quantified_step_index]    
      if self.verbosity >2:
        print ('\tset last_group_offsets_candidate wi lexdata from {} to {}'.format(step_start, step_end))    
    else:
      if self.verbosity >2:
        print ('\tdo not set last_group_offsets_candidate wi lexdata from {} to {}'.format(step_start, step_end))
       
    print('\treturn p[0]={}'.format(p[0]))


# _______________________________________________________________
  def p_quantified_step_group(self, p):
    ''' quantified_step_group : step_group
            | step_group OPTION
            | step_group ATLEASTONE 
            | step_group ANY 
            ''' 

    if self.verbosity >1:
      if len(p) == 2:
        self.log(p, '(quantified_step_group->step_group)')
      elif len(p) == 3:
        self.log(p, '(quantified_step_group->step_group QUANTIFIER)')

    # FIX and p[1] != [[]] is a fix, should probably be fixed at the p_step_group method
    #if p.lexer.step_already_counted == 0 and p[1] != [[]]:
    if True:
      if self.verbosity >2:
        print ('\tstep_not_counted i.e. step_already_counted == 0')
    # to prevent from duplicate step counting (wo then wi parenthesis), pattern_step storing... 
    # Production= (quantified_step_group->step_group) raw="is"
    #   Debug: quantified_step_index++
    #   Debug: store the step offsets corresponding to the character positions of lexdata i.e. 10->2 to 18->3
    # Production= (step_group->LPAREN step_group_class RPAREN) (raw="is") 
    #   Debug: group detected from 1 to 2 step(s)
    # Production= (quantified_step_group->step_group) (raw="is") 
    #   Debug: quantified_step_index++
    #   Debug: store the step offsets corresponding to the character positions of lexdata i.e. 9->3 to 20->4

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
        print ('Warning: syntactic_pattern_parser - p_quantified_step_group - should not be here p[2]=',p[2])
      #p.lexer.pattern_steps.append(p[0])
      #if self.verbosity >2:
      #  print ('\tpattern_steps.appends = {}'.format(p[0]))

      # get the start and the end of the part of the pattern recognized by the current rule 
      step_start, step_end = get_current_pattern_step_offsets(p)

      # store the corresponding quantified step at the character position start and end 
      p.lexer.quantified_step_start[step_start] = p.lexer.quantified_step_index
      p.lexer.quantified_step_end[step_end] = p.lexer.quantified_step_index +1
      if self.verbosity >2:
        print ('\tstore the mapping from lexdata character positions to quantified_step_index i.e. {}->{} to {}->{}'.format(step_start,p.lexer.quantified_step_index, step_end, p.lexer.quantified_step_index+1))
        print ('\tincrement the step: quantified_step_index++')
        print ('\tset the step counter to 1 to avoid duplicate counting: step_already_counted=1')

      # increment the step
      p.lexer.quantified_step_index += 1

      # to avoid duplicate counting
      p.lexer.step_already_counted = 1
    else:
      if self.verbosity >2:
        print ('\tstep_already_counted: consequently we do nothing')

    p.lexer.pattern_steps.append(p[0])
    #if self.verbosity >2:
    print ('\tappend pattern_steps = {}'.format(p[0]))       
    print ('\treturn p[0]={}'.format(p[0]))
 

# _______________________________________________________________
  def p_step_group(self,p):
    '''step_group : step
                  | NOT step_group
                  | LPAREN step_group_class RPAREN'''

    # get the start and the end of the part of the pattern recognized by the current rule 
    step_start, step_end = get_current_pattern_step_offsets(p) 
    p[0] = get_current_pattern_step(p, step_start, step_end)

    if len(p) == 2: 
      if self.verbosity >1:self.log(p, '(step_group->step)')
    elif len(p) == 3: 
      if self.verbosity >1:self.log(p, '(step_group->NOT step_group)') 
    elif len(p) == 4:
      if self.verbosity >1:self.log(p, '(step_group->LPAREN step_group_class RPAREN)')
      print ('Debug: depth={} ; p[2] = {} ; len(p[2]) = {}; len(p[2][0]) = {}; '.format(depth(p[2]), p[2],len(p[2]), len(p[2][0])))
      p[0] = [p[2]]

      if isinstance (p[2][0][0], list): 
      #if len(p[2]) >1:        # if we are dealing with alternatives 
        print ('\twe are dealing with alternatives') 
        p[0] = p[2]
      else:
        print ('\twe are not dealing with alternatives p[1][0][0]=', p[2][0][0])

      # if len(p.lexer.step_group_class) == 1:
      #   if self.verbosity >2:
      #     print ('\tprocessing a step_group_class made only of a quantified_step_group_list (wo alternatives)')
      #     print ('\tgroup detected from {} to {} step(s)'.format(p.lexer.last_group_offsets_candidate[0],p.lexer.last_group_offsets_candidate[1]))
      #     print ('\treset the group counter step_group_class (used for alternatives) i.e. step_group_class=[]')
      #   #print ('\tDebug: len(step_group_class)={} len(pattern_steps)={}'.format(len(p.lexer.step_group_class), len(p.lexer.pattern_steps)))
      #   #print ('\tDebug: del from={} to={}'.format(p.lexer.step_group_class[0][0], p.lexer.step_group_class[-1][1]))

      #   # the rule which recognize a group matches so we definitively store the last couple of quantified step position 
      #   # as a group (at least for the first position)
      #   p.lexer.group_pattern_offsets_group_list.append([p.lexer.last_group_offsets_candidate[0],p.lexer.quantified_step_index])

      #   # to process single group as list of alternatives groups ; step_group_class constains the offset of only one group
      #   p[0] = [p.lexer.pattern_steps[s:e] for s, e in p.lexer.step_group_class]
      #   #print('Debug: p[0]={}'.format(p[0]))
      #   #print('Debug: step_group_class={}'.format(p.lexer.step_group_class))
      #   #print('Debug: group_pattern_offsets_group_list={}'.format(p.lexer.group_pattern_offsets_group_list))

      #   # reset the counter of step groups
      #   p.lexer.step_group_class = []
        
      #  # p.lexer.step_already_counted = 0 # FIXME
        

      # alternative groups
      if self.verbosity >2:
        print ('\tprocessing a step_group_class made of quantified_step_group_list alternatives')
        print ('\tremove the steps which were parts of alternatives= {}'.format(p.lexer.pattern_steps[p.lexer.step_group_class[0][0]:p.lexer.step_group_class[-1][1]]))
        print ('\tupdate quantified_step_index by decrementing it with len (parts of alternatives)+1')
        print ('\tsignal that this current step should be appended to pattern_steps (step_already_counted=0)')

      #  print('Debug: p_step_group wi len(p.lexer.step_group_class)={} !=1'.format(len(p.lexer.step_group_class)))
      #exit()
      
      # # add the current alternatives as a step
      # # FIXME this should be done in p_quantified_step_group
      # #p.lexer.pattern_steps.append([p.lexer.pattern_steps[s:e] for s, e in p.lexer.step_group_class])
      # p[0] = [p.lexer.pattern_steps[s:e] for s, e in p.lexer.step_group_class]
      # #if p[0] != None:
      # p.lexer.step_already_counted = 0

      # # we reset all the steps made by each step of each alternative group 
      
      # # print ('\tDebug: len(step_group_class)={} len(pattern_steps)={}'.format(len(p.lexer.step_group_class), len(p.lexer.pattern_steps)))
      # # print ('\tDebug: del from={} to={}'.format(p.lexer.step_group_class[0][0], p.lexer.step_group_class[-1][1]))
      # # remove the steps which were parts of alternatives 
      # # FIXME check when this is only a group but not alternatives
      # del p.lexer.pattern_steps[p.lexer.step_group_class[0][0]:p.lexer.step_group_class[-1][1]]
      
      # # update index
      # # +1 because the list of alternatives groups worthes as a group and a step
      # p.lexer.quantified_step_index -= (p.lexer.step_group_class[-1][1] - p.lexer.step_group_class[0][0]) 
      # p.lexer.quantified_step_index += 1
      
      # # declare the current step (list of alternative groups) as a group
      # if self.verbosity >2:
      #   print ('\tdeclare the current step (list of alternatives) as a group ; group_pattern_offsets_group_list.append =',[p.lexer.quantified_step_index -1,p.lexer.quantified_step_index])
      # p.lexer.group_pattern_offsets_group_list.append([p.lexer.quantified_step_index -1,p.lexer.quantified_step_index])

      # # reset the counter of step groups
      # p.lexer.step_group_class = [] 
      #   # print ('\tDebug: len(step_group_class)={} len(pattern_steps)={}'.format(len(p.lexer.step_group_class), len(p.lexer.pattern_steps)))
    print('\treturn p[0]={}'.format(p[0]))

# _______________________________________________________________
  def p_step_group_class(self,p):
    '''step_group_class : quantified_step_group_list
                        | step_group_class OR quantified_step_group_list'''
 #                       | step_group_class OR quantified_step_group'''   # HERE

    if len(p) == 2:
      self.log(p, '(step_group_class->quantified_step_group_list)')
      #print ('Debug: len(p[1])=',len(p[1]))

      if not(isinstance (p[1][0], list)):
        p[0]=[p[1]]
      else:
        p[0]=p[1]

      print('\tlen(p[0])=', len(p[0]))
      #poped = p.lexer.pattern_steps.pop()
      print('\tpop pattern_steps=',p.lexer.pattern_steps[len(p.lexer.pattern_steps)-len(p[0]):len(p.lexer.pattern_steps)])
      del (p.lexer.pattern_steps[len(p.lexer.pattern_steps)-len(p[0]):len(p.lexer.pattern_steps)])

    else:
      self.log(p, '(step_group_class->step_group_class OR quantified_step_group_list)') 
       #     self.log(p, '(step_group_class->step_group_class OR quantified_step_group)') # HERE
      print ('Debug: p[1] = {} ; len(p[0]) = {}'.format(p[1],len(p[1])))
      print ('Debug: p[3] = {} ; len(p[3]) = {}'.format(p[3],len(p[3])))

      if not(isinstance (p[1][0][0], list)):  # 2nd part of an alternative
        print ('Debug: 2nd part of an alternative')
        if not(isinstance (p[3][0], list)) or len(p[3]) == 1:                      # 2nd part has only one step
          print ('Debug: 2nd part has only one step')
          p[0] = [p[1], [p[3]]]                     
        else:                                   # 2nd part is a sequence of several steps
          print ('Debug: 2nd part is a sequence of several steps')
          p[0] = [p[1], p[3]] 
      else:                                   # 3rd and more parts of an alternative
        print ('Debug: 3rd and more parts of an alternative')
        p[1].append(p[3])                     
        p[0] = p[1]
      #poped = p.lexer.pattern_steps.pop()
      print('\tpop pattern_steps=',p.lexer.pattern_steps[len(p.lexer.pattern_steps)-len(p[3]):len(p.lexer.pattern_steps)])
      del (p.lexer.pattern_steps[len(p.lexer.pattern_steps)-len(p[3]):len(p.lexer.pattern_steps)])

    # store the current group 
    p.lexer.step_group_class.append([p.lexer.last_group_offsets_candidate[0],p.lexer.last_group_offsets_candidate[1]])
    
    if self.verbosity >2:
      print ('\tstore the current group offset from {} to {}'.format(p.lexer.last_group_offsets_candidate[0], p.lexer.last_group_offsets_candidate[1]))



    print('\treturn p[0]={}'.format(p[0]))
 

# _______________________________________________________________
  def p_step(self,p):
    '''step : single_constraint
            | LBRACKET constraint_class RBRACKET '''  # | NOT atomicconstraint # ajoute WARNING: 2 shift/reduce conflicts
    self.log(p, '(step->...)')


# _______________________________________________________________
  def p_constraint_class(self,p):
    '''constraint_class : constraint_class AND constraint_class_part
            | constraint_class OR constraint_class_part 
            | constraint_class_part ''' 
    if self.verbosity >1:
      self.log(p, '(constraint_class->...)')  
# _______________________________________________________________
  def p_constraint_class_part(self,p):
    '''constraint_class_part : single_constraint
                    | LPAREN constraint_class RPAREN  
                    | NOT constraint_class '''
    if self.verbosity >1:
      self.log(p, '(constraint_class_part->...)')  

# _______________________________________________________________
  def p_single_constraint(self,p):
    '''single_constraint : NAME EQ VALUE 
                          | NAME MATCH VALUE
                          | NAME IN VALUE'''
    if self.verbosity >1:
      self.log(p, '(single_constraint->...)')  

    # to avoid duplicate counting
    if self.verbosity >2:
      print ('\treset the step counter: step_already_counted=0')
    p.lexer.step_already_counted = 0

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


  def log(self, p, production):
    # Line Number and Position Tracking
    # http://www.dabeaz.com/ply/ply.html#ply_nn33

    # if self.verbosity >2:
    #   startlineleftsymbol, endlineleftsymbol = p.linespan(1)  # Start,end lines of the left expression
    #   startlinerightsymbol, endlinerightsymbol = p.linespan(len(p)-1)  # Start,end lines of the right expression
    #   # The lexspan() function only returns the range of values up to the start of the last pattern symbol.
    #   startpositionleftsymbol, endpositionleftsymbol = p.lexspan(1)   # Start,end positions of left expression
    #   startpositionrightsymbol, endpositionrightsymbol = p.lexspan(len(p)-1)   # Start,end positions of left expression
    #   symbolsconcat = ''
    #   lasti=0
    #   for i in range (len(p)):
    #     sp, ep = p.lexspan(i)
    #     symbolsconcat = symbolsconcat+'>'+str(p[i])+'['+str(sp)+':'+str(ep)+']<'
    #     lasti = i



      # print ('symbolsconcat=',symbolsconcat)
      # The current input text stored in the lexer.


      #print ('\tleftsymbol\t\trightsymbol\t|\t\tleftsymbol\t\trightsymbol')
      #print('startline=\t',startlineleftsymbol,'\t\t',startlinerightsymbol,'\t\t|\tstartposition=\t',startpositionleftsymbol,'\t\t',endpositionleftsymbol)
      #print('endline=\t',endlineleftsymbol,'\t\t',endlinerightsymbol,'\t\t|\tendposition=\t',startpositionrightsymbol,'\t\t',endpositionrightsymbol)

      # p.lexer.lexpos This attribute is an integer that contains the current position within the input text.
      # Within token rule functions, this points to the first character after the matched text.
      #print ('firstcharacter after matched text, lexpos=', p.lexer.lexpos)
      #print ('Debug: p.lexer.lexTokenEndDict[p.lexer.lexpos]=',p.lexer.lexTokenEndDict[p.lexer.lexpos])
      #lextok = p.lexer.lexTokenEndDict[p.lexer.lexpos]
      #print ('Debug: lextok.value=',lextok.value)
      #if p.lexer.lexpos > len(p.lexer.lexdata):
      #  previouslextokenendposition = len(p.lexer.lexdata)
      #else:
      #  previouslextokenendposition = p.lexer.lexpos - len(p.lexer.lexTokenEndDict[p.lexer.lexpos].value)
      #print ('previous lextoken end position=', previouslextokenendposition)

      # This is the raw Match object returned by the Python re.match() function (used internally by PLY) for the current token 
      # print ('p.lexer.lexmatch=', p.lexer.lexmatch) 

      #print('p.lexdata[startpositionleftsymbol:endpositionrightsymbol]=',p.lexer.lexdata[startpositionleftsymbol:endpositionrightsymbol])
      #print('p.lexdata[startpositionleftsymbol:lexpos]=>',p.lexer.lexdata[startpositionleftsymbol:p.lexer.lexpos],'<')
      #print('p.lexdata[startpositionleftsymbol:previouslextokenendposition]=>',p.lexer.lexdata[startpositionleftsymbol:previouslextokenendposition],'<')

    step_start, step_end = get_current_pattern_step_offsets(p) 
    step = get_current_pattern_step(p, step_start, step_end)
    if self.verbosity >1:
      print ('  Production=', production, step)

    if self.verbosity >3:
      print ('      Whole pattern/lexdata=', p.lexer.lexdata, '; len(lexdata)=', len(p.lexer.lexdata))
      print ('      # of lexical tokens in the current production rule=', len(p))




# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING ERROR HANDLING
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def p_error(self,p):
    if not p:
      if self.verbosity >2: 
        print(2*'  ',"Info: pattern syntaxically parsed.")
      return

      # http://www.dabeaz.com/ply/ply.html#ply_nn26 6.8.2
      # Read ahead looking for a closing ';'
    if self.verbosity >0: 
      print ('Error: syntactic parsing error - unexpected token type="{}" with value="{}" at position {}. Search an error before this point.'.format(p.type, p.value, p.lexer.lexpos))
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
  m = SyntacticPatternParser(tokens=l.tokens, verbosity =2, start='expression')

  # try it out
  # print ("Copy the grammar line without 'Grammar: ' (whitespace should not been included); The semi-colon ';' will lead to a parsing error")
  # while True:
  #   try:
  #     #text2parse
  #     s = input('cl > ')   # Use raw_input on Python 2
  #   except EOFError:
  #     break
  #   m.parser.parse(s, l.lexer, tracking=True)


