Syntactic parsing
---------------------


Rule 0     S' -> expression
Rule 1     expression -> <empty>
Rule 2     expression -> quantified_step_group_list
Rule 3     quantified_step_group_list -> quantified_step_group_list quantified_step_group
Rule 4     quantified_step_group_list -> quantified_step_group
Rule 5     quantified_step_group -> step_group
Rule 6     quantified_step_group -> step_group OPTION
Rule 7     quantified_step_group -> step_group ATLEASTONE
Rule 8     quantified_step_group -> step_group ANY
Rule 9     step_group -> step
Rule 10    step_group -> NOT step_group
Rule 11    step_group -> LPAREN step_group_class RPAREN
Rule 12    step_group_class -> quantified_step_group_list
Rule 13    step_group_class -> step_group_class OR quantified_step_group_list
Rule 14    step -> single_constraint
Rule 15    step -> LBRACKET constraint_class RBRACKET
Rule 16    constraint_class -> constraint_class AND constraint_class_part
Rule 17    constraint_class -> constraint_class OR constraint_class_part
Rule 18    constraint_class -> constraint_class_part
Rule 19    constraint_class_part -> single_constraint
Rule 20    constraint_class_part -> LPAREN constraint_class RPAREN
Rule 21    constraint_class_part -> NOT constraint_class
Rule 22    single_constraint -> NAME EQ VALUE
Rule 23    single_constraint -> NAME MATCH VALUE
Rule 24    single_constraint -> NAME IN VALUE




when debugging or making the syntactic pattern parser evolve
1. edit syntactic_analysis re_method and uncomment the exit() line to force the program interruption

you will have access to the parser.out dedicated for syntactic.

chunks (sequence of tokens) as token and sequences alternatives 
-------------------------
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

The current test wi multiple embedded PAREN reveals some potentials limits when not using the step_already_counted variable.

    raw="It" (raw="is") (( pos="JJ"* (pos="JJ" raw="and") (pos="JJ") )) (raw="to")


With Rule 13    step_group_class -> step_group_class OR quantified_step_group

    pattern = '(raw="a" raw="cup" raw="of" raw="coffee" | raw="a" raw="tea" )' 

gets
    
    # Error: syntactic parsing error - unexpected token type="NAME" with value="raw" at position 54. Search an error before this point.

compile with   
   # pattern = '((raw="a" raw="cup" raw="of" raw="coffee") | (raw="a" raw="tea" ))'

but groups are
group 0 = [[None, 'raw="a" '], [None, 'raw="cup" '], [None, 'raw="of" '], [None, 'raw="coffee"'], [None, 'raw="a" '], [None, 'raw="tea" ']]
group 1 = [[None, 'raw="a" '], [None, 'raw="cup" '], [None, 'raw="of" '], [None, 'raw="coffee"']]
group 2 = [[None, 'raw="a" '], [None, 'raw="tea" ']]
group 3 = [[None, 'raw="a" '], [None, 'raw="tea" ']]

Solved with
Rule 13    step_group_class -> step_group_class OR quantified_step_group_list

But groups are
group 0 = [[None, 'raw="a" '], [None, 'raw="cup" '], [None, 'raw="of" '], [None, 'raw="coffee" '], [None, 'raw="a" '], [None, 'raw="tea" ']]
group 1 = [[None, 'raw="a" '], [None, 'raw="tea" ']]


The groups should be

group 0 = [[[None, 'raw="a" '], [None, 'raw="cup" '], [None, 'raw="of" '], [None, 'raw="coffee"']], [[None, 'raw="a" '], [None, 'raw="tea" ']]]
group 1 = [[[None, 'raw="a" '], [None, 'raw="cup" '], [None, 'raw="of" '], [None, 'raw="coffee"']], [[None, 'raw="a" '], [None, 'raw="tea" ']]]

do we force to set PAREN ? 

easier for capturing the right alternative sequence

Handling chunk in pattern
-------------------------
Working with __chunks in IOB tagged format__. As mentioned in [nltk book](http://www.nltk.org/book/ch07.html), _The most widespread file representation of chunks uses IOB tags. In this scheme, each token is tagged with one of three special chunk tags, I (inside), O (outside), or B (begin). A token is tagged as B if it marks the beginning of a chunk. Subsequent tokens within the chunk are tagged I. All other tokens are tagged O. The B and I tags are suffixed with the chunk type, e.g. B-NP, I-NP. Of course, it is not necessary to specify a chunk type for tokens that appear outside a chunk, so these are just labeled O. An example of this scheme is shown below_  

    >>> data = [{'pos': 'NNP', 'chunk': 'B-PERSON', 'raw': 'Mark'}, {'pos': 'NNP', 'chunk': 'I-PERSON', 'raw': 'Zuckerberg'}, {'pos': 'VBZ', 'chunk': 'O', 'raw': 'is'}, {'pos': 'VBG', 'chunk': 'O', 'raw': 'working'}, {'pos': 'IN', 'chunk': 'O', 'raw': 'at'}, {'pos': 'NNP', 'chunk': 'B-ORGANIZATION', 'raw': 'Facebook'}, {'pos': 'NNP', 'chunk': 'I-ORGANIZATION', 'raw': 'Corp'}, {'pos': '.', 'chunk': 'O', 'raw': '.'}] 

The current implementation of the chunk operator is a rewriting rule which turns the constraint into two with equality operator (e.g. `chunk-"PERSON" [pos~"VB.*"]*` is rewritten in `chunk="B-PERSON" chunk="I-PERSON"* [pos~"VB.*"]*`) before starting the syntax analysis (compilation stage). 
Consequently the current implementation does not support quantifiers on chunk constraints (e.g. `chunk-"PERSON"*` is forbidden), neither the inclusion of chunk constraints in classes (e.g. `[chunk-"PERSON" & raw="Mark"]` is forbidden). 


 Before introducing the chunk operator: introduce the annotate methods

    pos="IN" chunk-"ORGANIZATION" FIXME

  
- in analysis, when processing the '-' operator not in class, whatever it matchs B- or I- something, then increments the counters
pro: easy to implment
pro: can implement quantifier 
cons: do not handle alterative

- in analysis, when processing the '-' operator not in class, call analysis on the sub sequence which returns Truth and new position
pro: can implement quantifiers
pro: can implement alternatives

  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN :      can   extend pattern='pos~"DT|JJ|NN.*"+' annotation={'chunk1':'NP'} iob = True 
  PP: {<IN><NP>}               # Chunk prepositions followed by NP :  may   extend pattern='pos="IN" chunk1-"NP"' annotation={'chunk2':'PP'} iob = True 
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments :    might extend pattern='pos~"VB.*" (chunk1-"NP"|chunk2-"PP"|chunk3-"CLAUSE")+$' annotation={'chunk4':'VP'} iob = True
  CLAUSE: {<NP><VP>}           # Chunk NP, VP                         might extend pattern='chunk1-"NP" chunk4-"VP"' annotation={'chunk3':'CLAUSE'} iob = True

  Since various type of chunks are related by hierachical relation, they should be considered at various levels and so we introduced various feature names for this purpose. When it is not flat structure, ...

  Like for nltk.chunk the third rule should be called again for detecting VP based on CLAUSE 




~/tmp/Pyrata/ branch parsing-alternative-sequences where we were writing the first grammar to capture alternatives in group

~/tmp/p2/Pyrata last up to date 

~/Bureau/Pyrata this doc

on veut une grammar avec 


