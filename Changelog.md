## Changelog - index based search:
**compiled_pattern**:
method create_index_dic() added and used in finditer() - L_694_
method remove_overlap() added and used in finditer() - L_707_
method finditer() changed to fit the index based search - L_732_

**do_control-time-memory-usage**:
added pyrata exemple grammars for extensive time testing - L_76_

**do_tests**:
added 3 tests to check Sympy removal worked properly - L_2917-2936_

**On most files**:
replaced most NBSP (non breaking space) character by spaces in commentaries
to make it more readable for some IDEs.


## Past changelog - Sympy removal:
**nfa**:
method __step_special_state() changed to substitute Sympy with python RE - L_275_
method solve() added to substitute Sympy - L_80_

