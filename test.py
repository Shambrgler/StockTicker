import yfinance as yf
from datetime import date, timedelta

endDate = date.today().strftime('%Y-%m-%d')
startDate = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
print(startDate)


amd = yf.Ticker('amd')
amdHistory = amd.history(start=startDate, end=endDate, interval='1d', actions=False)
amdHistory.index = amdHistory.index.map(str)
for i in amdHistory.index:
    x = i.split()
    x = x[0]
    amdHistory.rename(index={i: x}, inplace=True)

#print(amdHistory)



amdPricesDicttmp = amdHistory.to_dict()
print(amdPricesDicttmp['Close'])
amdPrices = amdPricesDicttmp['Close']
del amdPricesDicttmp

#print(amdPrices)
print(amdPrices['2021-06-08'])






amdPricesTmp = amdHistory.values.tolist()
#print(amdPricesTmp)
amdPrices = []
for i in amdPricesTmp:
    amdPrices.append(i[3])


#print(amdPrices)

#print(amdHistory)
