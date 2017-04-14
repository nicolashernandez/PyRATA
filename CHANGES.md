Revision History
================

v0.3.0 (April 14, 2017)
---------------------
* File creation of CHANGES.md 
* File creation of doc/user-guide.rst
* Management of ^ and $ symbols in grammar parsing and pattern engine 
* Management of | (alternative sequence of steps) with quantifiers in grammar parsing and pattern engine 
* api/engine syntactic_pattern_parser code refactoring to define two methods for getting the position in lexdata and the other for getting the refered form of the pattern step (previously done via p.lexer.patternStep and setPatternStep)