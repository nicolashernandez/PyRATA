# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ply.yacc as yacc
from pyrata_lexer import *

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Parser(object):

  #self.tokens = self.lex.tokens
  #tokens = ()
  debug = False
  
  precedence = (
    ('left',  'OR'),
    ('left', 'AND'),
   # ('left', 'LBRACKET','RBRACKET'),    
    ('left', 'LPAREN','RPAREN'),
    ('right', 'NOT'),
    ('left', 'IS'),
#  ('right', 'OPTION', 'ANY', 'ATLEASTONE')
  )


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING METHODS
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



# _______________________________________________________________
  def p_expression(self,p):
    '''expression : quantifiedstep 
                  | quantifiedstep expression'''

    if len(p) == 2:
      p[0] = p[1]
      self.log(p, '(expression->quantifiedstep)')
    else:
      if self.debug: print ("\tDebug: p[1]=", p[1], "p[2]=",p[2])
      p[0] = p[2]
      self.log(p, '(expression->quantifiedstep expression)')

    p.lexer.expressionresult = p[0]

    if self.debug: print ('\treturn=',p[0])    

    # at this point, if p[0] and p.lexer.matchongoing means that a whole pattern has been recognized
    # so we store the end position of the recognized structure 
    # and we set the the next first at the end of the current match
    if p[0]: # and p.lexer.matchongoing:
      p.lexer.matchongoing = False
      p.lexer.groupendindex.append(p.lexer.currentExploredDataPosition)
      p.lexer.lastFirstExploredDataPosition=p.lexer.currentExploredDataPosition
      if self.debug: print ("\tDebug: we store the end position of the current match and set the next token position at the end of the current match")
    else: #if not(p[0]) and p.lexer.matchongoing:
      """TODO remove start"""
      p.lexer.lastFirstExploredDataPosition += 1
      p.lexer.currentExploredDataPosition = p.lexer.lastFirstExploredDataPosition
      if self.debug: print ("\tDebug: we set the next token position at the lastFirstExploredDataPosition+1")
    # if   
    #if p[0]:
    #  p.lexer.lastFirstExploredDataPosition=p.lexer.currentExploredDataPosition
    #else:
    #  p.lexer.lastFirstExploredDataPosition += 1
    #  p.lexer.currentExploredDataPosition = p.lexer.lastFirstExploredDataPosition
    #if self.debug: print ('\tDebug: len(featStrList):',len(p.lexer.data),'lastFirstExploredDataPosition',p.lexer.lastFirstExploredDataPosition)
    # findall mode

    ''' if some data remains to explore'''
    if  p.lexer.lastFirstExploredDataPosition < len(p.lexer.data):
      # and if none match so far or re mode is findall
      if not (p[0]) or p.lexer.re == 'findall': 
        if self.debug: print ("Context: dataPosition=",p.lexer.currentExploredDataPosition,"; dataToken=",p.lexer.data[p.lexer.currentExploredDataPosition], '; lexpos=',p.lexer.lexpos)
        if self.debug: print ('\tDebug: some data remains to explore and (not matched yet or re mode is "findall") we relaunch the grammar parser')
#      #self.parser.restart()
#      #self.parser = yacc.yacc(module=self) #start='expression',
        self.parser.parse(p.lexer.grammar, p.lexer, tracking=True)
      else:
        if self.debug: print ('\tDebug: some data remains to explore but already match something')
    else:
      if self.debug: print ('\tDebug: no more data to explore')




