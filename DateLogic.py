from StringConstants import StringConstants as sc
from datetime import timedelta, date
from dateutil import relativedelta as rd
from calendar import monthrange
import math
class DateLogic:
    """
    Method to find the number of periods between two dates
    :param startDate : Period start date
    :param endDate : Period end date
    :param periodCode : Period code (Weekly, Bi-Weekly, Semi-Monthly, Monthly, Quarterly, Semi-Annual, Annual)
    return period : number of periods
    """
    def periodBetween(self, startDate, endDate, periodCode):
        period = 0
        if startDate == endDate:
            return period
        if startDate > endDate:
            tempDate = endDate
            startDate = endDate
            endDate = tempDate

        # Precomputing number of months between 2 dates
        noOfMonths = (endDate.year - startDate.year) * 12 + (endDate.month - startDate.month)

        if periodCode.lower() == sc.Frequency_Weekly.lower():
            period = math.floor((endDate-startDate).days/7)
        elif periodCode.lower() == sc.Frequency_Bi_Weekly.lower():
            period = math.floor((endDate-startDate).days/14)
        elif periodCode.lower() == sc.Frequency_Semi_Monthly.lower():
            period = math.floor((endDate - startDate).days/15)
        elif periodCode.lower() == sc.Frequency_Monthly.lower():
            period = noOfMonths
        elif periodCode.lower() == sc.Frequency_Bi_Monthly.lower():
            period = math.floor(noOfMonths / 2)
        elif periodCode.lower() == sc.Frequency_Quarterly.lower():
            period = math.floor(noOfMonths/3)
        elif periodCode.lower() == sc.Frequency_Semi_Annual.lower():
            period = math.floor(noOfMonths/6)
        elif periodCode.lower() == sc.Frequency_Annual.lower():
            period = math.floor(noOfMonths/12)
        return period

    """
    Method to find the next payment due date
    :param givenDate : Current due date
    :param dueDay : Day of current due date
    :param frequency : Frequency code (Weekly, Bi-Weekly, Semi-Monthly, Monthly, Quarterly, Semi-Annual, Annual)
    :param period : number of periods
    return nextDueDate : returns the next due day
    """
    def nextPeriodDate(self, givenDate, dueDay, frequency, period):
        nextDueDate = givenDate
        if frequency.lower() == sc.Frequency_Weekly.lower():
            nextDueDate = givenDate + timedelta(days=(period*7))
        elif frequency.lower() == sc.Frequency_Bi_Weekly.lower():
            nextDueDate = givenDate + timedelta(days=(period*14))
        elif frequency.lower() == sc.Frequency_Semi_Monthly.lower():
            nextDueDate = DateLogic.deriveSemiMonthlyDueDate(givenDate, dueDay, period)
        elif frequency.lower() == sc.Frequency_Monthly.lower():
            nextDueDate = DateLogic.addPeriodToGivenDate(givenDate, dueDay, period)
        elif frequency.lower() == sc.Frequency_Bi_Monthly.lower():
            nextDueDate = DateLogic.addPeriodToGivenDate(givenDate, dueDay, period*2)
        elif frequency.lower() == sc.Frequency_Quarterly.lower():
            nextDueDate = DateLogic.addPeriodToGivenDate(givenDate, dueDay, period*3)
        elif frequency.lower() == sc.Frequency_Semi_Annual.lower():
            nextDueDate = DateLogic.addPeriodToGivenDate(givenDate, dueDay, period*6)
        elif frequency.lower() == sc.Frequency_Annual.lower():
            nextDueDate = DateLogic.addPeriodToGivenDate(givenDate, dueDay, period*12)
        return nextDueDate

    """
    Find number of days between two dates based the day counting method
    :param startDate : Period start date
    :param endDate : Period end date
    :param dayCountConvention : 
    return nextDueDate : returns the next due day
    """
    def getDaysBetweenTwoDates(self, startDate, endDate, dayCountConvention):
        daysBetween = 0
        if(startDate > endDate):
            tempDate = endDate
            startDate = endDate
            endDate = tempDate

        if(dayCountConvention == sc.Day_Count_Convention_366):
            daysBetween = (endDate - startDate).days
        elif(dayCountConvention == sc.Day_Count_Convention_365):
            daysBetween = (endDate - startDate).days
            # need to remove days depends on how many leap year are there in between the given dates
            startDate = startDate + rd.relativedelta(days=1)
            while(startDate < endDate):
                if(startDate.month == 2 and startDate.day == 29):
                    daysBetween = daysBetween -1
                if(startDate.month > 2):
                    startDate = date(startDate.year+1, 2, 28)
                startDate = startDate + rd.relativedelta(days=1)
        else:
            startDay = startDate.day
            endDay = endDate.day
            startDateLeapCheckDay = monthrange(startDate.year, startDate.month)[1]
            endDateLeapCheckDay = monthrange(endDate.year, endDate.month)[1]
            isStartDateFeb = False
            if(startDay == 31):
                startDay = 30
            if(endDay == 31 and (startDay == 30 or startDay == 31)):
                endDay = 30
            if(startDate.month == 2 and (startDateLeapCheckDay == 28 or startDateLeapCheckDay == 29)):
                startDay = 30
                isStartDateFeb = True
            if(isStartDateFeb and endDate.month == 2 and (endDateLeapCheckDay == 28 or endDateLeapCheckDay == 29)):
                endDay = 30
            years = endDate.year - startDate.year
            months = endDate.month - startDate.month
            days = endDay - startDay

            daysBetween = years * 360 + months * 30 + days

        return daysBetween

    """
    Internal method to add number of days to given due date to find next due date
    :param givenDate : Current due date
    :param dueDay : Day of current due date
    :param period : number of periods
    return nextDueDate : returns the next due day
    """
    @staticmethod
    def addPeriodToGivenDate(givenDate, dueDay, period):
        computedDate = givenDate + rd.relativedelta(months=period)
        computedDueDay = dueDay
        if(monthrange(computedDate.year, computedDate.month)[1] < dueDay):
            computedDueDay = monthrange(computedDate.year, computedDate.month)[1]
        computedDate = date(computedDate.year, computedDate.month, computedDueDay)
        return computedDate

    """
    Internal method to find next due date based on given due date but the logic is different in case of semi monthly.
    So we are handling it as a special case
    :param givenDate : Current due date
    :param dueDay : Day of current due date
    :param period : number of periods
    return nextDueDate : returns the next due day
    """
    @staticmethod
    def deriveSemiMonthlyDueDate(givenDate, dueDay, period):
        computedDate = givenDate
        computedDueDay = 30
        incrementor = 1
        if(period < 0):
            incrementor = -1
        if(givenDate.day < 30):
            computedDueDay = givenDate.day
        counter = 0
        if(givenDate.month == 2 and (givenDate+rd.relativedelta(days=1)).month > givenDate.month):
            if(dueDay >= 30 or dueDay == 15):
                computedDueDay = 30
            elif(dueDay == 14):
                computedDueDay = 29
        while(counter != period):
            month = 0
            if(computedDueDay > 15):
                computedDueDay = computedDueDay - 15
                if(incrementor > 0):
                    month = 1
            else:
                computedDueDay = computedDueDay + 15
                if(incrementor < 0):
                    month = -1
            computedDate = DateLogic.addPeriodToGivenDate(computedDate, computedDueDay, month)
            counter = counter + incrementor
        return computedDate