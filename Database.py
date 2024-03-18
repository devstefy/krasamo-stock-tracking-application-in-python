import sqlite3
import pandas as pd

class Database():

    def __init__(self):
        self.db = 'stock_tracking.db'
        self.connection = None

    def connectionDB(self):
        self.connection = sqlite3.connect(self.db)
        return self.connection

    def createTableListingStatus(self):
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
        try:
            self.connectionDB()

            DataFrameToDatabase = df.copy()

            DataFrameToDatabase.to_sql('listing_status', self.connection, if_exists = 'replace', index = False)

            self.connection.close()

            return True
        
        except:
            return False

    def readListingStatusDB(self):
        try:
            self.connectionDB()

            df = pd.read_sql_query("SELECT * FROM listing_status", self.connection)

            self.connection.close()

            return df
        
        except:
            return pd.DataFrame(columns=['symbol', 'name', 'exchange', 'assetType', 'ipoDate', 'delistingDate', 'status'])
    
    def createTableGlobalQuotes(self):
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
        try:
            self.connectionDB()

            DataFrameToDatabase = df.copy()

            DataFrameToDatabase.to_sql('global_quotes', self.connection, if_exists = 'replace', index = False)

            self.connection.close()

            return True
        
        except:
            return False
        
    def readGlobalQuotesDB(self):
        try:
            self.connectionDB()

            df = pd.read_sql_query("SELECT * FROM global_quotes", self.connection)

            self.connection.close()

            return df
        
        except:
            return pd.DataFrame(columns=['symbol', 'current', 'minimum', 'maximum'])

    