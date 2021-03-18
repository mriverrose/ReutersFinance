# Reuters Finance: Scrape, SQL Database, Visualize

## Overview
This project is a demonstration of how we can scrape data from the internet, store the data in a MySQL database, fetch data from the database, work with it as a Pandas `DataFrame`, and visualize our results with Plotly.

We start in the [reuters](https://github.com/mriverrose/ReutersFinance/tree/master/reuters) folder where we define what we are scraping and what to do with the data. Since we are pushing the scraped data to a database, we have defined our database and how we interact with it in the [database](https://github.com/mriverrose/ReutersFinance/tree/master/database) folder. Once we have all the financial data for the NASDAQ-100 companies in our database, we use [`CreateDataframeFromDatabase.ipynb`](https://github.com/mriverrose/ReutersFinance/blob/master/CreateDataframeFromDatabase.ipynb) to convert it into a single `.csv` file for easy Pandas manipulation. Finally, we build a `CalculateRatio` class in the [`CalculateRatio.ipynb`](https://github.com/mriverrose/ReutersFinance/blob/master/CalculateRatio.ipynb) where we analyze our `.csv` and plot some graphs.

## Using the code
### [database](https://github.com/mriverrose/ReutersFinance/tree/master/database)
Select the database credentials in [`database_operations.py`](https://github.com/mriverrose/ReutersFinance/blob/master/database/database_operations.py). Using this module, you can `drop_table()`, and `drop_database()`, for example. If you `drop_database('db_name')`, you can then use [`create_database.py`](https://github.com/mriverrose/ReutersFinance/blob/master/create_database.py) to create a fresh copy of your database. 

### [reuters](https://github.com/mriverrose/ReutersFinance/tree/master/reuters)
- [`scraper.py`](https://github.com/mriverrose/ReutersFinance/blob/master/reuters/scraper.py) is the `Scraper` class where you can decide how the scraper will do its job. 
- [`reuters_functions.py`](https://github.com/mriverrose/ReutersFinance/blob/master/reuters/reuters_functions.py) has the `BuildUrl` class that pieces together the Reuters url we want to scrape. Depending on the ticker, you might need to add a method that changes the RIC code in the url that comes after the ticker. In our case, we are only using NASDAQ-100 tickers which all have a `.O` RIC code.
- [`main.py`](https://github.com/mriverrose/ReutersFinance/blob/master/reuters/main.py) is the script we execute from the command line to generate all our data. This is where you set the list of desired tickers as well as which statements type and period you want to scrape data from. 

### [tables](https://github.com/mriverrose/ReutersFinance/tree/master/tables)
Holds the `.csv` file we generate in [`CreateDataframeFromDatabase.ipynb`](https://github.com/mriverrose/ReutersFinance/blob/master/CreateDataframeFromDatabase.ipynb).

### [CalculateRatio.ipynb](https://github.com/mriverrose/ReutersFinance/blob/master/CalculateRatio.ipynb)
`CalculateRatio` class for easy inputting of numerator and denominator. Use `df.fin_data_name.unique()` to get a list of all the financial data types avaiable for analyzing. 

You may contact me at `mriverrose@gmail.com`.
