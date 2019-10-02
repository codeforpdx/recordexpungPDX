from datetime import date
from dateutil.relativedelta import relativedelta


class Time:

    TWENTY_YEARS_AGO = (date.today() + relativedelta(years=-20)).strftime('%m/%d/%Y')
    LESS_THAN_TWENTY_YEARS_AGO = (date.today() + relativedelta(years=-20, days=+1)).strftime('%m/%d/%Y')
    TEN_YEARS_AGO = (date.today() + relativedelta(years=-10)).strftime('%m/%d/%Y')
    LESS_THAN_TEN_YEARS_AGO = (date.today() + relativedelta(years=-10, days=+1)).strftime('%m/%d/%Y')
    NINE_YEARS_AGO = (date.today() + relativedelta(years=-9)).strftime('%m/%d/%Y')
    SEVEN_YEARS_AGO = (date.today() + relativedelta(years=-7)).strftime('%m/%d/%Y')
    FIVE_YEARS_AGO = (date.today() + relativedelta(years=-5)).strftime('%m/%d/%Y')
    FOUR_YEARS_AGO = (date.today() + relativedelta(years=-4)).strftime('%m/%d/%Y')
    LESS_THAN_THREE_YEARS_AGO = (date.today() + relativedelta(years=-3, days=+1)).strftime('%m/%d/%Y')
    THREE_YEARS_AGO = (date.today() + relativedelta(years=-3)).strftime('%m/%d/%Y')
    TWO_YEARS_AGO = (date.today() + relativedelta(years=-2)).strftime('%m/%d/%Y')
    ONE_YEAR_AGO = (date.today() + relativedelta(years=-1)).strftime('%m/%d/%Y')
    YESTERDAY = (date.today() + relativedelta(days=-1)).strftime('%m/%d/%Y')

    TOMORROW = date.today() + relativedelta(days=+1)
    ONE_YEARS_FROM_NOW = date.today() + relativedelta(years=+1)
    THREE_YEARS = relativedelta(years=3)
    TEN_YEARS = relativedelta(years=10)
