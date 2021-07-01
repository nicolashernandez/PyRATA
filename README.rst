***************
PyRATA
***************
.. https://img.shields.io/badge/release-pyrata-brightgreen.svg

.. image:: https://img.shields.io/badge/pypi-release-brightgreen.svg
    :target: https://pypi.python.org/pypi/PyRATA
    :alt: Current Release Version    

.. image:: https://img.shields.io/badge/python-3.5.2-blue.svg
    :target: https://www.python.org/download/releases/
    :alt: Python 3


.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
    :target: https://raw.githubusercontent.com/nicolashernandez/PyRATA/master/LICENSE
    :alt: Apache License 2.0


PyRATA is an acronym which stands for "*Python Rule-based feAture sTructure Analysis*".

Features
===========
PyRATA 

* provides **regular expression (re) matching methods** on a more complex structure than a list of characters (string), namely a **sequence of features set** (i.e. ``list`` of ``dict`` in python jargon);
* is **free from the information encapsulated in the features** and consequently can work with word features, sentences features, calendar event features...   Indeed, PyRATA is not only dedicated to process textual data.
* offers a **similar re API to the python re module** in order not to confuse the python re users;
* in addition to the re methods, it provides **edit methods to substitute, update or extend (sub-parts of) the data structure** itself (this process can be named *annotation*);
* defines a pattern grammar whose **syntax follows the Perl regexes** de facto standard;
* the matching engine is based on a Gui Guan's implementation [#]_ of the **Thompson's algorithm** for converting Regular Expressions (RE) to Non-deterministic Finite Automata (NFA) and running them in a linear time efficiency of ``O(n)`` [#]_;
* is implemented in **python 3**;
* can draw out beautifully the *NFA to a PDF file*;
* can output the actual matches as *Deterministic Finite Automata (DFA)*;
* uses the `PLY <http://www.dabeaz.com/ply/ply.html>`_ implementation of lex and yacc parsing tools for Python (version 3.10), the `sympy <http://www.sympy.org/fr>`_ library for symbolic evaluation of logical expression, the `graph_tool <http://graph-tool.skewed.de>`_ library for drawing out PDF.
as of v0.5.1 (https://github.com/nicolashernandez/PyRATA/commit/19d0c33347ce3d1355cfdb09ba4e7b1dd9500839)the sympy library was removed and replaced by a home made implementation for performance reason.
* is released under the **`Apache License 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_** which allows you to *do what you like with the software, as long as you include the required notice*;
* published on `PyPI <https://pypi.python.org/pypi/PyRATA>`_;
* is *fun and easy to use* to explore data for research study, solve deterministic problems, formulate expert knowledge in a declarative way, prototype quickly models and generate training data for Machine Learning (ML) systems, extract ML features, augment ML models...

.. * is released under the **MIT Licence** which is *a short and simple permissive license*;
.. So it can be used for processing textual data but is not limited to. The only restriction is that the written patterns must specify the features actually present in the data structure to explore;

.. [#] Gui Guan, "A Beautiful Linear Time Python Regex Matcher via NFA", August 19, 2014 `<https://www.guiguan.net/a-beautiful-linear-time-python-regex-matcher-via-nfa>`_
.. [#] Thompson, K. (1968). Programming techniques: Regular expression search algorithm. Commun. ACM, 11(6):419–422, June.



Quick overview (in console)
==================


First install PyRATA (`available on PyPI <https://pypi.python.org/pypi/PyRATA>`_)

::

    sudo pip3 install pyrata

*v0.4.0* and *v0.4.1* check how to solve `importError No module named graph_tool <https://github.com/nicolashernandez/PyRATA/issues/2>`_ issue.

Run python

::

    python3

Then import the main PyRATA regular expression module:

.. doctest ::

    >>> import pyrata.re as pyrata_re

Let's work with a sentence as data:

.. doctest ::

    >>> sentence = "It is fast easy and funny to write regular expressions with PyRATA"

Do the process you want on the data...
Your analysis results should be represented in the PyRATA data structure format, **a list of dict** i.e. a sequence of features sets, each feature having a name and a value. Here a possible resulting example of such structure after tokenization and pos tagging: 

.. doctest ::

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]


To demonstrate how easily this data structure can be generated, we simulated your processing by simply using some `nltk <http://www.nltk.org/>`_ processing. Here below:

.. doctest ::

    >>> import nltk    
    >>> data =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]

There is **no requirement on the names of the features**. Value type is String. 
In the previous code, you see that the names ``raw`` and ``pos`` have been arbitrary chosen to mean respectively the surface form of a word and its part-of-speech.

.. s are primitives (String, Boolean, Numerical). 

At this point you can use the regular expression methods available to explore the data. Let's say you want to search all the adjectives in the sentence. By chance there is a property which specifies the part of speech of tokens, *pos*, the value of *pos* which stands for adjectives is *JJ*. Your pattern will be:

.. doctest ::

    >>> pattern = 'pos="JJ"'

To **find all the non-overlapping matches** of ``pattern`` in ``data``, you will use the ``findall`` method:

.. doctest ::

    >>> pyrata_re.findall(pattern, data)

And you get the following output:

.. doctest ::

    >>> [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]]

In python, ``list`` are marked by squared brackets, ``dict`` by curly brackets. Elements of ``list`` or ``dict``  are then separated by commas. Feature names are quoted. And so values when they are Strings. Names and values  are separated by a colon.

Here you can read an ordered list of four matches, each one corresponding to one specific adjective of the sentence. 

Reference
===========

.. doctest ::

    @InProceedings{HERNANDEZ18.732,
      author = {Nicolas Hernandez and Amir Hazem},
      title = {PyRATA, Python Rule-based feAture sTructure Analysis},
      booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
      year = {2018},
      month = {may},
      date = {7-12},
      location = {Miyazaki, Japan},
      editor = {Nicoletta Calzolari (Conference chair) and Khalid Choukri and Christopher Cieri and Thierry Declerck and Sara Goggi and Koiti Hasida and Hitoshi Isahara and Bente Maegaard and Joseph Mariani and Hélène Mazo and Asuncion Moreno and Jan Odijk and Stelios Piperidis and Takenobu Tokunaga},
      publisher = {European Language Resources Association (ELRA)},
      address = {Paris, France},
      isbn = {979-10-95546-00-9},
      language = {english}
      }
       

Documentation
===========

To go further, the next step is to have a look at the `user guide <docs/user-guide.rst>`_. 
