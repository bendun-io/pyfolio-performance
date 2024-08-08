import xmltodict

class Portfolio:
    """
    The main class to parse and access different aspects of a portfolio stored in a XML file.

    Uses the XML file created by portfolio performance.

    :param filename: The path of the XML file to parse.
    :type filename: str
    """

    parent_map = {}
    uuid_map = {}
    path_map = {}

    def __init__(self, filename):
        Portfolio.currentPortfolio = self
        xml_content = open(filename, 'r').read()
        self.content = xmltodict.parse(xml_content)

        self._parseSecurities() # needs to be done first, other parsing could depend on it being done 
        self._parseAccounts()
        self._parseDepots()
        CrossEntry.processCrossEntries()
        
        # Ensuring every reference is resolved
        for dep in self.depotList:
            dep.resolveReference()
        for acc in self.accList:
            acc.resolveReference()

    def _parseSecurities(self):
        self.securityList = []
        num = 0
        for sec in self.content['client']['securities']['security']:
            sec['num'] = num
            secObj = Security.parseContent(sec)
            self.uuid_map[sec['uuid']] = secObj
            self.securityList.append(secObj)
            num += 1

    def _parseAccounts(self):
        self.accList = []
        
        num = 1
        refPath = 'client/accounts/account'
        for acc in self.content['client']['accounts']['account']:
            acc['referencePath'] = refPath
            if num > 1:
                acc['referencePath'] += "[%d]" % num
            currentAccount = Account.parse(acc)
            self.accList.append(currentAccount)
            num += 1

        for acc in self.accList:
            acc.resolveReference()

    def _parseDepots(self):
        self.depotList = []
        
        num = 1
        refPath = 'client/portfolios/portfolio'
        for dep in self.content['client']['portfolios']['portfolio']:
            dep['referencePath'] = refPath
            if num > 1:
                dep['referencePath'] += "[%d]" % num
            currentDepot = Depot.parse(dep)
            self.depotList.append(currentDepot)
            num += 1
            
        for dep in self.depotList:
            dep.resolveReference()

    def registerUuid(self, uuid, obj):
        if uuid != None:
            self.uuid_map[uuid] = obj

    def registerPath(self, path, obj):
        if path != None:
            self.path_map[path] = obj

    def getObjectByPath(self, path):
        if path in self.path_map:
            return self.path_map[path]
        return None

    def getDepots(self):
        """
        Returns the list of Depot objects in the portfolio.

        :return: The extracted Depot list.
        :type: list(Depot)
        """
        return self.depotList


    def getAccounts(self):
        """
        Returns the list of Account objects in the portfolio.

        :return: The extracted Account list.
        :type: list(Account)
        """
        return self.accList

    def getSecurities(self):
        """
        Returns the list of all unique securities in any depot.
        :return: The list.
        :type: list(Security)
        """
        return self.securityList

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

from .classCrossEntry import *
from .classDepot import *
from .classAccount import *
from .helpers import *

from pyfolio_performance.classFilters import Filters