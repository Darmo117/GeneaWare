# https://fr.wikipedia.org/wiki/Concordance_des_dates_des_calendriers_républicain_et_grégorien
from __future__ import annotations

import functools
import math
import typing as typ


@functools.total_ordering
class Date:
    """
    This class represents a date as a day in a month, a month ans a year.

    Dates can be partial, that is up to 2 values can be omitted. You can represent dates such as
    """
    EXACT = 0
    BEFORE = 1
    AFTER = 2
    APPROX = 3
    PRECISIONS = {EXACT: '', BEFORE: '<', AFTER: '>', APPROX: '~'}

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def __init__(self, day: int = None, month: int = None, year: int = None, precision: int = EXACT):
        if day is None and month is None and year is None:
            raise ValueError('at least 1 value must be set')
        if precision not in self.PRECISIONS:
            raise ValueError(f'invalid precision mode <{precision}>')
        self.__day = day
        self.__month = month
        self.__year = year
        self.__check_date()
        self.__precision = precision

    def __check_date(self):
        if self.__month is not None:
            if not (1 <= self.__month <= 12):
                raise ValueError(f'month not between 1 and 12')
            if self.__day is not None:
                month_has_30_days = self.__month in [Date.APRIL, Date.JUNE, Date.SEPTEMBER, Date.NOVEMBER]
                if self.__year is not None:
                    allow_29_feb = self.is_leap_year
                else:
                    allow_29_feb = True  # We don't know but it could be a leap year.
                if self.__day > 30 and month_has_30_days or self.__day > 31 or self.__day > 29 and \
                        self.__month == self.FEBRUARY or self.__day == 29 and not allow_29_feb:
                    raise ValueError(f'invalid day <{self.__day}>')
        if self.__day is not None and not (1 <= self.__day <= 31):
            raise ValueError(f'invalid day <{self.__day}>')

    @staticmethod
    def get_days_in_month(month: int, year: int):
        if not (1 <= month <= 12):
            raise AssertionError('month must be between 1 and 12')
        if month in [Date.APRIL, Date.JUNE, Date.SEPTEMBER, Date.NOVEMBER]:
            return 30
        if month == Date.FEBRUARY:
            return 29 if Date.is_leap_year_(year) else 28
        return 31

    @staticmethod
    def is_leap_year_(year: int):  # TODO trouver un autre nom
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    @property
    def is_leap_year(self):
        return self.is_leap_year_(self.year)

    @property
    def day_set(self):
        return self.__day is not None

    @property
    def day(self):
        if not self.day_set:
            raise AssertionError('no day set')
        return self.__day

    @property
    def month_set(self):
        return self.__month is not None

    @property
    def month(self):
        if not self.month_set:
            raise AssertionError('no month set')
        return self.__month

    @property
    def year_set(self):
        return self.__year is not None

    @property
    def year(self):
        if not self.year_set:
            raise AssertionError('no year set')
        return self.__year

    @property
    def precision(self):
        return self.__precision

    # TODO voir les cas selon la précision ; n'a pas de sens si les dates sont BEFORE ou AFTER et se chevauchent
    def __gt__(self, other: Date):
        pass

    def __eq__(self, other: Date):  # TODO prise en compte de la précision ?
        if self.year_set and other.year_set:
            if self.month_set and other.month_set:
                if self.day_set and other.day_set:
                    return self.year == other.year and self.month == other.month and self.day == other.day
                elif not self.day_set and not other.day_set:
                    return self.year == other.year and self.month == other.month
            elif not self.month_set and not other.month_set:
                if self.day_set and other.day_set:
                    return self.year == other.year and self.day == other.day
                elif not self.day_set and not other.day_set:
                    return self.year == other.year
        elif not self.year_set and not other.year_set:
            if self.month_set and other.month_set:
                if self.day_set and other.day_set:
                    return self.month == other.month and self.day == other.day
                elif not self.day_set and not other.day_set:
                    return self.month == other.month
            elif not self.month_set and not other.month_set:
                if self.day_set and other.day_set:
                    return self.day == other.day
                elif not self.day_set and not other.day_set:
                    raise AssertionError('empty dates')

        return False

    def __compare_to(self, other: Date):
        if self.year_set and other.year_set:
            if not self.month_set or not other.month_set:
                if self.year < other.year:
                    return -1
                if self.year > other.year:
                    return 1
                return 0

            if not self.day_set or not other.day_set:
                if self.year < other.year or self.year == other.year and self.month < other.month:
                    return -1
                if self.year > other.year or self.year == other.year and self.month > other.month:
                    return 1
                return 0

            if self.year < other.year or self.year == other.year and self.month < other.month \
                    or self.year == other.year and self.month == other.month and self.day < other.day:
                return -1
            if self.year > other.year or self.year == other.year and self.month > other.month \
                    or self.year == other.year and self.month == other.month and self.day > other.day:
                return 1
            return 0
        elif not self.year_set and not other.year_set and self.month_set and other.month_set:
            if not self.day_set or not other.day_set:
                if self.month < other.month:
                    return -1
                if self.month > other.month:
                    return 1
                return 0

            if self.month < other.month or self.month == other.month and self.day < other.day:
                return -1
            if self.month > other.month or self.month == other.month and self.day > other.day:
                return 1
            return 0
        elif not self.year_set and not other.year_set and not self.month_set and not other.month_set \
                and self.day_set and other.day_set:
            if self.day < other.day:
                return -1
            if self.day > other.day:
                return 1
            return 0

        return 0

    def __add__(self, timespan: TimePeriod):
        if self.year_set:
            year = self.year + timespan.years
            if self.month_set:
                month, years_to_add = self.wrap_month(self.month + timespan.months)
                year += years_to_add
                if self.day_set:
                    # Update day based on month before adding new days
                    days_in_month = self.get_days_in_month(month, year)
                    day = min(self.day, days_in_month)  # Truncate days to end of month
                    day, month, year = self.__wrap_date(day + timespan.days, month, year)
                    return Date(day=day, month=month, year=year, precision=self.precision)
                else:
                    return Date(month=month, year=year, precision=self.precision)
            else:
                return Date(year=year, precision=self.precision)
        raise ValueError("can't add a time period to a date without a year")

    def __sub__(self, other: typ.Union[Date, TimePeriod]) -> typ.Union[Date, TimePeriod]:
        """
        Subtracts a TimePeriod or another Date from this Date.

        :param other: The Date or TimePeriod to subtract
        :return: A Date if the argument is a TimePeriod or a TimePeriod if the argument is a Date.
        """
        if type(other) == TimePeriod:
            return self + -other

        if self.precision not in [self.EXACT, self.APPROX] or other.precision not in [self.EXACT, self.APPROX]:
            raise ValueError("can only subtract exact or approx dates")

        if self.year_set and other.year_set:
            years = self.year - other.year
            if not self.month_set or not other.month_set:
                return TimePeriod(years=years)
            else:
                months = self.month - other.month
                if not self.day_set or not other.day_set:
                    return TimePeriod(months=months, years=years)
                else:
                    return TimePeriod(days=self.day - other.day, months=months, years=years)
        raise ValueError('missing year')

    @staticmethod
    def wrap_month(month) -> (int, int):
        """
        Wraps a month within the year.
        :param month: The month.
        :return: The new month and the value to add to the year.
        """
        if not (1 <= month <= 12):
            return ((month - 1) % 12) + 1, (month - 1) // 12
        return month, 0

    @staticmethod
    def __wrap_date(day, month, year) -> (int, int, int):
        """
        Wraps a date.
        :param day: The day.
        :param month: The month.
        :param year: The year.
        :return: The new day, the new month and the new year.
        """
        while 'Days not wrapped':
            days_in_month = Date.get_days_in_month(month, year)
            if day > days_in_month:
                day -= days_in_month
                month, year_add = Date.wrap_month(month + 1)
                year += year_add
            elif day < 1:
                month, year_add = Date.wrap_month(month - 1)
                day += Date.get_days_in_month(month, year)
                year += year_add
            else:
                return day, month, year

    def __repr__(self):
        """Returns the representation of this date as 'DD/MM/YYYY'. Any missing value will be replaced by '?'."""
        day = self.day if self.day_set else '??'
        month = self.month if self.month_set else '??'
        year = self.year if self.year_set else '????'
        return f'{self.PRECISIONS[self.precision]} {str(day).rjust(2, "0")}/{str(month).rjust(2, "0")}/{year}'.strip()


class TimePeriod:
    """
    This class represents a time period.
    The duration can be expressed as years, months or days.
    """

    def __init__(self, days: int = 0, months: int = 0, years: int = 0):
        self.__days = days
        self.__months = (abs(months) % 12) * int(math.copysign(1, months))
        self.__years = years + months // 12 + (0 if months >= 0 or months % 12 == 0 else 1)
        # noinspection PyChainedComparisons
        if self.__months < 0 and self.__years > 0:
            self.__months += 12
            self.__years -= 1
        elif self.__months > 0 and self.__years < 0:
            self.__months -= 12
            self.__years += 1

    @property
    def days(self):
        return self.__days

    @property
    def months(self):
        return self.__months

    @property
    def years(self):
        return self.__years

    def __neg__(self):
        return TimePeriod(days=-self.days, months=-self.months, years=-self.years)

    def __eq__(self, other: TimePeriod):
        return self.days == other.days and self.months == other.months and self.years == other.years

    def __repr__(self):
        return f'{self.years} year{"s" if self.years != 1 else ""}, ' \
            f'{self.months} month{"s" if self.months != 1 else ""}, ' \
            f'{self.days} day{"s" if self.days != 1 else ""}'
