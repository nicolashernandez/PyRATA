# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Nicolas Hernandez 2017
# 
# Turn common nltk process to pyrata data structure to perform re precessing
# 
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

rawFeatureName = 'raw'
posFeatureName = 'pos'

def list2pyrata (**kwargs):
  """ turn a list 'list' into a list of dict 
  e.g. a list of words into a list of dict 
  with a feature to represent the surface form of the word"""
  alist = []
  if 'list' in kwargs.keys(): # MANDATORY
    alist = kwargs['list']
  #kwargs.pop('list', None)
  name = 'f0'
  if 'name' in kwargs.keys(): # MANDATORY
    name = kwargs['name']

  dictList = []
  if 'dictList' in kwargs.keys(): # MANDATORY
    dictList = kwargs['dictList']

  if len(dictList) != 0:
    ''' extend a given dictList'''
    if len(dictList) == len(alist):
      for i in range(len(dictList)):
        dictList[i][name] = alist[i]
    else:
      raise Exception('list2pyrata - len of a given dictList should be equal to the len of a list')
  else:  
    for element in alist:
      currentDict = {}
      currentDict[name] = element
      dictList.append(currentDict)
  return dictList

def listList2pyrata (**kwargs):
  """ turn a list of list 'listList' into a list of dict
  with values being the elements of the second list ; 
  the value names are arbitrary choosen. 
  """
  alistList = []
  if 'listList' in kwargs.keys(): # MANDATORY
    alistList = kwargs['listList']
  
  if len(alistList)==0:
        raise Exception('listList2pyrata - len of listList cannot be empty')

  names = ['f'+str(i) for i in range (len(alistList[0]))] 
  # TODO len of contained list should be also checked (should not be empty and always have the same size)
  if 'names' in kwargs.keys(): # MANDATORY
    names = kwargs['names']
  if len(names)==0:
    raise Exception('listList2pyrata - len of names cannot be empty')

  dictList = []
  if 'dictList' in kwargs.keys(): # MANDATORY
    dictList = kwargs['dictList']

  #print ('Debug: dictList=',dictList,'\n')
  if len(dictList) != 0:
    ''' extend a given dictList'''
    if len(dictList) == len(alistList):
      for j in range(len(alistList)):
        adict = dictList[j]
        alist = alistList[j]
        for i in range(0,len(alist)):
          adict[names[i]]=alist[i]
        dictList[j] = adict
    else:
      raise Exception('listList2pyrata - len of a given dictList should be equal to the len of a listList')
  else:
    ''' create a dictList from scratch '''
    for alist in alistList:  
      adict = {}
      for i in range(0,len(alist)):
        adict[names[i]]=alist[i]
      dictList.append(adict)
  
  return dictList 


# extend a given dictList 

# merge dictList

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Run all the tests
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':

  import nltk
  lemmatizer = nltk.WordNetLemmatizer()
  stemmer = nltk.stem.SnowballStemmer('english')
  stopwords = nltk.corpus.stopwords.words('english')

  sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
  tokens = nltk.word_tokenize(sentence)

  
  print ('sentence:', sentence,'\n')
  print ('nltk tokens:',tokens,'\n')
  print ('pyrata wo name:',list2pyrata(list=tokens),'\n')
  print ('pyrata wi name:',list2pyrata(list=tokens, name='raw'),'\n')

  lowercases = [w.lower() for w in tokens]
  lowercasesdictlist = [{'lc' : w.lower()} for w in tokens]  
  print ('pyrata wi name and dictList wi name:',list2pyrata(list=tokens, name='raw', dictList=lowercasesdictlist),'\n')
  
  pos = nltk.pos_tag(tokens)
  print ('nltk pos:',pos,'\n')
  print ('pyrata wo names:',listList2pyrata(listList=pos),'\n')
  print ('pyrata wi names:',listList2pyrata(listList=pos, names=['raw', 'pos']),'\n')
  
  dictList = list2pyrata(list=tokens)
  print ('pyrata wo names but dictList wo name:',listList2pyrata(listList=pos,dictList=dictList),'\n')
  
  dictList = list2pyrata(list=tokens)
  print ('pyrata wi names and dictList wo name:',listList2pyrata(listList=pos, names=['raw', 'pos'],dictList=dictList),'\n')

  dictList = list2pyrata(list=tokens, name ='raw')
  print ('pyrata wo names but dictList wi name:',listList2pyrata(listList=pos,dictList=dictList),'\n')
  
  dictList = list2pyrata(list=tokens, name ='raw')
  print ('pyrata wi names and dictList wi name:',listList2pyrata(listList=pos, names=['raw', 'pos'],dictList=dictList),'\n')

  pyrata = [{'raw':word, 'pos':pos, 'stem':stemmer.stem(word), 'lem':lemmatizer.lemmatize(word.lower()), 'sw':(word in stopwords)} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
  print ('pyrata in one single line:',pyrata,'\n')

  ne_chunk_tree = nltk.chunk.ne_chunk(tagged_sent)  
  # TODO 
  #Tree('S', [('Today', 'NN'), ('you', 'PRP'), ("'ll", 'MD'), ('be', 'VB'), ('learning', 'VBG'), Tree('ORGANIZATION', [('NLTK', 'NNP')]), ('.', '.')])
  # tree.draw()

  # TODO http://stackoverflow.com/questions/30664677/extract-list-of-persons-and-organizations-using-stanford-ner-tagger-in-nltk
  # https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software

#    http://www.ling.helsinki.fi/kit/2009s/clt231/NLTK/book/ch07-ExtractingInformationFromText.html
# https://github.com/nltk/nltk.github.com/blob/master/book/pylisting/code_classifier_chunker.py