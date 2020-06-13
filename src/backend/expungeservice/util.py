import collections
from datetime import date as date_class, datetime
from functools import total_ordering

from dateutil.relativedelta import relativedelta


# Adapted from https://www.kunxi.org/2014/05/lru-cache-in-python/
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache: collections.OrderedDict = collections.OrderedDict()

    def __getitem__(self, key):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return None

    def __setitem__(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value


# Conceptually if date.max is infinity, then DateWithFuture.future() is "right before" infinity.
# In practice, date.max is year 9999 and DateWithFuture.future() is year 5000 -
# we then manipulate the comparison operators to make DateWithFuture.future() behave
# as though date.max - epsilon < DateWithFuture.future() < date.max.
@total_ordering
class DateWithFuture:
    FUTURE = date_class(5000, 1, 1)

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 3:
            self.date = date_class(*args)
            self.relative = relativedelta()
        else:
            self.date = kwargs["date"]
            self.relative = kwargs["relative"] if kwargs.get("relative") else relativedelta()

    @staticmethod
    def future():
        return DateWithFuture(date=DateWithFuture.FUTURE, relative=relativedelta(days=1))

    @staticmethod
    def fromtimestamp(t):
        return DateWithFuture(date=date_class.fromtimestamp(t))

    @staticmethod
    def today():
        return DateWithFuture(date=date_class.today())

    @staticmethod
    def fromordinal(n):
        return DateWithFuture(date=date_class.fromordinal(n))

    @staticmethod
    def fromdatetime(d):
        return DateWithFuture(date=datetime.date(d))

    @staticmethod
    def max():
        return DateWithFuture(9999, 12, 31)

    @staticmethod
    def min():
        return DateWithFuture(1, 1, 1)

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    @property
    def day(self):
        return self.date.day

    def strftime(self, fmt):
        if self.relative:
            years = f"{self.relative.years} year(s) " if self.relative.years else ""
            months = f"{self.relative.months} month(s) " if self.relative.months else ""
            days = f"{self.relative.days - 1} day(s) " if self.relative.days - 1 > 0 else ""
            return years + months + days + " From Conviction Of Open Charge"
        else:
            return self.date.strftime(fmt)

    def __add__(self, other):
        if isinstance(other, relativedelta):
            if self.relative:
                return DateWithFuture(date=DateWithFuture.FUTURE, relative=self.relative + other)
            else:
                return DateWithFuture(date=self.date + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, relativedelta):
            if self.relative:
                return DateWithFuture(date=DateWithFuture.FUTURE, relative=self.relative - other)
            else:
                return DateWithFuture(date=self.date - other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, DateWithFuture):
            if self.date == other.date:
                today = date_class.today()
                return today + self.relative == today + other.relative
            else:
                return self.date == other.date
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, DateWithFuture):
            if self.date == other.date == DateWithFuture.FUTURE:
                today = date_class.today()
                return today + self.relative < today + other.relative
            elif self.date == DateWithFuture.FUTURE:
                return other.date == date_class.max
            elif other.date == DateWithFuture.FUTURE:
                return self.date != date_class.max
            else:
                return self.date < other.date
        return NotImplemented

    def __repr__(self):
        return f"DateWithFuture(date={repr(self.date)}, relative={repr(self.relative)})"

    def __hash__(self):
        return hash((self.date, self.relative))
