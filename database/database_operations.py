import mysql.connector


class DatabaseOperations:
    """DatabaseOperations(host, user, password, database) connects to a 
    database and creates the <self.cursor> object to interact with the 
    database and execute functions on the database.
    """
    def __init__(self, host='localhost', user='root', 
                password='12345', database='testdb'):
        self.mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.cursor = self.mydb.cursor() # object to interact with database

    def _execute_sql_operation(self, sqlFormula, sqlParameters=None):
        """Class-specific _method to execute an sqlFormula and optional
        parameters.  Use sqlParameters when there are values to be 
        inserted into a table.
        """
        self.cursor.execute(sqlFormula, sqlParameters)
        self.mydb.commit()


    def drop_table(self, tableName):
        sqlFormula = "DROP TABLE " + tableName
        self._execute_sql_operation(sqlFormula)

    def drop_database(self, databaseName):
        sqlFormula = "DROP DATABASE " + databaseName
        self._execute_sql_operation(sqlFormula)


    def create_reuters_table(
            self, rowId='row_id', tableName='test_table', ticker='ticker', 
            columnName='column_name', conversionName='conversion_value', 
            statementDate='1900', statementType='statement_type',
            statementPeriod='statement_period', 
            companyName='company_name',
            url='url'
    ):
        sqlFormula = (
            "CREATE TABLE IF NOT EXISTS " 
            + tableName  
            + " (" 
            + rowId + " INT NOT NULL AUTO_INCREMENT UNIQUE, "
            + ticker + " VARCHAR(255), " 
            + columnName + " FLOAT(40), "
            + conversionName + " VARCHAR(255), "
            + statementDate + " VARCHAR(255), "
            + statementType + " VARCHAR(255), "
            + statementPeriod + " VARCHAR(255), "
            + "`timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            + companyName + " VARCHAR(255), "
            + url + " VARCHAR(255)"
            + ")"
        )
        self._execute_sql_operation(sqlFormula)

    def insert_reuters_financial_data(
            self, rowId, tableName, ticker, columnName, conversionName, 
            statementDate, statementType, statementPeriod, companyName,
            url,
            tickerValue, columnValue, conversionValue, statementDateValue,
            statementValue, statementPeriodValue, companyValue, urlValue
    ): 
        sqlFormula = (
            "INSERT IGNORE INTO " 
            + tableName
            + " (" 
            + rowId + ", "
            + ticker + ", " 
            + columnName + ", " 
            + conversionName + ", " 
            + statementDate + ", "
            + statementType + ", "
            + statementPeriod + ", "
            + companyName + ", "
            + url
            + ") "
            + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        sqlParameters = (
            rowId, tickerValue, columnValue, conversionValue, 
            statementDateValue, statementValue, statementPeriodValue, 
            companyValue, urlValue
        ) 
        self._execute_sql_operation(sqlFormula, sqlParameters)

if __name__ == "__main__":
    DatabaseOperations()