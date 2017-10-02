import unittest

from commons.model import Location
from clients.uber import build_uber_client_using_env_variables


class TestUberClient(unittest.TestCase):
    """
    To run this test locally, you must have proper environment variables set.
    See build_uber_client_using_env_variables() definition.
    """

    def setUp(self):
        self.uber_client = build_uber_client_using_env_variables()

    def test_wroclaw_products_should_be_available(self):
        wroclaw_location = Location(51.11, 17.022222)
        actual_response = self.uber_client.get_available_products(wroclaw_location)
        self.assertIsNotNone(actual_response)
        self.assertEqual(len(actual_response), 2)

    def test_should_estimate_wroclaw_pricing(self):
        wroclaw_location_a = Location(51.11801979999999, 17.04196479999996)
        wroclaw_location_b = Location(51.0987672, 17.036518600000022)
        actual_response = self.uber_client.estimate_price(wroclaw_location_a, wroclaw_location_b)
        self.assertIsNotNone(actual_response)
        self.assertEqual(len(actual_response), 2)
