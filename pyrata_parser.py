# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ply.yacc as yacc
from pyrata_lexer import *

import re

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# verbosity  (0 None 1 global 2 verbose) 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Parser(object):

  #self.tokens = self.lex.tokens
  #tokens = ()
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
  # def p_statement(self,p):
  #   '''statement : expression '''
  #   p[0] = p[1]
  #   self.log(p, '(statement->expression)')
# _______________________________________________________________
  def p_expression(self,p):
    '''expression : quantifiedstep expression
                  | quantifiedstep '''
    self.setPatternStep(p)

    if len(p) == 2:
      p[0] = p[1]
      self.log(p, '(expression->quantifiedstep)')
    else:
      p[0] = p[2]
      self.log(p, '(expression->quantifiedstep expression)')

    p.lexer.expressionresult = p[0]


    # at this point, if p[0] and p.lexer.matchongoing means that a whole pattern has been recognized
    # so we store the end position of the recognized structure 
    # and we move the cursor at the next first at the end of the current match
    ''' the whole expression has been successfully recognized '''
    if p[0]:
      if p.lexer.matchongoing:
        if self.verbosity >2: print ("\tDebug: matchongoing ; currentExploredDataPosition=",p.lexer.currentExploredDataPosition)
        p.lexer.matchongoing = False
      #  print ("Debug: len(l.lexer.groupstartindex):", len(p.lexer.groupstartindex), "; l.lexer.groupstartindex=",p.lexer.groupstartindex)
      #  print ("Debug: len(l.lexer.groupendindex):", len(p.lexer.groupendindex), "; l.lexer.groupendindex=",p.lexer.groupendindex)
      #print ("Debug: p.lexer.patternStep:", p.lexer.patternStep, "; p.lexer.lexdata=",p.lexer.lexdata)
      #if p.lexer.patternStep.strip() == p.lexer.lexdata.strip():
        

      p.lexer.groupendindex.append(p.lexer.currentExploredDataPosition) # FIXME quand j'indente je tombe dans une infinite loop
      p.lexer.lastFirstExploredDataPosition=p.lexer.currentExploredDataPosition

      if self.verbosity >2: print ("\tDebug: we store the end position of the current match and set the next token position at the end of the current match")
      #else:
      #  if self.verbosity >2: print ("\tDebug: we already stored the end position of the current match and set the next token position at the end of the current match")

     # and p.lexer.matchongoing:
      #p.lexer.matchongoing = False
      #p.lexer.groupendindex.append(p.lexer.currentExploredDataPosition)
      #p.lexer.lastFirstExploredDataPosition=p.lexer.currentExploredDataPosition
      #if self.verbosity >2: print ("\tDebug: we store the end position of the current match and set the next token position at the end of the current match")
    else: #if not(p[0]) and p.lexer.matchongoing:
      ''' the recognition of the expression has failed so we only the cursor of 1 data token'''
      p.lexer.lastFirstExploredDataPosition += 1
      p.lexer.currentExploredDataPosition = p.lexer.lastFirstExploredDataPosition
      if self.verbosity >2: print ("\tDebug: we set the next token position at the lastFirstExploredDataPosition+1")
    # if   
    #if p[0]:
    #  p.lexer.lastFirstExploredDataPosition=p.lexer.currentExploredDataPosition
    #else:
    #  p.lexer.lastFirstExploredDataPosition += 1
    #  p.lexer.currentExploredDataPosition = p.lexer.lastFirstExploredDataPosition
    #if self.verbosity >2: print ('\tDebug: len(featStrList):',len(p.lexer.data),'lastFirstExploredDataPosition',p.lexer.lastFirstExploredDataPosition)
    # findall mode

    ''' if some data remains to explore'''
    if  p.lexer.lastFirstExploredDataPosition < len(p.lexer.data):
      '''and if (none match so far and re mode is 'search') or (re mode is findall)
          then we relaunch the parser at the current location '''
      #if not (p[0]) or p.lexer.re == 'findall':
      if len(p.lexer.groupendindex) ==0 or p.lexer.re == 'findall': 
      # si la liste est non vide alors on a matché qqch 
        if self.verbosity >2: print ("\tContext: dataPosition=", p.lexer.currentExploredDataPosition,"; dataToken=",p.lexer.data[p.lexer.currentExploredDataPosition], '; lexpos=',p.lexer.lexpos)
        if self.verbosity >2: print ('\tDebug: some data remains to explore and (not matched yet or re mode is "findall") we relaunch the pattern parser')
        p.lexer.patternStepPosition = 0
        self.parser.parse(p.lexer.lexdata, p.lexer, tracking=True) # .grammar
      else:
        if self.verbosity >2: print ('\tDebug: some data remains to explore but already match something')
        while True:
          tok = p.parser.token()             # Get the next token
          if not tok: 
            break
    else:
      if self.verbosity >2: print ('\tDebug: no more data to explore')




