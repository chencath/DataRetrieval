# downloader script for nyt metadata archive
# see information here: https://archive.nytimes.com/www.nytimes.com/ref/membercenter/nytarchive.html
import NewYorkTime.api_NYT
import os
import glob
import importlib
import NewYorkTime.utils

importlib.reload(NewYorkTime.api_NYT)

"""  Step 1: API requests and data retrieval    """

# load API key, which can be generated for free here: https://developer.nytimes.com/accounts/create
#os.chdir('/Users/cathychen/PycharmProjects/resources')

#with open("access_token_NYT.txt", "r") as keyfile:
#    api_key = keyfile.readlines()[0]
api_key = 'cA4fWcbrjd8y80iYfYb7o6YjRksa0zl1'

#wk_dir='/Users/cathychen/PycharmProjects/resources/NYT_archive'
wk_dir = 'e:\\temp'
# access api of new york time news, given api_key and working_dir

#NewYorkTime.api_NYT.ApiRetrival(api_key, startYear=2019, endYear=2020, working_dir=wk_dir)

"""  Step 2: Parse JSON files to dataframe   """
from NewYorkTime.ParseJSON import PasringJSON

fileNameSearch = wk_dir + '/nyt_*'
fileNames = glob.glob(fileNameSearch)

result = []
for fileName in fileNames:
    print(fileName)
    result.append(NewYorkTime.utils.parse_monthly_json(fileName))

print(result)
