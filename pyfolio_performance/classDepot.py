from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Depot(PortfolioPerformanceObject):

    referenceSkip = 6
    depotMap = {}
    currentDepot = None
    scale = 100000000

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        self.transactions = []
        self.depotSecurities = None 
        Depot.depotMap[name] = self

    def getName(self):
        return self.name

    @staticmethod
    def getDepotByName(name):
        if name in Depot.depotMap.keys():
            return Depot.depotMap[name]

        return Depot(name, None)

    def getSecurities(self):
        if self.depotSecurities != None:
            return self.depotSecurities
        self.depotSecurities = {}
        
        for transaction in self.transactions:
            sec, change = transaction.getSecurityChange()
            if not sec in self.depotSecurities.keys():
                self.depotSecurities[sec] = 0
            self.depotSecurities[sec] += change
        
        keys = [k for k in self.depotSecurities.keys()]
        for k in keys:
            if self.depotSecurities[k] == 0:
                self.depotSecurities.pop(k)
            else:
                self.depotSecurities[k] = self.depotSecurities[k]/Depot.scale
                # Doing this scale at the end to get the most accurate result
        
        return self.depotSecurities

    @staticmethod
    def parseByXml(depot):
        name = depot.find("name")
        rslt = Depot.getDepotByName(name.text)
        rslt.xml = depot
        Depot.currentDepot = rslt
                
        transactionRoot = depot.find("transactions")
        for transact in transactionRoot:
            theTransaction = DepotTransaction.parse(transactionRoot, transact)
            if theTransaction==None:
                continue
            rslt.transactions.append(theTransaction)

        #rslt.processCrossEntries()

        return rslt
        
    def getTransactions(self):
        return self.transactions

    def __repr__(self):
        return "Depot/%s" % self.name


from .classDepotTransaction import *