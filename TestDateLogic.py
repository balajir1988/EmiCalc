from DateLogic import DateLogic as dl
from datetime import date, timedelta
from StringConstants import StringConstants as sc
class TestDateLogic:
    def npvComputation(self):
        d1 = date(2023, 1, 1)
        d2 = date(2023, 4, 1)
        period = dl.periodBetween(self, d1, d2, 'Monthly')
        print('period : ', period)
        print('\n')

    def testDates(self):
        d1 = date(2023, 1, 1)
        d2 = date(2023, 3, 31)
        tempPeriod = 1
        while(d2.year < 2024):
            period = dl.periodBetween(self, d1, d2, 'Monthly')
            if(period > tempPeriod):
                print("Date 1 : {}  : date 2 : {} : months : {}".format(d2, d1, period))
            d2 = d2 + timedelta(days=1)
            tempPeriod = period
        print('\n')

    def nextDueDate(self):
        newDate = dl.nextPeriodDate(self, date(2023, 1, 31), 20, "Semi-Monthly", 2)
        print("New Date : ", newDate)
        print('\n')

    def daysBetween(self):
        d1 = date(2024, 1, 1)
        d2 = date(2024, 3, 31)
        dcc = sc.Day_Count_Convention_360
        days = dl.getDaysBetweenTwoDates(self, d1, d2, dcc)
        print("Days : ", days)

if __name__ == "__main__":
    tdl = TestDateLogic()
    tdl.npvComputation()
    tdl.testDates()
    tdl.nextDueDate()
    tdl.daysBetween()