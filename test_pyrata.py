# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# SET in the __init__, uncomment the test to perform and set the loglevel (0 None 1 global 2 verbose) 
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pyrata_re

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class TestPyrata(object):

  testCounter = 0
  testSuccess = 0


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main test method
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def test (self, description, method, pattern, data, expected, loglevel):
    ''' output the result in console '''
    if loglevel>0:
      print ('________________________________________________')
    if loglevel>1:
      print ('Test:',description)
      print ('Method:\t',method)      
      print ('Pattern:\t',pattern)
      print ('Data:\t\t',data)
      print ('Expected:\t',expected)

    if method == 'search':
      result = pyrata_re.search(pattern, data, loglevel=loglevel)
      if result != None:
        result = result.group()
    elif method == 'findall':
      result = pyrata_re.findall(pattern, data, loglevel=loglevel)
    else:
      raise Exception('wrong method to test')
    #print('Result:',l.lexer.finalresult,'; start:',l.lexer.groupstartindex,'; end:',l.lexer.groupendindex)
    #if debug:    
    if loglevel>1:
      print ('Result:',result) 
    if result == expected:
      if loglevel>1:
        print ('Test:',description, '- SUCCESS')
      self.testSuccess +=1
    else:
      if loglevel>1:
        print ('Test:',description, '- FAIL')
    self.testCounter +=1

    if loglevel>0:
      print ()
    
  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  # Test cases definitions
  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def test_match_at_the_sequence_begining_is_atomic_constraint(self, loglevel):
    description = 'match_at_the_sequence_begining_is_atomic_constraint'
    method='search'
    pattern = 'lem="the"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}]
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_whole_sequence_with_pattern_of_atomic_constraints(self, loglevel):
    description = 'match_whole_sequence_with_pattern_of_atomic_constraints'
    method='search'
    pattern = 'pos="DT" pos="JJ" pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_inside_sequence_of_atomic_constraints(self, loglevel):
    description = 'search and match inside a sequence of "is" atomic constraints'
    method='search'
    pattern = 'pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}]
    expected = [{'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_multiple_inside_sequence_of_atomic_constraints(self, loglevel):
    description = 'match_multiple_inside_sequence_of_atomic_constraints'
    method='search'
    pattern = 'pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    expected = [{'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_unpresent_inside_sequence_of_atomic_constraints(self, loglevel):
    description = 'match_unpresent_inside_sequence_of_atomic_constraints'
    method='search'
    pattern = 'pos="Ex"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    expected = None
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_at_the_sequence_begining_quantifier_at_least_one_on_atomic_constraint(self, loglevel):
    description = 'match_at_the_sequence_begining_quantifier_at_least_one_on_atomic_constraint'
    method='search'
    pattern = 'pos="DT" +pos="JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_inside_sequence_quantifier_at_least_one_on_atomic_constraint(self, loglevel):
    description = 'match_inside_sequence_quantifier_at_least_one_on_atomic_constraint'
    method='search'
    pattern = '+pos="JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_at_the_ending_sequence_quantifier_at_least_one_on_atomic_constraint(self, loglevel):
    description = 'match_at_the_ending_sequence_quantifier_at_least_one_on_atomic_constraint'
    method='search'
    pattern = '+pos="JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]     
    expected = [{'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_inside_sequence_class_constraint(self, loglevel):
    description = 'match_inside_sequence_class_constraint'
    method='search'
    pattern = '[lem="be" | raw="is"]'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'are', 'lem':'be', 'pos':'VB'}]     
    self.test(description, method, pattern, data, expected, loglevel)

  def test_match_inside_sequence_quantifier_at_least_one_on_class_constraint(self, loglevel):
    description = 'match_inside_sequence_quantifier_at_least_one_on_class_constraint'
    method='search'
    pattern = '+[lem="be" | raw="is"]'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'are', 'lem':'be', 'pos':'VB'}]     
    self.test(description, method, pattern, data, expected, loglevel)  

  def test_match_inside_sequence_surrounded_at_least_one_complex_class_constraint(self, loglevel):
    description = 'match_inside_sequence_surrounded_at_least_one_complex_class_constraint'
    method='search'
    pattern = 'pos="DT" +[pos="JJ" & !pos="EX"]  pos="NN"'
    data = [{'raw':'Here', 'lem':'here', 'pos':'ADV'}, {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]     
#    data = [{'pos':'ADV'}, {'pos':'DT'}, {'pos':'JJ'}, {'pos':'JJ'}, {'pos':'JJ'}, {'pos':'NN'}, { 'pos':'VB'}, {'pos':'JJ'}]     
#    expected = [ {'pos':'DT'}, {'pos':'JJ'}, {'pos':'JJ'}, {'pos':'JJ'}, {'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel) 

  def test_match_inside_sequence_at_least_one_including_negation_in_class_constraint(self, loglevel):
    description = 'match_inside_sequence_at_least_one_including_negation_in_class_constraint'
    method='search'
    pattern = 'pos="DT" +[!pos="NN" & !pos="EX" ] pos="NN"'
    data = [{'raw':'Here', 'lem':'here', 'pos':'ADV'}, {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]     
    self.test(description, method, pattern, data, expected, loglevel) 

  def test_match_inside_sequence_at_least_one_including_negation_on_atomic_constraint(self, loglevel):
    description = 'match_inside_sequence_at_least_one_including_negation_on_atomic_constraint'
    method='search'
    pattern = 'pos="DT" +!pos="NN" pos="NN"'
    data = [{'raw':'Here', 'lem':'here', 'pos':'ADV'}, {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]     
    self.test(description, method, pattern, data, expected, loglevel) 


  def test_match_inside_sequence_quantifier_option_on_atomic_constraint(self, loglevel):
    description = 'match_inside_sequence_quantifier_option_on_atomic_constraint'
    method='search'
    pattern = '?pos="ADV"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = None
    self.test(description, method, pattern, data, expected, loglevel)

  def test_search_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint(self, loglevel):
    description = 'search_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint'
    method='search'
    pattern = 'pos="NN" ?pos="VB" pos="JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_search_partially_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint(self, loglevel):
    description = 'search_partially_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint'
    method='search'
    pattern = 'pos="NN" ?pos="VB" pos="JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_search_partially_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint_with_trailer(self, loglevel):
    description = 'search_partially_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint_with_trailer'
    method='search'
    pattern = 'pos="NN" ?pos="VB" pos="JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}, {'raw':'are', 'lem':'be', 'pos':'VB'}]     
    expected = [ {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]
    self.test(description, method, pattern, data, expected, loglevel)


  def test_search_unpresent_pattern_wi_surrounded_quantifier_option_on_atomic_constraint(self, loglevel):
    description = 'search_unpresent_pattern_wi_surrounded_quantifier_option_on_atomic_constraint'
    method='search'
    pattern = 'pos="NN" ?pos="ADV" pos="JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = None
    self.test(description, method, pattern, data, expected, loglevel)    

  def test_search_quantifier_option_at_the_pattern_beginning_on_atomic_constraint(self, loglevel):
    description = 'search_partially_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint'
    method='search'
    pattern = '?pos="JJ" pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_search_quantifier_option_at_the_pattern_end_on_atomic_constraint(self, loglevel):
    #echo 0 |  perl -ne '$s="abbbcb"; if ($s =~/(bc?)/) {print "$1\n"}'
    description = 'search_partially_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint'
    method='search'
    pattern = 'pos="JJ" ?pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'big', 'lem':'big', 'pos':'JJ'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_search_multiple_consecutive_quantifier_option_inside_the_pattern_on_atomic_constraint(self, loglevel):
    description = 'search_multiple_consecutive_quantifier_option_inside_the_pattern_on_atomic_constraint'
    method='search'
    pattern = 'pos="DT" ?pos="JJ" ?pos="JJ" ?pos="JJ" pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel)

  def test_search_quantifier_any_inside_the_pattern_on_atomic_constraint(self, loglevel):
    description = 'search_quantifier_any_inside_the_pattern_on_atomic_constraint'
    method='search'
    pattern = 'pos="DT" *pos="JJ" pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel)  

  def test_search_quantifier_any_at_the_pattern_beginning_on_atomic_constraint(self, loglevel):
    description = 'search_quantifier_any_at_the_pattern_beginning_on_atomic_constraint'
    method='search'
    pattern = '*pos="JJ" pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel)     


  def test_search_quantifier_any_at_the_pattern_end_on_atomic_constraint(self, loglevel):
    description = 'search_quantifier_any_at_the_pattern_end_on_atomic_constraint'
    method='search'
    pattern = 'pos="DT" *pos="JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]
    self.test(description, method, pattern, data, expected, loglevel)      

  def test_search_quantifier_any_inside_the_pattern_on_non_present_atomic_constraint(self, loglevel):
    # echo '0' | perl -ne '$s = "abde"; if ($s =~ /(bc?d)/) {print "$1\n"}'
    description = 'search_quantifier_any_inside_the_pattern_on_non_present_atomic_constraint'
    method='search'
    pattern = 'pos="DT" *pos="JJ" pos="NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'cars', 'lem':'car', 'pos':'NN'},  {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, method, pattern, data, expected, loglevel)  

  def test_findall_at_multiple_locations_in_the_pattern_on_atomic_constraint(self, loglevel):
    description = 'search_quantifier_any_at_the_pattern_end_on_atomic_constraint'
    method='findall'
    pattern = 'pos="NN"'
    data = [{'lem':'car', 'pos':'NN'}, {'lem':'the', 'pos':'DT'}, {'lem':'car', 'pos':'NN'},{'lem':'the', 'pos':'DT'}, {'lem':'car', 'pos':'NN'},{'lem':'the', 'pos':'DT'}, {'lem':'car', 'pos':'NN'}, {'lem':'car', 'pos':'NN'}, {'lem':'the', 'pos':'DT'}, {'lem':'car', 'pos':'NN'}]     
    expected = [[{'lem':'car', 'pos':'NN'}],[{'lem':'car', 'pos':'NN'}],[{'lem':'car', 'pos':'NN'}],[{'lem':'car', 'pos':'NN'}],[{'lem':'car', 'pos':'NN'}],[{'lem':'car', 'pos':'NN'}]]
    self.test(description, method, pattern, data, expected, loglevel)      


  def test_findall_any_atomic_class(self, loglevel):
    description = 'findall_any_atomic_class'
    method='findall'
    pattern = '*pos="JJ" [(pos="NNS" | pos="NNP")]'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'NNP', 'raw': 'Pyrata'}]]
    self.test(description, method, pattern, data, expected, loglevel)      

  def test_findall_match_atomic_class(self, loglevel):
    description = 'findall_match_atomic_class'
    method='findall'
    pattern = 'pos~"NN.*"'
    data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    expected = [[{'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'NNP', 'raw': 'Pyrata'}]]
    self.test(description, method, pattern, data, expected, loglevel)     

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Declare here all the tests you want to run
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def __init__(self):
    # 0 None
    # 1 production rules
    # 2 +header
    # 3 +production details 
    myloglevel=0
    self.test_match_at_the_sequence_begining_is_atomic_constraint(myloglevel)
    self.test_match_whole_sequence_with_pattern_of_atomic_constraints(myloglevel)
    self.test_match_inside_sequence_of_atomic_constraints(myloglevel)
    self.test_match_multiple_inside_sequence_of_atomic_constraints(myloglevel)
    self.test_match_unpresent_inside_sequence_of_atomic_constraints(myloglevel)
    self.test_match_at_the_sequence_begining_quantifier_at_least_one_on_atomic_constraint(myloglevel)
    self.test_match_inside_sequence_quantifier_at_least_one_on_atomic_constraint(myloglevel)
    self.test_match_inside_sequence_at_least_one_including_negation_on_atomic_constraint(myloglevel)
    self.test_match_inside_sequence_surrounded_at_least_one_complex_class_constraint(myloglevel)
    self.test_match_inside_sequence_at_least_one_including_negation_in_class_constraint(myloglevel)
    self.test_match_at_the_ending_sequence_quantifier_at_least_one_on_atomic_constraint(myloglevel)
    self.test_match_inside_sequence_class_constraint(myloglevel)
    self.test_match_inside_sequence_quantifier_at_least_one_on_class_constraint(myloglevel)
    self.test_match_inside_sequence_quantifier_option_on_atomic_constraint(myloglevel)
    self.test_search_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint(myloglevel)
    self.test_search_partially_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint(myloglevel)
    self.test_search_partially_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint_with_trailer(myloglevel)
    self.test_search_unpresent_pattern_wi_surrounded_quantifier_option_on_atomic_constraint(myloglevel)
    self.test_search_quantifier_option_at_the_pattern_beginning_on_atomic_constraint(myloglevel)
    self.test_search_quantifier_option_at_the_pattern_end_on_atomic_constraint(myloglevel)
    self.test_search_multiple_consecutive_quantifier_option_inside_the_pattern_on_atomic_constraint(myloglevel)
    self.test_search_quantifier_any_inside_the_pattern_on_atomic_constraint(myloglevel)
    self.test_search_quantifier_any_at_the_pattern_beginning_on_atomic_constraint(myloglevel)
    self.test_search_quantifier_any_at_the_pattern_end_on_atomic_constraint(myloglevel)
    self.test_search_quantifier_any_inside_the_pattern_on_non_present_atomic_constraint(myloglevel)
    self.test_findall_at_multiple_locations_in_the_pattern_on_atomic_constraint(myloglevel)
    self.test_findall_any_atomic_class(myloglevel)
    self.test_findall_match_atomic_class(myloglevel)


    
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  tests = TestPyrata()
  
  accuracy=tests.testSuccess/float(tests.testCounter)
  print ("PyRATA - testCounter=",tests.testCounter,'; testSuccess=',tests.testSuccess,'; accuracy=',accuracy)