from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

options = Options()
options.page_load_strategy = 'eager'
#options.add_argument('--headless')
options.add_argument('--log-level=3')

PATH = '/home/wayne/chromedriver/chromedriver'
driver = webdriver.Chrome(PATH, options=options)
stocknametxt = '/home/wayne/Documents/Code/Python/StockTicker/stocknametxt.txt'
stock = []
stockPrice = {}
balance = 14000 #amount available to trade with

def getOptionList(stockName):
    price = float(stockPrice[stockName])
    stockPage = ("https://finance.yahoo.com/quote/%s/options?p=%s" % (stockName, stockName))
    driver.get(stockPage)
    tabledata = WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[1]/div[2]/div/table'))
    )
    rows = tabledata.find_elements(By.TAG_NAME, 'tr')
    strikeList = {}
    maxitmprofit = 0
    maxitmstrike = 0
    maxotmprofit = 0
    maxotmstrike = 0
    for row in rows:
        try:   
            if (price - 10 < float(row.text.split(' ')[4]) < price) and ((float(row.text.split(' ')[4])) - price + (float(row.text.split(' ')[6])) > 0):
                profit = ((float(row.text.split(' ')[4])) - price + (float(row.text.split(' ')[6])))
                if profit > maxitmprofit:
                    maxitmprofit = profit
                    maxitmstrike = (float(row.text.split(' ')[4]))
                #strikeList[stockName] = ([float(row.text.split(' ')[4]), float(row.text.split(' ')[5])])
                #print(strikeList[stockName])

            elif (price + 10 > float(row.text.split(' ')[4]) > price):
                profit = float(row.text.split(' ')[6])
                if profit > maxotmprofit:
                    maxotmprofit = profit
                    maxotmstrike = float(row.text.split(' ')[4])
                #strikeList[stockName] = ([float(row.text.split(' ')[4]), float(row.text.split(' ')[5])])
                #print(strikeList[stockName])
            #if (price - 5 < float(row.text.split(' ')[4]) < price + 5) and ((float(row.text.split(' ')[4])) + (float(row.text.split(' ')[5])) < price):
        except:
            #have to have the except because first row is column names, not data
            pass
    print(stockName,":")
    print("Max in the money strike:", maxitmstrike, "Profit:", maxitmprofit)
    print("Max out the money strike:", maxotmstrike, "Profit:", maxotmprofit)
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
            if float(price.text) < 125.0:
                stockPrice[i] = price.text
        except:
            print("Could not find stock:", i)


getStocks()
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
