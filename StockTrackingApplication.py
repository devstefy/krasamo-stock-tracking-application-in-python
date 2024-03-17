import threading
import time

from APIsManagement import *

class StockTrackingApplication():

    def __init__(self):
        self.apisManagement = APIsManagement()
        self.stockSymbols = []
        """ self.apiThread = threading.Thread(target=self.getAPI())
        self.apiThread.start() """

    def startAPIsManagement(self):
        self.apisManagement.getListingStatus()

    