from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Account(PortfolioPerformanceObject):
    """
    The class that manages a money account and its transactions.
    """

    def __init__(self, content, reference=None):
        self.transactions = []
        self.uuid = content['uuid'] if 'uuid' in content else None
        self.name = content['name'] if 'name' in content else None
        self.content = content
        self.balance = None
        self.reference = reference
        Portfolio.currentPortfolio.registerPath(content['referencePath'], self)

    def copy_from(self, other):
        self.uuid = other.uuid
        self.name = other.name
        self.reference = other.reference
        self.transactions = other.transactions

    def getBalance(self):
        """
        :return: Balance of the account in cents.
        :type: int
        """
        if self.balance != None:
            return self.balance
        self.balance = 0
        for t in self.transactions:
            self.balance += t.getValue()
        return self.balance

    def getName(self):
        """
        :return: Name of the account.
        :type: str
        """
        return self.name

    def getTransactions(self):
        """
        :return: list of transactions in the account.
        :type: list(Transaction)
        """
        return self.transactions

    @staticmethod
    def parseByXml(content):
        acc = Account(content["uuid"], content["name"])
        # acc.content = content
        transactionRoot = content["transactions"]
        for transact in transactionRoot:
            transactionObject = Transaction.parse(transactionRoot, transact)
            transactionObject.setAccountName(acc.name)
            acc.transactions.append(transactionObject)
        return acc

    # @staticmethod
    # def parseContent(content):
    #     if "@reference" in content.keys():
    #         raise Exception("This method should not be called for Account references")
    #     return Account(content['uuid'], content['name'])

    @staticmethod
    def parse(content):
        if 'referencePath' not in content:
            content['referencePath'] = 'client/accounts/account'
            
        if "@reference" in content.keys():
            return Account(content, content['@reference'])
        
        rslt =  Account(content)
        rslt._parseTransactions(content)
        Portfolio.currentPortfolio.registerUuid(content['uuid'], rslt)
        
        return rslt
    
    def _parseTransactions(self, content):
        num = 1
        for transact in content['transactions']['account-transaction']:
            transact['account'] = self
            
            transact['referencePath'] = content['referencePath'] + '/transactions/account-transaction'
            if num > 1:
                transact['referencePath'] += '[%d]' % num
            transactionObject = Transaction.parse(transact)
            if 'uuid' in transact:
                Portfolio.currentPortfolio.registerUuid(transact['uuid'], transactionObject)
            self.transactions.append(transactionObject)
            num += 1
    
    def resolveReference(self):
        super().resolveReference()
        
        for transaction in self.transactions:
            transaction.resolveReference()


    def __repr__(self) -> str:
        """
        Computes and returns the string representation of the object.
        Format 'Account/NAME: BALANCE'.

        :return: String representation of the account.
        :type: str
        """
        if self.name != None:
            return "Account/%s: %s" % (self.name, self.getBalance())
        return "Account/%s: %d" % (self.reference, self.getBalance())

from .classTransaction import *
from .classPortfolio import *