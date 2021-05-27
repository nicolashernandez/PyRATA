import pyrata.re as pyrata_re

sentence = "It is fast easy and funny to write regular expressions with PyRATA"

data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': '44'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]
#adding features example : word position in the sentence
i = 1
for word in data :
    word["position"] = str(i)
    i+=1

# pattern = 'pos="JJ" [pos="JJ" & (position="44" | position="4")] [!pos="VBZ" | position~"[3-6]"]'
pattern = 'pos="JJ" [pos="JJ" & (!pos="JJ" | position="4")] [!pos="VBZ" | position~"[3-6]"]'
print(pyrata_re.findall(pattern, data))


# # = operator
# # pattern = 'position="9"'
# # pattern = 'pos="JJ"'
#
# # ~ operator
# pattern = 'position~"^[1-5]$"'
#
# # @ operator
# ParityLexicon = {'EvenLexicon':['0', '2','4','6','8','10','12','14','16',],
#                  'OddLexicon':['1', '3','5','7','9','11','13','15','17']}
# Lexicon = {'ItLexicon':["It"]}
# #method using @ operator
# # print(pyrata_re.findall('position@"EvenLexicon"', data, ParityLexicon))
#

# # print(pyrata_re.findall(pattern, data))
#
# #element class
# #print(pyrata_re.findall('[(position="8" | pos="JJ") & !raw="easy"]', data))
#
# # . wildcard element
# # print(pyrata_re.search('position="2" . raw="easy"', data))
#
#
# #Chunk dataset
#
# # Chunkdata = [{'pos': 'NNP', 'chunk': 'I-PERSON', 'raw': 'Mark'}, {'pos': 'NNP', 'chunk': 'I-PERSON', 'raw': 'Zuckerberg'}, {'pos': 'VBZ', 'chunk': 'O', 'raw': 'is'}, {'pos': 'VBG', 'chunk': 'I-PERSON', 'raw': 'working'}, {'pos': 'IN', 'chunk': 'O', 'raw': 'at'}, {'pos': 'NNP', 'chunk': 'B-ORGANIZATION', 'raw': 'Facebook'}, {'pos': 'NNP', 'chunk': 'I-ORGANIZATION', 'raw': 'Corp'}, {'pos': '.', 'chunk': 'O', 'raw': '.'}]
# # patternChunk = 'chunk="I-PERSON"*'
# # print(pyrata_re.search(patternChunk, Chunkdata))
#
# dataV1 =[{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}]
#
# patternV1 = 'raw="It" raw="is"'
#
# print(pyrata_re.findall(patternV1, dataV1))


