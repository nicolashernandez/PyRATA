Demo

* API demonstration in Python command line interpreter
* pyrata_re.py (which plots NFA graphs) in bash command line 

API demo
===========================

Requirement in python interpreter
----------------------------------------------------

python3

# only required for pyrata_re.py, a demo script to test PyRATA API in command line and plot NFA graphs
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags

# nice display
import pprint

# pyrata
import pyrata.re as pyrata_re


Generating a PyRATA data structure from a text
---------------------------------------------------

# our data (here a simple sentence)
data = 'Van Damme is much cooler than Chuck Norris. Silvester Stalone is an American actor and filmmaker.'

# nltk to process the data and format it into a list of dicts 
pyrata_data =  [{'raw':word, 'pos':pos, 'lem':nltk.WordNetLemmatizer().lemmatize(word.lower())} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(data))]


# have a look at the result 
pyrata_data

# or
pprint.pprint(pyrata_data)

::

    [{'lem': 'van', 'pos': 'NNP', 'raw': 'Van'},
     {'lem': 'damme', 'pos': 'NNP', 'raw': 'Damme'},
     {'lem': 'is', 'pos': 'VBZ', 'raw': 'is'},
     {'lem': 'much', 'pos': 'RB', 'raw': 'much'},
     {'lem': 'cooler', 'pos': 'JJR', 'raw': 'cooler'},
     {'lem': 'than', 'pos': 'IN', 'raw': 'than'},
     {'lem': 'chuck', 'pos': 'NNP', 'raw': 'Chuck'},
     {'lem': 'norris', 'pos': 'NNP', 'raw': 'Norris'},
     {'lem': '.', 'pos': '.', 'raw': '.'},
     {'lem': 'silvester', 'pos': 'NNP', 'raw': 'Silvester'},
     {'lem': 'stalone', 'pos': 'NNP', 'raw': 'Stalone'},
     {'lem': 'is', 'pos': 'VBZ', 'raw': 'is'},
     {'lem': 'an', 'pos': 'DT', 'raw': 'an'},
     {'lem': 'american', 'pos': 'JJ', 'raw': 'American'},
     {'lem': 'actor', 'pos': 'NN', 'raw': 'actor'},
     {'lem': 'and', 'pos': 'CC', 'raw': 'and'},
     {'lem': 'filmmaker', 'pos': 'NN', 'raw': 'filmmaker'},
     {'lem': '.', 'pos': '.', 'raw': '.'}]

# Note: The lemmatization for *is* is wrong. Should be *be* 


Quantifiers ``?+*`` and matching equal ``=`` operator to recognize simple Noun Phrases 
----------------------------------------------------

pyrata_np_pattern = 'pos="DT"? pos="JJ"* pos="NN"+'

found_noun_phrases = pyrata_re.findall(pyrata_np_pattern , pyrata_data)

pprint.pprint(found_noun_phrases)

:: 
    [[{'lem': 'an', 'pos': 'DT', 'raw': 'an'},
      {'lem': 'american', 'pos': 'JJ', 'raw': 'American'},
      {'lem': 'actor', 'pos': 'NN', 'raw': 'actor'}],
     [{'lem': 'filmmaker', 'pos': 'NN', 'raw': 'filmmaker'}]]


(maching operators) With the ``=`` operator, there are 4 constraints operators. Here the regular expression (re) ``~`` operator
----------------------------------------------------

pyrata_np_pattern = 'pos="DT"? pos~"(JJ|NN).?"* pos~"NN.?"+'

found_noun_phrases = pyrata_re.findall(pyrata_np_pattern , pyrata_data)

pprint.pprint(found_noun_phrases)


