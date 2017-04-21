.. http://www.sphinx-doc.org/en/stable/rest.html
.. http://rst.ninjs.org/

********************
User guide
********************

:Last Reviewed: 2017-04-17

.. contents:: Contents
    :local:


In addition to this current documentation, you may have look at ``test_pyrata.py`` to see the implemented examples and more.


Brief introduction
============================

Traditional regular expression (RE) engines handle character strings; In other words, lists of character tokens.
In Natural Language Processing, RE are used to define patterns which are used to recognized some phenomena in texts.
They are the essence of the rule-based approach for analysing the texts.

The data structure
------------------

But a character string is somehow a poor data structure. In the present work, we are dealing with lists of dict elements. The dict python type is a data structure to represent a set of name-value attributes. Right now we only handle primitive types as allowed values.
The objective is to offer a language and an engine to define patterns aiming at matching (parts of) lists of featureset. 

In the most common use case, a featureset list is a data structure used to represent a sentence as sequence of words, each word token coming with a set of features. 
But it is not limited to the representation of sentences. It can also be used to represent a text, with the sentence as token unit. Each sentence with its own set of features.

The API to process the data
------------------

The API is developed to be familiar for whom who develops with the python re module API. 

The module defines several known functions such as `search`, `findall`, or `finditer`. The functions are also available for compiled regular expressions. The former take at least two arguments including the pattern to recognize and the data to explore (e.g. `re.search(pattern, data)`) while the latter take at least one, the data to explore (e.g. `compiledPattern.search(data)`).
In addition to exploration methods, the module offers methods to modify the structure of the data either by substitution (`sub`) or update (`update`) or extension (`extend`) of the data feature structures.

More named arguments (`lexicons`, `verbosity`) allows to set lexicons which can be used to define set of accepted values for a specified feature or the level of verbosity.

The language to express pattern
------------------

A **pattern** is made of one or several steps. A **step** is, in its simplest form, the specification of a single constraint (*NAME OPERATOR VALUE*) that a data element should satisfy. For a given attribute name, you can specify its required exact value (with `=` *OPERATOR*), a regex definition of its value (`~` *OPERATOR*) or a list of possible values (`@` *OPERATOR*). A more complex step can be a *quantified step*, a *class step*, a *group step*, an *alternatives step* or a combination of these various types.
A **quantified step** allows to set *optional* step (`?`), steps which should occurs *at least one* (`+`), or *zero or more* (`*`). 
A **class step** aims at specifing more than one constraints and conditions on them with *parenthesis* (`()`) and logical connectors such as *and* (`&`), *or* (`|`) and *not* (`!`). 
A **group step**, surrounded by parenthesis  (`()`), is used to refer to and retrieve subparts of the pattern.
An **alternatives steps** defines the possible set of step sequences at a specific point of the pattern. 



Alternatives
------------------

* `python re module <https://docs.python.org/3/library/re.html>`_ python 3, PSF (open source) License
* `python nltk chunk module <http://www.nltk.org/_modules/nltk/chunk/regexp.html#RegexpChunkParser>`_ python 3, Apache v2 
.. [nltk.RegexpParser](https://gist.github.com/alexbowe/879414) ; http://nbviewer.jupyter.org/github/lukewrites/NP_chunking_with_nltk/blob/master/NP_chunking_with_the_NLTK.ipynb ; https://gist.github.com/alexbowe/879414
* `clips pattern <http://www.clips.ua.ac.be/pattern>`_ python 2.6, BSD-3
.. https://github.com/clips/pattern
* `spaCy <https://github.com/explosion/spaCy>`_ python 3, MIT
* `GATE JAPE <https://gate.ac.uk/sale/tao/splitch8.html>`_ Java 8, GNU
* `Apache UIMA RUTA <https://uima.apache.org/ruta.html>`_ JAVA 8, Apache v2
.. * xpath from me over graph of objects
.. * linguastream


Limitations
------------------

* cannot handle overlapping annotations  


Running pyrata (in console)
============================

First run python in console:

::

  python3

Then import the main pyrata regular expression module:

.. doctest ::

  >>> import pyrata.re as pyrata_re



Language expressivity
=====================

Basic concepts
--------------

pyrata data structure
  Pyrata is intented to process *data* made of *sequence of elements*, each element being a *features set* i.e. a set of name-value attributes. In other words the pyrata data structure is litteraly a ``list`` of ``dict``. The expected type of values is the primitive type ``String``.


.. doctest ::

  >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]

There is *no requirement on the names of the features*.
In the previous code, you see that the names ``raw`` and ``pos`` have been arbitrary choosen to means respectively the surface form of a word and its part-of-speech.

pyrata pattern
  Pyrata allows to define *regular expressions* over the pyrata data structure.

