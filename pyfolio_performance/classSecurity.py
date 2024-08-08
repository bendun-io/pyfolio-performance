from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Security(PortfolioPerformanceObject):
    """
    A class that manages securities.
    """

    referenceSkip = 0
    securityNameMap = {}
    securityIsinMap = {}
    securityWknMap = {}
    securityNums = {}
    mostRecentValue = None
    pricescale = 1000000 # scale factor to reach euro value
    
    def __init__(self, data): #, name, isin, wkn):
        self._attributeList = ['uuid', 'name', 'currencyCode', 'isin', 'tickerSymbol', 'wkn', 'feed']
        self.data = data
        self.name = data["name"]
        self.logo = None
        self.isin = data["isin"] if "isin" in data else None
        self.wkn = data["wkn"] if "wkn" in data else None
        self.mostRecentValue = None
        Security.securityNums[data['num']] = self
        Security.securityNameMap[self.name] = self
        if self.isin != None:
            Security.securityIsinMap[self.isin] = self
        if self.wkn != None:
            Security.securityWknMap[self.wkn] = self

    def getLogo(self):
        """
        :return: Logo of the security
        :type: str
        """
        if self.logo != None:
            return self.logo
        
        try:
            attributes = self.data["attributes"]["map"]["entry"]
            
            for string in attributes["string"]:
                if string == "logo":
                    continue
                self.logo = string
        except: # might have some None in there if no logo exists
            pass
            
        return self.logo

    def getSecurityByNum(num: int) -> 'Security':
        return Security.securityNums[num-1] # -1 because the num starts at 1

    def getMostRecentValue(self):
        """
        :return: Current security price from the file in Euro.
        :type: float
        """
        if self.mostRecentValue != None:
            return self.mostRecentValue
        
        priceList = self.data["prices"]
        if priceList == None:
            print("No price list found for %s" % str(self))
            return 0
        newestDate = DateObject("0000-00-00")
        newestXml = None
        for price in priceList:
            priceDate = DateObject(price['@t'])
            if priceDate.getOrderValue() < newestDate.getOrderValue():
                continue
            newestDate = priceDate
            newestXml = price
        
        if newestXml == None:
            self.mostRecentValue = 0
        else:    
            self.mostRecentValue = int(newestXml['@v'])/self.pricescale
        return self.mostRecentValue

    def getName(self) -> str:
        """
        :return: Name of the security
        :type: str
        """
        # return self._getXmlAttribute('name')
        return self.name

    @staticmethod
    def _getSecurityByMap(map, key):
        if key in map:
            return map[key]
        return None

    @staticmethod
    def getSecurityByName(name):
        """
        :param: Name of security that should be returned.
        :type: str

        :return: existing security object or None 
        :type: Security
        """
        return Security.getObjectByAttribute('name', name)
        # return Security._getSecurityByMap(Security.securityNameMap, name)

    @staticmethod
    def getSecurityByIsin(isin):
        """
        :param: Isin of security that should be returned.
        :type: str

        :return: existing security object or None 
        :type: Security
        """
        return Security.getObjectByAttribute('isin', isin)
        # return Security._getSecurityByMap(Security.securityIsinMap, isin)

    @staticmethod
    def getSecurityByWkn(wkn):
        """
        :param: Wkn of security that should be returned.
        :type: str

        :return: existing security object or None 
        :type: Security
        """
        return Security.getObjectByAttribute('wkn', wkn)
        # return Security._getSecurityByMap(Security.securityWknMap, wkn)

    @staticmethod
    def parseContent(data):
        return Security(data)

    def __repr__(self) -> str:
        return "Security/%s" % self.getName()

from .classDateObject import *