# _______________________________________________________________
  def p_quantifiedstep(self,p):
    '''quantifiedstep : step 
            | OPTION step
            | ATLEASTONE step 
            | ANY step''' 
    self.setPatternStep(p)

    if len(p) == 2:
      ''' the current step is wo quantifier'''
      p[0]=p[1]
      #if self.verbosity >2: 
      #  print ("\t\t(...->step)")
      self.log(p, '(quantifiedstep->step)')

      if p[0] and not(p.lexer.islocal):
        p.lexer.currentExploredDataPosition +=1
        if self.verbosity >2: 
          print ('\tDebug: the current pattern step has been recognized so we move to the next data token ; currentExploredDataPosition=',p.lexer.currentExploredDataPosition )
        if  p.lexer.currentExploredDataPosition >= len(p.lexer.data):
          if self.verbosity >2: 
            print ('\tDebug: the parsing of a pattern is on going (True so far) but no more data remains to explore ; we empty the parser buffer')
          while True:
            tok = p.parser.token()             # Get the next token
            #print ("Debug: p[0] and not(p.lexer.islocal) - p.parser.token()")
            if not tok: 
              #tok = p.parser.token() 
              break

    else:      
      #print ("Debug: symbol on the stack that appears immediately to the left=",p[-1])
      if p[1] == '?':
        '''gram ab?c recognizes abc or ac ; 
           when pattern step b is true we move forward in terms of data cursor ; we always move the pattern step''' 
        p[0] = p[2]
        self.log(p, '(quantifiedstep-> ' + p[1] + 'step)')
        #if not(p.lexer.islocal): when processing local step we never go to the quantified step so, this should not be called here
        if p[0]:
          p.lexer.currentExploredDataPosition +=1
        #else:
        #  p.lexer.matchongoing = False  
        if self.verbosity >2: 
          if p[0]:
            print ('\tDebug: Since we recognized the token, we move to the next data token ; currentExploredDataPosition=',p.lexer.currentExploredDataPosition)
          else:
            print ('\tDebug: We did not recognized the token, so we wont move to the next data token ; currentExploredDataPosition=',p.lexer.currentExploredDataPosition)
        p[0] = True 
        if self.verbosity >2: 
          print ('\tDebug: and change p[0]', p[0])

        if p.lexer.currentExploredDataPosition >= len(p.lexer.data):
          if self.verbosity >2: 
            print ('\tDebug: the parsing of a pattern is on going (True so far) but no more data remains to explore ; we empty the parser buffer')
          while True:
            tok = p.parser.token()             # Get the next token
            if not tok: 
              break
      elif p[1] == '+':
        p[0]=p[2]
        if p[0]:
          self.log(p, '(quantifiedstep-> ' + p[1] + 'step)')

          localLexer = Lexer(pattern=p.lexer.localstep, data=p.lexer.data)  # p.lexer.data)
          localLexer.lexer.localresult = True
          localLexer.lexer.currentExploredDataPosition = p.lexer.currentExploredDataPosition 
          localpatternstepparsingiter = 0
          #print ('Debug: before loop - data=', p.lexer.data, '; len(data)=',len(p.lexer.data), '; position=',localLexer.lexer.currentExploredDataPosition) 
          if self.verbosity >2: print("\tDebug: call localparser on step pattern=",p.lexer.localstep)
          #if self.verbosity >2: print('\tDebug: p.lexer.lexpos=',p.lexer.lexpos)
          
          ''' pre: the first step of the quantifier is true, we now explore if more tokens valid the pattern step'''
          localLexer.lexer.currentExploredDataPosition += 1
          while (localLexer.lexer.localresult and (localLexer.lexer.currentExploredDataPosition < len(p.lexer.data))):
            if self.verbosity >2: print ("\tDebug: start processing a (local) step pattern ; iteration=", localpatternstepparsingiter)
            
            #print ('Debug: in loop - data=', p.lexer.data, '; len(data)=',len(p.lexer.data), '; position=',localLexer.lexer.currentExploredDataPosition)
            if self.verbosity >2:
              #print ("\tDebug: len(p.lexer.data)=",len(p.lexer.data),"; inc(currentExploredDataPosition) ; currentExploredDataPosition=",localLexer.lexer.currentExploredDataPosition)
              print ("\tDebug: futuretoken=", p.lexer.data[localLexer.lexer.currentExploredDataPosition])
            localLexer.lexer.islocal = True
            localLexer.lexer.localstep = p.lexer.localstep
            
            localParser = Parser(tokens=localLexer.tokens, verbosity =self.verbosity , start='quantifiedstep') # Set Add True for debugging
            localParser.parser.parse(localLexer.lexer.localstep, localLexer.lexer) #, tracking=True)
            #localparser.parse(p.lexer.localstep,lexer=locallexer) #,start='expression'
            #print ("\tDebug: localparser.parser=",localParser.parser)
            
            if self.verbosity >2: print ("\tDebug: localLexer.lexer.localresult=",localLexer.lexer.localresult)
            localpatternstepparsingiter += 1
            localLexer.lexer.currentExploredDataPosition += 1
            if localLexer.lexer.currentExploredDataPosition >= len(p.lexer.data):
              if self.verbosity >2: 
                print ('\tDebug: the local parsing of a pattern is on going (True so far) but no more data remains to explore ; we empty the parser buffer')
              while True:
                tok = p.parser.token()             # Get the next token
                if not tok: 
                  break

          if self.verbosity >2: print("\tDebug: resume the global parser")          
          if self.verbosity >2: print ('\tDebug: localparser result=',localLexer.lexer.localresult)
          if not(localLexer.lexer.localresult): 
            if self.verbosity >2: print("\tDebug: since the last step pattern was False we decrement currentExploredDataPosition")
            localLexer.lexer.currentExploredDataPosition -=1
          localLexer.lexer.islocal = False
          #print ('\tDebug: localparser result=',locallexer.localresult)
          if self.verbosity >2: print ("\tDebug: + quantifier goes until the dataPosition=",localLexer.lexer.currentExploredDataPosition) #,'; token=',p.lexer.data[localLexer.lexer.currentExploredDataPosition])
          # TODO for '+' operator p.lexer.currentExploredDataPosition > localLexer.lexer.currentExploredDataPosition -1 otherwise the pattern is not matched
          p.lexer.currentExploredDataPosition = localLexer.lexer.currentExploredDataPosition #-1
         # if self.verbosity >2: print ("\tDebug: future dataPosition=",(p.lexer.currentExploredDataPosition),'; token=',p.lexer.data[p.lexer.currentExploredDataPosition])

          if self.verbosity >2: print('\tDebug: localLexer.lexer.lexpos=',localLexer.lexer.lexpos)

          if self.verbosity >2: print('\tDebug: p.lexer.lexpos=',p.lexer.lexpos)
          #print ("\tDebug: p.parser=",p.parser)
          #print ("\tDebug: p.lexer=",p.lexer)
          #parser.restart()

        else:
          # TODO #else: error, il faut passer à initial+1 et faire un restart du parseur sur la grammaire principale (si une seule règle)
          # ou bien rester sur initial et tester les autres règles et quand plus de règles passer à initial+1 et faire un parser.restart
          self.log(p, '(quantifiedstep-> ' + p[1] + 'step)')
          #p.lexer.matchongoing = False
      elif p[1] == '*':
        p[0] = p[2]
        self.log(p, '(quantifiedstep-> ' + p[1] + 'step)')
        #if not(p.lexer.islocal): when processing local step we never go to the quantified step so, this should not be called here
        if p[0]:
  
          localLexer = Lexer(pattern=p.lexer.localstep, data=p.lexer.data) 
          localLexer.lexer.localresult = True
          localLexer.lexer.currentExploredDataPosition = p.lexer.currentExploredDataPosition 
          localpatternstepparsingiter = 0
          #print ('Debug: before loop - data=', p.lexer.data, '; len(data)=',len(p.lexer.data), '; position=',localLexer.lexer.currentExploredDataPosition) 
          if self.verbosity >2: print("\tDebug: call localparser on step pattern=",p.lexer.localstep)
          #if self.verbosity >2: print('\tDebug: p.lexer.lexpos=',p.lexer.lexpos)
          
          ''' pre: the first step of the quantifier is true, we now explore if more tokens valid the grammar step'''
          localLexer.lexer.currentExploredDataPosition += 1
          while (localLexer.lexer.localresult and (localLexer.lexer.currentExploredDataPosition < len(p.lexer.data))):
            if self.verbosity >2: print ("\tDebug: start processing a (local) step pattern ; iteration=", localpatternstepparsingiter)
            
            #print ('Debug: in loop - data=', p.lexer.data, '; len(data)=',len(p.lexer.data), '; position=',localLexer.lexer.currentExploredDataPosition)
            if self.verbosity >2:
              #print ("\tDebug: len(p.lexer.data)=",len(p.lexer.data),"; inc(currentExploredDataPosition) ; currentExploredDataPosition=",localLexer.lexer.currentExploredDataPosition)
              print ("\tDebug: futuretoken=",p.lexer.data[localLexer.lexer.currentExploredDataPosition])
            localLexer.lexer.islocal = True
  #          locallexer = lex.lex()
  #          locallexer.islocal = True
  #          locallexer.localresult = ''
            localLexer.lexer.localstep = p.lexer.localstep
            localParser = Parser(tokens=localLexer.tokens, verbosity =self.verbosity , start='quantifiedstep') # Set Add True for debugging
            localParser.parser.parse(localLexer.lexer.localstep, localLexer.lexer) #, tracking=True)
            #localparser.parse(p.lexer.localstep,lexer=locallexer) #,start='expression'
            #print ("\tDebug: localparser.parser=",localParser.parser)
            
            if self.verbosity >2: print ("\tDebug: localLexer.lexer.localresult=",localLexer.lexer.localresult)
            localpatternstepparsingiter += 1
            localLexer.lexer.currentExploredDataPosition += 1
            if localLexer.lexer.currentExploredDataPosition >= len(p.lexer.data):
              if self.verbosity >2: 
                print ('\tDebug: the local parsing of a pattern is on going (True so far) but no more data remains to explore ; we empty the parser buffer')
              while True:
                tok = p.parser.token()             # Get the next token
                if not tok: 
                  break

          if self.verbosity >2: print("\tDebug: resume the global parser")          
          if self.verbosity >2: print ('\tDebug: localparser result=',localLexer.lexer.localresult)
          if not(localLexer.lexer.localresult): 
            if self.verbosity >2: print("\tDebug: since the last step pattern was False we decrement currentExploredDataPosition")
            localLexer.lexer.currentExploredDataPosition -=1
          localLexer.lexer.islocal = False
          #print ('\tDebug: localparser result=',locallexer.localresult)
          if self.verbosity >2: print ("\tDebug: + quantifier goes until the dataPosition=",localLexer.lexer.currentExploredDataPosition) #,'; token=',p.lexer.data[localLexer.lexer.currentExploredDataPosition])
          # TODO for '+' operator p.lexer.currentExploredDataPosition > localLexer.lexer.currentExploredDataPosition -1 otherwise the pattern is not matched
          p.lexer.currentExploredDataPosition = localLexer.lexer.currentExploredDataPosition #-1
         # if self.verbosity >2: print ("\tDebug: future dataPosition=",(p.lexer.currentExploredDataPosition),'; token=',p.lexer.data[p.lexer.currentExploredDataPosition])

          if self.verbosity >2: print('\tDebug: localLexer.lexer.lexpos=',localLexer.lexer.lexpos)

          if self.verbosity >2: print('\tDebug: p.lexer.lexpos=',p.lexer.lexpos)
          #print ("\tDebug: p.parser=",p.parser)
          #print ("\tDebug: p.lexer=",p.lexer)
          #parser.restart()
        if self.verbosity >2: 
          if p[0]:
            print ('\tDebug: Since we recognized at least one token, we move to the next data token ; currentExploredDataPosition=',p.lexer.currentExploredDataPosition)
          else:
            print ('\tDebug: We did not recognized the token, so we wont move to the next data token ; currentExploredDataPosition=',p.lexer.currentExploredDataPosition)
        p[0] = True 
        if self.verbosity >2: 
          print ('\tDebug: and anyway change p[0]', p[0])  

      
    # to log the parsing of the pattern
    #if p[0]  and not (p.lexer.islocal):
    p.lexer.patternStepPosition += 1

    # 
    if not (p[0]) and not (p.lexer.islocal):
      ''' the current pattern step is False so it abords the parsing, moves in the data to explore, and restart the parsing'''
      if self.verbosity >2:
        print ("\tQuantifier step fails to recognize")
      p.lexer.lastFirstExploredDataPosition += 1
      p.lexer.currentExploredDataPosition = p.lexer.lastFirstExploredDataPosition
      p.lexer.patternStepPosition = 0
      
      ''' if we already start to match something and consequently stored a start, we should remove it'''
      if p.lexer.matchongoing and len(p.lexer.groupstartindex) >0:
        if self.verbosity >2:
          print ("\t(Should be) Removing the last indexed start offset")
        p.lexer.groupstartindex.pop()  
        p.lexer.matchongoing = False
      # if some data remains to explore
      if  p.lexer.lastFirstExploredDataPosition < len(p.lexer.data):
  #       # and if none match so far or re mode is findall
  #       if not (p[0]) or p.lexer.re == 'findall': 
  #         if self.verbosity >2: print ("Context: dataPosition=",p.lexer.currentExploredDataPosition,"; dataToken=",p.lexer.data[p.lexer.currentExploredDataPosition], '; lexpos=',p.lexer.lexpos)
        if self.verbosity >2: print ('\tDebug: some data remains to explore and (not matched yet or re mode is "findall") we relaunch the pattern parser')
        # consequently the following lines will make as many p_expression calls as relaunch...
        p.parser.parse(p.lexer.lexdata, p.lexer, tracking=True) # .grammar .pattern

      else:
        if self.verbosity >2: print ('\tDebug: no more data to explore ; we empty the parser buffer')
        while True:
          tok = p.parser.token()             # Get the next token
          if not tok: 
            break

    if p.lexer.islocal: 
      if self.verbosity >2: print ("\tDebug: stop processing a (local) step pattern")
      p.lexer.islocal = False  
      p.lexer.localresult = p[0]

