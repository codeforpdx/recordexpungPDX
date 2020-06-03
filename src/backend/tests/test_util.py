from datetime import date

from dateutil.relativedelta import relativedelta
from hypothesis import given
from hypothesis._strategies import dates

from expungeservice.util import DateWithFuture


@given(dates(), dates())
def test_date_with_future_compares_like_date(x: date, y: date):
    x2 = DateWithFuture(x.year, x.month, x.day)
    y2 = DateWithFuture(y.year, y.month, y.day)
    assert (x == y) == (x2 == y2)
    assert (x >= y) == (x2 >= y2)  # type: ignore
    assert (x > y) == (x2 > y2)
    assert (x <= y) == (x2 <= y2)  # type: ignore
    assert (x < y) == (x2 < y2)


@given(dates(), dates(), dates(), dates())
def test_date_with_future_arithmetics_like_date(a: date, b: date, c: date, d: date):
    try:
        r1 = relativedelta(a, b)
        r2 = relativedelta(b, c)
        r3 = relativedelta(c, d)
        d2 = DateWithFuture(d.year, d.month, d.day)
        result = d + r1 - r2 + r3
        assert result == (d2 + r1 - r2 + r3).date
    except (ValueError, OverflowError) as e:
        pass


def test_future_date_is_less_than_max_date():
    assert DateWithFuture.future() < DateWithFuture.max()
    assert DateWithFuture.max() > DateWithFuture.future()
    assert DateWithFuture.future() + relativedelta(days=1) < DateWithFuture.max()
    assert DateWithFuture.future() - relativedelta(days=1) < DateWithFuture.max()


def test_future_date_is_greater_than_any_other_date_but_max():
    assert DateWithFuture.future() > DateWithFuture.max() - relativedelta(days=1)


def test_futures_are_equivalent():
    assert DateWithFuture.future() == DateWithFuture.future()
    assert DateWithFuture.future() + relativedelta(days=2) - relativedelta(
        days=1
    ) == DateWithFuture.future() + relativedelta(days=1)


def test_strftime():
    assert DateWithFuture(2020, 5, 24).strftime("%b %-d, %Y") == "May 24, 2020"
    assert DateWithFuture.future().strftime("%b %-d, %Y") == " from conviction of open case(s)"
