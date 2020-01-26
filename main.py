import DataSourceBHRRC
from DataSourceBHRRC import ResponseRateOperators

def Main():

    myKey = 'HgRyj8hRvDdKUSlxEGmlufNKjcog-8ZrtROYCu4aIX4'
    myToken = 'JL9MD4l4pUe3i4hE-eh1nw6rjtDTR2e-FqggRab8pRY'

    api = DataSourceBHRRC.BHRRCApi(myKey, myToken)

    #Get Categories
    #result = api.GetCategories()
    #print(result)

    #Get a company profile
    #result = api.GetCompany(80444)

    #Get a story
    #result = api.GetStory(id=173345)

    #Get stories
    #result = api.GetStories(categoryId=3398)

    #Get Company profiles
    result = api.GetCompanies(page=0, responseRate=50, responseRateOperator=ResponseRateOperators.Greater)
    print(result)



Main()
