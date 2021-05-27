import pyrata.re as pyrata_re



pattern = 'pos="JJ" raw="pos=\'JJ\'"'

data = [{'pos': 'JJ', 'raw': 'It'}, {'pos': 'VBZ', 'raw': "pos='JJ'"}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]

print(pyrata_re.findall(pattern, data))