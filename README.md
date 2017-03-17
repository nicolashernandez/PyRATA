# PyRATA
-------------

PyRATA is an acronym which stands both for "Python Rule-based feAture sTructure Analysis" and "Python Rule-bAsed Text Analysis". Indeed, PyRATA is not onlyt dedicated to process textual data.

## Description
-------------

Traditional regular expression (RE) engines handle character strings; In other words, lists of character tokens.
In Natural Language Processing, RE are used to define patterns which are used to recognized some phenomena in texts.
They are the essence of the rule-based approach for analysing the texts.

But character strings are a poor data structure. In the present work, we are dealing with lists of dict tokens. The dict python type is a data structure to represent a set of attribute name/value. Right now we only handle primitive types as allowed values.
The objective is to offer a language and an engine to define patterns aiming at matching (parts of) lists of featureset. 

In the most common use case, a featureset list is a data structure used to represent a sentence as sequence of words, each word token coming with a set of features. 
But it is not limited to the representation of sentences. It can also be used to represent a text, with the sentence as token unit. Each sentence with its own set of features.

The API is developed to be familiar for whom who develop with the python re module API.

In comparison
  * [nltk.RegexpParser](https://gist.github.com/alexbowe/879414) ; http://www.nltk.org/_modules/nltk/chunk/regexp.html#RegexpChunkParser ; http://nbviewer.jupyter.org/github/lukewrites/NP_chunking_with_nltk/blob/master/NP_chunking_with_the_NLTK.ipynb
  * pattern
  * ruta
  * xpath from me over graph of objects

### Limitations
* cannot handle overlapping annotations  

# Install and run
-----------------

## Requirement
PyRATA use the [PLY](http://www.dabeaz.com/ply/ply.html "PLY") implementation of lex and yacc parsing tools for Python (version 3.10).
One way to install it is:

    sudo pip3 install ply

## Use it (in console)
First run python

    python3

Then import the main pyrata regular expression module:

    >>> import pyrata_re

Let's say you have a sentence in the pyrata data structure format, __a list of dict__. A dict is a map i.e. a set of features, eachone with a name and value (in our case a primitive value).

    >>> data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'Pyrata'}]

There is no requirement on the names of the features.

By the way, you can also easily turn a sentence into the pyrata data structure, for example by doing:

    >>> import nltk
    >>> sentence = "It is fast easy and funny to write regular expressions with Pyrata"
    >>> data =  [{'raw':word, 'pos':pos} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]

In the previous code, you see that the names `raw` and `pos` have been arbitrary choosen to means respectively the surface form of a word and its part-of-speech.

At this point you can use the regular expression methods available to explore the data. Let's say you want to search the advectives. By chance there is a property which specifies the part of speech of tokens, *pos*, the value of *pos* which stands for adjectives is *JJ*.
To __search the first location__ where a given pattern (here `pos="JJ"`) produces a match:

    >>> pyrata_re.search('pos="JJ"', data)
    >>> <pyrata_re Match object; span=(2, 3), match="[{'pos': 'JJ', 'raw': 'fast'}]">

To get the __value of the match__:

    >>> pyrata_re.search('pos="JJ"', data).group()
    >>> [{'raw': 'fast', 'pos': 'JJ'}]
    
To get the __value of the start and the end__:

    >>> pyrata_re.search('pos="JJ"', data).start()
    >>> 2
    >>> pyrata_re.search('pos="JJ"', data).end()
    >>> 3

To __find all non-overlapping matches__ of pattern in data, as a list of datas:

    >>> pyrata_re.findall('pos="JJ"', data)
    >>> [[{'pos': 'JJ', 'raw': 'fast'}], [{'pos': 'JJ', 'raw': 'easy'}], [{'pos': 'JJ', 'raw': 'funny'}], [{'pos': 'JJ', 'raw': 'regular'}]]]

To __get an iterator yielding match objects__ over all non-overlapping matches for the RE pattern in data:

    >>> for m in pyrata_re.finditer('pos="JJ"', data): print (m)
    ... 
    <pyrata_re Match object; span=(2, 3), match="[{'pos': 'JJ', 'raw': 'fast'}]">
    <pyrata_re Match object; span=(3, 4), match="[{'pos': 'JJ', 'raw': 'easy'}]">
    <pyrata_re Match object; span=(5, 6), match="[{'pos': 'JJ', 'raw': 'funny'}]">
    <pyrata_re Match object; span=(8, 9), match="[{'pos': 'JJ', 'raw': 'regular'}]">