# _______________________________________________________________
  def p_step(self,p):
    '''step : atomicconstraint
            | NOT step
            | LBRACKET classconstraint RBRACKET '''  # | NOT atomicconstraint # ajoute WARNING: 2 shift/reduce conflicts
    self.setPatternStep(p)
    if len(p) == 2:
      p[0] = p[1]
      self.log(p, '(step->atomicconstraint)')
      if p.lexer.islocal:
        if self.verbosity >2: print ("\tDebug: processing a (local) step pattern")
  #      p.lexer.islocal = False
  #      p.lexer.localresult = p[0]
      else:
        p.lexer.localstep = p.lexer.patternStep 
    elif p[1] == '!':
      p[0] = not(p[2])
      self.log(p, '(step->NOT step)')
      if p.lexer.islocal:
        if self.verbosity >2: print ("\tDebug: processing a (local) step pattern")
  #      p.lexer.islocal = False
  #      p.lexer.localresult = p[0]
      else:
        p.lexer.localstep = p.lexer.patternStep        
    
    else:
      p[0] = p[2]
      self.log(p, '(step->LBRACKET classconstraint RBRACKET)')
      if p.lexer.islocal:
        if self.verbosity >2: print ("\tDebug: processing a (local) step pattern")
  #      p.lexer.islocal = False
  #      p.lexer.localresult = p[0]
      else:
        p.lexer.localstep = p.lexer.patternStep  

    if p[0] and not(p.lexer.matchongoing) and not (p.lexer.islocal): # do not need to store start position when it is a step pattern since it has alread been stored
      ''' this is the first step of a pattern'''
      if self.verbosity >2: print ("\tDebug: we store the start position of the current match")
      p.lexer.matchongoing = True
      p.lexer.groupstartindex.append(p.lexer.currentExploredDataPosition)

