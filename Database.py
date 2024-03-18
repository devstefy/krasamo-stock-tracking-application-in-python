"""
Database Class

This class handles database interactions for the Stock Tracking application, using SQLite for data storage.

Attributes:
    db (str): Name of the database file ('stock_tracking.db').
    connection (sqlite3.Connection): Connection object for interacting with the database.
"""

# Libraries
import sqlite3
import pandas as pd

class Database():

    def __init__(self):
        """
        Initializes the Database instance, setting the database name and connection to None.

        Args:
            self: The Database instance.

        """
        self.db = 'stock_tracking.db'
        self.connection = None

    def connectionDB(self):
        """
        Establishes a connection to the database and returns the connection object.

        Returns:
            sqlite3.Connection: The connection object.
        """
        self.connection = sqlite3.connect(self.db)
        return self.connection

    def createTableListingStatus(self):
        """
        Creates the 'listing_status' table with columns for stock information.

        Returns:
            bool: True if the table is created successfully, False otherwise.
        """
        try:
            self.connectionDB()

            cur = self.connection.cursor()

            cur.execute('''CREATE TABLE listing_status
                        (symbol text, name text, exchange text, assetType text, ipoDate text, delistingDate text, status text)''')
            
            self.connection.commit()

            self.connection.close()

            return True
        except:
            return False

    def updateTableListingStatus(self, df):
        """
        Updates the 'listing_status' table with the provided DataFrame.

        Args:
            df (pandas.DataFrame): DataFrame containing data to update the table.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        try:
            self.connectionDB()

            DataFrameToDatabase = df.copy()

            DataFrameToDatabase.to_sql('listing_status', self.connection, if_exists = 'replace', index = False)

            self.connection.close()

            return True
        
        except:
            return False

    def readListingStatusDB(self):
        """
        Retrieves data from the 'listing_status' table and returns it as a DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing data from the table.
        """
        try:
            self.connectionDB()

            df = pd.read_sql_query("SELECT * FROM listing_status", self.connection)

            self.connection.close()

            return df
        
        except:
            return pd.DataFrame(columns=['symbol', 'name', 'exchange', 'assetType', 'ipoDate', 'delistingDate', 'status'])
    
    def createTableGlobalQuotes(self):
        """
        Creates the 'global_quotes' table with columns for global quote data.

        Returns:
            bool: True if the table is created successfully, False otherwise.
        """
        try:
            self.connectionDB()

            cur = self.connection.cursor()

            cur.execute('''CREATE TABLE global_quotes
                        (symbol text, current text, minimum text, maximum text)''')
            
            self.connection.commit()

            self.connection.close()

            return True

        except:
            return False

    def updateTableGlobalQuotes(self, df):
        """
        Updates the 'global_quotes' table with the provided DataFrame.

        Args:
            df (pandas.DataFrame): DataFrame containing data to update the table.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        try:
            self.connectionDB()

            DataFrameToDatabase = df.copy()

            DataFrameToDatabase.to_sql('global_quotes', self.connection, if_exists = 'replace', index = False)

            self.connection.close()

            return True
        
        except:
            return False
        
    def readGlobalQuotesDB(self):
        """
        Retrieves data from the 'global_quotes' table and returns it as a DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing data from the table.
        """
        try:
            self.connectionDB()

            df = pd.read_sql_query("SELECT * FROM global_quotes", self.connection)

            self.connection.close()

            return df
        
        except:
            return pd.DataFrame(columns=['symbol', 'current', 'minimum', 'maximum'])

    