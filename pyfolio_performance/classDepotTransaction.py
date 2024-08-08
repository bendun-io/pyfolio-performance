from .classTransaction import Transaction

### DEPRECATED WILL BE REMOVED IF EVERYTHING WORKS

class DepotTransaction(Transaction):

    referenceSkip = 6


    def __init__(self, xml, tType, date):
        self.xml = xml
        self.type = tType
        self.date = date

    def getSecurity(self):
        return self.security

    def getValue(self):
        return self.getShares() * self.getSecurity().getMostRecentValue()