# _______________________________________________________________

  # def p_empty(self,p):
  #  'empty :'
  #  pass
# _______________________________________________________________
  def p_classconstraint(self,p):
    '''classconstraint : classconstraint AND partofclassconstraint
            | classconstraint OR partofclassconstraint 
            | partofclassconstraint ''' # partofclassconstraint  | terminalpartofclassconstraint 
            #| empty
            #     '''classconstraint : partofclassconstraint AND classconstraint
#            | partofclassconstraint OR classconstraint 
#            | partofclassconstraint ''' 
    self.setPatternStep(p)
    if len(p) == 2:

      #2:
      p[0] = p[1] #True # p[1]
    #  self.log(p, '(classconstraint->partofclassconstraint)')
    #
    else:
      if p[2] == '&':
        p[0] = p[1] and p[3]
        self.log(p, '(classconstraint->partofclassconstraint AND classconstraint)')

      else: 
        p[0] = p[1] or p[3]
        self.log(p, '(classconstraint->partofclassconstraint OR classconstraint)')

    if p.lexer.islocal:
      if self.verbosity >2: print ("\tDebug: processing a (local) step pattern")

# _______________________________________________________________
  #def p_terminalpartofclassconstraint(self,p):
  #  p_partofclassconstraint(self,p)

# _______________________________________________________________
  def p_partofclassconstraint(self,p):
    '''partofclassconstraint : atomicconstraint
                    | LPAREN classconstraint RPAREN  
                    | NOT classconstraint '''
    self.setPatternStep(p)

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
      if self.verbosity >2: print ("\tDebug: processing a (local) step pattern")

