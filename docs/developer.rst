Last version of this document is October 12 2017


Release procedure
=================

- develop
- list TODO in TODO.rst
- make the test run Ok ``python3 do_tests.py``
- edit do_tests.py to set logger.disabled to True
- review the README.rst (update badges)
- review the docs/user-guide.rst (update last modified date in the header)
- review the docs/developer.rst doc (update last modified date in the header)
- apply license recommendations
- update CHANGES.md
- last update TODO.rst

- update setup.py #  (logging version ; keep the same v for pupy)
- status/add/commit/push on github (with the diff content of CHANGES.md in comment)
- delete branch
- tag on github
- check MANIFEST.in to list files/dir to include in pypi module 
- publish on pypi



License application
----------------
- check the root LICENSE file
- update the root NOTICE file 
- add a license header to new files


github repository update 
-------------------

:: 
    git commit -a # m ''
    git push

github branch merging and suppression
--------------------

pousser une branche local
:: 
  git push <remote> <local branch name>:<remote branch to push into>
  git push origin develop:master

connaitre les branches dans votre repo
::
    git branch

créer une nouvelle branche
::
    git branch experimental

se placer dans une autre branche à l'intérieur de votre repo
::
    git checkout experimental

(éditer un fichier)
:: 
    git commit -a

merger au master
::
  git checkout master
  git merge experimental


pour gérer les conflits
::
    git diff
    git status

    git rm 

ou bien
edit fichier non mergé avec des HEAD
puis quand c'est corrigé
::
    git add file.txt
    git commit

pour effacer une branche 
:: 
    git branch -d experimental


github tagging
-------------------

list checksum of each commit
:: 

    git log --pretty="oneline"
 
annotated tag of a previous commited
:: 

    git tag -a v0.4 -m "Thompson's algorithm of NFA and Guan Gui implementation" efce8347d81b6bff6a7e1caa2e563d848e51b99b

push the tag
:: 
    git push origin v0.4 


pypi publication
---------------
the pypi version is without logging instruction for performance reason. If 2 versions are uploaded the odd first one is with logging and the even one is without

do not update setup.py # keep the same version as the tag. The only difference would be the logging information which will be not present.

prepare zip file to upload
::

    bash more/code-optimize.sh 
    rm -r dist/
    python3 setup.py sdist
    bash more/code-restore.sh 


live upload 
::
    python setup.py register -r pypi
    python setup.py sdist upload -r pypi

remove from local/install from local
:: 

  sudo pip3 uninstall pyrata
  sudo pip3 install .



API/engine implementation 
=================

description
-----------------------

Currently nfa.py holds the code for building and running an NFA.
- The building which turns a pattern string into a NFA is addressed by CompiledPattern.compile which in turn runs
pyrata.nfa_utils.pattern_to_guiguan_nfa_pattern_input(normalize_chunk_operator(p)) and self.compile_nfa_pattern()
The latter calls the recursive __parse_current_pattern_pos at position 0 which process each pattern 'char' element (special char and pyrata step).
Use append_element and append_B_to_A (which uses State.append_B_to_A).

- Running an NFA ...FIXME


