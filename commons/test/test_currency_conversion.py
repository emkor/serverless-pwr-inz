import unittest
from commons.conversion import convert_price
from commons.model import Price

DELTA = 0.01


class TestUberClient(unittest.TestCase):
    def test_should_convert_usd_to_pln(self):
        original_price = Price(value=1.0, currency="USD")
        pln_price = convert_price(original_price, target_currency="PLN")
        expected_pln_value = 3.88
        self.assertAlmostEqual(expected_pln_value, pln_price.value, delta=DELTA)

    def test_should_convert_pln_to_usd(self):
        original_pln_price = Price(value=1.0, currency="PLN")
        usd_price = convert_price(original_pln_price, target_currency="USD")
        expected_usd_value = 0.26
        self.assertAlmostEqual(expected_usd_value, usd_price.value, delta=DELTA)

    def test_should_convert_pln_to_eur(self):
        original_pln_price = Price(value=1.0, currency="PLN")
        actual_eur_price = convert_price(original_pln_price, target_currency="EUR")
        expected_eur_value = 0.24
        self.assertAlmostEqual(expected_eur_value, actual_eur_price.value, delta=DELTA)