# _______________________________________________________________
  def p_quantifiedstep(self,p):
    '''quantifiedstep : step 
            | OPTION step
            | ATLEASTONE step 
            | ANY step''' 
    # get the grammar span where is depicted the current parsed global step
    starti,endi = p.lexspan(1)   # Start,end positions of left expression
    p.lexer.globalgrammarstep = p.lexer.grammar[starti:p.lexer.lexpos-1]

    if len(p) == 2:
      ''' the current step is wo quantifier'''
      p[0]=p[1]
      #if self.debug: 
      #  print ("\t\t(...->step)")
      self.log(p, '(quantifiedstep->step)')

      if p[0] and not(p.lexer.islocal):
        p.lexer.currentExploredDataPosition +=1
      # FIXME have a look at the p_expression 
  #     elif not (p[0]) and not (p.lexer.islocal):
  #       # if the current global step is False it abords the parsing, moves in the data to explore, and restart the parsing
  #       p.lexer.lastFirstExploredDataPosition += 1
  #       p.lexer.currentExploredDataPosition = p.lexer.lastFirstExploredDataPosition
  #     # if some data remains to explore
  # #     if  p.lexer.lastFirstExploredDataPosition < len(p.lexer.data):
  #       # and if none match so far or re mode is findall
  #       if not (p[0]) or p.lexer.re == 'findall': 
  #         if self.debug: print ("Context: dataPosition=",p.lexer.currentExploredDataPosition,"; dataToken=",p.lexer.data[p.lexer.currentExploredDataPosition], '; lexpos=',p.lexer.lexpos)
  #         if self.debug: print ('\tDebug: some data remains to explore and (not matched yet or re mode is "findall") we relaunch the grammar parser')
  # #      #self.parser.restart()
  # #      #self.parser = yacc.yacc(module=self) #start='expression',
  #         self.parser.parse(p.lexer.grammar, p.lexer, tracking=True)
  #       else:
  #         if self.debug: print ('\tDebug: some data remains to explore but already match something')
  #     else:
  #       if self.debug: print ('\tDebug: no more data to explore')


      if p.lexer.islocal: 
        if self.debug: print ("\tDebug: stop processing a (local) step grammar")
        p.lexer.islocal = False  
        p.lexer.localresult = p[0]
    else:
      #if self.debug: print ("\t\t(...->",p[1],"step)")
      self.log(p, '(quantifiedstep-> ' + p[1] + ' step)')
      #print ("Debug: symbol on the stack that appears immediately to the left=",p[-1])
      if p[1] == '?':
        '''in any case we move to the next token '''
        if self.debug: print ("\tTODO process semantics of quantifier ?")
        if not(p.lexer.islocal):
          p.lexer.currentExploredDataPosition +=1
          if self.debug: print ("\tDebug: p.lexer.currentStepCursor=",(p.lexer.currentExploredDataPosition-1),'; inc(p.lexer.currentStepCursor) ; token=',p.lexer.data[p.lexer.currentExploredDataPosition])
      elif p[1] == '+':
        if self.debug: print ("\tDebug: process semantics of quantifier +")
        if p[2]:
          #print ("\tDebug: p.parser=",p.parser)
          #print ("\tDebug: p.lexer=",p.lexer)
         
          #print ("p.lexer.grammar:",p.lexer.grammar)
          localLexer = Lexer(grammar=p.lexer.grammarstep, data=p.lexer.data)  # p.lexer.data)
          localLexer.lexer.localresult = True
          localLexer.lexer.currentExploredDataPosition = p.lexer.currentExploredDataPosition 
          localgrammarstepparsingiter = 0
          #print ('Debug: before loop - data=', p.lexer.data, '; len(data)=',len(p.lexer.data), '; position=',localLexer.lexer.currentExploredDataPosition) 
          if self.debug: print("Debug: call localparser on step grammar=",p.lexer.grammarstep)
          if self.debug: print('\tDebug: p.lexer.lexpos=',p.lexer.lexpos)
          
          ''' pre: the first step of the quantifier is true, we now explore if more tokens valid the grammar step'''
          localLexer.lexer.currentExploredDataPosition += 1
          while (localLexer.lexer.localresult and (localLexer.lexer.currentExploredDataPosition < len(p.lexer.data))):
            if self.debug: print ("\tDebug: start processing a (local) step grammar ; iteration=",localgrammarstepparsingiter)
            
            #print ('Debug: in loop - data=', p.lexer.data, '; len(data)=',len(p.lexer.data), '; position=',localLexer.lexer.currentExploredDataPosition)
            if self.debug:
              print ("\tDebug: len(p.lexer.data)=",len(p.lexer.data),"; inc(currentExploredDataPosition) ; currentExploredDataPosition=",localLexer.lexer.currentExploredDataPosition)
              print ("\tDebug: futuretoken=",p.lexer.data[localLexer.lexer.currentExploredDataPosition])
            localLexer.lexer.islocal = True
  #          locallexer = lex.lex()
  #          locallexer.islocal = True
  #          locallexer.localresult = ''
            localLexer.lexer.grammarstep = p.lexer.grammarstep
  #          locallexer.currentExploredDataPosition = p.lexer.currentExploredDataPosition
            #localparser = yacc.yacc()
            #localparser.parse(p.lexer.grammarstep,lexer=lexer, tracking=True) #,start='expression'
            
            localParser = Parser(tokens=localLexer.tokens, debug=self.debug, start='quantifiedstep') # Set Add True for debugging
            localParser.parser.parse(localLexer.lexer.grammarstep, localLexer.lexer) #, tracking=True)
            #localparser.parse(p.lexer.grammarstep,lexer=locallexer) #,start='expression'
            #print ("\tDebug: localparser.parser=",localParser.parser)
            
            if self.debug: print ("\tDebug: localLexer.lexer.localresult=",localLexer.lexer.localresult)
            localgrammarstepparsingiter += 1
            localLexer.lexer.currentExploredDataPosition += 1

          if self.debug: print("Debug: resume the global parser")          
          if self.debug: print ('\tDebug: localparser result=',localLexer.lexer.localresult)
          if not(localLexer.lexer.localresult): 
            if self.debug: print("Debug: since the last step grammar was False we decrement currentExploredDataPosition")
            localLexer.lexer.currentExploredDataPosition -=1
          localLexer.lexer.islocal = False
          #print ('\tDebug: localparser result=',locallexer.localresult)
          if self.debug: print ("\tDebug: + quantifier goes until the dataPosition=",localLexer.lexer.currentExploredDataPosition) #,'; token=',p.lexer.data[localLexer.lexer.currentExploredDataPosition])
          # TODO for '+' operator p.lexer.currentExploredDataPosition > localLexer.lexer.currentExploredDataPosition -1 otherwise the pattern is not matched
          p.lexer.currentExploredDataPosition = localLexer.lexer.currentExploredDataPosition #-1
         # if self.debug: print ("\tDebug: future dataPosition=",(p.lexer.currentExploredDataPosition),'; token=',p.lexer.data[p.lexer.currentExploredDataPosition])

          if self.debug: print('\tDebug: localLexer.lexer.lexpos=',localLexer.lexer.lexpos)

          if self.debug: print('\tDebug: p.lexer.lexpos=',p.lexer.lexpos)
          #print ("\tDebug: p.parser=",p.parser)
          #print ("\tDebug: p.lexer=",p.lexer)
          #parser.restart()
          p[0] = True
        else:
          # TODO #else: error, il faut passer à initial+1 et faire un restart du parseur sur la grammaire principale (si une seule règle)
          # ou bien rester sur initial et tester les autres règles et quand plus de règles passer à initial+1 et faire un parser.restart

          p[0] = False
      elif p[1] == '*':
        if self.debug: print ("\tTODO process semantics of quantifier *")
      p[0]=p[2]
    #if self.debug: print ('\treturn=',p[0])    

    # to log the parsing of the grammar
    p.lexer.globalgrammarstepPosition += 1

