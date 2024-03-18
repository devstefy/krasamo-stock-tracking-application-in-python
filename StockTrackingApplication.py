"""
Stock Tracking Application Class

This class provides the core functionality for a stock tracking application. It interacts with various components to manage stock data and user interactions.

Attributes:
    db (Database): An instance of the Database class for database interactions.
    apisManagement (APIsManagement): An instance of the APIsManagement class for managing APIs.
    app (App): An instance of the App class for handling the user interface and application logic.

Methods:
    __init__(self): Initializes the application with database, API management, and app instances.
    createApp(self): Executes the application's main workflow:
        - Reads listing status data from the database using APIsManagement.readListingStatusDB().
        - Reads global quotes data from the database using APIsManagement.readGlobalQuotesDB().
        - Runs the user interface and application logic using app.run().
"""
# Classes
from APIsManagement import *
from Database import *
from App import *
class StockTrackingApplication():

    def __init__(self):
        """
        Initializes the application with database, API management, and app instances.

        Args:
            self: The StockTrackingApplication instance.
        """
        self.db = Database()
        self.apisManagement = APIsManagement(self.db)
        self.app = App(self)

    def createApp(self):
        """
        Executes the application's main workflow:

        1. Reads listing status data from the database using APIsManagement.readListingStatusDB().
        2. Reads global quotes data from the database using APIsManagement.readGlobalQuotesDB().
        3. Runs the user interface and application logic using app.run().

        Args:
            self: The StockTrackingApplication instance.
        """
        self.apisManagement.readListingStatusDB()
        self.apisManagement.readGlobalQuotesDB()
        self.app.run()

    