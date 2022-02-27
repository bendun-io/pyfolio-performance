
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