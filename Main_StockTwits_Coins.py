
import importlib
import StockTwitsAPI
importlib.reload(StockTwitsAPI)
import pandas as pd
import json
import os
import datetime as dt
import time
from StockTwitsAPI import StockTwitsApi    # create module NewsAPI for object class "NewsApi"

with open("access_token_stockTwits.txt", "r") as f:
    access_token = f.read()[:-1]

api = StockTwitsApi(access_token)


def list_currencies():
    """Return the list of currencies in database."""
    with open("currencies.json", "r", encoding="utf-8") as f:
        return (json.load(f))


def read_stream(cur):
    """Return the stream of messages in database related to cur.

      cur must be a dictionary with at least keys "title" and "symbol".
    An empty list is returned if the corresponding JSON file doesn't exist yet.
      """
    try:
        with open("stream{}.json".format(cur["symbol"]), "r", encoding="utf-8") as f:
            stream = json.load(f)
        return (stream)
    except FileNotFoundError:
        print("Stream not found for {} ({}).".format(cur["title"], cur["symbol"]))
        return ([])


def collect(cur):
  """Download cur-related messages that are older than the oldest in database.
	"""
  stream = read_stream(cur)
  max = None if len(stream) == 0 else stream[-1]["id"]
  more, success = True, True
  while more:
    kwargs = {"id": cur["id"]}
    if max is not None:
      kwargs["max"] = max
    newstream = api.stream_symbol(**kwargs).json()
    status = newstream["response"]["status"]
    if status == 200: # Success
      if len(newstream["messages"]) > 0:
        stream += newstream["messages"]
        max = stream[-1]["id"]
      else:
        more = False
    elif status == 404: # Symbol not found
      print(newstream["errors"][0]["message"])
      more = False
    else: # Other errors from StockTwits
      [print(e["message"]) for e in newstream["errors"]]
      success, more = False, False
  if len(stream) > 0:
    print("Oldest message collected was created on {}.".format(stream[-1]["created_at"]))
    with open("stream{}.json".format(cur["symbol"]), "w", encoding="utf-8") as f:
      json.dump(stream, f)
  return(success)

def update_database():
    """Update database.


    """

    start = dt.datetime.now()
    currencies = list_currencies()
    for cur in currencies:
        print("Updating {}...".format(cur["title"]))
        if read_stream(cur) == []:
            callback = collect(cur)
        while not (callback(cur)):
            # 200 unregistered requests and 400 registered requests are allowed
            # per hour.
            start += dt.timedelta(hours=1)
            print("Sleeping until {}...".format(start))
            time.sleep((start - dt.datetime.now()).seconds)
    # print("Making timeline...")
    # pre.make_timeline()


update_database()
