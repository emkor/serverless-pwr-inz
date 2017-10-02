import unittest
from datetime import datetime
from commons.conversion import parse_date


class TestUberClient(unittest.TestCase):
    def test_should_parse_iso_format_date(self):
        current_date = datetime(year=2017, month=6, day=14, hour=8, minute=15, second=5)
        current_date_str = current_date.isoformat()
        self.assertIsNotNone(current_date_str)

        parsed_date = parse_date(current_date_str)
        self.assertEqual(parsed_date, current_date)
