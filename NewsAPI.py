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
    GetCategories  -- Download categories for detailed retrieval information.
    GetCompany -- Search for users, symbols, or both.
    GetStory -- Download the stories about human rights.

  For more detail on HumanRight API, see the documentation at
  https://www.business-humanrights.org/en/using-our-business-and-human-rights-data-to-bring-about-change
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



    def GetCompany(self, id, languageCode = "en"):

        fullUri = ('{baseUri}companies/{id}'.format(baseUri=self.baseUri, id=id))
        getParams = { 'langcode': languageCode }

        try:
            result = requests.get(fullUri, headers=self.headers, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(url, e))
            return None
        return json.loads(result.content)

    # def GetCompanies(self, page, responseRate, responseRateOperator: ResponseRateOperators, languageCode ="en", ):
    #     fullUri = ('{baseUri}companies'.format(baseUri=self.baseUri))
    #     getParams = {
    #                     'page': page,
    #                     'langcode': languageCode,
    #                     'response_rate': responseRate,
    #                     'response_rate_operator': responseRateOperator.value
    #                 }
    #     try:
    #         result = requests.get(fullUri, headers=self.headers, params=getParams)
    #     except Exception as e:
    #         print("HTTP Request fail {}\r\n{}".format(url, e))
    #         return None
    #     return json.loads(result.content)
    #
    # def GetStory(self, id, languageCode = "en"):
    #
    #     fullUri = ('{baseUri}stories/{id}'.format(baseUri=self.baseUri, id=id))
    #     getParams = { 'langcode': languageCode }
    #
    #     try:
    #         result = requests.get(fullUri, headers=self.headers, params=getParams)
    #     except Exception as e:
    #         print("HTTP Request fail {}\r\n{}".format(url, e))
    #         return None
    #     return json.loads(result.content)
    #
    # def GetStories(self, categoryId, languageCode = "en", fullDetails = 1):
    #     fullUri = ('{baseUri}stories'.format(baseUri=self.baseUri))
    #     getParams = {
    #                     'langcode': languageCode,
    #                     'categories': categoryId,
    #                     'full_details': fullDetails
    #                 }
    #     try:
    #         result = requests.get(fullUri, headers=self.headers, params=getParams)
    #     except Exception as e:
    #         print("HTTP Request fail {}\r\n{}".format(url, e))
    #         return None
    #     return json.loads(result.content)


