from datetime import date
from dateutil.relativedelta import relativedelta


class Time:

    MORE_THAN_TWENTY_YEARS_AGO = date.today() + relativedelta(years=-20, days=-1)
    TWENTY_YEARS_AGO = date.today() + relativedelta(years=-20)
    LESS_THAN_TWENTY_YEARS_AGO = date.today() + relativedelta(years=-20, days=+1)
    TEN_YEARS_AGO = date.today() + relativedelta(years=-10)
    LESS_THAN_TEN_YEARS_AGO = date.today() + relativedelta(years=-10, days=+1)
    NINE_YEARS_AGO = date.today() + relativedelta(years=-9)
    SEVEN_YEARS_AGO = date.today() + relativedelta(years=-7)
    FIVE_YEARS_AGO = date.today() + relativedelta(years=-5)
    FOUR_YEARS_AGO = date.today() + relativedelta(years=-4)
    LESS_THAN_THREE_YEARS_AGO = date.today() + relativedelta(years=-3, days=+1)
    THREE_YEARS_AGO = date.today() + relativedelta(years=-3)
    TWO_YEARS_AGO = date.today() + relativedelta(years=-2)
    ONE_YEAR_AGO = date.today() + relativedelta(years=-1)
    YESTERDAY = date.today() + relativedelta(days=-1)

    TOMORROW = date.today() + relativedelta(days=+1)
    ONE_YEARS_FROM_NOW = date.today() + relativedelta(years=+1)
    THREE_YEARS = relativedelta(years=3)
    TEN_YEARS = relativedelta(years=10)
