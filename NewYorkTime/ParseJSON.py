
import glob
import multiprocessing
import pandas as pd
import nltk
from NewYorkTime.utils import parse_monthly_json
from NewYorkTime.utils import generate_tokens

class PasringJSON:

    def __init__(self, filePath, start, end):
        self.__filePath = filePath
        self.__start = start
        self.__end = end

    def FindFiles(self):
        fileName = self.__filePath + "nyt_"
        files = [glob.glob( fileName + str(i) + "*.json") for i in range(self.__start, self.__end)]
        files = [item for sublist in files for item in sublist]
        p = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        output = p.map(parse_monthly_json, files)
        return(output)







