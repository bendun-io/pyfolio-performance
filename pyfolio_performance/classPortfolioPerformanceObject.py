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

    _attributeList = []
    _attributes = {}
    _attribObjectMap = {}

    def _getAttribute(self, name):
        """
        :param name: the name of the attribute
        :type name: str

        :return: the stored value
        :type: arbitrary
        """
        if name in self._attributes.keys():
            return self._attributes[name]
        return None


    def _setAttribute(self, name, value):
        """
        :param name: name of the attribute
        :type name: str

        :param value: value to store
        :type value: arbitrary
        """
        self._attributes[name] = value

        # Connect attribute to the corresponding class map
        if not name in self.__class__._attribObjectMap:
            self.__class__._attribObjectMap[name] = {}
        self.__class__._attribObjectMap[name][value] = self

    def parseAttributes(self):
        for name in self._attributeList:
            txt = self.xml.find(name)
            if txt == None:
                continue
            self._setAttribute(name, txt.text)

    @classmethod
    def getObjectByAttribute(cls, attr, value):
        """
        Note it only works if there is a single object for the attribute and the value.
        For example, we can ask for the attribute `isin` of a security with the value `DE0005190003` leading to BMW.

        :param attr: the attribute we are looknig for
        :type attr: str

        :param value: the value the attribute should have
        :type value: str

        :return: the store object for the value
        :type: object
        """
        if not attr in cls._attribObjectMap:
            return
        attrMap = cls._attribObjectMap[attr]
        if not value in attrMap:
            return
        return attrMap[value]


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
            rslt.parseAttributes()

        cls.parsed[xml] = rslt
        return rslt