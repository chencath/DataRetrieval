from NewsAPI import NewsApi
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
    myKey = '3c2638e0b9b14ecd8f7b3bb2e83313c7'

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
