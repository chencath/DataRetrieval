""" The Web API provided by Business and Human Rights Resource Center https://www.business-humanrights.org/
"""

import DataSourceBHRRC
from DataSourceBHRRC import ResponseRateOperators

def Main():

    # access_key_HR.txt must contain your personal access key
    with open("access_key_HR.txt", "r") as f:
        myKey = f.read()[:-1]
    # access_token_HR.txt must contain your personal access token
    with open("access_token_HR.txt", "r") as f:
        myToken = f.read()[:-1]

    api = DataSourceBHRRC.BHRRCApi(myKey, myToken)

    #Get Categories
    result = api.GetCategories()
    print(result)

    #Get a company profile
    result = api.GetCompany(80444)
    print(result)

    #Get a story
    result = api.GetStory(id=173345)
    print(result)

    #Get stories
    result = api.GetStories(categoryId=3398)
    print(result)

    #Get Company profiles
    result = api.GetCompanies(page=0, responseRate=50, responseRateOperator=ResponseRateOperators.Greater)
    print(result)



Main()
