# v02

import sys
sys.path.append('../')

from database.database import Database

from reuters_functions import (
    BuildUrl,
    split_numbers_by_year,
    abbreviate_statement, 
    format_reuters_date,
)

from scraper import Scraper


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Track execution time for fun.
from datetime import datetime
startTime = datetime.now()
print(f'Starting script now: {startTime}')
"""To set the stage for the Scraper, we need a list of all the tickers
we want to scrape, along with the type of statement and the period of 
time. 
"""
# NASDAQ-100 list of tickers taken from:
# <https://www.nasdaq.com/market-activity/quotes/nasdaq-ndx-index>
NASDAQ100Tickers = ['AAPL','ADBE','ADI','ADP','ADSK','AEP','ALGN','ALXN','AMAT','AMD','AMGN','AMZN','ANSS','ASML','ATVI','AVGO','BIDU','BIIB','BKNG','CDNS','CDW','CERN','CHKP','CHTR','CMCSA','COST','CPRT','CSCO','CSX','CTAS','CTSH','DLTR','DOCU','DXCM','EA','EBAY','EXC','FAST','FB','FISV','FOX','FOXA','GILD','GOOG','GOOGL','IDXX','ILMN','INCY','INTC','INTU','ISRG','JD','KDP','KHC','KLAC','LRCX','LULU','MAR','MCHP','MDLZ','MELI','MNST','MRNA','MRVL','MSFT','MTCH','MU','MXIM','NFLX','NTES','NVDA','NXPI','OKTA','ORLY','PAYX','PCAR','PDD','PEP','PTON','PYPL','QCOM','REGN','ROST','SBUX','SGEN','SIRI','SNPS','SPLK','SWKS','TCOM','TEAM','TMUS','TSLA','TXN','VRSK','VRSN','VRTX','WBA','WDAY','XEL','XLNX','ZM']


# Tickers entered 2020.03.10
# `tickers` needs to be a list for `build_urls()` to execute properly.
tickers = NASDAQ100Tickers 

statement = ['income-statement-', 'balance-sheet-', 'cash-flow-'] 
periods = ['annual', 'quarterly']


# Initialize Selenium connection
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)



# Loop through the periods we are interested in.
for h in range( len(periods) ):
    period = periods[h]

    # Loop through the statements we are interested in.
    for i in range( len(statement) ):
        urls = BuildUrl(tickers, statement[i], period)
        listUrls = urls.build_urls()
        #print(f'URL(s) we are scraping: {listUrls}')
        statementValue = abbreviate_statement(statement[i])
        statementPeriodValue = period

        # Loop through the list of urls we wish to scrape.
        for j in range( len(listUrls) ):
            url = listUrls[j]
            print(f'Scraping url: {url}')

            ### Selenium to fetch the dynamic statement dates. ###
            dateData = []
            driver.get(listUrls[j])
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "time")))
            for match in driver.find_elements_by_tag_name("time"):  
                #print('Statement date: ', match.text)
                dateData.append(match.text)
            ### End Selenium. ###

            ### Get parameters for entering data into database. ###
            S = Scraper(listUrls[j])
            ticker = tickers[j]
            ### End paramenters. ###

            # Loop through each column of data.
            for k in range(len(dateData)-1):
                numbersList = split_numbers_by_year(S.numbersArray, k).tolist()
                statementDate = format_reuters_date(dateData[k+1])

                # Enter parameters into database.
                Database().enter_reuters_row(
                    S.columnNames, S.headersList, numbersList, statementDate,
                    S.sqlHeaders, S.numbersConversion, ticker, statementValue,
                    statementPeriodValue, S.companyName, url
                )

# Close Selenium connection 
driver.close()

runTime = datetime.now() - startTime
print(f'Ending script. Execution time: {runTime}')