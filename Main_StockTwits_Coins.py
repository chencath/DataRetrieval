

""" The Web API provided by StockTwits https://api.stocktwits.com/developers/docs/api#streams-symbol-docs
Retrieve symbol-related messages recursively,
to comply with  rate limit, program needs to sleep until it get accessibility again

"""
import importlib
import StockTwitsAPI
importlib.reload(StockTwitsAPI)
import json
import datetime as dt
import time
import pandas as pd
from StockTwitsAPI import StockTwitsApi    # create module NewsAPI for object class "NewsApi"
import preprocessing as pre             # create preprocessing class for NLP
importlib.reload(pre)



def read_stream(symbol):
  """Return the stream of messages for symbol.
  An empty list is returned if the corresponding JSON file doesn't exist yet.
	"""
  try:
    with open("stream{}.json".format(symbol), "r", encoding="utf-8") as f:
      stream = json.load(f)
    return(stream)
  except FileNotFoundError:
    print("Stream not found for {}.".format(symbol))
    return([])


def collect(symbol, access_token):
    """Download symbol-related messages recursively.
    Due to rate limit, program needs to sleep until it get accessibility again
      """
    stream = read_stream(symbol)
    api = StockTwitsApi(access_token)
    more, success = True, True
    while more:
        newstream = api.stream_symbol(symbol).json()
        status = newstream["response"]["status"]
        if status == 200:  # Success
            if len(newstream["messages"]) > 0:
                stream = newstream["messages"] + stream
                # since = stream[0]["id"]
            else:
                more = False
        elif status == 404:  # Symbol not found
            print(newstream["errors"][0]["message"])
            more = False
        else:  # Other errors from StockTwits
            [print(e["message"]) for e in newstream["errors"]]
            success, more = False, False
    if len(stream) > 0:
        print("Most recent message collected was created on {}.".format(stream[0]["created_at"]))
        with open("stream{}.json".format(symbol), "w", encoding="utf-8") as f:
            json.dump(stream, f)
    return (success)

def main():

    with open("access_token_stockTwits.txt", "r") as f:
        access_token = f.read()[:-1]
    start = dt.datetime.now()
    Symbol='IBB'
    with open("stream{}.json".format(Symbol), "w", encoding="utf-8") as f:
        json.dump([], f)
    while not (collect(symbol=Symbol, access_token=access_token) ):
        start += dt.timedelta(hours=1)
        print("Sleeping until {}...".format(start))
        time.sleep((start - dt.datetime.now()).seconds)


main()







