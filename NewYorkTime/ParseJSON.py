
import glob
import multiprocessing
import pandas as pd
import nltk
from NewYorkTime.utils import parse_monthly_json
from NewYorkTime.utils import generate_tokens

class PasringJSON:

    def __init__(self, filePath):
        self.__filePath = filePath

    def GetDataFrame(self):
        fileNameSearch = self.__filePath + '/nyt_*'
        fileNames = glob.glob(fileNameSearch)

        output = []
        for fileName in fileNames:
            print(fileName)
            output.append(parse_monthly_json(fileName))
        return(output)