# _______________________________________________________________
  def p_step(self,p):
    '''step : atomicconstraint
            | NOT step
            | LBRACKET classconstraint RBRACKET '''  # | NOT atomicconstraint # ajoute WARNING: 2 shift/reduce conflicts
    if len(p) == 2:
      self.log(p, '(step->atomicconstraint)')
      p[0] = p[1]
      if p.lexer.islocal:
        if self.debug: print ("\tDebug: processing a (local) step grammar")
  #      p.lexer.islocal = False
  #      p.lexer.localresult = p[0]
      else:
        start,end = p.linespan(1)    # Start,end lines of the right expression
        starti,endi = p.lexspan(1)   # Start,end positions of right expression
        # check the character offset of the step grammar
        #if self.debug: print ("\tDebug: startLine=",start,"endLine=",end)
        #if self.debug: print ("\tDebug: startChar=",starti,"endChar=",endi, " step grammar=",p.lexer.grammar[starti:endi])
        if self.debug: print ("\tDebug: startChar=",starti,"; endChar=p.lexer.lexpos-1 i.e.",(p.lexer.lexpos-1), "; step grammar=", p.lexer.grammar[starti:p.lexer.lexpos-1])
        p.lexer.grammarstep = p.lexer.grammar[starti:p.lexer.lexpos-1]
    elif p[1] == '!':
      p[0] = not(p[2])
      self.log(p, '(step->NOT step)')
      if p.lexer.islocal:
        if self.debug: print ("\tDebug: processing a (local) step grammar")
  #      p.lexer.islocal = False
  #      p.lexer.localresult = p[0]
      else:
        start,end = p.linespan(1)    # Start,end lines of the right expression
        startFirst,endFirst = p.lexspan(1)   # Start,end positions of right expression
        startLast,endLast = p.lexspan(2)   # Start,end positions of right expression
        # check the character offset of the step grammar
        #if self.debug: print ("\tDebug: startLine=",start,"endLine=",end)
        #if self.debug: print ("\tDebug: startChar=",startFirst,"endChar=",endLast, "step grammar=",p.lexer.grammar[startFirst:endLast])
        if self.debug: print ("\tDebug: startChar=",startFirst,"; endChar=p.lexer.lexpos-1 i.e.",(p.lexer.lexpos-1), "; step grammar=", p.lexer.grammar[startFirst:p.lexer.lexpos-1])
        
        p.lexer.grammarstep = p.lexer.grammar[startFirst:p.lexer.lexpos-1]

    else:
      p[0] = p[2]
      self.log(p, '(step->LBRACKET classconstraint RBRACKET)')
      if p.lexer.islocal:
        if self.debug: print ("\tDebug: processing a (local) step grammar")
  #      p.lexer.islocal = False
  #      p.lexer.localresult = p[0]
      else:
        start,end = p.linespan(1)    # Start,end lines of the right expression
        startFirst,endFirst = p.lexspan(1)   # Start,end positions of right expression
        startLast,endLast = p.lexspan(3)   # Start,end positions of right expression
        # check the character offset of the step grammar
        #if self.debug: print ("\tDebug: startLine=",start,"endLine=",end)
        #if self.debug: print ("\tDebug: startChar=",startFirst,"endChar=",endLast, "step grammar=",p.lexer.grammar[startFirst:endLast])
        if self.debug: print ("\tDebug: startChar=",startFirst,"; endChar=p.lexer.lexpos-1 i.e.",(p.lexer.lexpos-1), "; step grammar=", p.lexer.grammar[startFirst:p.lexer.lexpos-1])
        
        p.lexer.grammarstep = p.lexer.grammar[startFirst:p.lexer.lexpos-1]

    if p[0] and not(p.lexer.matchongoing) and not (p.lexer.islocal): # do not need to store start position when it is a step grammar since it has alread been stored
      ''' this is the first step of a pattern'''
      if self.debug: print ("\tDebug: we store the start position of the current match")
      p.lexer.matchongoing = True
      p.lexer.groupstartindex.append(p.lexer.currentExploredDataPosition)

