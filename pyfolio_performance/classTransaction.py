import xml.etree.ElementTree as ElementTree
from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Transaction(PortfolioPerformanceObject):

    negative = ['TRANSFER_OUT', 'REMOVAL', 'INTEREST_CHARGE', 'FEES', 'TAXES', 'BUY']
    positive = ['INTEREST', 'DEPOSIT', 'TRANSFER_IN', 'DIVIDENDS', 'SELL', 'FEES_REFUND']

    sourceMap = {
        'TRANSFER_IN': lambda x: 'Transfer',
        'TRANSFER_OUT': lambda x: 'Transfer',
        'DEPOSIT': lambda x: 'Transfer',
        'REMOVAL': lambda x: 'Type Removal',
        'INTEREST_CHARGE': lambda x: x.getAccountName(),
        'INTEREST': lambda x: x.getAccountName(),
        'TAXES': lambda x: x.getSecurity().getName() if x.getSecurity() != None else 'Tax',
        'FEES': lambda x: x.getSecurity().getName() if x.getSecurity() != None else x.getAccountName(),
        'FEES_REFUND': lambda x: x.getSecurity().getName() if x.getSecurity() != None else x.getAccountName(),
        'DIVIDENDS': lambda x: x.getSecurity().getName(),
        'SELL': lambda x: 'Trading',
        'BUY': lambda x: 'Trading'
    }

    def __init__(self, xml, tType, date):
        self.xml = xml
        self.type = tType
        self.date = DateObject(date)
        self.accountName = None
        
    def __repr__(self) -> str:
        return "Transaction(%s, %s)" % (self.type, str(self.date))

    def setAccountName(self, name):
        self.accountName = name
    
    def getAccountName(self):
        return self.accountName

    # <currencyCode>EUR</currencyCode> // Assuming all is EUR for the moment
    def getValue(self):
        try:
            val = int(self.xml.find("amount").text)
            if self.type in Transaction.negative:
                val = -val
            elif self.type not in Transaction.positive:
                print(self.type, val)
        except AttributeError:
            print(ElementTree.tostring(self.xml, encoding='utf8', method='xml'))
        return val

    def getAmount(self):
        return int(self.xml.find("amount").text)

    def getShares(self):
        return int(self.xml.find("shares").text)

    def getYear(self):
        return self.date.getYear()

    def getMonth(self):
        return self.date.getMonth()

    def getDay(self):
        return self.date.getDay()

    def getSourceName(self):
        if self.type in Transaction.sourceMap:
            return Transaction.sourceMap[self.type](self)
        return self.getSecurity().getName() # dont know the type of transaction

    def getSecurity(self):
        return self.computeSecurity()

    def computeSecurity(self):
        security = self.xml.find("security")
        if security == None:
            return None
        if "reference" not in security.attrib:
            raise RuntimeError("ERROR: Security not as a reference in the transaction!")
        
        currentNode = resolveXmlReference(security, security.attrib["reference"])
        if currentNode == None:
            raise RuntimeError("Cannot find referenced security", security.attrib["reference"])

        return Security.parse(self.xml, currentNode)

    @staticmethod
    def parseByXml(xml):
        tType = None
        tDate = None
        for child in xml:
            if child.tag == "type":
                tType = child.text
            if child.tag == "date":
                tDate = child.text
        if any([tType == None, tDate==None]):
            raise RuntimeError("Cannot parse Transaction", ElementTree.tostring(xml, encoding='utf8', method='xml') )
        
        # is there a crossentry that needs processing?
        crossEntry = xml.find("crossEntry")
        if crossEntry != None and "class" in crossEntry.attrib:
            CrossEntry.crossEntryQueue.append(crossEntry)
        
        return Transaction(xml, tType, tDate)


from .classSecurity import *
from .classCrossEntry import *
from .classDateObject import *
from .helpers import *