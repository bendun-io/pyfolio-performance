import re

arrayRegex = re.compile(r"\[(\d+)\]$")

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
    def parse(cls, parentNode, data: dict) -> 'PortfolioPerformanceObject':
        """
        This methods parses portfolio performance objects.
        It returns the parsed result of the referenced xml.

        :param root: Root of the parsing, in case it is needed to resolve references.
        :type root: Portfolio

        :param data: Object to be parsed.
        :type data: dict object

        :return: Parsed object.
        :type: Subclass of PortfolioPerformanceObject
        """
        rslt = None
        if '@reference' in data.keys():
            rslt = cls.parseByReference(parentNode, data['@reference'])
        else:
            rslt = cls.parseContent(data)
            # rslt.parseAttributes()

        return rslt
    
    def copy_from(self, other):
        copy_from(self, other)
    
    def resolveReference(self):
        if self.reference == None:
            return
        combined = combinePaths( self.content['referencePath'], self.reference)
        
        other = Portfolio.currentPortfolio.getObjectByPath(combined)
        if other == None:
            raise RuntimeError(f"Cannot resolve reference [{self.__class__}]: " + str(combined) + " from " + str(self.reference))
        
        self.copy_from(other)
        
from .helpers import *
from .classPortfolio import *