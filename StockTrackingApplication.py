from App import *
from APIsManagement import *

class StockTrackingApplication():

    def __init__(self):
        self.apisManagement = APIsManagement()
        self.app = App(self)
        self.stockSymbols = []

    def createApp(self):
        self.apisManagement.getListingStatus()
        self.app.run()

    