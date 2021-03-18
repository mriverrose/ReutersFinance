# Reuters Finance: Scrape, SQL Database, Visualize

## Overview
This project is a demonstration of how we can scrape data from the internet, store the data in a MySQL database, fetch data from the database, work with it as a Pandas `DataFrame`, and visualize our results with Plotly.

We start in the [reuters](https://github.com/mriverrose/ReutersFinance/tree/master/reuters) folder where we define what we are scraping and what to do with the data. Since we are pushing the scraped data to a database, we have defined our database and how we interact with it in the [database](https://github.com/mriverrose/ReutersFinance/tree/master/database) folder. Once we have all the financial data for the NASDAQ-100 companies in our database, we use [CreateDataframeFromDatabase.ipynb](https://github.com/mriverrose/ReutersFinance/blob/master/CreateDataframeFromDatabase.ipynb) to convert it into a single `.csv` file for easy Pandas manipulation. Finally, we build a `CalculateRatio` class in the [CalculateRatio.ipynb](https://github.com/mriverrose/ReutersFinance/blob/master/CalculateRatio.ipynb) where we analyze our `.csv` and plot some graphs.