:: 

    [[{'lem': 'van', 'pos': 'NNP', 'raw': 'Van'},
      {'lem': 'damme', 'pos': 'NNP', 'raw': 'Damme'}],
     [{'lem': 'chuck', 'pos': 'NNP', 'raw': 'Chuck'},
      {'lem': 'norris', 'pos': 'NNP', 'raw': 'Norris'}],
     [{'lem': 'silvester', 'pos': 'NNP', 'raw': 'Silvester'},
      {'lem': 'stalone', 'pos': 'NNP', 'raw': 'Stalone'}],
     [{'lem': 'an', 'pos': 'DT', 'raw': 'an'},
      {'lem': 'american', 'pos': 'JJ', 'raw': 'American'},
      {'lem': 'actor', 'pos': 'NN', 'raw': 'actor'}],
     [{'lem': 'filmmaker', 'pos': 'NN', 'raw': 'filmmaker'}]]


(API) Various search methods. In addition to findall, there is ``finditer`` which returns an iterator of Match objects (with offsets) 
----------------------------------------------------

pyrata_np_pattern = 'pos="DT"? pos~"(JJ|NN).?"* pos~"NN.?"+'

found_noun_phrases = pyrata_re.finditer(pyrata_np_pattern , pyrata_data)

# same results as above but with ``finditer`` instead of ``findall``

found_noun_phrases

:: 
    <pyrata.re MatchesList object; matcheslist="[
    <pyrata.re Match object; groups=[[[{'pos': 'NNP', 'raw': 'Van', 'lem': 'van'}, {'pos': 'NNP', 'raw': 'Damme', 'lem': 'damme'}], 0, 2]]>, 
    <pyrata.re Match object; groups=[[[{'pos': 'NNP', 'raw': 'Chuck', 'lem': 'chuck'}, {'pos': 'NNP', 'raw': 'Norris', 'lem': 'norris'}], 6, 8]]>, 
    <pyrata.re Match object; groups=[[[{'pos': 'NNP', 'raw': 'Silvester', 'lem': 'silvester'}, {'pos': 'NNP', 'raw': 'Stalone', 'lem': 'stalone'}], 9, 11]]>, 
    <pyrata.re Match object; groups=[[[{'pos': 'DT', 'raw': 'an', 'lem': 'an'}, {'pos': 'JJ', 'raw': 'American', 'lem': 'american'}, {'pos': 'NN', 'raw': 'actor', 'lem': 'actor'}], 12, 15]]>, 
    <pyrata.re Match object; groups=[[[{'pos': 'NN', 'raw': 'filmmaker', 'lem': 'filmmaker'}], 16, 17]]>
    ]">


Class element 
----------------------------------------------------

# square brackets allows to define a class of tokens by logically combining the features to match 
# can be used with quantifiers

# below the pattern accepts a sequence of tokens starting with an uppercase letter but not an adjective, or a NNP pos tag. 
NE_pattern = '[ (raw~"^[A-Z]" & !pos="JJ") | pos="NNP"]+'

# findall
NE = pyrata_re.findall (NE_pattern, pyrata_data)

pprint.pprint(NE)  

::

    [[{'lem': 'van', 'pos': 'NNP', 'raw': 'Van'},
      {'lem': 'damme', 'pos': 'NNP', 'raw': 'Damme'}],
     [{'lem': 'chuck', 'pos': 'NNP', 'raw': 'Chuck'},
      {'lem': 'norris', 'pos': 'NNP', 'raw': 'Norris'}],
     [{'lem': 'silvester', 'pos': 'NNP', 'raw': 'Silvester'},
      {'lem': 'stalone', 'pos': 'NNP', 'raw': 'Stalone'}]]


(API) Updating (edit operation) a PyRATA data structure by modifying a feature value 
----------------------------------------------------

updated_pyrata_data = pyrata_re.update ('[lem="is" | lem="are" | lem="wa"]', {'lem':'be'}, pyrata_data)

pprint.pprint(updated_pyrata_data)

