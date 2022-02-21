class DateObject:

    def __init__(self,dateStr):
        self.date = dateStr

    def getYear(self):
        return int(self.date[:4])

    def getMonth(self):
        return int(self.date[5:7])

    def getDay(self):
        return int(self.date[8:10])
    
    def getOrderValue(self):
        return self.getDay() + 31*(self.getMonth()-1) + 31*12*(self.getYear())

    def __repr__(self) -> str:
        return "%d-%d-%d" % (self.getYear, self.getMonth, self.getDay)