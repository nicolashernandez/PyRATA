Last version of this document is April 14 2017


A look at the grammar...
------------------
 ... for whom who are interested in ...

:: 

    Rule 0     S' -> expression
    Rule 1     expression -> <empty>
    Rule 2     expression -> quantified_step_group_list
    Rule 3     expression -> BEFORE_FIRST_TOKEN quantified_step_group_list
    Rule 4     expression -> quantified_step_group_list AFTER_LAST_TOKEN
    Rule 5     expression -> BEFORE_FIRST_TOKEN quantified_step_group_list AFTER_LAST_TOKEN
    Rule 6     quantified_step_group_list -> quantified_step_group_list quantified_step_group
    Rule 7     quantified_step_group_list -> quantified_step_group
    Rule 8     quantified_step_group -> step_group
    Rule 9     quantified_step_group -> step_group OPTION
    Rule 10    quantified_step_group -> step_group ATLEASTONE
    Rule 11    quantified_step_group -> step_group ANY
    Rule 12    step_group -> step
    Rule 13    step_group -> NOT step_group
    Rule 14    step_group -> LPAREN step_group_class RPAREN
    Rule 15    step_group_class -> quantified_step_group_list
    Rule 16    step_group_class -> step_group_class OR quantified_step_group_list
    Rule 17    step -> single_constraint
    Rule 18    step -> LBRACKET constraint_class RBRACKET
    Rule 19    constraint_class -> constraint_class AND constraint_class_part
    Rule 20    constraint_class -> constraint_class OR constraint_class_part
    Rule 21    constraint_class -> constraint_class_part
    Rule 22    constraint_class_part -> single_constraint
    Rule 23    constraint_class_part -> LPAREN constraint_class RPAREN
    Rule 24    constraint_class_part -> NOT constraint_class
    Rule 25    single_constraint -> NAME EQ VALUE
    Rule 26    single_constraint -> NAME MATCH VALUE
    Rule 27    single_constraint -> NAME IN VALUE 
    Rule 27    single_constraint -> NAME CHUNK VALUE 


When debugging or making the syntactic pattern parser evolve, edit syntactic_analysis re_method and uncomment the exit() line to force the program interruption.
Doing that, you will have access to the parser grammar present in the parser.out temporary file.

Group, chunk, alternatives
-------------------------
A __group__ is a mechanism to refer to some sub-parts of the pattern. Surrounding parenthesis are used to mark the wanted sub-parts. A sub-part of the pattern is a sequence of steps (at least one).
A __chunk__ is ...


Syntactic pattern parsing
-------------------------------
Initialy I wanted
* records the groups
* keeps trace of their offsets
* because of cycle among the parsing rules, have a processing counter (indeed a form and a group of the form should have the same offsets and the same step index)

All these problems were solved by adopting an embedding structure (the position of the embedding in the sup-list gives the offset of the group).





The compiled pattern structure
-------------------------------

The result of the compilation stage (aka the syntactic_pattern_parser analysis) is a tree, that represents  sequence of steps, groups and alternatives, and the specification of the pattern borders.

Steps, groups and alternatives can be quantified. An alternative is a group too (can be refered) and has to be marked by parenthesis.
Alternatives should not admit sub-groups (though the grammar allows it) since depending on the match of alternative option the sub group will not be systematically availlable. 
.. so this is not allowed: A|B, where A and B can be arbitrary REs, creates a regular expression that will match either A or B. An arbitrary number of REs can be separated by the '|' in this way. This can be used inside groups (see below) as well.


a list of steps

a step could be simple i.e. can be a list made of a quantifier and step constraints as String 
::
  