::

    [{'lem': 'van', 'pos': 'NNP', 'raw': 'Van'},
     {'lem': 'damme', 'pos': 'NNP', 'raw': 'Damme'},
     {'lem': 'be', 'pos': 'VBZ', 'raw': 'is'},
     {'lem': 'much', 'pos': 'RB', 'raw': 'much'},
     {'lem': 'cooler', 'pos': 'JJR', 'raw': 'cooler'},
     {'lem': 'than', 'pos': 'IN', 'raw': 'than'},
     {'lem': 'chuck', 'pos': 'NNP', 'raw': 'Chuck'},
     {'lem': 'norris', 'pos': 'NNP', 'raw': 'Norris'},
     {'lem': '.', 'pos': '.', 'raw': '.'},
     {'lem': 'silvester', 'pos': 'NNP', 'raw': 'Silvester'},
     {'lem': 'stalone', 'pos': 'NNP', 'raw': 'Stalone'},
     {'lem': 'be', 'pos': 'VBZ', 'raw': 'is'},
     {'lem': 'an', 'pos': 'DT', 'raw': 'an'},
     {'lem': 'american', 'pos': 'JJ', 'raw': 'American'},
     {'lem': 'actor', 'pos': 'NN', 'raw': 'actor'},
     {'lem': 'and', 'pos': 'CC', 'raw': 'and'},
     {'lem': 'filmmaker', 'pos': 'NN', 'raw': 'filmmaker'},
     {'lem': '.', 'pos': '.', 'raw': '.'}]


(API) Extending (edit operation) a PyRATA data structure by adding a new feature
----------------------------------------------------

# using the previously defined ``pyrata_np_pattern`` and working on ``updated_pyrata_data``, we add the features ``{'chunk':'NP'}`` to each token matched by the pattern.

extended_pyrata_data = pyrata_re.extend (pyrata_np_pattern, {'chunk':'NP'}, updated_pyrata_data)

pprint.pprint(extended_pyrata_data)  

::

    [{'chunk': 'NP', 'lem': 'van', 'pos': 'NNP', 'raw': 'Van'},
     {'chunk': 'NP', 'lem': 'damme', 'pos': 'NNP', 'raw': 'Damme'},
     {'lem': 'be', 'pos': 'VBZ', 'raw': 'is'},
     {'lem': 'much', 'pos': 'RB', 'raw': 'much'},
     {'chunk': 'NP', 'lem': 'cooler', 'pos': 'JJR', 'raw': 'cooler'},
     {'lem': 'than', 'pos': 'IN', 'raw': 'than'},
     {'chunk': 'NP', 'lem': 'chuck', 'pos': 'NNP', 'raw': 'Chuck'},
     {'chunk': 'NP', 'lem': 'norris', 'pos': 'NNP', 'raw': 'Norris'},
     {'lem': '.', 'pos': '.', 'raw': '.'},
     {'chunk': 'NP', 'lem': 'silvester', 'pos': 'NNP', 'raw': 'Silvester'},
     {'chunk': 'NP', 'lem': 'stalone', 'pos': 'NNP', 'raw': 'Stalone'},
     {'lem': 'be', 'pos': 'VBZ', 'raw': 'is'},
     {'chunk': 'NP', 'lem': 'an', 'pos': 'DT', 'raw': 'an'},
     {'chunk': 'NP', 'lem': 'american', 'pos': 'JJ', 'raw': 'American'},
     {'chunk': 'NP', 'lem': 'actor', 'pos': 'NN', 'raw': 'actor'},
     {'lem': 'and', 'pos': 'CC', 'raw': 'and'},
     {'chunk': 'NP', 'lem': 'filmmaker', 'pos': 'NN', 'raw': 'filmmaker'},
     {'lem': '.', 'pos': '.', 'raw': '.'}]


(API) Extending a PyRATA data structure with IOB values
----------------------------------------------------

# when the match is a token sequence (i.e. a chunk), it is possible to force the value of the extended feature to be in IOB format (i.e. with a value starting by *B-* if the token starts the chunk, *I-* it the token is inside the chunk, and "O-" for all other cases). To do that simply add ``iob=True`` as parameter of the extend method.

extended_pyrata_data = pyrata_re.extend (pyrata_np_pattern, {'chunk':'NP'}, updated_pyrata_data, iob=True)

# Below the same result as just above except that *chunk* values have got IOB prefix now. 

