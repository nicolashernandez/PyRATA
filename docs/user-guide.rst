.. http://www.sphinx-doc.org/en/stable/rest.html
.. http://rst.ninjs.org/

********************
User guide
********************

:Last Reviewed: 2017-10-12

.. contents:: Contents
    :local:


Brief introduction
============================


.. epigraph::

   Regular expressions (RE) are [traditionally known as] a sequence of characters that define a search pattern. Usually this pattern is then used by string searching algorithms for "finding" or "finding and replacing" operations on strings.

   -- `Wikipedia <https://en.wikipedia.org/wiki/Regular_expression>`_


The data structure
------------------

But a character string is somehow a poor data structure. 

PyRATA takes *lists* of *dict* tokens as data input. The *dict* python type consists in a set of name-value attributes (also named *features*). 

Consequently PyRATA is not restricted to some domain knowledge and attached use cases. It is free from the encapsulated information present in the features. Indeed, the data structure can represent a sentence as sequence of words, each word token coming with a set of features. 
But it is not limited to the representation of sentences. It can also be used to represent a text, with the sentence as token unit. Each sentence with its own set of features. Etc.

This is the first PyRATA innovation.

Right now, PyRATA handles only primitive types as allowed values.
.. The objective is to offer a language and an engine to define patterns aiming at matching (parts of) lists of features set. 

.. More named arguments (`lexicons`) allows to set lexicons which can be used to define set of accepted values for a specified feature or the level of verbosity.


The API to process the data
------------------

The API is developed to be familiar for whom who develops with the python re module API. 

The module defines several known functions such as `search`, `findall`, or `finditer`. The functions are also available for compiled regular expressions. The former take at least two arguments including the pattern to recognize and the data to explore (e.g. `re.search(pattern, data)`) while the latter take at least one, the data to explore (e.g. `compiledPattern.search(data)`).
In addition to exploration methods, the module offers methods to edit the structure of the data either by substitution (`sub`), update (`update`) or extension (`extend`) of the data feature structures.


The language to express pattern
------------------

A **pattern** is made of one or several **ordered elements**. We also called them **steps** in reference to the `XPath language <https://www.w3.org/TR/xpath/>`_. A **pattern element** is, in its simplest form, the specification of a single constraint (**NAME OPERATOR"VALUE"**) that a data token should satisfy. For a given attribute name, you can specify its required exact value (with `=` operator), a regex definition of its value (`~` operator), a list of possible values (`@` operator) or if it is part of a IOB tag (`-` operator).  

These constraint operators are probably the second major innovation offered by PyRATA in the regex world.

A more complex element can be a *quantified element*, an *element class*, a *group*, *alternatives* or a combination of these various types.

A **quantified element** allows to set *optional* element (`?`), element which should occurs *at least one* (`+`), or *zero or more* (`*`). 
An **element class** aims at specifying more than one constraints and conditions on them with *parenthesis* (`()`) and logical connectors such as *and* (`&`), *or* (`|`) and *not* (`!`). 
A **group of elements**, surrounded by parenthesis  (`()`), is used to refer to and retrieve subparts of the pattern.
An **alternative** defines a set of pattern subparts at a specific point of the pattern. 


Alternatives
------------------

* `python re module <https://docs.python.org/3/library/re.html>`_ python 3, PSF (open source) License
* `python nltk chunk module <http://www.nltk.org/_modules/nltk/chunk/regexp.html#RegexpChunkParser>`_ python 3, Apache v2 
* `clips pattern <http://www.clips.ua.ac.be/pattern>`_ python 2.6, BSD-3
* `spaCy <https://github.com/explosion/spaCy>`_ python 3, MIT
* `GATE JAPE <https://gate.ac.uk/sale/tao/splitch8.html>`_ Java 8, GNU
* `Apache UIMA RUTA <https://uima.apache.org/ruta.html>`_ JAVA 8, Apache v2
* `Nooj <http://www.nooj-association.org>`_ C++/Java 1.7, LGPL
* `unitex <http://unitexgramlab.org>`_ GPL restricted license: Academic Only, Non Commercial Use Only.

