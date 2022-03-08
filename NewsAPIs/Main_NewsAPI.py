""" The Web API provided by NewsAPI https://newsapi.org/
Search worldwide news with code
Get breaking news headlines, and search for articles from over 30,000 news sources and blogs with news API
"""
from NewsAPIs.NewsAPI import NewsApi    # create module NewsAPI for object class "NewsApi"
import pandas as pd
import datetime as dt
import os

def CreateDF(JsonArray,columns):
    dfData = pd.DataFrame()

    for item in JsonArray:
        itemStruct = {}

        for cunColumn in columns:
            itemStruct[cunColumn] = item[cunColumn]

        dfData = dfData.append(itemStruct,ignore_index=True)
    return dfData

def main():
    # access_token_NewsAPI.txt must contain your personal access token
    os.chdir('/Users/cathychen/PycharmProjects/resources')
    with open("access_token_NewsAPI.txt", "r") as f:
        myKey = f.read()[:-1]

    # Parameters for query
    symbol = "Omicron"
    # symbol = "tesla"
    sources = 'bbc.co.uk'
    pageSize = 100
    startDateTime = dt.datetime(2022, 2, 7)
    durationDays = 40

    # end of parameters for query section

    api = NewsApi(myKey)
    endDateTime = startDateTime + dt.timedelta(days=durationDays) - dt.timedelta(seconds=1)
    columns = ['author', 'publishedAt', 'title', 'description', 'content', 'source']
    df = pd.DataFrame({'author': [], 'publishedAt': [], 'title': [], 'description': [], 'content': [], 'source': []})

    while True:
        result = api.GetEverything(symbol, startDateTime, endDateTime, 'en', sources, pageSize, 'publishedAt')
        numOfArticles = len(result['articles'])
        print("got " + str(numOfArticles) + " articles")
        if numOfArticles == 0:
            break

        endDateTime = dt.datetime.strptime(result['articles'][numOfArticles - 1]['publishedAt'], "%Y-%m-%dT%H:%M:%SZ") - dt.timedelta(seconds=1)
        rst = CreateDF(result['articles'], columns)
        df = df.append(rst, ignore_index=True)

    df.to_csv('Headlines_everything.csv')

main()