pattern step
  The elementary component of a pyrata pattern is the **step**. It defines the combination of constraints a data element should match.

Let's say you want to search all the adjectives in the sentence. By chance there is a property which specifies the part of speech of tokens, *pos*, the value of *pos* which stands for adjectives is *JJ*. Your pattern will be made of only one step which will set only one constraint:

.. doctest ::

  >>> pattern = 'pos="JJ"'


Single constraint operators (*equal, match, in, chunk*)
------------------
Step are made of constraints. At the atomic level, the single constraint is defined with one of the following operators.

Equal operator
^^^^^^^^^^^^^^^

Classically, the value of the refered feature name should be equal to the specified value. The syntax is ``name="value"`` where name should match ``[a-zA-Z_][a-zA-Z0-9_]*``
and value ``\"([^\\\n]|(\\.))*?\"``.

The following operators use the same definition for the related name and value, only the operator changes. 

Regular expression match operator
^^^^^^^^^^^^^^^

In addition to the equal operator, you can **set a regular expression as a value**. 
In that case, the operator will be ``~`` 

.. doctest ::

    >>> pyrata_re.findall('pos~"NN."', data)
    [[{'raw': 'expressions', 'pos': 'NNS'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]


In 'list' operator
^^^^^^^^^^^^^^^

You can also **set a list of possible values (lexicon)**. In that case, the operator will be ``@`` in your constraint definition and the value will be the name of the lexicon. The lexicon is specified as a parameter of the pyrata_re methods (``lexicons`` parameter). Indeed, multiple lexicons can be specified. The data structure for storing lexicons is a dict/map of lists. Each key of the dict is the name of a lexicon, and each corresponding value a list of elements making of the lexicon.

.. doctest ::

    >>> pyrata_re.findall('raw@"positiveLexicon"', data, lexicons = {'positiveLexicon':['easy', 'funny']})
    [[ {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}]]

IOB Chunk operator
^^^^^^^^^^^^^^^

.. epigraph::

   The most widespread representation of chunks uses IOB tags. In this scheme, each token is tagged with one of three special chunk tags, I (inside), O (outside), or B (begin). A token is tagged as B if it marks the beginning of a chunk. Subsequent tokens within the chunk are tagged I. All other tokens are tagged O. The B and I tags are suffixed with the chunk type, e.g. B-NP, I-NP. Of course, it is not necessary to specify a chunk type for tokens that appear outside a chunk, so these are just labeled O.

   -- [nltk book](http://www.nltk.org/book/ch07.html)

An example of pyrata data structure with chunks annotated in IOB tagged format is shown below. See the values of the ``chunk`` feature.  

.. doctest ::

    >>> data = [{'pos': 'NNP', 'chunk': 'B-PERSON', 'raw': 'Mark'}, {'pos': 'NNP', 'chunk': 'I-PERSON', 'raw': 'Zuckerberg'}, {'pos': 'VBZ', 'chunk': 'O', 'raw': 'is'}, {'pos': 'VBG', 'chunk': 'O', 'raw': 'working'}, {'pos': 'IN', 'chunk': 'O', 'raw': 'at'}, {'pos': 'NNP', 'chunk': 'B-ORGANIZATION', 'raw': 'Facebook'}, {'pos': 'NNP', 'chunk': 'I-ORGANIZATION', 'raw': 'Corp'}, {'pos': '.', 'chunk': 'O', 'raw': '.'}] 

    >>> pattern = 'chunk-"PERSON"'
    >>> pyrata_re.search(pattern, data)
    <pyrata.re Match object; groups=[[[{'pos': 'NNP', 'raw': 'Mark', 'chunk': 'B-PERSON'}, {'pos': 'NNP', 'raw': 'Zuckerberg', 'chunk': 'I-PERSON'}], 0, 2], [[{'pos': 'NNP', 'raw': 'Mark', 'chunk': 'B-PERSON'}, {'pos': 'NNP', 'raw': 'Zuckerberg', 'chunk': 'I-PERSON'}], 0, 2]]>

``chunk-"PERSON"`` can be substitute literaly with ``(chunk="B-PERSON" chunk="I-PERSON"*)``. That's why the Match object contains two groups.


Class of step
------------------

A **class of step** is a step definition made of a combination of single constraints that a data element should check. The definition is marked by *squared brackets* (``[...]``). *Logical operators* (and ``&``, or ``|`` and not ``!``) and *parenthesis* are available to combine the constraints.

.. doctest ::
    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    >>> pyrata_re.findall('[(pos="NNS" | pos="NNP") & !raw="expressions"]', data)
    [[{'pos': 'NNP', 'raw': 'Pyrata'}]]


Consequently ``[pos="NNS" | pos="NNP"]``, ``pos~"NN[SP]"`` and 'pos~"(NNS|NNP)"' are equivalent (give the same result). They may not have the same processing time.

Sequence of steps
------------------

You can search a **sequence of steps**, for example an adjective (tagged *JJ*) followed by a noun in plural form  (tagged *NNS*). The natural separator between the steps is the whitespace character.

.. doctest ::

    >>> pattern = 'pos="JJ" pos="NNS"'
    >>> pyrata_re.search(pattern, data).group()
    [{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]


Start and End of data Anchors
------

To specify that a pattern should **match from the begining and/or to the end of a data structure**, you can use the anchors ``^`` and ``$`` respectively to the set the start or the end of the pattern relatively to the processed data.

.. doctest ::

    >>> pattern = '^raw="It" !foo="bar"+'
    >>> pyrata_re.search(pattern, data)
    <pyrata.re Match object; groups=[[[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'Pyrata', 'pos': 'NNP'}], 0, 12]]>
   


Step quantifiers (*at_least_one, any, optional*)
------------------

You can quantify the repetition of a step.

At_least_one quantifier
^^^^^^^^^^^^^^^
You can specify a **quantifier to match one or more times consecutively** the same form of an element. The step definition should be followed by the ``+`` symbol:

.. doctest ::

    >>> pyrata_re.findall('pos="JJ"+', data)
    [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}]

Any quantifier
^^^^^^^^^^^^^^^

You can specify a **quantifier to match zero or more times consecutively** a certain form of an element. The step definition should be followed by the ``*`` symbol:

.. doctest ::

    >>> pyrata_re.findall('pos="JJ"* [(pos="NNS" | pos="NNP")]', data)
    [[[{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]

Option quantifier
^^^^^^^^^^^^^^^

You can specify a  **quantifier to match once or not at all** the given form of an element. The step definition should be followed by the ``?`` symbol:


.. doctest ::

    >>> pyrata_re.findall('pos="JJ"? [(pos="NNS" | pos="NNP")]', data)
    [[{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'NNP', 'raw': 'Pyrata'}]]



Wildcard step
------------------

Currently no **wildcard character** is implemented but you can easily simulate it with a non existing attribute or value:

.. doctest ::

    >>> pyrata_re.findall('pos~"VB." [!raw="to"]* raw="to"', data)
    [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}]]



Groups
------

In order to **retrieve the contents a specific part of a match, groups can be defined with parenthesis** which indicate the start and end of a group. 

The ``search`` method, like ``finditer``, returns match objects. Only one for the search method, the first one, if it exists at least one. A match object contains by default one group, the zero group, which can be refered by ``.group(0)``. If groups are defined in the pattern by mean of parenthesis, then they are also indexed. A group is described is described by a value, the covered data, and a pair of offsets. 

.. doctest ::

    >>> import pyrata.re as pyrata_re
    >>> pyrata_re.search('raw="is" (!raw="to"+) raw="to"', [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]).group(1)
    [{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}]

Or a more complex example with many more groups and embedded groups:

.. doctest ::

    >>> pattern = 'raw="It" (raw="is") (( (pos="JJ"* pos="JJ") raw="and" (pos="JJ") )) (raw="to")'
    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    >>> pyrata_re.search(pattern, data)
    <pyrata.re Match object; groups=[[[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}], 0, 7], [[{'raw': 'is', 'pos': 'VBZ'}], 1, 2], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}], 2, 6], [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], 2, 4], [[{'raw': 'funny', 'pos': 'JJ'}], 5, 6], [[{'raw': 'to', 'pos': 'TO'}], 6, 7]]>


