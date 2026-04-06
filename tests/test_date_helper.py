import pytest
from Helpers.DateHelper import DateHelper


@pytest.fixture
def helper():
    return DateHelper()


class TestReformatDate:
    def test_us_long_format(self, helper):
        assert helper.reformat_date("January 20, 2020") == "2020-01-20"

    def test_us_short_format(self, helper):
        assert helper.reformat_date("Jan 20, 2020") == "2020-01-20"

    def test_day_month_year_long(self, helper):
        assert helper.reformat_date("20 January 2020") == "2020-01-20"

    def test_day_month_year_short(self, helper):
        assert helper.reformat_date("20 Jan 2020") == "2020-01-20"

    def test_parenthesized_iso_format(self, helper):
        assert helper.reformat_date("(2020-01-20)") == "2020-01-20"

    def test_year_only(self, helper):
        assert helper.reformat_date("2020") == "2020-01-01"

    def test_airdate_stripped(self, helper):
        assert helper.reformat_date("January 20, 2020 (airdate)") == "2020-01-20"

    def test_invalid_returns_none(self, helper):
        assert helper.reformat_date("not a date") is None


class TestAddYearsToDate:
    def test_add_one_year(self, helper):
        assert helper.add_years_to_date("2000-06-15", 1) == "2001-06-15"

    def test_add_many_years(self, helper):
        assert helper.add_years_to_date("1985-03-01", 38) == "2023-03-01"

    def test_leap_year(self, helper):
        # Feb 29 + 1 year should land on Feb 28
        assert helper.add_years_to_date("2000-02-29", 1) == "2001-02-28"
