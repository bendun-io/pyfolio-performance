from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class CrossEntry(PortfolioPerformanceObject):

    crossEntryQueue = []

    @staticmethod
    def processCrossEntries():
        while len(CrossEntry.crossEntryQueue) > 0:
            nextEntry = CrossEntry.crossEntryQueue.pop()

            if nextEntry.content['@class'] == "portfolio-transfer":
                CrossEntry.crossEntry_portfolioTransfer(nextEntry)
            elif nextEntry.content['@class'] == "buysell":
                CrossEntry.crossEntry_buysell(nextEntry)
            else:
                pass # still open to handle class="account-transfer"
                # print("Cant handle crossEntry class", nextEntry.attrib['class'])

    @staticmethod
    def crossEntry_buysell(nextEntry):
        otherDepot = nextEntry.content["portfolio"]
        transaction = nextEntry.content["portfolioTransaction"]
        if otherDepot==None or transaction == None:
            return # nothing to be done!
        if transaction.reference != None:
            return # assumption! this reference is parsed in another case
        
        # Other depot should already be resolved, but resolving is idempontent, lets be sure
        otherDepot.resolveReference()
        transaction.resolveReference()
        otherDepot.transactions.append(transaction)

    @staticmethod
    def crossEntry_portfolioTransfer(nextEntry):
        otherDepot = nextEntry.content["portfolioFrom"]
        transactionFrom = nextEntry.content["transactionFrom"]
        if otherDepot==None or transactionFrom == None:
            return # nothing to be done!

        # Other depot should already be resolved, but resolving is idempontent, lets be sure
        otherDepot.resolveReference()
        transactionFrom.resolveReference()
        otherDepot.transactions.append(transactionFrom)


    @staticmethod
    def parse(content):
        if "@reference" in content.keys():
            return None # should not be processed further

        if 'portfolio' in content:
            content['portfolio']['referencePath'] = content['referencePath'] + '/portfolio'
            content['portfolio'] = Depot.parse(content['portfolio'])
        if 'account' in content:
            content['account']['referencePath'] = content['referencePath'] + '/account'
            content['account'] = Account.parse(content['account'])
        if 'accountFrom' in content:
            content['accountFrom']['referencePath'] = content['referencePath'] + '/accountFrom'
            content['accountFrom'] = Account.parse(content['accountFrom'])
        if 'accountTo' in content:
            content['accountTo']['referencePath'] = content['referencePath'] + '/accountTo'
            content['accountTo'] = Account.parse(content['accountTo'])
        if 'portfolioTo' in content:
            content['portfolioTo']['referencePath'] = content['referencePath'] + '/portfolioTo'
            content['portfolioTo'] = Depot.parse(content['portfolioTo'])
        if 'portfolioFrom' in content:
            content['portfolioFrom']['referencePath'] = content['referencePath'] + '/portfolioFrom'
            content['portfolioFrom'] = Depot.parse(content['portfolioFrom'])
            
        if 'accountTransaction' in content:
            content['accountTransaction']['referencePath'] = content['referencePath'] + '/accountTransaction'
            content['accountTransaction']['account'] = content['account']
            content['accountTransaction'] = Transaction.parse(content['accountTransaction'])
        if 'transactionFrom' in content:
            content['transactionFrom']['referencePath'] = content['referencePath'] + '/transactionFrom'
            content['transactionFrom']['account'] = content['accountFrom'] if 'accountFrom' in content else None
            content['transactionFrom'] = Transaction.parse(content['transactionFrom'])
        if 'transactionTo' in content:
            content['transactionTo']['referencePath'] = content['referencePath'] + '/transactionTo'
            content['transactionTo']['account'] = content['accountTo'] if 'accountTo' in content else None
            content['transactionTo'] = Transaction.parse(content['transactionTo'])
        if 'portfolioTransaction' in content:
            content['portfolioTransaction']['referencePath'] = content['referencePath'] + '/portfolioTransaction'
            content['portfolioTransaction'] = Transaction.parse(content['portfolioTransaction'])

        crossEntry = CrossEntry(content)
        CrossEntry.crossEntryQueue.append(crossEntry)
        return crossEntry

    def __init__(self, content):
        self.content = content

from .helpers import *
from .classDepot import *
from .classDepotTransaction import *
from .classAccount import *