Groups can be quantified like in the following example:

.. doctest ::

    >>> pattern = '(pos="VB" pos="DT"? pos="JJ"* pos="NN" pos=".")+'
    >>> data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    >>> quantified_group = pyrata_re.search(pattern, data)
    >>> quantified_group
    >>> <pyrata.re Match object; groups=[[[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'NN', 'raw': 'Life'}, {'pos': '.', 'raw': '.'}, {'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'job'}, {'pos': '.', 'raw': '.'}, {'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'career'}, {'pos': '.', 'raw': '.'}, {'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'family'}, {'pos': '.', 'raw': '.'}, {'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'JJ', 'raw': 'fucking'}, {'pos': 'JJ', 'raw': 'big'}, {'pos': 'NN', 'raw': 'television'}, {'pos': '.', 'raw': '.'}], 0, 21], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'NN', 'raw': 'Life'}, {'pos': '.', 'raw': '.'}], 0, 3], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'job'}, {'pos': '.', 'raw': '.'}], 3, 7], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'career'}, {'pos': '.', 'raw': '.'}], 7, 11], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'family'}, {'pos': '.', 'raw': '.'}], 11, 15], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'JJ', 'raw': 'fucking'}, {'pos': 'JJ', 'raw': 'big'}, {'pos': 'NN', 'raw': 'television'}, {'pos': '.', 'raw': '.'}], 15, 21]]>

*Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television.*


Alternatives
------

Alternatives are a list of possible steps sequences which can occur at a given step. As a group the list is delimited by parenthesis while the options are delimited by a pipe ``|`` symbol. The options should be ordered. the first match leads the engine to pursue its analysis. There is no backtracking.

.. doctest ::

    >>> pattern = '(pos="IN") (raw="a" raw="tea" | raw="a" raw="cup" raw="of" raw="coffee" | raw="an" raw="orange" raw="juice" ) (!pos=";")'
    >>> data = [ {'raw':'Over', 'pos':'IN'},
      {'raw':'a', 'pos':'DT' }, 
      {'raw':'cup', 'pos':'NN' },
      {'raw':'of', 'pos':'IN'},
      {'raw':'coffee', 'pos':'NN'},
      {'raw':',', 'pos':','},
      {'raw':'Mr.', 'pos':'NNP'}, 
      {'raw':'Stone', 'pos':'NNP'},
      {'raw':'told', 'pos':'VBD'},
      {'raw':'his', 'pos':'PRP$'}, 
      {'raw':'story', 'pos':'NN'} ]
    >>>pyrata_re.search(pattern, data).group(2)
    [{'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'cup'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'coffee'}]

Groups can be embedded in alternatives:

.. doctest ::

    >>> pattern = '(pos="IN") (raw="a" (raw="tea") | raw="a" (raw="cup" raw="of" raw="coffee") | raw="an" (raw="orange" raw="juice") ) (!pos=";")'
    >>> pyrata_re.search(pattern, data).group(3)
    [{'pos': 'NN', 'raw': 'cup'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'coffee'}]

The opposite is less true... 
2017-04-22 *Warning*: unexpected compilation results will be obtained if you embed an alternative in a group.  


Alternatives can be quantified.

.. doctest ::

    >>> pattern = '(pos="VB" !pos="NN"* raw="Life" pos="."| pos="VB" !pos="NN"* raw="job" pos="."|pos="VB" !pos="NN"* raw="career" pos="."|pos="VB" !pos="NN"* raw="family" pos="."|pos="VB" !pos="NN"* raw="television" pos=".")+'
    >>> data = [ {'raw':'Choose', 'pos':'VB'},
      {'raw':'Life', 'pos':'NN' }, 
      {'raw':'.', 'pos':'.' },
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'job', 'pos':'NN'},
      {'raw':'.', 'pos':'.'}, 
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'career', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'family', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'},
      {'raw':'Choose', 'pos':'VB'},
      {'raw':'a', 'pos':'DT'},
      {'raw':'fucking', 'pos':'JJ'}, 
      {'raw':'big', 'pos':'JJ'},             
      {'raw':'television', 'pos':'NN'}, 
      {'raw':'.', 'pos':'.'}  
      ]
    >>> quantified_alternatives = pyrata_re.search(pattern, data)
    >>> quantified_alternatives
    >>> <pyrata.re Match object; groups=[[[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'NN', 'raw': 'Life'}, {'pos': '.', 'raw': '.'}, {'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'job'}, {'pos': '.', 'raw': '.'}, {'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'career'}, {'pos': '.', 'raw': '.'}, {'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'family'}, {'pos': '.', 'raw': '.'}, {'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'JJ', 'raw': 'fucking'}, {'pos': 'JJ', 'raw': 'big'}, {'pos': 'NN', 'raw': 'television'}, {'pos': '.', 'raw': '.'}], 0, 21], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'NN', 'raw': 'Life'}, {'pos': '.', 'raw': '.'}], 0, 3], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'job'}, {'pos': '.', 'raw': '.'}], 3, 7], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'career'}, {'pos': '.', 'raw': '.'}], 7, 11], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'NN', 'raw': 'family'}, {'pos': '.', 'raw': '.'}], 11, 15], [[{'pos': 'VB', 'raw': 'Choose'}, {'pos': 'DT', 'raw': 'a'}, {'pos': 'JJ', 'raw': 'fucking'}, {'pos': 'JJ', 'raw': 'big'}, {'pos': 'NN', 'raw': 'television'}, {'pos': '.', 'raw': '.'}], 15, 21]]>

Again *Choose Life. Choose a job. Choose a career. Choose a family. Choose a fucking big television.*


Regular expression methods 
=====================

The regular expression available methods offer multiple ways of exploring the data. 

Assuming the following data:

