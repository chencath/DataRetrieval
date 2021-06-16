"""
Description:
 - A simple demo to get RSS feed from Financial Times Journal.

Usage: Executing this whole file in your IDE or from Terminal or executing line by line in iPython.

 Author:
 - Cathy Chen
Last modified date: 3-18-2021
"""

import feedparser
import pandas as pd
import os


# retrieve RSS feedback
content = feedparser.parse("https://www.ft.com/?edition=international&format=rss")

# list all titles
print("\nTitles-------------------------\n")
content.keys()
# dict_keys(['feed', 'entries', 'bozo', 'headers', 'etag', 'href', 'status', 'encoding', 'version', 'namespaces'])
content.entries

titles = []
for item in content.entries:
    titles.append(item['title'])
    print(item['title'])
    ##print("{0}.{1}".format(index, item["title"]))

summarys = []
for item in content.entries:
    print(item)
    if item.has_key('summary'):
        summarys.append(item['summary'])

rst = zip(titles, summarys)
RSS_df = pd.DataFrame(list(rst), columns=['title', 'summary'])


## URL of WSJ RSS feed where you can find news category
url_1="https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
url_2="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml"
content = feedparser.parse(url_2)

# list all titles
dfData_title = pd.DataFrame(columns=['title'])
for index, item in enumerate(content.entries):
    dfData_title = dfData_title.append({'title': item["title"]}, ignore_index=True)
    print("{0}.{1}\n".format(index, item["title"]))

print("\r\nDescriptions-------------------\r\n")
dfData_des = pd.DataFrame(columns=['description'])  # create a dataframe
for index, item in enumerate(content.entries):
    dfData_des = dfData_des.append({'description': item["description"]}, ignore_index=True)
    print("{0}.{1}\n".format(index, item["description"]))
