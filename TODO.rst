
Project development
****************************

Roadmap
============

Last report
-----------


TODO list (almost following a decreasing priority order)
-------------------------------

* communication make tutorial to recognize NP and NP of NP, clause, Opinion mining or sentiment analysis
* quality - do_benchmark.py - evaluate performance time `[pos="NNS" | pos="NNP"]`, `pos~"NN[SP]"` and 'pos~"(NNS|NNP)"', more fined grained comparison with alternatives
* ihm pyrata_re add more features such as input-file lexicon, lexicon-file, output-dfa, output-group, 
* communication organize the documentation http://www.sphinx-doc.org/en/stable/ ; publish on github pages
* communication developer write code explanation: in particular Running an NFA ...
* communication developer make diagrams to explain process and relations between files
* quality revise logging information
* quality test - anchors wi each matching methods
* quality test - if lexicon argument kwargs is well handled in re compile is it necessary?
* quality code - refactor nfa.py to dissociate the pattern compilation (nfa build) from the data parsing (nfa run)
* quality code - refactor nfa.py to merge re search method with finditer/findall 
* quality test - systematize the tests (3 re methods + DFA in greedy/reluctant mode with aa .a a?a a*a a+a in caaaad (then aaaa/aabaa/caabaad) then the same with quantifier on the second char ; done in the first data configuration ; also consider ab a?b a*b a+b (and quantifier on last char) in cababd/abab ; some tests are already existing
* quality test - complex regex as value
* quality test - patterns error catching
* quality test - the chunk operator
* quality test - re methods on Compiled regular expression objects 
* api/engine - fix - explore the following behavior       
      >>> data = [{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'PyRATA', 'pos': 'NNP'}]
      >>> pyrata_re.search('(pos="JJ" | (pos="JJ" pos="NNS") )', data)
      <pyrata.re Match object; groups=[[[{'raw': 'fast', 'pos': 'JJ'}], 2, 3], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]>
      >>> pyrata_re.search('(pos="JJ" | (pos="JJ" pos="NNS") )', data)
      <pyrata.re Match object; groups=[[[{'raw': 'fast', 'pos': 'JJ'}], 2, 3], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]>
* api/engine - fix - the NFA _repr_ because it does not display all the states...
* api/engine - fix/revise code - In __step_special_state (i.e. when running a NFA), I add various fix since id(cs)={} was absent from NFA.states_dict. Should have be added during NFA build ! We store now.'.format(state.id)) ; Revise the code to find where to place the storing code during the build
* api/engine - apart from String, allow the processing of primitive types such as Boolean and Integer 
  python3 pyrata_re.py 'int="1"' "[{'int':1, 'str':'un', 'bool':True}]"
  python3 pyrata_re.py 'bool="True"' "[{'int':1, 'str':'un', 'bool':True}]"
* api/engine - revise - by default only the zero group is compared with eq and ne ; should be all the groups ?
* api/engine - implement methods to save, load and run previously saved DFA
* api/engine - implement draw option in main API to generate drawing when compiling
* api/engine - integrate match/exact_match in the re API, and make it evolve as search (in particular to generate DFA)
* api/engine - implement split, sub... in compiled_pattern_re module
* api/engine - implement insert, delete (sub with [] ; check), insert-to-the-leftmost (~ sub with reference)... 
* api/engine - implement "possessive matching" mode
* api/engine - implement re : see the pattern search module and its facilities
* quality code revise the __main__ section of each py
* api/engine negation of groups/alternatives is not possible ; a step is possible by the concept of class
* grammar - allow escaped " character in constraint values - pattern_to_guiguan_nfa_pattern_input ; if a " occurs when in_constraint_value is true and when the previous char is \ then do not aso do not change the value of in_constraint_value
* grammar think of an alternative as re implementation of the chunk operator in the grammar.
* grammar implement predefined quantifiers {n} Match exactly n times; {n,} Match at least n times; {n,m} Match at least n but not more than m times
* grammar implement backreference group reference so they can be matched later in the data with the \number special sequence
* grammar allow grammar with multiple rules (each rule should have an identifier... and its own groupindex)
* grammar move the python methods as grammar components
* grammar think about the context notion 
* api/engine performance - parallelize NFA running, implementation cython ?
* api/engine implement lex.lex(reflags=re.UNICODE)



