import xml.etree.ElementTree as ElementTree

class Portfolio:

    parent_map = {}

    def __init__(self, filename):
        self.tree = ElementTree.parse(filename)
        self.root = self.tree.getroot()
        Portfolio.parent_map = {c: p for p in self.tree.iter() for c in p}

        self.accList = self.getAccountsPrep()
        self.depotList = self.getDepotsPrep()
        CrossEntry.processCrossEntries()

    def getDepots(self):
        return self.depotList

    def getDepotsPrep(self):
        depotList = []
        for c in self.root.iter("portfolio"):
            theDepot = Depot.parse(self.root, c)
            if theDepot == None:
                continue
            if not theDepot in depotList: # dont count them twice
                depotList.append(theDepot)
        
        CrossEntry.processCrossEntries() # process them at the end!
        return depotList

    def getAccounts(self):
        return self.accList

    def getAccountsPrep(self):
        accs = None
        for child in self.root:
            if child.tag == "accounts":
                accs = child
                break
        if accs == None:
            raise RuntimeError("No Accounts found!")
        self.accountRoot = accs
        accountList = []
        for account in accs:
            accountList.append(Account.parse(accs, account))
        return accountList

    def getShares(self, theSecurity):
        if theSecurity == None:
            return 0 # if it is not in, we dont have it in the Portfolio
        
        val = 0
        for dep in self.getDepots():
            secVals = dep.getSecurities()
            if theSecurity in secVals:
                val += secVals[theSecurity]
        return val

    def getTotalTransactions(self):
        totalTransactions = []
        for depot in self.getDepots():
            totalTransactions.extend(depot.getTransactions())
        for acc in self.getAccounts():
            totalTransactions.extend(acc.getTransactions())
        return totalTransactions

    def evaluateCluster(self, clusters, fn_filter, fn_getClusterId, fn_aggregation):
        for transact in self.getTotalTransactions():
            if not fn_filter(transact):
                continue
            clusterId = fn_getClusterId(clusters, transact)
            clusters[clusterId] = fn_aggregation(clusters[clusterId], transact)


from .classAccount import *
from .classDepot import *
from .classCrossEntry import *