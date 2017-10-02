import unittest

from datetime import date

from clients.sky_scanner import build_sky_scanner_client_from_env_vars


class TestSkyScannerClient(unittest.TestCase):
    """
    To run this test locally, you must have proper environment variables set.
    See build_sky_scanner_client_from_env_vars() definition.
    """

    def setUp(self):
        self.client = build_sky_scanner_client_from_env_vars()

    def test_sky_scanner_client_should_resolve_flights_from_berlin_to_london_with_inbound(self):
        actual_response = self.client.find_flights_for_month("BERL-sky", "LOND-sky", date(2017, 6, 1))
        self.assertIsNotNone(actual_response)
        self.assertGreaterEqual(len(actual_response), 1)
