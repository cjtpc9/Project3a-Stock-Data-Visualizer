import unittest
from datetime import datetime


def validate_symbol(symbol):
    return (
        symbol.isalpha()
        and symbol.isupper()
        and 1 <= len(symbol) <= 7
    )


def validate_chart_type(chart_type):
    return (
        len(chart_type) == 1
        and chart_type.isdigit()
        and chart_type in ["1", "2"]
    )


def validate_time_series(time_series):
    return (
        len(time_series) == 1
        and time_series.isdigit()
        and time_series in ["1", "2", "3", "4"]
    )


def validate_date(date_value):
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class TestProject3Inputs(unittest.TestCase):

    def test_symbol(self):
        self.assertTrue(validate_symbol("AAPL"))
        self.assertTrue(validate_symbol("IBM"))
        self.assertFalse(validate_symbol("aapl"))
        self.assertFalse(validate_symbol("AAPL1"))
        self.assertFalse(validate_symbol(""))
        self.assertFalse(validate_symbol("ABCDEFGH"))

    def test_chart_type(self):
        self.assertTrue(validate_chart_type("1"))
        self.assertTrue(validate_chart_type("2"))
        self.assertFalse(validate_chart_type("0"))
        self.assertFalse(validate_chart_type("3"))
        self.assertFalse(validate_chart_type("12"))
        self.assertFalse(validate_chart_type("A"))

    def test_time_series(self):
        self.assertTrue(validate_time_series("1"))
        self.assertTrue(validate_time_series("2"))
        self.assertTrue(validate_time_series("3"))
        self.assertTrue(validate_time_series("4"))
        self.assertFalse(validate_time_series("0"))
        self.assertFalse(validate_time_series("5"))
        self.assertFalse(validate_time_series("12"))
        self.assertFalse(validate_time_series("A"))

    def test_start_date(self):
        self.assertTrue(validate_date("2026-11-17"))
        self.assertTrue(validate_date("2026-01-01"))
        self.assertFalse(validate_date("11-17-2026"))
        self.assertFalse(validate_date("2026/11/17"))
        self.assertFalse(validate_date("2026-13-01"))
        self.assertFalse(validate_date("2026-02-30"))

    def test_end_date(self):
        self.assertTrue(validate_date("2026-11-21"))
        self.assertTrue(validate_date("2026-12-31"))
        self.assertFalse(validate_date("11-21-2026"))
        self.assertFalse(validate_date("2026/11/21"))
        self.assertFalse(validate_date("2026-00-10"))
        self.assertFalse(validate_date("not-a-date"))


if __name__ == "__main__":
    unittest.main()