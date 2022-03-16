""" Find the 'synonyms', 'antonyms' of specific word using Wordnet
https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
Import wordnet module

"""


from nltk.corpus import wordnet
import numpy as np
import pandas as pd

syns = wordnet.synsets("program")
print(syns[0].name())
print(syns[0].lemmas()[0].name())


coop_list = ['good', 'happy', 'joy']
df = pd.DataFrame({'word': [], 'synonyms': [], 'antonyms': []})

for item in coop_list:
    for syn in wordnet.synsets(item):
        synonyms = []
        antonyms = []
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
        df = df.append({'word': item, 'synonyms': synonyms, 'antonyms': antonyms}, ignore_index=True)

#  search synonyms on specific word in the created dataframe
df.index = df['word']
searchTerm = ['good']
mask = [ term in searchTerm for term in df.index ]
# silicing the dataframe for the desired porportion
df[mask]
# print the column in the sliced dataframe
df[mask]['synonyms']
synList = list(df[mask]['synonyms'])

for word in np.unique(synList):
    print(word)
