""" The Web API provided by NewsAPI https://newsapi.org/
Search worldwide news with code
Get breaking news headlines, and search for articles from over 30,000 news sources and blogs with our news API
"""

import requests
import json
from enum import Enum


class NewsApi:
    """Class for accessing StockTwits API functions.

  Methods:
    GetResource  -- get the resources of news.
    GetHeadlines -- Download top headlines of specific country.
    GetEverything -- Download top headlines of specific country.

  For more detail on HumanRight API, see the documentation at
  https://newsapi.org/
  """

    def __init__(self, key: str):

        self.baseUri = "https://newsapi.org/v2/"
        self.api_key = key

    def GetSources(self, category = 'business', country = 'us'):
        """Download categories for detailed retrieval information.
    """
        fullUri = self.baseUri + "sources"
        getParams = {'country': country, "category": category }
        getParams['apiKey'] = self.api_key
        try:
            result = requests.get(fullUri, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(fullUri, e))
            return None
        return json.loads(result.content)

    def GetHeadlines(self, country = 'us'):
        """Download top headlines of specific country.
    """
        fullUri = self.baseUri + "top-headlines"
        getParams = {'country': country }
        getParams['apiKey'] = self.api_key

        try:
            result = requests.get(fullUri, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(fullUri, e))
            return None
        return json.loads(result.content)

    def GetEverything(self, symbol):
        """Download top headlines of specific country.
    """
        fullUri = self.baseUri + "everything"
        getParams = {'q': symbol }
        getParams['apiKey'] = self.api_key

        try:
            result = requests.get(fullUri, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(fullUri, e))
            return None
        return json.loads(result.content)


