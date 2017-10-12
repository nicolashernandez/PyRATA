Revision History
================


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

