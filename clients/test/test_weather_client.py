import unittest

from commons.model import Location
from clients.open_weather import build_open_weather_client_using_env_variables


class TestOpenWeatherClient(unittest.TestCase):
    """
    To run this test locally, you must have proper environment variables set.
    See build_open_weather_client_using_env_variables() definition.
    """

    def setUp(self):
        self.client = build_open_weather_client_using_env_variables()
        self.wroclaw_location = Location(51.11, 17.022222)

    def test_retrieving_wroclaw_weather(self):
        forecast = self.client.get_5_days_forecast(self.wroclaw_location)
        self.assertIsNotNone(forecast)
        self.assertGreaterEqual(len(forecast), 30)
