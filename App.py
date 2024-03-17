import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import datetime

class App():

    def __init__(self, stockTrackingApplication):
        self.stockTrackingApplication = stockTrackingApplication
        self.listingStatusDataFrame = pd.DataFrame()
        self.globalQuotesDataFrame = pd.DataFrame()
        self.symbolList = []

        self.currentGlobalQuoteDataFrame = pd.DataFrame(columns=['symbol', 'current', 'minimum', 'maximum'])

    def run(self):
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
                st.toast('Successfully saved!✅')

        if option == "Home":
            self.home()
        elif option == "Listing Status":
            self.listingStatus()
        elif option == "Global Quotes":
            self.globalQuotes()

    def createTableListingStatus(self):
        self.listingStatusDataFrame = self.stockTrackingApplication.apisManagement.listingStatusDataFrame.copy()
        self.listingStatusDataFrame = self.listingStatusDataFrame.drop("delistingDate", axis = 1)
        self.listingStatusDataFrame = self.listingStatusDataFrame.drop("Unnamed: 0", axis = 1)
        self.listingStatusDataFrame = self.listingStatusDataFrame.rename(columns={'symbol': 'Symbol', 'name': 'Name', 'exchange': 'Exchange', 'assetType': 'Type', 'ipoDate': 'Date', 'status': 'Status'})
    
    def createTableGlobalQuotes(self):
        self.globalQuotesDataFrame = self.stockTrackingApplication.apisManagement.globalQuotesDataFrame.copy()
        self.globalQuotesDataFrame = self.globalQuotesDataFrame.rename(columns={'symbol': 'Symbol', 'current': 'Current Price', 'minimum': 'Minimum Price', 'maximum': 'Maximun Price'})
    
    def home(self):
        st.title("Stock Tracking")
        st.write("Stock Tracking is a simple stock tracking and storage program based on finance API Alpha Vantage.")
        st.header("Alpha Vantage")
        st.write("Alpha Vantage offers a comprehensive suite of APIs and spreadsheets that provide real-time and historical financial market data. Whether you’re looking for information on traditional asset classes like stocks, ETFs, and mutual funds, or you need data on economic indicators, foreign exchange rates, commodities, fundamental data, or technical indicators, Alpha Vantage is your all-in-one solution for enterprise-grade global market data, delivered through user-friendly cloud-based APIs, Excel, and Google Sheets.")
        st.header("API Key")
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
        st.title("Listing Status")
        updateButton = st.button('Update', key = 'update')
        if updateButton:
            toast = self.stockTrackingApplication.apisManagement.getAPIListingStatus()
            if toast == "Successful API request!✅":
                st.toast(toast)
            else:
                st.toast(toast)
                st.toast("The last CSV displayed will be loaded.")
            self.createTableListingStatus()
            st.table(self.listingStatusDataFrame)
        else:
            self.createTableListingStatus()
            st.table(self.listingStatusDataFrame)

    def globalQuotes(self):
        st.title("Global Quotes")
        tab1, tab2 = st.tabs(["Global Quotes Consulted", "Search Global Quote"])
        with tab1:
            st.header("Global Quotes Consulted")
            self.createTableGlobalQuotes()
            if len(self.globalQuotesDataFrame.axes[0]) > 0:
                st.table(self.globalQuotesDataFrame)
            else:
                st.write("There are no existing successful requests.")

        with tab2:
            st.header("Search Global Quote")
            self.symbolList = self.stockTrackingApplication.apisManagement.symbolsDataFrame['symbol'].tolist()
            selectedSymbol = st.selectbox('Symbol', self.symbolList)
            st.caption(selectedSymbol)
            searchButton = st.button('Search', key = 'search', disabled = (selectedSymbol == ""))
            if searchButton:
                self.currentGlobalQuoteDataFrame = self.stockTrackingApplication.apisManagement.getGlobalQuote(selectedSymbol)
                self.currentGlobalQuoteDataFrame = self.currentGlobalQuoteDataFrame.rename(columns={'symbol': 'Symbol', 'current': 'Current Price', 'minimum': 'Minimum Price', 'maximum': 'Maximun Price'})
                if len(self.currentGlobalQuoteDataFrame.axes[0]) > 0:
                    st.subheader(f"{selectedSymbol} Global Quote")
                    st.table(self.currentGlobalQuoteDataFrame)
                    st.toast("Successful API request!✅")
                else:
                    st.toast("❌ Oops... an error occurred. Try again later.")