.. [nltk.RegexpParser](https://gist.github.com/alexbowe/879414) ; http://nbviewer.jupyter.org/github/lukewrites/NP_chunking_with_nltk/blob/master/NP_chunking_with_the_NLTK.ipynb ; https://gist.github.com/alexbowe/879414
.. https://github.com/clips/pattern
.. * xpath from me over graph of objects
.. * linguastream


Limitations
------------------

* The value type is String. May be extended to other primitive types or object.
* Cannot handle overlapping annotations. Inherent to the approach.


Download and installation procedure
===========


The simplest way
------------------------
Right now PyRATA is `published on PyPI <https://pypi.python.org/pypi/PyRATA>`_, so the simplest procedure to install is to type in a console:

::

    sudo pip3 install pyrata

Alternatively you can manually 
------------------------

Download the latest PyRATA release
    
::

    wget https://github.com/nicolashernandez/PyRATA/archive/master.zip
    unzip master.zip -d .
    cd PyRATA-master/

or clone it 

::

    git clone https://github.com/nicolashernandez/PyRATA.git
    cd pyrata/

Then install PyRATA 
::

    sudo pip3 install . 

Of course, as any python module you can barely copy the PyRATA sub dir in your project to make it available. This solution can be an alternative if you do not have root privileges or do not want to use a virtualenv.

Requirement
------------------------

In addition to ``python3``, PyRATA uses 

* the `PLY <http://www.dabeaz.com/ply/ply.html>`_ implementation of lex and yacc parsing tools for Python (version 3.10). 
* the `sympy <http://www.sympy.org/fr>`_ library for symbolic evaluation of logical expression.
* the `graph_tool <http://graph-tool.skewed.de>`_ library for drawing out PDF (optional)

If you encounter the ``ImportError: No module named 'graph_tool'`` issue, then `check the fix for the graph_tool module import here <https://github.com/nicolashernandez/PyRATA/issues/2>`_

Since graph_tool is more a wrapper for C++ code than a python module, it requires a dedicated installation. Roughly speaking, under Ubuntu 16:04, you have to   
::

    echo deb http://downloads.skewed.de/apt/xenial xenial universe > /etc/apt/sources.list.d/my_xenial.list
    echo deb-src http://downloads.skewed.de/apt/xenial xenial universe >> /etc/apt/sources.list.d/my_xenial.list

    apt-get update \
    && apt-get install -y --allow-unauthenticated python3-graph-tool 

If you do not properly install PyRATA, you will have to manually install ply (or download it manually to copy it in your local working dir).
::

    sudo pip3 install ply
    sudo pip3 install sympy

Run tests (optional)
------------------------

::

    python3 do_tests.py

Uses the ``unittest`` module. You may also edit the file to set ``logger.disabled`` to ``False``. By default, the logging file is ``do_tests.py.log``.


Running PyRATA
============================

In console
--------------
First run python in console:

::

  python3

Then import the main PyRATA regular expression module:

.. doctest ::

  >>> import pyrata.re as pyrata_re



In command line
--------------

PyRATA comes with a script which allow to test the API. In v0.4 it is an alpha code. As we said, it is provided "as is"...

More information on parameters with:

:: 
   
    python3 pyrata_re.py -h

For example to search a given pattern by using some nlp processing:  

::

    python3 pyrata_re.py 'pos="JJ"' "It is fast easy and funny to write regular expressions with PyRATA" --nlp

Or operating with the raw data structure finding all matches in reluctant mode while drawing the corresponding nfa in a filename my_nfa.pdf and logging the process in a pyrata_re_py.log file.

::

    python3 pyrata_re.py 'pos="JJ"' "[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'PyRATA', 'pos': 'NNP'}]" --method findall --mode reluctant --draw --pdf_file_name my_nfa.pdf --log


Language expressivity
=====================

Basic concepts
--------------

PyRATA data structure
  PyRATA is intented to process *data* made of *sequence of elements*, each element being a *features set* i.e. a set of name-value attributes. In other words the PyRATA data structure is litteraly a ``list`` of ``dict``. The expected type of values is the type ``String``.
In python, ``list`` are marked by squared brackets, ``dict`` by curly brackets. Elements of ``list`` or ``dict``  are then separated by commas. Feature names are quoted. And so values when they are Strings. Names and values  are separated by a colon.


.. doctest ::

  >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]

There is *no requirement on the names of the features*.
In the previous code, you see that the names ``raw`` and ``pos`` have been arbitrary chosen to respectively mean the surface form of a word and its part-of-speech.

PyRATA pattern
  PyRATA allows to define *regular expressions* on the PyRATA data structure. It is made of an ordered list of pattern elements.

PyRATA pattern element
  The elementary component of a PyRATA pattern defines the combination of constraints (at least one) a data token should match. A pattern element is also named a *step* in reference to the XPath Language. 

Let's say you want to search all the adjectives in the sentence. By chance there is a property which specifies the part of speech of tokens, *pos*, the value of *pos* which stands for adjectives is *JJ*. Your pattern will be made of only one element which will define only one constraint:

.. doctest ::

  >>> pattern = 'pos="JJ"'


Simple constraint operators (*equal, match, in, chunk*)
------------------
Pattern elements are made of constraints. At the atomic level, a simple constraint is defined with one of the following operators.

Equal operator
^^^^^^^^^^^^^^^

