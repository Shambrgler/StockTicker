from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

options = Options()
options.page_load_strategy = 'eager'
#options.add_argument('--headless')
options.add_argument('--log-level=3')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

PATH = r'c:/Installs/chromedriver/chromedriver.exe'
driver = webdriver.Chrome(PATH, options=options)

stockName = input("Enter Stock Name: ")
stockPage = ("https://www.barchart.com/stocks/quotes/%s/options" % (stockName))

driver.get(stockPage)
html = driver.page_source
df = pd.read_html(html)

print(df[0])