pprint.pprint(extended_pyrata_data)  

::

    [{'chunk': 'B-NP', 'lem': 'van', 'pos': 'NNP', 'raw': 'Van'},
     {'chunk': 'I-NP', 'lem': 'damme', 'pos': 'NNP', 'raw': 'Damme'},
     {'lem': 'be', 'pos': 'VBZ', 'raw': 'is'},
     {'lem': 'much', 'pos': 'RB', 'raw': 'much'},
     {'chunk': 'B-NP', 'lem': 'cooler', 'pos': 'JJR', 'raw': 'cooler'},
     {'lem': 'than', 'pos': 'IN', 'raw': 'than'},
     {'chunk': 'B-NP', 'lem': 'chuck', 'pos': 'NNP', 'raw': 'Chuck'},
     {'chunk': 'I-NP', 'lem': 'norris', 'pos': 'NNP', 'raw': 'Norris'},
     {'lem': '.', 'pos': '.', 'raw': '.'},
     {'chunk': 'B-NP', 'lem': 'silvester', 'pos': 'NNP', 'raw': 'Silvester'},
     {'chunk': 'I-NP', 'lem': 'stalone', 'pos': 'NNP', 'raw': 'Stalone'},
     {'lem': 'be', 'pos': 'VBZ', 'raw': 'is'},
     {'chunk': 'B-NP', 'lem': 'an', 'pos': 'DT', 'raw': 'an'},
     {'chunk': 'I-NP', 'lem': 'american', 'pos': 'JJ', 'raw': 'American'},
     {'chunk': 'I-NP', 'lem': 'actor', 'pos': 'NN', 'raw': 'actor'},
     {'lem': 'and', 'pos': 'CC', 'raw': 'and'},
     {'chunk': 'B-NP', 'lem': 'filmmaker', 'pos': 'NN', 'raw': 'filmmaker'},
     {'lem': '.', 'pos': '.', 'raw': '.'}]


(matching operator) Chunk can be matched thanks to the chunk ``-``operator
----------------------------------------------------

who_is_an_actor_pattern = 'chunk-"NP" lem="be" [pos="DT" | pos="JJ"]* lem="actor"'

who_is_an_actor = pyrata_re.findall (who_is_an_actor_pattern, extended_pyrata_data)

pprint.pprint(who_is_an_actor)  

::

    [[{'chunk': 'B-NP', 'lem': 'silvester', 'pos': 'NNP', 'raw': 'Silvester'},
      {'chunk': 'I-NP', 'lem': 'stalone', 'pos': 'NNP', 'raw': 'Stalone'},
      {'lem': 'be', 'pos': 'VBZ', 'raw': 'is'},
      {'chunk': 'B-NP', 'lem': 'an', 'pos': 'DT', 'raw': 'an'},
      {'chunk': 'I-NP', 'lem': 'american', 'pos': 'JJ', 'raw': 'American'},
      {'chunk': 'I-NP', 'lem': 'actor', 'pos': 'NN', 'raw': 'actor'}]]

specify group you want to work on with parenthesis 
--------------------------------------------------

# the group is marked with parenthesis
who_is_an_actor_pattern = '(chunk-"NP") lem="be" [pos="DT" | pos="JJ"]* lem="actor"'

# we search the first occurrence and get the first group in the recognized pattern
who_is_an_actor = pyrata_re.search (who_is_an_actor_pattern, extended_pyrata_data).groups()[1]

who_is_an_actor

::

    [[{'pos': 'NNP', 'chunk': 'B-NP', 'raw': 'Silvester', 'lem': 'silvester'}, {'pos': 'NNP', 'chunk': 'I-NP', 'raw': 'Stalone', 'lem': 'stalone'}], 9, 11]


# here how to get a list of actors in the whole corpus
who_is_an_actor_list = [i.groups()[1] for i in pyrata_re.finditer (who_is_an_actor_pattern, extended_pyrata_data)]