Classically, the value of the referenced feature name should be equal to the specified value. The syntax is ``name="value"`` where name should match ``[a-zA-Z_][a-zA-Z0-9_]*``
and value ``\"([^\\\n]|(\\.))*?\"``.

The following operators use the same definition for the related name and value, only the operator changes. 

Regular expression match operator
^^^^^^^^^^^^^^^

In addition to the equal operator, you can **set a regular expression as a value**. 
In that case, the operator will be ``~`` metacharacter 

.. doctest ::

    >>> pyrata_re.findall('pos~"NN."', data)
    [[{'raw': 'expressions', 'pos': 'NNS'}], [{'raw': 'PyRATA', 'pos': 'NNP'}]]


In 'list' operator
^^^^^^^^^^^^^^^

You can also **set a list of possible values (lexicon)**. In that case, the operator will be the ``@`` metacharacter in your constraint definition and the value will be the name of the lexicon. The lexicon is specified as a parameter of the pyrata_re methods (``lexicons`` parameter). Indeed, multiple lexicons can be specified. The data structure for storing lexicons is a dict/map of lists. Each key of the dict is the name of a lexicon, and each corresponding value a list of elements making of the lexicon.

.. doctest ::

    >>> pyrata_re.findall('raw@"positiveLexicon"', data, lexicons = {'positiveLexicon':['easy', 'funny']})
    [[ {'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}]]

IOB Chunk operator
^^^^^^^^^^^^^^^

.. epigraph::

   The most widespread representation of chunks uses IOB tags. In this scheme, each token is tagged with one of three special chunk tags, I (inside), O (outside), or B (begin). A token is tagged as B if it marks the beginning of a chunk. Subsequent tokens within the chunk are tagged I. All other tokens are tagged O. The B and I tags are suffixed with the chunk type, e.g. B-NP, I-NP. Of course, it is not necessary to specify a chunk type for tokens that appear outside a chunk, so these are just labeled O.

   -- `nltk book <http://www.nltk.org/book/ch07.html>`_

An example of PyRATA data structure with chunks annotated in IOB tagged format is shown below. See the values of the ``chunk`` feature.  

.. doctest ::

    >>> data = [{'pos': 'NNP', 'chunk': 'B-PERSON', 'raw': 'Mark'}, {'pos': 'NNP', 'chunk': 'I-PERSON', 'raw': 'Zuckerberg'}, {'pos': 'VBZ', 'chunk': 'O', 'raw': 'is'}, {'pos': 'VBG', 'chunk': 'O', 'raw': 'working'}, {'pos': 'IN', 'chunk': 'O', 'raw': 'at'}, {'pos': 'NNP', 'chunk': 'B-ORGANIZATION', 'raw': 'Facebook'}, {'pos': 'NNP', 'chunk': 'I-ORGANIZATION', 'raw': 'Corp'}, {'pos': '.', 'chunk': 'O', 'raw': '.'}] 

    >>> pattern = 'chunk-"PERSON"'
    >>> pyrata_re.search(pattern, data)
    <pyrata.re Match object; groups=[[[{'pos': 'NNP', 'raw': 'Mark', 'chunk': 'B-PERSON'}, {'pos': 'NNP', 'raw': 'Zuckerberg', 'chunk': 'I-PERSON'}], 0, 2], [[{'pos': 'NNP', 'raw': 'Mark', 'chunk': 'B-PERSON'}, {'pos': 'NNP', 'raw': 'Zuckerberg', 'chunk': 'I-PERSON'}], 0, 2]]>

The metacharacter which means a chunk is ``-`` (dash).

``chunk-"PERSON"`` can be substitute literally with ``(chunk="B-PERSON" chunk="I-PERSON"*)``. That's why the Match object contains two groups.

The actual chunk implementation uses the chunk operator `-` as a rewriting rule to turn the constraint into two with equality operator (e.g. ``chunk-"PERSON"`` would be rewritten in ``(chunk="B-PERSON" chunk="I-PERSON"*)``). 
This is done before starting the syntax analysis (compilation stage) or when building the compilation representation.

This trick has some consequences:

* Implicit groups are introduced around each chunk which be considered when referencing the groups
* It prevents us from including chunk constraints in classes (e.g. ``[chunk-"PERSON" & raw="Mark"]``). 


Element class
------------------

An **element class** offers a way to combine several simple constraints in the definition of a pattern element. The definition is marked by *squared brackets* (``[...]``). *Logical operators* (and ``&``, or ``|`` and not ``!``) and *parenthesis* are available to combine the constraints.

.. doctest ::

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]
    >>> pyrata_re.findall('[(pos="NNS" | pos="NNP") & !raw="expressions"]', data)
    [[{'pos': 'NNP', 'raw': 'PyRATA'}]]


Consequently ``[pos="NNS" | pos="NNP"]``, ``pos~"NN[SP]"`` and ``pos~"(NNS|NNP)"`` are equivalent (give the same result). They may not have the same processing time.

__Warning__ Since version 0.3.3, the grammar has a bit changed. It does not accept any longer raw negative element. ``'!pos="NNS"+'`` must be rewritten into ``'[!pos="NNS"]+'``.


Wildcard element
------------------

The  **wildcard element** can match any single data token. It is represented by the ``.`` (dot) metacharacter. 

.. doctest ::

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]
    >>> pyrata_re.search('. raw="PyRATA"', data)
    <pyrata.re Match object; groups=[[[{'raw': 'with', 'pos': 'IN'}, {'raw': 'PyRATA', 'pos': 'NNP'}], 10, 12]]>

It can be used with any quantifiers 

.. doctest ::

    >>> pyrata_re.search('.+ raw="PyRATA"', data)
    <pyrata.re Match object; groups=[[[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'PyRATA', 'pos': 'NNP'}], 0, 12]]>

