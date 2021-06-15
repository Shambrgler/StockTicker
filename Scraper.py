from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

options = Options()
options.page_load_strategy = 'none'
#options.add_argument('--headless')
options.add_argument('--log-level=3')

PATH = r'c:/Installs/chromedriver/chromedriver.exe'
driver = webdriver.Chrome(PATH, options=options)
stocknametxt = r'C:\Users\P44039\Documents\Visual Studio\Python\StockTicker\stocknametxt.txt'
stock = []
with open(stocknametxt) as filename:
    for line in filename:
        stock.append(line.strip('\n'))
    filename.close()

print(stock)


for i in stock:
    stockPage = ("https://finance.yahoo.com/quote/%s/history?p=%s" % (i, i))
    driver.get(stockPage)
    try:
        price = WebDriverWait(driver, 1).until(
            ec.presence_of_element_located((By.XPATH, '//*[@class="W(100%) M(0)"]/tbody/tr[1]/td[2]'))
        )
        driver.execute_script("window.stop();")
        print(i, ':', price.text)
    except:
        print("Could not find stock:", i)

driver.quit()


#/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/table/tbody/tr[1]/td[2]/span


#search = driver.find_element_by_name("q")
#search.send_keys("%s ticker" %(stock))
#search.send_keys(Keys.RETURN)

#print(price)

#time.sleep(5)
#driver.close()