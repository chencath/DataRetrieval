import requests
import json

class StockTwitsApi:

  """Class for accessing StockTwits API functions.

  Methods:
    login -- Change the token used for login.
    search -- Search for users, symbols, or both.
    stream_symbol -- Download the stream of a symbol.

  For more detail on StockTwits API, see the documentation at
  https://api.stocktwits.com/developers/docs/api
  """

  def __init__(self,token: str):
    self.base = "https://api.stocktwits.com/api/2/" #Base URL of all requests.
    self.token = token

  def search(self, mode=None, **kwargs):
    """Search for users, symbols, or both.

    You should call search with the keyword argument q, where q is the str you
    want to search (e.g. self.search(mode="symbols", q="BTC")).
    mode can have value None, "users" or "symbols". In the first case,
    the API will return a mix of users and symbols."""
    url = self.base + "search{}.json".format("" if mode is None else "/" + mode)
    if self.token != "":
      kwargs.update({"access_token": self.token})
    result = requests.get(url, params=kwargs)
    return(result)

  def stream_symbol(self, symbol):
    """Download the stream of the symbol identified by id.

    The result will contain at most 30 messages.
    Additional arguments such as since and max can be used to select a specific
    time period. See StockTwits documentation for more detail.
    """
    url = self.base + "streams/symbol/{}.json".format(symbol)
    result = requests.get(url)
    return(result)

  # def stream_symbol(self, id, **kwargs):
  #   """Download the stream of the symbol identified by id.
  #
  #   The result will contain at most 30 messages.
  #   Additional arguments such as since and max can be used to select a specific
  #   time period. See StockTwits documentation for more detail.
  #   """
  #   url = self.base + "streams/symbol/{}.json".format(id)
  #   if self.token != "":
  #     kwargs.update({"access_token": self.token})
  #   result = requests.get(url, params=kwargs)
  #   return(result)




