""" The Web API provided by NewsAPI https://newsapi.org/
Search worldwide news with code
Get breaking news headlines, and search for articles from over 30,000 news sources and blogs with news API
"""


from NewsAPI import NewsApi    # create module NewsAPI for object class "NewsApi"
import pandas as pd
import os
import datetime as dt
from datetime import date


def CreateDF(JsonArray,columns):
    dfData = pd.DataFrame()

    for item in JsonArray:
        itemStruct = {}

        for cunColumn in columns:
            itemStruct[cunColumn] = item[cunColumn]

        # dfData = dfData.append(itemStruct,ignore_index=True)
            # dfData = dfData.append({'id': item['id'], 'name': item['name'], 'description': item['description']},
            #                        ignore_index=True)

    # return dfData
    return itemStruct

def main():
    # access_token_NewsAPI.txt must contain your personal access token
    with open("access_token_NewsAPI.txt", "r") as f:
        myKey = f.read()[:-1]

    api = NewsApi(myKey)

    # get sources of news
    columns = ['id', 'name', 'description']
    rst_source = api.GetSources()
    df = CreateDF(rst_source['sources'], columns)
    df.to_csv('source_list.csv')


    # get news for specific country
    rst_country = api.GetHeadlines()
    columns = ['author', 'publishedAt', 'title', 'description','content', 'url']
    df = CreateDF(rst_country['articles'], columns)
    df.to_csv('Headlines_country.csv')

    # get  news for specific symbol
    symbol = "coronavirus"
    columns = ['author', 'publishedAt', 'title', 'description', 'content']
    limit = 500     # maximum requests per day
    i = 1
    startDate = dt.datetime(2020, 3, 1, 8)
    df = pd.DataFrame({'author': [], 'publishedAt': [], 'title': [], 'description': [], 'content':[]})
    while i < limit:
        endDate = startDate + dt.timedelta(hours=2)
        rst_symbol = api.GetEverything(symbol, 'en', startDate, endDate)
        rst = CreateDF(rst_symbol['articles'], columns)
        df = df.append(rst, ignore_index=True)
        # DF.join(df.set_index('publishedAt'), on='publishedAt')
        startDate = endDate
        i+=1

    df.to_csv('Headlines_symbol.csv')



main()