.. doctest ::

  >>> data = [{'pos': 'PRP', 'raw': 'It'}, 
    {'pos': 'VBZ', 'raw': 'is'}, 
    {'pos': 'JJ', 'raw': 'fast'}, 
    {'pos': 'JJ', 'raw': 'easy'}, 
    {'pos': 'CC', 'raw': 'and'}, 
    {'pos': 'JJ', 'raw': 'funny'}, 
    {'pos': 'TO', 'raw': 'to'}, 
    {'pos': 'VB', 'raw': 'write'}, 
    {'pos': 'JJ', 'raw': 'regular'}, 
    {'pos': 'NNS', 'raw': 'expressions'}, 
    {'pos': 'IN', 'raw': 'with'},
    {'pos': 'NNP', 'raw': 'Pyrata'}]

Let's say you want to search the adjectives. By chance there is a property which specifies the part of speech of tokens, *pos*, the value of *pos* which stands for adjectives is *JJ*.

Search the first match of a given pattern
-------------------------

To **search the first location** where a given pattern (here ``pos="JJ"``) produces a match:

.. doctest ::

    >>> pyrata_re.search('pos="JJ"', data)
    >>> <pyrata_re Match object; span=(2, 3), match="[{'pos': 'JJ', 'raw': 'fast'}]">

To get the **value of the match**:

.. doctest ::

    >>> pyrata_re.search('pos="JJ"', data).group()
    >>> [{'raw': 'fast', 'pos': 'JJ'}]


This default match is known as the **zero group**:

.. doctest ::

    >>> pyrata_re.search('pos="JJ"', data).group(0)
    >>> [{'raw': 'fast', 'pos': 'JJ'}]
    
To get the **value of the start and the end**:

.. doctest ::

    >>> pyrata_re.search('pos="JJ"', data).start()
    >>> 2
    >>> pyrata_re.search('pos="JJ"', data).end()
    >>> 3




Find all non-overlapping matches of a pattern
-------------------------

To **find all non-overlapping matches** of pattern in data, as a list of datas:

.. doctest ::

    >>> pyrata_re.findall('pos="JJ"', data)
    >>> [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]]


Get an iterator yielding match objects over all non-overlapping matches of a pattern
-------------------------

To **get an iterator yielding match objects** over all non-overlapping matches for the RE pattern in data:

.. doctest ::

    >>> for m in pyrata_re.finditer('pos="JJ"', data): print (m)
    ... 
    <pyrata_re Match object; span=(2, 3), match="[{'pos': 'JJ', 'raw': 'fast'}]">
    <pyrata_re Match object; span=(3, 4), match="[{'pos': 'JJ', 'raw': 'easy'}]">
    <pyrata_re Match object; span=(5, 6), match="[{'pos': 'JJ', 'raw': 'funny'}]">
    <pyrata_re Match object; span=(8, 9), match="[{'pos': 'JJ', 'raw': 'regular'}]">


Match and MatchesList objects
-------------------------

A **Match** is an object which is created when a pattern matching occurs. With the ``search`` method, only the first one is considered. With the ``finditer`` method, all the occurrences of the pattern will lead to the creation of a Match. For, ``finditer`` the Matches are appended to an object which lists all the Matches, namely a **MatchesList**.

Comparison operators and the ``len`` method on Match objects are available:

.. doctest ::

    >>> m1 = pyrata_re.search('pos="JJ"', data)
    <pyrata.re Match object; groups=[[[{'raw': 'fast', 'pos': 'JJ'}], 2, 3]]>

The Match object contains the value of instanciated pattern and its offsets in data.

.. doctest ::

    >>> m2 = pyrata_re.search('pos="JJ"', data)
    >>> m3 = pyrata_re.search('pos="NN"', data)
    >>> if m1 == m2: print ('True')
    ... 
    True

If none group is specified then the result of the comparison between the zero groups is returned with ``eq`` and ``ne`` operators.

.. doctest ::

    >>> if m1 != m3: print ('True')
    ... 
    True
    >>> len(m1)
    >>> 1
    >>> m4 = pyrata_re.search('(pos="JJ")+', data)
    >>> m4  
    <pyrata.re Match object; groups=[[[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], 2, 4], [[{'raw': 'fast', 'pos': 'JJ'}], 2, 3], [[{'raw': 'easy', 'pos': 'JJ'}], 3, 4]]>

In addition to the default zero group, the pattern defined a group which has two instances because of the quantifier.

.. doctest ::

    >>> len(m4)
    >>> 3   # 
    
Comparison operators and the ``len`` method on MatchesList objects are available:

.. doctest ::

    >>> ml1 = pyrata_re.finditer('pos="JJ"', data)    
    >>> ml2 = pyrata_re.finditer('pos="JJ"', data)
    >>> ml3 = pyrata_re.finditer('pos="NN"', data)

