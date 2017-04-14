# PyRATA
-------------

PyRATA is an acronym which stands both for "Python Rule-based feAture sTructure Analysis" and "Python Rule-bAsed Text Analysis". Indeed, PyRATA is not only dedicated to process textual data.

## Features
-------------
In short, PyRATA 
* provides regular expression matching methods over more complex structures than a list of characters (string), namely a sequence of features set (i.e. list of dict in python jargon);
* in addition to the re methods, it provides data structure modification methods to replace, update or extend (sub-parts of) the data structure itself;
* offers a similar re API to the python re module in order not to disturb python re users;
* degines a pattern matching language whose syntax follows the Perl regexes de facto standard;
* is implemented in python 3;
* can be used for processing textual data but is not limited to (the only restriction is the respect of the data structure to explore);
* is released under the MIT Licence which is *a short and simple permissive license*;
* is fun and easy to use.

## Brief introduction
-------------

Traditional regular expression (RE) engines handle character strings; In other words, lists of character tokens.
In Natural Language Processing, RE are used to define patterns which are used to recognized some phenomena in texts.
They are the essence of the rule-based approach for analysing the texts.

### The data structure

But a character string is somehow a poor data structure. In the present work, we are dealing with lists of dict elements. The dict python type is a data structure to represent a set of name-value attributes. Right now we only handle primitive types as allowed values.
The objective is to offer a language and an engine to define patterns aiming at matching (parts of) lists of featureset. 

In the most common use case, a featureset list is a data structure used to represent a sentence as sequence of words, each word token coming with a set of features. 
But it is not limited to the representation of sentences. It can also be used to represent a text, with the sentence as token unit. Each sentence with its own set of features.

### The API to process the data

The API is developed to be familiar for whom who develops with the python re module API. 

The module defines several known functions such as `search`, `findall`, or `finditer`. The functions are also available for compiled regular expressions. The former take at least two arguments including the pattern to recognize and the data to explore (e.g. `re.search(pattern, data)`) while the latter take at least one, the data to explore (e.g. `compiledPattern.search(data)`).
In addition to exploration methods, the module offers methods to modify the structure of the data either by substitution (`sub`) or update (`update`) or extension (`extend`) of the data feature structures.

More named arguments (`lexicons`, `verbosity`) allows to set lexicons which can be used to define set of accepted values for a specified feature or the level of verbosity.

### The language to express pattern

A __pattern__ is made of one or several steps. A __step__ is, in its simplest form, the specification of a single constraint (*NAME OPERATOR VALUE*) that a data element should satisfy. For a given attribute name, you can specify its required exact value (with `=` *OPERATOR*), a regex definition of its value (`~` *OPERATOR*) or a list of possible values (`@` *OPERATOR*). A more complex step can be a _quantified step_, a _class step_, a _group step_, an _alternatives step_ or a combination of these various types.
A __quantified step__ allows to set *optional* step (`?`), steps which should occurs *at least one* (`+`), or *zero or more* (`*`). 
A __class step__ aims at specifing more than one constraints and conditions on them with *parenthesis* (`()`) and logical connectors such as *and* (`&`), *or* (`|`) and *not* (`!`). 
A __group step__, surrounded by parenthesis  (`()`), is used to refer to and retrieve subparts of the pattern.
An __alternatives steps__ defines the possible set of step sequences at a specific point of the pattern. 

See the *Quick overview* section below and the [user guide](docs/user-guide.rst) for more details and examples.

### References
  * https://docs.python.org/3/library/re.html
  * [nltk.RegexpParser](https://gist.github.com/alexbowe/879414) ; http://www.nltk.org/_modules/nltk/chunk/regexp.html#RegexpChunkParser ; http://nbviewer.jupyter.org/github/lukewrites/NP_chunking_with_nltk/blob/master/NP_chunking_with_the_NLTK.ipynb ; https://gist.github.com/alexbowe/879414
  * linguastream
  * pattern
  * ruta
  * xpath from me over graph of objects

### Limitations
* cannot handle overlapping annotations  

## Download and installation procedure
-----------------

Right now pyrata is not published on PyPI, so the procedure to use it is the following:

### Download or clone pyrata
Download the latest PyRATA release
    
    wget https://github.com/nicolashernandez/PyRATA/archive/master.zip
    unzip master.zip -d .
    cd PyRATA-master/

or clone it 

    git clone https://github.com/nicolashernandez/PyRATA.git
    cd pyrata/

### Installation
Then install pyrata 

    sudo pip3 install . 

Of course, as any python module you can barely copy the pyrata sub dir in your project to make it available. This solution can be an alternative if you do not have root privileges or do not want to use a virtualenv.

### Requirement

PyRATA use the [PLY](http://www.dabeaz.com/ply/ply.html "PLY") implementation of lex and yacc parsing tools for Python (version 3.10).

You do not need to care about this stage if you performed the install procedure above.

If you do not properly install pyrata, you will have to manually install ply.

    sudo pip3 install ply

### Run tests (optional)

    python3 test_pyrata.py

Only one test should fail. The one named `test_search_any_class_step_error_step_in_data`. It is due to a `syntactic parsing error - unexpected token type="NAME" with value="pos" at position 35. Search an error before this point.` So far the process of a pattern is not stopped when it encounters a parsing error, we would like to prevent this behavior (expected result). So the current obtained result differs from the one expected, and consequently gives a fail.


## Quick overview (in console)
-----------------

First run python

    python3

Then import the main pyrata regular expression module:

    >>> import pyrata.re as pyrata_re

Let's work with the following sentence:

    >>> sentence = "It is fast easy and funny to write regular expressions with Pyrata"

Let's say your processing result in the pyrata data structure format, __a list of dict__ i.e. a sequence of features set, each feature having a name and a value.

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]

There is __no requirement on the names of the features__.
You can easily turn a sentence into the pyrata data structure, for example by doing:

    >>> import nltk    
    >>> data =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]

In the previous code, you see that the names `raw` and `pos` have been arbitrary choosen to means respectively the surface form of a word and its part-of-speech.

At this point you can use the regular expression methods available to explore the data. Let's say you want to search all the adjectives in the sentence. By chance there is a property which specifies the part of speech of tokens, *pos*, the value of *pos* which stands for adjectives is *JJ*. Your pattern will be:

    >>> pattern = 'pos="JJ"'

To __find all the non-overlapping matches__ of pattern in data, you will use the `findall` method:

    >>> pyrata_re.findall(pattern, data)
    >>> [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]]

More information in the [user guide](docs/user-guide.rst). 

