# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
#
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pyrata_re

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class TestNlpRe(object):

  testCounter = 0
  testSuccess = 0

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main test method
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def test (self,description, pattern, data, expected, debug):
    ''' output the result in console '''
    print ('________________________________________________')
    print ('Test:',description)
    print ('Pattern:\t',pattern)
    print ('Data:\t\t',data)
    print ('Expected:\t',expected)

    result = pyrata_re.search(pattern, data, debug=debug)
    #print('Result:',l.lexer.finalresult,'; start:',l.lexer.groupstartindex,'; end:',l.lexer.groupendindex)
    #if debug:    
    print ('Result:',result) 
    if result == expected:
      print ('Test:',description, '- SUCCESS')
      self.testSuccess +=1
    else:
      print ('Test:',description, '- FAIL')
    self.testCounter +=1

    print ()
    
  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  # Test cases definitions
  # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def test_match_at_the_sequence_begining_is_atomic_constraint(self):
    description = 'match_at_the_sequence_begining_is_atomic_constraint'
    pattern = 'lem:"the"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}]
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}]
    self.test(description, pattern, data, expected, False)

  def test_match_whole_sequence_with_pattern_of_atomic_constraints(self):
    description = 'match_whole_sequence_with_pattern_of_atomic_constraints'
    pattern = 'pos:"DT" pos:"JJ" pos:"NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, pattern, data, expected, False)

  def test_match_inside_sequence_of_atomic_constraints(self):
    description = 'search and match inside a sequence of "is" atomic constraints'
    pattern = 'pos:"NN"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'beautiful', 'lem':'beautiful', 'pos':'JJ'}]
    expected = [{'raw':'cars', 'lem':'car', 'pos':'NN'}]
    self.test(description, pattern, data, expected, True)

  def test_match_at_the_sequence_begining_quantifier_at_least_one_on_atomic_constraint(self):
    description = 'match_at_the_sequence_begining_quantifier_at_least_one_on_atomic_constraint'
    pattern = 'pos:"DT" +pos:"JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]
    self.test(description, pattern, data, expected, False)

  def test_match_inside_sequence_quantifier_at_least_one_on_atomic_constraint(self):
    description = 'match_inside_sequence_quantifier_at_least_one_on_atomic_constraint'
    pattern = '+pos:"JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [{'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]
    self.test(description, pattern, data, expected, False)

  def test_match_at_the_ending_sequence_quantifier_at_least_one_on_atomic_constraint(self):
    description = 'match_at_the_ending_sequence_quantifier_at_least_one_on_atomic_constraint'
    pattern = '+pos:"JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]     
    expected = [{'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}]
    self.test(description, pattern, data, expected, False)

  def test_match_inside_sequence_class_constraint(self):
    description = 'match_inside_sequence_class_constraint'
    pattern = '[lem:"be" | raw:"is"]'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'are', 'lem':'be', 'pos':'VB'}]     
    self.test(description, pattern, data, expected, False)

  def test_match_inside_sequence_quantifier_at_least_one_on_class_constraint(self):
    description = 'match_inside_sequence_quantifier_at_least_one_on_class_constraint'
    pattern = '+[lem:"be" | raw:"is"]'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'are', 'lem':'be', 'pos':'VB'}]     
    self.test(description, pattern, data, expected, False)  

  def test_match_inside_sequence_at_least_one_including_negation_on_atomic_constraint(self):
    description = 'match_inside_sequence_at_least_one_including_negation_on_atomic_constraint'
    pattern = 'pos:"DT" !pos:"NN"+ pos:"NN"'
    data = [{'raw':'Here', 'lem':'here', 'pos':'ADV'}, {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]     
    self.test(description, pattern, data, expected, True) 

  def test_match_inside_sequence_at_least_one_including_negation_in_class_constraint(self):
    description = 'match_inside_sequence_at_least_one_including_negation_in_class_constraint'
    pattern = 'pos:"DT" [!pos:"NN"]+ pos:"NN"'
    data = [{'raw':'Here', 'lem':'here', 'pos':'ADV'}, {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'the', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}]     
    self.test(description, pattern, data, expected, False) 


  def test_match_inside_sequence_quantifier_option_on_atomic_constraint(self):
    description = 'match_inside_sequence_quantifier_option_on_atomic_constraint'
    pattern = '?pos:"ADV"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = None
    self.test(description, pattern, data, expected, False)

  def test_search_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint(self):
    description = 'search_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint'
    pattern = 'pos:"NN" ?pos:"VB" pos:"JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = [ {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]
    self.test(description, pattern, data, expected, True)

  def test_search_unpresent_pattern_wi_surrounded_quantifier_option_on_atomic_constraint(self):
    description = 'search_unpresent_pattern_wi_surrounded_quantifier_option_on_atomic_constraint'
    pattern = 'pos:"NN" ?pos:"ADV" pos:"JJ"'
    data = [{'raw':'The', 'lem':'the', 'pos':'DT'}, {'raw':'big', 'lem':'big', 'pos':'JJ'}, {'raw':'fat', 'lem':'fat', 'pos':'JJ'}, {'raw':'giant', 'lem':'giant', 'pos':'JJ'}, {'raw':'cars', 'lem':'car', 'pos':'NN'}, {'raw':'are', 'lem':'be', 'pos':'VB'}, {'raw':'amazing', 'lem':'amaze', 'pos':'JJ'}]     
    expected = None
    self.test(description, pattern, data, expected, False)    

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Declare here all the tests you want to run
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  def __init__(self):
    #self.test_match_at_the_sequence_begining_is_atomic_constraint()
    #self.test_match_whole_sequence_with_pattern_of_atomic_constraints()
    self.test_match_inside_sequence_of_atomic_constraints()
    #self.test_match_at_the_sequence_begining_quantifier_at_least_one_on_atomic_constraint()
    #self.test_match_inside_sequence_quantifier_at_least_one_on_atomic_constraint()
    #self.test_match_inside_sequence_at_least_one_including_negation_on_atomic_constraint()
    #self.test_match_inside_sequence_at_least_one_including_negation_in_class_constraint()
    #self.test_match_at_the_ending_sequence_quantifier_at_least_one_on_atomic_constraint()
    #self.test_match_inside_sequence_class_constraint()
    #self.test_match_inside_sequence_quantifier_at_least_one_on_class_constraint()
    #self.test_match_inside_sequence_quantifier_option_on_atomic_constraint()
    #self.test_search_present_pattern_wi_surrounded_quantifier_option_on_atomic_constraint()
    #self.test_search_unpresent_pattern_wi_surrounded_quantifier_option_on_atomic_constraint()

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  tests = TestNlpRe()
  
  accuracy=tests.testSuccess/float(tests.testCounter)
  print ("testCounter=",tests.testCounter,'; testSuccess=',tests.testSuccess,'; accuracy=',accuracy)