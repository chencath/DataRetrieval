
""" Using NLTK for
    1. removing stopwords
    2. do tokenization

."""


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_sent = "This is a sample sentence, showing off the stop words filtration."
# stop words in English
stop_words = set(stopwords.words('english'))
# stop words in German
stop_words_German = set(stopwords.words('german'))
# stop words in Italian
stop_words_italian = set(stopwords.words('italian'))

word_tokens = word_tokenize(example_sent)
# compact syntax
filtered_sentence = [w for w in word_tokens if w not in stop_words]
# standard syntax
filtered_sentence = []
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

print(word_tokens)
print(filtered_sentence)
