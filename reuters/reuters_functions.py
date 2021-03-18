"""Miscellaneous functions needed throughout."""
from datetime import datetime


def format_reuters_date(date):
    """Format date from Reuters to look like SQL timestamp date."""
    dateObject = datetime.strptime(date, '%d-%b-%y')
    return dateObject.strftime('%Y-%m-%d')


def find_sigfigs(text):
    """Parse through a snippet of text that states what the values are in."""
    text = text.lower()
    if text.find('million') != -1:
        text = 'million'
        return text
    elif text.find('thousand') != -1:
        text = 'thousand'
        return text
    elif text.find('billion') != -1:
        text = 'billion'
        return text
    else:
        text = 'unknown'
        return text


def abbreviate_statement(text):
    """Depending on the type of statement, abbreviate it to two letters
    and add a trailing underscore so it can be used as the first prefix
    of a title for an SQL table.
    """
    if text.find('income-statement') != -1:
        text = 'income statement'
        return text
    elif text.find('balance-sheet') != -1:
        text = 'balance sheet'
        return text
    elif text.find('cash-flow') != -1:
        text = 'cash flow'
        return text
    else:
        text = 'unknown'
        return text


def split_numbers_by_year(npArray, N=0):
    """Given an MxN numpy array, select the column (N) that should be
    isolated.  For Reuters, there are five columns where the most 
    recent year corresponds with 0 and the earliest with 4.  
    """
    splitColumn = npArray[:,N]
    return splitColumn


class BuildUrl:
    """Given three parameters (ticker, statement, period), build a 
    list of urls that will be formatted as:
      'reuters.com/.../<ticker>.O/financials/<statement>...<period>'.
    Note <ticker> is a list while <statement> and <period> are strings.
    """
    def __init__(self, ticker, statement, period):
        self.ticker = ticker
        self.statement = statement
        self.period = period
        
    def _build_ticker_url(self, ticker):
        """Build the first chunk of the Reuters url that includes the 
        ticker.
        """
        tickerUrl = (
            'https://www.reuters.com/companies/' 
            + ticker + '.O/financials/'
        )
        return tickerUrl
    
    def build_urls(self):
        """Build the full Reuters url by tacking on the statement type 
        and the length of the period.
        """
        tickerUrls = []
        for t in self.ticker:
            tickerUrls.append(
                self._build_ticker_url(t) + self.statement + self.period
            )
        return tickerUrls