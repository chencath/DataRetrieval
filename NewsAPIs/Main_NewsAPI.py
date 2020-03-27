""" The Web API provided by NewsAPI https://newsapi.org/
Search worldwide news with code
Get breaking news headlines, and search for articles from over 30,000 news sources and blogs with news API
"""
from NewsAPIs.NewsAPI import NewsApi    # create module NewsAPI for object class "NewsApi"
import pandas as pd
import datetime as dt

def CreateDF(JsonArray,columns):
    dfData = pd.DataFrame()

    for item in JsonArray:
        itemStruct = {}

        for cunColumn in columns:
            itemStruct[cunColumn] = item[cunColumn]

        dfData = dfData.append(itemStruct,ignore_index=True)
    #dfData = dfData.append({'id': item['id'], 'name': item['name'], 'description': item['description']},
    #                               ignore_index=True)

    return dfData

def main():
    # access_token_NewsAPI.txt must contain your personal access token
    #with open("access_token_NewsAPI.txt", "r") as f:
    #    myKey = f.read()[:-1]
    # myKey = '08cf4b67d84a47b4b3fc72d7bab9f996'
    myKey = 'b0df47573c1d41c0a6ebefe348693b60'
    api = NewsApi(myKey)

    # get  news for specific symbol (Way 1)
    symbol = "coronavirus"
    sources = ''
    columns = ['author', 'publishedAt', 'title', 'description', 'content', 'source']
    limit = 500     # maximum requests per day

    pageSize = 100
    queryDate = dt.datetime(2020,3,26)

    startDateTime = queryDate
    endDateTime = queryDate + dt.timedelta(days=1)

    columns = ['author', 'publishedAt', 'title', 'description', 'content', 'source']
    df = pd.DataFrame({'author': [], 'publishedAt': [], 'title': [], 'description': [], 'content': [], 'source': []})

    while True:
        result = api.GetEverything(symbol, startDateTime, endDateTime, 'en', sources, pageSize, 'publishedAt')
        numOfArticles = len(result['articles'])
        print(numOfArticles)
        if numOfArticles == 0:
            break

        endDateTime = dt.datetime.strptime(result['articles'][numOfArticles - 1]['publishedAt'], "%Y-%m-%dT%H:%M:%SZ") - dt.timedelta(seconds=1)
        print(result)
        rst = CreateDF(result['articles'], columns)
        df = df.append(rst, ignore_index=True)

    df.to_csv('Headlines_symbol_way2.csv')

main()
