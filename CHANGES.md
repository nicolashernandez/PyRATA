Revision History
================

v0.4.1 
---------------------
* demo implementation of phrase-extraction.py (Justeson and Katz 1995) and (Handel et al 2016)
* demo implementation of sentiment-analysis.py: Illustration  of implementation of some constraints present in (Hutto et al. 2014), evaluation with nltk movie_reviews corpus
* api/engine implementation of match and fullmatch methods + some tests
* api/engine implementation of pos and endpos arguments for all matching methods + some tests
* grammar implementation of backslash in constraint value
* enhancement of pyrata_re.py wi data path parameter, match and fullmatch methods, nlp with lc (lowercase) feature, lexicons parameter
* fix+change the behavior of re methods when pos was lower than 0 or endpos parameter was greater than len(data), realign on O or len(data) instead of returning None
* fix re finditer method when data was empty, a variable was not correctly initialized
* fix nfa last_state_id computation for such a case '(a~"A|B"+) (b="B")' "[{'c':'C'}, {'a':'A'}, {'a':'A', 'b':'B'}, {'d':'D'}]" the id was a matching state but not mandatory a final state #M
* fix re and nfa compile to pass lexicons argument in the CompiledPattern.compile() method
* fix the `ImportError: No module named 'graph_tool'` issue by specifying the graph_tool installation procedure. 
* doc user-guide grammar clarification about the change in 0.3.3 (negative constraint are for now only allowed in class elements)
* enhancement of the time processing by a factor of 4: implementation of a dedicated deepcopy method instead of the one from copy module
* code refactoring by separating compiled_pattern from nfa
* minor user-guide enhancements

v0.4 (October 12, 2017)  
---------------------
* api/engine pattern parser and search engine replaced by Thompson NFA implementation of Guan Gui  
* api/engine extension of the finding methods with the possibility to set a greedy or a reluctant matching mode
* grammar extension of the language to consider '.' as wildcard
* ihm creation of a command line script pyrata_re.py with PDF drawing facility to export NFA
* api/engine DFA extraction facility corresponding to matched parts of NFA on data
* quality revise do_tests.py code by using the unittest library + tests extension
* quality do_benchmark.py on simple noun phrases + includes comparison with spaCy
* fix data immutability in nfa annotate (extend...) which works on a data copy. Switching 'data_copy = list(data)' with 'data_copy  = copy.deepcopy(data)'
* fix re extend fix action from extend to 'extend' with quotes
* doc user-guide revised: grammar modification with wildcard, maching mode exploration (global, greedy, reluctant), pyrata_re, DFA generation, pdf export, logging, time performance
* logging facilities partially maintained  
        

v0.3.3/v0.3.4 (July 25, 2017) ; latter one wo logging instructions to run faster
---------------------
* implement annotation methods (annotate, sub, update, extend) for working with a compiled pattern (see compiled_pattern_re) 
* code refactoring to increase time performance: removing the semantic_step_parser and replacing it by compiling the step tokens into symbolic expressions (use the sympy module) evaluated on fly for each data token (changes in syntactic_pattern_parser and in evaluate of semantic_pattern_parser)
* grammar does not accept anymore negative pattern step. '!pos="NNS"+' should be rewritten '[!pos="NNS"]+'
* code refactoring to increase time performance: releasing a pip version without I/O logging and a verbose git version with scripts to generate the opimized pip version 
* code refactoring to increase time performance: substituting string concat to format 
* added code to benchmark
* revised user-guide (logging, time performance and grammar modification)
* removed old logging mechanism (verbosity argument) from the main code
* fixed logging issues (output syntactic parsing problem and removing old verbosity facility) 
* fixed minor bug when falling in the b+b case (plus quantifier) of semantic_pattern_parser when finding all occurrences of '(pos="DT"? pos="JJ"*)+ pos="NN"' in the brown corpus 


v0.3.2 (April 22, 2017)
---------------------
* added the chunk operator (as a re rewritting rule)
* revised user-guide (group, alternative, chunk, ^$, compiled sections)
* added more tests


v0.3.1 (April 17, 2017)
---------------------
* first upload on pypi server
* adoption of a pattern compiled tree structure to represent sequences of quantified steps, quantified groups and alternatives
* syntactic_pattern_parser supplies a pattern compiled tree structure
* semantic_analysis consumes a pattern compiled tree structure
* using logging module for syntactic_pattern_parser and semantic_analysis
* renamed semantic_analysis into semantic_pattern_parser
* renamed syntactic_analysis.py into compiled_pattern_re
* added the chunk operator (as a re rewritting rule)
* deprecated verbosity argument

v0.3.0 (April 14, 2017)
---------------------
* File creation of CHANGES.md 
* File creation of doc/user-guide.rst
* Management of ^ and $ symbols in grammar parsing and pattern engine 
* Management of | (alternative sequence of steps) with quantifiers in grammar parsing and pattern engine 
* api/engine syntactic_pattern_parser code refactoring to define two methods for getting the position in lexdata and the other for getting the refered form of the pattern step (previously done via p.lexer.patternStep and setPatternStep)