.. doctest ::

    >>> if ml1 == ml2: print ('True')
    ... 
    True
    >>> if ml1 != ml3: print ('True')
    ... 
    True
    >>> len(ml1)
    >>> 4


The previous tests can be performed with the two Matches objects created above from the *Trainspotting* data i.e. ``quantified_group`` and ``quantified_alternatives``.


Debugging a pattern
------------------

**Deprecated**

To **understand the process of a pyrata_re method**, specify a **verbosity degree** to it (*0 None, 1 +Parsing Warning and Error, 2 +syntactic and semantic parsing logs, 3 +More parsing informations*):

Here some syntactic problems examples: 

.. doctest ::

    >>> pyrata_re.findall('*pos="JJ" [(pos="NNS" | pos="NNP")]', data, verbosity=1)
    Error: syntactic parsing error - unexpected token type="ANY" with value="*" at position 1. Search an error before this point.

    >>> pyrata_re.findall('pos="JJ"* bla bla [(pos="NNS" | pos="NNP")]', data, verbosity=1)
    Error: syntactic parsing error - unexpected token type="NAME" with value="bla" at position 17. Search an error before this point.





Compiled regular expression
===========================

**Compiled regular expression objects** support the following methods ``search``, ``findall`` and ``finditer``. It follows the same API as [Python re](https://docs.python.org/3/library/re.html#re.regex.search) but uses a sequence of features set instead of a string.

Below an example of use with the ``findall`` method

.. doctest ::

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]
    >>> compiled_re = pyrata_re.compile('pos~"JJ"* pos~"NN."')
    >>> compiled_re.findall(data)
    [[{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]

A compiled regular expression object is made of the pattern steps, the specification of having to start/end with the data and the lexicons which are used in its steps.

.. doctest ::

    >>> compiled_re
    <pyrata.syntactic_pattern_parser CompiledPattern object; 
    starts_wi_data="False"
    ends_wi_data="False"
    lexicon="dict_keys([])"
    pattern_steps="
    [['*', 'pos~"JJ"'], [None, 'pos~"NN."']]">

Here the representation of a more complex compiled pattern: 

.. doctest ::

    pyrata_re.compile('raw="a"? (pos~"JJ" pos~"JJ")* (pos="NNS"|pos="NNP")+')
    <pyrata.syntactic_pattern_parser CompiledPattern object; 
    starts_wi_data="False"
    ends_wi_data="False"
    lexicon="dict_keys([])"
    pattern_steps="
    [['?', 'raw="a"'], ['+', [[[None, 'pos="NNS"']], [[None, 'pos="NNP"']]]]]">

A compiled regular expression is made of a list of quantified steps. A quantified step is a quantifier with either a simple or complex step. A simple step is combination of one or several single contraints (e.g. a class step). A complex step is a list of alternatives, themself being a sequence of quantified steps.


Data Feature structure modification methods
====================================

By modification we mean subtitution, updating, extension of the data feature structure. 
The process of updating or extending a feature structure is also called *annotation*.

Substitution
------------

The ``sub(pattern, annotation, replacement, group = [0])`` method **substitutes the leftmost non-overlapping occurrences of pattern matches or a given group of matches by a dict or a sequence of dicts**. Returns a copy of the data obtained and by default the data unchanged.

.. doctest ::

    >>> import pyrata.re as pyrata_re
    >>> pattern = 'pos~"NN.?"'
    >>> annotation = {'raw':'smurf', 'pos':'NN' }
    >>> data = [ {'raw':'Over', 'pos':'IN'},  
          {'raw':'a', 'pos':'DT' },  {'raw':'cup', 'pos':'NN' }, 
          {'raw':'of', 'pos':'IN'}, 
          {'raw':'coffee', 'pos':'NN'}, 
          {'raw':',', 'pos':','},  
          {'raw':'Mr.', 'pos':'NNP'},  {'raw':'Stone', 'pos':'NNP'}, 
          {'raw':'told', 'pos':'VBD'}, 
          {'raw':'his', 'pos':'PRP$'},  {'raw':'story', 'pos':'NN'} ]    
    >>> pyrata_re.sub(pattern, annotation, data)
    [{'raw': 'Over', 'pos': 'IN'}, 
    {'raw': 'a', 'pos': 'DT'}, {'raw': 'smurf', 'pos': 'NN'},
    {'raw': 'of', 'pos': 'IN'}, 
    {'raw': 'smurf', 'pos': 'NN'}, 
    {'raw': ',', 'pos': ','}, 
    {'raw': 'smurf', 'pos': 'NN'}, {'raw': 'smurf', 'pos': 'NN'}, 
    {'raw': 'told', 'pos': 'VBD'}, 
    {'raw': 'his', 'pos': 'PRP$'}, {'raw': 'smurf', 'pos': 'NN'}]

Here an example by modifying a group of a Match:

.. doctest ::

    >>> pyrata_re.sub('pos~"(DT|PRP\$)" (pos~"NN.?")', {'raw':'smurf', 'pos':'NN' }, [{'raw':'Over', 'pos':'IN'}, {'raw':'a', 'pos':'DT' }, {'raw':'cup', 'pos':'NN' }, {'raw':'of', 'pos':'IN'}, {'raw':'coffee', 'pos':'NN'}, {'raw':',', 'pos':','}, {'raw':'Mr.', 'pos':'NNP'}, {'raw':'Stone', 'pos':'NNP'}, {'raw':'told', 'pos':'VBD'}, {'raw':'his', 'pos':'PRP$'}, {'raw':'story', 'pos':'NN'}], group = [1])
    [{'raw': 'Over', 'pos': 'IN'}, {'raw': 'a', 'pos': 'DT'}, {'raw': 'smurf', 'pos': 'NN'}, {'raw': 'of', 'pos': 'IN'}, {'raw': 'coffee', 'pos': 'NN'}, {'raw': ',', 'pos': ','}, {'raw': 'Mr.', 'pos': 'NNP'}, {'raw': 'Stone', 'pos': 'NNP'}, {'raw': 'told', 'pos': 'VBD'}, {'raw': 'his', 'pos': 'PRP$'}, {'raw': 'smurf', 'pos': 'NN'}]

To completely remove some parts of the data, the anotation should be an empty list ``[]``.

Update
---------------------------

The ``update(pattern, annotation, replacement, group = [0], iob = False)`` method **updates (and extends) the features of a match or a group of a match with the features of a dict or a sequence of dicts** (of the same size as the group/match).

.. doctest ::

    >>> pyrata_re.update('(raw="Mr.")', {'raw':'Mr.', 'pos':'TITLE' }, [{'raw':'Over', 'pos':'IN'}, {'raw':'a', 'pos':'DT' }, {'raw':'cup', 'pos':'NN' }, {'raw':'of', 'pos':'IN'}, {'raw':'coffee', 'pos':'NN'}, {'raw':',', 'pos':','}, {'raw':'Mr.', 'pos':'NNP'}, {'raw':'Stone', 'pos':'NNP'}, {'raw':'told', 'pos':'VBD'}, {'raw':'his', 'pos':'PRP$'}, {'raw':'story', 'pos':'NN'}])
    [{'raw': 'Over', 'pos': 'IN'}, {'raw': 'a', 'pos': 'DT'}, {'raw': 'cup', 'pos': 'NN'}, {'raw': 'of', 'pos': 'IN'}, {'raw': 'coffee', 'pos': 'NN'}, {'raw': ',', 'pos': ','}, {'raw': 'Mr.', 'pos': 'TITLE'}, {'raw': 'Stone', 'pos': 'NNP'}, {'raw': 'told', 'pos': 'VBD'}, {'raw': 'his', 'pos': 'PRP$'}, {'raw': 'story', 'pos': 'NN'}]


Extension
---------------------------

The ``extend(pattern, annotation, replacement, group = [0], iob = False)`` method **extends (i.e. if a feature exists then do not update) the features of a match or a group of a match with the features of a dict or a sequence of dicts** (of the same size as the group/match:

.. doctest ::

    >>> pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'
    >>> annotation = {'chunk':'NP'}
    >>> data = [ {'raw':'Over', 'pos':'IN'},  
          {'raw':'a', 'pos':'DT' },  {'raw':'cup', 'pos':'NN' }, 
          {'raw':'of', 'pos':'IN'}, 
          {'raw':'coffee', 'pos':'NN'}, 
          {'raw':',', 'pos':','},  
          {'raw':'Mr.', 'pos':'NNP'},  {'raw':'Stone', 'pos':'NNP'}, 
          {'raw':'told', 'pos':'VBD'}, 
          {'raw':'his', 'pos':'PRP$'},  {'raw':'story', 'pos':'NN'} ]
    >>> pyrata_re.extend(pattern, annotation, data)
    [{'pos': 'IN', 'raw': 'Over'}, 
    {'pos': 'DT', 'raw': 'a', 'chunk': 'NP'}, {'pos': 'NN', 'raw': 'cup', 'chunk': 'NP'}, 
    {'pos': 'IN', 'raw': 'of'}, 
    {'pos': 'NN', 'raw': 'coffee', 'chunk': 'NP'}, 
    {'pos': ',', 'raw': ','}, 
    {'pos': 'NNP', 'raw': 'Mr.', 'chunk': 'NP'}, {'pos': 'NNP', 'raw': 'Stone', 'chunk': 'NP'}, 
    {'pos': 'VBD', 'raw': 'told'}, 
    {'pos': 'PRP$', 'raw': 'his', 'chunk': 'NP'}, {'pos': 'NN', 'raw': 'story', 'chunk': 'NP'}]


IOB annotation
---------------------------

Both with update or extend, you can specify if the data obtained should be annotated with IOB tag prefix. 

.. doctest ::

    >>> pyrata_re.extend(pattern, annotation, data, iob = True)
    [{'raw': 'Over', 'pos': 'IN'}, 
     {'raw': 'a', 'chunk': 'B-NP', 'pos': 'DT'}, {'raw': 'cup', 'chunk': 'I-NP', 'pos': 'NN'}, 
     {'raw': 'of', 'pos': 'IN'}, {'raw': 'coffee', 'chunk': 'B-NP', 'pos': 'NN'}, 
     {'raw': ',', 'pos': ','}, 
     {'raw': 'Mr.', 'chunk': 'B-NP', 'pos': 'NNP'}, {'raw': 'Stone', 'chunk': 'I-NP', 'pos': 'NNP'}, 
     {'raw': 'told', 'pos': 'VBD'}, 
     {'raw': 'his', 'chunk': 'B-NP', 'pos': 'PRP$'}, {'raw': 'story', 'chunk': 'I-NP', 'pos': 'NN'}]



Generating the pyrata data structure
====================================

Have a look at the ``nltk.py`` script (run it). It shows **how to turn various nltk analysis results into the pyrata data structure**.
In practice two approaches are available: either by building the dict list on fly or by using the dedicated pyrata nltk methods: ``list2pyrata (**kwargs)`` and ``listList2pyrata (**kwargs)``. 

Building the dict list on fly 
-----------------------------

Thanks to python, you can also easily turn a sentence into the pyrata data structure, for example by doing:

.. doctest ::

    >>> import nltk
    >>> sentence = "It is fast easy and funny to write regular expressions with Pyrata"
    >>> pyrata_data =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
    pyrata_data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]

Generating a more complex data on fly is similarly easy:

.. doctest ::

    >>> import nltk
    >>> from nltk import word_tokenize, pos_tag, ne_chunk
    >>> from nltk.chunk import tree2conlltags
    >>> sentence = "Mark is working at Facebook Corp." 
    >>> pyrata_data =  [{'raw':word, 'pos':pos, 'stem':nltk.stem.SnowballStemmer('english').stem(word), 'lem':nltk.WordNetLemmatizer().lemmatize(word.lower()), 'sw':(word in nltk.corpus.stopwords.words('english')), 'chunk':chunk} for (word, pos, chunk) in tree2conlltags(ne_chunk(pos_tag(word_tokenize(sentence))))]
    >>> pyrata_data
    [{'lem': 'mark', 'raw': 'Mark', 'sw': False, 'stem': 'mark', 'pos': 'NNP', 'chunk': 'B-PERSON'}, {'lem': 'is', 'raw': 'is', 'sw': True, 'stem': 'is', 'pos': 'VBZ', 'chunk': 'O'}, {'lem': 'working', 'raw': 'working', 'sw': False, 'stem': 'work', 'pos': 'VBG', 'chunk': 'O'}, {'lem': 'at', 'raw': 'at', 'sw': True, 'stem': 'at', 'pos': 'IN', 'chunk': 'O'}, {'lem': 'facebook', 'raw': 'Facebook', 'sw': False, 'stem': 'facebook', 'pos': 'NNP', 'chunk': 'B-ORGANIZATION'}, {'lem': 'corp', 'raw': 'Corp', 'sw': False, 'stem': 'corp', 'pos': 'NNP', 'chunk': 'I-ORGANIZATION'}, {'lem': '.', 'raw': '.', 'sw': False, 'stem': '.', 'pos': '.', 'chunk': 'O'}]

Dedicated methods to generate the pyrata data structure 
-------------------------------------------------------

The former method, ``list2pyrata``, turns a list into a list of dict (e.g. a list of words into a list of dict) with a feature to represent the surface form of the word (default is ``raw``). If parameter ``name`` is given then the dict feature name will be the one set by the first value of the passed list as parameter value of name. If parameter ``dictList`` is given then this list of dict will be extented with the value of the list (named or not). 

The latter, ``listList2pyrata``, turns a list of list ``listList`` into a list of dict with values being the elements of the second list; the value names are arbitrary choosen. If the parameter ``names`` is given then the dict feature names will be the ones set (the order matters) in the list passed as ``names`` parameter value. If parameter ``dictList`` is given then the list of dict will be extented with the values of the list (named or not).

Example of uses of pyrata dedicated conversion methods: See the ``nltk.py`` scripts
