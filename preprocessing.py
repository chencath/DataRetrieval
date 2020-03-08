from string import punctuation
import numpy as np
from numpy.random import binomial
import pandas as pd
import json

PUNCTUATION = list(punctuation.replace("?", "").replace("!", ""))
NEGWORDS = ["not", "no", "none", "neither", "never", "nobody"]
STOPWORDS = ["an", "a", "the"] + NEGWORDS

def read_stream(symbol):
    """Return the stream of messages in database related to cur.

      cur must be a dictionary with at least keys "title" and "symbol".
    An empty list is returned if the corresponding JSON file doesn't exist yet.
      """
    try:
        with open("stream{}.json".format(symbol), "r", encoding="utf-8") as f:
            stream = json.load(f)
        return (stream)
    except FileNotFoundError:
        print("Stream not found for {} ({}).".format(["title"],["symbol"]))
        return ([])

# def read_cumStream(symbol):
#     """Return the stream of messages in database related to cur.
#
#       cur must be a dictionary with at least keys "title" and "symbol".
#     An empty list is returned if the corresponding JSON file doesn't exist yet.
#       """
#     try:
#         with open("cumStream{}.json".format(symbol), "r", encoding="utf-8") as f:
#             stream = json.load(f)
#         return (stream)
#     except FileNotFoundError:
#         print("Stream not found for {} ({}).".format(["title"],["symbol"]))
        return ([])

def make_timeline(symbol, path="timeline.csv"):
  """Create and save timeline to disk.

  The timeline is the time-ordered list of all messages in database without
  redundancies.
  It is saved as a CSV file with columns:
    id -- the unique id of the message
    created_at -- time at which was posted the message
    body -- the actual text of the message
    user -- the unique id of the author
    username -- the username of the author at the time he/she posted the message
    declared_sentiment -- 1 if the message was declared "Bullish" by the author,
                          -1 if it was declared "Bearish",
                          None (or empty field) otherwise
  """
  messages = []
  n = 0
  def extract_infos(message):
    return(message["id"], {
                           "created_at": message["created_at"],
                           "body": preprocess(message),
                           "user": message["user"]["id"],
                           "username": message["user"]["username"],
                           "declared_sentiment": _declared_sentiment(message)
                           })

  #messages.extend(extract_infos(read_stream(symbol)))
  # messages.extend([extract_infos(m) for m in read_stream(symbol)])
  messages.extend([extract_infos(m) for m in read_stream(symbol)['messages']])
  print(" "*(40 + n),"\rLoading and preprocessing...")
  print("Creating timeline...")
  dic = {id: infos for id, infos in messages}
  df = pd.DataFrame.from_dict(dic, orient='index')
  df["set"] = np.array(["training", "testing"])[binomial(1, 0.25, size=len(df))]
  df.index.name = "id"
  print("Writing to disk...")
  df.to_csv(path)
  print("Done.")


# def make_cum_timeline(symbol, path="cum_timeline.csv"):
#   """Create and save timeline to disk.
#
#   """
#   messages = []
#   n = 0
#   def extract_infos(message):
#     return(message["id"], {
#                            "created_at": message["created_at"],
#                            "body": preprocess(message),
#                            "user": message["user"]["id"],
#                            "username": message["user"]["username"],
#                            "declared_sentiment": _declared_sentiment(message)
#                            })
#
#   messages.extend([extract_infos(m) for m in read_cumStream(symbol)['messages']])
#   # messages.extend([extract_infos(m) for m in read_stream(symbol)['messages']])
#   print(" "*(40 + n),"\rLoading and preprocessing...")
#   print("Creating timeline...")
#   dic = {id: infos for id, infos in messages}
#   df = pd.DataFrame.from_dict(dic, orient='index')
#   df["set"] = np.array(["training", "testing"])[binomial(1, 0.25, size=len(df))]
#   df.index.name = "id"
#   print("Writing to disk...")
#   df.to_csv(path)
#   print("Done.")


