from .classTransaction import Transaction


class DepotTransaction(Transaction):

    referenceSkip = 6

    negative = ["DELIVERY_OUTBOUND", "SELL", "TRANSFER_OUT"]
    positive = ["BUY", "DELIVERY_INBOUND", "TRANSFER_IN"]

    def __init__(self, xml, tType, date):
        self.xml = xml
        self.type = tType
        self.date = date

    def getSecurityChange(self):
        val = int(self.xml.find("shares").text)
        if self.type in DepotTransaction.negative:
            val = -val
        elif self.type not in DepotTransaction.positive:
            print(self.type, val)
        return (self.security, val)

    def getSecurity(self):
        return self.security

    def getValue(self):
        return self.getShares() * self.getSecurity().getMostRecentValue()

    @staticmethod
    def parseByXml(xml):
        rslt = Transaction.parseByXml(xml)
        # is there a crossentry that needs processing? -> handled by Transaction.parseByXml(xml)
        rslt = DepotTransaction(rslt.xml, rslt.type, rslt.date)
        rslt.security = rslt.computeSecurity()

        return rslt

    def __repr__(self) -> str:
        return "Depot Transaction about Security %s" % str(self.security)
