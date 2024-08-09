from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Depot(PortfolioPerformanceObject):
    """
    The class that manages a depot and its transactions.
    """

    referenceSkip = 6
    depotMap = {}
    currentDepot = None
    scale = 100000000

    def __init__(self, content, reference=None):
        self.reference = reference
        self.transactions = []
        self.depotSecurities = None 
        self.content = content
        Portfolio.currentPortfolio.registerPath(content['referencePath'], self)
        
        if reference != None:
            return

        self.name = content['name']
        self.uuid = content['uuid']
        Depot.depotMap[self.name] = self
        Portfolio.currentPortfolio.registerUuid(content['uuid'], self)

    def copy_from(self, other):
        other.resolveReference()
        
        self.uuid = other.uuid
        self.name = other.name
        self.depotSecurities = other.depotSecurities 
        self.content = other.content
        self.reference = other.reference
        self.transactions = other.transactions

    def resolveReference(self):
        super().resolveReference()
        
        for transaction in self.transactions:
            transaction.resolveReference()

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
    def parse(content):
        if "@reference" in content.keys():
            return Depot(content, content['@reference'])
        
        rslt = Depot(content)
        rslt._parseTransactions(content)
        
        if 'referenceAccount' in content:
            content['referenceAccount']['referencePath'] = content['referencePath'] + '/referenceAccount'
            Account.parse(content['referenceAccount'])

        return rslt
    
    def _parseTransactions(self, content):
        num = 1
        for transact in content['transactions']['portfolio-transaction']:
            transact['depot'] = self
            if not 'referencePath' in content:
                content['referencePath'] = '../portfolio'
            if num == 1:
                transact['referencePath'] = content['referencePath'] + '/transactions/portfolio-transaction'
            else:
                transact['referencePath'] = content['referencePath'] + '/transactions/portfolio-transaction[%d]' % num
            transact['account'] = None
            transactionObject = Transaction.parse(transact)
            if 'uuid' in transact:
                Portfolio.currentPortfolio.registerUuid(transact['uuid'], transactionObject)
            self.transactions.append(transactionObject)
            num += 1

    def getTransactions(self):
        """
        :return: list of transactions in the depot.
        :type: list(Transaction)
        """
        return self.transactions

    def __repr__(self) -> str:
        return "Depot/%s" % self.name


from .classPortfolio import *
from .classTransaction import *
from .classAccount import *