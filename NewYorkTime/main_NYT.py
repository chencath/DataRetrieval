# Retrieve news articles from New York Times News Archive API
# """  Step 1: API requests and data retrieval    """
# """  Step 2: Parse JSON files to dataframe   """
# """  Step 3: Slice dataframe   """
# """  Step 4: Basic NLP   """
# see information here: https://archive.nytimes.com/www.nytimes.com/ref/membercenter/nytarchive.html
import NewYorkTime.api_NYT
import os
import glob
import importlib
import NewYorkTime.utils
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import pandas as pd
import re

importlib.reload(NewYorkTime.api_NYT)

"""  Step 1: API requests and data retrieval    """

# load API key, which can be generated for free here: https://developer.nytimes.com/accounts/create
os.chdir('/Users/cathychen/PycharmProjects/resources')

with open("access_token_NYT.txt", "r") as keyfile:
   api_key = keyfile.readlines()[0]

print(api_key)

wk_dir='/Users/cathychen/PycharmProjects/resources/NYT_archive_business'
# access api of new york time news, given api_key and working_dir
NewYorkTime.api_NYT.ApiRetrival(api_key, startYear=2020, endYear=2021, working_dir=wk_dir)

"""  Step 2: Parse JSON files to dataframe   """

fileNameSearch = wk_dir + '/nyt_*'
fileNames = glob.glob(fileNameSearch)

result = []
for fileName in fileNames:
    print(fileName)
    result.append(NewYorkTime.utils.parse_monthly_json(fileName))

print(result)
# combine monthly dataframes, sort articles by publication date, and reset index
df = pd.concat(result)
df.sort_values(by="pub_date", inplace=True)
df.reset_index(drop=True, inplace=True)

df.keys()
# Index(['pub_date', 'headline', 'abstract', 'news_desk', 'section_name'], dtype='object')

"""  Step 3: Slice dataframe   """
# select only certain sections (1.4m out of total of around 3.9m articles)
# list of all sections/desks here: https://developer.nytimes.com/docs/articlesearch-product/1/overview
sections = ["Business Day", "Business"]
# sections = ["World", "U.S.", "Business Day", "Business", "Technology", "Job Market"]
desks = ["Business/Financial Desk", "Business", "Business Day", "Financial", "Outlook"]
# desks = ["Business/Financial Desk", "Business", "Business Day", "Financial", "Outlook", "Politics"]
# sections = ["World", "U.S.", "Business Day", "Technology"]
# desks = ["Business/Financial Desk", "Business", "Business Day", "Financial Desk"]
print(df.columns)
df = df[df.section_name.isin(sections) | df.news_desk.isin(desks)]

# get rid of weird length abstracts
# 32k articles removed that were outside of +-1 magnitude from median length of ~200 chars/~2-3 sentences
df = df[(df.abstract.str.len() >=20) & (df.abstract.str.len() <2000)]

"""  Step 4: Basic NLP   """
# remove non-ascii characters
# source: https://stackoverflow.com/questions/36340627/remove-non-ascii-characters-from-pandas-column
df.abstract.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)

# remove special characters
df.abstract.replace({r'[^a-zA-z\s]':''}, regex=True, inplace=True)

# remove underscores
df.abstract.replace({r'_':''}, regex=True, inplace=True)

# remove start and end white spaces and make lower case
df.abstract = df.abstract.str.strip().str.lower()

# exclude standard nltk stopwords + defined stopwords + single letters
stop = nltk.corpus.stopwords.words("english")
print(stop)
df['abstract'] = df['abstract'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
os.chdir('/Users/cathychen/PycharmProjects/resources')
df.to_csv('NYT_business.csv')

