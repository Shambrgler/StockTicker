import yfinance as yf
#import pandas as pd
#import matplotlib.pyplot as plt
from datetime import datetime
import pickle

stocknametxt = "/home/wayne/Documents/Code/Python/StockTicker/stockstxt.txt"

#amd = yf.Ticker('googl')
#amdInfo = amd.info
#for key,value in amdInfo.items():
#    print(key, ":", value)

#amdPrice = amd.info['regularMarketPrice']
#print(amdPrice)
    
stockList = []
stockInfoDict = {}
with open(stocknametxt) as filename:
    for line in filename:
        stockList.append(line.strip('\n'))
    filename.close()

print(stockList)

def getStockInfo(stocks):
    for i in stocks:
        x = yf.Ticker(i)
        y = x.info
        ydict = {}
        stockInfoDict[i] = ydict
        for key, value in y.items():
            stockInfoDict[i][key] = value

def printStockInfo(stocks):
    for key, value in stockInfoDict.items():
        print("\n\n\nStock Name:", key)
        for x, y in value.items():
            print(x, ":", y)

def dumpStockInfo():
    pickle.dump(stockInfoDict, open('/home/wayne/Documents/Code/Python/StockTicker/stockInfoDict.p', "wb"))

getStockInfo(stockList)
dumpStockInfo()
