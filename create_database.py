import mysql.connector


"""This module is mostly for testing purposes.  After a database is
filled up, destroy it with the drop_database() function by using the 
DatabaseOperations class.  Once the database is dropped, use this
CreateDatabase class to create a fresh copy.
"""

class CreateDatabase:
	"""Create a MySQL database."""
	def __init__(self, host='localhost', user='root', password='12345'):
		self.mydb = mysql.connector.connect(
				host = host,
				user = user,
				password = password
			)
		self.cursor = self.mydb.cursor() # object to interact with database


	def _execute_sql_operation(self, sqlFormula, sqlParameters=None):
		"""Class-specific _method to execute an sqlFormula"""
		self.cursor.execute(sqlFormula, sqlParameters)
		self.mydb.commit()


	def create_database(self, databaseName):
		sqlFormula = "CREATE DATABASE " + databaseName
		self._execute_sql_operation(sqlFormula)