
import requests
import json


class NasaApi:
    """Class for accessing News API functions.
  For more detail on NASA API, see the documentation at
  https://api.nasa.gov/
  """

    def __init__(self, key: str):

        self.baseUri = "https://api.nasa.gov/techport/api/projects"
        self.api_key = key


    def Get(self):
        """Get list of projects
    """
        fullUri = self.baseUri
        getParams = {'api_key': self.api_key}
        # getParams['api_key'] = self.api_key
        try:
            result = requests.get(fullUri, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(fullUri, e))
            return None
        return json.loads(result.content)

    def GetProject(self, id):
        """ Get the fist N prjects
    """
        fullUri = self.baseUri + "/{}.json".format(id)
        getParams = {'api_key': self.api_key}
        try:
            result = requests.get(fullUri, params=getParams)
        except Exception as e:
            print("HTTP Request fail {}\r\n{}".format(fullUri, e))
            return None
        return json.loads(result.content)


