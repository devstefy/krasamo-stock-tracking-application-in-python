"""
APIsManagement Class

This class handles interactions with Alpha Vantage APIs and manages data retrieval and storage for listing status and global quotes.

Attributes:
    db (Database): Instance of the Database class for database interactions.
    apiKey (str): Alpha Vantage API key for authentication.
    date (str): Date for listing status retrieval.
    symbol (str): Stock symbol for global quote retrieval.
    apiURLGlobalQuotes (str): Base URL for the GLOBAL_QUOTE API endpoint.
    apiURLListingStatus (str): Base URL for the LISTING_STATUS API endpoint.
    apiURLGlobalQuotesWithKey (str): Complete URL for the GLOBAL_QUOTE API request.
    apiURLListingStatusWithKey (str): Complete URL for the LISTING_STATUS API request.
    listingStatusDataFrame (pandas.DataFrame): DataFrame containing listing status data.
    symbolsDataFrame (pandas.DataFrame): DataFrame containing a list of stock symbols.
    globalQuotesDataFrame (pandas.DataFrame): DataFrame containing global quote data.
"""

# Libraries
import requests
import pandas as pd
from io import StringIO
import datetime

class APIsManagement():

    def __init__(self, db):
        """
        Initializes the APIsManagement instance, setting up attributes for API calls and data management.

        Args:
            db (Database): Instance of the Database class for database interactions.
        """
        self.db = db

        self.apiKey = "VJ856XHXT0I8GR7N"

        try:
            today = datetime.datetime.now()
            year = today.year
            month = today.month if len(str(today.month)) == 2 else f"0{today.month}"
            day = today.day if len(str(today.day)) == 2 else f"0{today.day}"
            self.date = f"{year}-{month}-{day}"
        except:
            self.date = "2024-01-01"

        self.symbol = "GOOG"

        self.apiURLGlobalQuotes = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
        self.apiURLListingStatus = "https://www.alphavantage.co/query?function=LISTING_STATUS"

        self.apiURLGlobalQuotesWithKey = ""
        self.apiURLListingStatusWithKey = ""

        self.listingStatusDataFrame = None
        self.symbolsDataFrame = None
        self.globalQuotesDataFrame = pd.DataFrame(columns=['symbol', 'current', 'minimum', 'maximum'])

    def createURLAPIListingStatus(self):
        """
        Creates the complete URL for the LISTING_STATUS API request, appending the API key and date.
        """
        self.apiURLListingStatusWithKey = ""
        self.apiURLListingStatusWithKey += f"{self.apiURLListingStatus}&date={self.date}&apikey={self.apiKey}"

    def createURLAPIGlobalQuotes(self):
        """
        Creates the complete URL for the GLOBAL_QUOTE API request, appending the API key and symbol.
        """
        self.apiURLGlobalQuotesWithKey = ""
        self.apiURLGlobalQuotesWithKey += f"{self.apiURLGlobalQuotes}&symbol={self.symbol}&apikey={self.apiKey}"

    def getListingStatus(self):
        """
        Retrieves listing status data from Alpha Vantage and updates the listingStatusDataFrame attribute.

        Returns:
            str: Success message or error message based on the API request outcome.
        """
        self.createURLAPIListingStatus()
        return self.getAPIListingStatus()

    def getGlobalQuote(self, symbol : str):
        """
        Retrieves global quote data for a given symbol from Alpha Vantage and updates the globalQuotesDataFrame attribute.

        Args:
            symbol (str): Stock symbol for which to retrieve global quote data.

        Returns:
            pandas.DataFrame: DataFrame containing the retrieved global quote data.
        """
        self.symbol = symbol
        self.createURLAPIGlobalQuotes()
        return self.getAPIGlobalQuote()

    def getAPIListingStatus(self):
        """
        Performs the actual API request to retrieve listing status data using the pre-built URL (`self.apiURLListingStatusWithKey`). 

        - Fetches data using a requests.Session.
        - Parses the downloaded content as a DataFrame.
        - Validates the DataFrame format (ensuring it has expected columns like 'symbol' and 'status').
        - Updates `self.listingStatusDataFrame` and `self.symbolsDataFrame` with the retrieved data on success.
        - Handles potential exceptions related to requests library and falls back to reading data from the database if an error occurs.

        Returns:
            str: Success message ("Successful API request!✅") or error message ("An error has occurred ❌") depending on the outcome.
        """
        try:
            with requests.Session() as session:

                download = session.get(self.apiURLListingStatusWithKey)
                download.raise_for_status()

                decoded_content = download.content.decode('utf-8')
                
                df = pd.read_csv(StringIO(decoded_content))

                if len(df.axes[0]) > 0 and 'symbol' in df.columns and 'exchange' in df.columns and 'assetType' in df.columns and 'ipoDate' in df.columns and 'delistingDate' in df.columns and 'status' in df.columns:
                    #df.to_csv('listing_status.csv', index=True)
                    #self.db.updateTableListingStatus(df)
                    self.listingStatusDataFrame = df
                    self.symbolsDataFrame = df[["symbol"]]
                    return "Successful API request!✅"
                elif len(df.axes[0]) == 0:
                    print("A problem occurred with the API request.")
                    self.readListingStatusDB()
                else:
                    print(f"The CSV Listing Status of the date {self.date} does not comply with the format.")
                    self.readListingStatusDB()

        except requests.exceptions.HTTPError as http_err:
            print(f'Error HTTP: {http_err}') 
            self.readListingStatusDB()

        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection Error: {conn_err}')
            self.readListingStatusDB()

        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout: {timeout_err}')
            self.readListingStatusDB()

        except requests.exceptions.RequestException as req_err:
            print(f'Request Error: {req_err}')
            self.readListingStatusDB()

        except Exception as e:
            print(f'An error occurred: {e}')
            self.readListingStatusDB()

        return "An error has occurred ❌"
    
    def findKeyByPartialMatch(self, data, partial_key):
        """
        Searches for and returns the value associated with a key that contains a specific substring within a dictionary.

        Args:
            data (dict): The dictionary in which to perform the search.
            partial_key (str): The substring to search for within the dictionary keys.

        Returns:
            The value associated with the found key containing the substring. If no matching key is found, returns None.
        """
        for key in data.keys():
            if partial_key in key:
                return data[key]
        return None
        
    def getAPIGlobalQuote(self):
        """
        Retrieves global quote data for a specific symbol using the pre-built URL (`self.apiURLGlobalQuotesWithKey`).

        - Makes a GET request using requests.get.
        - Checks for a successful response status code (200).
        - Parses the JSON response to extract relevant data (current price, minimum, maximum).
        - Updates `self.globalQuotesDataFrame` with the retrieved data.
        - Creates and returns a DataFrame containing the global quote data.
        - Returns an empty DataFrame if the API request or data parsing fails.

        Args:
            symbol (str): Stock symbol for which to retrieve global quote data.

        Returns:
            pandas.DataFrame: DataFrame containing the retrieved global quote data, or an empty DataFrame if errors occur.
        """
        response = requests.get(self.apiURLGlobalQuotesWithKey)
        dfGlobalQuote = pd.DataFrame(columns=['symbol', 'current', 'minimum', 'maximum'])
        if response.status_code == 200:
            globalQuoteDict = response.json()
            globalQuoteValues = globalQuoteDict.get("Global Quote")
            if globalQuoteValues != None:
                current = self.findKeyByPartialMatch(globalQuoteValues, 'price')
                minimum = self.findKeyByPartialMatch(globalQuoteValues, 'low')
                maximum = self.findKeyByPartialMatch(globalQuoteValues, 'high')
                if current != None and min != None and max != None:
                    self.updateGlobalQuotesDataFrame(self.symbol, current, minimum, maximum)
                    dfGlobalQuote = pd.DataFrame({'symbol': [self.symbol], 'current': [current], 'minimum': [minimum], 'maximum': [maximum]})
                    print(self.globalQuotesDataFrame)
                    return dfGlobalQuote
        return dfGlobalQuote

    def readListingStatusCSV(self):
        """
        Reads listing status data from a CSV file named 'listing_status.csv'.

        - Prints a message indicating the CSV file being loaded.
        - Uses pandas.read_csv to parse the CSV data into a DataFrame.
        - Updates `self.listingStatusDataFrame` and `self.symbolsDataFrame` with the DataFrame containing listing status information.
        """
        print("The last CSV displayed will be loaded.")
        df = pd.read_csv('listing_status.csv')
        self.listingStatusDataFrame = df
        self.symbolsDataFrame = df[["symbol"]]

    def readListingStatusDB(self):
        """
        Reads listing status data from the database using the `db.readListingStatusDB()` method.

        - Prints a message indicating the table 'Listing Status' is being loaded.
        - Calls the `db.readListingStatusDB()` method of the connected database instance (`self.db`) to retrieve the data.
        - Updates `self.listingStatusDataFrame` and `self.symbolsDataFrame` with the DataFrame containing listing status information retrieved from the database.
        """
        print("The Table Listing Status will be loaded.")
        df = self.db.readListingStatusDB()
        self.listingStatusDataFrame = df
        self.symbolsDataFrame = df[["symbol"]]

    def readGlobalQuotesDB(self):
        """
        Reads global quote data from the database using the `db.readGlobalQuotesDB()` method.

        - Prints a message indicating the table 'Global Quotes' is being loaded.
        - Calls the `db.readGlobalQuotesDB()` method of the connected database instance (`self.db`) to retrieve the data.
        - Updates `self.globalQuotesDataFrame` with the DataFrame containing global quote information retrieved from the database.
        """
        print("The Table Global Quotes will be loaded.")
        df = self.db.readGlobalQuotesDB()
        self.globalQuotesDataFrame = df

    def updateGlobalQuotesDataFrame(self, symbol, current, minimum, maximum):
        """
        Updates the `self.globalQuotesDataFrame` with new global quote data for a specific symbol.

        - Checks if the symbol already exists in the DataFrame.
            - If it exists, updates the corresponding rows for 'current', 'minimum', and 'maximum' values.
            - If it doesn't exist, creates a new row with the provided data and concatenates it to the DataFrame.

        Args:
            symbol (str): Stock symbol for which to update global quote data.
            current (str): Current stock price.
            minimum (str): Minimum stock price for the day.
            maximum (str): Maximum stock price for the day.
        """
        if symbol in self.globalQuotesDataFrame['symbol'].values:
            self.globalQuotesDataFrame.loc[self.globalQuotesDataFrame['symbol'] == symbol, ['current', 'minimum', 'maximum']] = [current, minimum, maximum]
        else:
            new_row = pd.DataFrame({'symbol': [symbol], 'current': [current], 'minimum': [minimum], 'maximum': [maximum]})
            self.globalQuotesDataFrame = pd.concat([self.globalQuotesDataFrame, new_row], ignore_index=True)
