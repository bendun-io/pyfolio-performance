from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class CrossEntry(PortfolioPerformanceObject):

    crossEntryQueue = []

    @staticmethod
    def processCrossEntries():
        while len(CrossEntry.crossEntryQueue) > 0:
            nextEntry = CrossEntry.crossEntryQueue.pop()

            if nextEntry.attrib['class'] == "portfolio-transfer":
                CrossEntry.crossEntry_portfolioTransfer(nextEntry)
            elif nextEntry.attrib['class'] == "buysell":
                CrossEntry.crossEntry_buysell(nextEntry)
            else:
                pass # still open to handle class="account-transfer"
                # print("Cant handle crossEntry class", nextEntry.attrib['class'])

    @staticmethod
    def crossEntry_buysell(nextEntry):
        otherDepot = nextEntry.find("portfolio")
        transaction = nextEntry.find("portfolioTransaction")
        if otherDepot==None or transaction == None:
            return # nothing to be done!
        if "reference" in transaction.attrib:
            return # assumption! this reference is parsed in another case
        
        # Resolve other depot!
        currentNode = resolveXmlReference(otherDepot, otherDepot.attrib['reference'])
        otherName = currentNode.find("name").text
        otherDepot = Depot.getDepotByName(otherName)
        crossTransaction = DepotTransaction.parse(nextEntry, transaction)
        if crossTransaction == None:
            raise RuntimeError("Cannot parse Transaction")
        otherDepot.transactions.append(crossTransaction)

    @staticmethod
    def crossEntry_portfolioTransfer(nextEntry):
        otherDepot = nextEntry.find("portfolioFrom")
        transactionFrom = nextEntry.find("transactionFrom")
        if otherDepot==None or transactionFrom == None:
            return # nothing to be done!

        # Resolve other depot!
        currentNode = resolveXmlReference(otherDepot, otherDepot.attrib['reference'])
        otherName = currentNode.find("name").text
        otherDepot = Depot.getDepotByName(otherName)
        crossTransaction = DepotTransaction.parse(nextEntry, transactionFrom)
        if crossTransaction == None:
            return # TODO Just for the moment
            #raise RuntimeError("Cannot parse Transaction")
        otherDepot.transactions.append(crossTransaction)

from .helpers import *
from .classDepot import *
from .classDepotTransaction import *