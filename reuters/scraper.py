import requests
from bs4 import BeautifulSoup as soup
import numpy as np

from reuters_functions import find_sigfigs



class Scraper:
    """Represent a scraper that can scrape Reuters for financial data."""
    def __init__(self, url):
        """Initialize a scraper with a url for scraping."""
        self.url = url
        self.soup = self.get_soup()
        self.companyName = self.get_company_name()
        self.numbersConversionText = self.get_numbers_conversion()
        self.numbersConversion = self._find_number_conversion()
        self.headersList = self.list_of_headers()
        self.columnNames = self.string_of_headers()
        self.numbersArray = self.numbers_to_array() # array of numbers in table
        self.sqlHeaders = self.sql_list_of_headers() # names for sql table

    def get_soup(self):
        """Get soup (raw source code) from source code of webpage."""
        webPage = requests.get(self.url)
        soupData = soup(webPage.text, 'html.parser')
        return soupData
        

    def get_soup_table(self):
        soupTable = self.soup.find('tbody')
        return soupTable


# Class-specific _methods
    def _strip_soup_element(self, textToStrip, seperator="|"):
        """Strip the html from text and insert a seperator between 
        each chunk.
        """
        strippedText = ''
        for data in textToStrip:
            strippedText += data.text.strip() + seperator
        return strippedText

    def _stripped_soup_string_to_list(self, stringForList, seperator="|"):
        """From a list with separators bewteen each chunk, we generate
        a list with each entry being split by the seperator.
        """
        newList = stringForList.split(seperator)
        del newList[-1] # remove the empty item left in place by the separator
        return newList

    def _find_number_conversion(self):
        numberConversion = find_sigfigs(self.numbersConversionText)
        return numberConversion


# Get name of company
    def get_company_name(self):
        """Parse soup for <h1> tag. Pull out the text from it to get 
        the company's name.
        """
        companySoup = self.soup.find('h1')
        companyName = companySoup.text
        return companyName

# Get the chunk of text that says what the values are in, e.g. millions.    
    def get_numbers_conversion(self):
        """Parse soup for the <h3> tag. Then pull back to its parent to 
        get the chunk of text that includes the <span> that shows that 
        the values displayed are in, e.g., Millions.
        """
        h3Chunk = self.soup.find('h3')
        h3ChunkParent = h3Chunk.parent
        chunkWithSpan = h3ChunkParent.find('span')
        numbersConversionText = chunkWithSpan.text
        return numbersConversionText



# Get headers into a list
    def get_soup_headers(self):
        soupHeaders = self.get_soup_table().find_all('th')
        return soupHeaders

    def strip_soup_headers(self):
        strippedHeaders = self._strip_soup_element(self.get_soup_headers())
        return strippedHeaders


    def list_of_headers(self):
        tableHeaders = self._stripped_soup_string_to_list(
            self.strip_soup_headers()
        )
        return tableHeaders

    def string_of_headers(self):
        """Create string of headers matching the column names.  This
        cleans the headers of anything SQL will reject."""
        ss = self.strip_soup_headers()
        ss = ss.replace(' ', '') 
        ss = ss.replace(',', '') 
        ss = ss.replace('-', '') 
        ss = ss.replace('&', '')
        ss = ss.replace('.', '') 
        ss = ss.replace('\'', '') 
        ss = ss.replace('/', '_')
        ss = ss.replace('\\', '') 
        ss = ss.replace('(', 'OR')
        ss = ss.replace(')', '') 
        ss = ss.replace('|', ',') # leave comma separating all column names
        ss = ss[:-1] # Remove comma at the end.
        columnNames = ss
        return columnNames

    def sql_list_of_headers(self):
        """Create string of headers into list, ready for SQL table 
        column names.  This means removing all spaces and
        adding a comma between each column.
        """
        sqlHeaders = self._stripped_soup_string_to_list(self.columnNames, ',')
        return sqlHeaders


    
# Get numbers into a list
    def get_soup_numbers(self):
        soupNumbers = self.get_soup_table().find_all('td')
        return soupNumbers

    def strip_soup_numbers(self):
        strippedNumbers = self._strip_soup_element(self.get_soup_numbers())
        return strippedNumbers

    def clean_soup_numbers(self):
        sn = self.strip_soup_numbers()
        sn = sn.replace('||', '|') 
        sn = sn.replace('--', '0.00')    # turn all "--" entries into 0.00
        # Format negative numbers into regular negative numbers: (99) => -99
        sn = sn.replace('(', '-')   # ( => -
        sn = sn.replace(')', '')    # ) => 
        sn = sn.replace(',', '') 
        sn = sn.replace('.', '') 
        return sn

    def list_of_numbers(self):
        tableStringNumbers = self._stripped_soup_string_to_list(
            self.clean_soup_numbers()
        )
        # Turn list of string-numbers into list of floats
        tableNumbers = list(map(float, tableStringNumbers))
        return tableNumbers

    def numbers_to_array(self):
        numbersArray = np.array(self.list_of_numbers())
        # divide by 100 to have decimal in correct place
        # Then multiply by million to get full number
        numbersArray = (numbersArray / 100) #* 1000000
        # Resize number array to reflect the rows of numbers in the table
        # Make sure table is going back five years
        numYears = 5
        numbersArray = np.resize(
            numbersArray, [len(self.list_of_headers()), numYears]
        )
        return numbersArray

if __name__ == "__main__":
    Scraper()