def preprocess(m):
  """Preprocess m and return the corresponding str.

  m must be a dict with at least keys "body" and "symbol", or a str.
  """
  txt = _replace_symbols_users_links(m)
  txt = _remove_null_bytes(txt)
  # txt = _separate_emojis(txt)
  txt = txt.lower()
  txt = txt.replace("\n", " ")
  txt = txt.replace("\r", " ")
  txt = _remove_repeated_letters(txt)
  txt = _change_tags(txt, "$", "moneytag")
  txt = _change_tags(txt, "€", "moneytag")
  txt = _remove_punctuation(txt)
  txt = _numbertags(txt)
  txt = _contract_spaces(txt)
  txt = _negtags(txt)
  txt = _remove_stopwords(txt)
  txt = _contract_spaces(txt)
  if txt.startswith(" "):
    txt = txt[1:]
  return(txt)

def _remove_null_bytes(txt):
  return(txt.replace("\0", ""))

def _remove_stopwords(txt):
  """Delete from txt all words contained in STOPWORDS."""
  words = txt.split(" ")
  for i, word in enumerate(words):
    if word in STOPWORDS:
      words[i] = ""
  return(txt)

def _contract_spaces(txt):
  """Contract all repetitions of spaces to one space."""
  while "  " in txt:
    txt = txt.replace("  ", " ")
  return(txt)

def _replace_symbols_users_links(m):
  if type(m) is str:
    # SHOULD REPLACE SYMBOLS, USERS AND LINKS FOR RAW TEXT
    return(m)
  else:
    txt = m["body"]
    #symbols
    for s in m["symbols"]:
      txt = txt.replace("$" + s["symbol"], "cashtag")
      if "aliases" in s:
        for alias in s["aliases"]:
          txt = txt.replace("$" + alias, "cashtag")
    #users
    if "mentioned_users" in m:
      for u in m["mentioned_users"]:
        txt = txt.replace(u,  "usertag")
    #links
    if "links" in m:
      for l in m["links"]:
        txt = txt.replace(l["url"], "linktag")
  return(txt)

# def _separate_emojis(txt):
#   """Add a space before and after each emoji."""
#   for e in EMOJIS:
#     if e in txt:
#       txt = txt.replace(e, " " + e + " ")
#   return(txt)

def _remove_repeated_letters(txt):
  n = len(txt)
  if n < 4:
    return(txt)
  c1, c2, c3 = txt[0], txt[1], txt[2]
  txt2 = c1 + c2 + c3
  for i in range(3, n):
    if not(txt[i] == c1 == c2 == c3):
      txt2 += txt[i]
      c1, c2, c3 = c2, c3, txt[i]
  return(txt2)

def _numbertags(txt):
  """Replace all numbers by "numbertag"."""
  words = txt.split(" ")
  for i, word in enumerate(words):
    if word.isnumeric():
      words[i] = "numbertag"
  return(" ".join(words))

def _change_tags(txt, tag, newtag):
  """Replace words starting with tag by newtag."""
  words = txt.split(" ")
  for i, word in enumerate(words):
    if word.startswith(tag):
      words[i] = newtag
  return(" ".join(words))

def _remove_punctuation(txt):
  characters = list(txt)
  n = len(characters)
  insert, offset = [], 0
  for i in range(n):
    if characters[i] in PUNCTUATION:
      if 0 < i < n-1 and " " not in [characters[i-1], characters[i+1]]:
        characters[i] = " "
      else:
        characters[i] = ""
    if characters[i] in ["!", "?"] and characters[i-1] != " ":
      insert.append((i + offset, " "))
      offset += 1
  for i, c in insert:
    characters.insert(i, c)
  return("".join(characters))

def _negtags(txt):
  """Add "negtag_" to all words following one of NEGWORDS."""
  words = txt.split(" ")
  n = len(words)
  for i, word in reversed(list(enumerate(words))):
    if word in NEGWORDS:
      if i < n-1:
        words.pop(i)
        words[i] = "negtag_" + words[i]
      else:
        words[i] = "negtag_"
  return(" ".join(words))

def _declared_sentiment(message):
  stm = message["entities"]["sentiment"]
  return(2*int(stm["basic"] == "Bullish") - 1 if stm is not None else None)