# _______________________________________________________________
  def p_atomicconstraint(self,p):
    '''atomicconstraint : NAME EQ VALUE 
                          | NAME MATCH VALUE
                          | NAME IN VALUE'''
    self.setPatternStep(p)
    attName = p[1]
    operator = p[2]
    attValue = p[3][1:-1]
    

    if attName in p.lexer.data[p.lexer.currentExploredDataPosition]:
      # checking if the given value is equal to the current dict feature of the data
      if operator == '=':
        p[0] = (p.lexer.data[p.lexer.currentExploredDataPosition][attName] == attValue)
      # checking if the given value, interpreted as regex, matches the current dict feature of the data 
      elif operator == '~':
        p[0] = (re.search(attValue,p.lexer.data[p.lexer.currentExploredDataPosition][attName]) != None)
        # checking if the current dict feature of the data belongs to a list having the name of the given value
      elif operator == '@':
        # check if the named list is kwown
 #       print('Debug: p.lexer.lexicons=',p.lexer.lexicons)
 #       print('Debug: attValue=',attValue)
 #       print('Debug: attValue in p.lexer.lexicons=',(attValue in p.lexer.lexicons))


        if attValue in p.lexer.lexicons:
          p[0] =  (p.lexer.data[p.lexer.currentExploredDataPosition][attName] in p.lexer.lexicons[attValue])
  #        print('Debug: p.lexer.lexicons[attValue]=',p.lexer.lexicons[attValue])
  #        print('Debug: p.lexer.data[p.lexer.currentExploredDataPosition][attName]=',p.lexer.data[p.lexer.currentExploredDataPosition][attName])
  #        print('Debug: p.lexer.data[p.lexer.currentExploredDataPosition][attName] in p.lexer.lexicons[attValue]=',(p.lexer.data[p.lexer.currentExploredDataPosition][attName] in p.lexer.lexicons[attValue]))
          
        else:
          p[0] = False  
      # should not enter here, because it would mean that the parser encountered an unknown operator    
      else:
        p[0] = False
      self.log(p, '(atomicconstraint->NAME=VALUE)') #: ' + attName + ' ' + operator + ' ' + attValue +')')
        
    else:
      p[0] = False
      self.log(p, '(atomicconstraint->NAME=VALUE)') #: ' + attName + ' ' + operator + ' ' + attValue +')')
        
      if self.verbosity >1: 
        print ('Warning: unknown attribute name:', attName)

    if p.lexer.islocal:
      if self.verbosity >2: print ("\tDebug: processing a (local) step pattern")


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


  def log(self, p, production):
    # Line Number and Position Tracking
    # http://www.dabeaz.com/ply/ply.html#ply_nn33
    if self.verbosity >1:
      print ('________________________________________________')
    if self.verbosity >2:
      startlineleftsymbol, endlineleftsymbol = p.linespan(1)  # Start,end lines of the left expression
      startlinerightsymbol, endlinerightsymbol = p.linespan(len(p)-1)  # Start,end lines of the right expression
      # The lexspan() function only returns the range of values up to the start of the last pattern symbol.
      startpositionleftsymbol, endpositionleftsymbol = p.lexspan(1)   # Start,end positions of left expression
      startpositionrightsymbol, endpositionrightsymbol = p.lexspan(len(p)-1)   # Start,end positions of left expression
      symbolsconcat = ''
      lasti=0
      for i in range (len(p)):
        sp, ep = p.lexspan(i)
        symbolsconcat = symbolsconcat+'>'+str(p[i])+'['+str(sp)+':'+str(ep)+']<'
        lasti = i

    if self.verbosity >1:
      print ('Production=', production)

      # print ('symbolsconcat=',symbolsconcat)
      # The current input text stored in the lexer.
    if self.verbosity >3:
      print ('Whole pattern/lexdata=', p.lexer.lexdata, '; len(lexdata)=', len(p.lexer.lexdata))
      print ('# of lexical tokens in the current production rule=', len(p))

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
      print ("Pattern step:\tposition=", p.lexer.patternStepPosition, "\t; value=", p.lexer.patternStep)
      if p.lexer.currentExploredDataPosition < len(p.lexer.data):
        print ("Data token:\tposition=", p.lexer.currentExploredDataPosition, "\t; value=", p.lexer.data[p.lexer.currentExploredDataPosition])
      else:
        print ("Data token:\tposition=", p.lexer.currentExploredDataPosition, "\t; value= no-more")

      print ('Return=', p[0])


  def setPatternStep(self,p):
    startpositionleftsymbol, endpositionleftsymbol = p.lexspan(1)
    if self.verbosity >3: 
      print ('\tDebug: p.lexer.lexpos=',p.lexer.lexpos,'; isInLexTokenEndDict=',(p.lexer.lexpos in p.lexer.lexTokenEndDict))
    if p.lexer.lexpos > len(p.lexer.lexdata):
      previouslextokenendposition = len(p.lexer.lexdata)
    else:
      previouslextokenendposition = p.lexer.lexpos - len(p.lexer.lexTokenEndDict[p.lexer.lexpos].value)
    p.lexer.patternStep = p.lexer.lexdata[startpositionleftsymbol:previouslextokenendposition]



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PARSING ERROR HANDLING
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def p_error(self,p):
    if not p:
      if self.verbosity >0: 
        print("Info: pattern parsed.")
      return

      # http://www.dabeaz.com/ply/ply.html#ply_nn26 6.8.2
      # Read ahead looking for a closing ';'
    if self.verbosity >0: 
      print ('Error: parsing error - unexpected token type="{}" with value="{}" at position {}. Search an error before this point.'.format(p.type, p.value, p.lexer.lexpos))
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
    self.parser = yacc.yacc(module=self,  start=start, errorlog=yacc.NullLogger(), **kwargs) #

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  MAIN
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# example use:
if __name__ == '__main__':
  pattern='?lem:"the" +pos:"JJ" [pos:"NN" & (lem:"car" | !lem:"bike" | !(lem:"bike"))] [raw:"is" | raw:"are"]'
  print ('Pattern:', pattern)

  data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'blue', 'lem':'blue', 'pos':'JJ'}]     
  data = [{'raw':'The', 'lem':'the', 'pos':'DET'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
  print ('Data:', data)

  #pattern = 'pos:"NN"'
  data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}]

  # Build the parser and 
  l = Lexer(pattern=pattern, data=data) 
  m = Parser(tokens=l.tokens, verbosity =2, start='expression')

  # try it out
  print ("Copy the grammar line without 'Grammar: ' (whitespace should not been included); The semi-colon ';' will lead to a parsing error")
  while True:
    try:
      #text2parse
      s = input('cl > ')   # Use raw_input on Python 2
    except EOFError:
      break
    m.parser.parse(s, l.lexer, tracking=True)


