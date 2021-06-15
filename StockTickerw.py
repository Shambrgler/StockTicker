import pickle
import yfinance as yf
from datetime import date, timedelta

priceDict = {}
stockInfoDict = pickle.load(open("C:/Users/P44039/Documents/Visual Studio/Python/StockTicker/stockInfoDict.p", "rb"))
stocknametxt = r'C:\Users\P44039\Documents\Visual Studio\Python\StockTicker\stocknametxt.txt'
stockList = []

with open(stocknametxt) as filename:
    for line in filename:
        stockList.append(line.strip('\n'))
    filename.close()

print(stockList)

def todayPrice(name):
    pass


def printAllStockInfo():
    for key, value in stockInfoDict.items():
        print("\n\n\nStock Name:", key)
        for x, y in value.items():
            print(x, ":", y)

def createPriceDict():
    for key, values in stockInfoDict.items():
        priceDict[key] = stockInfoDict[key]['regularMarketPrice']


def printStockInfo(stock_name):
    print("\n", "Stock Name:", stock_name, "\n")
    for key, value in stockInfoDict[stock_name].items():
        print(key, ":", value)



class stock:
    def __init__(self, stockInfo):
        self.name = stockInfo['symbol']
        self.regularMarketPrice = stockInfo['regularMarketPrice']
        self.quoteType = stockInfo['quoteType']
        self.shortName = stockInfo['shortName']
        self.sector = stockInfo['sector']

        self.fiftyDayAverage = stockInfo['fiftyDayAverage']
        self.open = stockInfo['open']
        self.previousClose = stockInfo['previousClose']
        self.dayHigh = stockInfo['dayHigh']
        self.dayLow = stockInfo['dayLow']
        self.fiftyTwoWeekLow = stockInfo['fiftyTwoWeekLow']
        self.fiftyTwoWeekHigh = stockInfo['fiftyTwoWeekHigh']
        self.bid = stockInfo['bid']
        self.ask = stockInfo['ask']
        self.priceHistory = {}

        self.volume = stockInfo['volume']
        self.averageVolume10days = stockInfo['averageVolume10days']
        self.marketCap = stockInfo['marketCap']
        self.earningsQuarterlyGrowth = stockInfo['earningsQuarterlyGrowth']

        self.getHistory()

    def printName(self):
        print(self.name)

    def getHistory(self):
        endDate = date.today().strftime('%Y-%m-%d')
        startDate = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        xTicker = yf.Ticker(self.name)
        yHistory = xTicker.history(start=startDate, end=endDate, interval='1d', actions=False)
        yHistory.index = yHistory.index.map(str)
        for i in yHistory.index:
            newIndex = i.split()
            newIndex = newIndex[0]
            yHistory.rename(index={i: newIndex}, inplace=True)
        xHistTemp = yHistory.to_dict()
        #print(yHistory)
        #print(xHistTemp)
        self.priceHistory = xHistTemp['Close']
    
    def printHistory(self):
        print("Stock prices for %s for the Last 30 days" % (self.name.upper()))
        for key, value in self.priceHistory.items():
            print("%s: %s" % (key, '{:.2f}'.format(value)))


#amd = stock(stockInfoDict['amd'])


#amd.printName()
#amd.printHistory()

#amd = stock(stockInfoDict['amd'])

#amd.printHistory()
#print(amd.bid, amd.dayHigh)
