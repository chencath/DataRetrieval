"""
Description:
 - A simple demo to retrieve CRIX data and plot
Author:
 - Cathy Chen
Last modified date: 3-18-2021
"""

import requests
import json
import pandas as pd

url = 'http://data.thecrix.de/data/crix.json'
r = requests.get(url)

content = r.content
# json.loads : parse a JSON string
js_content = json.loads(content)

for item in js_content:
    print(item)

data_raw = pd.DataFrame(js_content)
data_raw.set_index(keys='date', inplace=True)
data_raw.to_csv('output_crix.csv')


