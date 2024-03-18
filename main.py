# Classes
from StockTrackingApplication import *

def main():
    """
    Entry point for the Stock Tracking Application.

    - Creates an instance of the StockTrackingApplication class.
    - Calls the createApp method on the application instance to initialize and potentially launch the application.

    This function is the starting point for the application's execution.
    """
    stockTrackingApplication = StockTrackingApplication()
    stockTrackingApplication.createApp()

if __name__ == '__main__':
    main()