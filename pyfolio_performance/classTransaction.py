from .classPortfolioPerformanceObject import PortfolioPerformanceObject
import re

class Transaction(PortfolioPerformanceObject):

    negative = ['TRANSFER_OUT', 'REMOVAL', 'INTEREST_CHARGE', 'FEES', 'TAXES', 'BUY']
    positive = ['INTEREST', 'DEPOSIT', 'TRANSFER_IN', 'DIVIDENDS', 'SELL', 'FEES_REFUND']

    negativeDepot = ["DELIVERY_OUTBOUND", "SELL", "TRANSFER_OUT"]
    positiveDepot = ["BUY", "DELIVERY_INBOUND", "TRANSFER_IN"]

    sourceMap = {
        'TRANSFER_IN': lambda x: 'Transfer',
        'TRANSFER_OUT': lambda x: 'Transfer',
        'DEPOSIT': lambda x: 'Transfer',
        'REMOVAL': lambda x: 'Type Removal',
        'INTEREST_CHARGE': lambda x: x.getAccountName(),
        'INTEREST': lambda x: x.getAccountName(),
        'TAXES': lambda x: x.getSecurity().getName() if x.getSecurity() != None else 'Tax',
        'FEES': lambda x: x.getSecurity().getName() if x.getSecurity() != None else x.getAccountName(),
        'FEES_REFUND': lambda x: x.getSecurity().getName() if x.getSecurity() != None else x.getAccountName(),
        'DIVIDENDS': lambda x: x.getSecurity().getName(),
        'SELL': lambda x: 'Trading',
        'BUY': lambda x: 'Trading'
    }
    
    referenceMap = {}

    def __init__(self, content, reference=None):
        self.reference = reference
        self.security = None
        self.content = content
        
        Transaction.referenceMap[content['referencePath']] = self
        Portfolio.currentPortfolio.registerPath(content['referencePath'], self)
        
        if reference != None:
            return
        
        self._account = content['account'] if 'account' in content else None
        self.type = content['type']
        self.date = DateObject(content['date'])
    
    def copy_from(self, other):
        self.reference = other.reference
        self._account = other._account
        self.type = other.type
        self.date = other.date
        self.content = other.content
    
    def to_dict(self):
        return {"content": self.content, "reference": self.reference}
        
    def __repr__(self) -> str:
        """
        :return: String representation of the transaction of the form Transaction(TYPE, DATE).
        :type: str
        """
        try:
            return "Transaction(%s, %s)" % (self.type, str(self.date))
        except:
            return "Transaction without type or date"

    def setAccount(self, account):
        """
        Setter method for the account name.

        :param name: Name of the account.
        :type name: str
        """
        self._account = account
    
    def getAccountName(self):
        """
        Getter method for the account name.

        :return: Name of the account.
        :type: str
        """
        return self._account.name

    def getValue(self):
        try:
            val = int(self.content["amount"])
            if self.type in Transaction.negative:
                val = -val
            elif self.type not in Transaction.positive:
                val = self.getSecurityBasedValue()
        except AttributeError:
            print(self.content)
        return val

    def getSecurityBasedValue(self):
        if self.type not in Transaction.positiveDepot and self.type not in Transaction.negativeDepot:
            print(self.type, int(self.content["amount"]))
        return self.getShares() * self.getSecurity().getMostRecentValue()

    def getAmount(self):
        return int(self.content["amount"])

    def getShares(self):
        return int(self.content["shares"])

    def getYear(self):
        """
        Getter method for the year of the underlying date object.

        :return: year of the transaction.
        :type: int
        """
        return self.date.getYear()

    def getMonth(self):
        """
        Getter method for the month of the underlying date object.

        :return: month of the transaction.
        :type: int
        """
        return self.date.getMonth()

    def getDay(self):
        """
        Getter method for the day of the underlying date object.

        :return: day of the transaction.
        :type: int
        """
        return self.date.getDay()

    def getDate(self):
        """
        Return the date object.

        :return: The included date object.
        :type: DateObject
        """
        return self.date

    def getSourceName(self):
        if self.type in Transaction.sourceMap:
            return Transaction.sourceMap[self.type](self)
        return self.getSecurity().getName() # dont know the type of transaction

    def getSecurity(self):
        self.computeSecurity()
        return self.security

    def hasSecurity(self):
        return self.computeSecurity()

    securityPattern = re.compile(r"(\.\./)*securities/security\[(\d+)\]$")
    def computeSecurity(self):
        if self.security != None:
            return True
        
        security = self.content['security']['@reference'] if 'security' in self.content else None
        if security == None:
            return False
        
        match = Transaction.securityPattern.search(security)
        if match:
            self.security = Security.getSecurityByNum(int(match.group(2)))
            return True
        elif security.endswith('securities/security'):
            self.security = Security.getSecurityByNum(1)
            return True

        raise RuntimeError("Security could not be resolved for transaction pattern '%s'" % security)

    def getSecurityChange(self):
        if not self.computeSecurity():
            raise RuntimeError("Security could not be resolved for transaction")
        
        val = int(self.content["shares"])
        if self.type in Transaction.negativeDepot:
            val = -val
        elif self.type not in Transaction.positiveDepot:
            print(self.type, val)
        return (self.security, val)

    #   {
    #     "uuid": "6ff55ee0-f3c7-410c-812b-424ad293ce97",
    #     "date": "2018-01-01T00:00",
    #     "currencyCode": "EUR",
    #     "amount": "899430",
    #     "shares": "0",
    #     "updatedAt": "2021-04-19T13:12:20.101395100Z",
    #     "type": "DEPOSIT"
    #   },
    
    @staticmethod
    def parse(content):
        if "@reference" in content.keys():
            return Transaction(content, content['@reference'])

        transaction = Transaction(content, None)

        # Potential tasks
        ## Resolve "security" reference if field "security" exists
        transaction.computeSecurity()
        
        ## Continue if there is a "crossEntry" in there
        if 'crossEntry' in content:
            content['crossEntry']['referencePath'] = content['referencePath'] + '/crossEntry'
            CrossEntry.parse(content['crossEntry'])
        
        return transaction

from .classSecurity import *
from .classCrossEntry import *
from .classDateObject import *
from .classPortfolio import *
from .helpers import *