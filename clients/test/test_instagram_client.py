import unittest

from clients.instagram import build_instagram_client_using_env_variables
from commons.model import Location
from commons.resources import DEFAULT_CITIES


class TestInstagramClient(unittest.TestCase):
    """
    To run this test locally, you must have proper environment variables set.
    See build_instagram_client_using_env_variables() definition.
    """

    def setUp(self):
        self.client = build_instagram_client_using_env_variables()

    def test_should_return_200_code_on_tag_request(self):
        media_list = self.client.recent_photos_from(city=DEFAULT_CITIES[0])
        self.assertIsNotNone(media_list)
        self.assertGreaterEqual(len(media_list), 0)

    def test_should_return_200_code_on_location_request(self):
        response = self.client.photos_from(location=Location(51.11, 17.022222))
        actual_response_code = int(response.get("meta").get("code"))
        actual_response_data = response.get("data")
        self.assertEqual(actual_response_code, 200)
        self.assertIsNotNone(actual_response_data)
