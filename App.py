"""
App Class

This class manages the user interface and application logic for the Stock Tracking application using Streamlit.

Attributes:
    stockTrackingApplication (StockTrackingApplication): Instance of the StockTrackingApplication class for interactions.
    listingStatusDataFrame (pandas.DataFrame): Stores listing status data for display.
    globalQuotesDataFrame (pandas.DataFrame): Stores global quotes data for display.
    symbolList (list): Collection of stock symbols for dropdown selection.
    currentGlobalQuoteDataFrame (pandas.DataFrame): Temporary DataFrame to store current global quote.
"""

# Libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import datetime

class App():

    def __init__(self, stockTrackingApplication):
        """
        Initializes the App instance with necessary attributes and references.

        Args:
            self: The App instance.
            stockTrackingApplication (StockTrackingApplication): Instance of the StockTrackingApplication class.
        """
        self.stockTrackingApplication = stockTrackingApplication

        self.listingStatusDataFrame = pd.DataFrame()
        self.globalQuotesDataFrame = pd.DataFrame()
        self.symbolList = []

        self.currentGlobalQuoteDataFrame = pd.DataFrame(columns=['symbol', 'current', 'minimum', 'maximum'])

    def run(self):
        """
        Runs the application's main logic:

        1. Sets up page configuration with title and icon.
        2. Creates a sidebar for navigation and saving.
        3. Manages navigation between Home, Listing Status, and Global Quotes views.
        4. Handles data retrieval, table creation, and display based on user interactions.

        Args:
            self: The App instance.
        """
        st.set_page_config(
            page_title="Stock Tracking",
            page_icon="💵",
        )

        with st.sidebar:
            option = option_menu(
                menu_title = "Stock Tracking",
                options = ["Home", "Listing Status", "Global Quotes"],
                icons = ["house", "list-columns-reverse", "cash-stack"],
                menu_icon = "cash-coin",
                default_index = 0,
                styles = {}
            )
            saveButton = st.button('Save', key = 'save')
            if saveButton:
                resultListingStatus = self.stockTrackingApplication.db.updateTableListingStatus(self.stockTrackingApplication.apisManagement.listingStatusDataFrame)
                resultGlobalQuotes = self.stockTrackingApplication.db.updateTableGlobalQuotes(self.stockTrackingApplication.apisManagement.globalQuotesDataFrame)
                if resultListingStatus and resultGlobalQuotes:
                    st.toast('Successfully saved!✅')
                elif resultListingStatus:
                    st.toast('Successfully saved!✅')
                    st.toast("❌ Oops... an error occurred while trying to update the Global Quotes Table.")
                elif resultGlobalQuotes:
                    st.toast('Successfully saved!✅')
                    st.toast("❌ Oops... an error occurred while trying to update the Listing Status Table.")
                else:
                    st.toast("❌ Oops... an error occurred while trying to update both tables.")


        if option == "Home":
            self.home()
        elif option == "Listing Status":
            self.listingStatus()
        elif option == "Global Quotes":
            self.globalQuotes()

    def createTableListingStatus(self):
        """
        Creates a DataFrame for displaying listing status data, formatting columns appropriately.

        Args:
            self: The App instance.
        """
        self.listingStatusDataFrame = self.stockTrackingApplication.apisManagement.listingStatusDataFrame.copy()
        self.listingStatusDataFrame = self.listingStatusDataFrame.drop("delistingDate", axis = 1)
        self.listingStatusDataFrame = self.listingStatusDataFrame.drop("Unnamed: 0", axis = 1)
        self.listingStatusDataFrame = self.listingStatusDataFrame.rename(columns={'symbol': 'Symbol', 'name': 'Name', 'exchange': 'Exchange', 'assetType': 'Type', 'ipoDate': 'Date', 'status': 'Status'})
    
    def createTableGlobalQuotes(self):
        """
        Creates a DataFrame for displaying global quotes data, formatting columns appropriately.

        Args:
            self: The App instance.
        """
        self.globalQuotesDataFrame = self.stockTrackingApplication.apisManagement.globalQuotesDataFrame.copy()
        self.globalQuotesDataFrame = self.globalQuotesDataFrame.rename(columns={'symbol': 'Symbol', 'current': 'Current Price', 'minimum': 'Minimum Price', 'maximum': 'Maximum Price'})
    
    def home(self):
        """
        Renders the Home page, providing:

        - Application title: "Stock Tracking"
        - Application description: Explains the purpose of the application and its reliance on Alpha Vantage API.
        - Alpha Vantage information: Describes the capabilities of Alpha Vantage for financial data retrieval.
        - API Key display and update:
            - Shows the current API key stored in `self.stockTrackingApplication.apisManagement.apiKey`.
            - Provides a text input field for users to update the API key.
            - Validates the updated key, requiring at least 12 characters (assuming that's the minimum for Alpha Vantage keys).
            - Updates `self.stockTrackingApplication.apisManagement.apiKey` with the validated key on successful update.
            - Provides appropriate feedback messages (success or error) based on the update attempt.
        - Date input for listing status:
            - Presents a date picker for users to select a date for listing status retrieval.
            - Sets appropriate minimum and maximum date limits.
            - Updates `self.stockTrackingApplication.apisManagement.date` with the chosen date for future API calls (assuming this is stored there).
            - Provides feedback messages upon successful date update.

        Args:
            self: The App instance.
        """
        st.title("Stock Tracking")
        st.write("Stock Tracking is a simple stock tracking and storage program based on finance API Alpha Vantage.")
        st.header("Alpha Vantage")
        st.write("Alpha Vantage offers a comprehensive suite of APIs and spreadsheets that provide real-time and historical financial market data. Whether you’re looking for information on traditional asset classes like stocks, ETFs, and mutual funds, or you need data on economic indicators, foreign exchange rates, commodities, fundamental data, or technical indicators, Alpha Vantage is your all-in-one solution for enterprise-grade global market data, delivered through user-friendly cloud-based APIs, Excel, and Google Sheets.")
        st.header("API Key")
        st.write(self.stockTrackingApplication.apisManagement.apiKey)
        apiKey = st.text_input('API Key', self.stockTrackingApplication.apisManagement.apiKey)
        updateAPIKeyButton = st.button('Update API Key', key = 'update_api_key')
        if updateAPIKeyButton:
            if len(apiKey.replace(" ", "")) >= 12:
                self.stockTrackingApplication.apisManagement.apiKey = apiKey.upper()
                st.write(self.stockTrackingApplication.apisManagement.apiKey)
                st.toast("Successful change✅")
            else:
                st.write(self.stockTrackingApplication.apisManagement.apiKey)
                st.toast("❌ Error, please enter a valid API Key (Minimum 12 characters).")
        else:
            st.write(self.stockTrackingApplication.apisManagement.apiKey)
        st.header("Date (Listing status)")

        today = datetime.datetime.now()
        minDate = datetime.date(2010, 1, 1)
        try:
            maxDate = datetime.date(int(today.year), int(today.month), int(today.day))
        except:
            maxDate = datetime.date(2024, 3, 17)
        
        date = self.stockTrackingApplication.apisManagement.date.split('-')
        try:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        except:
            year = 2024
            month = 1
            day = 1
            st.toast("❌ Oops... an error occurred. Try again later.")

        date = st.date_input("Date", datetime.date(year, month, day), minDate, maxDate)
        st.write(date)
        updateDateButton = st.button('Update', key = 'update_date')
        if updateDateButton:
            year = date.year
            month = date.month if len(str(date.month)) == 2 else f"0{date.month}"
            day = date.day if len(str(date.day)) == 2 else f"0{date.day}"
            self.stockTrackingApplication.apisManagement.date = f"{year}-{month}-{day}"
            st.toast("Successful change✅")

    def listingStatus(self):
        """
        Renders the Listing Status page:

        - Provides a button to update listing status data from the API.
        - Displays retrieved listing status data in a table.

        Args:
            self: The App instance.
        """
        st.title("Listing Status")
        updateButton = st.button('Update', key = 'update')
        if updateButton:
            toast = self.stockTrackingApplication.apisManagement.getListingStatus()
            if toast == "Successful API request!✅":
                st.toast(toast)
            else:
                st.toast(toast)
                st.toast("The Table Listing Status will be loaded.")
            self.createTableListingStatus()
            st.table(self.listingStatusDataFrame)
        else:
            self.createTableListingStatus()
            st.table(self.listingStatusDataFrame)

    def globalQuotes(self):
        """
        Renders the Global Quotes page:

        - Offers a dropdown for selecting a symbol to retrieve global quote data.
        - Displays retrieved global quote data in a table.
        - Shows a history of previously queried global quotes.

        Args:
            self: The App instance.
        """
        st.title("Global Quotes")

        st.header("Search Global Quote")
        self.symbolList = self.stockTrackingApplication.apisManagement.symbolsDataFrame['symbol'].tolist()
        selectedSymbol = st.selectbox('Symbol', self.symbolList)
        st.caption(selectedSymbol)
        searchButton = st.button('Search', key = 'search', disabled = (selectedSymbol == ""))
        if searchButton:
            self.currentGlobalQuoteDataFrame = self.stockTrackingApplication.apisManagement.getGlobalQuote(selectedSymbol)
            self.currentGlobalQuoteDataFrame = self.currentGlobalQuoteDataFrame.rename(columns={'symbol': 'Symbol', 'current': 'Current Price', 'minimum': 'Minimum Price', 'maximum': 'Maximum Price'})
            if len(self.currentGlobalQuoteDataFrame.axes[0]) > 0:
                st.subheader(f"{selectedSymbol} Global Quote")
                st.table(self.currentGlobalQuoteDataFrame)
                st.toast("Successful API request!✅")
                
            else:
                st.toast("❌ Oops... an error occurred. Try again later.")
            st.header("Global Quotes Consulted")
            self.createTableGlobalQuotes()
            if len(self.globalQuotesDataFrame.axes[0]) > 0:
                st.table(self.globalQuotesDataFrame)
            else:
                st.write("There are no existing successful requests.")
        else:
            st.header("Global Quotes Consulted")
            self.createTableGlobalQuotes()
            if len(self.globalQuotesDataFrame.axes[0]) > 0:
                st.table(self.globalQuotesDataFrame)
            else:
                st.write("There are no existing successful requests.")
