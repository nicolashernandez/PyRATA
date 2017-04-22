***************
PyRATA
***************
.. https://img.shields.io/badge/release-pyrata-brightgreen.svg

.. image:: https://img.shields.io/badge/pypi-release-brightgreen.svg
    :target: https://pypi.python.org/pypi/PyRATA
    :alt: Current Release Version    

.. image:: https://img.shields.io/badge/python-3.4.3-blue.svg
    :target: https://www.python.org/download/releases/
    :alt: Python 3


.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/nicolashernandez/PyRATA/master/LICENSE
    :alt: MIT License


PyRATA is an acronym which stands both for "*Python Rule-based feAture sTructure Analysis*" and "*Python Rule-bAsed Text Analysis*". Indeed, PyRATA is not only dedicated to process textual data.

Features
===========
In short, PyRATA 

* provides **regular expression (re) matching methods over** more complex structures than a list of characters (string), namely a **sequence of features set** (i.e. list of dict in python jargon);
* in addition to the re methods, it provides **modification methods to replace, update or extend (sub-parts of) the data structure** itself (also named *annotation*) ;
* offers a **similar re API to the python re module** in order not to disturb python re users;
* defines a pattern matching language whose **syntax follows the Perl regexes** de facto standard;
* is implemented in **python 3**;
* can be used for processing textual data but is not limited to (the only restriction is the respect of the data structure to explore);
* is released under the **MIT Licence** which is *a short and simple permissive license*;
* is *fun and easy to use* to explore data for research or pedagocial motivations, define machine learning features, formulate expert knowledge in a declarative way.


Documentation
===========

See the *Quick overview* section below and the `user guide <docs/user-guide.rst>`_ for more details and examples.


Download and installation procedure
===========

The simplest way
------------------------
Right now pyrata is `published on PyPI <https://pypi.python.org/pypi/PyRATA>`_, so the simplest procedure to install is to type in a console:

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

Then install pyrata 
::

    sudo pip3 install . 

Of course, as any python module you can barely copy the pyrata sub dir in your project to make it available. This solution can be an alternative if you do not have root privileges or do not want to use a virtualenv.

Requirement
------------------------

PyRATA use the `PLY <http://www.dabeaz.com/ply/ply.html>`_ implementation of lex and yacc parsing tools for Python (version 3.10).

You do not need to care about this stage if you performed the pip3 install procedure above.

If you do not properly install pyrata, you will have to manually install ply (or download it manually to copy it in your local working dir).
::

    sudo pip3 install ply


Run tests (optional)
------------------------

::
    python3 test_pyrata.py

The test named ``test_search_any_class_step_error_step_in_data`` may fail. It is due to a ``syntactic parsing error - unexpected token type="NAME" with value="pos" at position 35. Search an error before this point.`` So far the process of a pattern is not stopped when it encounters a parsing error, we would like to prevent this behavior (expected result). So the current obtained result differs from the one expected, and consequently gives a fail.


Quick overview (in console)
==================

First run python

::

    python3

Then import the main pyrata regular expression module:

.. doctest ::

    >>> import pyrata.re as pyrata_re

Let's work with the following sentence:

.. doctest ::

    >>> sentence = "It is fast easy and funny to write regular expressions with Pyrata"

Let's say your processing result in the pyrata data structure format, **a list of dict** i.e. a sequence of features set, each feature having a name and a value.

.. doctest ::

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]

There is **no requirement on the names of the features**.
You can easily turn a sentence into the pyrata data structure, for example by doing:

.. doctest ::

    >>> import nltk    
    >>> data =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]

In the previous code, you see that the names ``raw`` and ``pos`` have been arbitrary choosen to means respectively the surface form of a word and its part-of-speech.

At this point you can use the regular expression methods available to explore the data. Let's say you want to search all the adjectives in the sentence. By chance there is a property which specifies the part of speech of tokens, *pos*, the value of *pos* which stands for adjectives is *JJ*. Your pattern will be:

.. doctest ::

    >>> pattern = 'pos="JJ"'

To **find all the non-overlapping matches** of pattern in data, you will use the ``findall`` method:

.. doctest ::

    >>> pyrata_re.findall(pattern, data)
    >>> [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]]

To go further, the next step is to have a look to the `user guide <docs/user-guide.rst>`_. 

