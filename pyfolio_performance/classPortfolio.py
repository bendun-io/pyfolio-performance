from .classCrossEntry import *
from .classDepot import *
from .classAccount import *
import xml.etree.ElementTree as ElementTree

from pyfolio_performance.classFilters import Filters


class Portfolio:
    """
    The main class to parse and access different aspects of a portfolio stored in a XML file.

    Uses the XML file created by portfolio performance.

    :param filename: The path of the XML file to parse.
    :type filename: str
    """

    parent_map = {}

    def __init__(self, filename):
        self.tree = ElementTree.parse(filename)
        self.root = self.tree.getroot()
        Portfolio.parent_map = {c: p for p in self.tree.iter() for c in p}

        self.accList = self._getAccountsPrep()
        self.depotList = self._getDepotsPrep()
        CrossEntry.processCrossEntries()

    def getDepots(self):
        """
        Returns the list of Depot objects in the portfolio.

        :return: The extracted Depot list.
        :type: list(Depot)
        """
        return self.depotList

    def _getDepotsPrep(self):
        depotList = []
        for c in self.root.iter("portfolio"):
            theDepot = Depot.parse(self.root, c)
            if theDepot == None:
                continue
            if not theDepot in depotList:  # dont count them twice
                depotList.append(theDepot)

        CrossEntry.processCrossEntries()  # process them at the end!
        return depotList

    def getAccounts(self):
        """
        Returns the list of Account objects in the portfolio.

        :return: The extracted Account list.
        :type: list(Account)
        """
        return self.accList

    def _getAccountsPrep(self):
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

    def getSecurities(self):
        """
        Returns the list of all unique securities in any depot.
        :return: The list.
        :type: list(Security)
        """
        depotSecurities = []
        for depot in self.getDepots():
            for sec in depot.getSecurities().keys():
                if sec not in depotSecurities:
                    depotSecurities.append(sec)
        return depotSecurities

    def getShares(self, theSecurity):
        """
        Returns the number of shares that the given security objects has in the portfolio overall.

        :param theSecurity: The security queried.
        :type theSecurity: Security

        :return: The number of shares in all depots summed up.
        :type: float
        """
        if theSecurity == None:
            return 0  # if it is not in, we dont have it in the Portfolio

        val = 0
        for dep in self.getDepots():
            secVals = dep.getSecurities()
            if theSecurity in secVals:
                val += secVals[theSecurity]
        return val

    def getTotalTransactions(self):
        """
        Returns the list of all transactions in the portfolio across all depots and accounts.

        :return: The extracted transaction list.
        :type: list(Transaction)
        """
        totalTransactions = []
        for depot in self.getDepots():
            totalTransactions.extend(depot.getTransactions())
        for acc in self.getAccounts():
            totalTransactions.extend(acc.getTransactions())
        return totalTransactions

    def getInvestmentInto(self, security, before=None):
        """
        Computes how much is invested into a specific security before a given date. If no date is given, the total investment is calculated.

        :return: value in cents of investement
        :type: int
        """

        clusters = {'value': 0}
        myFilter = Filters.fSecurityTransaction
        if before != None:
            myFilter = Filters.fAnd(myFilter, Filters)

        def fn_cluster(x, y): return 'value'
        def fn_aggregate(x, y): return x+y.getValue()
        self.evaluateCluster(clusters, myFilter, fn_cluster, fn_aggregate)

        return clusters['value']

    def evaluateCluster(self, clusters, fn_filter, fn_getClusterId, fn_aggregation):
        """
        Evaluates all transactions of the portfolio as follows.
        Every transaction that is successfully filtered by fn_filter, gets put in a cluster through fn_getClusterId.
        The objects in the cluster are aggregated through the fn_aggregation function.

        :parameter clusters: The overall clusters.
        :type clusters: dict(object) / {k->v}

        :parameter fn_filter: Filter function. An entry needs to pass the filter with True to be considered.
        :type fn_filter: function(transaction) -> bool

        :parameter fn_getClusterId: Given the cluster and the transaction, this method gives the key to the cluster the transaction belongs to.
        :type fn_getClusterId: function({k->v}, Transaction) -> k

        :parameter fn_aggregation: The aggregation function that combines cluster values. This updates the cluster itself at the position cluster-id for every considered transaction.
        :type fn_aggregation: function(v, Transaction) -> v

        :return: Nothing is returned.
        :type: None
        """
        for transact in self.getTotalTransactions():
            if not fn_filter(transact):
                continue
            clusterId = fn_getClusterId(clusters, transact)
            clusters[clusterId] = fn_aggregation(clusters[clusterId], transact)
