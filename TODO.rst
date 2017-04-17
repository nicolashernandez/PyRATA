
Project development
****************************

Roadmap
============

Last report
-----------


TODO list following a decreasing priority order.
-------------------------------

* dispatch merged group tests in individual tests
* clean deprecated verbosity argument compiled_pattern_re, syntactic* and semantic*, and may be test* ?
* revise the __main__ section of each py
* grammar + api/engine add the chunk operator
* api/engine check negation of groups/alternatives
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

