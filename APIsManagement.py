import requests

import pandas as pd
from io import StringIO

class APIsManagement():

    def __init__(self):
        self.apiKey = "VJ856XHXT0I8GR7N"
        self.date = "2024-01-01"
        self.symbol = "GOOG"

        self.apiURLGlobalQuotes = ""
        self.apiURLListingStatus = "https://www.alphavantage.co/query?function=LISTING_STATUS"

        self.apiURLGlobalQuotesWithKey = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
        self.apiURLListingStatusWithKey = ""

        self.listingStatusDataFrame = None
        self.symbolsDataFrame = None

    def createURLAPIListingStatus(self):
        self.apiURLListingStatusWithKey = ""
        self.apiURLListingStatusWithKey += f"{self.apiURLListingStatus}&date={self.date}&apikey={self.apiKey}"

    def createURLAPIGlobalQuotes(self):
        self.apiURLGlobalQuotesWithKey = ""
        self.apiURLGlobalQuotesWithKey += f"{self.apiURLGlobalQuotes}&symbol={self.symbol}&apikey={self.apiKey}"

    def getListingStatus(self):
        self.createURLAPIListingStatus()
        self.getAPIListingStatus()

    def getGlobalQuote(self):
        if self.symbol in self.symbolsDataFrame:
            self.createURLAPIGlobalQuotes()
            self.getAPIGlobalQuote()
        else:
            print("Please enter a valid symbol. You can consult the list of symbols.")

    def getAPIListingStatus(self):
        try:
            with requests.Session() as session:

                download = session.get(self.apiURLListingStatusWithKey)
                download.raise_for_status()

                decoded_content = download.content.decode('utf-8')
                
                df = pd.read_csv(StringIO(decoded_content))
                if len(df.axes[0]) > 0 and 'symbol' in df.columns and 'exchange' in df.columns and 'assetType' in df.columns and 'ipoDate' in df.columns and 'delistingDate' in df.columns and 'status' in df.columns:
                    df.to_csv('listing_status.csv', index=True)
                    self.listingStatusDataFrame = df
                    self.symbolsDataFrame = df[["symbol"]]
                else:
                    print("The CSV Listing Status of the indicated date does not comply with the format.")
                    self.readListingStatusCSV()

        except requests.exceptions.HTTPError as http_err:
            print(f'Error HTTP: {http_err}') 
            self.readListingStatusCSV()

        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection Error: {conn_err}')
            self.readListingStatusCSV()

        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout: {timeout_err}')
            self.readListingStatusCSV()

        except requests.exceptions.RequestException as req_err:
            print(f'Request Error: {req_err}')
            self.readListingStatusCSV()

        except Exception as e:
            print(f'An error occurred: {e}')
            self.readListingStatusCSV()
        
    def getAPIGlobalQuote(self):
        pass

    def readListingStatusCSV(self):
        print("The last CSV displayed will be loaded.")
        df = pd.read_csv('listing_status.csv')
        self.listingStatusDataFrame = df
        self.symbolsDataFrame = df[["symbol"]]