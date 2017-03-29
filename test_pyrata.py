# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# SET in the __init__, uncomment the test to perform and set the verbosity  (0 None 1 global 2 verbose) 
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pyrata.re
import pyrata.semantic_analysis

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class TestPyrata(object):

  testCounter = 0
  testSuccess = 0


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main test method
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def test (self, description, method, lexicons, pattern, data, expected, verbosity):
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
    else:
      raise Exception('wrong method to test')
    #print('Result:',l.lexer.finalresult,'; start:',l.lexer.groupstartindex,'; end:',l.lexer.groupendindex)
    #if debug:
    if verbosity >0:
      print ()
      print ('Test:\t', description)
      print ('Method:\t', method) 
      print ('Lexicons:\t', lexicons)       
      print ('Pattern:\t', pattern)
      print ('Data:\t\t', data)
      print ('Expected:\t', expected)
      print ('Recognized:\t', result) 
    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
      self.testSuccess += 1
    else:
      if verbosity >0:
        print ('Result:\tFAIL')
    self.testCounter +=1

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
    matcheslist = pyrata.semantic_analysis.MatchesList()  
    matcheslist.append(pyrata.semantic_analysis.Match (start=2, end=3, value=[{'pos': 'JJ', 'raw': 'fast'}]))
    matcheslist.append(pyrata.semantic_analysis.Match (start=3, end=4, value=[{'pos': 'JJ', 'raw': 'easy'}]))
    matcheslist.append(pyrata.semantic_analysis.Match (start=5, end=6, value=[{'pos': 'JJ', 'raw': 'funny'}]))
    matcheslist.append(pyrata.semantic_analysis.Match (start=8, end=9, value=[{'pos': 'JJ', 'raw': 'regular'}]))
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

  def test_search_groups_in_data(self, verbosity):
    if verbosity >0:
      print ('================================================')
    description = 'test_search_groups_in_data'
    method = 'search'
    lexicons = {}
    pattern = '(raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}], 1, 7], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], [[{'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}], 3, 5], [[{'raw': 'funny', 'pos': 'JJ'}], 5, 6], [[{'raw': 'to', 'pos': 'TO'}], 6, 7]]
    #self.test(description, method, lexicons, pattern, data, expected, verbosity)  
    result = pyrata.re.search(pattern, data, lexicons=lexicons, verbosity = 1).groups

    #print ('Debug: type(result)=',result)
    if verbosity >0:
      print ()
      print ('Test:\t', description)
      print ('Method:\t', method) 
      print ('Lexicons:\t', lexicons)       
      print ('Pattern:\t', pattern)
      print ('Data:\t\t', data)
      print ('Expected groups:\t', expected)
      print ('Recognized groups:\t', result) 
    if result == expected:
      if verbosity >0:
        print ('Result:\tSUCCESS')
      self.testSuccess += 1
    else:
      if verbosity >0:
        print ('Result:\tFAIL')
    self.testCounter +=1

    if verbosity >0:
      print ()


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Declare here all the tests you want to run
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def __init__(self):

    myverbosity = 3
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

    self.test_search_any_class_step_error_step_in_data(myverbosity)
    self.test_findall_step_any_not_step1_step1_in_data(myverbosity)

    self.test_search_groups_in_data(myverbosity)





    
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  tests = TestPyrata()
  
  accuracy=tests.testSuccess/float(tests.testCounter)
  print ("PyRATA - testCounter=",tests.testCounter,'; testSuccess=',tests.testSuccess,'; accuracy=',accuracy)