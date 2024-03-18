from APIsManagement import *
from Database import *
from App import *
class StockTrackingApplication():

    def __init__(self):
        self.db = Database()
        self.apisManagement = APIsManagement(self.db)
        self.app = App(self)
        self.stockSymbols = []

    def createApp(self):
        self.apisManagement.readListingStatusDB()
        self.apisManagement.readGlobalQuotesDB()
        self.app.run()

    