# Note: ``chunk-"NP"`` is actually rewritten in ``(chunk="B-NP" chunk="I-NP"*)`` which is a group. So by marking explicitly groups around chunks, it is redundant. Without parenthesis it gives so the same:

who_is_an_actor_pattern = 'chunk-"NP" lem="be" [pos="DT" | pos="JJ"]* lem="actor"'
who_is_an_actor = pyrata_re.search (who_is_an_actor_pattern, extended_pyrata_data).groups()[1]


(matching operator) token features can be constraint to belong to lexicons thanks to ``@``operator
----------------------------------------------------  
# declaration of 4 lexicons (name then a list of values)
my_lexicons = { 'POS_ADJ':['cooler', 'stronger'], 
                'NEG_ADJ':['weaker', 'worst'],
                'POS_ADV':['much', 'more'],
                'NEG_ADV':['less', 'not']}

# sequence of adverbs which are not negative and adjectives which are positive
is_better_than_pattern = 'chunk-"NP" lem="be" ([ (pos="RB" & !lem@"NEG_ADV") | (pos~"JJ." & lem@"POS_ADJ") ]+) lem="than" chunk-"NP"'

# searching the first occurrence by giving the lexicons in parameters
is_better_than = pyrata_re.search (is_better_than_pattern, extended_pyrata_data, lexicons = my_lexicons).groups()[2]

is_better_than
::

    [[{'pos': 'RB', 'raw': 'much', 'lem': 'much'}, 
     {'pos': 'JJR', 'chunk': 'B-NP', 'raw': 'cooler', 'lem': 'cooler'}], 3, 5]


group alternatives
------------------------------------------

# positive adjective optionally stressed by a positive adverb
# or 
# negative adjective mandatory preceded by a negative adverb to reverse the polarity 
is_better_than_pattern = 'lem="be" (lem@"POS_ADV"? lem@"POS_ADJ"| lem@"NEG_ADV" lem@"NEG_ADJ") lem="than"'

# 
pyrata_re.search (is_better_than_pattern, extended_pyrata_data, lexicons = my_lexicons).groups()[1]

:: 

    [[{'pos': 'RB', 'lem': 'much', 'raw': 'much'}, {'pos': 'JJR', 'lem': 'cooler', 'raw': 'cooler'}], 3, 5]




pyrata_re.py 
================

# Warning: exported pdf wont be viewed from the current docker image 
#
# PyRATA comes with a script, pyrata_re.py, which allow to test the API and plots pretty graphs of NFAs. In v0.4 it is an alpha code. It is provided "as is"... Set your PATH environment variable consequently or run it from its install directory.
#
# Takes at least two parameters: the pattern to search and the data to process.
#
# By default, it performs English natural language processing (nlp) with NLTK on the input data and search the first occurrence of the specified pattern with a greedy pattern matching policy. No pdf draw. No log export. 

# assuming pyrata_re.py is in the current directory. Change directory so. In the docker image:
cd /root

# More information on parameters, API usage and language syntax with:

python3 pyrata_re.py -h


# For example to search the first match of given pattern (sequence of adjectives) by using some basic nlp processing (tokenization, pos tagging...):

python3 pyrata_re.py 'pos="JJ"+' "It is fast easy and funny to write regular expressions with PyRATA"


# To operate with the raw PyRATA data structure

python3 pyrata_re.py 'pos="JJ"+' "[{'raw': 'It', 'pos': 'PRP'}, {'raw': 'is', 'pos': 'VBZ'}, {'raw': 'fast', 'pos': 'JJ'}, {'raw': 'easy', 'pos': 'JJ'}, {'raw': 'and', 'pos': 'CC'}, {'raw': 'funny', 'pos': 'JJ'}, {'raw': 'to', 'pos': 'TO'}, {'raw': 'write', 'pos': 'VB'}, {'raw': 'regular', 'pos': 'JJ'}, {'raw': 'expressions', 'pos': 'NNS'}, {'raw': 'with', 'pos': 'IN'}, {'raw': 'PyRATA', 'pos': 'NNP'}]"  --pyrata_data