but cannot be considered as a simple constraint.



It can also easily be simulated by using a not wanted value or not-existing attribute. Below ``[!raw="to"]`` and ``[!foo="bar"]`` correspond to a not wanted data token. All give the same results as the dot wildcard. 

.. doctest ::

    >>> pyrata_re.findall('pos~"VB." [!raw="to"]* raw="to"', data)
    [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}]]
    >>> pyrata_re.findall('pos~"VB." [!foo="bar"]* raw="to"', data)
    [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}]]
    >>> pyrata_re.findall('pos~"VB." .* raw="to"', data)
    [[{'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}]]




Elements sequence
------------------

You can search a **sequence of elements**, for example an adjective (tagged *JJ*) followed by a noun in plural form (tagged *NNS*). The natural separator between the ordered elements is the whitespace character.

.. doctest ::

    >>> pattern = 'pos="JJ" pos="NNS"'
    >>> pyrata_re.search(pattern, data).group()
    [{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]


Start and End of data Anchors
------

To specify that a pattern should **match from the begining and/or to the end of a data structure**, you can use the anchors ``^`` and ``$`` metacharacters in the pattern, respectively to mean the start and the end of the data.

.. doctest ::

    >>> pattern = '^raw="It" [!foo="bar"]+'
    >>> pyrata_re.search(pattern, data)
    <pyrata.re Match object; groups=[[[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'PyRATA', 'pos': 'NNP'}], 0, 12]]>
   


Quantified elements (*at_least_one, any, optional*)
------------------

You can quantify the repetition of a pattern element.

At_least_one quantifier
^^^^^^^^^^^^^^^
You can specify a **quantifier to match one or more times consecutively** the same form of an element. The element definition should be followed by the ``+`` symbol:

.. doctest ::

    >>> pyrata_re.findall('pos="JJ"+', data)
    [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}]

Any quantifier
^^^^^^^^^^^^^^^

You can specify a **quantifier to match zero or more times consecutively** a certain form of an element. The element definition should be followed by the ``*`` symbol:

.. doctest ::

    >>> pyrata_re.findall('pos="JJ"* [(pos="NNS" | pos="NNP")]', data)
    [[[{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}], [{'raw': 'PyRATA', 'pos': 'NNP'}]]

Option quantifier
^^^^^^^^^^^^^^^

You can specify a  **quantifier to match once or not at all** the given form of an element. The element definition should be followed by the ``?`` symbol:


.. doctest ::

    >>> pyrata_re.findall('pos="JJ"? [(pos="NNS" | pos="NNP")]', data)
    [[{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'NNP', 'raw': 'PyRATA'}]]




Groups
------

In order to **retrieve the contents a specific part of a match, groups can be defined with parenthesis** which indicate the start and end of a group. 

The ``search`` method, like ``finditer``, returns match objects. Only one for the search method, the first one, if it exists at least one. A match object contains by default one group, the zero group, which can be referenced by ``.group(0)``. If groups are defined in the pattern by mean of parenthesis, then they are also indexed. A group is described is described by a value, the covered data, and a pair of offsets. 

.. doctest ::

    >>> import pyrata.re as pyrata_re
    >>> pyrata_re.search('raw="is" ([!raw="to"]+) raw="to"', [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]).group(1)
    [{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}]

Or a more complex example with many more groups and embedded groups:

.. doctest ::

    >>> pattern = 'raw="It" (raw="is") (( (pos="JJ"* pos="JJ") raw="and" (pos="JJ") )) (raw="to")'
    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]
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

Alternatives are a list of possible sub-patterns which can occur at a given position. As a group the list is delimited by parenthesis while the options are delimited by a pipe ``|`` symbol. The options should not need to be ordered. The match is dependent of the matching mode greedy or reluctant. 

.. doctest ::

    >>> pattern = '(pos="IN") (raw="a" raw="tea" | raw="a" raw="cup" raw="of" raw="coffee" | raw="an" raw="orange" raw="juice" ) ([!pos=";"])'
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

    >>> pattern = '(pos="IN") (raw="a" (raw="tea") | raw="a" (raw="cup" raw="of" raw="coffee") | raw="an" (raw="orange" raw="juice") ) ([!pos=";"])'
    >>> pyrata_re.search(pattern, data).group(3)
    [{'pos': 'NN', 'raw': 'cup'}, {'pos': 'IN', 'raw': 'of'}, {'pos': 'NN', 'raw': 'coffee'}]

And alternatives can embed groups. In the example below, the matching mode plays its role on the matched data.

.. doctest ::
    
      >>> data = [{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'PyRATA', 'pos': 'NNP'}]
      >>> pyrata_re.findall('(pos="JJ" | (pos="JJ" pos="NNS") )', data)
      [[{'raw': 'fast', 'pos': 'JJ'}], [{'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}]]
      >>> pyrata_re.findall('(pos="JJ" | (pos="JJ" pos="NNS") )', data, mode='reluctant')
      [[{'raw': 'fast', 'pos': 'JJ'}], [{'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}]]


Alternatives can be quantified.

.. doctest ::

    >>> pattern = '(pos="VB" [!pos="NN"]* raw="Life" pos="."| pos="VB" [!pos="NN"]* raw="job" pos="."|pos="VB" [!pos="NN"]* raw="career" pos="."|pos="VB" [!pos="NN"]* raw="family" pos="."|pos="VB" [!pos="NN"]* raw="television" pos=".")+'
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


Matching regular expression methods 
=====================

The matching methods available offer multiple ways of exploring the data. 

Search the first match of a given pattern
-------------------------

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
    {'pos': 'NNP', 'raw': 'PyRATA'}]

Let's say you want to search the adjectives. By chance there is a property which specifies the part of speech of tokens, *pos*, the value of *pos* which stands for adjectives is *JJ*.


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


Matching mode: global, greedy, reluctant
-------------------------

The PyRATA matching engine operates with a **global matching mode**. 

* If the match succeeds, the matching engine moves jumps just after the position of the last matched data token and starts a new search from this new position. Quantifiers in an expression benefit from this mode.  
* If the match fails, the matching engine moves to the next position in the data (from the current to the current+1) and starts a new search from this new position.

In addition, it allows to perform greedy or reluctant matching.
By default, a quantified subpattern is **greedy**, that is, it will match as many times as possible (given a particular starting location) while still allowing the rest of the pattern to match. 

Let's work with the following pattern and data:

.. doctest ::

    >>> pattern = 'pos="JJ"* pos="JJ"'
    >>> data = [ {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'JJ', 'raw': 'neat'}, {'pos': 'TO', 'raw': 'to'}]

In the example below ``greedy`` is explicitely specified (actually there is no need since it is the default mode).

.. doctest ::

    >>> pyrata_re.search(pattern, data, mode = 'greedy')
    <pyrata.re Match object; groups=[[[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'neat', 'pos': 'JJ'}], 1, 5]]>


**Reluctant matching** process means to match the minimum number of times possible. In the example below, the engine stops at the first match.

.. doctest ::

    >>> pyrata_re.search(pattern, data, mode = 'reluctant')
    <pyrata.re Match object; groups=[[[{'raw': 'fast', 'pos': 'JJ'}], 1, 2]]>

Same data, same pattern, same search method but distinct matching mode. We get two distinct object. The former being longer than the latter.

.. turns on "ungreedy mode", which switches the syntax for greedy and lazy quantifiers. So (?U)a* is lazy and (?U)a*? is greedy. 
.. g  - globally match the pattern repeatedly in the string
.. https://perldoc.perl.org/perlretut.html#Using-regular-expressions-in-Perl
.. If the match fails, the matching engine moves to the next position in the data and start a new search from this new position.
.. In scalar context, successive invocations against a string will have /g jump from match to match, keeping track of position in the string as it goes along. 
.. A failed match or changing the target string resets the position. 
..
.. https://perldoc.perl.org/perlre.html#Regular-Expressions greedy, reluctant and possessive
..
.. greedy (default mode) 
.. By default, a quantified subpattern is "greedy", that is, it will match as many times as possible (given a particular starting location) while still allowing the rest of the pattern to match. 
.. echo |perl -ne '$s="aaaa"; while ($s =~ /(a+a)/)  {print "$1\n"}'
.. aaaa
.. aaaa
.. aaaa
.. etc.
.. echo |perl -ne '$s="aaaa"; while ($s =~ /(a+a)/g)  {print "$1\n"}'
.. aaaa
.. echo |perl -ne '$s="aa bb cc dd"; while ($s =~ /(\w+)+/)  {print "$1\n"}'
.. aa
.. aa
.. aa
.. etc.
.. echo |perl -ne '$s="aa bb cc dd"; while ($s =~ /(\w+)+/g)  {print "$1\n"}'
.. aa
.. bb
.. cc
.. dd
..
.. reluctant 
..  If you want it to match the minimum number of times possible, follow the quantifier with a "?" . Note that the meanings don't change, just the "greediness":
.. echo |perl -ne '$s="aaaa"; while ($s =~ /(a+?a)/)  {print "$1\n"}'
.. aa
.. aa
.. aa
.. etc.
.. echo |perl -ne '$s="aaaa"; while ($s =~ /(a+?a)/g)  {print "$1\n"}'
.. aa
.. aa
.. echo |perl -ne '$s="aa bb cc dd"; while ($s =~ /(\w+)+?/)  {print "$1\n"}'
.. aa
.. aa
.. aa
.. etc.
.. echo |perl -ne '$s="aa bb cc dd"; while ($s =~ /(\w+)+?/g)  {print "$1\n"}'
.. aa
.. bb
.. cc
.. dd
..
.. possessive
.. will match as many times as possible and won't leave any for the remaining part of the pattern. This feature can be extremely useful to give perl hints about where it shouldn't backtrack.
.. perl -ne '$s="aaa"; $s =~ /(a++a)/; print "$1"'
.. (nothing matched)


Debugging the pattern compilation or the pattern matching
------------------

The logging facility was partially interrupted in v0.4. The following may not work as expected.

__ For some performance reason, the debugging facility is not available on the pip version but on the github version. __ 

PyRATA uses the `python logging facility <https://docs.python.org/3/howto/logging.html>`_. 

.. https://docs.python.org/3/library/logging.html

To **understand the process of a pyrata_re method either at the compilation or matching stage**, first import the logging module:

.. doctest ::

    >>> import pyrata.re as pyrata_re
    >>> import logging

Set the loggging filename, optionally the logging format of messages, and the logging level:   

* ``logging.DEBUG`` For very detailed output for diagnostic purposes (10)
* ``logging.INFO`` Report events that occur during normal operation of a program (e.g. for status monitoring or fault investigation) (20)
* ``logging.WARNING`` Issue a warning regarding a particular runtime event (30)

DEBUG is more verbose than WARNING. WARNING will only report syntactic parsing problems.

.. doctest ::

    >>> logging.basicConfig(format='%(levelname)s:\t%(message)s', filename='mypyrata.log', level=logging.INFO)

.. logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL

Now you can just run a compilation process

.. doctest :: 

    >>> pyrata_re.compile ('pos~"JJ"* pos~"NN."')

or any matching process (which encompasses a compilation process):

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
    {'pos': 'NNP', 'raw': 'PyRATA'}]
    >>> pyrata_re.findall ('pos="JJ" [(pos="NNS" | pos="NNP")]', data)

And observe the logging file in the current directory.

To dynamically change the log level without restarting the application, just type:

.. doctest :: 

    >>> logging.getLogger().setLevel(logging.DEBUG)

Log messages are incrementally appended at the end of the previous ones.

.. Syntactic problems are reported in INFO and DEBUG examples such as a star at the beggining of the pattern or unexpected token in the pattern: 

..    >>> pyrata_re.findall('*pos="JJ" [(pos="NNS" | pos="NNP")]', data)
..    Error: syntactic parsing error - unexpected token type="ANY" with value="*" at position 1. Search an error before this point.
..  >>> pyrata_re.findall('pos="JJ"* bla bla [(pos="NNS" | pos="NNP")]', data)
..    Error: syntactic parsing error - unexpected token type="NAME" with value="bla" at position 17. Search an error before this point.




Compiled regular expression
===========================

**Compiled regular expression objects** support the following methods ``search``, ``findall`` and ``finditer``. It follows the same API as `Python re <https://docs.python.org/3/library/re.html#re.regex.search>`_ but uses a sequence of features set instead of a string.

Below an example of use with the ``findall`` method

.. doctest ::

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]
    >>> compiled_re = pyrata_re.compile('pos~"JJ"* pos~"NN."')
    >>> compiled_re.findall(data)
    [[{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}], [{'raw': 'PyRATA', 'pos': 'NNP'}]]

A compiled regular expression object is made of a Non-deterministic Finite Automata (NFA), the specification of having to start/end with the data and the lexicons which are used in its pattern elements.

*Warning* v0.4 may have some display bugs and some states may not be present.

The following expression ``IN[pos~"JJ"]->CHAR(#S)->OUT[pos~"NN.",pos~"JJ"]`` defines the character state ``#S`` which can be get by the input state ``pos~"JJ"``and lead to two output states ``pos~"NN."`` and ``pos~"JJ"``. Characters ``#S``, ``#S`` and ``#S`` mean respectively *Start*, *Matching* and *Empty*.

.. doctest ::

    >>> compiled_re
    <pyrata.syntactic_pattern_parser CompiledPattern object; 
    starts_wi_data="False"
    ends_wi_data="False"
    lexicon="dict_keys([])"
    nfa="
      <pyrata.nfa NFA object; 
      states="{'IN[pos~"JJ"]->CHAR(#S)->OUT[pos~"NN.",pos~"JJ"]', 'IN[#S]->CHAR(pos~"NN.")->OUT[#M]', 'IN[pos~"NN."]->CHAR(#M)->OUT[]', 'IN[pos~"JJ"]->CHAR(#S)->OUT[pos~"NN.",pos~"JJ"]'}">
    ">


Here the representation of a compiled pattern with chunks:

.. doctest ::

    >>> pyrata_re.compile ('chunk-"NP"')
    <pyrata.syntactic_pattern_parser CompiledPattern object; 
      starts_wi_data="False"
      ends_wi_data="False"
      lexicon="dict_keys([])"
      nfa="
        <pyrata.nfa NFA object; 
        states="{'IN[chunk="I-NP",chunk="B-NP"]->CHAR(#M)->OUT[chunk="I-NP"]', 'IN[]->CHAR(#S)->OUT[chunk="B-NP"]'}">
      ">

Here the representation of a compiled pattern with quantified groups and alternatives : 

.. doctest ::

    pyrata_re.compile('raw="a"? (pos~"JJ" pos~"JJ")* (pos="NNS"|pos="NNP")+')
    <pyrata.syntactic_pattern_parser CompiledPattern object; 
    starts_wi_data="False"
    ends_wi_data="False"
    lexicon="dict_keys([])"
    nfa="
        <pyrata.nfa NFA object;
        states="{'IN[pos="NNS",pos="NNP"]->CHAR(#M)->OUT[#E]', 'IN[#S,raw="a",pos~"JJ"]->CHAR(#E)->OUT[pos~"JJ",#E]', 'IN[]->CHAR(#S)->OUT[#E,raw="a"]'}">
    ">

..[['?', 'raw="a"'], ['+', [[[None, 'pos="NNS"']], [[None, 'pos="NNP"']]]]]">

.. A compiled regular expression is made of a list of quantified elements. A quantified step is a quantifier with either a simple or complex step. A simple step is combination of one or several single constraints (e.g. a class step). A complex step is a list of alternatives, themself being a sequence of quantified steps.


Data feature structure edit methods
====================================

By edit methods we mean substitution, updating, extension of the data feature structure. 
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


Extracting  Deterministic Finite Automata
====================================

Each regular expression is converted into a Non-deterministic Finite Automata (NFA) at the compilation stage.
During the execution, a pattern can match several data patterns wrt the expression. Each match corresponds to a possible  Deterministic Finite Automata (DFA).  

PyRATA offers a way to extract the DFA as a list of actual encountered states. Successively the following example shows the internal representation of the NFA with all the present steps, then it shows the match obtained with a search method, and the corresponding ordered DFA states.

.. doctest ::

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'}, {'pos': 'NNP', 'raw': 'Pyrata'}]
    >>> pattern = '(pos="JJ"|pos="NN")* pos~"NN.*"+'
    >>> compiled_re = pyrata_re.compile(pattern)
    <pyrata.nfa CompiledPattern object; 
      starts_wi_data="False"
      ends_wi_data="False"
      lexicon="dict_keys([])"
      nfa="
      <pyrata.nfa NFA object; 
        states="{'IN[pos="JJ",pos="NN"]->CHAR(#S)->OUT[pos="JJ",pos="NN",pos~"NN.*"]', 'IN[pos="JJ",pos="NN"]->CHAR(#S)->OUT[pos="JJ",pos="NN",pos~"NN.*"]', 'IN[#S,pos~"NN.*"]->CHAR(pos~"NN.*")->OUT[pos~"NN.*",#M]', 'IN[pos~"NN.*"]->CHAR(#M)->OUT[]'}">
    ">
    >>> compile_re.search(data)
    <pyrata.re Match object; groups=[[[{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}], 8, 10], [[{'raw': 'regular', 'pos': 'JJ'}], 8, 9]]>
    >>> compiled_re.search(data).DFA()
    ['IN[#S]->CHAR(pos="JJ")->OUT[#S]', 'IN[pos~"NN.*",#S]->CHAR(pos~"NN.*")->OUT[pos~"NN.*",#M]']

In a near future they could also be searched in new data.


Generating the PyRATA data structure
====================================

Have a look at the ``nltk.py`` script (run it). It shows **how to turn various nltk analysis results into the pyrata data structure**.
In practice two approaches are available: either by building the dict list on fly or by using the dedicated PyRATA nltk methods: ``list2pyrata (**kwargs)`` and ``listList2pyrata (**kwargs)``. 

Building the dict list on fly 
-----------------------------

Thanks to python, you can also easily turn a sentence into the PyRATA data structure, for example by doing:

.. doctest ::

    >>> import nltk
    >>> sentence = "It is fast easy and funny to write regular expressions with PyRATA"
    >>> pyrata_data =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
    pyrata_data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]

Generating a more complex data on fly is similarly easy:

.. doctest ::

    >>> import nltk
    >>> from nltk import word_tokenize, pos_tag, ne_chunk
    >>> from nltk.chunk import tree2conlltags
    >>> sentence = "Mark is working at Facebook Corp." 
    >>> pyrata_data =  [{'raw':word, 'pos':pos, 'stem':nltk.stem.SnowballStemmer('english').stem(word), 'lem':nltk.WordNetLemmatizer().lemmatize(word.lower()), 'sw':(word in nltk.corpus.stopwords.words('english')), 'chunk':chunk} for (word, pos, chunk) in tree2conlltags(ne_chunk(pos_tag(word_tokenize(sentence))))]
    >>> pyrata_data
    [{'lem': 'mark', 'raw': 'Mark', 'sw': False, 'stem': 'mark', 'pos': 'NNP', 'chunk': 'B-PERSON'}, {'lem': 'is', 'raw': 'is', 'sw': True, 'stem': 'is', 'pos': 'VBZ', 'chunk': 'O'}, {'lem': 'working', 'raw': 'working', 'sw': False, 'stem': 'work', 'pos': 'VBG', 'chunk': 'O'}, {'lem': 'at', 'raw': 'at', 'sw': True, 'stem': 'at', 'pos': 'IN', 'chunk': 'O'}, {'lem': 'facebook', 'raw': 'Facebook', 'sw': False, 'stem': 'facebook', 'pos': 'NNP', 'chunk': 'B-ORGANIZATION'}, {'lem': 'corp', 'raw': 'Corp', 'sw': False, 'stem': 'corp', 'pos': 'NNP', 'chunk': 'I-ORGANIZATION'}, {'lem': '.', 'raw': '.', 'sw': False, 'stem': '.', 'pos': '.', 'chunk': 'O'}]

Dedicated methods to generate the PyRATA data structure 
-------------------------------------------------------

The former method, ``list2pyrata``, turns a list into a list of dict (e.g. a list of words into a list of dict) with a feature to represent the surface form of the word (default is ``raw``). If parameter ``name`` is given then the dict feature name will be the one set by the first value of the passed list as parameter value of name. If parameter ``dictList`` is given then this list of dict will be extended with the values of the list (named or not). 

The latter, ``listList2pyrata``, turns a list of list ``listList`` into a list of dict with values being the elements of the second list; the value names are arbitrary chosen. If the parameter ``names`` is given then the dict feature names will be the ones set (the order matters) in the list passed as ``names`` parameter value. If parameter ``dictList`` is given then the list of dict will be extented with the values of the list (named or not).

Example of uses of PyRATA dedicated conversion methods: See the ``nltk.py`` scripts


Drawing NFA in pdf file
====================================

So far (v0.4), the drawing option are only available in the ``pyrata_re.py`` script. See the command line running section.

Time performance
===========================

If you running the git version, you may make the code faster by removing the logging instructions.
Simply run:
  
.. doctest ::

    bash more/code-optimize.sh


To restore the code (modification will be lost): 

.. doctest ::

    bash more/code-restore.sh

A benchmark script is currently in development to compare PyRATA with some python alternatives.

.. doctest ::

    python3 do_benchmark.py 


License
============================


Up to v0.3.* the code was realised under the MIT license. Since the v0.4, PyRATA is released under the `Apache License 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_. Here a short `summary of the license <https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)>`_ .

The documentation is distributed under the terms of the `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license <https://creativecommons.org/licenses/by-nc-sa/4.0/>`_. 

To go further
============================

In addition to this current documentation, you may have look at ``do_tests.py`` to see the implemented examples and more.

You can also read

.. [#] `Regular Expression Matching Can Be Simple And Fast <http://swtch.com/~rsc/regexp/regexp1.html>`_ 
.. [#] An Efficient and Elegant Regular Expression Matcher in Python: http://morepypy.blogspot.com.au/2010/05/efficient-and-elegant-regular.html
