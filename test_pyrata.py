# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# SET in the __init__, uncomment the test to perform and set the verbosity  (0 None 1 global 2 verbose) 
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import logging
import pyrata.re
import pyrata.semantic_pattern_parser

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class TestPyrata(object):

  testCounter = 0
  testSuccess = 0


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main test method
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def test (self, description = '', method = '', lexicons = {}, pattern = '', data = [], expected = [], verbosity = 0, 
    action = '', annotation= {}, group = [0], iob = False, **kwargs):
    ''' 
    general method for testing 
    '''

    if verbosity >0:
      print ('================================================')
#      print ('________________________________________________')
#      print ('------------------------------------------------')
#      print ('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
#      print ('- -  - - - - - - - - - - - - - - - - - - - - - -')



    if method == 'search':
      result = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = verbosity)
      if result != None:
        result = result.group()
    elif method == 'findall':
      result = pyrata.re.findall(pattern, data, lexicons=lexicons, verbosity = verbosity)
    elif method == 'finditer':
      result = pyrata.re.finditer(pattern, data, lexicons=lexicons, verbosity = verbosity) 
    elif method == 'annotate':
      result = pyrata.re.annotate (pattern, annotation, data, group, action, iob, verbosity = verbosity, **kwargs)

    else:
      raise Exception('wrong method to test')
    #print('Result:',l.lexer.finalresult,'; start:',l.lexer.groupstartindex,'; end:',l.lexer.groupendindex)
    #if debug:

    success = False
    if result == expected:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)

    if verbosity >0:
      print ('Method:\t', method) 
      if action != '': print ('Action:\t', action) 
      if lexicons != {}: print ('Lexicons:\t', lexicons)       
      print ('Pattern:\t', pattern)
      if group != [0]:       print ('Group:\t', group)
      if annotation != {}:       print ('Annotation:\t', annotation)
      print ('Data:\t\t', data)
      print ('Expected:\t', expected)
      print ('Recognized:\t', result) 
    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
    else:
      if verbosity >0:
        print ('Result:\tFAIL') 
        #exit()

    if verbosity >0:
      print ()
    
  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  # Test cases definitions
  # by default (if not specified) 
  # * a step is an atomic constraint wi eq operator
  # * the pattern is at least present once
  # * data is made of one or several elements
  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


  def test_search_step_in_data(self, verbosity):
    description = 'test_search_step_in_data'
    method = 'search'
    lexicons = {}
    pattern = 'pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'JJ', 'raw': 'fast'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_step_in_data(self, verbosity):
    description = 'test_findall_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_finditer_step_in_data(self, verbosity):
    description = 'test_finditer_step_in_data'
    method = 'finditer'
    lexicons = {}
    pattern = 'pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    matcheslist = pyrata.semantic_pattern_parser.MatchesList()  
    matcheslist.append(pyrata.semantic_pattern_parser.Match (start=2, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}]))
    matcheslist.append(pyrata.semantic_pattern_parser.Match (start=3, end=4, value=[{'pos': 'JJ', 'raw': 'easy'}]))
    matcheslist.append(pyrata.semantic_pattern_parser.Match (start=5, end=6, value=[{'pos': 'JJ', 'raw': 'funny'}]))
    matcheslist.append(pyrata.semantic_pattern_parser.Match (start=8, end=9, value=[{'pos': 'JJ', 'raw': 'regular'}]))
    expected = matcheslist
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_search_step_absent_in_data(self, verbosity):
    description = 'test_search_step_absent_in_data'
    method = 'search'
    lexicons = {}
    pattern = 'foo="bar"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_step_absent_in_data(self, verbosity):
    description = 'test_findall_step_absent_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'foo="bar"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_search_class_step_in_data(self, verbosity):
    description = 'test_search_class_step_in_data'
    method = 'search'
    lexicons = {}
    pattern = '[pos="VB" | pos="VBZ"]'
    #data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    #expected = [ {'raw':'are', 'lem':'be', 'pos':'VB'}]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, 
      {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, 
      {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, 
      {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'VBZ', 'raw': 'is'}]   
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_search_rich_class_step_in_data(self, verbosity):
    description = 'test_search_rich_class_step_in_data'
    method = 'search'
    lexicons = {}
    pattern = '[(pos="VB" | pos="VBZ") & !raw="is"]'
    #data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    #expected = [ {'raw':'are', 'lem':'be', 'pos':'VB'}]
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, 
      {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, 
      {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, 
      {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'VBZ', 'raw': 'is'}]   

  def test_findall_regex_step_in_data(self, verbosity):
    description = 'test_findall_regex_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'NNP', 'raw': 'Pyrata'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_lexicon_step_in_data(self, verbosity):
    description = 'test_findall_lexicon_step_in_data'
    method = 'findall'
    lexicons = {'positiveLexicon':['easy', 'funny']}
    pattern = 'raw@"positiveLexicon"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)   

  def test_findall_undefined_lexicon_step_in_data(self, verbosity):
    description = 'test_findall_undefined_lexicon_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'raw@"positiveLexicon"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)      

  def test_findall_multiple_lexicon_step_in_data(self, verbosity):
    description = 'test_findall_multiple_lexicon_step_in_data'
    method = 'findall'
    lexicons = {'positiveLexicon':['easy', 'funny'], 'negativeLexicon':['fast', 'regular']}
    pattern = '[raw@"positiveLexicon" | raw@"negativeLexicon"]'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'fast'}], [ {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}],[ {'pos': 'JJ', 'raw': 'regular'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)  


  def test_search_optional_step_in_data(self, verbosity):
    # echo 1 | perl -ne '$s = "abcbdb"; if ($s =~ /b?/) {print "matched>$1<\n";} else {print "unmatched\n"}'
    # echo 1 | perl -ne '$s = "abcbdb"; if ($s =~ /e?/) {print "matched>$1<\n";} else {print "unmatched\n"}'
    # both return matche but wo any character
    description = 'test_search_optional_step_in_data'
    method = 'search'
    lexicons = {}
    pattern = 'pos="JJ"?'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'raw': 'fast', 'pos': 'JJ'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_optional_step_in_data(self, verbosity):
    # echo 1 | perl -ne '$s = "abcbdb"; if ($s =~ /b?/) {print "matched>$1<\n";} else {print "unmatched\n"}'
    # echo 1 | perl -ne '$s = "abcbdb"; if ($s =~ /e?/) {print "matched>$1<\n";} else {print "unmatched\n"}'
    # both return matche but wo any character
    description = 'test_findall_optional_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="JJ"?'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_step_step_in_data(self, verbosity):
    description = 'test_findall_step_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="JJ" pos="NNS"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_optional_step_step_in_data(self, verbosity):
    description = 'test_findall_optional_step_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="JJ"? pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_any_step_step_in_data(self, verbosity):
    description = 'test_findall_any_step_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="JJ"* pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_at_least_one_step_step_in_data(self, verbosity):
    description = 'test_findall_at_least_one_step_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="JJ"+ pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_any_step_step_nbar_in_data(self, verbosity):
    # https://gist.github.com/alexbowe/879414
    # echo 0 | perl -ne '$s = "abccd"; if ($s =~ /([bc]c)/) {print "$1\n"}'
    # bc
    description = 'test_findall_any_step_step_nbar_in_data'
    method = 'findall'
    lexicons = {}
    pattern = '[pos~"NN.*" | pos="JJ"]* pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    #data = [ {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}],[{'pos': 'NNP', 'raw': 'Pyrata'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)    

  def test_findall_at_least_one_step_step_nbar_in_data(self, verbosity):
    # https://gist.github.com/alexbowe/879414
    # echo 0 | perl -ne '$s = "abccd"; if ($s =~ /([bc]c)/) {print "$1\n"}'
    # bc
    description = 'test_findall_at_least_one_step_step_nbar_in_data'
    method = 'findall'
    lexicons = {}
    pattern = '[pos~"NN.*" | pos="JJ"]+ pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    #data = [ {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)   

  def test_findall_step_step_partially_matched_in_data_ending(self, verbosity):
    description = 'test_findall_step_step_partially_matched_in_data_ending'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="NNS" pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_optional_step_step_partially_matched_in_data_ending(self, verbosity):
    description = 'test_findall_optional_step_step_partially_matched_in_data_ending'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="NNS"? pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_any_step_step_partially_matched_in_data_ending(self, verbosity):
    description = 'test_findall_any_step_step_partially_matched_in_data_ending'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="NNS"? pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_at_least_one_step_step_partially_matched_in_data_ending(self, verbosity):
    description = 'test_findall_at_least_one_step_step_partially_matched_in_data_ending'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="NNS"+ pos="JJ"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)


  def test_findall_step_at_least_one_not_step_step_in_data(self, verbosity):
    description = 'test_findall_step_at_least_one_not_step_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="VB" !pos="NNS"+ pos="NNS"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_step_present_optional_step_step_in_data(self, verbosity):
    description = 'test_findall_step_present_optional_step_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="VB" pos="JJ"? pos="NNS"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_step_absent_optional_step_step_in_data(self, verbosity):
    description = 'test_findall_step_absent_optional_step_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="IN" pos="JJ"? pos="NNP"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)


  def test_findall_step_optional_step_in_data(self, verbosity):
    #echo 0 |  perl -ne '$s="abbbcb"; if ($s =~/(bc?)/) {print "$1\n"}' gives b
    description = 'test_findall_step_optional_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="JJ" pos~"NN.*"?'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'raw': 'fast', 'pos': 'JJ'}], [{'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_step_any_step_in_data(self, verbosity):
    description = 'test_findall_step_any_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="JJ" pos~"NN.*"*'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'raw': 'fast', 'pos': 'JJ'}], [{'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)

  def test_findall_step_optinal_step_optional_step_step_in_data(self, verbosity):
    #echo 0 |  perl -ne '$s="abbbcb"; if ($s =~/(bc?)/) {print "$1\n"}' gives b
    description = 'test_findall_step_optinal_step_optional_step_step_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos="VBZ" pos="JJ"? pos="JJ"? pos="CC"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)
  
  def test_search_any_class_step_error_step_in_data(self, verbosity):
    description = 'test_search_any_class_step_error_step_in_data'
    method = 'search'
    lexicons = {}
    pattern = '[pos~"NN.*" | pos="JJ"]* blabla pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)    

  def test_findall_step_any_not_step1_step1_in_data(self, verbosity):
    # https://gist.github.com/alexbowe/879414
    description = 'test_findall_step_any_not_step1_step1_in_data'
    method = 'findall'
    lexicons = {}
    pattern = 'pos~"VB." [!raw="to"]* raw="to"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}]]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)    

  def test_pattern_starting_with_the_first_token_of_data_present_as_expected_in_data(self, verbosity):
    # ^ matches the start of data before the first token in a data.
    # $ matches the end of data ~after the last token of data.
    # test_pattern_starting_with_the_first_token_of_data_present_as_expected_in_data
    # test_pattern_ending_with_the_last_token_of_data_present_as_expected_in_data
    # test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_present_as_expected_in_data   
    # test_pattern_starting_with_the_first_token_of_data_not_present_as_expected_in_data
    # test_pattern_ending_with_the_last_token_of_data_not_present_as_expected_in_data
    # test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_not_present_as_expected_in_data  
    description = 'test_pattern_starting_with_the_first_token_of_data_present_as_expected_in_data'
    method = 'search'
    lexicons = {}
    pattern = '^raw="It" raw="is"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)  

  def test_pattern_ending_with_the_last_token_of_data_present_as_expected_in_data(self, verbosity):
    description = 'test_pattern_ending_with_the_last_token_of_data_present_as_expected_in_data'
    method = 'search'
    lexicons = {}
    pattern = 'raw="with" raw="Pyrata"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)  

  def test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_present_as_expected_in_data(self, verbosity):

    description = 'test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_present_as_expected_in_data'
    method = 'search'
    lexicons = {}
    pattern = '^raw="with" raw="Pyrata"$'
    data = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [{'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity)  


  def test_pattern_starting_with_the_first_token_of_data_not_present_as_expected_in_data(self, verbosity):
    description = 'test_pattern_starting_with_the_first_token_of_data_not_present_as_expected_in_data'
    method = 'search'
    lexicons = {}
    pattern = '^raw="is" raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)  


  def test_pattern_starting_with_the_first_token_of_data_not_present_as_expected_in_data(self, verbosity):
    description = 'test_pattern_starting_with_the_first_token_of_data_present_as_expected_in_data'
    method = 'search'
    lexicons = {}
    pattern = '^raw="is" raw="fast"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)  

  def test_pattern_ending_with_the_last_token_of_data_not_present_as_expected_in_data(self, verbosity):
    description = 'test_pattern_ending_with_the_last_token_of_data_not_present_as_expected_in_data'
    method = 'search'
    lexicons = {}
    pattern = 'raw="is" raw="fast"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)  

  def test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_not_present_as_expected_in_data(self, verbosity):
    description = 'test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_not_present_as_expected_in_data'
    method = 'search'
    lexicons = {}
    pattern = '^raw="is" raw="fast"$'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = None
    self.test(description, method, lexicons, pattern, data, expected, verbosity)  


  def test_search_groups_in_data(self, verbosity):
    if verbosity >0:
      print ('================================================')
    description = 'test_search_groups_in_data'
    method = 'search'
    lexicons = {}
    #pattern = '(raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")'

    #pattern = 'raw="It" (raw="is" |fa="ke") (( pos="JJ"* (pos="JJ" raw="and"|fa="ke") (pos="JJ"|fa="ke") |fa="ke")|fa="ke") (raw="to"|fa="ke")'
    #pattern = 'raw="It" (raw="is"|fa="ke") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )|fa="ke") (raw="to"|fa="ke")'
    #pattern = 'raw="It" (raw="is"|fa="ke") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to"|fa="ke")'
    #pattern = 'raw="A" (raw="B") (( raw="C"* (raw="C" raw="D") (raw="E") )) (raw="F")'
    
    pattern = 'raw="is"'                     # [None, 'raw="is"']
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}], 1, 2]]

    pattern = '(raw="is")'                   # [None, [[[None, 'raw="is"']]]]
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}], 1, 2], [[{'pos': 'VBZ', 'raw': 'is'}], 1, 2]]
    
    pattern = '(((raw="is")))'               # [None, [[[None, [[[None, [[[None, 'raw="is"']]]]]]]]]]   
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'is', 'pos': 'VBZ'}], 0, 1], [[{'raw': 'is', 'pos': 'VBZ'}], 0, 1]]
    
    pattern = 'raw="is" pos="JJ" pos="JJ"'   # [[None, 'raw="is" '], [None, 'pos="JJ" '], [None, 'pos="JJ"']]
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}], 1, 4]]
    
    pattern = 'raw="is" (pos="JJ") pos="JJ"' # [[None, 'raw="is" '], [None, [[[None, 'pos="JJ"']]]], [None, 'pos="NN"']]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], 1, 4], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]

    pattern = 'raw="is" (pos="JJ") ((pos="JJ"))' # 
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], 1, 4], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3], [[{'raw': 'easy', 'pos': 'JJ'}], 3, 4], [[{'raw': 'easy', 'pos': 'JJ'}], 3, 4] ]

    pattern = '(raw="is" pos="JJ")'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}], 1, 3], [[{'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}], 1, 3]]

    pattern = '(raw="is"|pos="JJ")'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'pos': 'VBZ', 'raw': 'is'}], 1, 2], [[{'pos': 'VBZ', 'raw': 'is'}], 1, 2]]

    pattern = '(raw="is") (pos="JJ")'        # [[None, [[[None, 'raw="is"']]]], [None, [[[None, 'pos="JJ"']]]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]
    
    pattern = '(raw="is" (pos="JJ"))'        # [None, [[[None, 'raw="is" '], [None, [[[None, 'pos="JJ"']]]]]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]

    pattern = '(raw="is" pos="JJ"|raw="is" )'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3]]

    pattern = '(raw="is" pos="NN"|raw="is" pos="JJ")'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3]]

    pattern = '(raw="is" pos="NN"|raw="is" pos="NN"|raw="is" pos="JJ")'          # [None, [[[None, 'raw="is" '], [None, 'pos="JJ"']]]]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3], [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}], 1, 3]]

    pattern = 'raw="It" (raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")'
    expected = [[[{'pos': 'PRP', 'raw': 'It'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}], 0, 7], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], [[{'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}], 3, 5], [[{'raw': 'funny', 'pos': 'JJ'}], 5, 6], [[{'raw': 'to', 'pos': 'TO'}], 6, 7]]
    #self.getLexer().lexer.group_pattern_offsets_group_list= [[0, 7], [1, 2], [2, 6], [2, 6], [3, 5], [5, 6], [6, 7]]

    pattern = 'raw="It" (raw="is") (( (pos="JJ"* pos="JJ") raw="and" (pos="JJ") )) (raw="to")'
    expected = [[[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}], 0, 7], 
      [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], 
      [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], 
      [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], 
      [[{'raw': 'fast', 'pos': 'JJ'}, {'pos': 'JJ', 'raw': 'easy'}], 2, 4], 
      [[{'raw': 'funny', 'pos': 'JJ'}], 5, 6], 
      [[{'raw': 'to', 'pos': 'TO'}], 6, 7]]
    
  # [[[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}], 0, 7], 
  # [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], 
  # [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6],
  # [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], 
  # [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], 2, 4],
  # [[{'raw': 'funny', 'pos': 'JJ'}], 5, 6],
  # [[{'raw': 'to', 'pos': 'TO'}], 6, 7]]

    # test only the compilation stage
    #pattern = 'raw="A" (raw="B") (( raw="C"* (raw="C" raw="D") (raw="E") )) (raw="F")'

    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    #data = [{'raw': 'A'}, {'raw': 'B'}, {'raw': 'C'}, {'raw': 'C'}, {'raw': 'D'}, {'raw': 'E'}, {'raw': 'F'}, {'raw': 'G'}, {'raw': 'H'}, {'raw': 'I'}, {'raw': 'J'},{'raw': 'K'}]




    #self.test(description, method, lexicons, pattern, data, expected, verbosity)  
    result = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = verbosity)
    #print ('Debug: type(result)=',type(result))
    #print ('Debug: type(result.groups)=',type(result.groups()))
    #print ('Debug: result=',result)
    
    result = result.groups()

    success = False
    if result == expected:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)
    

    #print ('Debug: type(result)=',result)
    if verbosity >0:
      print ('Method:\t', method) 
      print ('Lexicons:\t', lexicons)       
      print ('Pattern:\t', pattern)
      print ('Data:\t\t', data)
      print ('Expected groups:\t', expected)
      print ('Recognized groups:\t', result) 
    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
    else:
      if verbosity >0:
        print ('Result:\tFAIL')

    if verbosity >0:
      print ()




  def test_annotate_default_action_sub_default_group_default_iob_annotation_dict_in_data(self, verbosity):
    if verbosity >0:
      print ('================================================')
    description = 'test_annotate_default_action_sub_default_group_default_iob_annotation_dict_in_data'
    method = 'annotate'
    pattern = 'pos~"NN.?"'
    annotation = {'raw':'smurf', 'pos':'NN' },
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [{'pos': 'IN', 'raw': 'Over'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'smurf'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'smurf'}, {'pos': ',', 'raw': ','}, {'pos': 'NN', 'raw': 'smurf'}, {'pos': 'NN', 'raw': 'smurf'}, {'pos': 'VBD', 'raw': 'told'}, {'pos': 'PRP$', 'raw': 'his'}, {'pos': 'NN', 'raw': 'smurf'}]
    result = pyrata.re.annotate(pattern, annotation, data, verbosity = verbosity)
 

    success = False
    if result == expected:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)
    

    if verbosity >0:
      print ()
      print ('Method:\t', method)
      print ('Action:\t', 'default (i.e. sub)')
      print ('Pattern:\t', pattern)
      print ('Group:\t', 'default (i.e. [0])')      
      print ('Annotation:\t', annotation) 
      print ('IOB:\t', 'default (i.e. False)')
      print ('Data:\t\t', data)
      print ('Expected:\t', expected)
      print ('Result:\t\t', result) 


    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
    else:
      if verbosity >0:
        print ('Result:\tFAIL')

    if verbosity >0:
      print ()

    gold = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT', 'chunk':'B-NP'}, 
      {'raw':'cup', 'pos':'NN', 'chunk':'I-NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'B-NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'B-NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'I-NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'B-NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'I-NP'} ]


  def test_annotate_default_action_sub_default_group_default_iob_annotation_dict_not_in_data(self, verbosity):
    description = 'test_annotate_default_action_sub_default_group_default_iob_annotation_dict_not_in_data'
    method = 'annotate'
    action = 'sub'
    pattern = 'pos="JJ"'
    lexicons = {}
    annotation = {'raw':'smurf', 'pos':'NN' }
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'}, 
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, {'raw':'story', 'pos':'NN'} ]
    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation)


  def test_annotate_default_action_sub_default_group_default_iob_annotation_empty_in_data(self, verbosity):
    description = 'test_annotate_default_action_sub_default_group_default_iob_annotation_empty_in_data'
    method = 'annotate'
    action = 'sub'
    pattern = 'pos~"NN.?"'
    lexicons = {}
    annotation = []
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'of', 'pos':'IN'},
      {'raw':',', 'pos':','},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation)



  def test_annotate_default_action_sub_default_group_default_iob_annotation_dict_pattern_sequence_to_annotation_step_in_data(self, verbosity):
    description = 'test_annotate_default_action_sub_default_group_default_iob_annotation_dict_pattern_sequence_to_annotation_step_in_data'
    method = 'annotate'
    action = 'sub'
    pattern = 'pos~"(DT|PRP\$)" pos~"NN.?"'
    lexicons = {}
    annotation = {'raw':'smurf', 'pos':'NN' }
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, {'raw':'story', 'pos':'NN'} ]
    expected = [{'raw': 'Over', 'pos': 'IN'}, 
      {'raw': 'smurf', 'pos': 'NN'}, 
      {'raw': 'of', 'pos': 'IN'}, 
      {'raw': 'coffee', 'pos': 'NN'}, 
      {'raw': ',', 'pos': ','}, 
      {'raw': 'Mr.', 'pos': 'NNP'}, {'raw': 'Stone', 'pos': 'NNP'}, 
      {'raw': 'told', 'pos': 'VBD'}, 
      {'raw': 'smurf', 'pos': 'NN'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation)  #def test (self, description = '', method = '', lexicons = {}, pattern = '', data = [], expected = [], verbosity = 0, action = '', annotation= {}, group = [0], iob = False, **kwargs):


  def test_annotate_default_action_sub_group_one_default_iob_annotation_dict_pattern_in_data (self, verbosity):
    description = 'test_annotate_default_action_sub_group_one_default_iob_annotation_dict_pattern_in_data'
    method = 'annotate'
    action = 'sub'
    pattern = 'pos~"(DT|PRP\$)" (pos~"NN.?")'
    group = [1]
    lexicons = {}
    annotation = {'raw':'smurf', 'pos':'NN' }
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [{'raw': 'Over', 'pos': 'IN'}, {'raw': 'a', 'pos': 'DT'}, {'raw': 'smurf', 'pos': 'NN'}, {'raw': 'of', 'pos': 'IN'}, {'raw': 'coffee', 'pos': 'NN'}, {'raw': ',', 'pos': ','}, {'raw': 'Mr.', 'pos': 'NNP'}, {'raw': 'Stone', 'pos': 'NNP'}, {'raw': 'told', 'pos': 'VBD'}, {'raw': 'his', 'pos': 'PRP$'}, {'raw': 'smurf', 'pos': 'NN'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation, group)  
    #def test (self, description = '', method = '', lexicons = {}, pattern = '', data = [], expected = [], verbosity = 0, action = '', annotation= {}, group = [0], iob = False, **kwargs):



  def test_annotate_default_action_update_default_group_default_iob_annotation_dict_pattern_in_data(self, verbosity):
    description = 'test_annotate_default_action_update_default_group_default_iob_annotation_dict_pattern_in_data'
    method = 'annotate'
    action = 'update'
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    lexicons = {}
    annotation = {'raw':'smurf', 'pos':'NN', 'chunk':'NP'}
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [{'pos': 'IN', 'raw': 'Over'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'pos': 'IN', 'raw': 'of'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'pos': ',', 'raw': ','}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'pos': 'VBD', 'raw': 'told'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}, {'chunk': 'NP', 'pos': 'NN', 'raw': 'smurf'}]
    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation)  #def test (self, description = '', method = '', lexicons = {}, pattern = '', data = [], expected = [], verbosity = 0, action = '', annotation= {}, group = [0], iob = False, **kwargs):

  def test_annotate_default_action_extend_default_group_default_iob_annotation_dict_pattern_in_data(self, verbosity):
    description = 'test_annotate_default_action_extend_default_group_default_iob_annotation_dict_pattern_in_data'
    method = 'annotate'
    action = 'extend'
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    lexicons = {}
    annotation = {'raw':'smurf', 'pos':'NN', 'chunk':'NP'}
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' , 'chunk':'NP'}, 
      {'raw':'cup', 'pos':'NN' , 'chunk':'NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'NP'} ]

    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation)  #def test (self, description = '', method = '', lexicons = {}, pattern = '', data = [], expected = [], verbosity = 0, action = '', annotation= {}, group = [0], iob = False, **kwargs):


  def test_annotate_default_action_extend_default_group_default_iob_annotation_sequence_of_dict_for_single_token_match_in_data(self, verbosity):
    description = 'test_annotate_default_action_extend_default_group_default_iob_annotation_sequence_of_dict_for_single_token_match_in_data'
    method = 'annotate'
    action = 'extend'
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    lexicons = {}
    annotation = {'chunk':'NP'}
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' , 'chunk':'NP'}, 
      {'raw':'cup', 'pos':'NN' , 'chunk':'NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'NP'} ]
    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation)  #def test (self, description = '', method = '', lexicons = {}, pattern = '', data = [], expected = [], verbosity = 0, action = '', annotation= {}, group = [0], iob = False, **kwargs):


  def test_annotate_default_action_extend_default_group_default_iob_annotation_sequence_of_dict_for_single_token_match_in_data(self, verbosity):
    description = 'test_annotate_default_action_extend_default_group_default_iob_annotation_sequence_of_dict_for_single_token_match_in_data'
    method = 'annotate'
    action = 'extend'
    pattern = 'pos~"NN.?"'
    lexicons = {}
    annotation = [{'raw':'smurf1'}, {'raw':'smurf2'} ]
    group = [0]
    iob = True
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation, group, iob)  




  def test_annotate_default_action_extend_default_group_iob_True_annotation_sequence_by_one_dict_in_data(self, verbosity):
    description = 'test_annotate_default_action_extend_default_group_iob_True_annotation_sequence_by_one_dict_in_data'
    method = 'annotate'
    action = 'extend'
    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    lexicons = {}
    annotation = {'chunk':'NP'}
    group = [0]
    iob = True
    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' , 'chunk':'B-NP'}, 
      {'raw':'cup', 'pos':'NN' , 'chunk':'I-NP'},
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN', 'chunk':'B-NP'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP', 'chunk':'B-NP'}, 
      {'raw':'Stone', 'pos':'NNP', 'chunk':'I-NP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$', 'chunk':'B-NP'}, 
      {'raw':'story', 'pos':'NN', 'chunk':'I-NP'} ]
    self.test(description, method, lexicons, pattern, data, expected, verbosity, action, annotation, group, iob)  
    #def test (self, description = '', method = '', lexicons = {}, pattern = '', data = [], expected = [], verbosity = 0, action = '', annotation= {}, group = [0], iob = False, **kwargs):



  def test_search_alternative_groups_in_data(self, verbosity):
    if verbosity >0:
      print ('================================================')
    description = 'test_search_alternative_groups_in_data'
    method = 'search'
    #group = [1]
    lexicons = {}
    pattern = '(raw="a" raw="cup" raw="of" raw="coffee")'
    pattern = '(raw="a" raw="cup" raw="of" raw="coffee" | raw="a" raw="tea" )' # Error: syntactic parsing error - unexpected token type="NAME" with value="raw" at position 54. Search an error before this point.
    pattern = '((raw="a" raw="cup" raw="of" raw="coffee") | (raw="a" raw="tea" ))'

    pattern = '((raw="of" raw="coffee") | (raw="of" raw="tea" ))'
    pattern = '(raw="of" raw="coffee" | raw="of" raw="tea" )'

    pattern = '(raw="a" raw="the")'  # [None, [[[None, 'raw="a" '], [None, 'raw="the"']]]]
    group_id = 0

    pattern = '(raw="a"|raw="the")'  # [None, [ [[None, 'raw="a" ']], [[None, 'raw="the"']] ]]
    expected =  [[{'pos': 'DT', 'raw': 'a'}], 1, 2]

    #pattern = '(raw="a" raw="cup"|raw="the")'  # [None, [ [[None, 'raw="a" ']], [[None, 'raw="the"']] ]]
    #pattern = '(raw="the"|raw="a" raw="cup" raw="of")'  # [None, [ [[None, 'raw="a" ']], [[None, 'raw="the"']] ]]


    pattern = '(pos="IN") (raw="a" raw="tea" | raw="a" raw="cup" raw="of" raw="coffee" | raw="an" raw="orange" raw="juice" ) !pos=";"'
    group_id = 2
    expected = [[{'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'cup'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'coffee'}], 1, 5]
    #self.test(description, method, lexicons, pattern, data, expected, verbosity)  

    #pattern = '((raw="a" raw="cup" raw="of" raw="coffee")*| (raw="a" raw="tea" ))+'

    #pattern = '(raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")'


    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]

    result = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = verbosity)
    #print ('Debug: type(result)=',type(result))
    #print ('Debug: result=',result)

    if result != None: result = result._groups[group_id] #group(2)


    success = False
    if result == expected:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)


    if verbosity >0:

      print ('Method:\t', method) 
      print ('Lexicons:\t', lexicons)       
      print ('Pattern:\t', pattern)
      print ('Data:\t\t', data)
      print ('Expected groups:\t', expected)
      print ('Recognized groups:\t', result) 
    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
    else:
      if verbosity >0:
        print ('Result:\tFAIL')

    if verbosity >0:
      print ()


  def test_search_alternative_groups_wi_unmatched_quantifiers_in_data(self, verbosity):
    if verbosity >0:
      print ('================================================')
    description = 'test_search_alternative_groups_wi_unmatched_quantifiers_in_data'
    method = 'search'
    group = [1]
    lexicons = {}
    pattern = '(pos="IN") (raw="a" raw="tea" | raw="a" raw="cup" raw="of"? raw="coffee" | raw="an" raw="orange"* raw="juice" )+ !pos=";"'

    data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    expected = [[{'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'cup'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'coffee'}], 1, 5]

    result = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = verbosity)
    if result != None: result = result.groups[2] #group(2)

    success = False
    if result == expected:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)

    #print ('Debug: type(result)=',result)
    if verbosity >0:
      print ('Method:\t', method) 
      print ('Lexicons:\t', lexicons)       
      print ('Pattern:\t', pattern)
      print ('Data:\t\t', data)
      print ('Expected groups:\t', expected)
      print ('Recognized groups:\t', result) 
    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
    else:
      if verbosity >0:
        print ('Result:\tFAIL')

    if verbosity >0:
      print ()

  def test_search_groups_wi_matched_quantifiers_in_data(self, verbosity):
    if verbosity >0:
      print ('================================================')
    description = 'test_search_groups_wi_matched_quantifiers_in_data'
    method = 'search'
    group = [1]
    lexicons = {}
    #pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos="."|pos="FAKE")+' # Debug: p[0]=[[[None, 'pos="VB" '], ['?', 'pos="DT"'], ['*', 'pos="JJ"'], [None, 'pos="NN" '], [None, 'pos="."']], [[None, 'pos="FAKE"']]]

    pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")+' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']


    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    result = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = verbosity)
    if result != None: result = result.group(0) #group(2)

    success = False
    if result == expected:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)

    #print ('Debug: type(result)=',result)
    if verbosity >0:
      print ('Method:\t', method) 
      print ('Lexicons:\t', lexicons)       
      print ('Pattern:\t', pattern)
      print ('Data:\t\t', data)
      print ('Expected groups:\t', expected)
      print ('Recognized groups:\t', result) 
    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
    else:
      if verbosity >0:
        print ('Result:\tFAIL')

    if verbosity >0:
      print ()


  def test_search_alternatives_groups_wi_matched_quantifiers_in_data(self, verbosity):
    if verbosity >0:
      print ('================================================')
    description = 'test_search_alternatives_groups_wi_matched_quantifiers_in_data'
    method = 'search'
    group = [1]
    lexicons = {}
    pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos="."|pos="FAKE")+' # Debug: p[0]=[[[None, 'pos="VB" '], ['?', 'pos="DT"'], ['*', 'pos="JJ"'], [None, 'pos="NN" '], [None, 'pos="."']], [[None, 'pos="FAKE"']]]

    pattern = '(pos="VB" !pos="NN"* raw="Life" pos="."| pos="VB" !pos="NN"* raw="job" pos="."|pos="VB" !pos="NN"* raw="career" pos="."|pos="VB" !pos="NN"* raw="family" pos="."|pos="VB" !pos="NN"* raw="television" pos=".")+' # Debug: p[0]=[[[None, 'pos="VB" '], ['?', 'pos="DT"'], ['*', 'pos="JJ"'], [None, 'pos="NN" '], [None, 'pos="."']], [[None, 'pos="FAKE"']]]


    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    result = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = verbosity)
    if result != None: result = result.group(0) #group(2)

    success = False
    if result == expected:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)
    
    #print ('Debug: type(result)=',result)
    if verbosity >0:
      #print ()
      #print ('Test:\t', description)
      print ('Method:\t', method) 
      print ('Lexicons:\t', lexicons)       
      print ('Pattern:\t', pattern)
      print ('Data:\t\t', data)
      print ('Expected groups:\t', expected)
      print ('Recognized groups:\t', result) 

    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
    else:
      if verbosity >0:
        print ('Result:\tFAIL')

    if verbosity >0:
      print ()



  def test_eq_ne_len_operators_on_Matches_and_MatchesList(self, verbosity):
    if verbosity >0:
      print ('================================================')

    method = 'search'
    group = [1]
    lexicons = {}
    #pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos="."|pos="FAKE")+' # Debug: p[0]=[[[None, 'pos="VB" '], ['?', 'pos="DT"'], ['*', 'pos="JJ"'], [None, 'pos="NN" '], [None, 'pos="."']], [[None, 'pos="FAKE"']]]


    # Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television, choose washing machines, cars, compact disc players and electrical tin openers. Choose good health, low cholesterol, and dental insurance. 
    data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    expected = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]

    pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")+' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']
    quantified_group = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = verbosity)
    pattern = '(pos="VB" !pos="NN"* raw="Life" pos="."| pos="VB" !pos="NN"* raw="job" pos="."|pos="VB" !pos="NN"* raw="career" pos="."|pos="VB" !pos="NN"* raw="family" pos="."|pos="VB" !pos="NN"* raw="television" pos=".")+'
    quantified_alternatives = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = verbosity)
    
    description = 'test_eq_operator_on_Matches'
    success = False
    if quantified_group == quantified_alternatives:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)

    description = 'test_ne_operator_on_Matches'
    success = False
    if not(quantified_group != quantified_alternatives):
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description)

    description = 'test_len_on_Matches_ie_len_groups'
    success = False
    if len(quantified_group) == 6 and len(quantified_group) == len (quantified_alternatives):
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description) 

    pattern = 'pos="VB" pos="DT"? pos="JJ"* pos="NN" pos="."' # Debug: p[0]=['(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")']
    aMatchesList = pyrata.re.finditer(pattern, data)
    anotherMatchesList = pyrata.re.finditer(pattern, data)

    description = 'test_eq_on_MatchesList'
    success = False
    if aMatchesList == anotherMatchesList:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description) 
     
    description = 'test_ne_on_MatchesList'
    success = False
    if not(aMatchesList != anotherMatchesList):
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description) 


    description = 'test_len_on_MatchesList'
    success = False
    if len(aMatchesList) == 5:
      success = True
      self.testSuccess += 1
    self.testCounter +=1
    print (success,'\t', description) 
     


  def test_clause(self):
    # http://www.nltk.org/book/ch07.html # Building Nested Structure with Cascaded Chunkers
    sentence = [("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"),
      ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
    sentence = [("John", "NNP"), ("thinks", "VBZ"), ("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"), ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
    data = [{'raw':w, 'pos':p} for (w, p) in sentence]
    print ('Debug:', data)

    # NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN :      can   
    # extend pattern='pos~"DT|JJ|NN.*"+' annotation={'ch1':'NP'} iob = True 
    method = 'annotate'
    action = 'extend'
    group = [0]
    iob = True
    pattern = 'pos~"DT|JJ|NN.*"+'
    annotation = {'ch1':'NP'}
    result_NP = pyrata.re.annotate (pattern, annotation, data, group, action, iob)
    print ('Debug: ch1 NP=',result_NP)

    #PP: {<IN><NP>}               # Chunk prepositions followed by NP :  may   
    #extend pattern='pos="IN" ch1-"NP"' annotation={'ch2':'PP'} iob = True 
    #       pattern='pos="IN" (ch1="B-NP" ch1="I-NP"*)"
    pattern = 'pos="IN" (ch1="B-NP" ch1="I-NP"*)'
    annotation = {'ch2':'PP'}
    result_PP = pyrata.re.annotate (pattern, annotation, result_NP, group, action, iob)
    print ('Debug: ch2 PP=',result_PP)

    # VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments :    might 
    # extend pattern='pos~"VB.*" (ch1-"NP"|ch2-"PP"|ch3-"CLAUSE")+$' annotation={'ch4':'VP'} iob = True
     #       pattern='pos~"VB.*" (ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$'
    pattern = 'pos~"VB.*" (ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$' 
    annotation = {'ch4':'VP'}
    result_VP = pyrata.re.annotate (pattern, annotation, result_PP, group, action, iob)
    print ('Debug: ch4 VP=',result_VP)


    # CLAUSE: {<NP><VP>}           # Chunk NP, VP                         might 
    #extend pattern='ch1-"NP" ch4-"VP"' annotation={'ch3':'CLAUSE'} iob = True
    #        pattern='(ch1="B-NP" ch1="B-NP"*) (ch4="B-VP" ch4="I-VP"*)'
    pattern = '(ch1="B-NP" ch1="I-NP"*) (ch4="B-VP" ch4="I-VP"*)'
    annotation = {'ch3':'CLAUSE'}
    result_CLAUSE = pyrata.re.annotate (pattern, annotation, result_VP, group, action, iob)
    print ('Debug: ch3 CLAUSE=',result_CLAUSE)

    # loop 2
    pattern = 'pos~"VB.*" (ch3="B-CLAUSE" ch3="I-CLAUSE"*)+$' # it is not an OR all inclusive it is the first presented which match ch1="B-NP" ch1="I-NP"*|ch2="B-PP" ch2="I-PP"*|
    annotation = {'ch5':'VP'}
    result_VP = pyrata.re.annotate (pattern, annotation, result_PP, group, action, iob)
    print ('Debug: ch5 (loop 2) VP=',result_VP)

    pattern = '(ch1="B-NP" ch1="I-NP"*) (ch5="B-VP" ch5="I-VP"*)'
    annotation = {'ch6':'CLAUSE'}
    result_CLAUSE = pyrata.re.annotate (pattern, annotation, result_VP, group, action, iob)
    print ('Debug: ch6 (loop 2) CLAUSE=',result_CLAUSE)

# Debug: [{'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'raw': 'the', 'pos': 'DT'}, {'raw': 'cat', 'pos': 'NN'}, {'raw': 'sit', 'pos': 'VB'}, {'raw': 'on', 'pos': 'IN'}, {'raw': 'the', 'pos': 'DT'}, {'raw': 'mat', 'pos': 'NN'}]
# Debug: ch1 NP= [{'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN'}, {'raw': 'sit', 'pos': 'VB'}, {'raw': 'on', 'pos': 'IN'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'mat', 'pos': 'NN'}]
# Debug: ch2 PP= [{'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN'}, {'raw': 'sit', 'pos': 'VB'}, {'raw': 'on', 'pos': 'IN', 'ch2': 'B-PP'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT', 'ch2': 'I-PP'}, {'ch1': 'I-NP', 'raw': 'mat', 'pos': 'NN', 'ch2': 'I-PP'}]
# Debug: ch4 VP= [{'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN'}, {'ch4': 'B-VP', 'raw': 'sit', 'pos': 'VB'}, {'ch4': 'I-VP', 'raw': 'on', 'pos': 'IN', 'ch2': 'B-PP'}, {'ch4': 'I-VP', 'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT', 'ch2': 'I-PP'}, {'ch4': 'I-VP', 'ch1': 'I-NP', 'raw': 'mat', 'pos': 'NN', 'ch2': 'I-PP'}]
# [{'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, 
# {'raw': 'saw', 'pos': 'VBD'}, 
# {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN'}, 
# {'ch4': 'B-VP', 'raw': 'sit', 'pos': 'VB'}, 
# {'ch4': 'I-VP', 'raw': 'on', 'pos': 'IN', 'ch2': 'B-PP'}, 
# {'ch4': 'I-VP', 'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT', 'ch2': 'I-PP'}, 
# {'ch4': 'I-VP', 'ch1': 'I-NP', 'raw': 'mat', 'pos': 'NN', 'ch2': 'I-PP'}]

# Debug: ch3 CLAUSE= [{'pos': 'NN', 'raw': 'Mary', 'ch1': 'B-NP'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'raw': 'the', 'ch1': 'B-NP', 'ch3': 'B-CLAUSE'}, {'pos': 'NN', 'raw': 'cat', 'ch1': 'I-NP', 'ch3': 'I-CLAUSE'}, {'pos': 'VB', 'raw': 'sit', 'ch4': 'B-VP', 'ch3': 'I-CLAUSE'}, {'pos': 'IN', 'raw': 'on', 'ch2': 'B-PP', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP'}, {'ch2': 'I-PP', 'ch4': 'I-VP', 'ch3': 'I-CLAUSE', 'pos': 'DT', 'raw': 'the', 'ch1': 'B-NP'}, {'ch2': 'I-PP', 'ch4': 'I-VP', 'ch3': 'I-CLAUSE', 'pos': 'NN', 'raw': 'mat', 'ch1': 'I-NP'}]
# (S
#   (NP Mary/NN)
#   saw/VBD
#   (CLAUSE
#     (NP the/DT cat/NN)
#     (VP sit/VB (PP on/IN (NP the/DT mat/NN)))))

# [{'pos': 'NN', 'raw': 'Mary', 'ch1': 'B-NP'}, 
# {'pos': 'VBD', 'raw': 'saw'}, 
# {'pos': 'DT', 'raw': 'the', 'ch1': 'B-NP', 'ch3': 'B-CLAUSE'}, 
# {'pos': 'NN', 'raw': 'cat', 'ch1': 'I-NP', 'ch3': 'I-CLAUSE'}, 
# {'pos': 'VB', 'raw': 'sit', 'ch4': 'B-VP', 'ch3': 'I-CLAUSE'}, 
# {'pos': 'IN', 'raw': 'on', 'ch2': 'B-PP', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP'},
# {'ch2': 'I-PP', 'ch4': 'I-VP', 'ch3': 'I-CLAUSE', 'pos': 'DT', 'raw': 'the', 'ch1': 'B-NP'}, 
# {'ch2': 'I-PP', 'ch4': 'I-VP', 'ch3': 'I-CLAUSE', 'pos': 'NN', 'raw': 'mat', 'ch1': 'I-NP'}]

#Debug: ch4 (loop 2) VP= [{'raw': 'Mary', 'ch1': 'B-NP', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch3': 'B-CLAUSE', 'raw': 'the', 'ch1': 'B-NP', 'pos': 'DT'}, {'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch1': 'I-NP', 'pos': 'NN'}, {'ch3': 'I-CLAUSE', 'raw': 'sit', 'ch4': 'B-VP', 'pos': 'VB'}, {'ch3': 'I-CLAUSE', 'raw': 'on', 'ch4': 'I-VP', 'ch2': 'B-PP', 'pos': 'IN'}, {'ch3': 'I-CLAUSE', 'raw': 'the', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'DT', 'ch1': 'B-NP'}, {'ch3': 'I-CLAUSE', 'raw': 'mat', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'NN', 'ch1': 'I-NP'}]
#Debug: ch3 (loop 2) CLAUSE= [{'raw': 'Mary', 'ch1': 'B-NP', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch3': 'B-CLAUSE', 'raw': 'the', 'ch1': 'B-NP', 'pos': 'DT'}, {'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch1': 'I-NP', 'pos': 'NN'}, {'ch3': 'I-CLAUSE', 'raw': 'sit', 'ch4': 'B-VP', 'pos': 'VB'}, {'ch3': 'I-CLAUSE', 'raw': 'on', 'ch4': 'I-VP', 'ch2': 'B-PP', 'pos': 'IN'}, {'ch3': 'I-CLAUSE', 'raw': 'the', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'DT', 'ch1': 'B-NP'}, {'ch3': 'I-CLAUSE', 'raw': 'mat', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'NN', 'ch1': 'I-NP'}]

# [{'raw': 'Mary', 'ch1': 'B-NP', 'pos': 'NN'}, 
# {'raw': 'saw', 'pos': 'VBD'}, 
# {'ch3': 'B-CLAUSE', 'raw': 'the', 'ch1': 'B-NP', 'pos': 'DT'}, 
# {'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch1': 'I-NP', 'pos': 'NN'}, 
# {'ch3': 'I-CLAUSE', 'raw': 'sit', 'ch4': 'B-VP', 'pos': 'VB'}, 
# {'ch3': 'I-CLAUSE', 'raw': 'on', 'ch4': 'I-VP', 'ch2': 'B-PP', 'pos': 'IN'}, 
# {'ch3': 'I-CLAUSE', 'raw': 'the', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'DT', 'ch1': 'B-NP'}, 
# {'ch3': 'I-CLAUSE', 'raw': 'mat', 'ch2': 'I-PP', 'ch4': 'I-VP', 'pos': 'NN', 'ch1': 'I-NP'}]

# sentence 2
#Debug: [{'pos': 'NNP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'raw': 'the'}, {'pos': 'NN', 'raw': 'cat'}, {'pos': 'VB', 'raw': 'sit'}, {'pos': 'IN', 'raw': 'on'}, {'pos': 'DT', 'raw': 'the'}, {'pos': 'NN', 'raw': 'mat'}]
#Debug: ch1 NP= [{'pos': 'NNP', 'ch1': 'B-NP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'ch1': 'B-NP', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'cat'}, {'pos': 'VB', 'raw': 'sit'}, {'pos': 'IN', 'raw': 'on'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'mat'}]
#Debug: ch2 PP= [{'pos': 'NNP', 'ch1': 'B-NP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'ch1': 'B-NP', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'cat'}, {'pos': 'VB', 'raw': 'sit'}, {'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on'}, {'pos': 'DT', 'ch1': 'B-NP', 'ch2': 'I-PP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'ch2': 'I-PP', 'raw': 'mat'}]
#Debug: ch4 VP= [{'pos': 'NNP', 'ch1': 'B-NP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'ch1': 'B-NP', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'cat'}, {'pos': 'VB', 'raw': 'sit', 'ch4': 'B-VP'}, {'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on', 'ch4': 'I-VP'}, {'pos': 'DT', 'ch1': 'B-NP', 'ch2': 'I-PP', 'raw': 'the', 'ch4': 'I-VP'}, {'pos': 'NN', 'ch1': 'I-NP', 'ch2': 'I-PP', 'raw': 'mat', 'ch4': 'I-VP'}]
#Debug: ch3 CLAUSE= [{'pos': 'NNP', 'ch1': 'B-NP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'pos': 'NN', 'ch1': 'B-NP', 'raw': 'Mary'}, {'pos': 'VBD', 'raw': 'saw'}, {'pos': 'DT', 'ch1': 'B-NP', 'raw': 'the', 'ch3': 'B-CLAUSE'}, {'pos': 'NN', 'ch1': 'I-NP', 'raw': 'cat', 'ch3': 'I-CLAUSE'}, {'pos': 'VB', 'raw': 'sit', 'ch3': 'I-CLAUSE', 'ch4': 'B-VP'}, {'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP'}, {'ch1': 'B-NP', 'ch2': 'I-PP', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP', 'pos': 'DT', 'raw': 'the'}, {'ch1': 'I-NP', 'ch2': 'I-PP', 'ch3': 'I-CLAUSE', 'ch4': 'I-VP', 'pos': 'NN', 'raw': 'mat'}]
#Debug: ch5 (loop 2) VP= [{'ch1': 'B-NP', 'raw': 'John', 'pos': 'NNP'}, {'raw': 'thinks', 'pos': 'VBZ'}, {'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'pos': 'DT', 'ch3': 'B-CLAUSE'}, {'ch1': 'I-NP', 'raw': 'cat', 'pos': 'NN', 'ch3': 'I-CLAUSE'}, {'ch4': 'B-VP', 'raw': 'sit', 'ch5': 'B-VP', 'pos': 'VB', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch1': 'B-NP', 'pos': 'DT', 'ch2': 'I-PP', 'raw': 'the', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch1': 'I-NP', 'pos': 'NN', 'ch2': 'I-PP', 'raw': 'mat', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}]
#Debug: ch6 (loop 2) CLAUSE= [{'ch1': 'B-NP', 'raw': 'John', 'pos': 'NNP'}, {'raw': 'thinks', 'pos': 'VBZ'}, {'ch1': 'B-NP', 'raw': 'Mary', 'pos': 'NN'}, {'raw': 'saw', 'pos': 'VBD'}, {'ch1': 'B-NP', 'raw': 'the', 'ch6': 'B-CLAUSE', 'pos': 'DT', 'ch3': 'B-CLAUSE'}, {'ch1': 'I-NP', 'raw': 'cat', 'ch6': 'I-CLAUSE', 'pos': 'NN', 'ch3': 'I-CLAUSE'}, {'ch4': 'B-VP', 'pos': 'VB', 'ch6': 'I-CLAUSE', 'raw': 'sit', 'ch5': 'B-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch6': 'I-CLAUSE', 'pos': 'IN', 'ch2': 'B-PP', 'raw': 'on', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch1': 'B-NP', 'ch6': 'I-CLAUSE', 'pos': 'DT', 'ch2': 'I-PP', 'raw': 'the', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch4': 'I-VP', 'ch1': 'I-NP', 'ch6': 'I-CLAUSE', 'pos': 'NN', 'ch2': 'I-PP', 'raw': 'mat', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}]
#Debug: ch5 (loop 2) VP= [{'ch1': 'B-NP', 'pos': 'NNP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'ch1': 'B-NP', 'pos': 'NN', 'raw': 'Mary'}, {'ch5': 'B-VP', 'pos': 'VBD', 'raw': 'saw'}, {'ch1': 'B-NP', 'ch3': 'B-CLAUSE', 'pos': 'DT', 'raw': 'the', 'ch5': 'I-VP'}, {'ch1': 'I-NP', 'ch3': 'I-CLAUSE', 'pos': 'NN', 'raw': 'cat', 'ch5': 'I-VP'}, {'ch3': 'I-CLAUSE', 'pos': 'VB', 'raw': 'sit', 'ch4': 'B-VP', 'ch5': 'I-VP'}, {'ch2': 'B-PP', 'pos': 'IN', 'raw': 'on', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch1': 'B-NP', 'ch2': 'I-PP', 'pos': 'DT', 'raw': 'the', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}, {'ch1': 'I-NP', 'ch2': 'I-PP', 'pos': 'NN', 'raw': 'mat', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE'}]
#Debug: ch6 (loop 2) CLAUSE= [{'ch1': 'B-NP', 'pos': 'NNP', 'raw': 'John'}, {'pos': 'VBZ', 'raw': 'thinks'}, {'ch1': 'B-NP', 'pos': 'NN', 'raw': 'Mary', 'ch6': 'B-CLAUSE'}, {'ch5': 'B-VP', 'pos': 'VBD', 'raw': 'saw', 'ch6': 'I-CLAUSE'}, {'ch1': 'B-NP', 'ch5': 'I-VP', 'pos': 'DT', 'ch3': 'B-CLAUSE', 'raw': 'the', 'ch6': 'I-CLAUSE'}, {'ch1': 'I-NP', 'ch5': 'I-VP', 'pos': 'NN', 'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch6': 'I-CLAUSE'}, {'ch5': 'I-VP', 'pos': 'VB', 'ch3': 'I-CLAUSE', 'ch4': 'B-VP', 'raw': 'sit', 'ch6': 'I-CLAUSE'}, {'ch2': 'B-PP', 'pos': 'IN', 'raw': 'on', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}, {'ch1': 'B-NP', 'ch2': 'I-PP', 'pos': 'DT', 'raw': 'the', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}, {'ch1': 'I-NP', 'ch2': 'I-PP', 'pos': 'NN', 'raw': 'mat', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}]


# (S
#   (NP John/NNP)
#   thinks/VBZ
#   (CLAUSE
#     (NP Mary/NN)
#     (VP
#       saw/VBD
#       (CLAUSE
#         (NP the/DT cat/NN)
#         (VP sit/VB (PP on/IN (NP the/DT mat/NN)))))))

# [{'ch1': 'B-NP', 'pos': 'NNP', 'raw': 'John'}, 
# {'pos': 'VBZ', 'raw': 'thinks'}, 
# {'ch1': 'B-NP', 'pos': 'NN', 'raw': 'Mary', 'ch6': 'B-CLAUSE'}, 
# {'ch5': 'B-VP', 'pos': 'VBD', 'raw': 'saw', 'ch6': 'I-CLAUSE'}, 
# {'ch1': 'B-NP', 'ch5': 'I-VP', 'pos': 'DT', 'ch3': 'B-CLAUSE', 'raw': 'the', 'ch6': 'I-CLAUSE'}, 
# {'ch1': 'I-NP', 'ch5': 'I-VP', 'pos': 'NN', 'ch3': 'I-CLAUSE', 'raw': 'cat', 'ch6': 'I-CLAUSE'}, 
# {'ch5': 'I-VP', 'pos': 'VB', 'ch3': 'I-CLAUSE', 'ch4': 'B-VP', 'raw': 'sit', 'ch6': 'I-CLAUSE'}, 
# {'ch2': 'B-PP', 'pos': 'IN', 'raw': 'on', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}, 
# {'ch1': 'B-NP', 'ch2': 'I-PP', 'pos': 'DT', 'raw': 'the', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}, 
# {'ch1': 'I-NP', 'ch2': 'I-PP', 'pos': 'NN', 'raw': 'mat', 'ch4': 'I-VP', 'ch5': 'I-VP', 'ch3': 'I-CLAUSE', 'ch6': 'I-CLAUSE'}]

    self.testCounter +=1


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Declare here all the tests you want to run
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def __init__(self):

    myverbosity = 0
    self.test_search_step_in_data(myverbosity)
    self.test_findall_step_in_data(myverbosity)
    self.test_finditer_step_in_data(myverbosity)

    self.test_search_step_absent_in_data(myverbosity)
    self.test_findall_step_absent_in_data(myverbosity)

    self.test_search_class_step_in_data(myverbosity)
    self.test_search_rich_class_step_in_data(myverbosity)

    self.test_findall_regex_step_in_data(myverbosity)
    self.test_findall_lexicon_step_in_data(myverbosity)
    self.test_findall_undefined_lexicon_step_in_data(myverbosity)

    self.test_findall_multiple_lexicon_step_in_data(myverbosity)

    self.test_search_optional_step_in_data(myverbosity)
    self.test_findall_optional_step_in_data(myverbosity)
    
    self.test_findall_step_step_in_data(myverbosity)

    self.test_findall_optional_step_step_in_data(myverbosity)
    self.test_findall_any_step_step_in_data(myverbosity)
    self.test_findall_at_least_one_step_step_in_data(myverbosity)

    self.test_findall_any_step_step_nbar_in_data(myverbosity)
    self.test_findall_at_least_one_step_step_nbar_in_data(myverbosity)

    self.test_findall_step_step_partially_matched_in_data_ending(myverbosity)
    self.test_findall_optional_step_step_partially_matched_in_data_ending(myverbosity)
    self.test_findall_any_step_step_partially_matched_in_data_ending(myverbosity)
    self.test_findall_at_least_one_step_step_partially_matched_in_data_ending(myverbosity)

    self.test_findall_step_at_least_one_not_step_step_in_data(myverbosity)
    self.test_findall_step_present_optional_step_step_in_data(myverbosity)
    self.test_findall_step_absent_optional_step_step_in_data(myverbosity)

    self.test_findall_step_optional_step_in_data(myverbosity)
    self.test_findall_step_any_step_in_data(myverbosity)
    self.test_findall_step_optinal_step_optional_step_step_in_data(myverbosity)

    self.test_findall_step_any_not_step1_step1_in_data(myverbosity)

    self.test_pattern_starting_with_the_first_token_of_data_present_as_expected_in_data(myverbosity)
    self.test_pattern_ending_with_the_last_token_of_data_present_as_expected_in_data(myverbosity)
    self.test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_present_as_expected_in_data(myverbosity)
    self.test_pattern_starting_with_the_first_token_of_data_not_present_as_expected_in_data(myverbosity)
    self.test_pattern_ending_with_the_last_token_of_data_not_present_as_expected_in_data(myverbosity)
    self.test_pattern_starting_with_the_first_token_of_data_and_ending_with_the_last_token_of_data_not_present_as_expected_in_data(myverbosity)


    self.test_search_groups_in_data(myverbosity)

    self.test_annotate_default_action_sub_default_group_default_iob_annotation_dict_in_data(myverbosity)
    self.test_annotate_default_action_sub_default_group_default_iob_annotation_dict_not_in_data(myverbosity)
    self.test_annotate_default_action_sub_default_group_default_iob_annotation_dict_pattern_sequence_to_annotation_step_in_data(myverbosity)
    self.test_annotate_default_action_sub_group_one_default_iob_annotation_dict_pattern_in_data(myverbosity)
    self.test_annotate_default_action_sub_default_group_default_iob_annotation_empty_in_data(myverbosity)


    self.test_annotate_default_action_update_default_group_default_iob_annotation_dict_pattern_in_data(myverbosity)
    self.test_annotate_default_action_extend_default_group_default_iob_annotation_dict_pattern_in_data(myverbosity)
    self.test_annotate_default_action_extend_default_group_default_iob_annotation_sequence_of_dict_for_single_token_match_in_data(myverbosity)
    self.test_annotate_default_action_extend_default_group_iob_True_annotation_sequence_by_one_dict_in_data(myverbosity)

    self.test_search_groups_wi_matched_quantifiers_in_data(myverbosity)

    self.test_search_alternative_groups_in_data(myverbosity)
    self.test_search_alternatives_groups_wi_matched_quantifiers_in_data(myverbosity)

    self.test_eq_ne_len_operators_on_Matches_and_MatchesList(myverbosity)



    #self.test_clause()

    #self.test_search_any_class_step_error_step_in_data(myverbosity)



    
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':



#  logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='test_pyrata.py.log', level=logging.DEBUG)
  logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='test_pyrata.py.log', level=logging.INFO)

  tests = TestPyrata()
  
  accuracy=tests.testSuccess/float(tests.testCounter)
  print ("PyRATA - testCounter=",tests.testCounter,'; testSuccess=',tests.testSuccess,'; accuracy=',accuracy)