.. [#] Gui Guan, "A Beautiful Linear Time Python Regex Matcher via NFA", August 19, 2014 `<https://www.guiguan.net/a-beautiful-linear-time-python-regex-matcher-via-nfa>`_
.. [#] Thompson, K. (1968). Programming techniques: Regular expression search algorithm. Commun. ACM, 11(6):419–422, June.

A look at the grammar...
-----------------------

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
    # Rule 13    step_group -> NOT step_group
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

v0.4 implementation choices
-----------------------

* State when adding new features to State object, we have also to modify a case (if A.is_empty():) in State.append_B_to_A
* Expression with regex such as 'pos="DT"? [pos~"NN|JJ"]* pos~"NN.*"' led to TypeError: cannot deepcopy this pattern object ; indeed the regex were precompiled at build stage. So to make copy works since it was fast, we compile at run time (no much lost)
Because the deepcopy of compiled regex pattern is not supported in Python (https://bugs.python.org/issue10076)



chunk operator 
^^^^^^^^^^^^^^^


Working with __chunks in IOB tagged format__. As mentioned in [nltk book](http://www.nltk.org/book/ch07.html), _The most widespread file representation of chunks uses IOB tags. In this scheme, each token is tagged with one of three special chunk tags, I (inside), O (outside), or B (begin). A token is tagged as B if it marks the beginning of a chunk. Subsequent tokens within the chunk are tagged I. All other tokens are tagged O. The B and I tags are suffixed with the chunk type, e.g. B-NP, I-NP. Of course, it is not necessary to specify a chunk type for tokens that appear outside a chunk, so these are just labeled O. An example of this scheme is shown below_  

.. doctest ::

    >>> data = [{'pos': 'NNP', 'chunk': 'B-PERSON', 'raw': 'Mark'}, {'pos': 'NNP', 'chunk': 'I-PERSON', 'raw': 'Zuckerberg'}, {'pos': 'VBZ', 'chunk': 'O', 'raw': 'is'}, {'pos': 'VBG', 'chunk': 'O', 'raw': 'working'}, {'pos': 'IN', 'chunk': 'O', 'raw': 'at'}, {'pos': 'NNP', 'chunk': 'B-ORGANIZATION', 'raw': 'Facebook'}, {'pos': 'NNP', 'chunk': 'I-ORGANIZATION', 'raw': 'Corp'}, {'pos': '.', 'chunk': 'O', 'raw': '.'}] 


The idea to handle chunks is to use the chunk operator `-` as a rewriting rule to turn the constraint into two with equality operator (e.g. `chunk-"PERSON"` would be rewritten in `(chunk="B-PERSON" chunk="I-PERSON"*)`).
This is done before starting the syntax analysis (compilation stage) or when building the compilation representation.

This trick has some consequences 
* 1) implicit groups are introduced around each chunk which be considered when referencing the groups
* it prevents us from including chunk constraints in classes (e.g. `[chunk-"PERSON" & raw="Mark"]`). 



<=v0.3
-----------------------

* branch automata-matcher (via fado)  modifying syntactic_pattern_parser ; idéalement doit changer p[0], j'ai essayé de passer par une variable de lexer mais je suis bloqué avec disj ; je note que l'import de lib de Fado cause un problème avec la méthode Not de sympy ... à creuser. -> on laisse tomber fado et on essaye d'utiliser l'implémentation de Guigan de Thompson : 
* lexer yacc to output a trace of the yacc parser, set the debug argument to True, it will write a parser.out https://github.com/dabeaz/ply/blob/master/ply/yacc.py
* ply access to parsed lextoken from the grammar, the grammar/pattern step, and the data token with length, Line Number and Position based on http://www.dabeaz.com/ply/ply.html#ply_nn33
reporting-parse-errors-from-ply-to-caller-of-parser
* code handle errors wo fatal crash http://stackoverflow.com/questions/18046579/
* code fix use test_match_inside_sequence_at_least_one_including_negation_on_atomic_constraint and test_match_inside_sequence_at_least_one_including_negation_in_class_constraint
* grammar parsing solve the shift/reduce conflict with AND and OR  ; The parser does not know what to apply between Rule 10    classconstraint -> partofclassconstraint,  and   (Rule 11    classconstraint -> partofclassconstraint AND classconstraint and Rule 12  or  classconstraint -> partofclassconstraint OR classconstraint) ; sol1 : removing Rule 10 since classconstraint should only be used to combine atomic constraint (at least two); but consequently negation should be accepted wo class (i.e. bracket) and with quantifier if so ; the use of empty rule lead to Parsing error: found token type= RBRACKET  with value= ] but not expected ; sol2 : which solve the problem, inverse the order partofclassconstraint AND classconstraint  -> classconstraint AND partofclassconstraint


* Warning: code cannot rename tokens into lextokens in parser since it is Ply 
* Warning: ihm, with Ply, when copying the grammar in the console, do not insert whitespace ahead
* code separate lexer, syntactic parser and semantic parser in distinct files http://www.dabeaz.com/ply/ply.html#ply_nn34 



Motivation for handling chunks and alternatives 
=================
.. doctest ::

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





Communication and code quality
===============================
* write README with short description, installation, quick overview sections
* logging 
* a test file 
* packaging and distributing package the project (python module, structure, licence wi copyright notice, gitignore)
* packaging and distributing configure the project 


* quality evaluate performance http://www.marinamele.com/7-tips-to-time-python-scripts-and-control-memory-and-cpu-usage


Ply debug
=================
Edit syntactic_step_parser.py
::

    self.parser = yacc.yacc(module=self, start='step', errorlog=yacc.NullLogger(), debug = True, **kwargs) 

Turn the debug option to True
It will generate a ``pyrata/parser.out`` file


Testing sympy
=================
http://docs.sympy.org/latest/modules/logic.html
http://docs.sympy.org/latest/tutorial/gotchas.html#symbols
You can build Boolean expressions with the standard python operators & (And), | (Or), ~ (Not):
python3
from sympy import *

x, y = symbols('x1 x2')
expr = y & y
>>> expr.subs({x: True, y: True})
True
>>> expr.subs([(x, True), (y, True)])

var = {}
var[0], var[1] = symbols('x1 x2')
expr = var[0] & var[1]
expr.subs([(var[0], True), (var[1], True)])
expr
# output the expr with given symbol names
x1 & x2

var[0], var[1] = symbols('pos="NN" x2')
var[0], var[1] = symbols('pos="NN" pos~"\ "')
works too



The guiguan nfa
=================

by firefox you can have a look at the doc

2to3
----
I generate a patch and apply it without any troubles.

testing the original one 
----------------

simply run 

    python3 regex_matching_py3.py "(ca*t|lion)+.*(dog)?" "catsdog" step
    evince NFA.pdf

testing the nfa on PyRATA pattern
---------------------------------
The code is not anymore a duplicat from pyrata/nfa.py but I had to make available method even not in DEBUG mode as draw, __check_and_clear_in_states, and __add_debug_info_from

    python3 guiguan_re.py 'raw="with" (pos="JJ"|raw="amazing")* raw="Pyrata"' "[{'pos': 'IN', 'raw': 'with'}, {'pos': 'JJ', 'raw': 'amazing'}, {'pos': 'NNP', 'raw': 'Pyrata'}]" yes

how guiguan nfa is working
--------------------------

* original data structure for pattern p and string s are strings i.e. list of characters
* for parsing the pattern, I prepare the pattern to build a list of "characters" by distinguishing special characters from step constraint definition. Then I use sympy to handle the step constraint as a symbolic expression to be evaluate at the runtime
* for matching the structure, I simply modify the code to evaluate the symbolic expression instead of the character identity relation.
* when matching a string, the nfa data structure generated at the pattern parsing time is modified so to be able to reuse the generated nfa, we have to copy it deeply. 
* the last point is a bit more complex since there are more matching methods