# To find all occurrences (by default in greedy mode) 

python3 pyrata_re.py 'pos="JJ"+' "It is fast easy and funny to write regular expressions with PyRATA"  --method findall 

# we see 3 matches
::

    [[{'chunk': 'O',
       'lc': 'fast',
       'lem': 'fast',
       'pos': 'JJ',
       'raw': 'fast',
       'stem': 'fast',
       'sw': False},
      {'chunk': 'O',
       'lc': 'easy',
       'lem': 'easy',
       'pos': 'JJ',
       'raw': 'easy',
       'stem': 'easi',
       'sw': False}],

     [{'chunk': 'O',
       'lc': 'funny',
       'lem': 'funny',
       'pos': 'JJ',
       'raw': 'funny',
       'stem': 'funni',
       'sw': False}],
     
     [{'chunk': 'O',
       'lc': 'regular',
       'lem': 'regular',
       'pos': 'JJ',
       'raw': 'regular',
       'stem': 'regular',
       'sw': False}]]


# To find all occurrences in reluctant mode 

python3 pyrata_re.py 'pos="JJ"+' "It is fast easy and funny to write regular expressions with PyRATA"  --method findall --mode reluctant


# each adjective is a match
::

    [[{'chunk': 'O',
       'lc': 'fast',
       'lem': 'fast',
       'pos': 'JJ',
       'raw': 'fast',
       'stem': 'fast',
       'sw': False}],
     [{'chunk': 'O',
       'lc': 'easy',
       'lem': 'easy',
       'pos': 'JJ',
       'raw': 'easy',
       'stem': 'easi',
       'sw': False}],
     [{'chunk': 'O',
       'lc': 'funny',
       'lem': 'funny',
       'pos': 'JJ',
       'raw': 'funny',
       'stem': 'funni',
       'sw': False}],
     [{'chunk': 'O',
       'lc': 'regular',
       'lem': 'regular',
       'pos': 'JJ',
       'raw': 'regular',
       'stem': 'regular',
       'sw': False}]]


#To draw the corresponding NFA in a filename my_nfa.pdf. Trick: No need to specify some data to draw a NFA.

python3 pyrata_re.py 'pos="DT"? pos~"JJ|NN"* pos~"NN.?"+' "" --draw --pdf_file_name my_nfa.pdf 
# && evince my_nfa.pdf

to copy files from the docker container to the local file system (to use a pdf viewer for instance)
--------------------------------------- 

# get the container NAME 
sudo docker ps

# then from a terminal in the local file system do
# sudo docker cp NAME:/root/my_nfa.pdf /tmp/my_nfa.pdf && evince my_nfa.pdf

# if NAME is *nostalgic_northcutt* then do
sudo docker cp nostalgic_northcutt:/root/my_nfa.pdf /tmp/my_nfa.pdf && evince /tmp/my_nfa.pdf



more nlp processing
-----------------------
pyrata_data = [{'raw':word, 'lc':word.lower(), 'pos':pos, 'stem':nltk.stem.SnowballStemmer('english').stem(word), 'lem':nltk.WordNetLemmatizer().lemmatize(word.lower()), 'sw':(word in nltk.corpus.stopwords.words('english')), 'chunk':chunk} for (word, pos, chunk) in tree2conlltags(ne_chunk(pos_tag(word_tokenize(data))))]


working on brown corpus (experimental)
-------------------
from nltk.corpus import brown

# selection of a sub-corpus
text_length = 200000 # len(brown.words())
tokens = brown.words()
tokens = tokens[:text_length]

# nlp processing 
pos_tags = nltk.pos_tag(tokens)

# and pyrata formating
pyrata_data = [{'raw':w, 'pos':p} for (w, p) in pos_tags]

# who is what (takes a few seconds) 
result = pyrata_re.findall('[pos~"NN" & raw~"^[A-Z]"]+ raw~"^(is|are)$" pos="DT"? pos~"JJ|NN.?"* pos~"NN.?"+', pyrata_data)

pprint.pprint(result)