# _______________________________________________________________
  def p_classconstraint(self,p):
    '''classconstraint : partofclassconstraint 
            | partofclassconstraint AND classconstraint
            | partofclassconstraint OR classconstraint '''

    if len(p) == 2:
      p[0] = p[1]
      self.log(p, '(classconstraint->partofclassconstraint)')
    
    else:
      if p[2] == '&':
        p[0] = p[1] and p[3]
        self.log(p, '(classconstraint->partofclassconstraint AND classconstraint)')

      else: 
        p[0] = p[1] or p[3]
        self.log(p, '(classconstraint->partofclassconstraint OR classconstraint)')

    if p.lexer.islocal:
      if self.debug: print ("\tDebug: processing a (local) step grammar")


# _______________________________________________________________
  def p_partofclassconstraint(self,p):
    '''partofclassconstraint : atomicconstraint
                    | LPAREN classconstraint RPAREN  
                    | NOT classconstraint '''
    #if lexer.atleastone:
    #  p.lexer.lexpos = lexer.lastTokenPosition
    # the position is changed but not the value of p...
    #  p.lexer.pop_state() 
    if p[1] == '(':
      p[0] = p[2]
      self.log(p, '(partofclassconstraint->LPAREN classconstraint RPAREN)')
    
    elif p[1] == '!':
      p[0] = not(p[2])
      self.log(p, '(partofclassconstraint->NOT classconstraint)')
    
    else:
      p[0] = p[1]
      self.log(p, '(partofclassconstraint->atomicconstraint)')

    if p.lexer.islocal:
      if self.debug: print ("\tDebug: processing a (local) step grammar")

