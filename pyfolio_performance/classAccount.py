from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Account(PortfolioPerformanceObject):
    """
    The class that manages a money account and its transactions.
    """

    def __init__(self):
        self.transactions = []
        self.name = None
        self.balance = None

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
    def parseByXml(xml):
        acc = Account()
        acc.xml = xml
        acc.name = xml.find("name").text
        transactionRoot = xml.find("transactions")
        for transact in transactionRoot:
            transactionObject = Transaction.parse(transactionRoot, transact)
            transactionObject.setAccountName(acc.name)
            acc.transactions.append(transactionObject)
        return acc

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