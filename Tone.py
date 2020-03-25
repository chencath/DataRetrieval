

"""Quantify the sentiemnt of stocktwits messages
"""
import preprocessing as pre
import pandas as pd
import numpy as np
import datetime as dt


def read_lexicon():
    lex = pd.read_csv("Thomas_lexicon.csv", index_col=0, sep=";")
    lex[lex.sw == "positive"] = 1
    lex[lex.sw == "negative"] = -1
    return (lex["sw"].to_dict())


def terms(txt, lexicon):
    """Return the list of all terms of txt present in self.lex.

    Bigrams are prioritized over unigrams: if a unigram of txt is in self.lex,
    and is also part of a bigram of txt that is in self.lex, then only the
    bigram will be included in self.terms(txt).
    """
    words = txt.split(" ")
    terms = []
    n = len(words)
    for i, word in enumerate(words):
        term = word + " " + words[i + 1] if i < n - 1 else word
        if term in lexicon:
            terms.append(term)
        elif word in lexicon:
            terms.append(word)
    return (terms)



def tone(message, lexicon, preprocess=False):
    """Return the tone of message.

    message can either be a str or a StockTwits message.
    If preprocess is True, pre.preprocess is called on message first.
    Tone is computed as the mean of weights of terms present in both message
    and self.lex. If no such term exists, returned tone is NaN.
    """
    if preprocess:
      message = pre.preprocess(message)
    if not isinstance(message, str):
      message = message["body"]
    termList = terms(message, lexicon)
    if len(terms) > 0:
      return(np.mean([term for term in termList]))
    else:
      return(np.nan)

# read lexicon
with open('Thomas_lexicon.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        dct = dct + line

# create a list of lexicon
dct = dct.split('\n')
lexicon = [entry for entry in dct]

timeline = pd.read_csv("output/timeline.csv", index_col=1,parse_dates=True)
timeline["tone"] = [tone(m, lexicon) for m in timeline["body"]]
timeline["day"] = pd.to_datetime(timeline["created_at"]
                                     .apply(lambda t: t.date()))

tones = timeline.groupby("day")["tone"].mean()


