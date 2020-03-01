""" The Web API provided by NewsAPI https://newsapi.org/
Search worldwide news with code
Get breaking news headlines, and search for articles from over 30,000 news sources and blogs with news API
"""


from NewsAPI import NewsApi    # create module NewsAPI for object class "NewsApi"
import pandas as pd
import os


def CreateDF(JsonArray,columns):
    dfData = pd.DataFrame()

    for item in JsonArray:
        itemStruct = {}

        for cunColumn in columns:
            itemStruct[cunColumn] = item[cunColumn]

        dfData = dfData.append(itemStruct,ignore_index=True)
            # dfData = dfData.append({'id': item['id'], 'name': item['name'], 'description': item['description']},
            #                        ignore_index=True)

    return dfData


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
    columns = [ 'author', 'publishedAt', 'title', 'description','content', 'url']
    df = CreateDF(rst_country['articles'], columns)
    df.to_csv('Headlines_country.csv')

    # get  news for specific symbol
    symbol = 'aapl'
    rst_symbol =api.GetEverything(symbol)
    columns = ['author', 'publishedAt', 'title', 'description', 'content', 'url']
    df = CreateDF(rst_symbol['articles'], columns)
    df.to_csv('Headlines_symbol.csv')



main()
