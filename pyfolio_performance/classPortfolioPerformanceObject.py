class PortfolioPerformanceObject:

    parsed = {}
    referenceSkip = 3

    @classmethod
    def parseByReference(cls, root, reference):
        rslt = None

        for x in root.findall(reference[cls.referenceSkip:]):
            rslt = cls.parse(root, x)
            if rslt != None:
                break

        return rslt

    @classmethod
    def parse(cls, root, xml):
        if xml in cls.parsed:
            return cls.parsed[xml]
        
        rslt = None
        if 'reference' in xml.attrib:
            rslt = cls.parseByReference(root, xml.attrib['reference'])
        else:
            rslt = cls.parseByXml(xml)
        
        cls.parsed[xml] = rslt
        return rslt