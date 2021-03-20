# downloader script for nyt metadata archive
# see information here: https://archive.nytimes.com/www.nytimes.com/ref/membercenter/nytarchive.html
import requests
import json
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os

# define a retry strategy to keep script going if a request fails

# for each year-month, make http request for all article headlines and abstracts that month
def ApiRetrival(api_key, startYear, endYear, working_dir):

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    httpClient = requests.Session()
    httpClient.mount("https://", adapter)
    httpClient.mount("http://", adapter)

    os.chdir(working_dir)

    for year in range(endYear, startYear, -1):
        for month in range(12, 0, -1):
            print(year, month)

            # http request
            req = httpClient.get(
                "https://api.nytimes.com/svc/archive/v1/{y}/{m}.json?api-key={key}".format(key=api_key, y=year,
                                                                                           m=month))
            # parse raw json
            # write to file
            with open('nyt_{y}_{m}.json'.format(y=year, m=month), 'wb') as outfile:
                outfile.write(req.content)

            # wait 6 seconds to ensure quota of 10 request per minute not breached
            # https://developer.nytimes.com/faq
            time.sleep(6)
