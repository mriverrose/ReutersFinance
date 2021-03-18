import mysql.connector

from database.database_operations import DatabaseOperations

# Create the `reuters` database operations object.
dbReuters = DatabaseOperations('localhost', 'root', '12345', 'reuters')

class Database():
    
    def __init__(self):
        """Database class for entering Reuter's information into a database."""

    def enter_reuters_row(self, columnNames, headersList, numbersList, statementDate,
                sqlHeaders, numbersConversion, ticker, statementType, 
                statementPeriod, companyName, url):
        for i in range( len(sqlHeaders) ):
        #for i in range(4): # Keep shorter for testing

            ### New database table will be created (if doesn't exist).
            dbReuters.create_reuters_table('row_id', sqlHeaders[i], 'ticker', 
                sqlHeaders[i], 'conversion_value', 'statement_date',
                'statement_type', 'statement_period', 'company_name', 'url')
            ### End.


            ### Function for determining if the row is already entered.
            def _does_row_exist(tableName, statementDate, ticker, statementPeriod):
                """Check Reuters database to see if row already exists.

                This is achieved by searching for a given statement 
                date for a given ticker.  If there is a match, we 
                return a True value, else we return False."""
                sqlFormula = (
                    "SELECT statement_date='" + statementDate + "'"
                    + " FROM " + tableName 
                    + " WHERE ticker='" + ticker + "'"
                    + " AND statement_period='" + statementPeriod + "'"
                )
                dbReuters.cursor.execute(sqlFormula)
                results = dbReuters.cursor.fetchall()
                temp = []
                # Format list of tuples into integers.
                for t in results: 
                    for s in t:
                        temp.append(s)
                # Sum = 1 implies a match for the date and ticker
                if sum(temp) == 1:  
                    return True
                else:
                    return False
            ### End of function.


            ### Logic to either pass or insert a new database row.
            if _does_row_exist(
                    sqlHeaders[i], statementDate,
                    ticker, statementPeriod
            ):
                pass
            else:
                dbReuters.insert_reuters_financial_data(
                    'row_id', sqlHeaders[i], 'ticker', sqlHeaders[i], 
                    'conversion_value', 'statement_date', 'statement_type', 
                    'statement_period', 'company_name', 'url',
                    ticker, 
                    numbersList[i], numbersConversion, 
                    statementDate, statementType,
                    statementPeriod, companyName, url
                )
            ### End of logic.

if __name__ == "__main__":
    Database()