What about the expressivity of the pyrata grammar? A pattern is made of __steps__, eachone specifying the form of the element to match. 
You can search a __sequence of elements__, for example an adjective (tagged *JJ*) followed by a noun in plural form  (tagged *NNS*):

    >>> pyrata_re.search('pos="JJ" pos="NNS"', data).group()
    [{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}]

You can specify a __class of elements__ by specifying constraints on the properties of the required element with logical operators like:

    >>> pyrata_re.findall('[(pos="NNS" | pos="NNP") & !raw="pattern"]', data)
    [[{'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'NNP', 'raw': 'Pyrata'}]]

You can quantify the repetition of a step: in other words specifying a __quantifier to match one or more times__ the same form of an element:

    >>> pyrata_re.findall('+pos="JJ"', data)
    [[{'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}], [{'raw': 'funny', 'pos': 'JJ'}], [{'raw': 'regular', 'pos': 'JJ'}]

Or specifying a __quantifier to match zero or more times__ a certain form of an element:

    >>> pyrata_re.findall('*pos="JJ" [(pos="NNS" | pos="NNP")]', data)
    [[[{'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]

Or specifying a __quantifier to match once or not at all__ the given form of an element:

    >>> pyrata_re.findall('?pos="JJ" [(pos="NNS" | pos="NNP")]', data)
    [[{'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}], [{'pos': 'NNP', 'raw': 'Pyrata'}]]

At the atomic level, there is not only the equal operator to set a constraint. You can also specify *a regular expression as a value*. 
In that case, the operator will not be `=` but `~` 

    >>> pyrata_re.findall('pos~"NN."', data)
    [[{'raw': 'expressions', 'pos': 'NNS'}], [{'raw': 'Pyrata', 'pos': 'NNP'}]]
 

To understand the process of a method, specify a __verbosity degree__ to it:

    >>> pyrata_re.findall('*pos="JJ" [(pos="NNS" | pos="NNP")]', data, loglevel=3)
    ....

## Run tests

    python3 test_pyrata.py


More complex data     

    >>> data =  [{'raw':word, 'pos':pos, 'stem':nltk.stem.SnowballStemmer('english').stem(word), 'lem':nltk.WordNetLemmatizer().lemmatize(word.lower()), 'sw':(word in nltk.corpus.stopwords.words('english'))} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
    >>> data
    [{'lem': 'it', 'stem': 'it', 'raw': 'It', 'pos': 'PRP', 'sw': False}, {'lem': "'s", 'stem': "'s", 'raw': "'s", 'pos': 'VBZ', 'sw': False}, {'lem': 'fun', 'stem': 'fun', 'raw': 'fun', 'pos': 'JJ', 'sw': False}, {'lem': 'and', 'stem': 'and', 'raw': 'and', 'pos': 'CC', 'sw': True}, {'lem': 'easy', 'stem': 'easi', 'raw': 'easy', 'pos': 'JJ', 'sw': False}, {'lem': 'to', 'stem': 'to', 'raw': 'to', 'pos': 'TO', 'sw': True}, {'lem': 'play', 'stem': 'play', 'raw': 'play', 'pos': 'VB', 'sw': False}, {'lem': 'with', 'stem': 'with', 'raw': 'with', 'pos': 'IN', 'sw': True}, {'lem': 'pyrata', 'stem': 'pyrata', 'raw': 'Pyrata', 'pos': 'NNP', 'sw': False}]


# How does it work?
-------------------
## Concepts 

A grammar to parse. Right now a pattern. Which is made of 1 or several steps. A step is in its simplest form the specification of a single constraint. A step can be a quantified step or a class step (the latter aims at specify more than one constraints and conditions on them with logical operators ('and', 'or' and 'not')).

A data structure to parse too... on which the pattern is applied.

## Grammar

(as generated in parser.out)

    Rule 0     S' -> expression
    Rule 1     expression -> quantifiedstep
    Rule 2     expression -> quantifiedstep expression
    Rule 3     quantifiedstep -> step
    Rule 4     quantifiedstep -> OPTION step
    Rule 5     quantifiedstep -> ATLEASTONE step
    Rule 6     quantifiedstep -> ANY step
    Rule 7     step -> atomicconstraint
    Rule 8     step -> NOT step
    Rule 9     step -> LBRACKET classconstraint RBRACKET
    Rule 10    classconstraint -> partofclassconstraint
    Rule 11    classconstraint -> partofclassconstraint AND classconstraint
    Rule 12    classconstraint -> partofclassconstraint OR classconstraint
    Rule 13    partofclassconstraint -> atomicconstraint
    Rule 14    partofclassconstraint -> LPAREN classconstraint RPAREN
    Rule 15    partofclassconstraint -> NOT classconstraint
    Rule 16    atomicconstraint -> NAME EQ VALUE



# Roadmap
---------

##  Done 
* implementation of token sequence parsing/semantic analysis with token an atomicconstraint
* implementation of class of tokens (parsing and semantic analysis with logical and/or/not operators and parenthesis)
* implementation of quantifier AT_LEAST_ONE
* lexer and parser as classes
* regex operation match 
* rename package, file, module, class, variable names
* improve the log experience by displaying parsed lextoken from the grammar, the grammar/pattern step, and the data token with length, Line Number and Position (based on http://www.dabeaz.com/ply/ply.html#ply_nn33)
* rename global step grammar -> patternStep and local into localstep (quantifiedStep is ambiguous since it is the name of the production just before expression)
* move the code for testing the validity of a patternstep into the quantifier production rule and non in expression
* fix global step count based on works on split(' ') when class constraints with multiple constraints 
* fix use test_match_inside_sequence_at_least_one_including_negation_on_atomic_constraint and test_match_inside_sequence_at_least_one_including_negation_in_class_constraint
* when a quantifier step is not valid, the parsing should be aborted wo waiting for expression parsing
* solve the shift/reduce conflict with AND and OR  ; The parser does not know what to apply between Rule 10    classconstraint -> partofclassconstraint,  and   (Rule 11    classconstraint -> partofclassconstraint AND classconstraint and Rule 12  or  classconstraint -> partofclassconstraint OR classconstraint) ; sol1 : removing Rule 10 since classconstraint should only be used to combine atomic constraint (at least two); but consequently negation should be accepted wo class (i.e. bracket) and with quantifier if so ; the use of empty rule lead to Parsing error: found token type= RBRACKET  with value= ] but not expected ; sol2 : which solve the problem, inverse the order partofclassconstraint AND classconstraint  -> classconstraint AND partofclassconstraint
* done nltk facilities to turn it into pyrata data structure
* implement optional quantifier in quantifiedstep 
* implement any quantifier in quantifiedstep
* symbol ':' turned into '=' (since it had an equal meaning)
* implement pyrata_re.search
* implement pyrata_re.findall
* implement pyrata_re.finditer
* README with a section part for the user
* declare a regex as a value of atomic constraint 

## TODO

* end location is stored several times with the expression rules ; have a look at len(l.lexer.groupstartindex): and len(l.lexer.groupendindex): after parsing in pyrata_re methods to compare 
* revise the README and create a specific developer page
* class atomic with non atomic contraint should be prefered to not step to adapt one single way of doing stuff: partofclassconstraint -> NOT classconstraint more than step -> NOT step ; but the latter is simpler so check if it is working as expected wi quantifier +!pos:"EX" = +[!pos:"EX"])
* separate lexer, parser and semantic implementation in distinct files
* parsing a whole text 
* handle errors wo fatal crash http://stackoverflow.com/questions/18046579/reporting-parse-errors-from-ply-to-caller-of-parser
* declare list of possible values for atomic constraints from a direct enumeration or from a file
* think about the context notion, and possibly about forcing the pattern to match from the begining ^ and/or to the end $
* regex operation in addition to match operation, offer the substitution sub/// and the annotation annotate/// ; the new feature is added to the current feature structure in a BIO style
* handle sequence of tokens with a BIO value as a single token
* extend the content of possible values of atomic constraints
* allow wildcards
* capture index of groups (identifiers required)
* reuse groups in regex
* make methods to turn nltk results into the input data structure (chunking Tree and IOB)
* lex.lex(reflags=re.UNICODE)
* move the python methods as grammar components
* allow grammar with multiple rules (each rule should have an identifier... and its own groupindex)
* Warning: when copying the grammar in the console, do not insert whitespace ahead


