from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Security(PortfolioPerformanceObject):
    """
    A class that manages securities.
    """

    referenceSkip = 0
    securityNameMap = {}
    securityIsinMap = {}
    securityWknMap = {}
    mostRecentValue = None
    pricescale = 1000000 # scale factor to reach euro value
    
    def __init__(self, xml): #, name, isin, wkn):
        self._attributeList = ['uuid', 'name', 'currencyCode', 'isin', 'tickerSymbol', 'wkn', 'feed']
        self.xml = xml
        self.name = xml.find("name").text
        # self.isin = isin
        # self.wkn = wkn
        # self.mostRecentValue = None
        # Security.securityNameMap[name] = self
        # if isin != None:
        #     Security.securityIsinMap[isin] = self
        # if wkn != None:
        #     Security.securityWknMap[wkn] = self

    def getMostRecentValue(self):
        """
        :return: Current security price from the file in Euro.
        :type: float
        """
        if self.mostRecentValue != None:
            return self.mostRecentValue
        
        priceList = self.xml.find("prices")
        if priceList == None:
            print("No price list found for %s" % str(self))
            return 0
        newestDate = DateObject("0000-00-00")
        newestXml = None
        for price in priceList:
            priceDate = DateObject(price.attrib['t']) 
            if priceDate.getOrderValue() < newestDate.getOrderValue():
                continue
            newestDate = priceDate
            newestXml = price
        
        self.mostRecentValue = int(newestXml.attrib['v'])/self.pricescale
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
    def parseByXml(xml):
        # name = xml.find("name").text
        # isin = xml.find("isin")
        # if isin != None:
        #     isin = isin.text
        # wkn  = xml.find("wkn")
        # if wkn != None:
        #     wkn = wkn.text
        # secs = Security(xml)
        # secs.parseAttributes()
        return Security(xml) #, name, isin, wkn)

    def __repr__(self) -> str:
        return "Security/%s" % self.getName()

from .classDateObject import *