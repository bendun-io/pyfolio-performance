
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