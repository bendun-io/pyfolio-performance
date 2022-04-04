from .classDepotTransaction import DepotTransaction

class Filters:
    """
    Class that provides usefull filtering functions for the cluster analysis.
    """

    @staticmethod
    def fEnsureTypeList(typelist):
        """
        :param typelist: List of types that are required by the filter.
        :type typelist: list(str)

        :return: A filter function that ensures the entry has a type contained in the typelist.
        :type: Entry -> bool
        """
        return lambda x: True if x.type in typelist else False

    @staticmethod
    def fExcludeTypeList(typelist):
        """
        :param typelist: List of types that are not allowed by the filter.
        :type typelist: list(str)

        :return: A filter function that ensures the entry has `not` a type contained in the typelist.
        :type: Entry -> bool
        """
        return lambda x: False if x.type in typelist else True

    @staticmethod
    def fDepotTransaction():
        """
        :return: A filter function that ensures the entry is a Depot Transaction.
        :type: Entry -> bool
        """
        return lambda x: False if not isinstance(x, DepotTransaction) else True

    @staticmethod
    def fSecurityTransaction(sec):
        """
        :param sec: A security to filter for.
        :type sec: Security

        :return: A filter function that ensures the entry is a transaction about the given security.
        :type: Entry -> bool
        """
        return lambda x: False if x.getSecurity() != sec else True

    @staticmethod
    def fBefore(date):
        """
        :param year: The date to filter for.
        :type year: DateObject

        :return: A filter function that ensures the entry was made before or on the date (<=).
        :type: Entry -> bool
        """
        return lambda x: True if (x.getYear()<date.getYear()) or \
            (x.getYear()==date.getYear() and x.getMonth()<date.getMonth()) or \
            (x.getYear()==date.getYear() and x.getMonth()==date.getMonth() and x.getDay()<=date.getDay()) else False

    @staticmethod
    def fYear(year):
        """
        :param year: The year to filter for.
        :type year: int

        :return: A filter function that ensures the entry was made in the specified year.
        :type: Entry -> bool
        """
        return lambda x: True if x.getYear()==year else False

    @staticmethod
    def fMonth(month):
        """
        :param month: The month to filter for.
        :type month: int

        :return: A filter function that ensures the entry was made in the specified month.
        :type: Entry -> bool
        """
        return lambda x: True if x.getMonth()==month else False

    @staticmethod
    def fDay(day):
        """
        :param day: The day to filter for.
        :type day: int

        :return: A filter function that ensures the entry was made in the specified day.
        :type: Entry -> bool
        """
        return lambda x: True if x.getDay()==day else False

    @staticmethod
    def fAnd(f1,f2):
        """
        :param f1: First function.
        :type: function entry -> bool

        :param f2: Second function.
        :type: function entry -> bool

        :return: Returns a function that first evaluates both functions and returns the `and`.
        :type: Entry -> bool
        """
        return lambda x: f1(x) and f2(x)

    @staticmethod
    def fOr(f1,f2):
        """
        :param f1: First function.
        :type: function entry -> bool

        :param f2: Second function.
        :type: function entry -> bool

        :return: Returns a function that first evaluates both functions and returns the `or`.
        :type: Entry -> bool
        """
        return lambda x: f1(x) or f2(x)

