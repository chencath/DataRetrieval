# downloader script for nyt metadata archive
# see information here: https://archive.nytimes.com/www.nytimes.com/ref/membercenter/nytarchive.html
from NewYorkTime.api_NYT import Retrieval as api_method
import os
import importlib
importlib.reload(api_method)
importlib.reload(NewYorkTime.api_NYT)

# load API key, which can be generated for free here: https://developer.nytimes.com/accounts/create
os.chdir('/Users/cathychen/PycharmProjects/resources')
with open("access_token_NYT.txt", "r") as keyfile:
    api_key = keyfile.readlines()[0]

wk_dir=os.chdir('/Users/cathychen/PycharmProjects/resources/NYT_archive')
wk_dir=os.chdir('/Users/cathychen/PycharmProjects/resources/test')
# access api of new york time news, given api_key and working_dir

api_method.api_retrieval(api_key, start=2019, end=2020, working_dir=wk_dir)

"""  Parse JSON files to dataframe   """
