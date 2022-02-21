from .classPortfolioPerformanceObject import PortfolioPerformanceObject

class Security(PortfolioPerformanceObject):
    
    referenceSkip = 0
    securityNameMap = {}
    securityIsinMap = {}
    securityWknMap = {}
    pricescale = 1000000 # scale factor to reach euro value

    def __init__(self, xml, name, isin, wkn):
        self.name = name
        self.xml = xml
        self.isin = isin
        self.wkn = wkn
        self.mostRecentValue = None
        Security.securityNameMap[name] = self
        if isin != None:
            Security.securityIsinMap[isin] = self
        if wkn != None:
            Security.securityWknMap[wkn] = self

    def getMostRecentValue(self):
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

    def getName(self):
        return self.name

    @staticmethod
    def getSecurityByMap(map, key):
        if key in map:
            return map[key]
        return None

    @staticmethod
    def getSecurityByName(name):
        return Security.getSecurityByMap(Security.securityNameMap, name)

    @staticmethod
    def getSecurityByIsin(isin):
        return Security.getSecurityByMap(Security.securityIsinMap, isin)

    @staticmethod
    def getSecurityByWkn(wkn):
        return Security.getSecurityByMap(Security.securityWknMap, wkn)

    @staticmethod
    def parseByXml(xml):
        name = xml.find("name").text
        isin = xml.find("isin")
        if isin != None:
            isin = isin.text
        wkn  = xml.find("wkn")
        if wkn != None:
            wkn = wkn.text
        return Security(xml, name, isin, wkn)

    def __repr__(self) -> str:
        return "Security/%s" % self.name

from .classDateObject import *