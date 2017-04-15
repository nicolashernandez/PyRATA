
Project development
****************************

Roadmap
============

Last report
-----------
The following test, test_search_groups_wi_matched_quantifiers_in_data, fails.
How to set quantifiers to groups which are not alternatives...

The compiled pattern is a list of quantified steps. 
The groups are an external data structure which refers to some range in this list.
The alternatives are specific steps made of lists of quantified steps. The depth does not go further (only two levels). Due to the current implementation and also about its strange meaning (depending on the alternative the group will not be systematic), alternatives should not admit groups (though the grammar allows it).

But how to allow quantifiers on groups ? The solution seems to come to represent groups as embedded lists of quantified steps like alternatives...

A|B, where A and B can be arbitrary REs, creates a regular expression that will match either A or B. An arbitrary number of REs can be separated by the '|' in this way. This can be used inside groups (see below) as well.

# ----------------------------------
Pattern:   raw="It" (raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")

# Syntactic structure parsed:
  [None, 'raw="It" ']
  [None, 'raw="is"']
  ['*', 'pos="JJ"']
  [None, 'pos="JJ" ']
  [None, 'raw="and"']
  [None, 'pos="JJ"']
  [None, 'raw="to"']
('# Must start the data=\t', False)
('# Must end the data=\t', False)
('# Group_pattern_offsets_group_list=', [[1, 2], [3, 5], [5, 6], [2, 6], [2, 6], [6, 7], [0, 7]])
('# Ordered group_pattern_offsets_group_list=', [[0, 7], [1, 2], [2, 6], [2, 6], [3, 5], [5, 6], [6, 7]])
  group 0 = [[None, 'raw="It" '], [None, 'raw="is"'], ['*', 'pos="JJ"'], [None, 'pos="JJ" '], [None, 'raw="and"'], [None, 'pos="JJ"'], [None, 'raw="to"']]
  group 1 = [[None, 'raw="is"']]
  group 2 = [['*', 'pos="JJ"'], [None, 'pos="JJ" '], [None, 'raw="and"'], [None, 'pos="JJ"']]
  group 3 = [['*', 'pos="JJ"'], [None, 'pos="JJ" '], [None, 'raw="and"'], [None, 'pos="JJ"']]
  group 4 = [[None, 'pos="JJ" '], [None, 'raw="and"']]
  group 5 = [[None, 'pos="JJ"']]
  group 6 = [[None, 'raw="to"']]
# ----------------------------------

# ----------------------------------
   Pattern:  (pos="IN") (raw="a" raw="tea" | raw="a" raw="cup" raw="of" raw="coffee" | raw="an" raw="orange" raw="juice" ) !pos=";"

# Syntactic structure parsed:
  [None, 'pos="IN"']
  [ None
    [[None, 'raw="a" '], [None, 'raw="tea" ']]
    [[None, 'raw="a" '], [None, 'raw="cup" '], [None, 'raw="of" '], [None, 'raw="coffee" ']]
    [[None, 'raw="an" '], [None, 'raw="orange" '], [None, 'raw="juice" ']]
  ]
  [None, '!pos=";"']
# Must start the data=   False
# Must end the data=   False
# Group_pattern_offsets_group_list= [[0, 1], [1, 2], [0, 3]]
# Ordered group_pattern_offsets_group_list= [[0, 3], [0, 1], [1, 2]]
  group 0 = [[None, 'pos="IN"'], [None, [[[None, 'raw="a" '], [None, 'raw="tea" ']], [[None, 'raw="a" '], [None, 'raw="cup" '], [None, 'raw="of" '], [None, 'raw="coffee" ']], [[None, 'raw="an" '], [None, 'raw="orange" '], [None, 'raw="juice" ']]]], [None, '!pos=";"']]
  group 1 = [[None, 'pos="IN"']]
  group 2 = [[None, [[[None, 'raw="a" '], [None, 'raw="tea" ']], [[None, 'raw="a" '], [None, 'raw="cup" '], [None, 'raw="of" '], [None, 'raw="coffee" ']], [[None, 'raw="an" '], [None, 'raw="orange" '], [None, 'raw="juice" ']]]]]
# ----------------------------------

TODO list following a decreasing priority order.
-------------------------------

* take the pattern of the group test and try to design its embedded structure  

  how to represent groups in that ? 
  Dynamically when parsing the data. Each embedded list is a group. We do not use the group_list built at compilation time. But during the data parsing, at each recursive call of parsing semantic we build the groups.

Pattern:   raw="It" (raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")
[list-of
  [quantified, step],
  [quantified, [_alternative [_sequence-of [quantified, step]]]]
]
with step -> [quantified, [_alternative [_sequence-of [quantified, step]]]]


self.getLexer().lexer.pattern_steps = [
  [None, 'raw="It" '],
  [None, [[[None, 'raw="is"']]]],
  [None, [[
    [None, [[ 
      ['*', 'pos="JJ"'],
      [None, [[
        [None, 'pos="JJ" '], 
        [None, 'raw="and"']]]],
      [None, [[
        [None, 'pos="JJ"']]]]]]]
    ]]],  
  [None, [[
    [None, 'raw="to"']]]]
]
[
  [None, 'raw="A" '],
  [None, [[[None, 'raw="B"']]]],
  [None, [[
    [None, [[ 
      ['*', 'raw="C"'],
      [None, [[
        [None, 'raw="C" '], 
        [None, 'raw="D"']]]],
      [None, [[
        [None, 'raw="E"']]]]]]]
    ]]],  
  [None, [[
    [None, 'raw="F"']]]]
]

pour remettre dans un état normal il faut rechanger des trucs 
Dans syntactic_analysis dans re_method
Dans semantic_analysis à la ligne : 
 if not(l.lexer.pattern_must_match_data_end) or (l.lexer.pattern_must_match_data_end and data_cursor == len(data)):
  avant il n'y avait pas l'extend
    et le test me semble bancal if (len(matcheslist) ==0):
          #if matcheslist_extension == None:  
          j'hésite avec           #if matcheslist_extension == None:  
      après avoir fait tourner la batterie de test j'obtiens des erreurs avec  #if (len(matcheslist) ==0): et non l'autre

tester sans les groupes aussi
ok jusqu'ici

il faut prendre un exemple plus simple
un groupe d'un step seul
un groupe d'un step et un non groupe
un groupe de deux step
un embedded de groupes

* run test group and compare the trace wi and without the line p.lexer.step_already_counted = 0 in p_step_group single make it works but fails for groups handling
* (pos="VB" pos="DT"? pos="JJ"* pos="NN" pos="."|pos="FAKE")+ works but not (pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")+ ; adding         p.lexer.step_already_counted = 0 in p_step_group single make it works but fails for groups handling


* api/engine revise annotate, sub, extend, and update method signatures for working with kwargs
* grammar implement IOB operator to handle sequence of tokens with a BIO value as a single token
* api/engine re implement insert, delete (sub with [] ; check), insert-to-the-leftmost (~ sub with reference)... 
* api/engine implement the position (from which word token position we start to search) and the search for annotate (not finditer) 
* communication update README with alternatives groups, ^$
* api/engine module re implement match
* api/engine the b*b case exploration in semantic_analysis ; currently check only the next step, but should explore as many as iter !
* quality implement logging facility
* communication packaging and distributing publish On PyPI
* communication user/developer reorganize README into specific docs : quick overview vs user guide, developer guide, roadmap pages
* communication structure the documentation http://www.sphinx-doc.org/en/stable/ ; publish on github pages
* quality evaluate performance http://www.marinamele.com/7-tips-to-time-python-scripts-and-control-memory-and-cpu-usage
* quality evaluate performance comparing to pattern and python 3 chunking (see the use example and show how to do similar)
* quality evaluate performance time `[pos="NNS" | pos="NNP"]`, `pos~"NN[SP]"` and 'pos~"(NNS|NNP)"' are equivalent forms. They may not have the same processing time.
* quality improve performance (memory and time) ; evaluate the possibility of doing the ply way to handle the debug/tracking mode
* grammar implement group alternative so they can be used to handle IOB-chunk operator
* grammar implement group reference so they can be matched later in the data with the \number special sequence
* grammar implement wildcards (so far handled by a `'!b*'` in `'!b* b'`
* grammar does class atomic with non atomic contraint should be prefered to not step to adapt one single way of doing stuff: partofclassconstraint -> NOT classconstraint more than step -> NOT step ; but the latter is simpler so check if it is working as expected wi quantifier +!pos:"EX" = +[!pos:"EX"])
* grammar allow grammar with multiple rules (each rule should have an identifier... and its own groupindex)
* grammar move the python methods as grammar components
* grammar think about the context notion 
* api/engine implement lex.lex(reflags=re.UNICODE)
* communication developer make diagrams to explain process and relations between files
* quality test complex regex as value
* quality code handle the test case of error in the patterns
* quality code test re methods on Compiled regular expression objects 
* quality code end location is stored several times with the expression rules ; have a look at len(l.lexer.groupstartindex): and len(l.lexer.groupendindex): after parsing in pyrata_re methods to compare 
* quality see the pattern search module and its facilities

Achieved
=============================
Done...

Grammar
-------------------------------

* implement sequence parsing
* implement CLASS OF tokens (parsing and semantic analysis with logical and/or/not operators and parenthesis)
* implement quantifier AT_LEAST_ONE
* implement quantifier OPTIONAL
* implement quantifier ANY
* implement surface EQ comparison operator for atomic constraint 
* implement list inclusion operator for atomic constraint 
* implement REGEX comparison operator for atomic constraint 
* implement groups
* implement operator to search the pattern from the begining ^ and/or to the end $
* implement alternatives groups

API and regex engine
-------------------------------

* module re implement search
* module re implement findall
* module re implement finditer
* module re implement compile
* module re compiled re object implement
* module nltk implement methods to turn nltk structures (POS tagging, chunking Tree and IOB) into the pyrata data structure 
* make modular pyrata_re _syntactic_parser and semantic_parser : creation of syntactic_analysis, syntactic_pattern_parser, semantic_analysis, semantic_step_parser,
* module re implement CRUD operations on data such as sub, update and extend features -- kind of annotation method -- (optionally in a BIO style)


Communication and code quality
-------------------------------

* write README with short description, installation, quick overview sections
* home made debugging solution for users when writting patterns (e.g. using an attribute name not existing in the data) ; wirh verbosity levels
* a test file 
* packaging and distributing package the project (python module, structure, licence wi copyright notice, gitignore)
* packaging and distributing configure the project 

