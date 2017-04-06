# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# The current parser is used to compile pattern to recognize
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ply.yacc as yacc
from pyrata.lexer import *

import re



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# verbosity  (0 None 1 global 2 verbose) 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class SyntacticPatternParser(object):

  verbosity  = 0 # degree of verbosity
  
  #quantified_step_list_counter = 0
  #quantified_step_counter = 0

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
       expression : quantified_step_group_list'''

    p.lexer.group_pattern_offsets_group_list.append([0, len(p.lexer.pattern_steps)])  
    
    if self.verbosity >1:
      self.log(p, '(expression->...)')

    if self.verbosity >2:  
      print ('  ','Syntactic structure parsed: {}'.format(p.lexer.pattern_steps))
      print ('Debug: group_pattern_offsets_group_list=',p.lexer.group_pattern_offsets_group_list)
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
      print ('Ordered group_pattern_offsets_group_list=',p.lexer.group_pattern_offsets_group_list)
      for i, (a, b) in enumerate(p.lexer.group_pattern_offsets_group_list):
        print ('group {} = {}'.format(i, p.lexer.pattern_steps[a:b]))

# _______________________________________________________________
  def p_quantified_step_group_list(self, p): 
    ''' quantified_step_group_list : quantified_step_group_list quantified_step_group
                             | quantified_step_group   '''
    if self.verbosity >1:
      self.setPatternStep(p)
      if len(p) == 2:
        self.log(p, '(p_quantified_step_group_list->quantified_step_group)')
      elif len(p) == 3:
        self.log(p, '(p_quantified_step_group_list->p_quantified_step_group_list quantified_step_group)')

    # get the start and the end of the part of the pattern recognized by the current rule 
    startpositionleftsymbol, endpositionleftsymbol = p.lexspan(1)
    if p.lexer.lexpos > len(p.lexer.lexdata):
      previouslextokenendposition = len(p.lexer.lexdata)
    else:
      previouslextokenendposition = p.lexer.lexpos - len(p.lexer.lexTokenEndDict[p.lexer.lexpos].value)

    # store the last couple of quantified step position which delimits a group candidate
    #print ('   Debug: p_quantified_step_group_list - lexdata from {} to {}'.format(startpositionleftsymbol, previouslextokenendposition))    
    if startpositionleftsymbol in p.lexer.quantified_step_start: # and previouslextokenendposition in p.lexer.quantified_step_end:
      #p.lexer.last_group_offsets_candidate = [p.lexer.quantified_step_start[startpositionleftsymbol],p.lexer.quantified_step_end[previouslextokenendposition]]    
      p.lexer.last_group_offsets_candidate = [p.lexer.quantified_step_start[startpositionleftsymbol],p.lexer.quantified_step_index]    
      if self.verbosity >2:
        print ('   Debug: p_quantified_step_group_list - set last_group_offsets_candidate wi lexdata from {} to {}'.format(startpositionleftsymbol, previouslextokenendposition))    
    else:
      if self.verbosity >2:
        print ('   Debug: p_quantified_step_group_list - do not set last_group_offsets_candidate wi lexdata from {} to {}'.format(startpositionleftsymbol, previouslextokenendposition))    

# _______________________________________________________________
  def p_quantified_step_group(self, p): 
    ''' quantified_step_group : quantified_step
                    | LPAREN quantified_step_group_list RPAREN   '''
    if self.verbosity >1:
      self.setPatternStep(p)
      if len(p) == 2:
        self.log(p, '(quantified_step_group->quantified_step)')
      else:
        self.log(p, '(quantified_step_group->LPAREN p_quantified_step_group_list RPAREN)')
        #p.lexer.group_pattern_offsets_group_list.append([p.lexer.last_group_offsets_candidate[0],p.lexer.last_group_offsets_candidate[1]])
  
    # the rule which recognize a group matches so we definitively store the last couple of quantified step position as a group (at least for the first position)
    if len(p) == 4:    
      p.lexer.group_pattern_offsets_group_list.append([p.lexer.last_group_offsets_candidate[0],p.lexer.quantified_step_index])
      if self.verbosity >2:
        print ('      group detected from {} to {}'.format(p.lexer.last_group_offsets_candidate[0],p.lexer.last_group_offsets_candidate[1]))
        

# _______________________________________________________________
  def p_quantified_step(self, p):
    '''quantified_step : step 
            | step OPTION
            | step ATLEASTONE 
            | step ANY 
            ''' 

    if len(p) == 2:
      p.lexer.pattern_steps.append([None, p[1]])
    elif p[2] == '*':
      p.lexer.pattern_steps.append(['*', p[1]])
    elif p[2] == '+':
      p.lexer.pattern_steps.append(['+', p[1]])
    elif p[2] == '?':  
      p.lexer.pattern_steps.append(['?', p[1]])
#    else:
#      print ('Debug: LPAREN quantified_step_list RPAREN from {} to {}'.format())

    if self.verbosity >1:
      self.setPatternStep(p)  
      if len(p) == 2:
        self.log(p, '(p_quantified_step->step)')
      elif len(p) == 3:
        self.log(p, '(p_quantified_step->step QUANTIFIER)')

    # get the start and the end of the part of the pattern recognized by the current rule 
    startpositionleftsymbol, endpositionleftsymbol = p.lexspan(1)
    if p.lexer.lexpos > len(p.lexer.lexdata):
      previouslextokenendposition = len(p.lexer.lexdata)
    else:
      previouslextokenendposition = p.lexer.lexpos - len(p.lexer.lexTokenEndDict[p.lexer.lexpos].value)

    # store the corresponding quantified step at the character position start and end 
    p.lexer.quantified_step_start[startpositionleftsymbol] = p.lexer.quantified_step_index
    p.lexer.quantified_step_end[previouslextokenendposition] = p.lexer.quantified_step_index +1
    p.lexer.quantified_step_index += 1
    if self.verbosity >2:
      print ('   Debug: p_quantified_step - lexdata from {} to {}'.format(startpositionleftsymbol, previouslextokenendposition))

  
# _______________________________________________________________
  def p_step(self,p):
    '''step : atomicconstraint
            | NOT step
            | LBRACKET classconstraint RBRACKET '''  # | NOT atomicconstraint # ajoute WARNING: 2 shift/reduce conflicts
    self.setPatternStep(p)    
    p[0] = p.lexer.patternStep
    self.log(p, '(p_step->...)')

# _______________________________________________________________
  def p_classconstraint(self,p):
    '''classconstraint : classconstraint AND partofclassconstraint
            | classconstraint OR partofclassconstraint 
            | partofclassconstraint ''' 
    if self.verbosity >1:
      self.setPatternStep(p)
      self.log(p, '(p_classconstraint->...)')  
# _______________________________________________________________
  def p_partofclassconstraint(self,p):
    '''partofclassconstraint : atomicconstraint
                    | LPAREN classconstraint RPAREN  
                    | NOT classconstraint '''
    if self.verbosity >1:
      self.setPatternStep(p)
      self.log(p, '(p_partofclassconstraint->...)')  

# _______________________________________________________________
  def p_atomicconstraint(self,p):
    '''atomicconstraint : NAME EQ VALUE 
                          | NAME MATCH VALUE
                          | NAME IN VALUE'''
    if self.verbosity >1:
      self.setPatternStep(p)
      self.log(p, '(p_atomicconstraint->...)')  

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

    if self.verbosity >1:
      print ('  Production=', production, p.lexer.patternStep)

    if self.verbosity >3:
      print ('      Whole pattern/lexdata=', p.lexer.lexdata, '; len(lexdata)=', len(p.lexer.lexdata))
      print ('      # of lexical tokens in the current production rule=', len(p))

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  def setPatternStep(self,p):
    ''' Line Number and Position Tracking'''
    # http://www.dabeaz.com/ply/ply.html#ply_nn33
    startpositionleftsymbol, endpositionleftsymbol = p.lexspan(1)
    if self.verbosity >3: 
      print (3*'  ','setPatternStep: p.lexer.lexpos=',p.lexer.lexpos,'; isInLexTokenEndDict=',(p.lexer.lexpos in p.lexer.lexTokenEndDict))
    if p.lexer.lexpos > len(p.lexer.lexdata):
      previouslextokenendposition = len(p.lexer.lexdata)
    else:
      previouslextokenendposition = p.lexer.lexpos - len(p.lexer.lexTokenEndDict[p.lexer.lexpos].value)
    #print ('Debug: lexdata from {} to {}'.format(startpositionleftsymbol, previouslextokenendposition))
    p.lexer.patternStep = p.lexer.lexdata[startpositionleftsymbol:previouslextokenendposition]



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


