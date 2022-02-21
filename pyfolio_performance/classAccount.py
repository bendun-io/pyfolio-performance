from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Account(PortfolioPerformanceObject):

    def __init__(self):
        self.transactions = []
        self.name = None
        self.balance = None

    def getBalance(self):
        if self.balance != None:
            return self.balance
        self.balance = 0
        for t in self.transactions:
            self.balance += t.getValue()
        return self.balance

    def getName(self):
        return self.name

    def getTransactions(self):
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
        if self.name != None:
            return "Account/"+self.name
        return "Account/%s: %d" % (self.reference, self.getBalance())

from .classTransaction import *