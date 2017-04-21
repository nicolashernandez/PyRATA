Revision History
================


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

