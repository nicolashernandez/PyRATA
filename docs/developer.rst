Last version of this document is April 14 2017

Syntactic parsing
---------------------

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


When debugging or making the syntactic pattern parser evolve, edit syntactic_analysis re_method and uncomment the exit() line to force the program interruption.
Doing that, you will have access to the parser grammar present in the parser.out temporary file.

Group, chunk, alternatives
-------------------------
A __group__ is a mechanism to refer to some sub-parts of the pattern. Surrounding parenthesis are used to mark the wanted sub-parts. A sub-part of the pattern is a sequence of steps (at least one).
A __chunk__ is ...




Implementing embedded groups (sequence of step tokens) 
-------------------------

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

  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN :      can   extend pattern='pos~"DT|JJ|NN.*"+' annotation={'chunk1':'NP'} iob = True 
  PP: {<IN><NP>}               # Chunk prepositions followed by NP :  may   extend pattern='pos="IN" chunk1-"NP"' annotation={'chunk2':'PP'} iob = True 
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments :    might extend pattern='pos~"VB.*" (chunk1-"NP"|chunk2-"PP"|chunk3-"CLAUSE")+$' annotation={'chunk4':'VP'} iob = True
  CLAUSE: {<NP><VP>}           # Chunk NP, VP                         might extend pattern='chunk1-"NP" chunk4-"VP"' annotation={'chunk3':'CLAUSE'} iob = True

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
