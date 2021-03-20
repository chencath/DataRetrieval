# downloader script for nyt metadata archive
# see information here: https://archive.nytimes.com/www.nytimes.com/ref/membercenter/nytarchive.html

from api_NYT import Retrieval as api_method
import os

# load API key, which can be generated for free here: https://developer.nytimes.com/accounts/create
os.chdir('/Users/cathychen/PycharmProjects/resources')
with open("access_token_NYT.txt", "r") as keyfile:
    api_key = keyfile.readlines()[0]

working_dir)=os.chdir('/Users/cathychen/PycharmProjects/resources/NYT_archive')
api_method.api_retrieval(api_key, start=2020, end=2020, working_dir)
# for each year-month, make http request for all article headlines and abstracts that month
