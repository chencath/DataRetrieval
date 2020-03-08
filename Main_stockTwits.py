

""" The Web API provided by StockTwits https://api.stocktwits.com/developers/docs/api#streams-symbol-docs
Search for symbols or users
1. Get message streams in the form of JSON
2. NLP for messages
3. Create timeline (dataframe)
"""
import importlib
import StockTwitsAPI
importlib.reload(StockTwitsAPI)
import json
import datetime as dt
import time
from StockTwitsAPI import StockTwitsApi    # create module NewsAPI for object class "NewsApi"
import preprocessing as pre             # create preprocessing class for NLP
importlib.reload(pre)


def collect(symbol, access_token):
    """Download cur-related messages that are older than the oldest in database.
      """
    api = StockTwitsApi(access_token)
    stream = api.stream_symbol(symbol=Symbol).json()
    status = stream["response"]["status"]
    with open("stream{}.json".format(symbol), "w", encoding="utf-8") as f:
        json.dump(stream, f)

# def cumcollect(symbol, access_token):
#     api = StockTwitsApi(access_token)
#     n = 0
#     cumStream = []
#     while n < 10:
#         stream = api.stream_symbol(symbol).json()
#         cumStream += stream
#         n += 1
#     with open("cumStream{}.json".format(symbol), "w", encoding="utf-8") as f:
#         json.dump(cumStream, f)


def cumcollect(symbol, access_token):
    """Download cur-related messages that are older than the oldest in database.
          """
    api = StockTwitsApi(access_token)
    n = 0
    while n < 10:
        stream = api.stream_symbol(symbol=Symbol).json()
        with open("cumStream{}.json".format(symbol), "w", encoding="utf-8") as f:
            json.dump(stream, f)
        n += 1


def main():

    with open("access_token_stockTwits.txt", "r") as f:
        access_token = f.read()[:-1]
    start = dt.datetime.now()
    Symbol='IBB'
    collect(symbol=Symbol, access_token=access_token)   # single request
    # cumcollect(symbol=Symbol, access_token=access_token)    # rate of limit: 400 requests
    print("Making timeline...")
    pre.make_timeline(symbol=Symbol)
    # pre.make_cum_timeline(symbol=Symbol)

main()







