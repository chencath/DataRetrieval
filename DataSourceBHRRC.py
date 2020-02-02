""" The Web API provided by Business and Human Rights Resource Center https://www.business-humanrights.org/
"""

import requests
import json
from enum import Enum

class ResponseRateOperators(Enum):
    Greater = '>'
    Less = '<'

class BHRRCApi:
    """Class for accessing StockTwits API functions.

  Methods:
    GetCategories  -- Download categories for detailed retrieval information.
    GetCompany -- Search for users, symbols, or both.
    GetStory -- Download the stories about human rights.

  For more detail on HumanRight API, see the documentation at
  https://www.business-humanrights.org/en/using-our-business-and-human-rights-data-to-bring-about-change
  """

    def __init__(self, key: str, token: str):

        self.baseUri = "https://business-humanrights.org/api/v1/"
        self.api_key = key
        self.api_token = token

        self.headers = {
            "API-KEY": self.api_key,
            "TOKEN": self.api_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def GetCategories(self):
        """Download categories for detailed retrieval information.
    """
        fullUri = self.baseUri + "categories"
        try:
            result = requests.get(fullUri, headers=self.headers)

        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(url, e))
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

    def GetCompanies(self, page, responseRate, responseRateOperator: ResponseRateOperators, languageCode ="en", ):
        fullUri = ('{baseUri}companies'.format(baseUri=self.baseUri))
        getParams = {
                        'page': page,
                        'langcode': languageCode,
                        'response_rate': responseRate,
                        'response_rate_operator': responseRateOperator.value
                    }
        try:
            result = requests.get(fullUri, headers=self.headers, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(url, e))
            return None
        return json.loads(result.content)

    def GetStory(self, id, languageCode = "en"):

        fullUri = ('{baseUri}stories/{id}'.format(baseUri=self.baseUri, id=id))
        getParams = { 'langcode': languageCode }

        try:
            result = requests.get(fullUri, headers=self.headers, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(url, e))
            return None
        return json.loads(result.content)

    def GetStories(self, categoryId, languageCode = "en", fullDetails = 1):
        fullUri = ('{baseUri}stories'.format(baseUri=self.baseUri))
        getParams = {
                        'langcode': languageCode,
                        'categories': categoryId,
                        'full_details': fullDetails
                    }
        try:
            result = requests.get(fullUri, headers=self.headers, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(url, e))
            return None
        return json.loads(result.content)


