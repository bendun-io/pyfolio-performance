class PortfolioPerformanceObject:
    """
    Base class for most objects in the library.
    Offers basic functionality needed, such as:
    - cache of already parsed objects,
    - resolution of objects that are defined by references,
    - general parsing methods.
    """
    parsed = {}
    referenceSkip = 3

    @classmethod
    def parseByReference(cls, root, reference):
        """
        This methods resolves the attribute referenced.
        It returns the parsed result of the referenced xml.

        :param root: Root from where the reference is searched in the XML.
        :type root: xml

        :param reference: Encoding of the reference
        :type reference: str

        :return: Parsed object.
        :type: Subclass of PortfolioPerformanceObject
        """
        rslt = None

        for x in root.findall(reference[cls.referenceSkip:]):
            rslt = cls.parse(root, x)
            if rslt != None:
                break

        return rslt

    @classmethod
    def parse(cls, root, xml):
        """
        This methods parses portfolio performance objects.
        It returns the parsed result of the referenced xml.

        :param root: Root of the parsing, in case it is needed to resolve references.
        :type root: xml

        :param xml: Object to be parsed.
        :type xml: xml

        :return: Parsed object.
        :type: Subclass of PortfolioPerformanceObject
        """
        if xml in cls.parsed:
            return cls.parsed[xml]
        
        rslt = None
        if 'reference' in xml.attrib:
            rslt = cls.parseByReference(root, xml.attrib['reference'])
        else:
            rslt = cls.parseByXml(xml)
        
        cls.parsed[xml] = rslt
        return rslt