# _______________________________________________________________
  def p_atomicconstraint(self,p):
    '''atomicconstraint : NAME IS VALUE '''

    attName=p[1]
    attValue=p[3][1:-1]
    p[0] = (p.lexer.data[p.lexer.currentExploredDataPosition][attName] == attValue)
    self.log(p, '(atomicconstraint->NAME IS VALUE: ' + attName + ' is ' +attValue +')')

    if p.lexer.islocal:
      if self.debug: print ("\tDebug: processing a (local) step grammar")


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def moreAboutProduction(self,p):
  # see doc/internal.html 3. productions
    #print ('Debug: p.name=',p.name,'p.prod=',p.prod,'p.number=',p.number,'p.usyms=',p.usyms,,'p.lr_items=',p.lr_items
    if self.debug: print('p.lineno=',p.lineno)

  # debug (p, "(quantifiedstep->step)")
  def log(self, p, production):
    if self.debug:
      print ('________________________________________________')
      print ('Production=',production)
      if p.lexer.globalgrammarstepPosition < p.lexer.grammarsize:
        print ("Grammar: cursor-position=",p.lexer.globalgrammarstepPosition,"; globalGrammarStep=",p.lexer.globalgrammarstep)
      else:
        print ("Grammar: cursor-position=",p.lexer.globalgrammarstepPosition,"; globalGrammarStep=no-more")
      if p.lexer.currentExploredDataPosition < len(p.lexer.data):
        print ("Data:\t cursor-position=",p.lexer.currentExploredDataPosition,"; dataToken=",p.lexer.data[p.lexer.currentExploredDataPosition])
      else:
        print ("Data:\t cursor-position=",p.lexer.currentExploredDataPosition,"; dataToken=no-more")

      print ('Return=',p[0])
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING ERROR HANDLING
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def p_error(self,p):
    if not p:
      print("Info: End of Grammar File.")
      return

      # http://www.dabeaz.com/ply/ply.html#ply_nn26 6.8.2
      # Read ahead looking for a closing ';'
    print ("Parsing error: found token type=",p.type, " with value=",p.value,"but not expected")
    while True:
      tok = parser.token()             # Get the next token
  #      if not tok or tok.type == 'EOI': 
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

    self.debug = False
    if 'debug' in kwargs.keys(): # MANDATORY
      self.debug = kwargs['debug']
    kwargs.pop('debug', None)

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
    start='expression'
    if 'start' in kwargs.keys(): # MANDATORY
      start = kwargs['start'] 
    kwargs.pop('start', None)      
    self.parser = yacc.yacc(module=self,  start=start, **kwargs) #

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  MAIN
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# example use:
if __name__ == '__main__':
  #Parser("").test_from_console_input()
  pattern='?lem:"the" +pos:"JJ" [pos:"NN" & (lem:"car" | !lem:"bike" | !(lem:"bike"))] [raw:"is" | raw:"are"]\n'
  #grammar='+pos:"JJ" pos:"NN"'
  print ('Grammar:', pattern)

  data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'blue', 'lem':'blue', 'pos':'JJ'}]     
  data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
  print ('Data:', data)

  pattern = 'pos:"NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}]

  # Build the parser and 
  l = Lexer(grammar=pattern, data=data) 
  m = Parser(tokens=l.tokens, debug=True, start='expression')

  # try it out
  print ("Copy the grammar line without 'Grammar: ' (whitespace should not been included); The semi-colon ';' will lead to a parsing error")
  while True:
    try:
      #text2parse
      s = input('cl > ')   # Use raw_input on Python 2
    except EOFError:
      break
    m.parser.parse(s, l.lexer, tracking=True)


