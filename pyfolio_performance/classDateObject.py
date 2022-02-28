class DateObject:
    """
    Represents a data of a transaction.
    
    :param dateStr: Date string as used by portfolio performance in the XML.
    """

    def __init__(self,dateStr):
        self.date = dateStr

    def getYear(self):
        """
        :return: Returns the year of the date.
        :type: int
        """
        return int(self.date[:4])

    def getMonth(self):
        """
        :return: Returns the month of the date.
        :type: int
        """
        return int(self.date[5:7])

    def getDay(self):
        """
        :return: Returns the day in the month of the date.
        :type: int
        """
        return int(self.date[8:10])
    
    def getOrderValue(self):
        """
        Used to order dates. Gives a comparable int s.t. `getOrderValue(a) < getOrderValue(b)` iff the date `a` was before the date `b`.
        :return: Returns an int representing the position in an order of the date.
        :type: int
        """
        return self.getDay() + 31*(self.getMonth()-1) + 31*12*(self.getYear())

    def __repr__(self) -> str:
        """
        :return: Returns the date string the same way portfolio performance uses it in the XML.
        :type: str
        """
        return "%d-%d-%d" % (self.getYear, self.getMonth, self.getDay)