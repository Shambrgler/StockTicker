from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

options = Options()
options.page_load_strategy = 'eager'
options.add_argument('--headless')
options.add_argument('--log-level=3')

PATH = r'C:\Code\Chrome Driver\chromedriver.exe'
driver = webdriver.Chrome(PATH, options=options)
stocknametxt = '/home/wayne/Documents/Code/Python/StockTicker/stocknametxt.txt'
stock = ['amd','arkk']
stockPrice = {}
balance = 14000 #amount available to trade with
maxStockPrice = balance / 100

def getOptionList(stockName):
    price = float(stockPrice[stockName])
    stockPage = ("https://finance.yahoo.com/quote/%s/options?&p=%s" % (stockName, stockName))
    driver.get(stockPage)
    #strikeList = {}
    maxitmprofit = [0,0,0]
    maxitmstrike = [0,0,0]
    maxotmprofit = 0
    maxotmstrike = 0

    try:
        tabledata = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[1]/div[2]/div/table'))
        )
        rows = tabledata.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                strikeprice = float(row.text.split(' ')[4])
                bidprice = float(row.text.split(' ')[6])
                if (price - 10 < strikeprice < price) and (strikeprice - price + bidprice > 0):
                    profit = (strikeprice - price + bidprice)
                    #for i in range(len(maxitmprofit)):

                    if profit > min(maxitmprofit):
                        i = maxitmprofit.index(min(maxitmprofit))
                        maxitmprofit[i] = profit
                        maxitmstrike[i] = strikeprice
                    #print(maxitmprofit)
                    #print(maxitmstrike)

                elif (price + 10 > strikeprice > price):
                    profit = bidprice
                    if profit > maxotmprofit:
                        maxotmprofit = profit
                        maxotmstrike = strikeprice
                    #strikeList[stockName] = ([strikeprice, float(row.text.split(' ')[5])])
                    #print(strikeList[stockName])
                #if (price - 5 < strikeprice < price + 5) and ((strikeprice) + (float(row.text.split(' ')[5])) < price):
            except:
                #have to have the except because first row is column names, not data
                pass
    except:
        pass
    print("\n\n",stockName,":")
    for i in range(len(maxitmprofit)):
        if maxitmprofit[i] != 0:
            totalitmprofit = (((balance / price) // 100) * maxitmprofit[i]) * 100
            print("Max in the money strike:", maxitmstrike[i], "Profit:", ("{:.2f}".format(totalitmprofit)))
            itmbreakeven = price - maxitmprofit[i]
            print("In the money break even price:", ("{:.2f}".format(itmbreakeven)))

    totalotmprofit = (((balance / price) // 100) * maxotmprofit) * 100
    otmbreakeven = price - maxotmprofit
    print("\nMax out the money strike:", maxotmstrike, "Profit:", ("{:.2f}".format(totalotmprofit)))
    print("Out of the money Break even:", ("{:.2f}".format(otmbreakeven)))
    #return maxitmprofit, maxotmprofit

def getStocks():
    with open(stocknametxt) as filename:
        for line in filename:
            x = line.split()
            stock.append(x[0].strip('\n'))
        filename.close()

def getStockPrice(stock):
    stockPage = ("https://finance.yahoo.com/quote/%s/history?p=%s" % (stock, stock))
    driver.get(stockPage)
    try:
        price = WebDriverWait(driver, 1).until(
            ec.presence_of_element_located((By.XPATH, '//*[@class="W(100%) M(0)"]/tbody/tr[1]/td[5]'))
        )
        driver.execute_script("window.stop();")
        return price.text
        #print(i, ':', price.text)
    except:
        print("Could not find stock:", stock)

def getPriceDict():
    for i in stock:
        stockPage = ("https://finance.yahoo.com/quote/%s/history?p=%s" % (i, i))
        driver.get(stockPage)
        try:
            price = WebDriverWait(driver, 1).until(
                ec.presence_of_element_located((By.XPATH, '//*[@class="W(100%) M(0)"]/tbody/tr[1]/td[5]'))
            )
            #driver.execute_script("window.stop();")
            if float(price.text) < maxStockPrice:
                stockPrice[i] = price.text
        except:
            print("Could not find stock:", i)


#getStocks()
getPriceDict()
for key, value in stockPrice.items():
    print(key, ":", value)

for i in stockPrice.keys():
    getOptionList(i)
driver.quit()

#/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/table/tbody/tr[1]/td[2]/span


#search = driver.find_element_by_name("q")
#search.send_keys("%s ticker" %(stock))
#search.send_keys(Keys.RETURN)

#print(price)

#time.sleep(5)
#driver.close()
