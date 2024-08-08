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
    
    def securityPatternMatch(match):
        from .classSecurity import Security
        return Security.getSecurityByNum(int(match.group(2)))

    referencePatterns = {
        re.compile(r"(\.\./)*securities/security\[(\d+)\]$"): securityPatternMatch 
    }
    
    @classmethod
    def parseByReference(cls, root, reference):
        """
        This methods resolves the attribute referenced.
        It returns the parsed result of the referenced xml.

        :param root: Root of the parsing, in case it is needed to resolve references.
        :type root: Portfolio

        :param reference: Encoding of the reference
        :type reference: str

        :return: Parsed object.
        :type: Subclass of PortfolioPerformanceObject
        """
        for pattern in PortfolioPerformanceObject.referencePatterns.keys():
            match = pattern.search(reference)
            if match:
                return PortfolioPerformanceObject.referencePatterns[pattern](match)
        
        rslt = None

        # Example:       
        # "@reference": "../../accounts/account/transactions/account-transaction[2]/crossEntry/portfolio/transactions/portfolio-transaction[40]/crossEntry/account/transactions/account-transaction[11]/crossEntry/portfolio"
        # reference.replace("../", "")
        steps = reference.split("/")
        
        position = root #.content['client']
        num = 0
        try:
            for step in steps:
                if step == "..":
                    continue
                match = arrayRegex.search(step)
                if match:
                    index = int(match.group(1))
                    position = position[step.split("[")[0]]
                    position = position[index]
                else:
                    try:
                        position = position[step]
                    except:
                        position = position[0][step]
                num += 1
        except Exception as e:
            if step == "crossEntry":
                print("NOT YET IMPLEMENTED CrossEntry")
                return None
            print()
            print("Position: " + str(position))
            print("Error in resolving reference: " + str(reference) + " at " + str(step))
            print("Type: " + str(type(position)))
            print("Keys: "  + str(position.keys()))
            print("Num: " + str(num))
            print()
            exit(-1)

        rslt = cls.parse(root, position)

        return rslt

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