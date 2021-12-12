import binance_client as client
from datetime import datetime
import pandas as pd
import requests
import json

class TechStockData:
    def __init__(self, stockSym):
        self.stockSym = stockSym

    def getStockData(self):
        url = "https://alpha-vantage.p.rapidapi.com/query"
        querystring = {"function":"TIME_SERIES_DAILY","symbol":self.stockSym,"outputsize":"compact","datatype":"json"}
        headers = {
            'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
            'x-rapidapi-key': "d31236ababmsh64e96c7f45871b9p14c333jsn3dff867c3ac0"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        df = pd.read_json(response.text).iloc[:,[1]][5:]
        print(df)
        names1 = ['TimeStamp', 'Open', 'Low', 'High', 'Close', 'Volume']
        allData = []
        for index, row in df.iterrows():
            newRow = []
            #print(row.name)
            newRow.append(row.name)
            final_dictionary = eval(str(row[0]))
            print(final_dictionary)
            for v in final_dictionary.values():
                newRow.append(v)
            allData.append(newRow)

        df = pd.DataFrame(allData, columns = names1)
        #print(df)
        return df.head(200)