from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Depot(PortfolioPerformanceObject):
    """
    The class that manages a depot and its transactions.
    """

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
        """
        :return: Name of the depot.
        :type: str
        """
        return self.name

    @staticmethod
    def getDepotByName(name):
        """
        If no such Depot exists, it returns an empty depot with the name.
        If it exists, it returns the corresponding Depot.

        :param: Name of the depot that should be returned
        :type: str

        :return: Existing or new Depot
        :type: Depot
        """
        if name in Depot.depotMap.keys():
            return Depot.depotMap[name]

        return Depot(name, None)

    def getSecurities(self):
        """
        :return: Mapping of currently Securities to the number of contained shares
        :type: dict(Security -> float)
        """
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
        """
        :return: list of transactions in the depot.
        :type: list(Transaction)
        """
        return self.transactions

    def __repr__(self) -> str:
        return "Depot/%s" % self.name


from .classDepotTransaction import *