Pattern:   raw="It" (raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")
CompiledPattern.pattern_steps = [
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

or a step can be more complex to represent a quantified alternatives 

TODO take the log of the test from group test to explain the embeddings

  [list-of
    [quantified, step],
    [quantifier, [_alternatives-list-of [_sequence-of [quantifier, step]]]]
  
  with step can be simple or [quantified, [_alternative [_sequence-of [quantified, step]]]]

The procedure to develop and debug the group, alternative was take the pattern of the group test and try to design its embedded structure  

Pour ne produire que la compilation alors activate the exit in syntactic_analysis dans re_method


    pattern_steps -> [ part_of_pattern_steps_list ]
    part_of_pattern_steps_list -> step
    part_of_pattern_steps_list -> part_of_pattern_steps_list step
    step -> [QUANTIFIER simple_step]
    step -> [QUANTIFIER [complex_step]]
    complex_step ->  part_of_alternatives_list s 

    Rule 6     quantified_step_group_list -> quantified_step_group_list quantified_step_group
    Rule 7     quantified_step_group_list -> quantified_step_group

Implementing embedded groups (sequence of step tokens) 
-------------------------

DEPRECATED

::

   Production= (single_constraint->...) raw="is"
        Debug: step_already_counted=0
    Production= (step->...) raw="is"
    Production= (step_group->step) raw="is"
    Production= (quantified_step_group->step_group) raw="is"
        Debug: quantified_step_index++
        Debug: store the step offsets corresponding to the character positions of lexdata i.e. 10->1 to 18->2
        Debug: step_already_counted=1
    Production= (quantified_step_group_list->quantified_step_group) raw="is"
        Debug: set last_group_offsets_candidate wi lexdata from 10 to 18
    Production= (step_group_class->quantified_step_group_list) raw="is"
    Production= (step_group->LPAREN step_group_class RPAREN) (raw="is") 
        Debug: group detected from 1 to 2 step(s)
    Production= (quantified_step_group->step_group) (raw="is") 
    Production= (quantified_step_group_list->quantified_step_group_list quantified_step_group) raw="It" (raw="is") 
        Debug: set last_group_offsets_candidate wi lexdata from 0 to 20
    Production= (single_constraint->...) pos="JJ"
        Debug: step_already_counted=0


1. when quantified_step_group is matched and when the current match does not correspond to a group content (surrounded by PAREN) then we increment the step, the store the step offsets corresponding to the character positions of lexdata i.e. 10->1 to 18->2

2. when quantified_step_group_list is matched then we keep in mind the last couple of stored character positions

3. when step_group->LPAREN step_group_class RPAREN is match then we consider it as as group and we store it at the corresponding step offsets of the last couple of stored character positions.

step_already_counted is used to prevent from storing quantified_step_group when they have already been stored wo PAREN, neither from incrementing step index... It is set to 1 at quantified_step_group and 0 for a single_constraint.



chunk operator 
-------------------------


Working with __chunks in IOB tagged format__. As mentioned in [nltk book](http://www.nltk.org/book/ch07.html), _The most widespread file representation of chunks uses IOB tags. In this scheme, each token is tagged with one of three special chunk tags, I (inside), O (outside), or B (begin). A token is tagged as B if it marks the beginning of a chunk. Subsequent tokens within the chunk are tagged I. All other tokens are tagged O. The B and I tags are suffixed with the chunk type, e.g. B-NP, I-NP. Of course, it is not necessary to specify a chunk type for tokens that appear outside a chunk, so these are just labeled O. An example of this scheme is shown below_  

    >>> data = [{'pos': 'NNP', 'chunk': 'B-PERSON', 'raw': 'Mark'}, {'pos': 'NNP', 'chunk': 'I-PERSON', 'raw': 'Zuckerberg'}, {'pos': 'VBZ', 'chunk': 'O', 'raw': 'is'}, {'pos': 'VBG', 'chunk': 'O', 'raw': 'working'}, {'pos': 'IN', 'chunk': 'O', 'raw': 'at'}, {'pos': 'NNP', 'chunk': 'B-ORGANIZATION', 'raw': 'Facebook'}, {'pos': 'NNP', 'chunk': 'I-ORGANIZATION', 'raw': 'Corp'}, {'pos': '.', 'chunk': 'O', 'raw': '.'}] 


The idea to handle chunks is to use the chunk operator `-` as a rewriting rule to turn the constraint into two with equality operator (e.g. `chunk-"PERSON"` would be rewritten in `chunk="B-PERSON" chunk="I-PERSON"*`).
This could be done before starting the syntax analysis (compilation stage) or when building the compilation representation.

Without a correct management of step sequences as token, some issues can be encountered: 1) support of quantifiers on chunk constraints (e.g. `chunk-"PERSON"*`), 2) inclusion of chunk constraints in classes (e.g. `[chunk-"PERSON" & raw="Mark"]`). 


Motivation for handling chunks and alternatives 
-------------------------

  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN :      can   
    extend pattern='pos~"DT|JJ|NN.*"+' annotation={'ch1':'NP'} iob = True 
  
  PP: {<IN><NP>}               # Chunk prepositions followed by NP :  may   
    extend pattern='pos="IN" ch1-"NP"' annotation={'ch2':'PP'} iob = True 
           pattern='pos="IN" (ch1="B-NP" ch1="B-NP"*)"

  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments :    might 
    extend pattern='pos~"VB.*" (ch1-"NP"|ch2-"PP"|ch3-"CLAUSE")+$' annotation={'ch4':'VP'} iob = True
           pattern='pos~"VB.*" (ch1="B-NP" ch1="B-NP"*|ch2="B-PP" ch2="B-PP"*|ch3="B-CLAUSE" ch3="B-CLAUSE"*)+$'

  CLAUSE: {<NP><VP>}           # Chunk NP, VP                         might 
    extend pattern='ch1-"NP" ch4-"VP"' annotation={'ch3':'CLAUSE'} iob = True
           pattern='(ch1="B-NP" ch1="B-NP"*) (ch4="B-VP" ch4="B-VP"*)'

  Since various type of chunks are related by hierachical relation, they should be considered at various levels and so we introduced various feature names for this purpose. When it is not flat structure, ...

  Like for nltk.chunk the third rule should be called again for detecting VP based on CLAUSE 





Developpers tips
---------

* access to parsed lextoken from the grammar, the grammar/pattern step, and the data token with length, Line Number and Position based on http://www.dabeaz.com/ply/ply.html#ply_nn33
reporting-parse-errors-from-ply-to-caller-of-parser
* code handle errors wo fatal crash http://stackoverflow.com/questions/18046579/
* code fix use test_match_inside_sequence_at_least_one_including_negation_on_atomic_constraint and test_match_inside_sequence_at_least_one_including_negation_in_class_constraint
* grammar parsing solve the shift/reduce conflict with AND and OR  ; The parser does not know what to apply between Rule 10    classconstraint -> partofclassconstraint,  and   (Rule 11    classconstraint -> partofclassconstraint AND classconstraint and Rule 12  or  classconstraint -> partofclassconstraint OR classconstraint) ; sol1 : removing Rule 10 since classconstraint should only be used to combine atomic constraint (at least two); but consequently negation should be accepted wo class (i.e. bracket) and with quantifier if so ; the use of empty rule lead to Parsing error: found token type= RBRACKET  with value= ] but not expected ; sol2 : which solve the problem, inverse the order partofclassconstraint AND classconstraint  -> classconstraint AND partofclassconstraint
* Warning: code cannot rename tokens into lextokens in parser since it is Ply 
* Warning: ihm when copying the grammar in the console, do not insert whitespace ahead
* code separate lexer, syntactic parser and semantic parser in distinct files http://www.dabeaz.com/ply/ply.html#ply_nn34 
* fix parsing bug with pos~"VB." *[!raw="to"] raw="to", +[pos~"NN.*" | pos="JJ"] pos~"NN.*", *[pos~"NN.*" | pos="JJ"] pos~"NN.*", 



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