""" The Web API provided by NASA API https://api.nasa.gov/
step 1: get API key from  https://api.nasa.gov/#signUp
step 2: Browse APIs of Interests

Here we domonstrate Techport
Welcome to TechPort - NASA's resource for collecting and sharing information about NASA-funded technology development.
Techport allows the public to discover the technologies NASA is working on every day to explore space,
understand the universe, and improve aeronautics. NASA is developing technologies in areas such as propulsion,
nanotechnology, robotics, and human health. NASA is committed to making its data available and machine-readable
through an Application Programming Interface (API) to better serve its user communities.
As such, the NASA TechPort system provides a RESTful web services API to make technology project data available in
a machine-readable format. This API can be used to export TechPort data into either an XML or a JSON format,
which can then be further processed and analyzed.


"""
import importlib
import NasaAPI
importlib.reload(NasaAPI)
from NasaAPI import NasaApi
import pandas as pd


def main():
    with open("access_token_Nasa.txt", "r") as f:
        myKey = f.read()[:-1]

    api = NasaApi(myKey)

    # get list of project
    Proj_list= api.Get()
    Proj_DF = pd.DataFrame(Proj_list['projects']['projects'])

    # get detail of specific project
    selectID= Proj_DF['id'][:10]    # select first 10 projects
    mydata = []

    for i, item in enumerate(selectID):
        rst= api.GetProject(item)
        print('making dataframe for {}... ({}/{})'.format(item, i, len(selectID)), end="\r")
        mydata.append({'id': item, 'title': rst['project']['title'], 'description': rst['project']['description'], 'benefits': rst['project']['benefits']})

    NASA_project_DF= pd.DataFrame(mydata, ignore_index='True')
    NASA_project_DF.to_csv("NASA_Project.csv")

main()
