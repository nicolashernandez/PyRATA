# PyRATA
PyRATA is an acronym which stands for "Python Rule-based feAture sTructure Analysis" or "Python Rule-bAsed Text Analysis".

# Description
Traditional regular expression (re) engines handle character strings; In other words lists of character tokens.
re are used to define patterns which are used to recognized some phenomena in texts.
In Natural Language Processing, they are the essence of the rule-based approach for analysing the texts.

But character strings are a poor data structure. In the present work, we aim at offering both a language and engine implementation for working on lists of token, a token being defined as a feature structure (right now a feature feature is only made of a set of attribute name/value (i.e. a map/dict) with primitive type as allowed value; more precisely in the current implementation only the String).

The objective is to offer a language and an engine to define patterns aiming at matching (parts of) feature structure lists. In the first version, the interpretation of patterns will be integrated in python operations.

In the most common use case, a token list is a data structure used to represent a sentence as sequence of words, each word token coming with a set of features. 
The data structure is not limited to the representation of sentences. It can also be used to represent a text, with the sentence as token unit. Each sentence with its own set of features.

# Install and run

## Requirement
PyRATA use the [PLY](http://www.dabeaz.com/ply/ply.html "PLY") implementation of lex and yacc parsing tools for Python (version 3.10).
One way to install it is:
    sudo pip3 install ply

## Run tests
    python3 test_pyrata.py

The main module is pyrata_re. It is the one you should import.


# How does it work?

## Concepts 

A grammar to parse. Right now a pattern. Which is made of 1 or several steps. A step is in its simplest form the specification of a single constraint. A step can be a quantified step or a class step (the latter aims at specify more than one constraints and conditions on them with logical operators ('and', 'or' and 'not')).

A data structure to parse too... on which the pattern is applied.

## Grammar

(as generated in parser.out)

    Rule 0     S' -> expression
    Rule 1     expression -> quantifiedstep
    Rule 2     expression -> quantifiedstep expression
    Rule 3     quantifiedstep -> step
    Rule 4     quantifiedstep -> OPTION step
    Rule 5     quantifiedstep -> ATLEASTONE step
    Rule 6     quantifiedstep -> ANY step
    Rule 7     step -> atomicconstraint
    Rule 8     step -> NOT step
    Rule 9     step -> LBRACKET classconstraint RBRACKET
    Rule 10    classconstraint -> partofclassconstraint
    Rule 11    classconstraint -> partofclassconstraint AND classconstraint
    Rule 12    classconstraint -> partofclassconstraint OR classconstraint
    Rule 13    partofclassconstraint -> atomicconstraint
    Rule 14    partofclassconstraint -> LPAREN classconstraint RPAREN
    Rule 15    partofclassconstraint -> NOT classconstraint
    Rule 16    atomicconstraint -> NAME IS VALUE

## parcours pour une règle note: des règles comme des items ordonnés d'une liste ?
textInitialCursor=0
textCursor=textInitialCursor
on parse la grammaire
si error de parsing: 
  si text non fini
    on inc textInitialCursor et set textCursor=textInitialCursor
    on réinitialise la grammaire
  sinon si texte fini
    fin
si pas d'erreur et on arrive à la fin (de la grammaire/d'une règle):
  on trace id règle, textInitialCursor, textCursor
  textInitialCursor=textCursor+1  et set textCursor=textInitialCursor
  on réinitialise la grammaire


# Roadmap

##  Done 
* implementation of token sequence parsing/semantic analysis with token an atomicconstraint
* implementation of class of tokens (parsing and semantic analysis with logical and/or/not operators and parenthesis)
* implementation of quantifier +
* lexer and parser as classes
* regex operation match 
* rename package, file, module, class, variable names
* improve the log experience by displaying parsed lextoken from the grammar, the grammar/pattern step, and the data token with length, Line Number and Position (based on http://www.dabeaz.com/ply/ply.html#ply_nn33)
* rename global step grammar -> patternStep and local into localstep (quantifiedStep is ambiguous since it is the name of the production just before expression)

## TODO
* move the code for testing the validity of a patternstep into the quantifier production rule and non in expression
* in pyrata_parser log if p.lexer.globalgrammarstepPosition < p.lexer.grammarsize: should works with string length since we cannot know a priori the size because of complex class

* fix global step count based on works on split(' ') when class constraints with multiple constraints 
* fix use test_match_inside_sequence_at_least_one_including_negation_on_atomic_constraint and test_match_inside_sequence_at_least_one_including_negation_in_class_constraint
* when a quantifier step is not valid, the parsing should be aborted wo waiting for expression parsing
* class atomic with non atomic contraint should be prefered to not step : partofclassconstraint -> NOT classconstraint more than step -> NOT step (to remove the latter)
* implzmznr optional quantifier: see quantifiedstep : step (or other) to restart the parser 
* implement tests in particular search then firstall (be careful for lexpos...)
* separte lexer, parser and semantic implementation in distinct files
* implement search * Si l'expression est trouvée, la fonction renvoie un objet symbolisant l'expression recherchée. Sinon, elle renvoie None.
* implement regex operation findall(grammar,data) which return a list of recognized feature structure sequences
* implement regex operation finditer : list of all the objects and their positions m.group(0) m.start() m.end()
* handling quantifiers *, ?
* parsing a whole text 
* si error dans le parsing de la grammaire récupération en sautant les tokens jusqu'au prochain ; en relançant la grammaire (pas tout à fait parce qu'il faut prévoir la progression dans le texte à analyser)
* handle errors wo fatal crash http://stackoverflow.com/questions/18046579/reporting-parse-errors-from-ply-to-caller-of-parser
* declare list of possible values for atomic constraints from a direct enumeration or from a file
* think about the context notion, and possibly about forcing the pattern to match from the begining ^ and/or to the end $
* regex operation in addition to match operation, offer the substitution sub/// and the annotation annotate/// ; the new feature is added to the current feature structure in a BIO style
* handle sequence of tokens with a BIO value as a single token
* extend the content of possible values of atomic constraints
* declare a regex as a value of atomic constraint 
* allow wildcards
* capture index of groups (identifiers required)
* reuse groups in regex
* make methods to turn nltk results into the input data structure
* lex.lex(reflags=re.UNICODE)
* move the python methods as grammar components
* allow grammar with multiple rules (each rule should have an identifier... and its own groupindex)
* Warning: when copying the grammar in the console, do not insert whitespace ahead


